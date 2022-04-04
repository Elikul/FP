from tkinter import *  
from tkinter import scrolledtext
from tkinter import messagebox 
from RSA import chooseKeys, encrypt, decrypt

def createWindow():  
    """
    Генерируем ключи и выводим их в соответсвующие поля
    """
    def handlerGk_btn():
        chooseKeys()
        pu_k.delete(1.0,END)
        public_file = open('public_keys.txt', 'r')
        pk = public_file.read().splitlines()
        pu_k.insert(INSERT,str(pk))
        public_file.close()

        pr_k.delete(1.0,END)
        private_file = open('private_keys.txt', 'r')
        prk = private_file.read().splitlines()
        pr_k.insert(INSERT,str(prk))
        public_file.close()


    """
    Шифруем сообщение
    """
    def handlerEn_btn():
        txt_out.delete(1.0, END)
        msg_in = txt_in.get(1.0, END)
        if msg_in != "\n":
            msg_out = encrypt(msg_in)
            txt_out.insert(INSERT,str(msg_out))
        else:
            messagebox.showerror("Ошибка шифрования","Нельзя зашифровать пустое сообщение!")

    """
    Расшифровываем сообщение
    """
    def handlerDe_btn():
        txt_out.delete(1.0, END)
        msg_in = txt_in.get(1.0, END)
        if msg_in != "\n":
            msg_out = decrypt(msg_in)
            txt_out.insert(INSERT,str(msg_out))
        else:
            messagebox.showerror("Ошибка расшифровки","Нельзя расшифровать пустое сообщение!")

    """
    Для полей ввода и вывода базовые hot keys с текстом
    """
    def _onKeyRelease(event):
        ctrl  = (event.state & 0x4) != 0
        if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
            event.widget.event_generate("<<Cut>>")

        if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
            event.widget.event_generate("<<Paste>>")

        if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")

        if event.keycode==65 and  ctrl and event.keysym.lower() != "a":
            event.widget.event_generate("<<SelectAll>>")

    window = Tk()  
    window.title("RSA")  
    window.geometry('800x600') 
    window.config(background="#AAF0D1")
    window.bind_all("<Key>", _onKeyRelease, "+")

    gk_btn = Button(window, text="Сгенерировать ключи", command=handlerGk_btn, bg="#0BDA51", fg="#FFFFFF", font=("Vernada",12,"bold"), padx="3", pady="3", activebackground="#3CAA3C", activeforeground="#121910")             
    gk_btn.place(relx=.2, rely=.1, anchor="c", height=35, width=200)

    pu_k_lb = Label(text="Открытый ключ", bg="#AAF0D1", fg="#181513", font=("Vernada",12))
    pu_k_lb.place(relx=.2, rely=.2, anchor="c")
    pu_k = scrolledtext.ScrolledText(window, width=20, height=0.5, font=("Arial",12))  
    pu_k.place(relx=.2, rely=.3, anchor="c") 

    pr_k_lb = Label(text="Закрытй ключ", bg="#AAF0D1", fg="#181513", font=("Vernada",12))
    pr_k_lb.place(relx=.2, rely=.4, anchor="c")
    pr_k = scrolledtext.ScrolledText(window, width=20, height=0.5, font=("Arial",12)) 
    pr_k.place(relx=.2, rely=.5, anchor="c") 

    en_btn = Button(window, text="Зашифровать", command=handlerEn_btn, bg="#0BDA51", fg="#FFFFFF", font=("Vernada",12,"bold"), padx="3", pady="3", activebackground="#3CAA3C", activeforeground="#121910")  
    en_btn.place(relx=.2, rely=.7, anchor="c", height=35, width=200) 

    de_btn = Button(window, text="Расшифровать", command=handlerDe_btn, bg="#0BDA51", fg="#FFFFFF", font=("Vernada",12,"bold"), padx="3", pady="3", activebackground="#3CAA3C", activeforeground="#121910")  
    de_btn.place(relx=.2, rely=.8, anchor="c", height=35, width=200) 

    label_in = Label(text="Ввод", bg="#AAF0D1", fg="#181513", font=("Vernada",14,"bold"))
    label_in.place(relx=.7, rely=.1, anchor="c")
    txt_in = scrolledtext.ScrolledText(window, width=35, height=10, font=("Arial",12))  
    txt_in.place(relx=.7, rely=.3, anchor="c") 

    label_out = Label(text="Вывод", bg="#AAF0D1", fg="#181513", font=("Vernada",14,"bold"))
    label_out.place(relx=.7, rely=.6, anchor="c")
    txt_out = scrolledtext.ScrolledText(window, width=35, height=10, font=("Arial",12))  
    txt_out.place(relx=.7, rely=.8, anchor="c") 

    window.mainloop() 