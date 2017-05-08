import pandas as pd
import sys

path_to_deletion_collection_list = "/Users/Simon/Documents/lists/Boone collection.xlsx"

X=pd.read_excel(path_to_deletion_collection_list, header=1)
#Strips whitespace from column-names
X=X.rename(columns=lambda x: x.strip())
#X=X['orf ids']
#X["pl"] = X.index

#Produces a meta data excel file for scannomatic 
# Use meta.py plate1 plate2 plate3 plate4 (from del coll proto) filename.xls

a=sys.argv[1]
b=sys.argv[2]
c=sys.argv[3]
d=sys.argv[4]
name=sys.argv[5]

def meta_constructor(plate,X):
	p1 = str(plate) + "A"
	p2 = str(plate) + "B"
	p3 = str(plate) + "C"
	p4 = str(plate) + "D"
	pl1=X[X.Plate == p1]
	pl2=X[X.Plate == p2]
	pl3=X[X.Plate == p3]
	pl4=X[X.Plate == p4]
	pl1=pl1.ORF.tolist()
	pl2=pl2.ORF.tolist()
	pl3=pl3.ORF.tolist()
	pl4=pl4.ORF.tolist()
	OUT = []
	for i in range(0,8):
		for col in range(0,12):
				col = col + 12*i
				OUT.append(pl1[col])
				OUT.append(pl1[col])

				OUT.append(pl2[col])
				OUT.append(pl2[col])
		for col in range(0,12):
				col = col + 12*i
				OUT.append(pl1[col])
				OUT.append("CONTROL_WT")
				OUT.append(pl2[col])
				OUT.append("CONTROL_WT")
		for col in range(0,12):
				col = col + 12*i
				OUT.append(pl3[col])
				OUT.append(pl3[col])
				OUT.append(pl4[col])
				OUT.append(pl4[col])
		for col in range(0,12):
				col = col + 12*i
				OUT.append(pl3[col])
				OUT.append("CONTROL_WT")
				OUT.append(pl4[col])
				OUT.append("CONTROL_WT")
	return OUT
			
x = meta_constructor(a,X)
y = meta_constructor(b,X)
z = meta_constructor(c,X) 
k = meta_constructor(d,X)
x = pd.DataFrame(x)
y = pd.DataFrame(y)
z = pd.DataFrame(z)
k = pd.DataFrame(k)

writer = pd.ExcelWriter(name)
x.to_excel(writer,"Plate1",header=False,index=False)
y.to_excel(writer,"Plate2",header=False,index=False)
z.to_excel(writer,"Plate3",header=False,index=False)
k.to_excel(writer,"Plate4",header=False,index=False)
writer.save()
