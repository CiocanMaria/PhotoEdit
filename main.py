import tkinter as tk
from tkinter import ttk
from butoane import EditBar
from imagine import ImageViewer


class Main(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.filename = ""
        self.original_image = None
        self.processed_image = None
        self.is_image_selected = False

        self.filter_frame = None
        self.adjust_frame = None

        self.title("Image Editor")

        self.menu = EditBar(master=self)
        sep_line = ttk.Separator(master=self, orient=tk.HORIZONTAL)
        self.image_viewer = ImageViewer(master=self)

        self.menu.pack(pady=10)
        sep_line.pack(fill=tk.X, padx=20, pady=5)
        self.image_viewer.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)
