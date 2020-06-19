# Processing data from [`mishra2016systematic`](http://ac.els-cdn.com/S2211124716303175/1-s2.0-S2211124716303175-main.pdf?_tid=ceb214be-14bd-11e7-8d9f-00000aacb35e&acdnat=1490819290_99c62c0c6d511fad788c96ef51056d76)


From the abstract:  
> To probe the mechanism of the **Hsp90 chaperone** that is required for the maturation of many signaling proteins in eukaryotes, we analyzed the effects of **all individual amino acid changes in the ATPase domain on yeast growth rate**. The sensitivity of a position to mutation was strongly influenced by proximity to the phosphates of ATP, indicating that ATPase-driven conformational changes impose stringent physical constraints on Hsp90. To investigate how these constraints may vary for different clients, we performed biochemical analyses on a panel of Hsp90 mutants spanning the full range of observed fitness effects. We observed distinct effects of nine Hsp90 mutations on activation of v-src and glucocorticoid receptor (GR), indicating that different chaperone mechanisms can be utilized for these clients. These results provide a detailed guide for understanding Hsp90 mechanism and highlight the potential for inhibitors of Hsp90 that target a subset of clients.

The preferences are from the measurements on **yeast growth rate**.

## Calculation of amino-acid preferences
The results of the DMS are summarized in [`mishra_2016_systematic_tableS1.xlsx`](`mishra_2016_systematic_tableS1.xlsx`) and the data-cleaning/transformations are performed by [`process_preferences.py`](`process_preferences.py`).

The final preferences are in the file `prefs.csv`.

### Definition of amino-acid preferences

I defined the preferences as follows:

$\pi_{r,A\left(x\right)} = \frac{\log_{2}\left(e_{r,A\left(x\right)}\right)}{\sum_{A\left(y\right)} \log_{2}\left(e_{r,A\left(y\right)}\right)}$

where $e_{r, A\left(x\right)}$ is equal to the `NORM_RATIOCHANGE` for position $r$ and amino acid $A\left(x\right)$.

### Special Cases

There were two "nonsense" `NORM_RATIOCHANGE` values in [`mishra_2016_systematic_tableS1.xlsx`](`mishra_2016_systematic_tableS1.xlsx`), -999 and `NaN`.
I interpreted them as follows:   

• -999 means a very small measurement. I took the $\log_{2}$ of this value. This does not pass the `min_enrichment` filter so these values were replaced with the `min_enrichment` value.   
• `NaN` means the (amino acid, position) pair was not measured. I replaced these values with the average of `NORM_RATIOCHANGE` values not equal to -999 or `NaN`.

### Order of transformations

1. Determine *which* sites at least 1 $e_{r, A\left(x\right)}$ measured.
2. Remove stop codon measurements.
2. Replace `NaN` values with average $e_{r, A\left(x\right)}$ value.
3. Take $\log_{2}$ of the $e_{r, A\left(x\right)}$ values.
4. Replace small $\log_{2} e_{r, A\left(x\right)}$ values with `min_enrichment` value.
5. Normalize the values so the $\pi_{r,A\left(x\right)}$ values sum to one at a given site $r$.
6. Re-set the site index

## Alignments

`alignment_1`: yeast orthologs only  
`alignment_2`: human orthologs only  
`alignment_3`: all orthologs  
`alignment_4`: all orthologs
`alignment_5`: all orthologs from Horse.  
`alignment_6`: yeast orthologs from 5 different species from the sensu stricto website below.   
`alignment_7`: same as `alignment_6` except for one extra species (from JR).  
`alignment_8`: same as `alignment_5` but I removed *Ciona intestinali*.  

I got this from the ensembl homolog page.

The human gene is `Gene: HSP90AA2P ENSG00000224411`

I got alignment 4 from this [Ensembl Gene Tree](http://uswest.ensembl.org/Multi/GeneTree/Image?gt=ENSGT00840000129758) page.

Here is how `alignment_5.fa` was made:
1. I was looking at the [Ensembl Gene Tree](http://uswest.ensembl.org/Multi/GeneTree/Image?gt=ENSGT00840000129758) page and I looked at the Horse Hsp90AB1.
2. I took the protein number from this gene (
ENSECAG00000008511) and queried that on Ensemble. [results](https://www.ensembl.org/Multi/Search/Results?q=ENSECAG00000008511;site=ensembl_all).
3. I then clicked on the [Horse Gene](https://www.ensembl.org/Equus_caballus/Gene/Summary?db=core;g=ENSECAG00000008511;r=20:43115768-43121698;t=ENSECAT00000009101) page.
4. Then I clicked on [orthologs](https://www.ensembl.org/Equus_caballus/Gene/Compara_Ortholog?db=core;g=ENSECAG00000008511;r=20:43115768-43121698;t=ENSECAT00000009101).
5. Downloaded all orthologs, CDS.
6. I tried to do this for horse and yeast and I couldn't find the ortholog page.

I took the [ensembl_species_chart.csv](https://www.ensembl.org/info/genome/stable_ids/index.html) and annotated the sequence id's in `hsp90_alignment5.fa`.


**More alignment notes:**  
Specifically for yeast [SGD](http://www.yeastgenome.org/) or from the website in [The awesome power of yeast evolutionary genetics: New genome sequences and strain resources for the Saccharomyces sensu stricto genus](http://www.saccharomycessensustricto.org/cgi-bin/s3.cgi?data=Orthologs&version=current). The second website is just from 5 species and the first one has more species but the ortholog alignments are not as well curated.

## Wildtype sequence

I was not able to find the wildtype sequence in the original paper.
Instead, I saw that figure 2D is the N-terminal domain of Hsp90.
I then looked and ["the chaperoning function of Hsp90 is intimately coupled to the ATPase activity presented by its N-terminal domain"](http://www.nature.com.offcampus.lib.washington.edu/articles/srep09542).

Here are the printed statements from `process_preferences.py`:
```
Position 222 was not measured (original numbering)
Sites 2 to 231 were measured (original numbering)
Numbering is now shifted by 1
```

With the assumption that site 1 (original numbering) is the starting methionine, then the "wildtype" sequence should be sites 2-231 but without site 222.

I am going to use the *S. cerevisiae* sequence from `hsp90_alignment5.fa` as the starting sequence and I will edit it create the "wildtype" sequence. The code to do this can be found in `process_sequences.py`.
