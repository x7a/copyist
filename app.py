import tkinter as tk
from tkinter.constants import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
from os import path
from shutil import copyfile

main = tk.Tk()
main.geometry('500x200')
main.title('copyist')
main.resizable(False, False)

PADDING = 7


def choose_file(txt):
  file_path = filedialog.askopenfilename()
  if not file_path:
    return

  txt.delete(0, END)
  txt.insert(0, file_path)


def choose_dir(txt):
  dir_path = filedialog.askdirectory()
  if not dir_path:
    return

  txt.delete(0, END)
  txt.insert(0, dir_path)


def update_check_state(state, txt):
  if state.get() == 1:
    txt.config(state=NORMAL)
  elif state.get() == 0:
    txt.config(state=DISABLED)


def copy():
  original_path = original_txt.get().strip()
  filenames_path = filenames_txt.get().strip()
  dest_path = dest_txt.get().strip()
  extension = path.splitext(original_path)[1]

  prefix = prefix_txt.get().lstrip()
  suffix = suffix_txt.get().rstrip()

  # if prefix or suffix is unchecked, prefix or suffix stays blank
  if prefix_txt.cget('state') != NORMAL:
    prefix = ''
  if suffix_txt.cget('state') != NORMAL:
    suffix = ''

  # if any of the paths are invalid
  is_invalid = False

  if not path.isfile(original_path) or original_path == '':
    original_txt.config(bg='tomato')
    is_invalid = True
  else:
    original_txt.config(bg=ORIGINAL_TXT_COLOR)

  if not path.isfile(filenames_path) or filenames_path == '':
    filenames_txt.config(bg='tomato')
    is_invalid = True
  else:
    filenames_txt.config(bg=ORIGINAL_TXT_COLOR)

  if not path.isdir(dest_path) or dest_path == '':
    dest_txt.config(bg='tomato')
    is_invalid = True
  else:
    dest_txt.config(bg=ORIGINAL_TXT_COLOR)

  if is_invalid:
    return

  names = []
  with open(filenames_path, 'r') as fp:
    for line in fp:
      names.append(prefix + line.strip() + suffix)

  for name in names:
    copyfile(original_path, path.join(dest_path, name + extension))

  showinfo('Done', 'Copying finished!')


# widgets
original_lbl = tk.Label(main, text='Original: ', anchor=W, width=3)
original_txt = tk.Entry(main)
original_btn = tk.Button(main, text='Choose',
                         command=lambda: choose_file(original_txt))

filenames_lbl = tk.Label(main, text='Filenames: ', anchor=W, width=3)
filenames_txt = tk.Entry(main)
filenames_btn = tk.Button(main, text='Choose',
                          command=lambda: choose_file(filenames_txt))

dest_lbl = tk.Label(main, text='Destination: ', anchor=W, width=3)
dest_txt = tk.Entry(main)
dest_btn = tk.Button(main, text='Choose', command=lambda: choose_dir(dest_txt))

prefix_state = tk.IntVar()
prefix_txt = tk.Entry(main, state=DISABLED)
prefix_checkbox = tk.Checkbutton(main, text='Prefix', onvalue=1, offvalue=0,
                                 variable=prefix_state,
                                 command=lambda:
                                   update_check_state(prefix_state,
                                                      prefix_txt))

suffix_state = tk.IntVar()
suffix_txt = tk.Entry(main, state=DISABLED)
suffix_checkbox = tk.Checkbutton(main, text='Suffix', onvalue=1, offvalue=0,
                                 variable=suffix_state,
                                 command=lambda:
                                   update_check_state(suffix_state,
                                                      suffix_txt))

ORIGINAL_TXT_COLOR = original_txt.cget('bg')

copy_btn = tk.Button(main, text='Copy', command=copy)

# apply widgets
main.rowconfigure((0, 1, 2, 3, 4), weight=1)
main.columnconfigure((0, 1, 2), weight=1)

original_lbl.grid(row=0, column=0, sticky=EW, padx=PADDING, pady=PADDING)
original_txt.grid(row=0, column=1, sticky=EW, padx=PADDING, pady=PADDING)
original_btn.grid(row=0, column=2, sticky=EW, padx=PADDING, pady=PADDING)

filenames_lbl.grid(row=1, column=0, sticky=EW, padx=PADDING, pady=PADDING)
filenames_txt.grid(row=1, column=1, sticky=EW, padx=PADDING, pady=PADDING)
filenames_btn.grid(row=1, column=2, sticky=EW, padx=PADDING, pady=PADDING)

dest_lbl.grid(row=2, column=0, sticky=EW, padx=PADDING, pady=PADDING)
dest_txt.grid(row=2, column=1, sticky=EW, padx=PADDING, pady=PADDING)
dest_btn.grid(row=2, column=2, sticky=EW, padx=PADDING, pady=PADDING)

prefix_checkbox.grid(row=3, column=0, sticky=EW, padx=PADDING, pady=PADDING)
prefix_txt.grid(row=3, column=1, sticky=EW, padx=PADDING, pady=PADDING)

suffix_checkbox.grid(row=4, column=0, sticky=EW, padx=PADDING, pady=PADDING)
suffix_txt.grid(row=4, column=1, sticky=EW, padx=PADDING, pady=PADDING)

copy_btn.grid(row=3, column=2, rowspan=2, sticky=NSEW,
              padx=PADDING, pady=PADDING)

main.mainloop()

