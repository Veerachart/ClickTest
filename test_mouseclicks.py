# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 12:07:10 2017

@author: veerachart
"""

from __future__ import print_function

import matplotlib
#matplotlib.use("WxAgg")
#matplotlib.use("TkAgg")
#matplotlib.use("GTKAgg")
#matplotlib.use("Qt4Agg")
#matplotlib.use("MacOSX")
import matplotlib.pyplot as plt
matplotlib.rcParams['keymap.back'] = ''

#print("***** TESTING WITH BACKEND: %s"%matplotlib.get_backend() + " *****")


def OnClick(event):
    if event.dblclick:
        print("DBLCLICK", event)
    else:
        print("DOWN    ", event)


def OnRelease(event):
    print("UP      ", event)
    
    
def OnKey(event):
    print(event.key, event.xdata, event.ydata)


fig = plt.gcf()
cid_up = fig.canvas.mpl_connect('button_press_event', OnClick)
cid_down = fig.canvas.mpl_connect('button_release_event', OnRelease)
cid_key = fig.canvas.mpl_connect('key_press_event', OnKey)

plt.gca().text(0.5, 0.5, "Click on the canvas to test mouse events.",
               ha="center", va="center")

plt.show()