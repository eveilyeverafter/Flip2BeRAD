import itertools # For grouping pair-end reads together
import sys, getopt # For parsing command line args
import os.path # For checking whether a given file exists
# from fuzzywuzzy import fuzz # For fuzzy matching
from itertools import combinations, product
from Bio.Seq import reverse_complement # working with strings
import sys


class Tee: # log file generation
    def write(self, *args, **kwargs):
        self.out1.write(*args, **kwargs)
        self.out2.write(*args, **kwargs)
    def write_silent(self, *args, **kwargs):
		self.out1.write(*args, **kwargs)   	
    def __init__(self, out1, out2):
        self.out1 = out1
        self.out2 = out2

sys.stdout = Tee(open("log.txt", "w"), sys.stdout)

def file_exists(f, r, b):
	""" This function checks to see if the user-given files exists """
	kill = False
	if not os.path.isfile(f):
		print "Error: The forward fastq file %r does not exists." % f
		kill = True
	if not os.path.isfile(r):
		print "Error: The reverse fastq file %r does not exists." % r
		kill = True
	if not os.path.isfile(b):
		print "Error: The barcodes file %r does not exists." % b
		kill = True			
	if kill:
		sys.exit()		

description = """
Help file for Flip2BeRAD.

-c <cutsite(s)> or --cutsites=<cutsite(s)>]
	The restriction cut site used. Can be its name or actual sequence 
	but not	both (for now). If multiple cutsites were used, specify them 
	with a	',' (e.g., <pstI,nsiI>).  

-f <foward file>
	The forward reads fastq file. Must be the same length as the reverse 
	(paired-end) fastq file. 

-r <reverse file>
	The reverse (paired-end) reads fastq file. Must be the same length as 
	the forward fastq file. 

-b <barcodes file> 
	A one-column file specifiying the sequnence of each of the sample 
	barcodes to use. 

-m <number of mismatches>
	Optional. The number (integer) of mismatches allowed in the barcode 
	region.	Warning, this should not be above 0 if barcodes are not 
	'redundant'.

-q <quiet>
	Optional. Turn off verbose printing. 	
	"""

# Here are some global variables that may be changed from the user.
forward_file = ' '
reverse_file = ' '
barcodes_file = ' '
VERBOSE = True
n_mismatches = 0
cutsites = 'pstI'
offset = 2 # This is the nucleotide offset for barcode parsing

def main(argv):
	""" This function parses out the command-line arguments."""
	global forward_file
	global reverse_file
	global barcodes_file
	global VERBOSE
	global n_mismatches
	global cutsites

	usage = 'Flip2BeRAD.py -h [for help file] -c <cutsite or cutsite1,cutsite2,...> -f <forward.fastq> -r <reverse.fastq> -b <barcode.list> -m <num of mismatches allowed in barcode> -q'
	try:
		opts, args = getopt.getopt(argv,"hc:f:r:b:m:q",["cutsites=", "forward.fastq=","reverse.fastq=", "barcode.list", "quiet"])
	except getopt.GetoptError:
		print usage
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print description
			sys.exit()
		elif opt in ("-f", "--forward"):
			forward_file = arg
		elif opt in ("-r", "--reverse"):
			reverse_file = arg
		elif opt in ("-b", "--barcodes"):
			barcodes_file = arg
		elif opt in ("-q", "--quiet"):
			VERBOSE = False
		elif opt in ("-m", "--mismatches"):
			try:
				n_mismatches = int(arg)
			except ValueError:
				print "The number of mismatches must be an integer!"
				sys.exit()
		elif opt in ("-c", "--cutsites"):
			cutsites = arg.split(',')

	# Now check to make sure the files actually exist
	file_exists(forward_file, reverse_file, barcodes_file)
	
	# Optional printing of arguments
	if VERBOSE:
		print """
This is Flip2BeRAD. Run this scrpt with -h flag to see the help file.
Go to https://github.com/tylerhether/Flip2BeRAD for more information.\n"""
		print 'Verbose printing is ON. Use -q flag to turn OFF.'
		print 'Cutsite(s): %s' % cutsites
		print 'The forward fastq file is ', forward_file
		print 'The reverse fastq file is ', reverse_file
		print 'The barcode file is ', barcodes_file
		print 'The number of mismatches allowed in the bacode sequence: %d\n\n' % n_mismatches
	else:
		sys.stdout.write_silent("""
This is Flip2BeRAD. Run this scrpt with -h flag to see the help file.
Go to https://github.com/tylerhether/Flip2BeRAD for more information.""")

