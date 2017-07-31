### A shell script (csh) to run 3DFSC using Anaconda3 without altering the user's Python environment
### Use the commented out parts for bash

source activate fscenv

/gpfs/sw/anaconda/anaconda3/bin/python /gpfs/sw/ThreeDFSC/Anisotropy/ThreeDFSC/ThreeDFSC_Start.py  ${1} ${2} ${3} ${4} ${5} ${6} ${7} ${8} ${9} ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} ### Change to your Anaconda3 and 3DFSC directory

source deactivate
