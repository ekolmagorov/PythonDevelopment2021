import tkinter as tk
import tkinter.font as tkFont

class Cursor():
    def __init__(self, master, width, height, position=0):
        self.__cursor = tk.Frame(master, width=width, height=height, bg='black')
        self.__cursor_pos = position
        self.__cursor.place(x=self.__cursor_pos, y=1)

    
    def change_pos(self, new_position):
        self.__cursor_pos = new_position
        self.__cursor.place(x=self.__cursor_pos, y=1)

    def get_position(self):
        return self.__cursor_pos
        

class InputLabel(tk.Label):
    def __init__(self,  master=None, size=8):
        self.size = size
        self.text = tk.StringVar()

        super().__init__(
                            master,
                            textvariable=self.text,
                            takefocus=1, 
                            highlightthickness=4,
                            cursor="arrow",
                            relief=tk.GROOVE,
                            anchor="sw",
                            font='TkFixedFont'
                        )

        self.cursor = Cursor(self, 1, 16)

        self.bind("<KeyPress>", self.__key_input)
        self.bind("<Button-1>", self.__lkm)
          

    def __key_input(self, event):
        
        cursor_position = self.cursor.get_position()
        new_pos = cursor_position
 

        if event.keysym == "Left" :
            new_pos = cursor_position - self.size

        elif event.keysym == "Right":
            new_pos = cursor_position + self.size


        elif (event.keysym == "BackSpace" ) and self.cursor.get_position() > 0:
            index = cursor_position // self.size
            new_text = self.text.get()[:index-1] + self.text.get()[index:]
            self.text.set(new_text)

            new_pos = cursor_position - self.size
        
        elif (event.keysym == 'Home'):
            new_pos = 0

        elif (event.keysym == 'End'):
            new_pos = len(self.text.get()) * self.size

        else:
            symbol = event.char
            if symbol.isprintable():
                index = cursor_position // self.size
                tmp_text = self.text.get()
                self.text.set(tmp_text[:index] + symbol + tmp_text[index:])
                new_pos = cursor_position + self.size

        self.__change_pos(new_pos)

    def __lkm(self, event):
        self.focus()
        text_width = len(self.text.get()) * self.size
        new_pos = min(event.x // self.size * self.size, text_width)
        
        self.cursor.change_pos(new_pos)

    def __change_pos(self, new_pos):
        num_symbols = len(self.text.get())
        new_pos = max(0, new_pos)
        if new_pos > num_symbols * self.size:
            new_pos = num_symbols * self.size
        
        self.cursor.change_pos(new_pos)


class application(tk.Frame):
    def __init__(self, master=None, title="inputlabel", **kwargs):
        super().__init__(master, **kwargs)
        
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.geometry("250x100")
        self.grid(sticky="news")
        self.create_widgets()

        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):

        self.inp_label = InputLabel(self, 9)
        self.inp_label.grid(sticky='we')

        self.buttonquit = tk.Button(self, text="quit", command=self.quit)
        self.buttonquit.grid()

if __name__ == '__main__':
    app = application()
    app.mainloop()
