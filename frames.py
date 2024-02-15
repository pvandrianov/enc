from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, UnidentifiedImageError
from tkinter.messagebox import showerror
from encryption import MyEncrypt
from cesar import cesar
from polybius import Polibius
from vigenere import Vigenere


class CanvasFrame(Frame):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.image = None

        self.canvas_width = 300
        self.canvas_height = 300
        self.label_image = Label(self, text="Изображение:")
        self.label_image.pack(anchor="nw")
        self.canvas = Canvas(self, bg='white', width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(anchor=CENTER, expand=1)
        self.open_image_btn = ttk.Button(self, text="Загрузить изображение...")
        self.open_image_btn.pack(anchor=CENTER, padx=5, pady=5)
        self.open_image_btn["command"] = self.open_file

    def open_file(self):
        filepath = filedialog.askopenfilename()
        if filepath != "":
            try:
                with Image.open(filepath) as image:
                    self.image = image
                    text = (f'Оригинальный размер: {image.width} x {image.height} '
                            f'({filepath})')
                    max_side = max(image.width, image.height)
                    zoom = self.canvas_width / max_side
                    image = image.resize(
                        (int(image.width * zoom), int(image.height * zoom)),
                        Image.LANCZOS)
                    self.photo = ImageTk.PhotoImage(image)
                    # image.show()

                    self.canvas.create_image(
                        ((self.canvas_width - image.width) / 2, (self.canvas_width - image.height) / 2),
                        anchor='nw', image=self.photo, state=NORMAL)
                    self.label_image.config(text=text)
            except UnidentifiedImageError as e:
                showerror(title="Ошибка", message=str(e))


class QueryFrame(Frame):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_image = Label(self, text="Входные данные:")
        self.label_image.pack(anchor="nw")

        self.frame_query_text = Frame(self)
        self.v = Scrollbar(self.frame_query_text, orient='vertical')
        self.v.pack(side=RIGHT, fill='y')
        self.query_text = Text(self.frame_query_text, height=5, yscrollcommand=self.v.set)
        self.query_text.pack(anchor="nw")
        self.frame_query_text.pack(anchor=NW, fill=BOTH)


class ReplyFrame(Frame):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_image = Label(self, text="Выходные данные:")
        self.label_image.pack(anchor="nw")

        self.frame_reply_text = Frame(self)
        self.v = Scrollbar(self.frame_reply_text, orient='vertical')
        self.v.pack(side=RIGHT, fill='y')
        self.reply_text = Text(self.frame_reply_text, height=5, yscrollcommand=self.v.set)
        self.reply_text.pack(anchor="nw")
        self.frame_reply_text.pack(anchor=NW, fill=BOTH)


class EncFrame(Frame):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas_frame = CanvasFrame(self)
        self.canvas_frame.pack(fill=BOTH, padx=5, pady=5)
        self.query_frame = QueryFrame(self)
        self.query_frame.pack(fill=BOTH, padx=5, pady=5)
        self.action_btn_frame = Frame(self)
        self.action_btn_frame.pack(fill=BOTH, padx=5, pady=5)
        self.encrypt_btn = ttk.Button(self.action_btn_frame, text="Зашифровать")
        self.encrypt_btn["command"] = self.encrypt
        self.decrypt_btn = ttk.Button(self.action_btn_frame, text="Расшифровать")
        self.decrypt_btn["command"] = self.decrypt
        self.decrypt_btn.pack(side=RIGHT, padx=5)
        self.encrypt_btn.pack(side=RIGHT, padx=5, pady=5)
        self.reply_frame = ReplyFrame(self)
        self.reply_frame.pack(fill=BOTH, padx=5, pady=5)

    def encrypt(self):
        message = self.query_frame.query_text.get("1.0", END)
        image = self.canvas_frame.image
        if image:
            if message:
                e = MyEncrypt(image)
                encrypted_message = e.image_encrypt(message)
                self.reply_frame.reply_text.delete("1.0", END)
                self.reply_frame.reply_text.insert("1.0", encrypted_message)
            else:
                self.reply_frame.reply_text.delete("1.0", END)
                self.reply_frame.reply_text.insert("1.0", "None")
        else:
            showerror(title="Ошибка", message="Загрузите сначала картинку")

    def decrypt(self):
        message = self.query_frame.query_text.get("1.0", END)
        image = self.canvas_frame.image
        if image:
            if message:
                e = MyEncrypt(image)
                encrypted_message = e.image_decrypt(message)
                self.reply_frame.reply_text.delete("1.0", END)
                self.reply_frame.reply_text.insert("1.0", encrypted_message)
            else:
                self.reply_frame.reply_text.delete("1.0", END)
                self.reply_frame.reply_text.insert("1.0", "None")
        else:
            showerror(title="Ошибка", message="Загрузите сначала картинку")


class CesarFrame(Frame):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_frame = Frame(self)
        self.input_frame.pack(fill=BOTH, padx=5, pady=5)
        self.label_title = Label(self.input_frame, text="Цезарь", font = ("Arial", 14))
        self.label_title.pack(anchor="nw")
        self.label_input_title = Label(self.input_frame, text="Входные данные:")
        self.label_input_title.pack(anchor="nw")
        self.label_input_text = Label(self.input_frame, text="Текст:")
        self.label_input_text.pack(anchor="nw")
        self.input_text = Entry(self.input_frame)
        self.input_text.pack(anchor="nw", fill='x')
        self.label_input_text = Label(self.input_frame, text="Сдвиг (целое число):")
        self.label_input_text.pack(anchor="nw")
        self.input_shift = Entry(self.input_frame)
        self.input_shift.pack(anchor="nw")
        self.shift_btn = ttk.Button(self, text="Выполнить")
        self.shift_btn["command"] = self.shift
        self.shift_btn.pack(anchor='nw', padx=5, pady=5)
        self.label_output_text = Label(self.input_frame, text="Выходные данные:")
        self.label_output_text.pack(anchor="nw")
        self.output_text = Entry(self.input_frame)
        self.output_text.pack(anchor="nw", fill='x')

    def shift(self):
        text = self.input_text.get().upper()
        shift = self.input_shift.get()
        shift = int(shift) if shift.replace('-', '').isdigit() else 0
        self.input_text.delete(0, END)
        self.input_text.insert(0, text)
        self.output_text.delete(0, END)
        self.output_text.insert(0, cesar(text, shift))


class PolibiusFrame(Frame):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_frame = Frame(self)
        self.input_frame.pack(fill=BOTH, padx=5, pady=5)
        self.label_title = Label(self.input_frame, text="Квадрат Полибия", font = ("Arial", 14))
        self.label_title.pack(anchor="nw")
        self.label_input_title = Label(self.input_frame, text="Входные данные:")
        self.label_input_title.pack(anchor="nw")
        self.input_text = Entry(self.input_frame)
        self.input_text.pack(anchor="nw", fill='x')
        self.encrypt_btn = ttk.Button(self, text="Зашифровать (латинские символы без пробелов)")
        self.encrypt_btn["command"] = self.encrypt
        self.encrypt_btn.pack(anchor='nw', padx=5, pady=5)
        self.decrypt_btn = ttk.Button(self, text="Расшифровать (цифры)")
        self.decrypt_btn["command"] = self.decrypt
        self.decrypt_btn.pack(anchor='nw', padx=5, pady=5)
        self.label_output_text = Label(self.input_frame, text="Выходные данные:")
        self.label_output_text.pack(anchor="nw")
        self.output_text = Entry(self.input_frame)
        self.output_text.pack(anchor="nw", fill='x')

    def encrypt(self):
        e = Polibius()
        text = self.input_text.get().upper()
        self.input_text.delete(0, END)
        self.input_text.insert(0, text)
        self.output_text.delete(0, END)
        self.output_text.insert(0, e.encrypt(text))

    def decrypt(self):
        e = Polibius()
        text = self.input_text.get().upper()
        self.input_text.delete(0, END)
        self.input_text.insert(0, text)
        self.output_text.delete(0, END)
        self.output_text.insert(0, e.decrypt(text))


class VigenereFrame(Frame):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_frame = Frame(self)
        self.input_frame.pack(fill=BOTH, padx=5, pady=5)
        self.label_title = Label(self.input_frame, text="Вижинер", font = ("Arial", 14))
        self.label_title.pack(anchor="nw")
        self.label_input_title = Label(self.input_frame, text="Входные данные:")
        self.label_input_title.pack(anchor="nw")
        self.label_message = Label(self.input_frame, text="Текст:")
        self.label_message.pack(anchor="nw")
        self.input_message = Entry(self.input_frame)
        self.input_message.pack(anchor="nw", fill='x')
        self.label_keyword = Label(self.input_frame, text="Ключевое слово")
        self.label_keyword.pack(anchor="nw")
        self.input_keyword = Entry(self.input_frame)
        self.input_keyword.pack(anchor="nw", fill='x')
        self.encrypt_btn = ttk.Button(self, text="Зашифровать (допустимы пробелы)")
        self.encrypt_btn["command"] = self.encrypt
        self.encrypt_btn.pack(anchor='nw', padx=5, pady=5)
        self.decrypt_btn = ttk.Button(self, text="Расшифровать")
        self.decrypt_btn["command"] = self.decrypt
        self.decrypt_btn.pack(anchor='nw', padx=5, pady=5)
        self.label_output_text = Label(self.input_frame, text="Выходные данные:")
        self.label_output_text.pack(anchor="nw")
        self.output_text = Entry(self.input_frame)
        self.output_text.pack(anchor="nw", fill='x')

    def encrypt(self):
        e = Vigenere()
        message = self.input_message.get().upper()
        self.input_message.delete(0, END)
        self.input_message.insert(0, message)
        keyword = self.input_keyword.get().upper()
        self.input_keyword.delete(0, END)
        self.input_keyword.insert(0, keyword)

        self.output_text.delete(0, END)
        self.output_text.insert(0, e.crypt(message=message, keyword=keyword, action='encrypt'))

    def decrypt(self):
        e = Vigenere()
        message = self.input_message.get().upper()
        self.input_message.delete(0, END)
        self.input_message.insert(0, message)
        keyword = self.input_keyword.get().upper()
        self.input_keyword.delete(0, END)
        self.input_keyword.insert(0, keyword)

        self.output_text.delete(0, END)
        self.output_text.insert(0, e.crypt(message=message, keyword=keyword, action='decrypt'))


class AnotherFrame(Frame):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cesar_frame = CesarFrame(self, borderwidth=1, relief=SOLID)
        self.cesar_frame.pack(fill=BOTH, padx=5, pady=5)
        self.polib_frame = PolibiusFrame(self, borderwidth=1, relief=SOLID)
        self.polib_frame.pack(fill=BOTH, padx=5, pady=5)
        self.polib_frame = VigenereFrame(self, borderwidth=1, relief=SOLID)
        self.polib_frame.pack(fill=BOTH, padx=5, pady=5)
