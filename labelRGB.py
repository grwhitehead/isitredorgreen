#!/usr/bin/env python3
#coding: utf-8

import sys
from optparse import OptionParser

import numpy as np
import cv2

def labelColor(src, dst, lowerBound, upperBound, text, textColor):
    # create a mask including all pixels within the specified color range
    mask = cv2.inRange(src, lowerBound, upperBound)
    # find contours around clusters of pixels selected in mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(dst, contours, -1, (255, 255, 255), 3)
    # label each contour with the specified text
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            # place label at the centroid of the contour
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.putText(dst, text, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 2, textColor, 4)

def main():
    parser = OptionParser("usage: %prog [options] file")
    parser.add_option("-b", action="store_true", dest="batch", default=False, help="non-interactive batch mode")
    parser.add_option("-w", action="store_true", dest="wait", default=False, help="wait for key press before exit")
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    file = args[0]

    cap = cv2.VideoCapture(file)
    if not cap.isOpened():
        print("Error opening file", file)
    else:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'), frame_rate, (frame_width, frame_height))

        n = 0
        while (True):
            ret, frame = cap.read()
            if not ret:
                break
            n = n+1

            # overlay labels on frame
            dst = frame.copy();
            # colors are BGR
            labelColor(frame, dst, (0, 0, 200), (100, 100, 255), 'R', (0, 0, 255));
            labelColor(frame, dst, (0, 200, 0), (100, 255, 100), 'G', (0, 255, 0));
            labelColor(frame, dst, (200, 0, 0), (255, 100, 100), 'B', (255, 0, 0));
            
            out.write(dst)
            if n == 1:
                cv2.imwrite('output.jpg',dst)
            if not opts.batch:
                cv2.imshow('Frame', dst)
                cv2.waitKey(int(1000/frame_rate))

        print("processed {} frames".format(n))
        
        # wait for key press on still images or very short videos, if not in batch mode
        if not opts.batch and (opts.wait or n < frame_rate):
            print("press any key (in frame window) to exit")
            cv2.waitKey(0)
            
        out.release()
        cap.release()
        
    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
