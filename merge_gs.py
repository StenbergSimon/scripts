from scanomatic.models.factories.compile_project_factory import CompileImageAnalysisFactory
import re
from optparse import OptionParser as opt


prsr = opt()
prsr.add_option("-i", "--input", dest="input_file", metavar="FILE", help="Input pass.analaysis to patch")
prsr.add_option("-c", "--compilation", dest="compilation", metavar="FILE", help="Compilation file to steal grayscale from")
prsr.add_option("-o", "--output", dest="out", metavar="FILE", help="Output file, overwrites old by default")

(options, args) = prsr.parse_args()

class gray_scale_patcher():

    def __init__(self):
        pass

    def get_new_gs(self, compilation):
		comp = CompileImageAnalysisFactory.serializer.load(compilation)
		new_gs = []
		for i in comp:
			newgs = i.fixture.grayscale.values
			template = "\'grayscale_values\': " + str(newgs)
			new_gs.append(template)
		return new_gs
	
    def patch(self, input_file, compilation, output):

        PASS_ANALYSIS = self.parser(input_file)
        new_gs = self.get_new_gs(compilation)
        PASS_ANALYSIS.pop()
	for i in xrange(1, len(PASS_ANALYSIS)):
	    p = re.compile(r"\'grayscale_values\':\s\[(.+)\],")
            new_insert = new_gs.pop(0)
	    new_insert = str(new_insert) + str(",")
	    PASS_ANALYSIS[i] = p.sub(new_insert, PASS_ANALYSIS[i])
        self.writer(PASS_ANALYSIS, output)

    def writer(self, PASS_ANALYSIS, output):

        fh = open(output, "w")
        for line in PASS_ANALYSIS:
           fh.write(line)

    def parser(self, input_file):

        with open(input_file, "r") as pass_analysis:
            PASS_ANALYSIS = pass_analysis.readlines()
        return PASS_ANALYSIS

if __name__ == "__main__":
    patch = gray_scale_patcher()
    patch.patch(options.input_file, options.compilation, options.out)



