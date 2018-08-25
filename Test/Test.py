import os

os.chdir("../")
if "results" not in os.listdir("./Test/"):
    os.mkdir("./Test/results")

print("Testing GSE45966.")
files = os.listdir("./Test/data/GSE45966")

if "GSE45966" not in os.listdir("./Test/results/"):
    os.mkdir("./Test/results/GSE45966")

for f in files:
    if "txt" in f:
        inp = "./Test/data/GSE45966/" + f
        oup = "./Test/results/GSE45966/" + f[:-4] + ".pdb"

        command = "python evr.py -i %s -o %s --seed 1 --iter_num 2000"%(inp, oup)
        os.system(command)

        print(inp + " done!")

print("Testing GSE68418.")
files = os.listdir("./Test/data/GSE68418")

if "GSE68418" not in os.listdir("./Test/results/"):
    os.mkdir("./Test/results/GSE68418")

for f in files:
    if "txt" in f:
        inp = "./Test/data/GSE68418/" + f
        oup = "./Test/results/GSE68418/" + f[:-4] + ".pdb"

        command = "python evr.py -i %s -o %s --seed 1 --iter_num 2000"%(inp, oup)
        os.system(command)

        print(inp + " done!")

print("Testing GSE107301.")
files = os.listdir("./Test/data/GSE107301")

if "GSE107301" not in os.listdir("./Test/results/"):
    os.mkdir("./Test/results/GSE107301")

for f in files:
    if "txt" in f:
        inp = "./Test/data/GSE107301/" + f
        oup = "./Test/results/GSE107301/" + f[:-4] + ".pdb"

        command = "python evr.py -i %s -o %s --seed 1 --iter_num 2000"%(inp, oup)
        os.system(command)

        print(inp + " done!")
