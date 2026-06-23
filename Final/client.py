import socket
import json
import tkinter as tk
from tkinter import scrolledtext
from server import RobotServer
import threading

class RobotClient:
    def __init__(self, server_host, server_port, logger):
        self.HOST = server_host
        self.PORT = server_port
        self.logger = logger
        self.socket = None
        self.db_action = []


    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.HOST, self.PORT))
            print("Connected to server")
            self.logger("Connected to server.")

            # Listen for results
            while True:
                data = self.socket.recv(1024)
                if not data:
                    self.logger("Server disconnected.")
                    break
                print("\n")
                msg = json.loads(data.decode("utf-8"))
                print(f"[Client]: {msg['action']}")
                self.logger(msg['action'])

        except Exception as e:
            self.logger(f"Client error: {e}")


    def request_action(self, selected_opcode):
        dict_opcode = {"opcode": selected_opcode}
        request = json.dumps(dict_opcode)
        # print(f"[CLIENT]: Requesting {request}")
        self.socket.sendall(request.encode("utf-8"))


def log_message(widget, text):
    widget.configure(state="normal", font=("Segoe UI", 12))
    widget.insert("end", text + "\n")
    widget.configure(state="disabled")
    widget.see("end")

class GUI:
    def __init__(self):
        self.command_list = [('Stop'      , "000"),
                             ('Power On'  , "001"),
                             ('Forward'   , "010"),
                             ('Backward'  , "011"),
                             ('Turn Left' , "100"),
                             ('Turn Right', "101"),
                             ('Raise Arm' , "110"),
                             ('Lower Arm' , "111")]

        self.root = tk.Tk()
        self.root.title("Robot GUI")
        self.root.geometry("900x900")
        self.root.config(bg="#F5F5F7")

        self.connection_lb_frame()
        self.command_lb_frame()

        self.display_log_frame()
        self.server_status_lbl()
        self.build_server_btn()

        self.client = None
        self.server = None


    def connection_lb_frame(self):
        lf_connection = tk.LabelFrame(self.root, text="Connection", bg="lightgreen")
        lf_connection.grid(row=0, column=0, padx=70, pady=20)

        server_conn_label = tk.Label(lf_connection, text="Server IP Entry")
        server_conn_label.grid(row=0, column=1, padx=2, pady=10)


        self.server_conn_entry = tk.Entry(lf_connection, width=20)
        self.server_conn_entry.grid(row=0, column=2, padx=2, pady=10)

        port_conn_label = tk.Label(lf_connection, text="Port Entry")
        port_conn_label.grid(row=1, column=1, padx=2, pady=10, ipadx=4)

        self.port_conn_entry = tk.Entry(lf_connection, width=20)
        self.port_conn_entry.grid(row=1, column=2, padx=2, pady=10)

        connect_btn = tk.Button(lf_connection, text="Connect", foreground="blue", command=self.connect_to_server)
        connect_btn.grid(row=2, column=1, padx=2, pady=5)

    def command_lb_frame(self):
        lf_command = tk.LabelFrame(self.root, text="Commands", bg="lightblue", font=("Segoe UI", 12))
        lf_command.grid(row=1, column=0, padx=70, pady=20)

        mv_commands = self.command_list[:4]

        turn_left = self.command_list[4][0]
        turn_right = self.command_list[5][0]
        raise_arm = self.command_list[6][0]
        lower_arm = self.command_list[7][0]

        self.movement_var = tk.StringVar(lf_command)

        lf_movement = tk.LabelFrame(lf_command, text="Movement")
        lf_movement.pack(fill="x", pady=10)

        for (text, opcode) in mv_commands:
            tk.Radiobutton(lf_movement,text=text, value=opcode, variable=self.movement_var,
                command=self.on_radio_select).pack(fill="x", side="left")


        lf_direction = tk.LabelFrame(lf_command, text="Direction", font=("Segoe UI", 12))
        lf_direction.pack(fill="x", pady=10)
        turn_left_btn  = tk.Button(lf_direction, text=turn_left, command=self.turn_left_command, font=("Segoe UI", 12))
        turn_right_btn = tk.Button(lf_direction, text=turn_right, command=self.turn_right_command, font=("Segoe UI", 12))
        turn_left_btn.pack(fill="x", side="left")
        turn_right_btn.pack(fill="x", side="left")


        lf_arm = tk.LabelFrame(lf_command, text="Arm", font=("Segoe UI", 12))
        lf_arm.pack(fill="x",pady=10)
        raise_arm_btn  = tk.Button(lf_arm, text=raise_arm, command=self.raise_arm_command)
        lower_arm_btn  = tk.Button(lf_arm, text=lower_arm, command=self.lower_arm_command)
        raise_arm_btn.pack(fill="x", side="left")
        lower_arm_btn.pack(fill="x", side="left")


    def on_radio_select(self):
        selected_opcode = self.movement_var.get()
        self.client.request_action(selected_opcode)

    def turn_left_command(self):
        self.client.request_action(self.command_list[4][1])

    def turn_right_command(self):
        self.client.request_action(self.command_list[5][1])

    def raise_arm_command(self):
        self.client.request_action(self.command_list[6][1])

    def lower_arm_command(self):
        self.client.request_action(self.command_list[7][1])


    def connect_to_server(self):
        server_ip = self.server_conn_entry.get()
        server_port = int(self.port_conn_entry.get())

        if self.client is None:
            try:
                self.client = RobotClient(server_ip, server_port, lambda msg: log_message(self.server_log, msg))
                threading.Thread(target=self.client.run, daemon=True).start()
                log_message(self.server_log, f"Successfully connected.")
            except Exception as e:
                log_message(self.server_log, f"Failed to connect {e}.")
                self.client = None
        else:
            log_message(self.server_log, "Already connected.")

    def server_status_lbl(self):
        lbl_server_status = tk.Label(self.root, text="Server Status")
        lbl_server_status.grid(row=2, column=0)

    def display_log_frame(self):
        self.server_log = scrolledtext.ScrolledText(self.root, width=60,
                                                    height=20,
                                                    state="disabled")
        self.server_log.grid(row=3, columnspan=1)
        self.server_log.configure(bg='#F4ECD6')


    def start_server(self):
        if self.server is None:
            self.server = RobotServer(lambda msg: log_message(self.server_log, msg))
            threading.Thread(target=self.server.run, daemon=True).start()
            log_message(self.server_log, "Server starting.")


    def build_server_btn(self):
        self.start_server_btn = tk.Button(self.root, text="Start Server", command=self.start_server)
        self.start_server_btn.grid(row=4, column=0)

    def run(self):
        self.root.mainloop()


