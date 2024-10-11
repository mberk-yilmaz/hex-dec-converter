import tkinter as tk
from tkinter import ttk, messagebox

from factory.conversion_factory import ConversionFactory
from common.data_types import DataTypes as data_types
from common.conversion_types import ConversionTypes as conversion_types
import components.commands.shortcut_commands as shortcuts

class ConverterComponent:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Hex <-> Decimal Converter")
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
        self.entries = []
        self.wnd_comps = {}
        self.create_main_ui()

    def destroy(self) -> None:
        for key in list(self.wnd_comps.keys()):
            if isinstance(self.wnd_comps[key], tk.Widget):
                self.wnd_comps[key].destroy()
            del self.wnd_comps[key]

        self.entries.clear()
        self.root.destroy()

    def create_main_ui(self) -> None:
        # Conversion type dropdown
        conversion_type = tk.StringVar(value=conversion_types.HEX_TO_DECIMAL.value)
        ttk.Label(self.root, text="Conversion Type:").grid(row=0, column=0, padx=10, pady=10)
        self.wnd_comps['conversion_type'] = conversion_type

        enum_values = [conversion_types.value for conversion_types in conversion_types]
        conversion_combo = ttk.Combobox(self.root, textvariable=conversion_type, values=enum_values)
        conversion_combo.grid(row=0, column=1)
        conversion_combo.bind("<<ComboboxSelected>>", self.update_fields)
        self.wnd_comps['conversion_combo'] = conversion_combo

        # Data type dropdown
        data_type = tk.StringVar(value=data_types.UINT16.name.lower())
        data_type.trace_add("write", lambda *args: self.update_fields())
        enum_values = [data_type.value for data_type in data_types]
        ttk.Label(self.root, text="Data Type:").grid(row=1, column=0, padx=10, pady=10)
        ttk.Combobox(self.root, textvariable=data_type, values=enum_values).grid(row=1, column=1)
        self.wnd_comps['data_type'] = data_type

        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.grid(row=2, column=0, columnspan=2, pady=10)
        self.wnd_comps['input_frame'] = input_frame

        # Result label
        result_label = tk.Label(self.root, text="Result:")
        result_label.grid(row=3, column=0, columnspan=2, pady=10)
        self.wnd_comps['result_label'] = result_label

        # Result text box
        result_text = tk.Text(self.root, height=1, width=30)
        result_text.grid(row=4, column=0, columnspan=2, pady=10)
        result_text.bind("<Control-c>", lambda event: shortcuts.copy_text(result_text))
        result_text.bind("<Control-a>", lambda event: shortcuts.select_all(result_text))
        self.wnd_comps['result_text'] = result_text

        # Convert button
        convert_button = tk.Button(self.root, text="Convert", command=self.convert_text)
        convert_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.wnd_comps['convert_button'] = convert_button

        # Update input fields when data type changes
        self.update_fields()

## shortcuts
        for enter_key in ['<Return>', "<KP_Enter>"]:
            self.root.bind(enter_key, lambda event: convert_button.invoke())

        for alt_key_idx in range(len(list(conversion_types))):
            shortcut = "<Alt-Key-{}>".format(alt_key_idx + 1)
            self.root.bind(shortcut, lambda event, idx=alt_key_idx: shortcuts.set_combobox_value(conversion_combo, idx, self.update_fields))

    def update_fields(self, event : tk.Event = None) -> None:
        input_frame = self.wnd_comps['input_frame']

        for widget in input_frame.winfo_children():
            widget.destroy()

        self.entries.clear()

        conversion_type = self.wnd_comps['conversion_type']

        if conversion_type.get() == conversion_types.DECIMAL_TO_HEX.value:
            self.create_entry("Value:", 0)
        else:
            
            data_type = self.wnd_comps['data_type']

            if data_type.get() == data_types.UINT16.value:
                self.create_uint16_entry()
            elif data_type.get() == data_types.UINT32.value:
                self.create_uint32_entry()

    def create_uint32_entry(self) -> None:
        uint32_size = data_types.UINT32.size
        self.create_special_entry(uint32_size)

    def create_uint16_entry(self) -> None:
        uint16_size = data_types.UINT16.size
        self.create_special_entry(uint16_size)

    def create_special_entry(self, length : int) -> None:
        for idx in range(length):
            self.create_entry(f"Byte {idx + 1}", idx)

    def create_entry(self, label_text: str, row: int):
        input_frame = self.wnd_comps['input_frame']

        tk.Label(input_frame, text=label_text).grid(row=row, column=0)
        entry = tk.Entry(input_frame)
        entry.grid(row=row, column=1)
        self.entries.append(entry)

    def convert_text(self) -> None:
        try:
            values = [entry.get() for entry in self.entries]

            conversion_type = self.wnd_comps['conversion_type']
            strategy = ConversionFactory.get_strategy(conversion_type.get())

            data_type = self.wnd_comps['data_type']
            result = strategy.convert(values, data_type.get())

            result_text = self.wnd_comps['result_text']
            result_text.delete('1.0', tk.END)  # clear
            result_text.insert(tk.END, result)
        except ValueError as err:
            messagebox.showerror(title="Input Error", message="Please enter valid numbers!")
            print(err)