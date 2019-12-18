from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog, messagebox
import cv2
import Client_class as client
import os
import numpy as np


class SendImage(object):
    panelA = None
    panelB = None
    i = 0
    imgPathTable = []
    root = None

    def __init__(self, window, client):
        self.client = client
        self.root = window
        self.name = None

        btnBack = Button(self.root, text="Back", command=self.destroyWindow)
        btnBack.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btnSel = Button(self.root, text="Select an image", command=self.select_image)
        btnSel.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btnSend = Button(self.root, text="Approve image", command=self.approve)
        btnSend.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btnRight = Button(self.root, text=">", command=self.iterate_right)
        btnRight.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btnLeft = Button(self.root, text="<", command=self.iterate_left)
        btnLeft.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")


    def destroyWindow(self):
        self.root.destroy()

    def approve(self):
       self.client.approve(self.name)

    def select_image(self):
        # reset i
        self.i = 0

        # open a file chooser dialog and allow the user to select an input
        # image
        images = filedialog.askopenfilenames()
        self.imgPathTable = self.root.tk.splitlist(images)
        paths = self.imgPathTable

        # ensure a file path was selected
        if len(paths) > 0:

            # load the image from disk, convert it to grayscale, and detect
            # edges in it
            image = cv2.imread(paths[self.i])
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            edged = cv2.Canny(gray, 50, 100)

            # OpenCV represents images in BGR order; however PIL represents
            # images in RGB order, so we need to swap the channels
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # convert the images to PIL format...
            image = Image.fromarray(image)
            edged = Image.fromarray(edged)

            # Send to server
            self.name = ""
            pt = os.path.split(paths[self.i])
            print(pt[1])

            for j in pt[1]:
                if str(j) == '.':
                    break
                else:
                    self.name = self.name + str(j)
            print(self.name)
            if os.path.exists("org.jpg"):
                os.remove("org.jpg")
            if os.path.exists("edged.jpg"):
                os.remove("edged.jpg")
            edged.save("edged.jpg")
            image.save("org.jpg")
            self.client.sendimage("org.jpg", self.name)
            self.client.sendcloud("edged.jpg", self.name)
            if os.path.exists("edged.jpg"):
                os.remove("edged.jpg")
            if os.path.exists("org.jpg"):
                os.remove("org.jpg")

            # ...and then to ImageTk format
            image = ImageTk.PhotoImage(image)
            edged = ImageTk.PhotoImage(edged)

            # if the panels are None, initialize them
            if self.panelA is None or self.panelB is None:
                # the first panel will store our original image
                self.panelA = Label(self.root, image=image)
                self.panelA.image = image
                self.panelA.pack(side="left", padx=10, pady=10)

                # while the second panel will store the edge map
                self.panelB = Label(self.root, image=edged)
                self.panelB.image = edged
                self.panelB.pack(side="right", padx=10, pady=10)

            # otherwise, update the image panels
            else:
                # update the panels
                self.panelA.configure(image=image)
                self.panelB.configure(image=edged)
                self.panelA.image = image
                self.panelB.image = edged

    def iterate_right(self):
        if self.i < len(self.imgPathTable) - 1:
            self.i = self.i + 1

            image = cv2.imread(self.imgPathTable[self.i])

            # load the image from disk, convert it to grayscale, and detect
            # edges in it
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            edged = cv2.Canny(gray, 50, 100)

            # OpenCV represents images in BGR order; however PIL represents
            # images in RGB order, so we need to swap the channels
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # convert the images to PIL format...
            image = Image.fromarray(image)
            edged = Image.fromarray(edged)
            # ...and then to ImageTk format
            image = ImageTk.PhotoImage(image)
            edged = ImageTk.PhotoImage(edged)

            # if the panels are None, initialize them
            if self.panelA is None or self.panelB is None:
                # the first panel will store our original image
                self.panelA = Label(self.root, image=image)
                self.panelA.image = image
                self.panelA.pack(side="left", padx=10, pady=10)

                # while the second panel will store the edge map
                self.panelB = Label(self.root, image=edged)
                self.panelB.image = edged
                self.panelB.pack(side="right", padx=10, pady=10)

            # otherwise, update the image panels
            else:
                # update the panels
                self.panelA.configure(image=image)
                self.panelB.configure(image=edged)
                self.panelA.image = image
                self.panelB.image = edged
        else:
            messagebox.showerror("Error", "Out of range")

    def iterate_left(self):
        if self.i > 0:
            self.i = self.i - 1

            image = cv2.imread(self.imgPathTable[self.i])

            # load the image from disk, convert it to grayscale, and detect
            # edges in it
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            edged = cv2.Canny(gray, 50, 100)

            # OpenCV represents images in BGR order; however PIL represents
            # images in RGB order, so we need to swap the channels
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # convert the images to PIL format...
            image = Image.fromarray(image)
            edged = Image.fromarray(edged)
            # ...and then to ImageTk format
            image = ImageTk.PhotoImage(image)
            edged = ImageTk.PhotoImage(edged)

            # if the panels are None, initialize them
            if self.panelA is None or self.panelB is None:
                # the first panel will store our original image
                self.panelA = Label(self.root, image=image)
                self.panelA.image = image
                self.panelA.pack(side="left", padx=10, pady=10)

                # while the second panel will store the edge map
                self.panelB = Label(self.root, image=edged)
                self.panelB.image = edged
                self.panelB.pack(side="right", padx=10, pady=10)

            # otherwise, update the image panels
            else:
                # update the panels
                self.panelA.configure(image=image)
                self.panelB.configure(image=edged)
                self.panelA.image = image
                self.panelB.image = edged
        else:
            messagebox.showerror("Error", "Out of range")


