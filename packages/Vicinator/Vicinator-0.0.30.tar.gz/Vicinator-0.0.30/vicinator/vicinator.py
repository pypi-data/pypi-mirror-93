"""
Created on Apr 17, 2020
#!/usr/bin/python3

#Locate position and orientation of orthologs in related genomes (shared synteny analysis)

@author: ba1
"""

import argparse
import os
import pickle
import pandas as pd
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
from collections import OrderedDict
from colorama import Fore as fg
from colorama import Back as bg
from colorama import Style
from colorama import init as colorinit
import ete3
from ansi2html import Ansi2HTMLConverter
import multiprocessing as mp
import logging
import pathlib
import gc

# from beautifultable import BeautifulTable

#### Get Version
FILENAME = pathlib.Path(__file__).stem

try:
    from importlib.metadata import version, PackageNotFoundError

    __version__ = version(FILENAME)
except:
    try:
        # if the python version is <3.8 this module is used as backport
        from importlib_metadata import version, PackageNotFoundError

        __version__ = version(FILENAME)
    except:
        # if module or this python package is not installed
        from pkg_resources import get_distribution, DistributionNotFound

        try:
            __version__ = get_distribution(FILENAME).version
        # except DistributionNotFound:
        except:
            # package is not installed
            __version__ = "unspec"
####

#TODO: New function:
# Instead of a window around a centerprotein a list of proteins can be given.
# There should be two modes, one where the names of the groups can be given as a list
# and another where the protein ids can be given as a list with a required reference genome.

#TODO: Seperate the final window annotation from visualization

#TODO: Visualize the tree in the output

#TODO: Implement an optional rerun through the featurefile to identify the found genes and extract other relevant info
#like intergenic distance, gene annotation, gene symbols and other non-coding genes in between

#TODO: Unify the output widths by putting the genes to be tracked in columns and the gene numbers in between

#TODO: Improve incode documentation

#TODO: Improve usage documentation and give examples or write a tutorial

#TODO: Implement a scoring system that allows the quantify the relative conservedness of the neighborhood

#TODO: Implement a web-version with javascript that can access the entire gff/feature_table of refseq


def writeable_dir(prospective_dir):
    """
    Defines a class for the argparse argument type
    """
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError(
            "writeable_dir:{0} is not a valid path".format(prospective_dir)
        )
    if os.access(prospective_dir, os.W_OK):  # R_OK, X_OK
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError(
            "writeable_dir:{0} is not a writeable dir".format(prospective_dir)
        )


def parse_args():
    parser = argparse.ArgumentParser(
        prog="vicinator",
        description="Track Microsynteny of target proteins and its orthologs across genomes.",
    )

    parser._action_groups.pop()

    required = parser.add_argument_group("required arguments")

    required.add_argument(
        "--tabular-ortholog-groups",
        dest="ogtable",
        metavar="<orthology_table>",
        type=argparse.FileType("rt"),
        required=True,
        help="path to mapping file with format ortholog_group_id<tab>genome_id<tab>protein_seq_id",
    )

    required.add_argument(
        "--feat-tables-dir",
        dest="feat_tables_dir",
        metavar="<dir_path>",
        type=str,
        required=True,
        help="path to directory of *.feature_tables.txt or *.gff3 files that shall be screen",
    )

    # TODO: FUTURE_FEATURE
    # parser.add_argument(
    #     "--intergenic-distances",
    #     dest="genedist",  # metavar='<newick_tree_file_path>',
    #     action="store_true",
    #     required=False,
    #     help="if option is set, shows intergenic distances of genes surrounding the center gene",
    # )

    n_group = parser.add_argument_group("required arguments (neighborhood)")
    group_ex = n_group.add_mutually_exclusive_group(required=True)

    n_group.add_argument(
        "--reference",
        dest="ref_feat_table",
        metavar="<file_path>",
        type=argparse.FileType("rt"),
        required=True,
        help="path to a ncbi style feature table or gff file that acts as a reference",
    )

    n_group.add_argument(
        "--centerprotein-accession",
        dest="centerprotein_accession",
        metavar="<str>",
        type=str,
        required=True,
        help="unique identifier of the central gene of the window",
    )

    group_ex.add_argument(
        "--extension-size",
        dest="ext_size",
        metavar="<int>",
        type=int,
        required=False,
        help="defines the #features that are co-checked to the left and right of the centerprotein",
    ),

    group_ex.add_argument(
        "--extension-mask",
        dest="ext_mask",
        metavar="<int>",
        type=int,
        nargs='+',
        required=False,
        help="defines the position of features that are co-checked to the left and right relative to the centerprotein (position 0).",
    ),

    o_group = parser.add_argument_group("optional arguments (output)")

    o_group.add_argument(
        "--tree",
        dest="tree",
        metavar="<newick_tree_file_path>",
        type=argparse.FileType("rt"),
        required=False,
        help="path to newick tree that includes all taxa to be screened",
    )

    o_group.add_argument(
        "--outdir",
        dest="outdir",
        metavar="<dir_path>",
        type=writeable_dir,
        required=False,
        default=os.getcwd(),
        help="path to desired output directory",
    )

    o_group.add_argument(
        "--prefix",
        dest="output_prefix",  # metavar='<newick_tree_file_path>',
        type=str,
        metavar="<str>",
        required=False,
        help="if option is set, shows intergenic distances of genes surrounding the center gene",
    )

    o_group.add_argument(
        "--outputlabel-map",
        dest="labelmap",
        metavar="<file_path>",
        type=argparse.FileType("rt"),
        default=None,
        help="Attempts to replace genome accessions in the outputs with a replacement string. Requires a two-column map file formatted like so: 'genome file accession' <tab> 'replacement string'",
    )

    r_group = parser.add_argument_group("optional arguments (run)")

    r_group.add_argument(
        "--nprocs",
        dest="nprocs",
        metavar="<int>",
        type=int,
        default=mp.cpu_count() - 1,
        help="Number of CPUs for parallel processing of genomes. Default: Number of CPUs-1",
    )

    r_group.add_argument(
        "--force",
        dest="force_new_database",  # metavar='<newick_tree_file_path>',
        action="store_true",
        required=False,
        default=False,
        help="if option is set, existing ortholog databases in the output dir are ignored and will be overwritten",
    )

    parser.add_argument("--version", action="version", version=__version__)

    return parser.parse_args()


