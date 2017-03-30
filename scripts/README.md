# Scripts
This directory contains the scripts to summarize information about the datasets contained in the repository.

Currently, all scripts must be executed from this directory. 

##`make_bib.py`  
Makes a master bibliography (`BibTex` format).
Loops through the `data/` directories and extracts the information from `citation.txt`  
##`make_summary.py`  
Makes a master csv with the basic preference information.   
Protein, Source ID, ID, number of residues, etc.   
Loops through the `data/` directories and extracts the information from `README.MD`.  
##`make_html.py`  
Makes a `README.html` in each `data/` directory.  
Contains all of the information in `README.md`.

##`all_make.py`
Runs all of the scripts which start with `make` and end with `.py`.
