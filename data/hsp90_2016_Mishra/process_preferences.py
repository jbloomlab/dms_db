#!/python
"""
This script processes the data from Mishra *et al* to amino-acid
preferences.

The amino-acid preferences are the normalized log2(NORM_RATIOCHANGE).

Script notes:
• I interpreted a `NORM_RATIOCHANGE` of -999 to mean a very small measurement.
        I replaced the log2() of these values with the min_enrichment value
• I interpreted a `NORM_RATIOCHANGE` of `NaN` to mean that the
        (amino acid, position) pair was not measured.
        I replaced the `NaN` value with the average of *all* NORM_RATIOCHANGE
        values not equal to -999 or `NaN`

Dataset notes:
• The data is in a `xslx` file with the data for 10 residues per sheet.
• The numbering of the input file is sequential starting with residue 2 of Hsp90.
• There is one site which was not measured at all (site 222).
• Some of the sets of 10 residues were measured twice. I took the values from
        the first replicate.
• There are headings before the data on each sheet. The length of the header is
        not standard across all of the sheets.

SKH 04/14/2017
"""

import pandas as pd
import numpy as np

# Globals
amino_acids = ["F", "L", "I", "M", "V", "S", "P", "T", "A", "Y", "H", "Q", "N",\
        "K", "D", "E", "C", "W", "R", "G"]
amino_acids = list(set(amino_acids))
amino_acids.sort()
min_enrichment = 2.0e-4


def calc_prefs(df):
    """
    This function calculates the final preference values.
    It takes an input of a dataframe with three columns
            ["POSITION", "AA", "NORM_RATIOCHANGE"]
    It deals with "nonsense values" such as -999 or `NaN`.
    It takes log2 of each values.
    It normalizes the values to sum at 1 at a given position.
    It returns a pivoted dataframe in the `phydms` format.
    """

    df["AA"] = [x.strip() for x in df["AA"]]
    df = df[df["AA"] != "*"]

    # Step 1: Replace (amino acid, position) pairs which have not been measured
    # with the average of *all* measured (amino acid, position pairs)
    average_score = np.average([x for x in df["NORM_RATIOCHANGE"].tolist() \
            if x not in [-999] and not np.isnan(x)])
    df = df.replace(float("NaN"), average_score)

    # Step 2: Take the log2() of all of the values and replace very small
    # values with the minimum value
    df["NORM_RATIOCHANGE"] = [max(min_enrichment, np.power(2,float(x))) \
            for x in df["NORM_RATIOCHANGE"]]

    # Step 3: Normalize the values at each position
    for pos in list(set(df["POSITION"].tolist())):
        pos_sum = df[df["POSITION"] == pos]["NORM_RATIOCHANGE"].sum()
        df.ix[df.POSITION==pos, 'NORM_RATIOCHANGE'] = df.ix[df.POSITION==pos, \
                'NORM_RATIOCHANGE'] / pos_sum

    # Step 4: Pivot the dataframe and re-order the columns to match
    # the `phydms` input
    df= df.pivot(index='POSITION', columns='AA', values='NORM_RATIOCHANGE')
    print("Sites {0} to {1} were measured (original numbering)".format(df.index.values.min(), df.index.values.max()))
    print("Numbering is now shifted by 1")
    df["site"] = [x for x in range(1,len(df)+1)]
    cols = [x for x in df.columns.values if x != "site"]
    cols.sort()
    cols.insert(0,"site")
    df = df[cols]

    return df

def main():

    # input file name
    xls = pd.ExcelFile('mishra_2016_systematic_tableS1.xlsx')

    # Specific information about the dataformat
    residue_per_tab = 10
    number_aa = 21

    # list position-specific dataframes
    prefs = []

    # loop through all of the different tabs
    sheet_names = xls.sheet_names
    for sheet_name in sheet_names:
        df1 = xls.parse(sheet_name)
        stop = False
        i = 0 # index to keep track of where the data starts
        while not stop:
            # find the first row with the column headers
            if str(df1.iloc[i, 0]).upper().startswith("POSITION"):
                #quality control on column headers
                df1.columns = [str(x).upper().strip() for x in df1.iloc[i]]
                # take the rows with data
                df1 = df1.iloc[i+1:i+(residue_per_tab*number_aa)+1]
                stop = True # stop searching for the column headers
            i += 1
        df1 = df1[["POSITION", "AA", "NORM_RATIOCHANGE"]] # relevant columns
        positions = list(set(df1["POSITION"]))
        assert len(positions) == residue_per_tab

        # check to see if the position was measured or not
        for pos in positions:
            pos_df = df1[df1["POSITION"] == pos]
            if len(set(pos_df["NORM_RATIOCHANGE"])) == 1:
                print("Position {0} was not measured (original numbering)".format(pos))
            else:
                prefs.append(pos_df)

    # create gene-wide dataframe of preferences
    prefs = pd.concat(prefs)
    prefs = calc_prefs(prefs) # convert reported values to preferences
    prefs.to_csv("prefs.csv", index = False) # output the created preferences

if __name__ == '__main__':
	main() # run the script
