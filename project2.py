from FirstFit import FirstFit
from bestFit import BestFit
from nextFit import NextFit
import sys

if(len(sys.argv)<5):
	sys.stderr.write("ERROR: Please enter the correct number of inputs\n")
	sys.exit(0)

try:
    int(sys.argv[1])
    int(sys.argv[4])
    int(sys.argv[2])
    mmt = int(sys.argv[4])
    fpl = int(sys.argv[1])
    tms = int(sys.argv[2])
except ValueError:
	sys.stderr.write("ERROR: Improper inputs\n")
	sys.exit(0)


try:
    fn = sys.argv[3]
    fh = open(fn)
    # Store configuration file values
except FileNotFoundError:
	sys.stderr.write("ERROR: File cannot be opened\n")
	sys.exit(0)

if mmt < 0 or fpl < 0 or tms < 0:
	sys.stderr.write("ERROR: Please enter positive values\n")
	sys.exit(0)


FF = FirstFit(fpl, tms, fn, mmt)
NF = NextFit(fpl, tms, fn, mmt)
BF = BestFit(fpl, tms, fn, mmt)

FF.simulate()
print()
NF.simulate()
print()
BF.simulate()
print()
FF.simulateNonContig()
