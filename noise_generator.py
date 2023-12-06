# Noise generator by Amiah Belle Isle
import tkinter as tk
import random
from PIL import Image, ImageDraw


class MainGUI():


    def __init__(self):
        # Setting up GUI
        self.root = tk.Tk()
        self.root.title("Noise Texture Generator")
        self.root.minsize(width=400, height=300)
        # Create Widgets
        self.__create_frames()
        self.__create_entries()
        self.__create_labels()
        self.__create_radio_buttons()
        self.__create_buttons()
        self.__create_canvas()
        # Variables
        self.__original_list = self.__create_list(12)
        # Pack and enter mainloop
        self.__pack_all()
        self.root.mainloop()

    def __create_frames(self):
        # Frames to hold and group the options
        self.options_frame = tk.LabelFrame(self.root,
                                           text="Options")
        self.top_options_frame = tk.Frame(self.options_frame)
        self.bottom_options_frame = tk.Frame(self.options_frame)
        self.size_frame = tk.Frame(self.top_options_frame)
        self.seed_frame = tk.Frame(self.top_options_frame)
        self.color_frame = tk.Frame(self.bottom_options_frame)
        # Frame for the canvas
        self.canvas_frame = tk.LabelFrame(self.root,
                                          text="Noise Texture")
        # Frame for the generate/save buttons
        self.buttons_frame = tk.Frame(self.root)
        # Frame for info messages
        self.info_frame = tk.Frame(self.root)

    def __create_entries(self):
        self.size_entry_var = tk.StringVar()
        self.size_entry_var.set(12)
        self.size_entry = tk.Entry(self.size_frame,
                                   textvariable=self.size_entry_var,
                                   bd=5,
                                   width=4)
        self.seed_entry_var = tk.StringVar()
        self.seed_entry_var.set(12345)
        self.seed_entry = tk.Entry(self.seed_frame,
                                   textvariable=self.seed_entry_var,
                                   bd=5,
                                   width=12)
    def __create_labels(self):
        self.size_label = tk.Label(self.size_frame,
                                   text="Size:")
        self.seed_label = tk.Label(self.seed_frame,
                                   text="Seed:")
        self.info_var = tk.StringVar()
        self.info_var.set("Remember to press \"Apply\" to set changes")
        self.info_label = tk.Label(self.info_frame,
                                   textvariable=self.info_var)

    def __create_radio_buttons(self):
        self.radio_var = tk.IntVar()
        self.radio_var.set(1)
        self.color_button1 = tk.Radiobutton(self.color_frame,
                                            text="Color",
                                            variable=self.radio_var,
                                            value=1)
        self.color_button2 = tk.Radiobutton(self.color_frame,
                                            text="Grayscale",
                                            variable=self.radio_var,
                                            value=2)

    def __create_buttons(self):
        self.apply_button = tk.Button(self.bottom_options_frame,
                                      text="Apply",
                                      command=self.__change_list,
                                      bd=5)
        self.generate_button = tk.Button(self.buttons_frame,
                                        text="Start",
                                        command=self.__start_generate,
                                        bg="#55c24e",
                                        activebackground="#2a7d34",
                                        bd=3,
                                        width=7)
        self.save_button = tk.Button(self.buttons_frame,
                                     text="Save",
                                     command=self.__save,
                                     bg="#33a3cc",
                                     activebackground="#28618a",
                                     bd=3,
                                     width=7)

    def __create_canvas(self):
        self.sim_canvas = tk.Canvas(self.canvas_frame,
                                    height=200,
                                    width=200)

    def __pack_all(self):
        # Pack frames
        self.options_frame.pack()
        self.top_options_frame.pack()
        self.bottom_options_frame.pack()
        self.size_frame.pack(side="left")
        self.seed_frame.pack(side="left")
        self.color_frame.pack(side="left")
        self.canvas_frame.pack()
        self.buttons_frame.pack()
        self.info_frame.pack()
        # Pack Labels
        self.size_label.pack(side="left")
        self.seed_label.pack(side="left")
        self.info_label.pack()
        # Pack Entries
        self.size_entry.pack(side="left", pady=6, padx=6)
        self.seed_entry.pack(side="left", pady=6, padx=6)
        # Pack Radio Buttons
        self.color_button1.pack(side="left")
        self.color_button2.pack(side="left")
        # Pack Buttons
        self.apply_button.pack(pady=6, padx=6)
        self.generate_button.pack(side="left", pady=6, padx=6)
        self.save_button.pack(side="left", pady=6, padx=6)
        # Pack canvas
        self.sim_canvas.pack(pady=6, padx=6)

    def __change_list(self):
        if self.size_entry_var.get().isnumeric():
            self.info_var.set("")
            # Color
            if self.radio_var.get() == 1:
                self.__original_list = self.__create_list(
                    int(self.size_entry_var.get()),
                    False,
                    self.seed_entry_var.get())
            # Grayscale
            if self.radio_var.get() == 2:
                self.__original_list = self.__create_list(
                    int(self.size_entry_var.get()),
                    True,
                    self.seed_entry_var.get())
        else:
            self.info_var.set("Size must be a postive integer")

    def __save(self):
        # Redraw the image with PIL to save it
        # This image will not be sized up like the one in the canvas
        img = Image.new(mode="RGB",
                        size=(len(self.__original_list),
                              len(self.__original_list)))
        save = ImageDraw.Draw(img, mode="RGB")
        for i, row in enumerate(self.__original_list):
            for j, cell in enumerate(row):
                save.point((i, j), fill=cell.to_hex_code())
        # Transform image so it appears the same as on the canvas
        img = img.transpose(method=Image.Transpose.ROTATE_270)
        img = img.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
        img.save(fp="generated_noise.png")
        self.info_var.set("Saved image as \"generated_noise.png\".")

    def __start_generate(self):
        displayed_list = self.__original_list.copy()
        # The 200 is the width/height of the square canvas
        pixel_size = 200 // len(displayed_list)
        offset = ((200 - (len(displayed_list) * pixel_size)) // 2) + 1
        self.__clear_canvas()
        for i, row in enumerate(displayed_list):
            for j, element in enumerate(row):
                self.sim_canvas.create_rectangle(pixel_size * j
                                                 + offset,
                                                 pixel_size * i
                                                 + offset,
                                                 pixel_size * j + pixel_size
                                                 + offset,
                                                 pixel_size * i + pixel_size
                                                 + offset,
                                                 fill=element.to_hex_code(),
                                                 width=0)

    def __clear_canvas(self):
        # Fill canvas with the color of the background
        self.sim_canvas.create_rectangle(0, 0,
                                         201, 201,
                                         fill="#F0F0F0",
                                         width=0)
        
    def __create_list(self, list_size, grayscale=False, seed=0):
        '''create a 2D list filled with random numbers'''
        random.seed(a=seed)
        if list_size > 200:
            list_size = 200
            self.info_var.set("Size restricted to 200")
        if list_size < 1:
            list_size = 1
            self.info_var.set("Size restricted to 1")
        random_list = list()
        for i in range(list_size):
            random_list.append([])
            for j in range(list_size):
                cell = Cell()
                cell.randomize(grayscale)
                random_list[i].append(cell)
        return random_list


class Cell():


    def __init__(self, r=0, g=0, b=0):
        # Restrict value to be between 0 and 255
        self.__r = min(max(0, r), 255)
        self.__g = min(max(0, g), 255)
        self.__b = min(max(0, b), 255)

    def randomize(self, grayscale=False):
        if grayscale is True:
            random_number = random.randint(0, 255)
            self.__r = random_number
            self.__g = random_number
            self.__b = random_number
        else:
            self.__r = random.randint(0, 255)
            self.__g = random.randint(0, 255)
            self.__b = random.randint(0, 255)

    def set_r(self, r):
        # Restrict value to be between 0 and 255
        self.__r = min(max(0, r), 255)

    def get_r(self):
        return self.__r

    def set_g(self, g):
        # Restrict value to be between 0 and 255
        self.__g = min(max(0, g), 255)

    def get_g(self):
        return self.__g

    def set_b(self, b):
        # Restrict value to be between 0 and 255
        self.__b = min(max(0, b), 255)

    def get_b(self):
        return self.__b

    def to_hex_code(self):
        # Slice off "0x" part and add in the zero if needed.
        hex_r = hex(self.__r)[2:]
        if len(hex_r) == 1:
            hex_r = "0" + hex_r
        hex_g = hex(self.__g)[2:]
        if len(hex_g) == 1:
            hex_g = "0" + hex_g
        hex_b = hex(self.__b)[2:]
        if len(hex_b) == 1:
            hex_b = "0" + hex_b
        return f"#{hex_r}{hex_g}{hex_b}"

    def __repr__(self):
        return f"R:{self.__r} G:{self.__g} B:{self.__b} | {self.to_hex_code()}"
    
    
if __name__ == "__main__":
    gui = MainGUI()

    
