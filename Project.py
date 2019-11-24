import math
import cv2
import easygui
import tkinter as tk
from tkinter import *
from tkinter import ttk


def char_generator():
    # getting input from console for our secret message
    n = str(input("Enter a message to hide: "))
    # for each character in the string convert it to unicode numbers and store it in a generator
    # generators feed values in one by one using next()
    for c in n:
        yield ord(c)


def get_image():
    f = easygui.fileopenbox()
    I = cv2.imread(f)
    return I


def gcd(a, b):
    # Calculate the Greatest Common Divisor of a and b.
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def encode_image():
    img = get_image()  # gets our rgb numpy array of the image
    msg_gen = char_generator()  # our unicode values for the message in a generator
    height, width, channels = img.shape  # getting dimensions of the image
    channels -= 1  # taking 1 from 3 to be array friendly
    pattern = gcd(height, width)  # this gets our gcd for the image to gather every nth pixel to embed
    # this ensures that we do not alter each pixel sequentially which would make it obvious that the image was altered
    # so with this method we get a more dispersed alteration
    for i in range(height):  # nested for loop to loop through 2D array -> height pixels
        for j in range(width):  # -> width pixels
            if (i + 1 * j + 1) % pattern == 0:  # if it is divisible by our GCD
                # (adding 1 to iteration to not just write to the first column/row
                # on first iteration of either because 0 % any number is 0)
                try:
                    if channels == -1:  # channels must be 0,1 or 2 value -> RGB
                        channels += 3  # add 3 to -1 to go back to B channel
                    img[i - 1][j - 1][channels] = next(msg_gen)  # adding back the 1 we took away previously
                    # to get our correct row and column
                    channels -= 1  # take 1 away from channels to go to next color channel
                except StopIteration:  # this indicates the final character in our generator
                    img[i - 1][j - 1][channels] = 0  # adding the 1 back and making our terminating character to be 0
                    # (this way in the decoder we can tell when we are on the end of our image
                    return img  # return encoded image


def decode_image():
    img = get_image()  # get image to be decoded
    height, width, channels = img.shape  # getting dimensions of the image
    channels -= 1
    pattern = gcd(height, width)
    message = ''
    for i in range(height):
        for j in range(width):
            if (i - 1 * j - 1) % pattern == 0:
                if img[i - 1][j - 1][channels] != 0:
                    message = message + chr(img[i - 1][j - 1][channels])
                    channels -= 1
                    if channels == -1:
                        channels += 3
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


class DecodePage():
    pass


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        Button(self, background="white", text="Encode", command=lambda: master.switch_frame(EncodePage), height=15,
               width=15).grid(row=0, column=0)
        self.rowconfigure(0, weight=1)

        Button(self, background="white", text="Decode", command=lambda: master.switch_frame(DecodePage), height=15,
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


class EncodePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        Button(self, background="white", text="Image", command=lambda: master.switch_frame(), height=15,
               width=15).grid(row=0, column=0)
        self.rowconfigure(0, weight=1)

        Button(self, background="white", text="Text", command=lambda: master.switch_frame(TextEncodePage), height=15,
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


class TextEncodePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        Button(self, background="white", text="Encode", command=lambda: master.switch_frame(EncodePage), height=15,
               width=15).grid(row=0, column=0)
        self.rowconfigure(0, weight=1)

        Button(self, background="white", text="Decode", command=lambda: master.switch_frame(TextEncodePage), height=15,
               width=15).grid(row=1, column=0)
        self.rowconfigure(1, weight=1)

        Button(self, background="white", text="Exit", command=lambda: master.switch_frame(EncodePage), height=15,
               width=15).grid(row=2, column=0)
        self.rowconfigure(2, weight=1)

        self.grid(row=0, column=0, sticky="new")
        sep = ttk.Separator(self, orient="vertical")
        sep.rowconfigure(0, weight=1)
        sep.columnconfigure(1, weight=1)
        sep.grid(row=0, column=1, sticky="new")


if __name__ == "__main__":
    # encode
    img = encode_image()
    print "Image Encoded Successfully"
    cv2.imwrite("output.png", img)

    # decode
    print(decode_image())

    window = SampleApp()
    window.geometry("1000x500")
    window.title("Steganography Assignment")
    window.config(background='Dark gray')
    window.rowconfigure(0, weight=1)
    window.mainloop()