class Frames(object):
    root = None
    textentryLogin = None
    textentryPassword = None
    buttonLogin = None
    panelA = None


    def __init__(self):
        self.root = Tk()


    def openImage(self):
        None

    # Wysyłanie obrazów
    def sendImage(self):
        newwin = Toplevel(self.root)
        siwin = SendImage(newwin, self.client)

    # TODO: Zrobić odbieranie obrazów
    def getImage(self):
        choices = self.client.getall()
        print(choices)
        if len(choices) > 0:
            newwin = Toplevel(self.root)
            mainframe = Frame(newwin)
            mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
            mainframe.columnconfigure(0, weight=1)
            mainframe.rowconfigure(0, weight=1)
            mainframe.pack(pady=100, padx=100)

            # Create a Tkinter variable
            tkvar = StringVar(newwin)

            # TODO: funkcja zwracająca obrazy do słownika choices

            tkvar.set('')  # set the default option

            popupMenu = OptionMenu(mainframe, tkvar, *choices)
            Label(mainframe, text="Choose a file").grid(row=1, column=1)
            popupMenu.grid(row=2, column=1)

            imgwin = Toplevel(newwin)
        else:
            messagebox.showerror("Error","No available pictures")

        # TODO: Funkcja wyświetlająca dane
        def change_dropdown(*args):
            imgname = tkvar.get()
            image = self.client.ReciveImage(imgname)
            image2 = self.client.ReciveCloud(imgname)
            cv2.imshow(imgname + "Cloud",image2)
            cv2.imshow(imgname,image)
            # image = cv2.imread()  # TODO: Wczytać odpowieni obraz (nie można podać jako argument funkcji)
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # image = Image.fromarray(image)

            # if self.panelA is None:
            #     self.panelA = Label(imgwin, image=image)
            #     self.panelA.image = image
            #     self.panelA.pack(side="left", padx=10, pady=10)
            # else:
            #     self.panelA.configure(image=image)
            #     self.panelA.image = image

        # link function to change dropdown
        tkvar.trace('w', change_dropdown)

    # TODO: Zrobić wysyłanie SQLa
    def sendQuery(self):
        newwin = Toplevel(self.root)

    # TODO: Zrobić walidację użytkowników
    def loginButton(self):
        loginname = self.textentryLogin.get()
        password = self.textentryPassword.get()
        self.client = client.Client(loginname, password)
        if self.client.auth():
            for widget in self.root.winfo_children():
                widget.destroy()

            # Układ przycisków menu głównego
            Label(self.root, text="Please choose option:").grid(row=0, column=0, sticky=W)
            button1 = Button(self.root, text="send images", command=self.sendImage)
            button1.place(x=75, y=35, width=100, height=25)
            button2 = Button(self.root, text="get images", command=self.getImage)
            button2.place(x=75, y=65, width=100, height=25)
            button3 = Button(self.root, text="SQL query", command=self.sendQuery)
            button3.place(x=75, y=95, width=100, height=25)

    # Otwiera ekran logowania
    def mainFrame(self):
        self.root.title('Main menu')
        self.root.geometry("250x200")
        self.root.resizable(0, 0)
        loginInfo = Label(self.root, text="Please enter your account data:")
        loginInfo.grid(row=0, column=0, sticky=W)
        self.textentryLogin = Entry(self.root, width=30, bg="white")
        self.textentryLogin.grid(row=1, column=0, sticky=W)
        self.textentryPassword = Entry(self.root, width=30, bg="white", show="*")
        self.textentryPassword.grid(row=2, column=0, sticky=W)
        self.buttonLogin = Button(self.root, text="Submit", command=self.loginButton)
        self.buttonLogin.place(x=75, y=65, width=100, height=25)
        # button1 = Button(root, text="send images", command=self.sendImage)
        # button1.place(x=75, y=35, width=100, height=25)