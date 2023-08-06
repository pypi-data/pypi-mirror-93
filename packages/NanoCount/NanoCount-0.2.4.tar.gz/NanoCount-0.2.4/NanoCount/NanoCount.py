#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~#
# Standard library imports
from collections import *

# Third party imports
import pysam
import pandas as pd
from tqdm import tqdm

# Local imports
from NanoCount.Read import Read
from NanoCount.common import *

#~~~~~~~~~~~~~~MAIN FUNCTION~~~~~~~~~~~~~~#
class NanoCount ():

    #~~~~~~~~~~~~~~MAGIC METHODS~~~~~~~~~~~~~~#
    def __init__ (self,
        alignment_file:str,
        count_file:str="",
        min_read_length:int = 50,
        discard_suplementary:bool = False,
        min_query_fraction_aligned:float = 0.5,
        equivalent_threshold:float = 0.9,
        scoring_value:str = "alignment_score",
        convergence_target:float = 0.005,
        max_em_rounds:int = 100,
        extra_tx_info:bool = False,
        primary_score:str = "primary",
        max_dist_3_prime:int = 100,
        max_dist_5_prime:int = -1,
        verbose:bool = False,
        quiet:bool = False):
        """
        Estimate abundance of transcripts using an EM
        * alignment_file
            BAM or SAM file containing aligned ONT dRNA-Seq reads including secondary and supplementary alignment
        * count_file
            Output file path where to write estimated counts (TSV format)
        * min_read_length
            Minimal length of the read to be considered valid
        * min_query_fraction_aligned
            Minimal fraction of the primary alignment query aligned to consider the read valid
        * equivalent_threshold
            Fraction of the alignment score or the alignment length of secondary alignments compared to the primary alignment to be considered valid
            alignments
        * scoring_value
            Value to use for score thresholding of secondary alignments either "alignment_score" or "alignment_length"
        * convergence_target
            Convergence target value of the cummulative difference between abundance values of successive EM round to trigger the end of the EM loop.
        * max_em_rounds
            Maximum number of EM rounds before triggering stop
        * extra_tx_info
            Add transcripts length and zero coverage transcripts to the output file (required valid bam/sam header)
        * primary_score
            Method to pick the best alignment for each read. By default ("primary") it uses the primary read defined by the aligner but it can be changed to
            use either the best alignment score ("align_score") or the best alignment length ("align_len"). choices = [primary, align_score, align_len]
        * discard_suplementary
            Discard any supplementary alignment. Otherwise they are considered like secondary alignments
        * max_dist_3_prime
            Maximum distance of alignment end to 3 prime of transcript. In ONT dRNA-Seq reads are assumed to start from the polyA tail (-1 to deactivate)
        * max_dist_5_prime
            Maximum distance of alignment start to 5 prime of transcript. In conjunction with max_dist_3_prime it can be used to select near full lenght reads
            only (-1 to deactivate).
        * verbose
            Increase verbosity for QC and debugging
        * quiet
            Reduce verbosity
        """

        # Init package
        opt_summary_dict = opt_summary(local_opt=locals())
        self.log = get_logger (name="Nanocount", verbose=verbose, quiet=quiet)

        self.log.warning("Checking options and input files")
        log_dict(opt_summary_dict, self.log.debug, "Options summary")

        # Save args in self variables
        self.alignment_file = alignment_file
        self.count_file = count_file
        self.min_read_length = min_read_length
        self.min_query_fraction_aligned = min_query_fraction_aligned
        self.equivalent_threshold = equivalent_threshold
        self.scoring_value = scoring_value
        self.convergence_target = convergence_target
        self.max_em_rounds = max_em_rounds
        self.extra_tx_info = extra_tx_info
        self.primary_score = primary_score
        self.discard_suplementary = discard_suplementary
        self.max_dist_5_prime = max_dist_5_prime
        self.max_dist_3_prime = max_dist_3_prime

        self.log.warning("Initialise Nanocount")

        # Collect all alignments grouped by read name
        self.log.info ("Parse Bam file and filter low quality alignments")
        self.read_dict = self._parse_bam()

        # Generate compatibility dict grouped by reads
        self.log.info ("Generate initial read/transcript compatibility index")
        self.compatibility_dict = self._get_compatibility()

        # EM loop to calculate abundance and update read-transcript compatibility
        self.log.warning ("Start EM abundance estimate")

        self.em_round = 0
        self.convergence = 1

        with tqdm (unit=" rounds", unit_scale=True, desc="\tProgress", disable=(quiet or verbose)) as pbar:
            # Iterate until convergence threshold or max EM round are reached
            while self.convergence > self.convergence_target and self.em_round < self.max_em_rounds:
                self.em_round += 1
                # Calculate abundance from compatibility assignments
                self.abundance_dict = self._calculate_abundance()
                # Update compatibility assignments
                self.compatibility_dict = self._update_compatibility()
                # Update counter
                pbar.update(1)
                self.log.debug ("EM Round: {} / Convergence value: {}".format(self.em_round, self.convergence))

        self.log.info ("Exit EM loop after {} rounds".format (self.em_round))
        self.log.info ("Convergence value: {}".format(self.convergence))
        if not self.convergence <= self.convergence_target:
            self.log.error ("Convergence target ({}) could not be reached after {} rounds".format(self.convergence_target, self.max_em_rounds))

        # Write out results
        self.log.warning ("Summarize data")

        self.log.info ("Convert results to dataframe")
        self.count_df = pd.DataFrame (self.abundance_dict.most_common(), columns=["transcript_name","raw"])
        self.count_df.set_index("transcript_name", inplace=True, drop=True)

        self.log.info ("Compute estimated counts and TPM")
        self.count_df["est_count"] = self.count_df["raw"]*len(self.read_dict)
        self.count_df["tpm"] = self.count_df["raw"] * 1000000

        # Add extra transcript info is required
        if self.extra_tx_info:
            tx_df = self._get_tx_df()
            self.count_df = pd.merge(self.count_df, tx_df, left_index=True, right_index=True, how="outer")

        # Cleanup and sort
        self.count_df.sort_values(by="raw", ascending=False, inplace=True)
        self.count_df.fillna(value=0, inplace=True)
        self.count_df.index.name = "transcript_name"

        if self.count_file:
            self.log.info ("Write file")
            self.count_df.to_csv (self.count_file, sep="\t")

    #~~~~~~~~~~~~~~PRIVATE METHODS~~~~~~~~~~~~~~#
    def _parse_bam (self):
        """
        Parse Bam/Sam file, group alignments per reads, filter reads based on
        selection criteria and return a dict of valid read/alignments
        """
        # Parse bam files
        read_dict = defaultdict (Read)
        ref_len_dict = OrderedDict()
        c = Counter()
        with pysam.AlignmentFile (self.alignment_file) as bam:

            # Collect reference lengths in dict
            for name, length in zip(bam.references, bam.lengths):
                ref_len_dict[name]=length

            for alignment in bam:
                if alignment.is_unmapped:
                    c["Discarded unmapped alignments"] +=1
                elif alignment.is_reverse:
                    c["Discarded negative strand alignments"] +=1
                elif self.discard_suplementary and alignment.is_supplementary:
                    c["Discarded supplementary alignments"] +=1
                elif self.max_dist_3_prime>=0 and alignment.reference_end <= ref_len_dict[alignment.reference_name]-self.max_dist_3_prime:
                    c["Discarded alignment with invalid 3 prime end"] +=1
                elif self.max_dist_5_prime>=0 and alignment.reference_start >= self.max_dist_5_prime:
                    c["Discarded alignment with invalid 5 prime end"] +=1
                else:
                    c["Valid alignments"] +=1
                    read_dict [alignment.query_name].add_pysam_alignment (alignment)

        # Write filtered reads counters
        log_dict (d=c, logger=self.log.info, header="Summary of alignments parsed in input bam file")

        # Filter alignments
        filtered_read_dict = defaultdict (Read)
        c = Counter()

        for query_name, read in read_dict.items ():
            # Check if best alignment is valid
            best_alignment = read.get_best_alignment(primary_score=self.primary_score)

            # In case the primary alignment was removed by filters
            if best_alignment:
                if best_alignment.align_score == 0:
                    c["Reads with zero score"] +=1
                elif best_alignment.align_len == 0:
                    c["Reads with zero len"] +=1
                elif best_alignment.qlen < self.min_read_length:
                    c["Reads too short"] +=1
                elif best_alignment.query_fraction_aligned < self.min_query_fraction_aligned:
                    c["Reads with low query fraction aligned"] +=1
                else:
                    filtered_read_dict [query_name].add_alignment (best_alignment)
                    c["Reads with valid best alignment"] +=1
                    for alignment in read.get_secondary_alignments_list(primary_score=self.primary_score):

                        # Filter out secondary alignments based on minimap alignment score
                        if self.scoring_value == "alignment_score" and alignment.align_score/best_alignment.align_score < self.equivalent_threshold:
                            c["Invalid secondary alignments"] += 1

                        # Filter out secondary alignments based on minimap alignment length
                        elif self.scoring_value == "alignment_length" and alignment.align_len/best_alignment.align_len < self.equivalent_threshold:
                            c["Invalid secondary alignments"] += 1

                        # Select valid secondary alignments
                        else:
                            c["Valid secondary alignments"] += 1
                            filtered_read_dict [query_name].add_alignment (alignment)
            else:
                c["Reads without best alignment"] += 1

        if not "Valid secondary alignments" in c:
            self.log.error("No valid secondary alignments found in bam file. Were the reads aligned with minimap `-p 0 -N 10` options ?")

        # Write filtered reads counters
        log_dict (d=c, logger=self.log.info, header="Summary of reads filtered")
        return filtered_read_dict

    def _get_compatibility (self):
        """
        """
        compatibility_dict = defaultdict(dict)
        for read_name, read in self.read_dict.items ():
            for alignment in read.alignment_list:
                compatibility_dict[read_name][alignment.rname] = score=1.0/read.n_alignment

        return compatibility_dict

    def _calculate_abundance (self):
        """
        Calculate the abundance of the transcript set based on read-transcript compatibilities
        """
        abundance_dict = Counter()
        total = 0
        convergence = 0

        for read_name, comp in self.compatibility_dict.items ():
            for ref_name, score in comp.items():
                abundance_dict [ref_name] += score
                total += score

        for ref_name in abundance_dict.keys():
            abundance_dict [ref_name] = abundance_dict[ref_name] / total

            if self.em_round > 1:
                convergence += abs (self.abundance_dict[ref_name] - abundance_dict[ref_name])

        if self.em_round == 1:
            self.convergence = 1
        else:
            self.convergence = convergence

        return abundance_dict

    def _update_compatibility (self):
        """
        Update read-transcript compatibility based on transcript abundances
        """
        compatibility_dict = defaultdict (dict)

        for read_name, comp in self.compatibility_dict.items ():
            total=0
            for ref_name in comp.keys ():
                total += self.abundance_dict [ref_name]

            for ref_name in comp.keys ():
                compatibility_dict[read_name][ref_name] = self.abundance_dict [ref_name] / total

        return compatibility_dict

    def _get_tx_df(self):
        """
        Extract transcript info from bam file header
        """
        try:
            with pysam.AlignmentFile (self.alignment_file) as bam:
                references = bam.references
                lengths = bam.lengths

            return pd.DataFrame(index=references, data=lengths, columns=["transcript_length"])
        # If any error return empty DataFrame silently
        except Exception:
            return pd.DataFrame()
