from SQL import CommandExecutor
import sqlite3
import socket
import json
from database import Database
from client import RobotClient, GUI
# from server import RobotServer

def main():

    # db.cur.execute("CREATE TABLE IF NOT EXISTS commands (opcode TEXT PRIMARY KEY,action TEXT NOT NULL, response TEXT NOT NULL);")
    #
    # db.cur.execute("""INSERT INTO commands(opcode,action,response)
    #           VALUES("000","Stop","Robot stopping") """)
    #
    # db.cur.execute("""INSERT INTO commands(opcode,action,response)
    #           VALUES("001","Power On","Robot powering on") """)
    #
    #
    # db.cur.execute("""INSERT INTO commands(opcode,action,response)
    #           VALUES("010","Move Forward","Robot moving forward") """)
    #
    # db.cur.execute("""INSERT INTO commands(opcode,action,response)
    #           VALUES("011","Move Backward","Robot moving backward") """)
    #
    # db.cur.execute("""INSERT INTO commands(opcode,action,response)
    #           VALUES("100","Turn Left","Robot turning left") """)
    #
    #
    # db.cur.execute("""INSERT INTO commands(opcode,action,response)
    #           VALUES("101","Turn Right","Robot turning right") """)
    #
    #
    # db.cur.execute("""INSERT INTO commands(opcode,action,response)
    #           VALUES("110","Raise Arm","Robot raising arm") """)
    #
    # db.cur.execute("""INSERT INTO commands(opcode,action,response)
    #           VALUES("111","Lower Arm","Robot lowering arm") """)
    #
    # db.conn.commit()

    gui = GUI()
    gui.run()


if __name__ == '__main__':
    main()