# class Window:
#     def __init__(self):
#         self.ref_indices=[]
#         self.ogs = []
#         self.directions = []
#         self.center = None


class Genome:
    def __init__(self, genome_name, feature_table):
        self.feature_df = feature_table
        # print(self.feature_df.iloc[:3][["start", "end"]], self.feature_df.iloc[-3:][["start", "end"]])
        self.name = genome_name
        self.contigs = feature_table["genomic_accession"].unique()
        self.contig_lengths = {key: None for key in self.contigs}

    def OrientAnnotatedContigs(self, center_strand):
        """
        Flips the contigs to best fit reference order and orientation
        :return:
        """
        # print(self.feature_df.iloc[-3:].to_string(), self.feature_df.iloc[:3].to_string())

        def flip_strand(row):
            if row["strand.old"] == "+":
                return "-"
            else:
                return "+"

        def flipFeatTable(ft):

            ft.columns = ["strand.old" if i == "strand" else i for i in ft.columns]
            ft.columns = ["start.old" if i == "start" else i for i in ft.columns]
            ft.columns = ["end.old" if i == "end" else i for i in ft.columns]

            contig_length = ft.iloc[-1]["end.old"]
            self.contig_lengths[ga] = contig_length

            if (
                contig_length < ft.iloc[0]["end.old"]
                or ft.iloc[-1]["start.old"] > ft.iloc[-1]["end.old"]
            ):
                ft_is_circular = True
            else:
                ft_is_circular = False
            ft["end"] = contig_length - ft["start.old"] + 1
            # print(contig_length, '-', ft.iloc[0]["end.old"], '+1')
            ft["start"] = contig_length - ft["end.old"] + 1
            ft["strand"] = ft.apply(lambda row: flip_strand(row), axis=1)

            ft = ft.drop(["start.old", "end.old", "strand.old"], axis=1)

            return ft

        if len(self.feature_df["OG"]):
            for ga in (
                self.feature_df[["genomic_accession", "OG"]]
                .dropna()["genomic_accession"]
                .unique()
            ):

                temp = self.feature_df[self.feature_df["genomic_accession"] == ga]
                ogs_pos_list = temp["window_position"].dropna().values

                if (
                    0 in ogs_pos_list
                ):  # If the centerprotein has different orientation, flip the contig
                    current_strand = temp[temp["window_position"] == 0][
                        "strand"
                    ].values[0]
                    if current_strand == center_strand:
                        continue
                    else:
                        self.feature_df.update(flipFeatTable(temp))
                        self.feature_df = self.feature_df.iloc[
                            ::-1
                        ]  # .reset_index(drop=True)
                        continue

                # Strategy: If the majority of neighboring OGs have ascending relative (to the ref) positions
                # Don't do anything. Otherwise flip.
                asc = [x < y for x, y in zip(ogs_pos_list, ogs_pos_list[1:])]
                asc = max(len(list(filter(None, asc))), 1)

                if asc < (len(ogs_pos_list) / 2):
                    self.feature_df.update(flipFeatTable(temp))
                    self.feature_df = self.feature_df.iloc[
                        ::-1
                    ]  # .reset_index(drop=True)
                    # TODO: Idea: leave the original indices to avoid to problem of messed up
                    # consecutive order of GENE and CDS Features

    def annotWindowOGs(self, window_ogs, ogtable, center_strand, extension_mask):
        def mapPAtoOG(ogset, pa2og_dict):
            if not ogset or (ogset != ogset):
                return float("nan")
            res = []
            for og in ogset:
                if og and not (og != og):
                    res.append(pa2og_dict.get(og))
            res = [r for r in res if r]
            if res:
                return res[0]  ##Crudely limit to only one OG

            return float("nan")

        pos_dict = dict()
        pruned_ogtable = ogtable[
            ogtable.index.isin([self.name], level=0)
        ]  # slice OGtable to Genome
        if pruned_ogtable.empty:
            logging.warning(
                "[{}] No orthologs found in table. Retrying with fuzzy name resolution.".format(
                    self.name
                )
            )
            pruned_ogtable = ogtable[
                ogtable.index.isin(["_".join(self.name.split("_")[:2])], level=0)
            ]  # slice OGtable to Genome
        # pruned_ogtable.columns = pruned_ogtable.columns.get_level_values(0)
        pruned_ogtable.reset_index(
            level=pruned_ogtable.index.names, inplace=True
        )  # remove multilevel
        pruned_ogtable.drop(
            ["Taxon"], axis=1, inplace=True
        )  # remove the new Taxon column
        pruned_ogtable.set_index("PA", inplace=True)
        all_relevant_ogs = [
            og for ogset in window_ogs for og in ogset if type(og) == str
        ]

        pruned_ogtable = pruned_ogtable[
            pruned_ogtable["OG"].isin(all_relevant_ogs)
        ]  # drop all non-window OGs

        pa2og_dict = pruned_ogtable.to_dict()["OG"]

        for i, ogset in enumerate(window_ogs):
            for og in ogset:
                if type(og) == str:
                    # if not og in pos_dict:
                    #     pos_dict[og] = [i - extension_size]
                    # else:
                    #     pos_dict[og].append(i - extension_size)
                    pos_dict[og] = extension_mask[i]  # relevant position

        # reduce dict to relevant ones only
        # reduced_pa2og_dict = {pa:og for pa,og in pa2og_dict.items() if og in window_ogs} #subset of relevant pa2hogs
        # insert here solution to deal with sets of product_accession, basically the map function must be able to take
        # as input not a single string but rather an entire set and check individually

        self.feature_df["OG"] = self.feature_df["product_accession"].apply(
            mapPAtoOG, args=(pa2og_dict,)
        )

        self.feature_df["window_position"] = self.feature_df["OG"].map(pos_dict)
        self.OrientAnnotatedContigs(center_strand)

        # print(self.feature_df[["OG","window_position"]].dropna())

    def getOGidFromTable(self, ogtable, genome, pa):

        try:
            og = ogtable[~ogtable.index.duplicated()].loc[(genome, pa)]["OG"]
            # Note: default pandas behaviour: multi-index df loc gives a df for dfs with duplicate indexes
        except:
            return -1  # Code for missing protein information in genome
        if not og:
            return 0  # Code for missing OG value in OG table (==Singleton)
        else:
            return og

    def orderContigs(self):
        # df = self.feature_df[self.feature_df['class'] == 'with_protein'].groupby('genomic_accession').count()
        # df.sort_values(['OG', 'product_accession'], inplace=True, ascending=False)
        df = (
            self.feature_df[self.feature_df["class"] == "protein_coding"]
            .groupby("genomic_accession")["window_position"]
            .max()
        )
        df.sort_values(ascending=True, inplace=True)
        self.contigs = df.index  # in order of appearance

    def findProteinAccessionIndices(self, protein_accession):
        """find the product accession and identify the index of its corresponding gene feature in a preceding row"""

        indices = self.feature_df[
            self.feature_df["product_accession"]
            .astype(str)
            .str.contains(protein_accession)
            .fillna(False)
        ].index.values

        return indices

    def findProteinAccessionIndicesOfWindow(self, extension_mask, center):
        """get upstream and downstream neighboring indexes of CDS and their gene feature"""

        center_genomic_accession = self.feature_df.loc[center.name]["genomic_accession"]

        filter1 = self.feature_df["class"] == "protein_coding"
        filter2 = self.feature_df["genomic_accession"] == center_genomic_accession
        df = self.feature_df[filter1 & filter2]

        c = df.index.get_loc(center.name)

        upstream = []
        downstream = []

        for i in extension_mask:
            if i < 0:
                if c + i >= 0: #if the contig position exceeds the contig indicate by "" in window
                    upstream.append(df.iloc[c + i].name)
                else:
                    upstream.append("")

            if i > 0:
                if c + i <= len(df) - 1:
                    downstream.append(df.iloc[c + i].name)
                else:
                    downstream.append("")

        return upstream + [center.name] + downstream

    def produceCMDLOutput(self, label_map=None):

        colorinit()

        def decorIntermedNum(n):
            s = str(n)
            return ".({n}){dots}".format(n=num_of_intermdiates, dots="." * (4 - len(s)))

        basket_list = [bg.YELLOW + fg.BLACK + "|" + Style.RESET_ALL]

        for ga in self.contigs:
            df = self.feature_df[self.feature_df["genomic_accession"] == ga]

            df = df[df["class"] == "protein_coding"]
            df.index = range(1, len(df) + 1)

            current_pos = 0
            ogpos = 0

            for ogpos in df["OG"].dropna().index:
                if df.loc[ogpos]["strand"] == "-":
                    ogstring = "<" + df.loc[ogpos]["OG"].replace(".fa", "")
                elif df.loc[ogpos]["strand"] == "+":
                    ogstring = df.loc[ogpos]["OG"].replace(".fa", "") + ">"
                else:
                    ogstring = "?" + df.loc[ogpos]["OG"].replace(".fa", "") + "?"

                num_of_intermdiates = ogpos - (current_pos + 1)
                if num_of_intermdiates:
                    basket_list.append(decorIntermedNum(num_of_intermdiates))
                if df.loc[ogpos]["window_position"] < 0:
                    colored_string = bg.CYAN + fg.BLACK + ogstring + Style.RESET_ALL
                elif df.loc[ogpos]["window_position"] > 0:
                    colored_string = bg.MAGENTA + fg.BLACK + ogstring + Style.RESET_ALL
                else:
                    colored_string = bg.WHITE + fg.BLACK + ogstring + Style.RESET_ALL
                basket_list.append(colored_string)
                current_pos = ogpos

            if len(df) > 0 and ogpos <= len(df):
                num_of_intermdiates = len(df) - ogpos
                if num_of_intermdiates:
                    basket_list.append(decorIntermedNum(num_of_intermdiates))
                basket_list.append(bg.YELLOW + fg.BLACK + "|" + Style.RESET_ALL)
                if ogpos == 0:
                    del basket_list[-2:]

        if label_map:
            return (
                self.name + "\t" + label_map[self.name] + "\t" + " ".join(basket_list)
            )
        else:
            return self.name + "\t" + " ".join(basket_list)


