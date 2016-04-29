# Flip2BeRAD
Python and C++ utilities for flipping RADseq reads

Flip2BeRAD is a utility for flipping the forward and reverse raw
reads generated from paired-end sequencing. For some RADseq protocols
(e.g., BestRAD), the barcode plus cut site combination can 
occur on the reverse read. This is problematic when downstream programs
(e.g., stacks) require that these be on the forward read. There are two
flavors of Flip2BeRAD: a fuller feature python script and a quicker C++
program. 


## The Python version of Flip2BeRAD

Flip2BeRAD.py performs the following tasks: 

1. Remove any reads that do not contain a barcode on either the forward
or the reverse read. n-bp mismatching of the barcode is allowed (i.e., 
this assumes your barcodes are n-bp redundant). 

2. Identify whether a cut site is adjacent to the barcode sequence. 
Multiple cut sites can simultaneously be searched. 

3. Output data into three bins: a) those without a barcode, b) those
with a barcode but no adjacent cut site, and c) filtered reads containing
a barcode and a cut site.

To install, clone the github repo and navigate to Flip2BeRAD.py script. 
For help, type in the following:
``` 
python Flip2BeRAD.py -h
```

Please note, Flip2BeRAD was built under Python 2.7 so it is recommended
that you use this version of Python to run. 


## The C++ version of Flip2BeRAD

This version is most actively under development. 

```
g++ main.cpp -o Flip2BeRAD
```

