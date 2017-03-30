#!/python
"""
The purpose of this script is to run all of the python scripts and create
all of the summary files.

written in `python3`
SKH 03/29/2017
"""
import subprocess
import glob

def main():
    for fname in glob.glob("make*.py"):
        print("Running {0}".format(fname))
        subprocess.check_output(['python', '{0}'.format(fname)])

    print("done.")



if __name__ == '__main__':
    main() # run the script
