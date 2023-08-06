from tkinter import *
from tkinter.ttk import Combobox
def app_start():


    window = Tk()

    window.title("Welcome to Da Edukation App")

    window.geometry("800x1000")


    lbl = Label(window, text="Name:")

    lbl.grid(column=0, row=0)

    txt = Entry(window,width=50)

    txt.grid(column=0, row=1)

    def clicked():

        nwindow = Tk()

        nwindow.title("Da Edukation App")

        window.geometry('300x250')

        lbl = Label(nwindow, text="Hello "+txt.get())

        lbl.grid(column=0, row=0)

        lbl1 = Label(nwindow, text="Select subject ")

        lbl1.grid(column=0, row=1)

        combo1 = Combobox(nwindow)

        combo1['values']= ('Math', "Physics", "Chemistry", "Biology", "Computers", "English", )

        combo1.current(1) #set the selected item

        combo1.grid(column=0, row=3)

        window.geometry('300x250')
        
        def mnt():
            mwindow = Tk()
            mwindow.title(combo1.get())
            
            
            
            lbl1 = Label(mwindow, text=combo1.get()+":")

            lbl1.grid(column=0, row=0)
            
            if combo1.get() == "Physics":
            
                lbl2 = Label(mwindow, text="It is the physical application of science")

                lbl2.grid(column=0, row=1)  
            
            elif combo1.get()=="Math":
                lbl1 = Label(mwindow, text="It takes your thinking capacity away")

                lbl1.grid(column=0, row=1)
                
            elif combo1.get()=="Chemistry":
                lbl1 = Label(mwindow, text="Visible confusion")

                lbl1.grid(column=0, row=1)
                
            elif combo1.get()=="Biology":
                lbl1 = Label(mwindow, text="Something you will regret")

                lbl1.grid(column=0, row=1)
            elif combo1.get()=="Computers":
                lbl1 = Label(mwindow, text="God")

                lbl1.grid(column=0, row=1)
            elif combo1.get()=="English":
                lbl1 = Label(mwindow, text="Duh, dont you know?")

                lbl1.grid(column=0, row=1)
            else:
                lbl1 = Label(mwindow, text="Did you change the options?")

                lbl1.grid(column=0, row=1)
            btn = Button(mwindow, text="Quit", command=quit)

            btn.grid(column=0, row=2)
            mwindow.geometry("250x200")

        btn = Button(nwindow, text="Select", command=mnt)

        btn.grid(column=0, row=4)
        



        nwindow.mainloop()

    btn = Button(window, text="Submit", command=clicked)

    btn.grid(column=0, row=9)

    window.geometry('300x250')

    lbl = Label(window, text="Grade:")

    lbl.grid(column=0, row=2)

    combo = Combobox(window)

    combo['values']= ("lower", 9, 10, 11, 12, "Type year if college")

    combo.current(1) #set the selected item

    combo.grid(column=0, row=3)

    chk_state = BooleanVar()

    chk_state.set(FALSE) #set check state

    chk = Checkbutton(window, text='I Agree to tearms and conditions'+"'there are none'", var=chk_state)

    chk.grid(column=0, row=8)
    rad1 = Radiobutton(window,text='Male', value=1)

    rad2 = Radiobutton(window,text='Female', value=2)

    rad3 = Radiobutton(window,text='Both', value=3)

    rad1.grid(column=0, row=5)

    rad2.grid(column=0, row=6)

    rad3.grid(column=0, row=7)

    rads = rad1 and rad2 and rad3

    rads_state = BooleanVar()
    rads_state.set(False)

    lbl = Label(window, text="Gender:")

    lbl.grid(column=0, row=4)

    window.mainloop()