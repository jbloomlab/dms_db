# dms_db

Curated collection of Deep Mutational Scanning datasets for `phydms` analysis.   

## Data
#### Naming
The directories have the following naming scheme:   
`PROTEIN_YEAR_FIRSTAUTHOR`

#### Contents
##### README
Each directory will have a `README` with the following information:   
• Database ID (name of directory)  
• Protein   
• Source ID (`BibTeX` id from `references.bib`)   
• Number of residues in the preferences   
• Notes (ie, numbering scheme, concentration if multiple experiments)  

There will also be a table.css file for the `HTML` mark-up of the `README` file.

#### `Citation.txt`
`BibTeX` citation

#### Preferences
Each deep mutational dataset will be transformed into amino-acid preferences.  

#### Alignments
The directory will also contain large alignments which can be sampled for `phydms` analysis.
