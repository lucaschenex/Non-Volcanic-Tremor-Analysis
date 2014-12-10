from obspy.iris import Client
import numpy as np
import matplotlib.pyplot as plt
from obspy.core import UTCDateTime
from obspy.signal import cornFreq2Paz, seisSim

client = Client()
# dt = UTCDateTime(2005, 4, 26, 21, 0, 0, 31225480)
dt = UTCDateTime("2006-5-26")
data = client.evalresp("TA", "M03C", "--", "BHE", dt) 
# data[0]
