
import os
import sys
from optparse import OptionParser as opt
from subprocess import call
import numpy as np
import scanomatic.dataProcessing.norm as som_norm
import textwrap
import shutil
from pyPdf import PdfFileWriter, PdfFileReader
import plot_phen

DEVNULL = open(os.devnull, 'wb')

"""
"""


#Set the options that need to be set
prsr = opt()

prsr.add_option("-l", "--list", dest="list", metavar="FILE", help="List of dates to be analyzed. Format: DDMMYY")
prsr.add_option("-i", "--input-path", dest="path", metavar="PATH", help="Path to projects")
prsr.add_option("-n", "--name-list", dest="name", metavar="FILE", help="list of environments plate1 -> plate8")
prsr.add_option("-k", "--keep-rscript", dest="keep", metavar="BOOLEAN", default="False", help="Set True to keep the plotting Rscripts. Default:%default")

# Get options
(options, args) = prsr.parse_args()

def extractExp_kept(options, scan_date, scan_no):
        scan = "_scanner" + str(scan_no)
        project = os.path.join(options.path,(scan_date + scan), (scan_date + scan), "analysis", "normalized_phenotypes_latest.npy")
        tmpdir = os.path.dirname(project)
        tmpdir = os.path.join(tmpdir, "temp")
        checkDir(os.path.dirname(project))
        if not os.path.exists(tmpdir):
                os.makedirs(tmpdir)
        DN = np.load(project)
        EP = [som_norm.DEFAULT_CONTROL_POSITION_KERNEL == False] * 4
        pn1,pn2,pn3,pn4 = som_norm.getControlPositionsArray(DN,EP)
	D_CONTROL = np.isnan(som_norm.getControlPositionsArray(DN))
        D_CONTROL_1 = D_CONTROL[0]
        D_CONTROL_2 = D_CONTROL[1]
        D_CONTROL_3 = D_CONTROL[2]
        D_CONTROL_4 = D_CONTROL[3]
        pn1=np.ma.array(pn1[:, :, 0], mask=(D_CONTROL_1==False))
        pn2=np.ma.array(pn2[:, :, 0], mask=(D_CONTROL_2==False))
	pn3=np.ma.array(pn3[:, :, 0], mask=(D_CONTROL_3==False))
	pn4=np.ma.array(pn4[:, :, 0], mask=(D_CONTROL_4==False))
	np.savetxt((os.path.join(tmpdir,"plate4_exp_gt.txt")), pn4[pn4.mask == False], fmt='%.8f')
        np.savetxt((os.path.join(tmpdir,"plate1_exp_gt.txt")), pn1[pn1.mask == False], fmt='%.8f')
        np.savetxt((os.path.join(tmpdir,"plate2_exp_gt.txt")), pn2[pn2.mask == False], fmt='%.8f')
        np.savetxt((os.path.join(tmpdir,"plate3_exp_gt.txt")), pn3[pn3.mask == False], fmt='%.8f')
        FILES_FOR_PLOTTING = []
        FILES_FOR_PLOTTING.append(os.path.join(tmpdir, "plate1_exp_gt.txt"))
        FILES_FOR_PLOTTING.append(os.path.join(tmpdir, "plate2_exp_gt.txt"))
        FILES_FOR_PLOTTING.append(os.path.join(tmpdir, "plate3_exp_gt.txt"))
        FILES_FOR_PLOTTING.append(os.path.join(tmpdir, "plate4_exp_gt.txt"))
        return FILES_FOR_PLOTTING, tmpdir

if __name__ == "__main__":
        plot_phen.checkValidArgs(options)

        PLATE1, PLATE2, PLATE3, PLATE4, PLATE5, PLATE6, PLATE7, PLATE8, PLATE9 = [],[],[],[],[],[],[],[],[]
        CLEAN_LIST = []
        with open (options.list, "r") as file_date:
                for date in file_date:
                        date = date.rstrip()
                        try:
                                SCANNER1, tmpdir = extractExp_kept(options,date,1)
                                PLATE1.append(SCANNER1[0])
                                PLATE2.append(SCANNER1[1])
                                PLATE3.append(SCANNER1[2])
                                PLATE4.append(SCANNER1[3])
                                CLEAN_LIST.append(tmpdir)
                        except:
                                pass
                        try:
                                SCANNER2, tmpdir = extractExp_kept(options,date,2)
                                PLATE5.append(SCANNER2[0])
                                PLATE6.append(SCANNER2[1])
                                PLATE7.append(SCANNER2[2])
                                PLATE8.append(SCANNER2[3])
                                CLEAN_LIST.append(tmpdir)
                        except:
                                pass
                        try:
                                SCANNER3, tmpdir = extractExp_kept(options,date,3)
                                PLATE9.append(SCANNER3[0])
                                CLEAN_LIST.append(tmpdir)
                        except:
                                pass


        PLATE4 = plot_phen.fixParaquat(PLATE4, PLATE9)
        PLATE1, PLATE2, PLATE3, PLATE4, PLATE5, PLATE6, PLATE7, PLATE8 = plot_phen.fixMissingCycles(PLATE1, PLATE2, PLATE3, PLATE4, PLATE5, PLATE6, PLATE7, PLATE8)

        PLATES = []
        PLATES.append(PLATE1)
        PLATES.append(PLATE2)
        PLATES.append(PLATE3)
        PLATES.append(PLATE4)
        PLATES.append(PLATE5)
        PLATES.append(PLATE6)
        PLATES.append(PLATE7)
        PLATES.append(PLATE8)

        namefile = open(options.name, "r")

        #for PLATE, temp_name  in zip(PLATES, namefile):
        #       temp_name = temp_name.rstrip()
        #       writeRscript(PLATE, temp_name)
        #       runPlot(options, temp_name)
        #       pdfTrimmer(temp_name,options)
	
	for PLATE, temp_name in zip(PLATES, namefile):
		temp_name = temp_name.rstrip()
		
	
        #cleaner(CLEAN_LIST)
