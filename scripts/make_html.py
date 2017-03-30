#!/python
"""
The purpose of this script is convert all of the `README.md` to `HTML`.

written in `python3`
SKH 03/29/2017
"""
import subprocess
import glob
import os

def main():
    for dir in glob.glob("../data/*"):
        fname = dir+"/README.md"
        outputName = dir +"/README.html"
        assert os.path.isfile(fname),\
                "README.md does not exist in {0}".format(dir)
        subprocess.check_output(['pandoc', '--css' ,'table.css', '-s', fname, '-o', outputName])
        print(" ".join(['pandoc', '--css' ,'css/table.css', '-s', fname, '-o', outputName]))
    print("done.")



if __name__ == '__main__':
    main() # run the script
