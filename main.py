from tkinter import *
from tkinter import ttk
from frames import EncFrame, AnotherFrame


class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Шифрование')
        self.geometry('700x730')
        self.resizable(False, False)
        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH, padx=5, pady=5)

        self.my_enc_frame = EncFrame(self.notebook)
        self.my_enc_frame.pack(fill=BOTH, expand=True)

        self.another_frame = AnotherFrame(self.notebook)
        self.another_frame.pack(fill=BOTH, expand=True)

        self.notebook.add(self.my_enc_frame, text=" Свой метод ")
        self.notebook.add(self.another_frame, text=" Another ")


if __name__ == '__main__':
    root = MainWindow()
    root.mainloop()
