from nose.tools import *
import Flip2BeRAD
from Flip2BeRAD.functions import *

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"

def test_multiply1():
	x = multiply(3,4)
	assert x == 12

def test_file_len():
	x = file_len("./examples/forward_test.fastq")
	assert x == 10000

def test_mismatch_it():
	x = mismatch_it('AAA', 1)
	assert len(list(x)) == 12

def test_enumerate_mismatches():
	bars = []
	with open('./examples/barcodes76.txt') as b:
		for line in b:
			if line != '\n': # ignores if there's a just a new line (i.e., at the end)
				# Now add the list of mismatches to the master list, removing the \n as needed.
				bars += list(mismatch_it(line.rstrip('\n'), 1))
		assert len(bars) == len(set(bars)) == 2432

def test_check_lengths():
	x = check_lengths('./examples/forward_test.fastq', './examples/reverse_test.fastq')
	assert x == 2500

