import itertools # For grouping pair-end reads together
import sys, getopt # For parsing command line args
import os.path # For checking whether a given file exists
# from fuzzywuzzy import fuzz # For fuzzy matching
from itertools import combinations, product

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
		print '\n\n\nVerbose printing is ON. Use -q flag to turn OFF.'
		print 'Cutsite(s): %s' % cutsites
		print 'The forward fastq file is ', forward_file
		print 'The reverse fastq file is ', reverse_file
		print 'The barcode file is ', barcodes_file
		print 'The number of mismatches allowed in the bacode sequence: %d\n\n' % n_mismatches

if __name__ == "__main__":
   main(sys.argv[1:])


def mismatch_it(s, d=n_mismatches):
	""" This enumerates all the mismatches of a given barcode."""
	# http://stackoverflow.com/questions/19822847/how-to-generate-all-strings-with-d-mismatches-python
	N = len(s)
	letters = 'ACGT'
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
		print "\nErrror:\tBarcodes with %i mismatches did not produce unique oligos.\nReduce the number of mismatches allowed and rerun." % n_mismatches
		sys.exit()
	else:
		return bars

bars = enumerate_mismatches(barcodes_file, n_mismatches)



# # Some helper functions for grouping
# # From https://docs.python.org/2/library/itertools.html#recipes
# def grouper(iterable, n, fillvalue=None):
#     "Collect data into fixed-length chunks or blocks"
#     # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
#     args = [iter(iterable)] * n
#     return itertools.izip_longest(fillvalue=fillvalue, *args)

# def flatten(listOfLists):
#     "Flatten one level of nesting"
#     return itertools.chain.from_iterable(listOfLists)

# def file_len(fname):
#     with open(fname) as f:
#         for i, l in enumerate(f):
#             pass
#     return i + 1

# def check_lengths(f, r):
# 	""" Checks to see if forward and reverse files are the same length """
# 	total_length_f = file_len(f)
# 	total_length_r = file_len(r)
# 	assert total_length_f == total_length_r, "\n\nInput error:\tThe number of forward reads (%i) does not\n\t\tmatch the number of reverse reads (%i). Check\n\t\tforward and reverse fastq files." % ((total_length_f / 4.0), (total_length_r / 4.0))
# 	return (total_length_f / 4)

# n_pairs = check_lengths(forward_file, reverse_file)

# increment = round((n_pairs / 10))


# if VERBOSE:
# 	print "Processing %i pairs from files\n%r and\n%r" % (n_pairs, forward_file, reverse_file)
# 	# The main loop. This block: 
# 	# 1. iterates 4 lines at a time from each of the f and r fastq files (=8 total lines)
# 	# 2. and prints them.
# 	with open(forward_file) as f, open(reverse_file) as r:
# 	    pairs1 = grouper(f, 4) # group the forward file 4 lines at a time
# 	    pairs2 = grouper(r, 4) # group the reverse file 4 lines at a time
# 	    zipped_pairs = itertools.izip(pairs1, pairs2)
# 	    for i, zipped_pair in enumerate(zipped_pairs):
# 	        f_line1, f_line2, f_line3, f_line4, r_line1, r_line2, r_line3, r_line4 = flatten(zipped_pair)
# 	        if i % increment == 0:
# 	        	print "%d%% complete\r" % (10*i/increment + 10)
# 	        print f_line1, r_line1, f_line2, r_line2, f_line3, r_line3, f_line4, r_line4

# else: 
# 	print "This block under construction..."

# bar = ['atc', 'rad', 'abc']
# if 'abc' in bar:
# 	print "yes"

# x = fuzz.ratio("this is a test", ["this is a test!", "This is a test"])
# print x