def readOGTable(orthotable_filepath, outdir, force_new_database):
    if (
        not os.path.exists(os.path.join(outdir, "vicinator.ogtable.pickle"))
        or force_new_database
    ):
        ogtable = pd.read_csv(
            orthotable_filepath,
            sep="\t",
            index_col=[1, 2],
            comment="#",
            names=["OG", "Taxon", "PA"],
        )
        ogtable = ogtable.sort_index()

        outfile = open(os.path.join(outdir, "vicinator.ogtable.pickle"), "wb")
        pickle.dump(ogtable, outfile)

    else:
        infile = open(os.path.join(outdir, "vicinator.ogtable.pickle"), "rb")
        ogtable = pickle.load(infile)

    return ogtable


def AggregateProductsOfProteinCodingGenes(ft_df):

    # Investigate which is best suited as grouping column or create a new one based on Parent ID relationship:

    groupers = ["GeneID", "locus_tag", "NEW_grouper"]
    for i, grouper in enumerate(groupers):
        if (
            not ft_df[ft_df["feature"] == "gene"][grouper].dropna().empty
            and not ft_df[ft_df["feature"] == "CDS"][grouper].dropna().empty
        ):
            break
        if i == len(groupers) - 2:
            grouper = groupers[-1]
            break

    if grouper == "NEW_grouper":
        ft_df[grouper] = ft_df["parent"]
        ft_df.loc[ft_df["feature"] == "gene", grouper] = ft_df["ID"]

    # print('GROUPER used', grouper)

    temp = (
        ft_df[ft_df["feature"] == "CDS"]
        .groupby([grouper], sort=False)[["product_accession"]]
        .agg(set)
        .reset_index()
    )

    ft_df = pd.merge(ft_df, temp, on=[grouper], sort=False, how="left")

    ft_df = ft_df.drop("product_accession_x", axis=1).rename(
        {"product_accession_y": "product_accession"}, axis=1
    )

    ft_df = ft_df[ft_df["feature"] == "gene"]

    return ft_df


