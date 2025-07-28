import numpy as np
import cv2
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
#tk.Tk().withdraw()



class NoiseImage:
    def __init__(self, imagePath=""):
        if not imagePath == "":
            self.fullColor = cv2.imread(imagePath)
            self.blue, self.green, self.red = cv2.split(self.fullColor)
            self._tkImage = []

    @property
    def tkImage(self):
        self.getNoises()
        return ImageTk.PhotoImage(image=(
            Image.fromarray(self.mergedNoiseTK)
        ))

    def openFileDialog(self):
        fn = askopenfilename()
        self.fileName = fn
        self.__init__(fn)
        return self

    def getNoises(self, R=True, G=True, B=True):
        blueBlurred, greenBlurred, redBlurred = (cv2.GaussianBlur(i, (5, 5), 0) for i in (self.blue, self.green, self.red)) # generator expression to individually blur each channel
        self.blueNoise, self.greenNoise, self.redNoise = (cv2.subtract(i[0], i[1]) for i in zip((self.blue, self.green, self.red), (blueBlurred, greenBlurred, redBlurred))) # generator expression that subracts the blurred channel from the original to get the noise
        self.mergedNoise = cv2.merge((self.blueNoise*B, self.greenNoise*G, self.redNoise*R))
        self.mergedNoiseTK = cv2.merge((self.redNoise*R, self.greenNoise*G, self.blueNoise*B))

# miscellaneous functions ///

def updateImage():
    displayedImage.configure(image=currentImage)

# tkinter button commands ///

def selectImageButtonCommand():
    global currentImage
    im = NoiseImage().openFileDialog()
    fileNameLbl.configure(text=im.fileName)
    currentImage = im.tkImage
    if "displayedImage" in globals():
        updateImage()

def channelButtonCommand(channel):
    if rgb[channel]:
        if channel == "r":
            redBtn.configure(bg="grey")
        elif channel == "g":
            greenBtn.configure(bg="grey")
        elif channel == "b":
            blueBtn.configure(bg="grey")
        rgb[channel] = False
    else:
        if channel == "r":
            redBtn.configure(bg="red")
        if channel == "g":
            greenBtn.configure(bg="green")
        if channel == "b":
            blueBtn.configure(bg="blue")
        rgb[channel] = True
    updateImage()

# defining tkinter gui underneath ///

global currentImage

global rgb
rgb = {"r" : True, "g" : True, "b" : True}

root = tk.Tk()
root.title("Noise Analyzer")
root.geometry("800x600")
root.resizable(True, True)

selectImageBtn = tk.Button(root, text="Select Image", command=lambda: selectImageButtonCommand())
redBtn = tk.Button(root, text="Red", command=lambda: channelButtonCommand("r"), bg="red")
greenBtn = tk.Button(root, text="Green", command=lambda: channelButtonCommand("g"), bg="green")
blueBtn = tk.Button(root, text="Blue", command=lambda: channelButtonCommand("b"), bg="blue")

fileNameLbl = tk.Label(root, text="")

selectImageButtonCommand()
displayedImage = tk.Label(root, image=currentImage)

# displaying widgets with grid ///
selectImageBtn.grid(row=1, column=0, pady=2)
redBtn.grid(row=1, column=1, pady=2)
greenBtn.grid(row=1, column=2, pady=2)
blueBtn.grid(row=1, column=3, pady=2)

fileNameLbl.grid(row=0, column=0, pady=2, sticky="snw", columnspan=4)

displayedImage.grid(row=2, column=0, columnspan=4)

root.mainloop()