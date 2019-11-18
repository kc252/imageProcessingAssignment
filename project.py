import cv2
import sys
import easygui
import numpy as np
from matplotlib import pyplot as plt

def char_generator():
  n = str(input("Enter a message to hide: "))
  for c in n:
    yield ord(c)

def get_image():
  f = easygui.fileopenbox()
  I = cv2.imread(f)
  return I

def gcd(x, y):
  while(y):
    x, y = y, x % y

  return x

def encode_image():
  img = get_image()
  msg_gen = char_generator()
  pattern = gcd(len(img), len(img[0]))
  for i in range(len(img)):
    for j in range(len(img[0])):
      if (i+1 * j+1) % pattern == 0:
        try:
          img[i-1][j-1][0] = next(msg_gen)
        except StopIteration:
          img[i-1][j-1][0] = 0
          return img

def decode_image():
  img = get_image()
  pattern = gcd(len(img), len(img[0]))
  message = ''
  for i in range(len(img)):
    for j in range(len(img[0])):
      if (i-1 * j-1) % pattern == 0:
        if img[i-1][j-1][0] != 0:
          message = message + chr(img[i-1][j-1][0])
        else:
          return message


def main():

  #img = encode_image()
  #print "Image Encoded Sucessfully"
  #cv2.imwrite("output.jpeg", img)

  #print decode_image()

if __name__ == "__main__":
	main()