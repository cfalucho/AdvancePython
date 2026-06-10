import time
import logging
import tkinter as tk
import threading
import pandas as pd
import re
from SQL import QueryBuilder, CommandExecutor
from queue import Queue


def database_filename(filename):
    db_file = re.sub(r'.csv', '.db',  filename)
    return db_file

def table_name(filename):
    # remove .csv extension and use the file name for table name
    match = re.search(r"^(.+)\.csv$", filename)
    if match:
        name_only = match.group(1)
        return name_only
    return None

class DataFrame:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file, dtype=str)
        self.db_filename = database_filename(csv_file)
        self.table_name = table_name(csv_file)
        self.df.columns = self.df.columns.str.strip()
        self.df.columns = [re.sub(r' ', '_', key)
                                  for key in self.df.columns]



    def get_db_filename(self):
        return self.db_filename

    def get_table_name(self):
        return self.table_name

    def get_df(self):
        return self.df

    def get_list(self):
        return self.df.to_dict(orient='records')

    def iter_rows(self):
        for index, row in self.df.iterrows():
            yield row.to_dict()

    def get_cols(self):
        return tuple(self.df.columns)



class Producer(threading.Thread):
    def __init__(self, csv_file, shared_queue):

        super().__init__()
        self.csv_file = csv_file
        self.queue = shared_queue
        self.df = DataFrame(csv_file)

    def run(self):
        print("Producer running...")

        table_task = {'seq_num': 0, 'query': 'CREATE', 'kwargs':
                     {'table_name': self.df.get_table_name(), 'row': self.df.get_cols()}
                      }
        self.queue.put(table_task)
        logging.info(
            logging.info(f'Producer generating SEQ #{table_task['seq_num']}'))

        rows = self.df.iter_rows()
        for seq_num, row in enumerate(rows, start=1):
            query_task = {'seq_num': seq_num, 'query': 'INSERT', 'kwargs':
                     {'table_name': self.df.get_table_name(), 'row': row}}
            self.queue.put(query_task)
            print(f'Inside producer: {query_task['seq_num']}')
            logging.info(f'Producer generating SEQ #{query_task['seq_num']}: {query_task['query']}')
            time.sleep(0.10)

        self.queue.put(None)





class Consumer(threading.Thread):
    def __init__(self, command_executor, shared_queue):
        super().__init__()
        self.queue = shared_queue
        self.ce = command_executor

    def run(self):
        print("Server now running." + "\n" +
              "Listening for requests..")
        while True:
            # print(self.queue.get())
            task = self.queue.get()

            if task is None:
                print("No more items in queue.")
                break
            seq_num = task['seq_num']
            sql_query = task['query']
            table_name = task['kwargs']['table_name']
            row=task['kwargs']['row']
            # print(task['query'], task['kwargs']['table_name'], task['kwargs']['row'])
            self.ce.execute(sql_query, table_name=table_name, row=row)
            logging.info(
                f'Consumer processing SEQ #{seq_num} {sql_query}')
            time.sleep(1)






def with_threads(producer, df, shared_queue):
    producer.start('CREATE', cols=df.get_cols())
    producer.producer_thread.join()

    start = time.perf_counter()
    row_gen = df.iter_rows()

    all_rows = df.get_list()

    producer.start('INSERT', rows=all_rows)
    producer.producer_thread.join()

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 3)} second(s)')

def without_threads(ce, df):
    ce.execute('CREATE', table_name=df.get_table_name(), cols=df.get_cols())

    start = time.perf_counter()
    rows = df.iter_rows()
    for row in rows:
        ce.execute('INSERT', table_name=df.get_table_name(), row=row)

    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 3)} second(s)')

