from quickstats._version import __version__

from ROOT import gSystem
gSystem.Load('./macros/RooTwoSidedCBShape_cc')
from ROOT import RooTwoSidedCBShape
