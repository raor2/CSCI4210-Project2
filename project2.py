from FirstFit import FirstFit
from bestFit import BestFit
from nextFit import NextFit
import sys

try:
    int(sys.argv[1])
    int(sys.argv[4])
    int(sys.argv[2])
    mmt = int(sys.argv[4])
    fpl = int(sys.argv[1])
    tms = int(sys.argv[2])
except ValueError:
    sys.exit(0)


try:
    fn = sys.argv[3]
    fh = open(fn)
    # Store configuration file values
except FileNotFoundError:
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
