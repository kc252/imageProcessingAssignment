import cv2
import sys
import easygui
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import ttk


def char_generator():
    n = str(input("Enter a message to hide: "))
    for c in n:
        yield ord(c)


def get_image():
    f = easygui.fileopenbox()
    I = cv2.imread(f)
    return I


def gcd(x, y):
    while (y):
        x, y = y, x % y

    return x


def encode_image():
    img = get_image()
    msg_gen = char_generator()
    pattern = gcd(len(img), len(img[0]))
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (i + 1 * j + 1) % pattern == 0:
                try:
                    img[i - 1][j - 1][0] = next(msg_gen)
                except StopIteration:
                    img[i - 1][j - 1][0] = 0
                    return img


def decode_image():
    img = get_image()
    pattern = gcd(len(img), len(img[0]))
    message = ''
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (i - 1 * j - 1) % pattern == 0:
                if img[i - 1][j - 1][0] != 0:
                    message = message + chr(img[i - 1][j - 1][0])
                else:
                    return message


buttons = ["Encode", "Decode", "Exit"]


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


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        Label(self, text="Please choose a function", bg='dark gray', font=("Times", 20, 'bold'))
        for i in range(len(buttons)):
            Button(self, background="white", text=buttons[i], command=lambda: master.switch_frame(), height=15, width=15).grid(
                row=i, column=0)
            self.rowconfigure(i, weight=1)

        self.grid(row=0, column=0, sticky="nesw")
        sep = ttk.Separator(self, orient="vertical")
        sep.rowconfigure(0, weight=1)
        sep.columnconfigure(1, weight=1)
        sep.grid(row=0, column=1, sticky="new")


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='blue')
        tk.Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="left", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

#class PageTwo(tk.Frame):



class kill(tk.Frame):
    tk.Frame.destroy()




if __name__ == "__main__":
    # img = encode_image()
    # print "Image Encoded Sucessfully"
    # cv2.imwrite("output.jpeg", img)

    # print(decode_image())

    window = SampleApp()
    window.geometry("1000x500")
    window.title("Steganography Assignment")
    window.config(background='Dark gray')
    window.rowconfigure(0, weight=1)
    window.mainloop()
