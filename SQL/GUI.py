import tkinter as tk
from tkinter import ttk


class GUI:
    print("SQL GUI")
    def __init__(self, command_executor, df):
        self.ce = command_executor
        self.table_name = command_executor.get_table_name()
        self.dataframe = df


        self.label_list = []


        self.root = tk.Tk()
        self.root.title("SQL Project")
        self.root.geometry("1200x1900")
        self.root.config(bg="#F5F5F7")

        self.build_frames()
        self.build_labels()
        self.build_buttons()
        self.record_entry = tk.StringVar(value="")


        self.canvas = tk.Canvas(self.frame_right, bg="#f0f0f0")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.frame_right, orient="vertical",
                                       command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame_right.grid_rowconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=1)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.canvas_window = self.canvas.create_window((0, 0),
                                                       window=self.scrollable_frame,
                                                       anchor="nw")

        self.scrollable_frame.bind("<Configure>", self.configure_scroll_region)
        self.canvas.bind("<Configure>", self.configure_canvas_width)



        self.root.mainloop()

    def configure_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def configure_canvas_width(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)


    def select_btn_trigger(self):
        print("Button Select Triggered!")
        data_list = self.ce.execute("SELECT", table_name=self.table_name)

        self.label_table.config(text=f"{self.table_name}")
        self.create_btn_trigger()
        for row_index, rows in enumerate(data_list, start=1):
            for col_index, cols in enumerate(rows):
                record_label = tk.Label(self.scrollable_frame, text=cols,
                                        bg="light blue", bd=2, relief="solid",
                                        width=15)
                self.label_list.append(record_label)
                record_label.grid(row=row_index, column=col_index)



        # for index , rows in enumerate(data_list):
        #     print(rows)
        # print(f"Rows:", len(data_list))


    def create_label_insert_rows(self, rows_data):
        for row_index, rows in enumerate(rows_data, start=1):
            for col_index, cols in enumerate(rows):
                record_label = tk.Label(self.scrollable_frame, text=cols,
                                        bg="light blue", bd=2, relief="solid",
                                        width=15)
                record_label.grid(row=row_index, column=col_index)


    def create_table_cols(self):
        for column_index, column_headers in enumerate(self.cols_header):
            column_label = tk.Label(self.scrollable_frame, text=column_headers,
                                    bg="light green", bd=2, relief="solid",
                                    width=15)
            self.label_list.append(column_label)
            column_label.grid(row=0, column=column_index)

    def create_btn_trigger(self):
        print("Button Create Triggered!")
        self.cols_header = self.ce.execute("CREATE", table_name=self.table_name,
                        cols=self.dataframe.get_df_cols())
        self.label_table.config(text=f"{self.table_name}")
        self.create_table_cols()

    def insert_btn_trigger(self):
        print("Button Insert Triggered!")

        rows_data = []
        df_dict = self.dataframe.to_dict()
        for row in df_dict:
            # print(row)
            rows_data.append(self.ce.execute("INSERT", table_name=self.table_name, row=row))

        print(rows_data)
        self.create_label_insert_rows(rows_data)

    def update_pop_up_win(self, event):
        self.win_prompt = tk.Toplevel(self.root, background="grey")
        self.win_prompt.title("UPDATE")
        self.win_prompt.geometry("600x100")
        self.win_prompt.resizable(True, True)

        set_label = tk.Label(self.win_prompt, text="SET",
                             bg="yellow", bd=2, relief="solid", width=12)
        set_label.grid(row=1, column=0)

        set_label = tk.Label(self.win_prompt, text="WHERE",
                             bg="yellow", bd=2, relief="solid", width=12)
        set_label.grid(row=2, column=0)

        for column_index, column_headers in enumerate(
                self.dataframe.get_df_cols(), start=1):
            column_label = tk.Label(self.win_prompt, text=column_headers,
                                    bg="light green", bd=2, relief="solid",
                                    width=15)
            column_label.grid(row=0, column=column_index)

        self.set_entry_dict = {}
        for col_index, col_header in enumerate(self.cols_header, start=1):
            var_data = tk.StringVar()
            self.set_entry_dict[col_header] = var_data

            update_entry = tk.Entry(self.win_prompt,
                                    textvariable=self.set_entry_dict[
                                        col_header],
                                    bd=2, relief="solid",
                                    font=("Arial", 15), width=15)
            update_entry.grid(row=1, column=col_index)

        self.where_entry_dict = {}
        for col_index, col_header in enumerate(self.cols_header, start=1):
            var_data = tk.StringVar()
            self.where_entry_dict[col_header] = var_data

            update_entry = tk.Entry(self.win_prompt,
                                    textvariable=self.where_entry_dict[
                                        col_header],
                                    bd=2, relief="solid",
                                    font=("Arial", 15), width=15)
            update_entry.grid(row=2, column=col_index)

        btn_update_submit = tk.Button(self.win_prompt,
                                      text="Submit",
                                      font=("Inter", 18),
                                      background="black",
                                      command=self.update_btn_trigger,
                                      padx=10)
        btn_update_submit.grid(row=5, column=0)

    def update_btn_trigger(self):
        print("Update button triggered!")

        cols_dict = {}
        for key, val in self.set_entry_dict.items():
            cols_dict[key] = val.get()
            if cols_dict[key] == "":
                del cols_dict[key]

        for k, v in cols_dict.items():
            print(f"{k} {v}")

        where_dict = {}
        for key, val in self.where_entry_dict.items():
            where_dict[key] = val.get()
            if where_dict[key] == "":
                del where_dict[key]

        result = self.ce.execute("UPDATE", table_name=self.table_name,
                                 cols=cols_dict,
                                 where=where_dict)
        self.select_btn_trigger()

        print(result)

    def drop_btn_table(self):
        print("Dropping the table...")
        self.ce.execute("DROP", table_name=self.table_name)

        print(self.label_list)
        for label in self.label_list:
            label.config(text="")



    def delete_btn_trigger(self):
            where_dict = {}
            for key, val in self.delete_entry_dict.items():
                where_dict[key] = val.get()
                if where_dict[key] == "":
                    del where_dict[key]

            self.ce.execute("DELETE", table_name=self.table_name,
                            where=where_dict)

            self.select_btn_trigger()

    def delete_pop_up_win(self, event):
        self.win_prompt = tk.Toplevel(self.root, background="grey")
        self.win_prompt.title("DELETE")
        self.win_prompt.geometry("600x100")
        self.win_prompt.resizable(True, True)

        set_label = tk.Label(self.win_prompt, text="WHERE",
                                bg="yellow", bd=2, relief="solid", width=12)
        set_label.grid(row=1, column=0)

        for column_index, column_headers in enumerate(
                self.dataframe.get_df_cols(),
                start=1):
            column_label = tk.Label(self.win_prompt, text=column_headers,
                                    bg="light green", bd=2, relief="solid",
                                    width=15)
            column_label.grid(row=0, column=column_index)

        self.delete_entry_dict = {}
        for column_index, column_headers in enumerate(self.dataframe.get_df_cols(),start=1):
            var_data = tk.StringVar()
            self.delete_entry_dict[column_headers] = var_data

            delete_entry_dict = tk.Entry(self.win_prompt,
                                         textvariable=self.delete_entry_dict[column_headers],
                                            bd=2, relief="solid",
                                            font=("Arial", 15), width=15)
            delete_entry_dict.grid(row=1, column=column_index)

        btn_update_submit = tk.Button(self.win_prompt,
                                      text="Submit",
                                      font=("Inter", 18),
                                      background="black",
                                      command=self.delete_btn_trigger,
                                      padx=10)
        btn_update_submit.grid(row=2, column=0)

    def build_buttons(self):
        btn_create = tk.Button(self.sql_query_frame,
                               text="CREATE TABLE",
                               font=("Inter", 18),
                               background="black",
                               command=self.create_btn_trigger,
                               padx=1)

        btn_create.pack(padx=10, pady=10)

        btn_drop_table = tk.Button(self.sql_query_frame,
                                   text="DROP TABLE",
                                   font=("Inter", 18),
                                   background="black",
                                   command=self.drop_btn_table,
                                   padx=2)
        btn_drop_table.pack(padx=10, pady=10)

        btn_insert = tk.Button(self.sql_query_frame,
                               text="INSERT",
                               font=("Inter", 18),
                               background="black",
                               command=self.insert_btn_trigger,
                               padx=30)

        btn_insert.pack(padx=10, pady=10)

        btn_select = tk.Button(self.sql_query_frame,
                               text="SELECT",
                               font=("Inter", 18),
                               background="black",
                               command=self.select_btn_trigger,
                               padx=30)

        btn_select.pack(padx=10, pady=10)
        # btn_select.bind("<Button-1>", self.select_pop_up_win)

        btn_update = tk.Button(self.sql_query_frame,
                               text="UPDATE",
                               font=("Inter", 18),
                               background="black",
                               padx=30)

        btn_update.pack(padx=10, pady=10)
        btn_update.bind("<Button-1>", self.update_pop_up_win)

        btn_delete = tk.Button(self.sql_query_frame,
                               text="DELETE",
                               font=("Inter", 18),
                               background="black",
                               padx=30)

        btn_delete.pack(padx=10, pady=10)
        btn_delete.bind("<Button-1>", self.delete_pop_up_win)

    def build_labels(self):
        label_sql = tk.Label(self.sql_query_frame,
                         text="SQL Query",
                         font=("Arial", 25))
        label_sql.pack(padx=20,pady=20, ipadx=20)

        self.label_table = tk.Label(self.header_frame,
                             text="Table Name",
                             font=("Arial", 25))
        self.label_table.pack(padx=1, pady=1, ipadx=1)



    def build_frames(self):
        self.header_frame = tk.Frame(self.root,
                                     width=200,
                                     height=40,
                                     background="#C9C9C9")
        self.header_frame.pack(side="top",anchor="center",padx=1, pady=1)
        # === Left Frame ===
        self.sql_query_frame = tk.Frame(self.root,
                                    width=200,
                                    height=100,padx=1, pady=1,
                                    background="#C9C9C9")
        self.sql_query_frame.pack(side='left',
                              anchor='n',
                              ipadx=10,
                              padx=10,
                              pady=10,
                              fill='x')
        # === Right Frame ===
        self.frame_right = tk.Frame(self.root,
                                     width=500, height=1,
                                     padx=1, pady=1,
                                     background="#C9C9C9")
        self.frame_right.pack(side='right',
                               padx=10, pady=10,
                               expand=True, fill='both')










    # def build_window_configuration(self):
    #     self.root = tk.Tk()
    #     self.root.title("SQL Project")
    #     self.root.geometry("1200x1900")
    #     self.root.config(bg="#F5F5F7")