def parseFeatureTable(feattable_path):
    """parses the ncbi feature table file into a pandas dataframe"""
    ft_df = pd.read_csv(
        feattable_path,
        header=0,
        names=[
            "feature",
            "class",
            "assembly",
            "assembly_unit",
            "seq_type",
            "chromosome",
            "genomic_accession",
            "start",
            "end",
            "strand",
            "product_accession",
            "non-redundant_refseq",
            "related_accession",
            "name",
            "symbol",
            "GeneID",
            "locus_tag",
            "feature_interval_length",
            "product_length",
            "attributes",
        ],
        sep="\t",
        index_col=False,
    )

    return AggregateProductsOfProteinCodingGenes(ft_df)


def parseGFF3(gff3_path):

    # from BCbio import GFF
    #
    # examiner = GFFExaminer()
    # with open(gff3_path, 'r') as in_file:
    #     for rec in GFF.parse(in_handle):
    #         print

    """parses the ncbi gff3 file into a pandas dataframe"""
    # ft_df = pd.read_csv(gff3_path,
    #                  header=0,
    #                  names=['genomic_accession','source','feature', 'start', 'end', 'score', 'strand',
    #                         'phase', 'attributes'],
    #                  sep='\t',
    #                  index_col=False,
    #                     comment='#')

    # ft_df = ft_df[~ft_df['feature'].isin(['exon','transcript','mRNA'])]
    # ft_df['ID'] = ft_df['attributes'].str.split('ID=', n=1, expand=True)[1].str.split(';', n=1, expand=True)[0]
    # ft_df['name'] = ft_df['attributes'].str.split('Name=', n=1, expand=True)[1].str.split(';', n=1, expand=True)[0]
    # #ft_df['product_accession'] = ft_df[ft_df['feature'] == 'CDS']['attributes'].str.split('protein_id=', n=1, expand=True)[1].str.split(';', n=1, expand=True)[0]
    # ft_df['product_accession'] = ft_df[ft_df['feature'] != 'gene']['attributes'].str.split('Name=', n=1, expand=True)[1].str.split(';',n=1,expand=True)[0]
    # ft_df['geneid'] = ft_df['attributes'].str.split('Dbxref=', n=1, expand=True)[1].str.split(',', n=1, expand=True)[0]
    # #ft_df['locus_tag'] = float("NaN")
    # #ft_df['locus_tag'] = ft_df[ft_df['feature'] == 'gene']['attributes'].str.split('locus_tag=', n=1, expand=True)[1].str.split(';', n=1, expand=True)[0]
    # ft_df['related_accession'] = ft_df['attributes'].str.split('Parent=', n=1, expand=True)[1].str.split(';', n=1, expand=True)[0]
    # ft_df['class'] = ['with_protein' if x else float("NaN") for x in ft_df['product_accession'].fillna(0)]
    # ft_df['product_group_id'] = (ft_df['product_accession'] != ft_df['product_accession'].shift(1)).astype(int).cumsum() #consecutive entries with same product_accession
    # temp = ft_df.groupby(['product_accession','product_group_id'], sort=False).agg({'start':'min','end':'max'}).reset_index()
    # ft_df = ('start_x',axis=1) \
    #                                                                                       .drop('end_x',axis=1) \
    #                                                                                       .rename(columns={'start_y':'start','end_y':'end'}) \
    #                                                                                       .astype({'start': 'Int32', 'end':'Int32'}) \
    #                                                                                       .reset_index(drop=True)
    #
    # ft_df['gene_group'] = (ft_df['geneid'] != ft_df['geneid'].shift(1)).astype(int).cumsum()
    # temp = ft_df[ft_df['feature']=='CDS'].groupby(['gene_group'], sort=False)[['product_accession']].agg(set).reset_index()
    # ft_df = pd.merge(ft_df, temp, on=['gene_group'], sort=False, how='left')
    # ft_df = ft_df.drop('product_accession_x', axis=1).rename({'product_accession_y': 'product_accession'}, axis=1)
    # ft_df['product_accession'] = ft_df['product_accession'].map(lambda x: str(x), na_action="ignore")
    # ft_df = ft_df.groupby(['gene_group','feature']).agg('first').reset_index()

    ft_df = pd.read_csv(
        gff3_path,
        header=0,
        names=[
            "genomic_accession",
            "source",
            "feature",
            "start",
            "end",
            "score",
            "strand",
            "phase",
            "attributes",
        ],
        sep="\t",
        index_col=False,
        comment="#",
    )

    ft_df = ft_df[~ft_df["feature"].isin(["exon", "transcript", "mRNA"])]

    for cname, attrid in [
        ("product_accession", "Name"),
        ("class", "gene_biotype"),
        ("locus_tag", "locus_tag"),
        ("parent", "Parent"),
        ("ID", "ID"),
    ]:
        try:

            ft_df[cname] = (
                ft_df["attributes"]
                .str.split(attrid + "=", n=1, expand=True)[1]
                .str.split(";", n=1, expand=True)[0]
            )
        except:
            logging.warning(
                "An error occured while parsing the subattribute {} from the gff file. Probably absent.".format(
                    attrid
                )
            )
            ft_df[cname] = float("NaN")

    ft_df["GeneID"] = ft_df["attributes"].str.extract(r"Dbxref=.*?GeneID:([\d]+)")[0]

    ft_df.loc[
        (ft_df["feature"] == "CDS") & (ft_df["attributes"].str.contains("protein_id=")),
        "class",
    ] = "with_protein"

    return AggregateProductsOfProteinCodingGenes(ft_df)


