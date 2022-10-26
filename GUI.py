import pyperclip
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from nCrypt import nCrypt #import the class written in nCrypt.py
import os
nc = nCrypt()#call our class and assign a name
global cwd
cwd = os.path.dirname(os.path.realpath(__file__))
#configure the window
root = Tk()
frame = tk.Frame(root)
root.title("nCrypt GUI")
root.geometry("500x220")
#root.overrideredirect(1)  #not gonna remove window border
root.iconphoto(False, tk.PhotoImage(file=f'{cwd}\icon_TEMP.png'))
global decryptVariable
decryptVariable = tk.StringVar(value="Decrypt")

global notified
notified = False

lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x , y))

#root.overrideredirect(True)

global topMost 
topMost = False
root.attributes('-topmost', topMost)
root.geometry("500x220+500+300")
root.bind('<Button-1>', SaveLastClickPos)
#root.bind('<B1-Motion>', Dragging)

def openFile(event=None):
    
    filetypes = (
        
        ('Unencrypted Files', '*.*'),
        ('All files', '*.*')
    )
    
    global filename
    
    filename = fd.askopenfilename(
        title='Open a file',
        #initialdir='/',
        filetypes=filetypes)
    return filename
    

def openFileDec(event=None):

    filetypes = (
        ('Encrypted Files', '*.aes'),
        ('All files', '*.*')
    )

    global filename

    filename = fd.askopenfilename(
        title='Open a file',
        #initialdir='/',
        filetypes=filetypes)
    #print(filename)
    return filename

    

#configure window styles, using dark theme for GUI
paddings = {'padx': 5, 'pady': 5}
entry_font = {'font': ('Gill Sans MT', 11)}
from tkinter import ttk
s=ttk.Style()
#s.theme_names()
#('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
s.theme_use('clam')
style = ttk.Style(root)
root.tk.call('source', f'{cwd}/theme/azure dark/azure dark.tcl')
style.theme_use('azure')
style.configure("Accentbutton", foreground='white')
style.configure("Togglebutton", foreground='white')



def infoLabel(type="Error", message=None):
    if type == "Error":
        statusbar = tk.Label(root, text=message,
                            bd=1, relief=tk.SUNKEN, anchor=tk.W)
    
    

#configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)

#encoding and decoding entry box variables
encding = ""

decding = ""

typeVar = StringVar(root)
typeVar.set("base64")  # default value
#notified = False
def notifTrue():
    notified = True
def changeEncType(options):
    decryptVariable.set("Decrypt")
    encType = typeVar.get()
    #print(encType)
    if encType == "base64":
        decode["state"] = ACTIVE
        dec1["state"] = NORMAL
        encKey.grid_forget()
        encKeyLabel.grid_forget()
        encode.grid(column=0, row=4, pady=2)
    if encType == "hash":
        encKey.grid_forget()
        encKeyLabel.grid_forget()
        encode.grid(column=0, row=4, pady=2)
        if notified == True:
            show_notif("Hash", "Can't Decrypt Hash")
            notifTrue()
        elif notified == False:
            #print("true")
            pass
        else:
            raise Exception("Variable notified must be true or false")
        
        decode["state"] = DISABLED
        dec1["state"] = DISABLED
    if encType == "cryptocode":
        decode["state"] = ACTIVE
        dec1["state"] = NORMAL
        encode.grid(column=0, row=4, pady=2)
        encKey.grid(row=14, column=1, pady=2)
        encKeyLabel.grid(row=13, column=1)
    if encType == "file encrypt":
        decode["state"] = ACTIVE
        dec1["state"] = NORMAL
        encKey.grid(row=14, column=1, pady=2)
        encKeyLabel.grid(row=13, column=1)
        
    


type = OptionMenu(root, typeVar, "base64", "cryptocode", "file encrypt", "hash",command=changeEncType)
type.grid(row=8, column=1)
#text entry widget
enc1 = Entry(root, textvariable = encding, width=20)
dec1 = Entry(root, textvariable = decding, width=20)
encKey = Entry(root)
# this will arrange entry widgets
enc1.grid(row = 5, column = 0, pady = 2)
encKey.grid(row = 14, column = 1, pady = 2)
dec1.grid(row = 5, column = 3, pady = 2, padx=10)
encKey.grid_forget()