if __name__ == "__main__":
   main(sys.argv[1:])

def mismatch_it(s, d=n_mismatches):
	""" This enumerates all the mismatches of a given barcode."""
	# http://stackoverflow.com/questions/19822847/how-to-generate-all-strings-with-d-mismatches-python
	N = len(s)
	letters = 'ACGTN'
	pool = list(s)

	for indices in combinations(range(N), d):
		for replacements in product(letters, repeat=d):
			skip = False
			for i, a in zip(indices, replacements):
				if pool[i] == a: skip = True
			if skip: continue

			keys = dict(zip(indices, replacements))
			yield ''.join([pool[i] if i not in indices else keys[i] 
				for i in range(N)])

def enumerate_mismatches(b_file, m):
	""" This function returns a list of all the possible mismatches """
	if VERBOSE:
		print "Creating a list of mismatched barcodes."
	bars = []
	with open(b_file) as b:
		for line in b:
			if line != '\n': # ignores if there's a just a new line (i.e., at the end)
				# Now add the list of mismatches to the master list, removing the \n as needed.
				bars += list(mismatch_it(line.rstrip('\n'), m))
	
	# Now check to make sure they are all unique
	if len(bars) != len(set(bars)):
		print "\nErrror:\tBarcodes with %i mismatches did not produce unique oligos.\n\t-->%i total barcodes but only %i unique<--\n\tReduce the number of mismatches allowed and rerun." % (n_mismatches, len(bars), len(set(bars)))
		sys.exit()
	else:
		if VERBOSE:
			print "Total number of mismatched barcodes is %i\n" % len(bars)
		return bars

# Some helper functions for grouping
# From https://docs.python.org/2/library/itertools.html#recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def flatten(listOfLists):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(listOfLists)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def check_lengths(f, r):
	""" Checks to see if forward and reverse files are the same length """
	total_length_f = file_len(f)
	total_length_r = file_len(r)
	assert total_length_f == total_length_r, "\n\nInput error:\tThe number of forward reads (%i) does not\n\t\tmatch the number of reverse reads (%i). Check\n\t\tforward and reverse fastq files." % ((total_length_f / 4.0), (total_length_r / 4.0))
	return (total_length_f / 4)

# get some simple size data for making progress bars and log files
n_pairs = check_lengths(forward_file, reverse_file) # Gets the number of pairs
increment = round((n_pairs / 10)) # For showing progress percentages

# Here's the enumerated (fuzzy matched) barcodes
bars = enumerate_mismatches(barcodes_file, n_mismatches)
barcode_length = len(bars[0])
# print "Barcode length is: ", barcode_length # testing


# This opens some of the 'remainder' files:
nobarcodes_forward = open("nobarcodes_forward.fastq", 'w')
nobarcodes_reverse = open("nobarcodes_reverse.fastq", 'w')
barcode_no_cut_forward = open("barcode_no_cut_forward.fastq", 'w')
barcode_no_cut_reverse = open("barcode_no_cut_reverse.fastq", 'w')
barcode_yes_cut_forward = open("filtered_forward.fastq", 'w')
barcode_yes_cut_reverse = open("filtered_reverse.fastq", 'w')

