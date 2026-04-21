import tkinter as tk
import tkinter.scrolledtext as scrolltext

class GUI:
    def __init__(self, scrape_web_page):
        self._scraper = scrape_web_page

        #    Root Window Configuration
        self._build_window_configuration()

        #    Build Variables Functions
        self._build_variables()

        #    Build Frames Functions
        self._build_frames()

        #    Build Labels Functions
        self._build_labels()

        #    Build Button Functions
        self._build_radio_btn()
        self._build_generate_btn()

        #    Build Textbox Functions
        self._build_text_box()


        self._root.mainloop()

    def _build_radio_btn(self):
        """
        Creates radio buttons using a list
        """
        for button in self._radio_btn_list:
            tk.Radiobutton(
                self._frame_left,
                text=button,
                variable=self._var_string_value,
                value=button,
                bg="white",
                fg="black",
                font=("Arial", 20),
                pady=10,
                width=20,
            ).pack(anchor="w",fill='x')

    def _build_generate_btn(self):
        """
        Creates a generate button and command uses a function
        """
        generate_btn = tk.Button(
            self._frame_left,
            text="GENERATE",
            command=self._on_click_btn_generate,
            font=("Helvetica", 18, "bold"),
            fg="#1493B5",
            padx=20,
            pady=10,
        )
        generate_btn.pack(side="bottom", fill="x")


    def _on_click_btn_generate(self):
        """
        Triggered when a button is clicked, clears the textbox
        and displays the generated text from scrape_web_page
        """
        self._display_tags = ""
        self._clear_text()
        selected_tag = self._var_string_value.get()
        self._display_tags = self._scraper.find_all(selected_tag)
        self.text_box_area.insert(tk.INSERT, self._display_tags)


    def _clear_text(self):
        """
        Clears the display of Textbox Area
        """
        return self.text_box_area.delete(1.0, tk.END)


    def _build_text_box(self):
        """
        Creates a textbox with a scrollable area
        """
        self.text_box_area = scrolltext.ScrolledText(self._frame_right,
                                             width=90,
                                             height=50,
                                             font=("Arial", 20))
        self.text_box_area.pack(fill="x")
        self.text_box_area.configure(state="normal")

    def _build_labels(self):
        """
        Creates labels on each frame
        """
        # === Left Labels ===
        self._title_label_left = tk.Label(self._frame_left,
                                          text="Select a Tag to Display",
                                          background="#DEAA5F",
                                          anchor='n',
                                          font=("Arial", 20, "bold"),
                                          padx=5, pady=5)
        self._title_label_left.pack(side='top', fill='x')

        # === Right Labels ===
        self.title_label_right = tk.Label(self._frame_right,
                                          text="Display HTML Tags",
                                          background="#3498DB",
                                          anchor='n',
                                          font=("Arial", 20, "bold"),
                                          padx=5, pady=5)
        self.title_label_right.pack(side='top', fill='x')

    def _build_frames(self):
        """
        Builds the left and right frames
        """
        # === Left Frame ===
        self._frame_left = tk.Frame(self._root,
                                    width=200,
                                    height=1000,padx=1, pady=1,
                                    background="#C9C9C9")
        self._frame_left.pack(side='left',
                              anchor='n',
                              ipadx=10,
                              padx=10,
                              pady=10,
                              fill='x')
        # === Right Frame ===
        self._frame_right = tk.Frame(self._root,
                                     width=500, height=200,
                                     padx=1, pady=1,
                                     background="#C9C9C9")
        self._frame_right.pack(side='right',
                               padx=10, pady=10,
                               expand=True, fill='both')

    def _build_variables(self):
        """
        Builds variables which will be used to get values
        """
        self._radio_btn_list = ["table", "tr", "th", "td"]
        self._var_string_value = tk.StringVar(self._root,
                                              f"{self._radio_btn_list[0]}")

    def _build_window_configuration(self):
        """
        Builds the window configuration
        """
        self._root = tk.Tk()
        self._root.title("Web Scraper App")
        self._root.geometry("1200x1900")
        self._root.config(bg="#F5F5F7")
