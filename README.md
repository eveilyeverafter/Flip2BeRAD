# Flip2BeRAD
Python and C++ utilities for flipping RADseq reads

Flip2BeRAD is a utility for flipping the forward and reverse raw
reads generated from paired-end sequencing when the sample barcode is
found on the reverse (paired-end) read. For some RADseq protocols
(e.g., BestRAD), the barcode plus cut site combination can 
occur on the reverse read. This is problematic when downstream programs
(e.g., stacks) require that these be on the forward read. There are two
flavors of Flip2BeRAD: a fuller featured Python script and a quicker C++
variant. Both perform similarly but currently the Python version has 
more functionality. 


## The Python version of Flip2BeRAD

Flip2BeRAD.py performs the following tasks: 

1. Remove any reads that do not contain a barcode on either the forward
or the reverse read. n-bp mismatching of the barcode is allowed (i.e., 
this assumes your barcodes are n-bp redundant). 

2. Identify whether a cut site is adjacent to the barcode sequence. 
Multiple cut sites can simultaneously be searched. 

3. Output data into three bins: a) those without a barcode, b) those
with a barcode but no adjacent cut site, and c) filtered reads containing
a barcode and a cut site. Outputs of the `remainder' sequences can be useful in troubleshooting library preperation etc.

To run, clone the github repo and navigate to the directory containing the Flip2BeRAD.py script. 
For help, type in the following:
``` 
python Flip2BeRAD.py -h
```

To run the example, try:
```
python ./Flip2BeRAD.py -f ../examples/forward_test.fastq -r ../examples/reverse_test.fastq -b ../examples/barcodes76.txt -c TGCAT -m 0 -o 2

```

Please note, Flip2BeRAD was built under Python 2.7 so it is recommended
that you use this version of Python to run. 


## The C++ version of Flip2BeRAD

This version is a bare-bones version of the Python script and is most actively under development. Unlike the Python variant, this one does not allow barcode mismatching nor does it allow multiple cut sites to be coprocessed. To compile, clone the github repo and navigate to the directory containing the main.cpp. 
Type in:

```
g++ main.cpp -O3 -o Flip2BeRAD
or
clang++ main.cpp -03 -o Flip2BeRAD # Some OS X variants
```

Right now there's no help file for this variant but command-line options are similar between the two. To run the example, type in:

```
./Flip2BeRAD -c TGCAT -f ../../examples/forward_test.fastq -r ../../examples/reverse_test.fastq -b ../../examples/barcodes76.txt -m 0 -o 2 -q 0
```




