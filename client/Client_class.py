import socket
import os
from tkinter import Tk
from tkinter import filedialog
import cv2

from tkinter.filedialog import askopenfilename
from PIL import Image
import io




class Client:
    def __init__(self, user, password):
        self.host = '127.0.0.1'
        self.port = 10000
        self.name = user
        self.psw = password
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        self.collection = []

    # logowanie
    def auth(self):
        self.s.sendall(("user::" + self.name + ";password::" + self.psw).encode())
        answer = self.s.recv(4096).decode()
        if answer == "ack::n":
            return False
        if answer == "ack::y":
            return True


    def ReciveImage(self, name):
        self.s.sendall(("getimg::"+name).encode())
        leng = int(self.s.recv(1024).decode())
        gotBytes = 0
        print(leng)
        if os.path.exists("choice.jpg"):
            os.remove("choice.jpg")
        with open('choice.jpg', 'wb') as img:
            while gotBytes != leng:
                data = self.s.recv(1024)
                gotBytes += len(data)
                if not data:
                    break
                img.write(data)
        image = cv2.imread('choice.jpg')
        return image

    def ReciveCloud(self, name):
        self.s.sendall(("getcloud::"+name).encode())
        leng = int(self.s.recv(1024).decode())
        gotBytes = 0
        print(leng)
        if os.path.exists("cloud.jpg"):
            os.remove("cloud.jpg")
        with open('cloud.jpg', 'wb') as img:
            while gotBytes != leng:
                data = self.s.recv(1024)
                gotBytes += len(data)
                if not data:
                    break
                img.write(data)
        image = cv2.imread('cloud.jpg')
        return image

    def approve(self, image):
        if image is not None:
            self.s.sendall(("approve::"+image).encode())

    # funkcja do wybierania i przesyłania zdjęć
    def sendimage(self):
        # wybór zdjęć do wysłania
        image = filedialog.askopenfilenames()
        root = Tk()
        tab = root.tk.splitlist(image)
        if image != "":
            for x in tab:
                myfile = open(x, 'rb')
                bytes = bytearray(myfile.read())
                size = len(bytes)
                size = size.to_bytes(size.bit_length(), byteorder='big')
                self.s.sendall(
                    ("sendimg::" + os.path.basename(myfile.name)).encode())  # wysyłanie komendy i nazwy zdjęcia
                self.s.send(size)  # wysłanie rozmiaru przesyłanego zdjęcia
                answer = self.s.recv(4096)  # odbiór potwierdzenia
                # send image to server
                if answer == b'GOT SIZE':
                    self.s.sendall(bytes)  # wysłanie zdjęcia

                    # check what server send
                    answer = self.s.recv(4096)
                    if answer == b'GOT IMAGE':
                        continue
                    else:
                        return
                else:
                    return
        else:
            print("Error: image not send")

    # wersja bez wyboru(może się przyda)
    # wysyła zdjęcie z argumentu, jako argument przyjmuje wynik funkcji open("ścieżka do zdjęcie")
    def sendimage(self, path, name):
        # print(os.path.basename(myfile.name))
        image = open(path, 'rb')
        bytes = bytearray(image.read())
        size = len(bytes)
        size = size.to_bytes(size.bit_length(), byteorder='big')
        self.s.sendall(("sendimg::" + name).encode())  # wysyłanie komenty i nazwy zdjęcia
        answer = self.s.recv(4096)
        if answer == b'ack':
            self.s.send(size)
            answer = self.s.recv(4096)
            # send image to server
            if answer == b'GOT SIZE':
                self.s.sendall(bytes)

                # check what server send
                answer = self.s.recv(4096)
                if answer == b'GOT IMAGE':
                    None
                else:
                    print("send error")
                    return

    def sendcloud(self, path, name):
        # print(os.path.basename(myfile.name))
        image = open(path, 'rb')
        bytes = bytearray(image.read())
        size = len(bytes)
        size = size.to_bytes(size.bit_length(), byteorder='big')
        self.s.sendall(("sendcloud::" + name).encode())  # wysyłanie komenty i nazwy zdjęcia
        answer = self.s.recv(4096)
        if answer == b'ack':
            self.s.send(size)
            answer = self.s.recv(4096)
            # send image to server
            if answer == b'GOT SIZE':
                self.s.sendall(bytes)

                # check what server send
                answer = self.s.recv(4096)
                if answer == b'GOT IMAGE':
                    None
                else:
                    print("send error")
                    return


    # pobranie zdjęcia po nazwie
    def getimg(self, nazwa):
        self.s.sendall(("getimg::" + nazwa.encode()))
        data = self.s.recv(4096)  # odbiór rozmiaru zjęcia
        size = int.from_bytes(data, "big")
        self.s.sendall(b'GOT SIZE')  # potwierdzenie
        data = self.s.recv(size)  # odbór zdjęcia
        image = Image.open(io.BytesIO(data))
        self.dodaj(image)
        # image.show()
        # image.save(name)
        self.s.sendall(b"GOT IMAGE")

    # pobranie wszystkich zdjęć
    def getall(self):
        self.s.sendall(("getall").encode())
        msg = self.s.recv(99999).decode()
        msg = msg.split("!@")
        print(msg)
        return msg

    # wysyłanie zapytania sql
    def SendSql(self, zapytanie):
        self.s.sendall(("sql::" + zapytanie.encode()))
        anwser = self.recv(4096)
        print(anwser)

    def dodaj(self, zdj):
        self.collection.append(zdj)

    def pokaz(self):
        for x in self.collection:
            image = Image.open(x)
            image.show()

