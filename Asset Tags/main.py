import sqlite3
import pandas as pd
from collections import defaultdict


def main():

    conn = sqlite3.connect("asset_tag.db")

    device_type = "LT-"
    alphabet = ['A', 'B', 'C', 'D']
    numbers = []
    for num in range(401, 999):
        str_i = str(num)
        numbers.append(str_i)



    hostname_dict = {}
    # print(hostname_dict)
    hostname = []
    for index, num in enumerate(numbers, start=401):
        new_hostname = device_type + "B" + num + "-B1"
        hostname_dict[index] = new_hostname

    df = pd.DataFrame(list(hostname_dict.items()), columns=['ID', 'Hostname'])

    #
    conn = sqlite3.connect("asset_tag.db")
    cursor = conn.cursor()
    # CREATE TABLE IF NOT EXISTS Presidents(Presidency TEXT UNIQUE,President TEXT,Wikipedia_Entry TEXT,Took_office TEXT,Left_office TEXT,Party TEXT,Portrait TEXT,Thumbnail TEXT,Home_State TEXT)
    cursor.execute("CREATE TABLE IF NOT EXISTS AssetTag(ID TEXT UNIQUE, Hostname TEXT UNIQUE)")
    conn.commit()


    table_name = "AssetTag"
    cols_len = 2
    cols_name = ", ".join(f"{cols_n}" for cols_n in df.keys())
    placeholders = ",".join("?" * cols_len)
    sql_insert = f"""
                INSERT INTO {table_name}({cols_name})
                VALUES ({placeholders})
            """
    # df_dict = df.to_dict()
    # print(type(df_dict))
    # for row in df.values:
    #     tup = tuple(row)
    #     print(type(tup[1]))
    #     cursor.execute(sql_insert, tup)
    #     conn.commit()
    #
    # result = generate_tag(table_name, conn)
    # cursor.execute(sql_insert, (1000, result))
    # conn.commit()
    #
    # for i in range(1099, 1998):
    result = generate_tag(table_name, conn)
    cursor.execute(sql_insert, (2001, result))
    conn.commit()

    # delete_last_row(table_name, cursor, conn)


"""
LT-A001
LT-B002
DT-A101
DT-B102
HD-A999
HD-B001
"""


def generate_tag(table_name, conn):
    alpha_letters = ("A", "B", "C", "D", "E", "F", "G", "H",
                     "I", "J", "K", "L", "M", "N", "O", "P",
                     "Q", "R", "S", "T", "U", "V", "W", "X",
                     "Y", "Z")

    sql_db = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    # print(sql_db)
    last_row = sql_db.tail(1)
    hostname = last_row.Hostname.values
    print(hostname[0])
    curr_alpha_letter = hostname[0][3]
    print(curr_alpha_letter)
    uid_num = hostname[0][4:7]


    # if length of str is 4. Then it is going to the thousandth place
    # we want it to go back to 001 but with the next alphabet letter
    # A999
    # B001
    # B999
    # C001
    new_uid_num = int(uid_num) + 1
    if len(str(new_uid_num)) == 4:
        # move to the next alphabet
        # reset uid to 000
        if curr_alpha_letter in alpha_letters:
            curr_alpha_index = alpha_letters.index(curr_alpha_letter)
            next_alpha_index = curr_alpha_index + 1
            curr_alpha_letter = alpha_letters[next_alpha_index]
            print(f"New letter: {curr_alpha_letter}")

            reset_uid_num = 0
            print(f"New UID: {new_uid_num}")
            new_generated_tag = "LT-" + curr_alpha_letter + str(reset_uid_num).zfill(3) + "-B1"
            print(new_generated_tag)
            return new_generated_tag

    new_generated_tag = "LT-" + curr_alpha_letter + str(new_uid_num).zfill(3) + "-B1"
    print(new_generated_tag)
    return new_generated_tag

def delete_last_row(table, cursor, conn):
    sql_delete = f"""
                DELETE FROM {table} WHERE ID = 1
            """
    cursor.execute(sql_delete)
    conn.commit()








if __name__ == "__main__":
    main()