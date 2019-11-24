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


def gcd(a, b):
    # Calculate the Greatest Common Divisor of a and b.
    while b:
        a, b = b, a % b
    return a


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


class Exit(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.quit()

    def quit(self):
        self.master.destroy()
        sys.exit(0)


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        Button(self, background="white", text="Encode", command=lambda: master.switch_frame(PageOne), height=15,
               width=15).grid(row=0, column=0)
        self.rowconfigure(0, weight=1)

        Button(self, background="white", text="Decode", command=lambda: master.switch_frame(PageTwo), height=15,
               width=15).grid(row=1, column=0)
        self.rowconfigure(1, weight=1)

        Button(self, background="white", text="Exit", command=lambda: master.switch_frame(Exit), height=15,
               width=15).grid(row=2, column=0)
        self.rowconfigure(2, weight=1)

        self.grid(row=0, column=0, sticky="nesw")
        sep = ttk.Separator(self, orient="vertical")
        sep.rowconfigure(0, weight=1)
        sep.columnconfigure(1, weight=1)
        sep.grid(row=0, column=1, sticky="new")


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        Button(self, background="white", text="Image", command=lambda: master.switch_frame(), height=15,
               width=15).grid(row=0, column=0)
        self.rowconfigure(0, weight=1)

        Button(self, background="white", text="Text", command=lambda: master.switch_frame(PageTwo), height=15,
               width=15).grid(row=1, column=0)
        self.rowconfigure(1, weight=1)

        Button(self, background="white", text="Back", command=lambda: master.switch_frame(StartPage), height=15,
               width=15).grid(row=2, column=0)
        self.rowconfigure(2, weight=1)

        self.grid(row=0, column=0, sticky="nesw")
        sep = ttk.Separator(self, orient="vertical")
        sep.rowconfigure(0, weight=1)
        sep.columnconfigure(1, weight=1)
        sep.grid(row=0, column=1, sticky="new")


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        Button(self, background="white", text="Encode", command=lambda: master.switch_frame(PageOne), height=15,
               width=15).grid(row=0, column=0)
        self.rowconfigure(0, weight=1)

        Button(self, background="white", text="Decode", command=lambda: master.switch_frame(PageTwo), height=15,
               width=15).grid(row=1, column=0)
        self.rowconfigure(1, weight=1)

        Button(self, background="white", text="Exit", command=lambda: master.switch_frame(PageOne), height=15,
               width=15).grid(row=2, column=0)
        self.rowconfigure(2, weight=1)

        self.grid(row=0, column=0, sticky="nesw")
        sep = ttk.Separator(self, orient="vertical")
        sep.rowconfigure(0, weight=1)
        sep.columnconfigure(1, weight=1)
        sep.grid(row=0, column=1, sticky="new")


if __name__ == "__main__":
    # encode
    # img = encode_image()
    # print "Image Encoded Sucessfully"
    # cv2.imwrite("output.jpeg", img)

    # decode
    # print(decode_image())

    window = SampleApp()
    window.geometry("1000x500")
    window.title("Steganography Assignment")
    window.config(background='Dark gray')
    window.rowconfigure(0, weight=1)
    window.mainloop()