if VERBOSE:
	print "Processing %i pairs from files\n%r and\n%r\n" % (n_pairs, forward_file, reverse_file)
	# The main loop. This block: 
	# 1. iterates 4 lines at a time from each of the f and r fastq files (== 8 total lines)
	with open(forward_file) as f, open(reverse_file) as r:
	    pairs1 = grouper(f, 4) # group the forward file 4 lines at a time
	    pairs2 = grouper(r, 4) # group the reverse file 4 lines at a time
	    zipped_pairs = itertools.izip(pairs1, pairs2)

	    # These are counters for various summary stats
	    n_barcodes_found = 0
	    n_barcodes_on_forward = 0
	    n_barcodes_on_reverse = 0
	    n_reads_with_no_barcode = 0
	    n_reads_with_barcode_no_cut = 0
	    n_reads_with_barcode_yes_cut = 0

	    for i, zipped_pair in enumerate(zipped_pairs):
	        f_line1, f_line2, f_line3, f_line4, r_line1, r_line2, r_line3, r_line4 = flatten(zipped_pair)
	        # Prints percentage at 10% intervals (i.e., when VERBOSE == True)
	        if i % increment == 0:
	        	print "%d%% complete\r" % (10*i/increment + 10)
	        # 2. (fuzzy) Barcode present on of the reads?
	        if (f_line2[(offset):(barcode_length+offset)] in bars) or (r_line2[offset:(barcode_length+offset)] in bars): 
	        	n_barcodes_found += 1

	        	# 3. Is there a cut site next to the barcode on either read? If 
	        	# not, output to a 'remainder file'. If on the forward, print to 
	        	# main filtered files. If on reverse, print the flipped pair to file.
	        	if (f_line2[(offset):(barcode_length+offset)] in bars): 
	        		n_barcodes_on_forward += 1
	        		if f_line2[offset+barcode_length:].startswith(tuple(cutsites)):
	        			n_reads_with_barcode_yes_cut += 1
	        			barcode_yes_cut_forward.write(f_line1)
	        			barcode_yes_cut_forward.write(f_line2)
	        			barcode_yes_cut_forward.write(f_line3)
	        			barcode_yes_cut_forward.write(f_line4)	
	        			barcode_yes_cut_reverse.write(r_line1)
	        			barcode_yes_cut_reverse.write(r_line2)
	        			barcode_yes_cut_reverse.write(r_line3)
	        			barcode_yes_cut_reverse.write(r_line4)	
	        		else:
		        		n_reads_with_barcode_no_cut += 1
		        		barcode_no_cut_forward.write(f_line1); barcode_no_cut_forward.write(f_line2); barcode_no_cut_forward.write(f_line3); barcode_no_cut_forward.write(f_line4)
		        		barcode_no_cut_reverse.write(r_line1); barcode_no_cut_reverse.write(r_line2); barcode_no_cut_reverse.write(r_line3); barcode_no_cut_reverse.write(r_line4)

	        	else:
	        		n_barcodes_on_reverse += 1
	        		if r_line2[offset+barcode_length:].startswith(tuple(cutsites)):
	        			n_reads_with_barcode_yes_cut += 1
	        			barcode_yes_cut_forward.write(r_line1)
	        			barcode_yes_cut_forward.write(r_line2)
	        			barcode_yes_cut_forward.write(r_line3)
	        			barcode_yes_cut_forward.write(r_line4)	
	        			barcode_yes_cut_reverse.write(f_line1)
	        			barcode_yes_cut_reverse.write(f_line2)
	        			barcode_yes_cut_reverse.write(f_line3)
	        			barcode_yes_cut_reverse.write(f_line4)	
	        		else:
		        		n_reads_with_barcode_no_cut += 1
		        		barcode_no_cut_forward.write(f_line1); barcode_no_cut_forward.write(f_line2); barcode_no_cut_forward.write(f_line3); barcode_no_cut_forward.write(f_line4)
		        		barcode_no_cut_reverse.write(r_line1); barcode_no_cut_reverse.write(r_line2); barcode_no_cut_reverse.write(r_line3); barcode_no_cut_reverse.write(r_line4)

	        else:
	        	# If no barcode present on the forward or reverse read, output into 'nobarcode' file
	        	n_reads_with_no_barcode += 1
	        	nobarcodes_forward.write(f_line1); nobarcodes_forward.write(f_line2); nobarcodes_forward.write(f_line3); nobarcodes_forward.write(f_line4)
	        	nobarcodes_reverse.write(r_line1); nobarcodes_reverse.write(r_line2); nobarcodes_reverse.write(r_line3); nobarcodes_reverse.write(r_line4)

	    print "\nSummary:"
	    print "Number of reads without barcodes: %i (out of %i)." % (n_reads_with_no_barcode, n_pairs)
	    print "Number of reads found with barcodes: %i (out of %i)." % (n_barcodes_found, n_pairs)

	    print "Of the %i reads containing barcodes, %i were found on\nthe forward and %i were found on the paired-end read.\n" % (n_barcodes_found, n_barcodes_on_forward, n_barcodes_on_reverse)
	    print "Of the %i reads containing barcodes, %i had adjacent cutsites (%i did not)." % (n_barcodes_found,n_reads_with_barcode_yes_cut,n_reads_with_barcode_no_cut)