def filterFeatTable(ft_df, column="feature", value="gene"):
    filtered_ft_df = ft_df[ft_df[column] == value]
    return filtered_ft_df


def generateMapCDStoGeneFeat(ft_df):
    """ generates a dict that links every index of CDS feature to its corresponding gene feature"""
    gene_indexes = filterFeatTable(ft_df, column="feature", value="gene").index
    cds_indexes = filterFeatTable(ft_df, column="feature", value="CDS").index

    gi_pointer = -1
    cds_to_gene_map = dict()
    for cds_index in cds_indexes[::-1]:
        while cds_index < gene_indexes[gi_pointer]:
            gi_pointer -= 1
        cds_to_gene_map[cds_index] = gene_indexes[gi_pointer]

    return cds_to_gene_map


def getTaxonOrder(treepath, ref_path):
    """Parses tree from given path to a newick tree. Locates the specified reference taxon and outputs
    a sorted list of ascending topological distances of each taxon to the reference taxon"""

    p = pathlib.Path(ref_path)
    if p.suffix == ".txt":
        refname = p.stem.replace("_feature_table", "")
    elif p.suffix == ".gff":
        refname = p.stem
    else:
        refname = "XXX"
        logging.warning(
            "Reference name could not be found in provided tree, returning neighborhoods in arbitrary order"
        )
    # refname = "_".join(os.path.basename(ref_path).split('_',2)[:2])
    # dist_list = []
    leaf_list = []
    try:
        t = ete3.Tree(treepath)
    except:
        logging.warning(
            "Provided tree does not have standard newick format. Now attempting to parse with must flexible format"
        )
        t = ete3.Tree(treepath, format=5, quoted_node_names=True)

    for i, leafnode in enumerate(t.iter_leaves()):
        if leafnode.name == refname:
            leafnode.name = "000"
            t.sort_descendants(attr="name")
            # t.ladderize()
            leafnode.name = refname
            break
            # dist_list.append((leafnode.name, 0))
        # else:
        #    dist_list.append((leafnode, t.get_distance(refname, leafname, topology_only=True)))
        # print((leafname, t.get_distance(refname, leafname, topology_only=True)))
        # s = [l for l,d in sorted(dist_list, key=lambda x: (x[1],x[0]))]
    return t.get_leaf_names()


