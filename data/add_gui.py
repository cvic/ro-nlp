import json
from tkinter import *
from tkinter import ttk


class DeclarationGui(ttk.Frame):
    __WIDTH = 400
    __HEIGHT = 400

    __STR = {
        'author' : 'Who wrote this declaration?',
        'date' : 'When was the declaration given?',
        'source' : 'Source',
    }

    __JSON = {
        'author' : None,
        'date' : None,
        'source' : None,
        'filename' : None
    }

    __MAIN_FILE = 'declarations.json'

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master.title('Add Declaration')

        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.__style = ttk.Style()
        self.__style.theme_use('clam')

        self.__populate()

    def __populate(self):

        # text entry
        self.__text_frame = ttk.Frame(self, relief=SUNKEN)
        self.__text_frame.grid(column=0, row=1, columnspan=4, sticky=W)
        self.__text_frame.grid_rowconfigure(0, weight=1)
        self.__text_frame.grid_columnconfigure(0, weight=1)

        self.__scrollbar = Scrollbar(self.__text_frame, orient=VERTICAL)
        self.__scrollbar.grid(column=1, row=0, sticky=(W, E))

        self.__text = Text(self.__text_frame, wrap=WORD, yscrollcommand=self.__scrollbar.set)
        self.__text.grid(column=0, row=0, sticky=(N, S, W, E))

        self.__scrollbar.config(command=self.__text.yview)

        # author
        self.__author_label = ttk.Label(self, text=self.__STR['author'])
        self.__author_label.grid(column=0, row=3, sticky=W)

        self.__author_entry = ttk.Entry(self)
        self.__author_entry.grid(column=1, row=3, sticky=E)

        # date
        self.__date_label = ttk.Label(self, text=self.__STR['date'])
        self.__date_label.grid(column=0, row=4, sticky=W)

        self.__date_entry = ttk.Entry(self)
        self.__date_entry.grid(column=1, row=4, sticky=E)

        # src
        self.__source_label = ttk.Label(self, text=self.__STR['source'])
        self.__source_label.grid(column=0, row=5, sticky=W)

        self.__source_entry = ttk.Entry(self)
        self.__source_entry.grid(column=1, row=5, sticky=E)

        # add
        self.__add_button = ttk.Button(self, text='Add declaration', command=self.__add)
        self.__add_button.grid(column=0, row=6, sticky=W)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.master.update()
        self.master.minsize(root.winfo_width(), root.winfo_height())
        self.master.geometry('{}x{}'.format(self.__WIDTH, self.__HEIGHT))

    def __add(self):
        decl_file_name = self.__author_entry.get() + '-{}'.format(self.__get_timestamp())

        self.__JSON['author'] = self.__author_entry.get()
        self.__JSON['date'] = self.__date_entry.get()
        self.__JSON['source'] = self.__source_entry.get()
        self.__JSON['filename'] = decl_file_name

        with open(self.__MAIN_FILE, 'a') as json_file:
            # ensure_ascii=False is used to get an utf-8 encoded file
            json.dump(self.__JSON, json_file, ensure_ascii=False)

        with open(decl_file_name, 'w') as decl_file:
            decl_file.write(self.__text.get(1.0, END))

        self.__clean_widgets()

    def __clean_widgets(self):
        self.__author_entry.delete(0, END)
        self.__date_entry.delete(0, END)
        self.__source_entry.delete(0, END)
        self.__text.delete(1.0, END)

    def __get_timestamp(self):
        from time import gmtime, strftime
        return strftime("%Y-%m-%d-%H-%M-%S", gmtime())


if __name__ == '__main__':
    root = Tk()

    app = DeclarationGui(master=root)
    app.mainloop()
