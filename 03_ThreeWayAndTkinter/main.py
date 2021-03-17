import random
import numpy as np
import tkinter as tk
from tkinter import messagebox
   
class myButton(tk.Button):

    def __init__(self, *args, **kwargs):

        self.pos = (kwargs["pos_x"], kwargs["pos_y"])
        kwargs.pop("pos_x")
        kwargs.pop("pos_y")

        tk.Button.__init__(self, *args, **kwargs)



class Application(tk.Frame):


    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.E+tk.S+tk.W)
        self.numbers = []
        self.positions = np.zeros((4, 4), dtype=np.int8)
        self.createWidgets()

    def __check_win(self):
        prev_i, prev_j = 0, 0
        for i in range(4):
            for j in range(4):
                if self.positions[i, j] < self.positions[prev_i, prev_j]:
                    return False

                prev_i, prev_j = i, j

        return True

    def __move(self, btn):

        is_equal_x = btn.pos[0]==self.empty_pos[0] \
				and abs(btn.pos[1]-self.empty_pos[1])==1

        is_equal_y = btn.pos[1]==self.empty_pos[1] \
				and abs(btn.pos[0]-self.empty_pos[0])==1

        if is_equal_x or is_equal_y:
            
            tmp = self.positions[btn.pos[1]-1, btn.pos[0]]
 
            self.positions[btn.pos[1]-1, btn.pos[0]] = \
                self.positions[self.empty_pos[1]-1, self.empty_pos[0]]

            self.positions[self.empty_pos[1]-1, self.empty_pos[0]] = tmp

            btn.pos, self.empty_pos = self.empty_pos,  btn.pos
            btn.grid(row=btn.pos[1], column=btn.pos[0], sticky="NSEW")

        if self.__check_win():
            messagebox.showinfo("", "You win!")
            self.__renew()
        
    
    def __renew(self):

        for number in self.numbers:
            number.destroy()

        self.numbers.clear()

        available_numbers = [ i for i in range(1, 16, 1)]

        for i in range(0, 15, 1):

            r_int = random.choice(available_numbers)
            self.positions[i // 4, i % 4] = r_int
            available_numbers.pop(available_numbers.index(r_int))
            button = myButton(self, text=r_int, pos_y=1+i//4, pos_x=i%4)
            button['command'] = lambda btn=button: self.__move(btn)

            button.grid(row=1 + i // 4, column= i % 4, padx=2, pady=2, sticky="NSEW")
            self.empty_pos = (3, 4)
            self.numbers.append(button)

        self.positions[3, 3] = 16

        return self.numbers



    def createWidgets(self):

        top=self.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure((0, 1, 2, 3, 4),  weight=1)
        self.columnconfigure((0, 1, 2, 3), weight=1)
        
        self.quitButton = tk.Button(self, text='Exit', command=self.quit)
        self.newButton = tk.Button(self, text='New', command=self.__renew)

        self.quitButton.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        self.newButton.grid(row=0, column=2, columnspan=2, sticky="NSEW")
        
        self.__renew()
        print(self.grid_size())

if __name__ == '__main__':
    app = Application()
    app.master.title("15")
    app.mainloop()
