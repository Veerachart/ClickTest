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

last_idx = 0        # Last idx in previous run --- for the case that you can't finish labeling in one time
global center, a, b, r, angle, fig, ax, imgIdx, img, personId, direction
#img = plt.imread('/home/veerachart/Dropbox/Todai_Research/Human-fisheye.jpg')
#img = cv2.imread('/home/veerachart/Dropbox/Todai_Research/Human-fisheye.jpg')
### PIROPO Dataset
camera = 'omni_1A/'
imgSet = 'omni1A_training'
imgDir = '/home/veerachart/Datasets/Dataset_PIROPO/'+ camera + camera + imgSet
groundTruthName = '/home/veerachart/Datasets/Dataset_PIROPO/' + camera + camera + 'Ground_Truth_Annotations/groundTruth_'+ imgSet + '.csv'
labelName = '/home/veerachart/Datasets/PIROPO_annotated/' + camera + imgSet + 'direction_label.csv'
groundTruthFile = open(groundTruthName, 'rb')
reader = csv.reader(groundTruthFile, delimiter=',')
if last_idx:        # something other than zero, then continue from previous file
    labelFile = open(labelName, 'a')
    print ("Starting from index: " + str(last_idx))
else:
    labelFile = open(labelName, 'wb')
writer = csv.writer(labelFile)
#writer.writerow('figname,idx,person_id,position_x,position_y,width,height,angle'.split(','))

imgList = []
for path in os.listdir(imgDir):
    imgList.append(path)
imgList.sort()

line = reader.next()
imgIdx = 0
idxOffset = int(line[0])
while int(line[0]) < last_idx or (int(line[1]) == 0 and int(line[2]) == 0):
    try:        
        data = "%d,%d,%d,%d,%d,%d,%d" % (imgIdx+idxOffset, -1, int(line[1]), int(line[2]), -1, -1, -1)
        writer.writerow(data.split(','))
    except csv.Error as e:
        sys.exit('File %s, line %d: %s') % (labelFile, writer.line_num, e)
    line = reader.next()
    imgIdx += 1
print (line[0])

img = plt.imread(imgDir+'/'+imgList[imgIdx])
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
center = [int(line[1])+pads[0], int(line[2])+pads[1]]
a = 20
b = a
r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
angle = np.arctan2(center[0]-w/2, h/2-center[1]) * 180./np.pi
personId = 0
direction = 0
fig = plt.figure(figsize=figsize)
ax = fig.add_axes([0,0,1,1])
fig_cropped = plt.figure(figsize=(200/float(dpi), 200/float(dpi)))
ax_cropped = fig_cropped.add_axes([0,0,1,1])
cropped = None

