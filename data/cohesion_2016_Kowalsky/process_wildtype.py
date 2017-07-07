#!/python
"""
This script extracts the wildtype sequence from the `kowalsky2016determination`
supplementary tables.
"""
import os
import pandas as pd

def main():
    files = ["kowalsky2016determination_suppinfotxts1.csv",\
            "kowalsky2016determination_suppinfotxts2.csv",\
             "kowalsky2016determination_suppinfotxts3.csv"]
    output = []
    for fileName in files:
        name = os.path.splitext(fileName)[0]
        df = pd.read_csv(fileName)
        df = df[["Mutation", "Counts_Unselected"]]
        df = df[df["Counts_Unselected"] == "WT"]
        output.append(">{0}\n".format(name))
        output.append("".join(df["Mutation"].tolist()) + "\n")

    with open(name.split("_")[0]+"_reference.fasta", "wb") as f:
        for item in output:
            f.write(item)


if __name__ == '__main__':
	main() # run the script
