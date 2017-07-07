# Processing data from [`kowalsky2016determination`](http://onlinelibrary.wiley.com/doi/10.1002/prot.25175/full)


From the abstract:  
> The comprehensive sequence determinants of binding affinity for **type I cohesin** toward dockerin from **Clostridium thermocellum and Clostridium cellulolyticum** was evaluated using deep mutational scanning coupled to yeast surface display. We measured the relative binding affinity to dockerin for 2970 and 2778 single point mutants of C. thermocellum and C. cellulolyticum, respectively, representing over 96% of all possible single point mutants.

Currently, the only data being processed is from `kowalsky2016determination_suppinfotxts1.csv` which corresponds to the cohesion from *Clostridium Thermocellum*.

## Converting sequencing counts to amino-acid preferences
These transformations are performed by `process_preferences.py`.  

The amino-acid preferences are the normalized enrichment ratios (selected/unselected).
Below are the types of missing data and how they are handled in the transformation to amino-acid preferences.

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
