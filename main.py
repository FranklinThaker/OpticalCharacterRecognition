# for python2
# from Tkinter import *
# import ttk
# import tkFileDialog as askopenfilename

#for python3
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image
import pytesseract
import numpy as np
import cv2
import os
import sys


from userimageski import UserData

root = Tk(  )

def readFimage():
    path = PathTextBox.get('1.0','end-1c')
    if path:
        im = Image.open(path)
        # text = pytesseract.image_to_string(im, lang = 'eng')
        # Read image with opencv
        img = cv2.imread(path)    
        # Convert to gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply dilation and erosion to remove some noise
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        # Write the image after apply opencv to do some ...
        cv2.imwrite("thres.png", img)
        # Recognize text with tesseract for python
        result = pytesseract.image_to_string(Image.open("thres.png"))
        print(pytesseract.image_to_data(Image.open('thres.png')))
        os.remove("thres.png")
        text = result        
        ResultTextBox.delete('1.0',END)
        ResultTextBox.insert(END,text)


        ##### the following code includes all the steps to get from a raw image to a prediction.
        ##### the working code is the uncommented one. 
        ##### the two pickle models which are passed as argument to the select_text_among_candidates
        ##### and classify_text methods are obviously the result of a previously implemented pipeline.
        ##### just for the purpose of clearness below the code is provided. 
        ##### I want to emphasize that the commented code is the one necessary to get the models trained.
        
        # creates instance of class and loads image    
        user = UserData(path)
        # plots preprocessed imae 
        user.plot_preprocessed_image()
        # detects objects in preprocessed image
        candidates = user.get_text_candidates()
        # plots objects detected
        user.plot_to_check(candidates, 'Total Objects Detected')
        # selects objects containing text
        # maybe_text = user.select_text_among_candidates('linearsvc-hog-fulltrain2-90.pickle')
        # plots objects after text detection
        # user.plot_to_check(maybe_text, 'Objects Containing Text Detected')
        # classifies single characters
        # classified = user.classify_text('linearsvc-hog-fulltrain36-90.pickle')
        # plots letters after classification 
        # user.plot_to_check(classified, 'Single Character Recognition')
        # plots the realigned text
        # user.realign_text()
    else:
        ResultTextBox.delete('1.0',END)
        ResultTextBox.insert(END,"FILE CANNOT BE READ")
    

def OpenFile():
    name = askopenfilename(initialdir="/home/frank/Desktop/OCR_PROJECT/data",
                           filetypes =(("PNG File", "*.png"),("BMP File", "*.bmp"),("JPEG File", "*.jpeg"),("JPG File", "*.jpg")),
                           title = "Choose a file."
                           ) 
    PathTextBox.delete("1.0",END)
    PathTextBox.insert(END,name)
Title = root.title( "Image Reader!")
path = StringVar()

HeadLabel1 = Label(root,text="Image ")
HeadLabel1.grid(row = 1,column = 1,sticky=(E))
HeadLabel2 = Label(root,text=" Reader")
HeadLabel2.grid(row = 1,column = 2,sticky=(W))

InputLabel = Label(root,text = "INPUT IMAGE:")
InputLabel.grid(row=2,column = 1)

BrowseButton = Button(root,text="Browse",command = OpenFile)
BrowseButton.grid(row=2,column=2)

PathLabel = Label(root,text = "Path:")
PathLabel.grid(row = 3,column=1,sticky=(W))

PathTextBox = Text(root,height = 2)
PathTextBox.grid(row = 4,column = 1,columnspan=2)

ReadButton = Button(root,text="READ FROM IMAGE",command = readFimage)
ReadButton.grid(row = 5,column = 2)

DataLabel = Label(root,text = "DATA IN IMAGE:")
DataLabel.grid(row = 6,column=1,sticky=(W))

ResultTextBox = Text(root,height = 6)
ResultTextBox.grid(row = 7,column = 1,columnspan=2)



root.mainloop()
