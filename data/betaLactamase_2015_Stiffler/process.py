#!/python
"""
The purpose of this script is to convert the beta-lactamase enrichment scores
from `stiffler2015evolvability` into amino-acid preferences.

This script uses the average of the highest concentration of amp (2500 ug/mL).

written in `python3`
SKH 03/30/2017
"""

import pandas as pd

def main():
    minEnrichment = 1.0e-4 # minimum allowed enrichment


    df = pd.read_csv("scores.csv", skiprows = [0,1])
    df["Preference"] = [x if x>minEnrichment else minEnrichment for x in (10**df["2500"] + 10**df["2500.1"])/2]
    df["site"] = [int(x[1:-1]) for x in df["Mutation"]]
    df["AminoAcid"] = [x[-1] for x in df["Mutation"]]
    df = df[["site","AminoAcid", "Preference"]]
    df = df.sort_values(by = "site", axis=0, ascending=True)
    df = df.pivot(index = "site", columns='AminoAcid', values='Preference')
    df = df.fillna(1)
    df = df.div(df.sum(axis=1), axis=0)
    newSites = [x for x in range(1,len(df)+1)]
    df.insert(0,'site', newSites)
    df.to_csv("prefs.csv", index=False)

    #print(df.head())

if __name__ == '__main__':
    main() # run the script

#prefs[r][aa] = max(minenrichment, sum(10**score for score in scores[r][aa]) / float(ntrials))