encKeyLabel = tk.Label(root, text="Encryption Key:")
encKeyLabel.grid(row=13, column = 1)
encKeyLabel.grid_forget()

#putting the entry before the functions so they are already defined when called 

import webbrowser

def show_notif(notification):
    middle_text.config(text = notification)
    root.after(3000, lambda: middle_text.config(text = ""))

middle_text = tk.Label(root, text="",
                    bd=1, 
                    #relief=tk.SUNKEN, 
                       anchor=tk.W, padx=5, pady=5)
middle_text.grid(row = 5,column =1)
spacer = tk.Label(root, text="")
spacer.grid(row=6, column=1)
#spacer.grid_forget()
def OpenUrl():
    webbrowser.open_new("https://replit.com/@CodingAndMemes")
link = Button(root, text="replit.com/@CodingAndMemes", command=OpenUrl)
#link.grid(row = 9,column =1)
#functions for the buttons

def enc():
    key = encKey.get()
    
    if not typeVar.get() == "base64" and not typeVar.get() == "hash":
        if key == "":
            show_notif("Error: No Key")
            return
    if typeVar.get() == "base64":
        
        inp1 = enc1.get()
        out1 = nc.base64.encrypt(inp1)
        enc1.delete(0,"end")
        enc1.insert(0, out1)
        decryptVariable.set("Decrypt")
    elif typeVar.get() == "cryptocode":
        key = encKey.get()
        inp1 = enc1.get()
        out1 = nc.cryptoCode.encrypt(inp1, key)
        enc1.delete(0, "end")
        enc1.insert(0, out1)
        decryptVariable.set("Decrypt")
    elif typeVar.get() == "file encrypt":
        key = encKey.get()
        inpFile = openFile()
        #folder_selected = fd.askdirectory(
        #    title="Select a folder to save the file")
        try:
            out1 = nc.fileEncrypt.encrypt(input=inpFile, key=key)
            show_notif("File {inpFile} encrypted")
        except Exception as e:
            print(e)
            #pass
    elif typeVar.get() == "hash":
        input = enc1.get()
        out = nc.hash.hash(input)
        enc1.delete(0, "end")
        enc1.insert(0, out)
        
        
    else:
        pass
        #print("wtf")    

decryptVariable.set("Decrypt")
# folder_selected = filedialog.askdirectory()
    
def dec():
    key = encKey.get()
    if not typeVar.get() == "base64" and not typeVar.get() == "hash":
        if key == "":
            show_notif("Error: No Key")
            return
    inp2 = dec1.get()
    if typeVar.get() == "base64":
        try:
            out2 = nc.base64.decrypt(inp2)
            dec1.delete(0, "end")
            dec1.insert(0, out2)
            decryptVariable.set("Decrypt")
        except:
            decryptVariable.set("Can't Decrypt Plain Text!")
    elif typeVar.get() == "cryptocode":
        try:
            key = encKey.get()
            out2 = nc.cryptoCode.decrypt(inp2, key)
            dec1.delete(0, "end")
            dec1.insert(0, out2)
            decryptVariable.set("Decrypt")
        except:
            decryptVariable.set("Can't Decrypt Plain Text!")
    elif typeVar.get() == "file encrypt":
        key = encKey.get()
        inpFile = openFileDec()
        #folder_selected = fd.askdirectory(title="Select a folder to save the file")
        try:
            decryptVariable.set("Decrypt")
            out1 = nc.fileEncrypt.decrypt(input=inpFile, key=key)
            show_notif(
                f"File {inpFile} decrypted.\nOutput file is {inpFile[:-4]}.\nDeleting {inpFile} in 5 seconds...")
            root.after(5000, lambda: os.remove(inpFile))
        except ValueError:
            show_notif("Unable to decrypt: Wrong Password")
        except:
            pass
        #    print(e)
        #    print("No File Given")
    



class clipboard:
    def encode(self):
        input = enc1.get()
        pyperclip.copy(input)
        return True
    def decode(self):
        try:
            input = dec1.get()
            pyperclip.copy(input)
        except:
            return False
        return True
#button to encode
encode = ttk.Button(root, 
                text="Encrypt",
                command=enc)

encode.grid(column=0, row=4, pady = 2)




decode = ttk.Button(root, 
                    textvariable=decryptVariable,
                command=dec)

decode.grid(column=3, row=4, pady = 2)

root.mainloop()
