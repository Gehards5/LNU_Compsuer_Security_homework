from os import path
from tkinter import *
from tkinter import messagebox, filedialog
from decrypt_encrypt import dec_rail_fence, dec_subst_cypher
from decrypt_encrypt import enc_rail_fence, enc_subst_cypher

root: Tk = Tk()
path1 = StringVar()
path1.set(str(path.dirname(path.realpath(__file__))))

root.title("Information encryption software")
label1 = Label(
    root,
    text="Welcome to your safe information program. Please choose an action!").\
    pack()
label2 = Label(
    root,
    text="Which one you want to do today?").\
    pack()
label3 = Label(
    root,
    text="WARNING - after pressing button").\
    pack()
label4 = Label(
    root,
    text="You will be immediately asked to").\
    pack()
label5 = Label(
    root,
    text="select file you want to work with!").\
    pack()


def response(encryption: bool):
    if encryption:
        process = "Encryption"
    else:
        process = "Decryption"
    response = messagebox.askyesno(
        process + " Finished",
        "Do you want to do another procedure?")
    if response:
        msg_label = Label(
            root,
            text="Don't close this window!") \
            .pack()
    if not response:
        msg_label3 = Label(
            root,
            text="Thank you for using this program!") \
            .pack()
        msg_label4 = Label(
            root,
            text="Please, close all windows!") \
            .pack()


def substitution_gui(encryption: bool):
    if encryption:
        process = "Encryption"
    else:
        process = "Decryption"
    
    top1 = Toplevel()
    top1.title("Mono-alphabetic Substitution " + process + " guide")
    # noinspection PyUnusedLocal
    
    sub_label1 = Label(
        top1,
        text="You already have chosen file you work with!") \
        .pack()
    sub_label2 = Label(
        top1,
        text="Write alphabet to substitute text") \
        .pack()
    sub_label3 = Label(
        top1,
        text="Alphabet should be uppercase and 26 letters long") \
        .pack()
    sub_label9 = Label(
        top1,
        text="If alphabet won't be unique letters, encrypted file will become useless!") \
        .pack()
    sub_entry1 = Entry(top1, width=40)
    sub_entry1.pack()
    sub_entry1.insert(0, "NEWPRAVDBGHJIQXYZFUCKLMOST")
    
    def my_click(encryption: bool):
        txt1 = "Line span: " + sub_entry1.get()
        sub_label7 = Label(top1, text=txt1)
        sub_label7.pack()
        
        if encryption:
            cypher: str = sub_entry1.get()
            cypher = cypher.upper()
            # print(len(cypher))
            if len(cypher) == 26:
                enc_key: dict = {}
                for w in range(26):
                    enc_key.update({chr(65 + w): cypher[w]})
                    enc_key.update({chr(97 + w): chr(ord(cypher[w]) + 32)})
                    # chr(ord(chr1) + 32)
                enc_subst_cypher(top1.filename.name, enc_key)
            else:
                print("Input wrong. Try again!")
        else:
            cypher: str = sub_entry1.get()
            cypher = cypher.upper()
            # print(len(cypher))
            if len(cypher) == 26:
                enc_key: dict = {}
                for w in range(26):
                    enc_key.update({cypher[w]: chr(65 + w)})
                    enc_key.update({chr(ord(cypher[w]) + 32): chr(97 + w)})
                    # chr(ord(chr1) + 32) chr(97 + w)
                dec_subst_cypher(top1.filename.name, enc_key)
            else:
                print("Input wrong. Try again!")
        response(encryption)
    
    top1.filename = filedialog.askopenfile(
        initialdir=path1.get(),
        title="Select your file",
        filetypes=(("text files", "*.txt"), ("all files", "*.*"))
    )
    sub_button = Button(
        top1,
        text="Perform " + process,
        command=lambda: my_click(encryption)) \
        .pack()
    sub_label4 = Label(
        top1,
        text="This is file location:") \
        .pack()
    sub_label5 = Label(
        top1,
        text=top1.filename.name) \
        .pack()
    sub_label6 = Label(
        top1,
        text="Close this window after you finish the process") \
        .pack()


def rail_fence_gui(encryption: bool):
    if encryption:
        process = "Encryption"
    else:
        process = "Decryption"
    
    top = Toplevel()
    top.title("Rail Fence " + process + " guide")
    # noinspection PyUnusedLocal

    rail_label1 = Label(
        top,
        text="You already have chosen file you work with!")\
        .pack()
    rail_label2 = Label(
        top,
        text="Choose your expansion rate:") \
        .pack()
    rail_entry1 = Entry(top, width=10)
    rail_entry1.pack()
    rail_entry1.insert(0, "5")
    rail_label3 = Label(
        top,
        text="Choose your starting position:") \
        .pack()
    rail_entry2 = Entry(top, width=10)
    rail_entry2.pack()
    rail_entry2.insert(0, "2")
    
    def my_click(encryption: bool):
        txt1 = "Line span: " + rail_entry1.get()
        rail_label7 = Label(top, text=txt1)
        rail_label7.pack()
        txt2 = "Starting position: " + rail_entry2.get()
        rail_label8 = Label(top, text=txt2)
        rail_label8.pack()
        if encryption:
            enc_rail_fence(int(rail_entry2.get()), int(rail_entry1.get()), top.filename.name)
        else:
            dec_rail_fence(int(rail_entry2.get()), int(rail_entry1.get()), top.filename.name)
        response(encryption)
       
    top.filename = filedialog.askopenfile(
        initialdir=path1.get(),
        title="Select your file",
        filetypes=(("text files", "*.txt"), ("all files", "*.*"))
    )
    rail_button = Button(
        top,
        text="Perform " + process,
        command=lambda: my_click(encryption))\
        .pack()
    rail_label4 = Label(
        top,
        text="This is file location:") \
        .pack()
    rail_label5 = Label(
        top,
        text=top.filename.name)\
        .pack()
    rail_label6 = Label(
        top,
        text="Close this window after you finish the process") \
        .pack()


btn1 = Button(
    root,
    text="Encrypt file with Rail fence cypher",
    command=lambda: rail_fence_gui(True)) \
    .pack()

btn2 = Button(
    root,
    text="Decrypt file from Rail fence cypher",
    command=lambda: rail_fence_gui(False))\
    .pack()


btn3 = Button(
    root,
    text="Encrypt file with Substitution cypher",
    command=lambda: substitution_gui(True))\
    .pack()

btn4 = Button(
    root,
    text="Decrypt file from Substitution cypher",
    command=lambda: substitution_gui(False))\
    .pack()

root.mainloop()
