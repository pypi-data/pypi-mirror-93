#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a tool to convert Hex/Dec/Oct/Bin
"""

import os
import time
import sys
import argparse
import re
from functools import wraps
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage

__author__ = "House Chou"


class IntSubject():
    def __init__(self):
        self.observers = []
        self.value = 0

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, val):
        self.value = val
        for observer in self.observers:
            observer.update(val)

    def get_val(self):
        return self.value


class BinView(tk.Frame):
    def __init__(self, master, subject):
        tk.Frame.__init__(self,
                          master,
                          highlightbackground='grey',
                          highlightthickness=1)
        self.master = master
        self.subject = subject
        self.bits = []
        self.value = 0
        for i in range(0, 32):
            header = tk.Label(self, text=31 - i)
            bit = ToggleLabel(
                self,
                '1',
                '0',
                command=self.notify,
                highlightbackground='grey',
                highlightthickness=1,
            )
            self.bits.append(bit)
            header.grid(row=1, column=i, padx=5, pady=5)
            bit.grid(row=2, column=i, padx=5, pady=5)

    def notify(self):
        bitstr = ''
        for b in self.bits:
            bitstr += b['text']
        try:
            val = int(bitstr, 2)
            self.subject.notify(val)
        except ValueError as e:
            print(e)

    def update(self, val):
        self.value = val
        # iterate from MSB to LSB
        for i in range(0, 32):
            s = '{:d}'.format((val >> (31 - i)) & 0x1)
            if s == '1':
                self.bits[i].config(text=s, background='yellow')
                self.bits[i].current = True
            else:
                self.bits[i].config(text=s, background='#d9d9d9')
                self.bits[i].current = False


class HexView(tk.Frame):
    def __init__(self, master, subject):
        tk.Frame.__init__(self, master)
        self.master = master
        self.subject = subject
        self.value = 0
        self.hex_label = tk.Label(self, text='Hex')
        self.hex_text = tk.StringVar()
        self.hex_text.trace("w", lambda name, index, mode: self.notify())
        self.hex_entry = tk.Entry(self,
                                  width=10,
                                  textvariable=self.hex_text,
                                  font=('Ariel', 12))
        self.hex_label.grid(row=0, column=0)
        self.hex_entry.grid(row=0, column=1)

    def notify(self):
        hex_str = self.hex_text.get()
        try:
            val = int(hex_str, 16)
            self.subject.notify(val)
        except ValueError as e:
            pass
            #print(e)

    def update(self, val):
        self.value = val
        self.hex_entry.delete(0, 'end')
        if val != 0:
            self.hex_entry.insert(0, '{:x}'.format(val))


class DecView(tk.Frame):
    def __init__(self, master, subject):
        tk.Frame.__init__(self, master)
        self.master = master
        self.subject = subject
        self.value = 0
        self.dec_label = tk.Label(self, text='Dec')
        self.dec_text = tk.StringVar()
        self.dec_text.trace("w", lambda name, index, mode: self.notify())
        self.dec_entry = tk.Entry(self,
                                  width=10,
                                  textvariable=self.dec_text,
                                  font=('Ariel', 12))
        self.dec_label.grid(row=0, column=0)
        self.dec_entry.grid(row=0, column=1)

    def notify(self):
        dec_str = self.dec_text.get()
        try:
            val = int(dec_str, 10)
            self.subject.notify(val)
        except ValueError as e:
            pass
            #print(e)

    def update(self, val):
        self.value = val
        self.dec_entry.delete(0, 'end')
        self.dec_entry.insert(0, '{:d}'.format(val))


class OctView(tk.Frame):
    def __init__(self, master, subject):
        tk.Frame.__init__(self, master)
        self.master = master
        self.subject = subject
        self.value = 0
        self.oct_label = tk.Label(self, text='Oct')
        self.oct_text = tk.StringVar()
        self.oct_text.trace("w", lambda name, index, mode: self.notify())
        self.oct_entry = tk.Entry(self,
                                  width=10,
                                  textvariable=self.oct_text,
                                  font=('Ariel', 12))
        self.oct_label.grid(row=0, column=0)
        self.oct_entry.grid(row=0, column=1)

    def notify(self):
        oct_str = self.oct_text.get()
        try:
            val = int(oct_str, 8)
            self.subject.notify(val)
        except ValueError as e:
            pass
            #print(e)

    def update(self, val):
        self.value = val
        self.oct_entry.delete(0, 'end')
        self.oct_entry.insert(0, '{:o}'.format(val))


class Shift(tk.Frame):
    def __init__(self, master, subject):
        tk.Frame.__init__(self, master)
        self.master = master
        self.subject = subject
        self.rbtn = tk.Button(self, text='Shift >>', command=self.right_shift)
        self.lbtn = tk.Button(self, text='<< Shift', command=self.left_shift)
        self.shift_text = tk.StringVar()
        self.shift_text.set('1')
        self.shift_entry = tk.Entry(self,
                                    width=2,
                                    textvariable=self.shift_text,
                                    font=('Ariel', 12))
        self.lbtn.grid(row=0, column=0, padx=2)
        self.shift_entry.grid(row=0, column=1, padx=2)
        self.rbtn.grid(row=0, column=2, padx=2)

    def get_shift_val(self):
        shift = self.shift_text.get()
        try:
            shift = int(shift, 10)
            return shift
        except ValueError as e:
            print(e)
            return None

    def right_shift(self):
        shift = self.get_shift_val()
        if shift is not None:
            self.subject.notify(self.subject.get_val() >> shift)

    def left_shift(self):
        shift = self.get_shift_val()
        if shift is not None:
            self.subject.notify(self.subject.get_val() << shift)


class ClearButton(tk.Frame):
    def __init__(self, master, subject):
        tk.Frame.__init__(self, master)
        self.master = master
        self.subject = subject
        self.btn = tk.Button(self, text='Clear', command=self.clear)
        self.btn.grid(row=0, column=0)

    def clear(self):
        self.subject.notify(0)


class ToggleLabel(tk.Label):
    def __init__(self,
                 master,
                 on_indicator,
                 off_indicator,
                 default_state=0,
                 command=None,
                 **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind("<Button-1>",
                  lambda event, command=command: self.toggle(command))
        self.on_indicator = on_indicator
        self.off_indicator = off_indicator
        self.on_use_img = 0
        self.off_use_img = 0
        self.on_use_str = 0
        self.off_use_str = 0
        if type(on_indicator) == PhotoImage:
            self.on_use_img = 1
        elif type(on_indicator) == str:
            self.on_use_str = 1

        if type(off_indicator) == PhotoImage:
            self.off_use_img = 1
        elif type(off_indicator) == str:
            self.off_use_str = 1

        self.current = default_state
        self.set_state(default_state)

    def toggle(self, func):
        self.current = not self.current
        self.set_state(self.current)
        if func is not None:
            func()

    def set_state(self, state):
        if state:
            if self.on_use_img:
                self.config(text='', image=self.on_indicator)
            elif self.on_use_str:
                self.config(text=self.on_indicator, image='')
        else:
            if self.off_use_img:
                self.config(text='', image=self.off_indicator)
            elif self.off_use_str:
                self.config(text=self.off_indicator, image='')


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root = tk.Tk()
    root.title("HDOB Converter")
    subject = IntSubject()
    bin_view = BinView(root, subject)
    hex_view = HexView(root, subject)
    dec_view = DecView(root, subject)
    oct_view = OctView(root, subject)
    shift = Shift(root, subject)
    clear = ClearButton(root, subject)
    subject.attach(bin_view)
    subject.attach(hex_view)
    subject.attach(dec_view)
    subject.attach(oct_view)
    hex_view.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    dec_view.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    oct_view.grid(row=0, column=2, padx=5, pady=5, sticky='e')
    bin_view.grid(row=1, columnspan=3, padx=5, pady=5, sticky='news')
    shift.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    clear.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky='e')
    root.mainloop()


if __name__ == "__main__":
    main()
