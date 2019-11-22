import cv2
import sys
import easygui
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import*


"""def char_generator():
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

  print(decode_image())


if __name__ == "__main__":
    main()
"""


class SampleApp(tk.Tk):
  def __init__(self):
    tk.Tk.__init__(self)
    self._frame = None
    self.switch_frame(StartPage)


  def switch_frame(self, frame_class):
    new_frame = frame_class(self)

    if self._frame is not None:
      self._frame.destroy()
    self._frame = new_frame
    self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
      tk.Frame.__init__(self, master)

      label = tk.Label(self, text="Please choose a function", bg='dark gray', font=("Times", 20, 'bold'))
      label.pack(side=RIGHT, expand=True)
      #tk.Label(self, text="Start page", font=('Times', 18, "bold")).pack(side="top", fill="x", pady=5)
      Button1 = tk.Button(self, text="Go to page one",
                command=lambda: master.switch_frame(PageOne)).place(x=0,y=10)
      #Button1.place(x=0,y=10)
      #tk.Button(self, text="Go to page two",
      #          command=lambda: master.switch_frame(PageTwo)).pack()


class PageOne(tk.Frame):
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    tk.Frame.configure(self, bg='blue')
    tk.Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="left", fill="x", pady=5)
    tk.Button(self, text="Go back to start page",
              command=lambda: master.switch_frame(StartPage)).pack()




if __name__ == "__main__":
    window = SampleApp()
    window.geometry("1000x500")
    window.title("Steganography Assignment")
    window.config(background='Dark gray')
    window.mainloop()
