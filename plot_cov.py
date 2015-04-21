#!/usr/bin/env python 
from subprocess import Popen, PIPE
from optparse import OptionParser as opt
import matplotlib
matplotlib.use('PDF')
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import os
import numpy as np

plt.ioff()
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

def plotHist(COV, options, mean, iqr):
	plt.hist(COV, bins=100, range=(0,300))
	plt.title(os.path.basename(options.input_file))	
	plt.ylabel("Number of bases")
	plt.xlabel("Coverage")
        mean = float(mean)
	iqr = float(iqr)
	mean = str(round(mean, 2))
	iqr = str(round(iqr, 2))
	plt.annotate(("Average = " + mean), xy=(0.65, 0.95), xycoords='axes fraction')
	plt.annotate(("IQR = " + iqr), xy=(0.65, 0.85), xycoords='axes fraction')
	pp = PdfPages(options.out)
	pp.savefig()
	pp.close()

COV = ()
COV = getCov(options)
COV = COV.split("\n")
COV = filter(None, COV)
COV = [int(x) for x in COV]
q75, q25 = np.percentile(COV, [75 ,25])
iqr = q75 - q25
mean = np.mean(COV)
plotHist(COV, options, mean, iqr)