def Redraw(save=False, newImg=False):
    global center, a, b, r, angle, fig, img, personId, direction, w, h, imgIdx
    ax.cla()
    ax_cropped.cla()
    
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    dst = cv2.warpAffine(img, M, (w,h))
    cropped = dst[int(h/2.-r-b/2.): int(h/2.-r+b/2.), int((w-a)/2.): int((w+a)/2.)]
    draw = cv2.resize(cropped, (200,200))
    if save:
        try:        
            data = "%d,%d,%d,%d,%d,%d,%d" % (imgIdx+idxOffset, personId, center[0]-pads[0], center[1]-pads[1], a, b, direction)
            writer.writerow(data.split(','))
        except csv.Error as e:
            sys.exit('File %s, line %d: %s') % (labelFile, writer.line_num, e)
        picName = "/home/veerachart/Datasets/PIROPO_annotated/omni_1A/omni1A_training/with_directions/%06d_%02d.jpg" % (imgIdx+idxOffset, personId)
        plt.imsave(fname=picName,arr=cropped)
    if newImg:
        line = reader.next()
        imgIdx += 1
        while int(line[1]) == 0 and int(line[2]) == 0:
            try:
                data = "%d,%d,%d,%d,%d,%d,%d" % (imgIdx+idxOffset, -1, int(line[1]), int(line[2]), -1, -1, -1)
                writer.writerow(data.split(','))
            except csv.Error as e:
                sys.exit('File %s, line %d: %s') % (labelFile, writer.line_num, e)
            line = reader.next()
            imgIdx += 1
        img = plt.imread(imgDir+'/'+imgList[imgIdx])
        center = [int(line[1])+pads[0], int(line[2])+pads[1]]
        r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
        angle = np.arctan2(center[0]-w/2, h/2-center[1]) * 180./np.pi
        h,w,ch = img.shape
        if h>w:
            img = np.lib.pad(img,((0,0),(pad_width,pad_width),(0,0)),'constant',constant_values=0)
        elif w>h:
            img = np.lib.pad(img,((pad_width,pad_width),(0,0),(0,0)),'constant',constant_values=0)
        h,w,ch = img.shape
        M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
        dst = cv2.warpAffine(img, M, (w,h))
        cropped = dst[int(h/2.-r-b/2.): int(h/2.-r+b/2.), int((w-a)/2.): int((w+a)/2.)]
        draw = cv2.resize(cropped, (200,200))
    ax.axis('off')
    ax_cropped.axis('off')
    cv2.rectangle(dst,(int((w-a)/2.), int(h/2.-r-b/2.)), (int((w+a)/2.), int(h/2.-r+b/2.)), (0,255,0), 2)
    M = cv2.getRotationMatrix2D((w/2, h/2), -angle, 1)
    dst = cv2.warpAffine(dst, M, (w,h))
    cv2.line(dst, (center[0], center[1]), (int(round(center[0]+50*np.cos((angle-direction+90.)*np.pi/180.))),int(round(center[1]+50*np.sin((angle-direction+90)*np.pi/180.)))),(255,0,0))
    ax.imshow(dst)
    fig.canvas.draw_idle()
    cv2.line(draw, (100,100), (int(round(100+100*np.sin(direction*np.pi/180.))),int(round(100+100*np.cos(direction*np.pi/180.)))),(255,0,0))
    ax_cropped.imshow(draw)
    fig_cropped.canvas.draw_idle()


def OnClick(event):
    global center, a, b, r, angle
    center[0] = event.xdata
    center[1] = event.ydata
    angle = np.arctan2(center[0]-w/2, h/2-center[1]) * 180./np.pi
    r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
    Redraw()

def OnKey(event):
    global center, a, b, r, angle, imgIdx, personId, w, h, direction
    key = event.key
    save = False
    newImg = False
    if key == "up":
        a += 1      # Larger window
        b = a
    elif key == "down":
        a -= 1      # Smaller window
        b = a
    if key == 'left':
        direction = (direction+1)%360
    elif key == 'right':
        direction = (direction-1)%360
    #elif key == "right":
    #    #imgIdx += 1     # Next frame
    #    newImg = True
    #elif key == "left":
    #    #imgIdx -= 1     # Previous frame
    #    newImg = True
    elif key == "w":
        center[1] -= 1  # +Y
        r = np.sqrt((h/2-center[1])**2 + (center[0]-w/2)**2)
        angle = np.arctan2(center[0]-w/2, h/2-center[1]) * 180./np.pi
    elif key == "s":
        center[1] += 1  # -Y
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
    elif key == '2':
        direction = 0
    elif key == '3':
        direction = 45
    elif key == '6':
        direction = 90
    elif key == '9':
        direction = 135
    elif key == '8':
        direction = 180
    elif key == '7':
        direction = 225
    elif key == '4':
        direction = 270
    elif key == '1':
        direction = 315
    elif key == "enter":
        # OK with the current crop. Extract and save
        save = True
        newImg = True
    elif key == "p":
        personId += 1
        print ("Current ID: ", str(personId))
    elif key == "o":
        personId -= 1
        print ("Current ID: ", str(personId))
    elif key == "q":
        last_idx = imgIdx+idxOffset
        print ("Stopped at index "+str(last_idx))
        labelFile.close()
        plt.close('all')
        return
    Redraw(save, newImg)
    
    
def OnClickDirection(event):
    global direction
    click_x = event.xdata
    click_y = event.ydata
    direction = int(round(np.arctan2(click_x-100, click_y-100) * 180./np.pi))
    if direction < 0:
        direction += 360
    Redraw(False, False)
    

ax.axis('off')
cid_up = fig.canvas.mpl_connect('button_press_event', OnClick)
cid_key = fig.canvas.mpl_connect('key_press_event', OnKey)
cid_dirclick = fig_cropped.canvas.mpl_connect('button_press_event', OnClickDirection)
cid_dirkey = fig_cropped.canvas.mpl_connect('key_press_event', OnKey)
ax.imshow(img)
Redraw(False, False)
plt.show()