from tkinter import Frame, Button, LEFT
from tkinter import filedialog
from filtre import FilterFrame
import cv2


class EditBar(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.upload_button = Button(self, text="Încarcă")
        self.save_button = Button(self, text="Salvare")
        self.save_as_button = Button(self, text="Salvare ca")
        self.filter_button = Button(self, text="Filtre")
        self.clear_button = Button(self, text="Ștergere")

        self.upload_button.bind("<ButtonRelease>", self.upload_button_released)
        self.save_button.bind("<ButtonRelease>", self.save_button_released)
        self.save_as_button.bind("<ButtonRelease>", self.save_as_button_released)
        self.filter_button.bind("<ButtonRelease>", self.filter_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)

        self.upload_button.pack(side=LEFT)
        self.save_button.pack(side=LEFT)
        self.save_as_button.pack(side=LEFT)
        self.filter_button.pack(side=LEFT)
        self.clear_button.pack()

    def upload_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.upload_button:

            filename = filedialog.askopenfilename()
            image = cv2.imread(filename)

            if image is not None:
                self.master.filename = filename
                self.master.original_image = image.copy()
                self.master.processed_image = image.copy()
                self.master.image_viewer.show_image()
                self.master.is_image_selected = True

    def save_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_button:
            save_image = self.master.processed_image
            image_filename = self.master.filename
            cv2.imwrite(image_filename, save_image)

    def save_as_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_button:
            original_file_type = self.master.filename.split('.')[-1]
            filename = filedialog.asksaveasfilename()
            filename = filename + "." + original_file_type

            save_image = self.master.processed_image
            cv2.imwrite(filename, save_image)

            self.master.filename = filename

    def filter_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.filter_button:
            self.master.filter_frame = FilterFrame(master=self.master)
            self.master.filter_frame.grab_set()

    def clear_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.clear_button:
            self.master.processed_image = self.master.original_image.copy()
            self.master.image_viewer.show_image()
