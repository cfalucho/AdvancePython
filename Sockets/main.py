import tkinter as tk
import socket
import pandas as pd
import threading
import re
import time
import random
import json
from tkinter import scrolledtext
from SQL import QueryBuilder, CommandExecutor
from DataFrame import DataFrame


class Server:
    def __init__(self, logger):
        self.logger = logger
        self.HOST = '127.0.0.1'
        self.PORT = 65000

        self.ce = CommandExecutor()

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
                    if not data:
                         break

                    query_msg = json.loads(data.decode("utf-8"))
                    print(f"[SEVER]: Received {query_msg}")

                    self.logger(f"[SERVER]: Received {query_msg["query"]}\n")
                    self.logger(f"[SERVER]: Executing {query_msg["query"]}")
                    result = self.ce.execute(query_msg["query_type"])
                    print(result)

                    response = json.dumps({"value": result})
                    conn.sendall(response.encode("utf-8"))

            time.sleep(1)

class Client:
    def __init__(self, logger, csv_file):
        self.HOST = '127.0.0.1'
        self.PORT = 65000
        self.socket = None
        self.logger = logger
        self.df = DataFrame(csv_file)
        self.qb = QueryBuilder(self.df)

    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.HOST, self.PORT))
            self.logger("Connected to server.")

            # Listen for results
            while True:
                data = self.socket.recv(1024)
                # print(data)
                if not data:
                    self.logger("Server disconnected.")
                    break
                print("\n")
                msg = json.loads(data.decode("utf-8"))
                print(msg)
                self.logger(msg["value"])

        except Exception as e:
            self.logger(f"Client error: {e}")


    def request_query(self):
        query_choice = random.choice(list(self.qb.get_dispatch_keys()))
        # print(query_choice)

        query = ""
        sql_str = ""
        # query_choice = "DELETE"
        if query_choice == "CREATE":
            _, sql_str = self.qb.dispatcher(query_choice, table_name=self.df.get_table_name(), columns=self.df.get_cols())

        if query_choice == "SELECT":
            sql_str = self.qb.dispatcher(query_choice)

        if query_choice == "INSERT":
            _, sql_str = self.qb.dispatcher(query_choice, table_name=self.df.get_table_name(), columns=self.df.get_cols())

        if query_choice == "UPDATE":
            _, sql_str = self.qb.dispatcher(query_choice, table_name=self.df.get_table_name(), columns=self.df.get_cols(), values="5", where={"Presidency": 1})

        if query_choice == "DELETE":
            _, sql_str = self.qb.dispatcher(query_choice, table_name=self.df.get_table_name(), where={"Presidency": 10})

        if query_choice == "DROP":
            _, sql_str = self.qb.dispatcher(query_choice, table_name=self.df.get_table_name())


        dict_query = {"query_type": query_choice, "query":sql_str}
        print(dict_query)

        request = json.dumps(dict_query)
        print(f"[CLIENT]: Sending {request}")
        self.socket.sendall(request.encode("utf-8"))
        self.logger("Generate a query.")


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
        self.root.geometry("1000x1200")
        self.root.config(bg="#F5F5F7")

        self.build_label()
        self.build_display()
        self.buttons()


        self.client = None
        self.server = None

    def build_label(self):
        tk.client_lbl = tk.Label(text="Client")
        tk.client_lbl.grid(row=0, column=0)

        tk.server_lbl = tk.Label(text="Server")
        tk.server_lbl.grid(row=0, column=1)

    def build_display(self):
        self.client_log = scrolledtext.ScrolledText(self.root, width=80, height=20, state="disabled")
        self.client_log.grid(row=1, column=0)
        self.client_log.configure(bg='#F6D0B1')

        self.server_log = scrolledtext.ScrolledText(self.root, width=80, height=20, state="disabled")
        self.server_log.grid(row=1, column=1)
        self.server_log.configure(bg='#C7D66D')


    def buttons(self):
        self.start_client = tk.Button(self.root, text="Start Client", command=self.start_client)

        self.start_client.grid(row=2, column=0)

        self.start_server = tk.Button(self.root, text="Start Server", command=self.start_server)

        self.start_server.grid(row=2, column=1)

        self.generate_query_btn = tk.Button(self.root, text="Generate Query",
                                            command=self.generate)

        self.generate_query_btn.grid(row=3, columnspan=2)



    def start_client(self):
        if self.client is None:
            self.client = Client(
                lambda msg: log_message(self.client_log, msg), self.csv_file)
            threading.Thread(target=self.client.run, daemon=True).start()
            log_message(self.client_log, "Client thread started.")

    def start_server(self):
        if self.server is None:
            self.server = Server(lambda msg: log_message(self.server_log, msg))
            threading.Thread(target=self.server.run, daemon=True).start()
            log_message(self.server_log, "Server thread started.")



    def generate(self):
        if self.client:
            self.client.request_query()

    def run(self):
        self.root.mainloop()



def main():
    gui = GUI()
    gui.run()


if __name__ == '__main__':
    main()