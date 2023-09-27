from tkinter import *

if __name__ == "__main__":
    window = Tk()
    # add widgets here

    lbl = Label(window, text="This is a Label widget", fg='red', font=("Helvetica", 16))
    lbl.place(x=60, y=50)

    btn = Button(window, text="This is Button widget", fg='blue')
    btn.place(x=80, y=100)

    txtfld = Entry(window, text="This is Entry Widget", bd=5, show='*')
    txtfld.place(x=80, y=150)

    window.title('Hello Python')
    window.geometry("300x200+50+50")
    window.mainloop()
