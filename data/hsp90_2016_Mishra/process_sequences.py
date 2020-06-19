"""
This script is to annotate the sequence IDs from the ensembl ortholog page with
the species names.
SKH 20170816
"""

from Bio import SeqIO
import pandas as pd

def rename_ensembl_alignment(species_fname, alignment_fname, alignment_outName):
    """
    This function takes an unprocessed alignment and a csv file to convert
    between `Ensebml` IDs and species names.
    The output is a new alignment with the species labeled on the sequences.

    I had to add ID/species pairs by hand.
    """
    # read in files
    species = pd.read_csv(species_fname)
    species = dict(zip(species["Ensembl_ID"], species["Species"]))
    seqs = list(SeqIO.parse(open(alignment_fname),'fasta'))

    # add extra species to the secies dictionary
    species["C47E8.5.3"] = "Caenorhabditis elegans (C elegans)"
    species["YPL240C"] = "Saccharomyces cerevisiae (S cerevisiae)"
    species["ENSP00000360609"] = "Homo sapien (Human)"
    species["FBpp0305095"] = "Fruitfly (Fruitfly)"

    # loop through the sequences and pull out the `Ensembl` identifier
    for seq in seqs:
        query = seq.id[0:6]
        if query in species.keys():
            new_seq_id = species[query]
            # new_seq_id = "{0}_{1}".format(species[query], seq.id)
        elif seq.id in species.keys():
            new_seq_id = species[seq.id]
        else:
            print("Couldn't parse id: {0}".format(seq.id))
        new_seq_id = new_seq_id.split("(")[-1][:-1] # extract the common name
        new_seq_id = "_".join(new_seq_id.split()) # format
        new_seq_id = "{0}_{1}".format(seq.id, new_seq_id)
        seq.id = new_seq_id
        seq.description = ""
    with open(alignment_outName, "w") as output_handle:
        SeqIO.write(seqs, output_handle, "fasta")

def make_wildtype_seq(fname, outName):
    ref_seq = str(list(SeqIO.parse(open(fname),'fasta'))[0].seq)

    start = 2
    end = 231
    skip = [222]

    final_seq = []

    counter = 1
    for i in range(0,len(ref_seq),3):
        if counter >= 2 and counter <= 231 and counter not in skip:
            final_seq.append(ref_seq[i:i+3])
            if counter == 122:
                print(ref_seq[i:i+3])
        counter += 1
    final_seq = "".join(final_seq)

    with open(outName, "w") as f:
        f.write(">hsp90_dms_ref_nt\n")
        f.write(final_seq)

def main():

    # set up files
    species_fname = "ensembl_species_chart.csv"
    alignment_fname = "hsp90_alignment5_preprocess.fa"
    alignment_outName = "hsp90_alignment5.fa"
    ref_fname = "hsp90_Scerevisiae_ref_nt.fasta"
    ref_outName = "hsp90_dms_ref_nt.fasta"

    # # make final alignment with species names
    # rename_ensembl_alignment(species_fname, alignment_fname, alignment_outName)

    # make the "wildtype" seq
    make_wildtype_seq(ref_fname, ref_outName)






if __name__ == '__main__':
    main()