else: 
	# print "Processing %i pairs from files\n%r and\n%r\n" % (n_pairs, forward_file, reverse_file)
	# The main loop. This block: 
	# 1. iterates 4 lines at a time from each of the f and r fastq files (== 8 total lines)
	with open(forward_file) as f, open(reverse_file) as r:
	    pairs1 = grouper(f, 4) # group the forward file 4 lines at a time
	    pairs2 = grouper(r, 4) # group the reverse file 4 lines at a time
	    zipped_pairs = itertools.izip(pairs1, pairs2)

	    # These are counters for various summary stats
	    n_barcodes_found = 0
	    n_barcodes_on_forward = 0
	    n_barcodes_on_reverse = 0
	    n_reads_with_no_barcode = 0
	    n_reads_with_barcode_no_cut = 0
	    n_reads_with_barcode_yes_cut = 0

	    for i, zipped_pair in enumerate(zipped_pairs):
	        f_line1, f_line2, f_line3, f_line4, r_line1, r_line2, r_line3, r_line4 = flatten(zipped_pair)

	        # 2. (fuzzy) Barcode present on of the reads?
	        if (f_line2[(offset):(barcode_length+offset)] in bars) or (r_line2[offset:(barcode_length+offset)] in bars): 
	        	n_barcodes_found += 1

	        	# 3. Is there a cut site next to the barcode on either read? If 
	        	# not, output to a 'remainder file'. If on the forward, print to 
	        	# main filtered files. If on reverse, print the flipped pair to file.
	        	if (f_line2[(offset):(barcode_length+offset)] in bars): 
	        		n_barcodes_on_forward += 1
	        		if f_line2[offset+barcode_length:].startswith(tuple(cutsites)):
	        			n_reads_with_barcode_yes_cut += 1
	        			barcode_yes_cut_forward.write(f_line1)
	        			barcode_yes_cut_forward.write(f_line2)
	        			barcode_yes_cut_forward.write(f_line3)
	        			barcode_yes_cut_forward.write(f_line4)	
	        			barcode_yes_cut_reverse.write(r_line1)
	        			barcode_yes_cut_reverse.write(r_line2)
	        			barcode_yes_cut_reverse.write(r_line3)
	        			barcode_yes_cut_reverse.write(r_line4)	
	        		else:
		        		n_reads_with_barcode_no_cut += 1
		        		barcode_no_cut_forward.write(f_line1); barcode_no_cut_forward.write(f_line2); barcode_no_cut_forward.write(f_line3); barcode_no_cut_forward.write(f_line4)
		        		barcode_no_cut_reverse.write(r_line1); barcode_no_cut_reverse.write(r_line2); barcode_no_cut_reverse.write(r_line3); barcode_no_cut_reverse.write(r_line4)

	        	else:
	        		n_barcodes_on_reverse += 1
	        		if r_line2[offset+barcode_length:].startswith(tuple(cutsites)):
	        			n_reads_with_barcode_yes_cut += 1
	        			barcode_yes_cut_forward.write(r_line1)
	        			barcode_yes_cut_forward.write(r_line2)
	        			barcode_yes_cut_forward.write(r_line3)
	        			barcode_yes_cut_forward.write(r_line4)	
	        			barcode_yes_cut_reverse.write(f_line1)
	        			barcode_yes_cut_reverse.write(f_line2)
	        			barcode_yes_cut_reverse.write(f_line3)
	        			barcode_yes_cut_reverse.write(f_line4)	
	        		else:
		        		n_reads_with_barcode_no_cut += 1
		        		barcode_no_cut_forward.write(f_line1); barcode_no_cut_forward.write(f_line2); barcode_no_cut_forward.write(f_line3); barcode_no_cut_forward.write(f_line4)
		        		barcode_no_cut_reverse.write(r_line1); barcode_no_cut_reverse.write(r_line2); barcode_no_cut_reverse.write(r_line3); barcode_no_cut_reverse.write(r_line4)

	        else:
	        	# If no barcode present on the forward or reverse read, output into 'nobarcode' file
	        	n_reads_with_no_barcode += 1
	        	nobarcodes_forward.write(f_line1); nobarcodes_forward.write(f_line2); nobarcodes_forward.write(f_line3); nobarcodes_forward.write(f_line4)
	        	nobarcodes_reverse.write(r_line1); nobarcodes_reverse.write(r_line2); nobarcodes_reverse.write(r_line3); nobarcodes_reverse.write(r_line4)


# Housekeeping
nobarcodes_forward.close()
nobarcodes_reverse.close()
barcode_no_cut_forward.close()
barcode_no_cut_reverse.close()
barcode_yes_cut_forward.close()
barcode_yes_cut_reverse.close()







