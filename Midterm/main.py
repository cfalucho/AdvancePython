from CSVLoader import CSVLoader, DataFrameView
import tkinter as tk


def main():
    filename = "../SQL/Presidents.csv"

    df = CSVLoader(filename)

    root = tk.Tk()
    DataFrameView(root, df)



if __name__ == '__main__':
    main()