class GUI:
    def __init__(self, producer, consumer, shared_queue):
        self.client = producer
        self.server = consumer
        self.queue = shared_queue


        self.root = tk.Tk()
        self.root.title("SQL Project")
        self.root.geometry("900x900")
        self.root.config(bg="#F5F5F7")



        self.build_frames()
        self.build_labels()
        self.build_text()
        self.build_buttons()

        self.root.mainloop()

    def build_labels(self):
        self.producer_lbl = tk.Label(self.root, text='Producer Thread', font=('Inter', 20))
        self.producer_lbl.grid(row=0, column=1)

        self.consumer_lbl = tk.Label(self.root, text='Consumer Thread',
                                     font=('Inter', 20))
        self.consumer_lbl.grid(row=0, column=2)
    def build_frames(self):
        self.producer_frame = tk.Frame(self.root)
        self.producer_frame.grid(row=1, column=1, pady=10, padx=20)

        self.consumer_frame = tk.Frame(self.root)
        self.consumer_frame.grid(row=1, column=2, pady=10, padx=20)

    def build_text(self):
        self.producer_text = tk.Text(self.producer_frame, height=35, width=60, background="#272932", foreground="#EDD83D",
                                     font=('Inter', 15),
                                      state="disabled")
        self.producer_text.grid(row=0, column=0)

        self.consumer_text = tk.Text(self.consumer_frame, height=35, width=60,
                                     background="#272932",
                                     foreground="#628B48",
                                     font=('Inter', 15),
                                     state="disabled")
        self.consumer_text.grid(row=0, column=0)

    def build_buttons(self):
        self.start_client = tk.Button(self.root,
                               text="Start Client",
                               font=("Inter", 18),
                               background="black",
                               command=self.start_client,
                               padx=1)

        self.start_client.grid(row=2, column=1)

        self.start_server = tk.Button(self.root,
                                      text="Start Server",
                                      font=("Inter", 18),
                                      background="black",
                                      command=self.start_server,
                                      padx=1)

        self.start_server.grid(row=2, column=2)



    def start_client(self):
        self.start_client.config(state="disabled")

        tkinter_thread = threading.Thread(target=self.queue_producer_log,
                                           daemon=True)
        tkinter_thread.start()

    def start_server(self):
        self.server.start()
        self.queue_consumer_log()


    def queue_producer_log(self):
        self.client.start()
        while True:
            # task = self.queue.get()
            query_text = (f'PRODUCER: SEQ #{task['seq_num']}: ')
                          # f'{task['query']}: {task['kwargs']['row']}') + "\n"
            logging.info(f'Producer generating SEQ #{task['seq_num']}: {task['query']}')

            self.root.after(0, self.update_producer_text, query_text)
            time.sleep(2)
            # self.queue.task_done()
            if task is None:
                self.queue.task_done()
                break

    def queue_consumer_log(self):
        while True:
            # task = self.queue.get()
            query_text = f"test"
            # query_text = (f'CONSUMER: SEQ #{task['seq_num']}: ')
            # f'{task['query']}: {task['kwargs']['row']}') + "\n"

            self.root.after(0, self.update_consumer_text, query_text)
            time.sleep(2)
            self.queue.task_done()
            if task is None:
                self.queue.task_done()
                break

    def update_producer_text(self, text):
        self.producer_text.config(state='normal')
        self.producer_text.insert('end', f"{text}\n")
        self.producer_text.config(state='disabled')
        self.producer_text.see('end')

    def update_consumer_text(self, text):
        self.consumer_text.config(state='normal')
        self.consumer_text.insert('end', f"{text}\n")
        self.consumer_text.config(state='disabled')
        self.consumer_text.see('end')


def main():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(name)s: [%(threadName)s] %(message)s'))
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    csv_file = "Presidents.csv"
    shared_queue = Queue()
    df = DataFrame(csv_file)
    qb = QueryBuilder()
    ce = CommandExecutor(df, qb)



    producer = Producer(csv_file, shared_queue)
    # producer.start()
    consumer = Consumer(ce, shared_queue)
    # consumer.start()
    GUI(producer, consumer, shared_queue)


    # while not shared_queue.empty():
    #     print("Queue Item:", shared_queue.get())




if __name__ == '__main__':
    main()