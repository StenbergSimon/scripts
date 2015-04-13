#!/usr/bin/env python 
from subprocess import Popen, PIPE
from optparse import OptionParser as opt
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# Need program genomeCoverageBEd

prsr = opt()
prsr.add_option("-i", "--input", dest="input_file", metavar="FILE", help="Input BAM file")
prsr.add_option("-o", "--output", dest="out", default="coverage_plot.pdf", metavar="FILE", help="Output plot [Default:%default]")
(options, args) = prsr.parse_args()

def getCov(options):
	COV = []
	bed = Popen(["genomeCoverageBed", "-d", "-ibam", options.input_file], stdout=PIPE, stderr=PIPE)
	cut = Popen(["cut", "-f", "3"], stdin=bed.stdout, stdout=PIPE, stderr=PIPE)
	bed.stdout.close()
	COV = cut.communicate()[0]
	bed.wait()
	return COV

def plotHist(COV, options):
	plt.hist(COV, bins=100, range=(0,300))
	plt.title(os.path.basename(options.input_file))	
	plt.ylabel("Number of bases")
	plt.xlabel("Coverage")
	pp = PdfPages(options.out)
	pp.savefig()
	pp.close()

COV = ()
COV = getCov(options)
COV = COV.split("\n")
COV = filter(None, COV)
COV = [int(x) for x in COV]
plotHist(COV, options)
variance = np.var(COV)
mean = np.mean(COV)
print "Completed plotting, variance of depth was: %s, mean depth was: %s" % (variance, mean)
