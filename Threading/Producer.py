import time
import logging

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
        # print("Running...")
        logging.info("Thread starting")
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
            logging.info(f'Producer generating SEQ #{query_task['seq_num']}: {query_task['query']}')

        self.queue.put(None)





class Consumer(threading.Thread):
    def __init__(self, command_executor, shared_queue):
        super().__init__()
        self.queue = shared_queue
        self.ce = command_executor

    def run(self):
        print("Consumer running...")

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


def main():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(name)s: [%(threadName)s] %(message)s'))
    # set the new log handler
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    csv_file = "Presidents.csv"
    shared_queue = Queue()
    df = DataFrame(csv_file)
    qb = QueryBuilder()
    ce = CommandExecutor(df, qb)



    producer = Producer(csv_file, shared_queue)
    producer.start()
    consumer = Consumer(ce, shared_queue)
    consumer.start()


    # while not shared_queue.empty():
    #     print("Queue Item:", shared_queue.get())




if __name__ == '__main__':
    main()