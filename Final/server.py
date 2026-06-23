import socket
import json
from database import Database

class RobotServer:
    def __init__(self, logger):
        self.HOST = '127.0.0.1'
        self.PORT = 65000
        self.logger = logger


    def run(self):
        db = Database()
        db.connect()

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

                    opcode_msg = json.loads(data.decode("utf-8"))
                    print(f"[SERVER]: Received {opcode_msg}")

                    opcode = opcode_msg.get("opcode")
                    if opcode:
                        result = db.get_action_for_opcode(opcode_msg["opcode"])
                    else:
                        result = None

                    if result:
                        response = json.dumps({"action": result})
                    else:
                        response = json.dumps({"error": "Invalid or missing opcode"})

                    conn.sendall(response.encode("utf-8"))