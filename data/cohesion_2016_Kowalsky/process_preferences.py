#!/python
"""
This script transforms the counts from kowalsky and whitehead into preferences.

Here is how missing data is treated in this script:

selected/unselected = enrichment
0/0 = inf : set to the minimum enrichment value
0/1 = 0.0 : set to the minimum enrichment value
0/0 = NaN : set to the average of all non-missing data

SKH 04/13/2017
"""
import os
import pandas as pd
import numpy as np

def main():
    minenrichment = 1.0e-4

    output = []
    for fileName in ["kowalsky2016determination_suppinfotxts1.csv"]:
        print(fileName)

        #read in the dataframe subset to the relevant columns
        name = os.path.splitext(fileName)[0]
        df = pd.read_csv(fileName)
        df.columns = [x.lower().strip() for x in df.columns]
        df = df[["location", "mutation", "counts_unselected", "counts_selected"]]

        #replace all instances of 'WT' with a value of 1
        df.replace("WT", 1, inplace=True)
        df.replace("WT0", 1, inplace=True)
        df= df.apply(pd.to_numeric, errors='ignore')

        #calculate the enrichment ratio
        df[['enrichment']]=df[['counts_selected']].div(df.counts_unselected, axis=0)

        #change the orientation, drop the stop codon, sort by location and amino-acid
        avg = df["enrichment"]
        df = df.pivot(index = "location", columns='mutation', values='enrichment')
        df.drop("*", inplace=True, axis=1)
        df.sort_index(inplace=True)
        df.reindex_axis(sorted(df.columns), axis=1)
        df.to_csv("testout.csv")

        #calculate the average and replace missing values (NaN) with this value
        avg = avg.replace([np.inf, -np.inf], np.nan).replace(0, np.nan).mean()
        df.replace(np.nan, avg, inplace=True)

        #replace all 0 entries and all inf entries with min preferences
        df = df.replace(0, minenrichment).replace([np.inf, -np.inf], minenrichment)

        #normalize so the rows sum to 1
        df = df.div(df.sum(axis=1), axis=0)

        #reset sites so they start at 1
        newSites = [x for x in range(1,len(df)+1)]
        df.insert(0,'site', newSites)

        #output the preferences
        df.to_csv("prefs.csv", index=False)

if __name__ == '__main__':
	main() # run the script
