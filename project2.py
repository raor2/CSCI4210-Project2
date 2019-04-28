from FirstFit import FirstFit
from bestFit import BestFit
from nextFit import NextFit
import sys


fpl = int(sys.argv[1])
tms = int(sys.argv[2])
fn = sys.argv[3]
mmt = int(sys.argv[4])

FF = FirstFit(fpl,tms,fn,mmt)
NF = NextFit(fpl,tms,fn,mmt)
BF = BestFit(fpl,tms,fn,mmt)

FF.simulate()
NF.simulate()
BF.simulate()
FF.simulateNonContig()
