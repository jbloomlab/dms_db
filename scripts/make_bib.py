#!/python
"""
The purpose of this script is to create a `BibTeX` bibliography for the
datasets in `dms_db`.

written in `python3`
SKH 03/29/2017
"""
import glob
import os

def main():
    bib = []
    for dir in glob.glob("../data/*"):
        fname = dir+"/citation.txt"
        assert os.path.isfile(fname),\
                "citation.txt does not exist in {0}".format(dir)
        with open(fname) as f:
            bib.extend(f.readlines())
            bib.extend("\n")
    with open("../metadata/references.bib", "wb") as out:
        for item in bib:
            out.write(item)


if __name__ == '__main__':
    main() # run the script
