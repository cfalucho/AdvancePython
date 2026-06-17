import tkinter as tk
import socket
import pandas as pd
import threading
import re
import time
import json
from tkinter import scrolledtext
from SQL import QueryBuilder, CommandExecutor
from DataFrame import DataFrame


class Server(threading.Thread):
    def __init__(self):
        super().__init__()
        self.HOST = '127.0.0.1'
        self.PORT = 65000

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.HOST, self.PORT))
            sock.listen()
            print("[SERVER]: Listening for incoming requests...")
            conn, address = sock.accept()

            with conn:
                print(f"[SERVER]: Connected by {address}")


                while True:
                    data = conn.recv(1024)

                    # receive the data as a json

                    # {
                    #   "query": "<SQL string>"
                    # }
                    if not data:
                         break

                    sql_msg = json.dumps(data.decode("utf-8"))
                    print(sql_msg)
                    print(f"[SERVER]: Received {sql_msg}" )
                    # conn.sendall(data)

            time.sleep(1)

class Client:
    def __init__(self, csv_file):
        self.HOST = '127.0.0.1'
        self.PORT = 65000
        self.qb = QueryBuilder()
        self.df = DataFrame(csv_file)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.HOST, self.PORT))
            print(f"[CLIENT]: Connected to server. Sending data...")

            query = self.qb.create_table(self.df.get_table_name(), self.df.get_cols())
            json_data = json.dumps(query, indent=2)
            print(json_data)
            sock.sendall(b'"query": "<SQL string>"')
            data = sock.recv(1024)
            print(f"[CLIENT]: Received from server {data.decode()}")




def log_message(widget, text):
    widget.configure(state="normal")
    widget.insert("end", text + "\n")
    widget.configure(state="disabled")
    widget.see("end")



class GUI:
    def __init__(self):
        self.csv_file = "Presidents.csv"
        self.root = tk.Tk()
        self.root.title("Sockets")
        self.root.geometry("900x900")
        self.root.config(bg="#F5F5F7")

        self.build_label()
        self.build_display()
        self.buttons()


        self.client = Client(self.csv_file)
        self.server = Server()

    def build_label(self):
        tk.client_lbl = tk.Label(text="Client")
        tk.client_lbl.grid(row=0, column=0)

        tk.server_lbl = tk.Label(text="Server")
        tk.server_lbl.grid(row=0, column=1)

    def build_display(self):
        self.client_log = scrolledtext.ScrolledText(self.root, width=50, height=20, state="disabled")
        self.client_log.grid(row=1, column=0)
        self.client_log.configure(bg='#F6D0B1')

        self.server_log = scrolledtext.ScrolledText(self.root, width=50,
                                                    height=20,
                                                    state="disabled")
        self.server_log.grid(row=1, column=1)
        self.server_log.configure(bg='#C7D66D')


    def buttons(self):
        self.start_client = tk.Button(self.root, text="Start Client", command=self.start_client_threads)

        self.start_client.grid(row=2, column=0)

        self.start_server = tk.Button(self.root, text="Start Server", command=self.start_server_threads)

        self.start_server.grid(row=2, column=1)

    def start_client_threads(self):
        self.client_thread = threading.Thread(target=self.client.start, daemon=True).start()
        log_message(self.client_log,"Client Thread Started...")


    def start_server_threads(self):
        self.server_thread = threading.Thread(target=self.server.start, daemon=True).start()
        log_message(self.server_log,"Server Thread Started...")

    def run(self):
        self.root.mainloop()



def main():
    gui = GUI()
    gui.run()


if __name__ == '__main__':
    main()