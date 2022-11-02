import tkinter as tk
from utils import SerialPort, Thermogram, get_serial_data
from PIL import Image, ImageTk


# port = SerialPort(115200).open()

# data = get_serial_data(port)
data = [27.0] * 50
thermogram = Thermogram.generate_thermogram(data)

BACKGROUND_COLOR = "#1e1e2e"
SURFACE_COLOR = "#313244"
FOREGROUND_COLOR = "#cdd6f4"

root = tk.Tk()
# root.geometry("1260x720")
root.configure(bg=BACKGROUND_COLOR)

# left_frame = tk.Frame(frame, bg=SURFACE_COLOR, width=300, height=720)
# # left_frame.grid(row=0, column=0, sticky=tk.W)
# left_frame.pack(side=tk.LEFT)

title = tk.Label(root, bg=BACKGROUND_COLOR, font=(None, 20), fg=FOREGROUND_COLOR, text="THERMOGRAM")
title.grid(row=5, column=0, sticky=tk.W)
# title.pack(side=tk.TOP)

text_input = tk.Entry(bg=BACKGROUND_COLOR, font=(None, 16), fg=FOREGROUND_COLOR,)
text_input.grid(row=6, column=0, sticky=tk.W)

btn = tk.Button(root, bg=BACKGROUND_COLOR, font=(None, 16), fg=FOREGROUND_COLOR, text="RECORD")
btn.grid(row=7, column=0, sticky=tk.W)

test = ImageTk.PhotoImage(Image.fromarray(thermogram))
image = tk.Label(root, image=test, borderwidth=0)
image.grid(row=0, column=1, rowspan=30)

root.mainloop()