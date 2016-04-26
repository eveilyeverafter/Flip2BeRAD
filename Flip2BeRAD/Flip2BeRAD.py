import itertools # For grouping pair-end reads together
import sys, getopt # For parsing command line args
import os.path # For checking whether a given file exists

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

def main(argv):
	""" This function parses out the command-line arguments."""
	forward_file = ' '
	reverse_file = ' '
	barcodes_file = ' '
	VERBOSE = True
	n_mismatches = 0
	cutsites = 'pstI'
	
	usage = 'Flip2BeRAD.py -c <cutsite or cutsite1,cutsite2,...> -f <forward.fastq> -r <reverse.fastq> -b <barcode.list> -m <num of mismatches allowed in barcode> -q'
	try:
		opts, args = getopt.getopt(argv,"h:c:f:r:b:m:q",["cutsites=", "forward.fastq=","reverse.fastq=", "barcode.list", "quiet"])
	except getopt.GetoptError:
		print usage
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print usage
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

print "OK"




# # Here are the forward (f) and reverse (r) files.
# forward_file = '../examples/forward_test.fastq'
# reverse_file = '../examples/reverse_test.fastq'
# VERBOSE = True



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

# # Some functions for verbose output
# def check_lengths(f, r):
# 	total_length_f = file_len(f)
# 	total_length_r = file_len(r)
# 	assert total_length_f == total_length_r, "\n\nInput error:\tThe number of forward reads (%i) does not\n\t\tmatch the number of reverse reads (%i). Check\n\t\tforward and reverse fastq files." % ((total_length_f / 4.0), (total_length_r / 4.0))
# 	return (total_length_f / 4)

# n_pairs = check_lengths(forward_file, reverse_file)

# if VERBOSE:
# 	print "Processing %i pairs from files %s and %s" % (n_pairs, forward_file, reverse_file)
# 	# The main loop. This block: 
# 	# 1. iterates 4 lines at a time from each of the f and r fastq files (=8 total lines)
# 	# 2. and prints them.
# 	with open(forward_file) as f, open(reverse_file) as r:
# 	    pairs1 = grouper(f, 4) # group the forward file 4 lines at a time
# 	    pairs2 = grouper(r, 4) # group the reverse file 4 lines at a time
# 	    zipped_pairs = itertools.izip(pairs1, pairs2)
# 	    for i, zipped_pair in enumerate(zipped_pairs):
# 	        f_line1, f_line2, f_line3, f_line4, r_line1, r_line2, r_line3, r_line4 = flatten(zipped_pair)
# 	        pass
# 	        # print f_line1, r_line1, f_line2, r_line2, f_line3, r_line3, f_line4, r_line4
# 	    # print "There are %d total pairs" % total_pairs
# else: 
# 	pass