def profile_genome(t, window_ogs, ogtable, center, extension_mask):

    try:
        if t.suffix in [".gff", ".gff3"]:
            ft_df = parseGFF3(t)
        elif t.suffix in [".txt"]:
            ft_df = parseFeatureTable(t)

    except:
        logging.error(
            "[{}] Parsing error. Correct format? Note: '~.txt' files must be of format feature_table, '~.gff' files of format GFF3.".format(
                t.name
            )
        )
        return None

    genome_name = t.stem.replace("_feature_table", "").replace("_genomic", "")
    g = Genome(genome_name, ft_df)

    import traceback

    try:
        # only_window_ogtable = ogtable[ogtable["OG"].isin(window_ogs)]
        # g.annotWindowHOGs(window_ogs, only_window_ogtable)
        g.annotWindowOGs(window_ogs, ogtable, center.loc["strand"], extension_mask)
    except:
        logging.error(
            "[{}] No orthology information found. Ignoring taxon.".format(t.name)
        )
        tb = traceback.format_exc()
        return None

    g.orderContigs()

    return g


def compare_taxon(t, window_ogs, ogtable, center, extension_mask, label_map):
    logging.info("[{}] profiling ...".format(t.name))
    g = profile_genome(t, window_ogs, ogtable, center, extension_mask)
    if g:
        # runprofile.enable()
        str_out = g.produceCMDLOutput(label_map=label_map)
        # res = fg.WHITE + bg.BLACK + "IHateThis" + Style.RESET_ALL
        # runprofile.disable()
        # stats = pstats.Stats(runprofile).sort_stats('cumtime')
        # stats.print_stats(10)
        if str_out:
            print(str_out)
            logging.info("[{}] ... OK.".format(t.name))
            return str_out
    else:
        logging.warning("[{}] ... Failed. Ignoring taxon.".format(t.name))
    gc.collect()


