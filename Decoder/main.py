import audioread
import pyaudio
import wave

import cv2
import os
import numpy
import matplotlib.pyplot as plt
from PIL import ImageEnhance
from skimage.morphology import skeletonize, thin
import hashlib
import pickle

from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
import binascii
import codecs

ciphered=[]
ivs=[]

def removedot(invertThin):
    temp0 = numpy.array(invertThin[:])
    temp0 = numpy.array(temp0)
    temp1 = temp0/255
    temp2 = numpy.array(temp1)
    temp3 = numpy.array(temp2)
    
    enhanced_img = numpy.array(temp0)
    filter0 = numpy.zeros((10,10))
    W,H = temp0.shape[:2]
    filtersize = 6
    
    for i in range(W - filtersize):
        for j in range(H - filtersize):
            filter0 = temp1[i:i + filtersize,j:j + filtersize]

            flag = 0
            if sum(filter0[:,0]) == 0:
                flag +=1
            if sum(filter0[:,filtersize - 1]) == 0:
                flag +=1
            if sum(filter0[0,:]) == 0:
                flag +=1
            if sum(filter0[filtersize - 1,:]) == 0:
                flag +=1
            if flag > 3:
                temp2[i:i + filtersize, j:j + filtersize] = numpy.zeros((filtersize, filtersize))

    return temp2


def get_descriptors(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)
    img = numpy.array(img, dtype=numpy.uint8)
    # Threshold
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # Normalize to 0 and 1 range
    img[img == 255] = 1
    
    #Thinning
    skeleton = skeletonize(img)
    keleton = numpy.array(skeleton, dtype=numpy.uint8)
    skeleton = removedot(skeleton)
    # Harris corners
    harris_corners = cv2.cornerHarris(img, 3, 3, 0.04)
    harris_normalized = cv2.normalize(harris_corners, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
    threshold_harris = 125
    # Extract keypoints
    keypoints = []
    for x in range(0, harris_normalized.shape[0]):
    	for y in range(0, harris_normalized.shape[1]):
    		if harris_normalized[x][y] > threshold_harris:
    			keypoints.append(cv2.KeyPoint(y, x, 1))
    # Define descriptor
    orb = cv2.ORB_create()
    # Compute descriptors
    _, des = orb.compute(img, keypoints)
    return (keypoints, des)


def fpmain():
    img1 = cv2.imread("./fp1.jpeg", cv2.IMREAD_GRAYSCALE)
    kp1, des1 = get_descriptors(img1)
    
    nzarr = des1[numpy.nonzero(des1)]
    finalstr = ""
    for i in range(16):
        strr = hex(nzarr[i])[2:]
        if len(strr)==1:
            strr = "0"+ strr
        finalstr+= strr
    return(finalstr)

def decrypt(key, iv, ciphertext):
    key_bytes = 32
    assert len(key) == key_bytes

    iv_int = int(codecs.encode(iv,'hex'), 16) 
    ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)

    aes = AES.new(key, AES.MODE_CTR, counter=ctr)

    plaintext = aes.decrypt(ciphertext)
    return plaintext

with open('../Encoder/encoded.txt','rb') as f:
    for i in f:
        ciphered.append(i)

with open('../Encoder/ivs.txt','rb') as f:
    for i in f:
        ivs.append(i)

with open('../Encoder/config.dictionary', 'rb') as config_dictionary_file:
    decodd = pickle.load(config_dictionary_file)        

decoded=[]
key=fpmain()
for i in decodd.keys():
    decode = decrypt(key,i,decodd[i])
    decoded.append(decode)

print(decoded)