import sys
import time
import tkinter as tk
from threading import Thread


class Background(Thread):
    def __init__(self, gui):
        Thread.__init__(self)
        self.gui = gui
        self.flag = True

    def destroy(self):
        self.flag = False

    def run(self):
        while self.flag:
            time.sleep(3)
            self.gui.update()


class App(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.state_lbl = tk.Label(self, text="initial words")
        self.state_lbl.grid(row=0, column=0)
        self.btn = tk.Button(self, text="Hello")
        self.btn.grid(row=1, column=0)

    def update(self):
        self.state_lbl["text"] = "updated words"

    
if __name__ == "__main__":
    root = tk.Tk()
    main = App(root)
    main.grid()
    background = Background(main)
    background.daemon = True
    background.start()
    root.wm_geometry("600x300")
    root.mainloop()
    # sys.exit(0)