def main():

    # import cProfile, pstats

    # runprofile = cProfile.Profile()

    args = parse_args()

    pd.set_option("mode.chained_assignment", None)

    if args.output_prefix:
        PREFIX = args.output_prefix
    else:
        if args.ext_mask:
            extension_info = "custom_mask"
        elif args.ext_size:
            extension_info = args.ext_size
        PREFIX = "prot_{}_ext_{}".format(args.centerprotein_accession, extension_info)

    logfilepath = pathlib.Path(args.outdir) / "{}.vicinator.log".format(PREFIX)
    if logfilepath.is_file():
        pathlib.Path.unlink(logfilepath)
    # logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logging.basicConfig(  # filename=str(logfilepath),
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(str(logfilepath)),
            logging.StreamHandler(),  # to sys.stderr by default
        ],
    )
    logging.getLogger().handlers[1].setLevel(logging.CRITICAL)

    ####################################

    ogtable = readOGTable(args.ogtable.name, args.outdir, args.force_new_database)

    reference_genome_feature_file_path = pathlib.Path(args.ref_feat_table.name)
    ref_name = reference_genome_feature_file_path.stem
    ref_suffix = reference_genome_feature_file_path.suffix

    if ref_suffix in [".gff", ".gff3"]:
        reference_genome_accession = ref_name.replace(
            "_genomic", ""
        )  # RefSeq added String to Assembly ID
        ref_ft_df = parseGFF3(args.ref_feat_table.name)
    elif ref_suffix in [".txt"]:
        reference_genome_accession = ref_name.replace("_feature_table", "")
        ref_ft_df = parseFeatureTable(args.ref_feat_table.name)
    else:
        raise TypeError(
            "Filetype not supported, {}".format(reference_genome_feature_file_path)
        )

    ref_g = Genome(reference_genome_accession, ref_ft_df)

    # IDENTIFY CENTRAL PROTEIN
    center_index_list = ref_g.findProteinAccessionIndices(args.centerprotein_accession)

    if len(center_index_list) > 1:
        logging.info(
            "centerprotein {} has multiple hits. Only the first hit is considered.".format(
                args.centerprotein_accession
            )
        )
    elif len(center_index_list) < 1:
        logging.exception(
            "Centerprotein {} not found in reference feature file {}.".format(
                args.centerprotein_accession, args.ref_feat_table.name
            ),
            # exc_info=True
        )

        quit()

    center = ref_g.feature_df.loc[
        center_index_list[0]
    ]  # only take the first of all hits of the central protein

    # FIND UPSTREAM AND DOWNSTREAM PROTEINS
    if args.ext_size:
        extension_size = abs(int(args.ext_size))
        extension_mask = tuple(range(-extension_size, extension_size+1))
    if args.ext_mask:
        extension_mask = [int(x) for x in args.ext_mask]
        if 0 not in extension_mask:
            extension_mask.append(0)
        extension_mask = tuple(sorted(extension_mask))

    window = ref_g.findProteinAccessionIndicesOfWindow(extension_mask, center)

    prot_accessions = [
        ref_g.feature_df.loc[i]["product_accession"] if i != "" else "" for i in window
    ]

    print()
    print("Center protein:", args.centerprotein_accession)
    print("Window reference accessions:", prot_accessions)

    window_ogs = []
    for i, accession_set in enumerate(prot_accessions):
        # print(i, accession_set)
        ogs = set()
        for acc in accession_set:
            og = ref_g.getOGidFromTable(ogtable, ref_g.name, acc)
            ogs.add(og)

        res = [i for i in ogs if type(i) != int]  # remove all non hits
        if res:
            window_ogs.append(set(res))  # report a set of hits
        else:
            window_ogs.append(set())  # or report empty set

    # window_ogs = [ref_g.getOGidFromTable(ogtable, ref_g.name, i) if i != "" else "" for i in prot_accessions]
    # window_ogs = [i if type(i) == str and i!= "" else 0 for i in window_ogs]

    print("translates to...")

    window_ogs_repr = []

    print(
        "Window reference OGs:",
        ["/".join(ogset) if len(ogset) >= 1 else "-" for ogset in window_ogs],
    )

    if not any(window_ogs):
        logging.critical(
            "No OGs found in window. Aborting. tablular OG file correctly formatted?"
            + "\n"
            + " Changing it requires deleting *.pickle from output directory to force reparsing."
        )
        quit()

    ##################################################################################

    taxon_feature_files = [
        p.absolute()
        for p in pathlib.Path(args.feat_tables_dir).glob("*")
        if p.is_file() and p.suffix in [".gff", ".gff3", ".txt"]
    ]
    logging.info("{} feature files (.txt,.gff) found.".format(len(taxon_feature_files)))
    if args.tree:
        taxon_order = getTaxonOrder(args.tree.name, args.ref_feat_table.name)
        ordered_taxon_feature_files = []
        for t in taxon_order:
            current_length = len(ordered_taxon_feature_files)
            for p in taxon_feature_files:
                if (
                    t in p.stem
                ):  # checking with "in" instead of "==" due to possible differences
                    ordered_taxon_feature_files.append(p)
            if len(ordered_taxon_feature_files) == current_length:
                logging.warning(
                    "Missing gff/_feature_table.txt file with taxon string: "
                    + t
                    + ". Ignoring taxon."
                )

        taxon_feature_files = ordered_taxon_feature_files
    ####
    ####

    if args.labelmap:
        label_map = dict()
        with open(args.labelmap.name, "r") as m:
            for line in m:
                k = line.strip().split("\t")[0]
                v = line.strip().split("\t")[1:]
                label_map[k] = " - ".join(v)
    else:
        label_map = None

    # table = BeautifulTable()
    # header = []
    # table.set_style(BeautifulTable.STYLE_MARKDOWN)
    # for i in range((int(args.k)+1)*2+1):
    #     if i%2 == 0:
    #         header.append("i"+str(i))
    #     else:
    #         header.append(window_ogs[i-1])
    # table.columns.header == header

    ####
    ####
    converter = Ansi2HTMLConverter(dark_bg=False, scheme="solarized", markup_lines=True)

    pool = mp.Pool(processes=args.nprocs)
    manager = mp.Manager()
    return_dict = manager.dict()
    logging.info("Number of CPUs used: {}".format(args.nprocs))
    full_output = pool.starmap(
        compare_taxon,
        [
            (t, window_ogs, ogtable, center, extension_mask, label_map)
            for t in taxon_feature_files
        ],
    )

    # full_output = []
    #
    # for t in taxon_feature_files:
    #     logging.info("[{}] profiling ...".format(t))
    #
    #     g = profile_genome(t, window_ogs, ogtable, center, extension_size)
    #
    #     if g:
    #         # runprofile.enable()
    #         str_out = g.produceCMDLOutput(label_map=label_map)
    #         # res = fg.WHITE + bg.BLACK + "IHateThis" + Style.RESET_ALL
    #         # runprofile.disable()
    #         # stats = pstats.Stats(runprofile).sort_stats('cumtime')
    #         # stats.print_stats(10)
    #     if str_out:
    #         print(str_out)
    #         full_output.append(str_out)
    #         logging.info("[{}] ... OK.".format(t))
    #     else:
    #         logging.info("[{}] ... Failed.".format(t))
    #     gc.collect()

    full_output = "\n".join([f for f in full_output if f])
    htmloutputfilepath = pathlib.Path(args.outdir) / "{}.vicinator.out.html".format(
        PREFIX
    )
    with open(htmloutputfilepath, "w") as htmlout:
        htmlout.write(converter.convert(full_output))

    logging.info("Finished successfully.")


if __name__ == "__main__":
    main()
