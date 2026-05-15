import csv
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk


def command_test():
    print("hello")

class CSVLoader:
    def __init__(self, csv_file):
        self.dataframe = self.csv_loader(csv_file)


    def csv_loader(self, file):
        if not os.path.exists(file):
            print("File not found.")
            return



        data_list = []
        with open(file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for value in reader:
                data_list.append(value)




        # print(pd.DataFrame(data_list))
        return pd.DataFrame(data_list)


class DataFrameView:
    def __init__(self, root, csv_loader):
        self.dframe = csv_loader.dataframe
        self.columns = self.dframe.columns
        col_len = len(self.columns)

        print(self.dframe)

        self.root = root
        self.root.title("DataFrame Viewer")
        self.root.geometry("1450x900")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)


        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(frame, bg="#f0f0f0")
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical",
                                  command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas)

        canvas.create_window((0, 0), window=scrollable_frame,
                                             anchor="nw")

        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", configure_scroll_region)

        for column_index, column_headers in enumerate(self.columns):
            column_label = tk.Label(scrollable_frame, text=column_headers, bg="light green", bd=2, relief="solid", width=10)
            column_label.grid(row=0, column=column_index)

        # Build the buttons
        # print(self.dframe.values)
        # for every value, create a button
        buttons = []
        for row_index, value in enumerate(self.dframe.values):
            print(f"row_index: {row_index}")
            for col_index, field in enumerate(value):

                column_name = self.columns[col_index]
                print(f"column: {column_name}")
                button = tk.Button(scrollable_frame, text=field, width=14, font=('Inter', 14),
                                   command=lambda row_i=row_index, col_name=column_name, f=field: CellInspector(self.root, row_i, col_name, f))

                buttons.append(button)



        # button1 = tk.Button(root, text="Button 1")
        # button2 = tk.Button(root, text="Button 2")
        # button3 = tk.Button(root, text="Button 3")

        #
        # buttons[0].grid(row=0, column=0)
        # buttons[1].grid(row=0, column=1)
        # buttons[2].grid(row=0, column=2)
        # buttons[3].grid(row=1, column=0)
        # buttons[4].grid(row=1, column=1)
        # buttons[5].grid(row=1, column=2)
        # buttons[6].grid(row=2, column=0)
        # buttons[7].grid(row=2, column=1)
        # buttons[8].grid(row=2, column=2)

        # place the buttons
        i = 0
        for b in buttons:
            row = (i // col_len) + 1
            column = i % col_len
            b.grid(row=row, column=column)
            i += 1

        root.mainloop()

class CellInspector:
    def __init__(self, parent, row_idx, col_name, value):

        win_prompt = tk.Toplevel(parent, background="grey")
        win_prompt.geometry("600x100")
        win_prompt.title("Cell Inspector")
        win_prompt.resizable(True, True)

        print(value)

        combined_text_widget = tk.Text(win_prompt,
                                           font=("Arial", 30, "bold"),
                                           # Optional: dark bg makes cyan pop
                                           height=5,
                                           width=40,
                                           highlightthickness=0)

        combined_text_widget.tag_configure("index",)
        combined_text_widget.tag_configure("column name")
        combined_text_widget.tag_configure("cell value")

        combined_text_widget.insert("end", "index:", "index")
        combined_text_widget.insert("end", row_idx, "cell value")
        combined_text_widget.insert("end", "\n", "index")

        combined_text_widget.insert("end", "column:", "column name")
        combined_text_widget.insert("end", col_name, "cell value")
        combined_text_widget.insert("end", "\n", "column_name")

        combined_text_widget.insert("end", "cell value:", "cell value")
        combined_text_widget.insert("end", value, "cell value")
        combined_text_widget.insert("end", "\n", "cell value")

        combined_text_widget.pack()


