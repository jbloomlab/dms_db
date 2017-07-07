# Processing data from [`mishra2016systematic`](http://ac.els-cdn.com/S2211124716303175/1-s2.0-S2211124716303175-main.pdf?_tid=ceb214be-14bd-11e7-8d9f-00000aacb35e&acdnat=1490819290_99c62c0c6d511fad788c96ef51056d76)


From the abstract:  
> To probe the mechanism of the **Hsp90 chaperone** that is required for the maturation of many signaling proteins in eukaryotes, we analyzed the effects of **all individual amino acid changes in the ATPase domain on yeast growth rate**. The sensitivity of a position to mutation was strongly influenced by proximity to the phosphates of ATP, indicating that ATPase-driven conformational changes impose stringent physical constraints on Hsp90. To investigate how these constraints may vary for different clients, we performed biochemical analyses on a panel of Hsp90 mutants spanning the full range of observed fitness effects. We observed distinct effects of nine Hsp90 mutations on activation of v-src and glucocorticoid receptor (GR), indicating that different chaperone mechanisms can be utilized for these clients. These results provide a detailed guide for understanding Hsp90 mechanism and highlight the potential for inhibitors of Hsp90 that target a subset of clients.

The preferences are from the measurements on **yeast growth rate**.

## Converting sequencing counts to amino-acid preferences

### Hand-curation
The raw counts are found in `mishra_2016_systematic_tableS1.xlsx`. Each sheet in the file is 10 residues across the protein. I copied the first (or only) replicate into `mishra_2016_systematic_tableS1.csv`.

### Amino-acid preference transformation
These transformations are performed by `process_preferences.py` on the values in `mishra_2016_systematic_tableS1.csv`.

unselected count|selected count|solution|
---|---|---|
0|0|average of all non-missing data values (pre-normalization)
0|non-zero|minimum enrichment value (1.0e-4)
non-zero|0|minimum enrichment value (1.0e-4)

The normalization ($\sum_x \pi_{r,A\left(x\right)} = 1$) occurs *after* the missing data is filled in. This means that the final values assigned to the site/codon pair with missing data is not *exactly* the average nor the minimum value.

The final preferences are in the file `prefs.csv`.

## Determining reference sequence and organism
The sequence determination is performed by `process_wildtype.py`.  

For each of the supplementary files, the above script creates a sequence based on which **mutations** are called **WT**  in the **Counts_Unselected** column. All three sequences can be found in `kowalsky2016determination_suppinfotxts1.csv`.

The original source/organism for each sequence was determined with `BLASTp`:

`kowalsky2016determination` file name|sequence length|`BLAST`match ID|organism|length of `BLAST` match sequence|perfect match?|
---|---|---|---|---|---|
suppinfotxts1|162|[Chain A, Cohesin-Dockerin Complex From The Cellulosome Of Clostridium Thermocellum](https://www.ncbi.nlm.nih.gov/protein/39654358?report=genbank&log$=prottop&blast_rank=1&RID=EZW9AUDD016)|*Clostridium Thermocellum*|162|yes  
suppinfotxts2|77|[Chain A, The Clostridium Cellulolyticum Dockerin Displays A Dual Binding Mode For Its Cohesin Partner](https://www.ncbi.nlm.nih.gov/protein/188036132?report=genbank&log$=protalign&blast_rank=1&RID=EZY2P66Z016)|*Clostridium Cellulolyticum*|151|no
suppinfotxts3|76|[Chain A, The Clostridium Cellulolyticum Dockerin Displays A Dual Binding Mode For Its Cohesin Partner](https://www.ncbi.nlm.nih.gov/protein/188036132?report=genbank&log$=protalign&blast_rank=1&RID=EZY2P66Z016)|*Clostridium Cellulolyticum*|151|no|

It looks like `suppinfotxts2` and `suppinfortxts3` are overlapping fragments of the same protein.  

## Creating alignment
