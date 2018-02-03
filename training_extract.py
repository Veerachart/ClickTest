# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:15:51 2017

@author: veerachart
"""

from __future__ import print_function

import matplotlib.pyplot as plt
import matplotlib
import cv2
import numpy as np
import sys,os
import csv

dpi = 80
global center, a, b, r, angle, fig, ax, imgIdx, img, personId, currentImg
#img = plt.imread('/home/veerachart/Dropbox/Todai_Research/Human-fisheye.jpg')
#img = cv2.imread('/home/veerachart/Dropbox/Todai_Research/Human-fisheye.jpg')
### PIROPO Dataset
imgDir = '/home/veerachart/Python-dir/Dataset_PIROPO/omni_1A/omni_1A/omni1A_training'
annotateName = '/home/veerachart/Python-dir/PIROPO_annotated/omni_1A/omni1A_training/Backup/omni1A_training.csv'
newName = '/home/veerachart/Python-dir/PIROPO_annotated/omni_1A/omni1A_training/omni1A_training.csv'
annotateFile = open(annotateName, 'rb')
reader = csv.reader(annotateFile, delimiter=',')
reader.next()   # Header line
newFile = open(newName, 'a')
writer = csv.writer(newFile)
#writer.writerow('figname,idx,person_id,position_x,position_y,width,height,angle'.split(','))

line = reader.next()
while line[0] != '2015-05-12T12-29-30.637Z.jpg':
    line = reader.next()
img = plt.imread(imgDir+'/'+line[0])
currentImg = line[0]
#imgIdx = 0
#imgList = []
#for path in os.listdir(imgDir):
#    imgList.append(path)
#imgList.sort()
#img = plt.imread(imgDir+'/'+imgList[imgIdx])
h,w,ch = img.shape
if h>w:
    pad_width = (h-w)/2
    pads = (pad_width,0)
    img = np.lib.pad(img,((0,0),(pad_width,pad_width),(0,0)),'constant',constant_values=0)
elif w>h:
    pad_width = (w-h)/2
    pads = (0,pad_width)
    img = np.lib.pad(img,((pad_width,pad_width),(0,0),(0,0)),'constant',constant_values=0)
else:
    pads = (0,0)
matplotlib.rcParams['keymap.save'] = ''
matplotlib.rcParams['keymap.pan'] = ''
h,w,ch = img.shape
figsize = w/float(dpi), h/float(dpi)
#center = [0,0]
#a = 40
#b = a
#r = 0
#angle = 0
#personId = 0
center = [int(line[3])+pads[0], int(line[4])+pads[1]]
a = int(line[5])
b = int(line[6])
r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
angle = float(line[7])
personId = int(line[2])
imgIdx = int(line[1])
print (line[0])
fig = plt.figure(figsize=figsize)
ax = fig.add_axes([0,0,1,1])

def Redraw(save=False, newImg=False):
    global center, a, b, r, angle, fig, ax, img, personId, currentImg, w, h, imgIdx
    ax.cla()
    if newImg:
        line = reader.next()
        img = plt.imread(imgDir+'/'+line[0])
        currentImg = line[0]
        center = [int(line[3])+pads[0], int(line[4])+pads[1]]
        a = int(line[5])
        b = int(line[6])
        r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
        angle = float(line[7])
        personId = int(line[2])
        imgIdx = int(line[1])
        h,w,ch = img.shape
        if h>w:
            img = np.lib.pad(img,((0,0),(pad_width,pad_width),(0,0)),'constant',constant_values=0)
        elif w>h:
            img = np.lib.pad(img,((pad_width,pad_width),(0,0),(0,0)),'constant',constant_values=0)
        h,w,ch = img.shape
        print (line[0])
        ax.imshow(img)
    ax.axis('off')
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    dst = cv2.warpAffine(img, M, (w,h))
    if save:
        cropped = dst[int(h/2.-r-b/2.): int(h/2.-r+b/2.), int((w-a)/2.): int((w+a)/2.)]
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.imshow(cropped)
        fig2.show()
        picName = "/home/veerachart/Python-dir/PIROPO_annotated/omni_1A/omni1A_training/%06d_%02d.jpg" % (imgIdx, personId)
        plt.imsave(picName,cropped)
        print ("Saved")
        try:        
            data = "%s,%d,%d,%d,%d,%d,%d,%.6f" % (currentImg, imgIdx, personId, center[0]-pads[0], center[1]-pads[1], a, b, angle)
            print (data)
            writer.writerow(data.split(','))
        except csv.Error as e:
            sys.exit('File %s, line %d: %s') % (newFile, writer.line_num, e)
    cv2.rectangle(dst,(int((w-a)/2.), int(h/2.-r-b/2.)), (int((w+a)/2.), int(h/2.-r+b/2.)), (0,255,0), 2)
    M = cv2.getRotationMatrix2D((w/2, h/2), -angle, 1)
    dst = cv2.warpAffine(dst, M, (w,h))
    ax.imshow(dst)
    plt.draw()


def OnClick(event):
    global center, a, b, r, angle
    center[0] = event.xdata
    center[1] = event.ydata
    angle = np.arctan2(center[0]-w/2, h/2-center[1]) * 180./np.pi
    r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
    Redraw()

def OnKey(event):
    global center, a, b, r, angle, imgIdx, personId, w, h
    key = event.key
    save = False
    newImg = False
    if key == "up":
        a += 1      # Larger window
        b = a
    elif key == "down":
        a -= 1      # Smaller window
        b = a
    elif key == "right":
        #imgIdx += 1     # Next frame
        newImg = True
    elif key == "left":
        #imgIdx -= 1     # Previous frame
        newImg = True
    elif key == "w":
        center[1] += 1  # +Y
        r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
        angle = np.arctan2(center[0]-w/2, h/2-center[1]) * 180./np.pi
    elif key == "s":
        center[1] -= 1  # -Y
        r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
        angle = np.arctan2(center[0]-w/2, h/2-center[1]) * 180./np.pi
    elif key == "d":
        center[0] += 1  # +X
        r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
        angle = np.arctan2(center[0]-w/2, h/2-center[1]) * 180./np.pi
    elif key == "a":
        center[0] -= 1  # +X
        r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
        angle = np.arctan2(center[0]-w/2, h/2-center[1]) * 180./np.pi
    elif key == "enter":
        # OK with the current crop. Extract and save
        save = True
    elif key == "p":
        personId += 1
        print ("Current ID: ", str(personId))
    elif key == "o":
        personId -= 1
        print ("Current ID: ", str(personId))
    elif key == "q":
        annotateFile.close()
        plt.close('all')
    Redraw(save, newImg)

ax.axis('off')
cid_up = fig.canvas.mpl_connect('button_press_event', OnClick)
cid_key = fig.canvas.mpl_connect('key_press_event', OnKey)
ax.imshow(img)
Redraw(False, False)
plt.show()