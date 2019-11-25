import math
import cv2
import easygui
import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib import pyplot as plt


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
    try:
        rgbImg = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
    except cv2.error:
        print("Incorrect input type, please select an image of appropriate type")
        exit(1)
    return rgbImg


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


# encodeImageToImage(cover,hidden)
def encodeImageToImage(i1, i2):
    x1, y1, z1 = i1.shape
    x2, y2, x2 = i2.shape
    i3 = i1
    if x1 < x2 or y1 < y2:
        print("Incorrect size")
        print(i1.size)
        print(i2.size)
    else:
        print("Correct size")
        #print("Size is X:"+x1+" Y:"+y1)
        for i in range(x1):
            for j in range(y1):
                if i > x2 or j > y2:
                    #print("Outside bounds of Hidden, painting black")
                    i3[i, j] = encodeBits(i1[i, j], (0, 0, 0))
                else:
                    i3[i, j] = encodeBits(i1[i, j], i2[i, j])
                #print(i3[i, j])
        return i3

def decodeImageFromImage(i1):
    i2 = i1
    x1, y1, z1 = i1.shape
    for i in range(x1):
        for j in range(y1):
            i2[i, j] = decodeBits(i1[i, j])
    return i2

#in = colourCover, colourHidden; out = colourEncoded
def encodeBits(coverVal, hiddenVal):
    # convert the cover to binary
    print("##########")
    print(coverVal)
    redBinCover = format(coverVal[0], '08b')
    greenBinCover = format(coverVal[1], '08b')
    blueBinCover = format(coverVal[2], '08b')
    print(redBinCover)
    # cut off the end 2 characters
    redBinCover = redBinCover[:-2]
    greenBinCover = greenBinCover[:-2]
    blueBinCover = blueBinCover[:-2]
    print(redBinCover)

    redBinHidden = format(hiddenVal[0], '08b')
    greenBinHidden = format(hiddenVal[1], '08b')
    blueBinHidden = format(hiddenVal[2], '08b')
    print(redBinHidden[-2:])

    # Add one to the end of the other.
    redBinCover = redBinCover + redBinHidden[-2:]
    greenBinCover = greenBinCover + greenBinHidden[-2:]
    blueBinCover = blueBinCover + blueBinHidden[-2:]
    #print(redBinCover)

    return (int(redBinCover, 2), int(greenBinCover, 2), int(blueBinCover, 2))


def decodeBits(inputVal):
    redBin = format(inputVal[0], '08b')
    greenBin = format(inputVal[1], '08b')
    blueBin = format(inputVal[2], '08b')

    #print(redBin + " " + redBin[:-2])
    redBin = redBin[:-2] + '000000'
    greenBin = greenBin[:-2] + '000000'
    blueBin = blueBin[:-2] + '000000'

    return (int(redBin, 2), int(greenBin, 2), int(blueBin, 2))

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
    print("Image Encoded Successfully")
    cv2.imwrite("output.png", img)

    # decode
    print(decode_image())



    img = get_image()
    img2 = get_image()
    img3 = encodeImageToImage(img,img2)
    img4 = decodeImageFromImage(img3)

    plt.imshow(img3)
    plt.imshow(img4)
    plt.show()

    print(img.size)
    x, y, z = img.shape
    print(x*y*z)

    window = SampleApp()
    window.geometry("1000x500")
    window.title("Steganography Assignment")
    window.config(background='Dark gray')
    window.rowconfigure(0, weight=1)
    window.mainloop()
