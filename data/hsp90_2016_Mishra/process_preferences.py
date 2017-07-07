#!/python
"""
This script process the raw count data from Mishra *et al* to amino-acid
preferences.

The amino-acid preferences are the normalized enrichment values using the
average of "count1" and "count2".

SKH 04/14/2017
"""

import pandas as pd

def main():
    df = pd.read_csv("mishra_2016_systematic_tableS1.csv")
    print(df)


if __name__ == '__main__':
	main() # run the script
