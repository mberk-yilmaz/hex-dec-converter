import tkinter as tk
from tkinter import ttk
from typing import Callable

from common.conversion_types import ConversionTypes as conversion_types

## control + c for textbox
def copy_text(result_text: tk.Text, event: tk.Event = None):
    try:
        selected_text = result_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        result_text.clipboard_clear()
        result_text.clipboard_append(selected_text)
    except tk.TclError as err:
        print(err)

## control + a for textbox
def select_all(result_text: tk.Text, event: tk.Event = None):
    result_text.tag_add("sel", "1.0", "end")
    return "break"

## alt + x shortcut
def set_combobox_value(conversion_combo: ttk.Combobox , index: int, callback_func: Callable[[], None], event: tk.Event = None):
    if 0 <= index < len(list(conversion_types)):
        conversion_combo.current(index)
        callback_func()