
import os
import sys
from optparse import OptionParser as opt
import numpy as np
import pandas as pd
import scanomatic.dataProcessing.norm as som_norm

#Set the options that need to be set
prsr = opt()

prsr.add_option("-l", "--list", dest="list", metavar="FILE", help="List of dates to be analyzed. Format: DDMMYY")
prsr.add_option("-i", "--input-path", dest="path", metavar="PATH", help="Path to projects")
prsr.add_option("-g", "--random", dest="random", metavar="BOOL", default=True, help="Generate random position? [Default:%default]")
prsr.add_option("-o", "--output-path", dest="out_path", metavar="PATH", help="output path")
prsr.add_option("-r", "--row", dest="row", type="int", metavar="Int", help="Row")
prsr.add_option("-c", "--col", dest="col", type="int", metavar="Int", help="Col")
prsr.add_option("-p", "--plt", dest="plt", type="int", metavar="Int", help="Plate")
prsr.add_option("-s", "--scan_no", dest="scan_no", metavar="Int", help="Scanner")

# Get options
(options, args) = prsr.parse_args()
if options.random == "False":
	options.random = False

def extract_curves(options, scan_dates):
 	OUTPUT = []
	for scan_date in scan_dates:       
		scan_date = scan_date.rstrip()
		scan = "_scanner" + str(options.scan_no)
        	project = os.path.join(options.path,(scan_date + scan), (scan_date + scan), "analysis", "curves_smooth.npy")
        	DN = np.load(project)
        	EP = [som_norm.DEFAULT_CONTROL_POSITION_KERNEL == False] * 4
        	PROJECT = som_norm.getControlPositionsArray(DN,EP)
        	OUTPUT.append(PROJECT[options.plt][options.row][options.col])

	
	return OUTPUT

def get_random_pos():
	row = np.random.randint(31)
	col = np.random.randint(47)
	return row,col

if __name__ == "__main__":

	options.plt = options.plt - 1

	with open(options.list, "r") as date_file:
		dates = date_file.readlines()
	if options.random:
		options.row,options.col = get_random_pos()
		out = extract_curves(options, dates)
		test = np.ma.masked_array(out[0],np.isnan(out[0]))
		while not np.sum(test) > 1:
			options.row,options.col = get_random_pos()
                	out = extract_curves(options, dates)
                	test = np.ma.masked_array(out[0],np.isnan(out[0])) 
	else:
		out = extract_curves(options, dates)
	filename = "scanner_%s_%s_%s_%s.csv" % (options.scan_no,options.plt,options.col,options.row)
	filename = os.path.join(options.out_path, filename)	

	table = pd.DataFrame(out)
	table = table.transpose()
	table.to_csv(filename)
		
