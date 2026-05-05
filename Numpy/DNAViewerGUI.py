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
                                  width=20,
                                  height=100,
                                  border=1)
        self.listbox.insert(tk.END, *self.strand_names)
        self.listbox.pack(pady=20)
        self.listbox.bind('<<ListboxSelect>>', self.pop_up_window)


        return self.listbox

    def create_frame(self):
        self.root = tk.Tk()
        self.root.title("DNA Strand")
        self.root.geometry("550x500")
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
            item_selected = self.series.dna_objects_series[strand_name]
            codon_sequence_list = item_selected.get_strand()
            print(codon_sequence_list)

            # assign mutated string
            mutated_str = codon_sequence_list[0]

            # assign the color index item into a variable
            start_codon = codon_sequence_list[1][0]
            start_codon_color = codon_sequence_list[1][1]

            protein_region = codon_sequence_list[2][0]
            protein_region_color = codon_sequence_list[2][1]

            stop_codon = codon_sequence_list[3][0]
            stop_codon_color = codon_sequence_list[3][1]

            # builds the text for each codon sequence
            # apply the corresponding color to each codon sequence
            start_codon_text_widget = tk.Text(win_prompt,
                                              font=("Arial", 30, "bold"),
                                              fg=start_codon_color,
                                              height=5,
                                              width=5,
                                              highlightthickness=0)

            protein_region_text_widget = tk.Text(win_prompt,
                                                 font=("Arial", 30, "bold"),
                                                 fg=protein_region_color,
                                                 width=23,height=5,
                                                 highlightthickness=0
                                                 )


            stop_codon_text_widget = tk.Text(win_prompt,
                                             font=("Arial", 30, "bold"),
                                             fg=stop_codon_color,
                                             width=7,height=5,
                                             highlightthickness=0)

            start_codon_text_widget.grid(row=0, column=0)
            protein_region_text_widget.grid(row=0, column=1)
            stop_codon_text_widget.grid(row=0,column=2)

            start_codon_text_widget.insert("end", f"{start_codon}")
            protein_region_text_widget.insert("end", f"{protein_region}")
            stop_codon_text_widget.insert("end", f"{stop_codon}")

            if mutated_str == "Mutated":
                start_codon_text_widget.config(bg="#fbeeb8")
                protein_region_text_widget.config(bg="#fbeeb8")
                stop_codon_text_widget.config(bg="#fbeeb8")
                win_prompt.title(f"{strand_name}  MUTATED")


    def run(self):
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