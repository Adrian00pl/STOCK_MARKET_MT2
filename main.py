import time
from tkinter import messagebox
from tkinter.ttk import Treeview
import requests
import json
from tkinter import *
import threading
from datetime import datetime
from tkinter import messagebox as mb

przedmioty = []
exit_event = threading.Event()
exit_event.set()
def update(data):
    my_list.delete(0,END)
    for item in data:
        my_list.insert(END, item)

def fill(e):
    txtfld.delete(0,END)
    if my_list.get(my_list.curselection()) != "":
        txtfld.insert(0, my_list.get(my_list.curselection()))

def check(e):
    typed = txtfld.get()
    if typed=='':
        data2 = data
    else:
        data2 = []
        for item in data:
            if typed.lower() in item.lower():
                data2.append(item)
    update(data2)

def dodaj():
    try:
        dane= int(txtfld2.get())
    except ValueError:
        mb.showinfo(title="Alert", message="Wprowadz liczbe")
    zap(my_list.get(my_list.curselection()),dane)

def zmien():
    przedmioty[tree.index(tree.focus())][6]=txtfld2.get()
    tree.delete(*tree.get_children())
    for n in przedmioty:
        tree.insert('', END, values=n)
def zapisz():
    with open('data.json', 'w') as filehandle:
        json.dump(przedmioty, filehandle)
def wczytaj():
    with open('data.json', 'r') as openfile:
        json_object = json.load(openfile)
        przedmioty.clear()
        for k in json_object:
            przedmioty.append(k)
            tree.insert('', END, values=przedmioty[len(przedmioty) - 1])

def zap(przedmiot,cenad):
    przedmioty.append([przedmiot,0,0,0,0,0,cenad])
    tree.insert('', 0, values=przedmioty[len(przedmioty)-1])

def spr():
    while True:
        if exit_event.is_set():
            time.sleep(1)
        else:
            data = pobierz()
            lbl3.config(text="Ostanie odświeżenie: "+str(datetime.now().time()))
            tree.delete(*tree.get_children())
            for n in przedmioty:
                tree.insert('', END, values=(n[0],data[n[0]]["n"]["p"][0]["n"],data[n[0]]["n"]["p"][1]["n"],data[n[0]]["n"]["p"][2]["n"],data[n[0]]["n"]["p"][3]["n"],data[n[0]]["n"]["p"][4]["n"],n[6]))
                if float(n[6]) >= data[n[0]]["n"]["p"][0]["n"] != 0:
                    messagebox.showinfo("", "Przedmiot: " + n[0] + "Cena: " + str(data[n[0]]["n"]["p"][0]["n"]))
                elif float(n[6]) >= data[n[0]]["n"]["p"][1]["n"] != 0:
                    messagebox.showinfo("", "Przedmiot: " + n[0] + "Cena: " + str(data[n[0]]["n"]["p"][1]["n"]))
                elif float(n[6]) >= data[n[0]]["n"]["p"][2]["n"] != 0:
                    messagebox.showinfo("", "Przedmiot: " + n[0] + "Cena: " + str(data[n[0]]["n"]["p"][2]["n"]))
                elif float(n[6]) >= data[n[0]]["n"]["p"][3]["n"] != 0:
                    messagebox.showinfo("", "Przedmiot: " + n[0] + "Cena: " + str(data[n[0]]["n"]["p"][3]["n"]))
                elif float(n[6]) >= data[n[0]]["n"]["p"][4]["n"] != 0:
                    messagebox.showinfo("", "Przedmiot: " + n[0] + "Cena: " + str(data[n[0]]["n"]["p"][4]["n"]))
            time.sleep(60)

def pobierz():
    url = "https://pangeayt2.eu/offshop_exchange_new.php"
    resp = requests.get(url)
    data = json.loads(resp.text)
    return data
data = pobierz()

window=Tk()
window.title('Hello Python')
window.geometry("1300x500+1000+20")

lbl=Label(window, text="Giełda", fg='red', font=("Helvetica", 16))
lbl.place(x=550, y=30)
lbl1=Label(window, text="Szukaj", fg='black', font=("Helvetica", 10))
lbl1.place(x=240, y=90)
lbl2=Label(window, text="Alert", fg='black', font=("Helvetica", 10))
lbl2.place(x=240, y=160)
lbl3=Label(window, text="Ostanie odświeżenie:", fg='black', font=("Helvetica", 10))
lbl3.place(x=600, y=340)

txtfld=Entry(window, text="Szukaj", bd=5, width=50)
txtfld.place(x=100, y=120)
txtfld2=Entry(window, text="Alert", bd=5, width=50)
txtfld2.place(x=100, y=190)


my_list = Listbox(window,width=50)
my_list.place(x=100, y=250)

t1 = threading.Thread(target=spr)
t1.daemon = True
t1.start()
btn=Button(window, text="Dodaj", fg='blue', command=dodaj, width=10)
btn.place(x=460, y=120)
btn1=Button(window, text="Wlacz alerty", fg='blue', command=lambda :[exit_event.clear(),btn5.config(background='green')], width=10)
btn1.place(x=460, y=240)
btn2=Button(window, text="Zapisz", fg='blue', command=zapisz, width=10)
btn2.place(x=460, y=200)
btn3=Button(window, text="Wczytaj", fg='blue', command=wczytaj, width=10)
btn3.place(x=460, y=160)
btn4=Button(window, text="Wylacz alerty", fg='blue', command=lambda:[exit_event.set(),btn5.config(background='red')] , width=10)
btn4.place(x=460, y=280)
btn5=Button(window, text="", background='red', width=10)
btn5.place(x=460, y=360)
btn6=Button(window, text="Zmień", fg='blue', command=zmien, width=10)
btn6.place(x=460, y=320)

cols = ('nazwa', 'cena1', 'cena2', 'cena3', 'cena4', 'cena5','alert')
tree = Treeview(window, columns=cols, show='headings')
tree.heading('nazwa', text='Nazwa', anchor=CENTER)
tree.column('nazwa', minwidth=0, width=200, stretch=NO)
tree.heading('cena1', text='Cena1', anchor=CENTER)
tree.column('cena1', minwidth=0, width=75, stretch=NO)
tree.heading('cena2', text='Cena2', anchor=CENTER)
tree.column('cena2', minwidth=0, width=75, stretch=NO)
tree.heading('cena3', text='Cena3', anchor=CENTER)
tree.column('cena3', minwidth=0, width=75, stretch=NO)
tree.heading('cena4', text='Cena4', anchor=CENTER)
tree.column('cena4', minwidth=0, width=75, stretch=NO)
tree.heading('cena5', text='Cena5', anchor=CENTER)
tree.column('cena5', minwidth=0, width=75, stretch=NO)
tree.heading('alert', text='Alert', anchor=CENTER)
tree.column('alert', minwidth=0, width=75, stretch=NO)
tree.grid(row=0, column=0, sticky='nsew')
tree.place(x=600, y=100)
update(data)

my_list.bind("<<ListboxSelect>>",fill)
txtfld.bind("<KeyRelease>", check)

window.mainloop()