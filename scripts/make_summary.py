#!/python
"""
The purpose of this script is to create a summary csv for the DMS datasets
in `dms_db`.

written in `python3`
SKH 03/29/2017
"""
import glob
import os
import pandas as pd

def main():
    final = pd.DataFrame()
    for dir in glob.glob("../data/*"):
        fname = dir+"/README.md"
        assert os.path.isfile(fname),\
                "README.md does not exist in {0}".format(dir)
        df = pd.read_csv(fname, sep = "|", skiprows = [1])
        df = df.drop(["`NOTES`", "`SOURCE`"],1)
        if len(final) > 0:
            final = pd.concat([final,df])
        else:
            final = df
    final.to_csv("../metadata/summary.csv", index=False, na_rep="NaN")
    
    final.reset_index(drop=True, inplace=True)
    inds = pd.isnull(final).any(1).nonzero()[0]
    if len(inds) > 0:
        print("The following datasets have missing information: ")
        print(final.ix[inds])



if __name__ == '__main__':
    main() # run the script
