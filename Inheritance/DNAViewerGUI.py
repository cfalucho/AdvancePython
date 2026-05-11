import tkinter as tk
from tkinter import Scrollbar


"""
I do think I can probably make this class be an inheritance to DNATableModel
"""
class DNAViewerGUI:
    def __init__(self, dna_objects_series):
        self.root = None
        self.strand_names = dna_objects_series.get_list()
        self.series = dna_objects_series


        # create frame
        self.create_frame()

        self.scrollbar = self.create_scrollable_list()
        self.listbox = self.create_listbox()

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.run()

    def create_scrollable_list(self):
        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side="right", fill="both")
        return scrollbar

    def create_listbox(self):
        self.listbox = tk.Listbox(self.root,
                                  font=("Inter", 32),
                                  width=23,
                                  height=100,
                                  border=1)
        self.listbox.insert(tk.END, *self.strand_names)
        self.listbox.pack(pady=20)
        self.listbox.bind('<<ListboxSelect>>', self.pop_up_window)
        return self.listbox

    def create_frame(self):
        self.root = tk.Tk()
        self.root.title("DNA Strand App")
        self.root.geometry("500x500")
        self.root.configure(bg="#494D52")
        self.root.resizable(False, False)


    # this is called with an item is selected
    def pop_up_window(self, event):
        win_prompt = tk.Toplevel(self.root, background="grey")
        win_prompt.geometry("600x100")
        win_prompt.resizable(False, False)

        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            strand_name = event.widget.get(index)
            win_prompt.title(strand_name)
            item_selected = self.series.get_objects()[strand_name]
            strand_codon_list = item_selected.get_codon_list()

            # start codon
            start_codon_str       = strand_codon_list[0][0]
            start_codon_color_str = strand_codon_list[0][1]

            # protein region codon
            protein_region_str = " ".join([x[0] for x in strand_codon_list[1:-1]])


            # stop codon
            stop_codon_str        = strand_codon_list[-1][0]
            stop_codon_color_str  = strand_codon_list[-1][1]

            combined_text_widget = tk.Text(win_prompt,
                                           font=("Arial", 30, "bold"),
                                           # Optional: dark bg makes cyan pop
                                           height=5,
                                           width=40,
                                           highlightthickness=0)

            combined_text_widget.tag_configure("start_tag",
                                               foreground=start_codon_color_str)
            combined_text_widget.tag_configure("protein_tag",
                                               foreground="cyan")
            combined_text_widget.tag_configure("stop_tag",
                                               foreground=stop_codon_color_str)


            combined_text_widget.insert("end", start_codon_str, "start_tag")
            combined_text_widget.insert("end", " " + protein_region_str + " ",
                                        "protein_tag")
            combined_text_widget.insert("end", stop_codon_str, "stop_tag")


            combined_text_widget.config(state="disabled")  # Make it read-only
            combined_text_widget.pack()

            mutated = item_selected.get_mutation_status()
            if mutated:
                combined_text_widget.config(bg="#fbeeb8")
                win_prompt.title(f"{strand_name}")

    def run(self):
        print("Running app..")
        return self.root.mainloop()

""" References used
- Creating a scrollable listbox
https://www.geeksforgeeks.org/python/scrollable-listbox-in-python-tkinter/

- Used a modern font
https://rsms.me/inter/

https://tk-tutorial.readthedocs.io/en/latest/listbox/listbox.html

https://www.geeksforgeeks.org/python/python-tkinter-text-widget/

https://docs.python.org/3.14/library/tkinter.html#tkinter.grid
"""