"""
Calculate the max amino acid and nucleotide divergence between these
different hsp90 alignments.

SKH 20170816
"""
import pandas as pd
from phydmslib import constants
import scipy
from Bio import SeqIO
import itertools

### Set up for translation and pairwise
# codon to index, add codon `---`
max_codon_index = (max(list(constants.CODON_TO_INDEX.values())))
if "---" not in list(constants.CODON_TO_INDEX.keys()):
    constants.CODON_TO_INDEX["---"] = max_codon_index + 1
# index to AA, add AA `-`
max_AA_index = max(list(constants.INDEX_TO_AA.keys()))
if "-" not in list(constants.INDEX_TO_AA.values()):
    constants.INDEX_TO_AA[max_AA_index+1] = "-"
# condon to AA, add mapping of `---` to `-`
constants.CODON_TO_AA = scipy.append(constants.CODON_TO_AA, [[max_AA_index+1]])

def translate_with_gaps(seq):
    prot_seq = []
    for i in range(0, len(seq),3):
        codon = seq[i:i+3]
        codon = constants.CODON_TO_INDEX[codon]
        AA = constants.CODON_TO_AA[codon]
        AA = constants.INDEX_TO_AA[AA]
        prot_seq.append(AA)
    return "".join(prot_seq)

def calc_pairwise_distance_aa(seq1, seq2):
    seq1_aa = translate_with_gaps(seq1)
    seq2_aa = translate_with_gaps(seq2)
    assert len(seq1_aa) == len(seq2_aa)
    pair_wise = sum([1 if seq1_aa[i] == seq2_aa[i] else 0 for i in range(len(seq1_aa))])/len(seq1_aa)
    return pair_wise

def calc_pairwise_distance_nt(seq1, seq2):
    assert len(seq1) == len(seq2)
    pair_wise = sum([1 if seq1[i] == seq2[i] else 0 for i in range(len(seq1))])/len(seq1)
    return pair_wise

def main():
    fname = "hsp90_alignment5_ref_prep.fasta"
    seqs = list(SeqIO.parse(open(fname),'fasta'))
    aa_distances = []
    nt_distances = []
    for pair in itertools.combinations(seqs,2):
        catch = pair
        pair = [str(x.seq).upper() for x in pair]
        pair = [x[:-3] if x[-3:] in ["TAA", "TAG", "TGA"] else x for x in pair]
        aa_distances.append(calc_pairwise_distance_aa(pair[0], pair[1]))
        nt_distances.append(calc_pairwise_distance_nt(pair[0], pair[1]))
        if nt_distances[-1] < 0.5:
            print([x.id for x in catch])
    # summary
    aa_distances = scipy.array(aa_distances)
    nt_distances = scipy.array(nt_distances)
    print("Nucelotide:\n Min = {0},\n Max = {1},\n Mean = {2}".format(nt_distances.min(), nt_distances.max(), nt_distances.mean()))
    print()
    print("Amino acid:\n Min = {0},\n Max = {1},\n Mean = {2}".format(aa_distances.min(), aa_distances.max(), aa_distances.mean()))

if __name__ == '__main__':
    main()
