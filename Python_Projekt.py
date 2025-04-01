from tkinter import *
from tkinter import filedialog, messagebox
import smtplib, ssl
from email.message import EmailMessage
import imghdr

file = None

def choose_img():
    global file
    file = filedialog.askopenfilename()
    added.configure(text = file)
    added.configure(font=("Arial", 14, "italic"), fg="blue")
    return file



root = Tk()
root.geometry("600x500")
root.resizable(False, False)
root.title("Adobe Photoshop 1 bit")