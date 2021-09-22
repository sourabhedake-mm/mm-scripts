import json
import sys
import csv

fp = open(sys.argv[1], mode="r")
csv_reader = csv.reader(fp, delimiter=",")

data = []
print("Reading data...")
for line in csv_reader:
    br = line[1].split(" ")
    data.append((br[0]," ".join(br[0:])))

print(data[:5])
data.sort(key=lambda x:x[0])

stack = data
print(data[:5])
print(stack[:5])
writable_stack = []
for i,x in enumerate(stack):
    sys.stdout.write("Writing to %s: %.2f%% Completed...\r" % (sys.argv[1]+".stack", (i*100)/len(stack) ))
    sys.stdout.flush()
    writable_stack.append(x[0] + " " + x[1] + "\n")

stack_fp = open(sys.argv[1]+".stack", mode="w")
stack_fp.writelines(writable_stack)
stack_fp.close()
