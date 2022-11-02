import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from typing import Callable
from numpy.typing import NDArray


BACKGROUND_COLOR = "#1e1e2e"
SURFACE_COLOR = "#313244"
FOREGROUND_COLOR = "#cdd6f4"
ACCENT_COLOR = "#f38ba8"

ENTRY_WIDTH = 24
ENTRY_PAD = 6
BTN_WIDTH = 22
PAD_X = (24, 24)


class App(tk.Tk):
    def __init__(
        self,
        # save_thermogram: callable
    ):
        super().__init__()
        self.title("IR THERMOGRAM")
        self.configure(bg=BACKGROUND_COLOR)
        # self.save_thermogram = save_thermogram
        # self.geometry('300x50')

        self.header = tk.Label(
            self,
            bg=BACKGROUND_COLOR,
            font=(None, 20),
            fg=FOREGROUND_COLOR,
            text="IR THERMOGRAM"
        )
        self.header.grid(row=3, column=0)

        self.patient_id_label = tk.Label(
            self,
            bg=BACKGROUND_COLOR,
            font=(None, 14),
            fg=FOREGROUND_COLOR,
            text="ID"
        )
        self.patient_id_label.grid(
            row=7,
            column=0,
            sticky=tk.W,
            padx=PAD_X
        )

        self.patient_id = tk.Entry(
            bg=BACKGROUND_COLOR,
            font=(None, 14),
            fg=FOREGROUND_COLOR,
            width=ENTRY_WIDTH,
        )
        self.patient_id.grid(
            row=8,
            column=0,
            sticky=tk.W,
            padx=PAD_X,
            ipady=ENTRY_PAD
        )

        self.patient_name_label = tk.Label(
            self,
            bg=BACKGROUND_COLOR,
            font=(None, 14),
            fg=FOREGROUND_COLOR,
            text="NAME"
        )
        self.patient_name_label.grid(
            row=9,
            column=0,
            sticky=tk.W,
            padx=PAD_X
        )

        self.patient_name = tk.Entry(
            bg=BACKGROUND_COLOR,
            font=(None, 14),
            fg=FOREGROUND_COLOR,
            width=ENTRY_WIDTH
        )
        self.patient_name.grid(
            row=10,
            column=0,
            sticky=tk.W,
            padx=PAD_X,
            ipady=ENTRY_PAD
        )

        self.patient_age_label = tk.Label(
            self,
            bg=BACKGROUND_COLOR,
            font=(None, 14),
            fg=FOREGROUND_COLOR,
            text="AGE"
        )
        self.patient_age_label.grid(
            row=11,
            column=0,
            sticky=tk.W,
            padx=PAD_X
        )

        self.patient_age = tk.Entry(
            bg=BACKGROUND_COLOR,
            font=(None, 14),
            fg=FOREGROUND_COLOR,
            width=ENTRY_WIDTH
        )
        self.patient_age.grid(
            row=12,
            column=0,
            sticky=tk.W,
            padx=PAD_X,
            ipady=ENTRY_PAD
        )

        self.patient_weight_label = tk.Label(
            self,
            bg=BACKGROUND_COLOR,
            font=(None, 14),
            fg=FOREGROUND_COLOR,
            text="WEIGHT"
        )
        self.patient_weight_label.grid(
            row=13,
            column=0,
            sticky=tk.W,
            padx=PAD_X
        )

        self.patient_weight = tk.Entry(
            bg=BACKGROUND_COLOR,
            font=(None, 14),
            fg=FOREGROUND_COLOR,
            width=ENTRY_WIDTH
        )
        self.patient_weight.grid(
            row=14,
            column=0,
            sticky=tk.W,
            padx=PAD_X,
            ipady=ENTRY_PAD
        )

        self.patient_gender_label = tk.Label(
            self,
            bg=BACKGROUND_COLOR,
            font=(None, 14),
            fg=FOREGROUND_COLOR,
            text="GENDER"
        )
        self.patient_gender_label.grid(
            row=15,
            column=0,
            sticky=tk.W,
            padx=PAD_X
        )

        self.patient_gender = tk.Entry(
            bg=BACKGROUND_COLOR,
            font=(None, 14),
            fg=FOREGROUND_COLOR,
            width=ENTRY_WIDTH
        )
        self.patient_gender.grid(
            row=16,
            column=0,
            sticky=tk.W,
            padx=PAD_X,
            ipady=ENTRY_PAD
        )

        self.record_btn = tk.Button(
            self,
            bg=ACCENT_COLOR,
            font=(None, 14),
            fg=BACKGROUND_COLOR,
            text="SAVE THERMOGRAM",
            width=BTN_WIDTH,
            height=2,
            command=self.on_record,
            highlightthickness = 0,
            bd=0
        )
        self.record_btn.grid(
            row=19,
            column=0,
            sticky=tk.W,
            padx=PAD_X
        )

        self.copyright = tk.Label(
            self,
            bg=BACKGROUND_COLOR,
            font=(None, 12),
            fg=FOREGROUND_COLOR,
            text="Made by Qatar University Machine Learning Group",
            wraplength=270
        )
        self.copyright.grid(
            row=27,
            column=0,
            sticky=tk.W,
            padx=PAD_X
        )

        self.thermogram = np.zeros((720, 960, 3), np.uint8)
        self.image = ImageTk.PhotoImage(Image.fromarray(self.thermogram))
        self.thermogram = tk.Label(
            self,
            image=self.image,
            borderwidth=0,
            background=BACKGROUND_COLOR
        )
        self.thermogram.grid(row=0, column=1, rowspan=30)

    def add_record_callback(self, save_thermogram: Callable):
        self.save_thermogram = save_thermogram

    def update_thermogram(self, thermogram: NDArray[np.uint8]):
        self.image = ImageTk.PhotoImage(Image.fromarray(thermogram))
        self.thermogram.configure(image=self.image)

    def on_record(self):
        id = self.patient_id.get()
        name = self.patient_name.get()
        age = self.patient_age.get()
        weigth = self.patient_weight.get()
        gender = self.patient_gender.get()
        self.save_thermogram(id, name, age, weigth, gender)
