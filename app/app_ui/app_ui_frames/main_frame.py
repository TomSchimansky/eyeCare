import tkinter
import customtkinter
from PIL import Image, ImageTk

from app.settings import Settings


class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, app=None, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, master, *args, **kwargs)

        self.app_pointer = app
        self.color_manager = master.color_manager

        self.open_eye_image = ImageTk.PhotoImage(Image.open(Settings.MAIN_PATH +
                                                            "/assets/images/eye_open.png").resize((120, 75)))
        self.closed_eye_image = ImageTk.PhotoImage(Image.open(Settings.MAIN_PATH +
                                                              "/assets/images/eye_closed.png").resize((120, 75)))

        self.analyzing_started = False

        self.time_bar = customtkinter.CTkProgressBar(master=self,
                                                     width=350,
                                                     height=20,
                                                     border_width=1)
        self.time_bar.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
        self.time_bar.set(0)

        self.pause_button = customtkinter.CTkButton(master=self,
                                                    text="Start",
                                                    command=self.pause_button_click)
        self.pause_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.data_frame = customtkinter.CTkFrame(master=self,
                                                 width=350,
                                                 height=50,
                                                 fg_color=customtkinter.Color.FRAME)
        self.data_frame.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.average_time_text = customtkinter.CTkLabel(master=self.data_frame,
                                                        fg_color=customtkinter.Color.FRAME_2,
                                                        width=165,
                                                        text="Durchschn. Zeit: - sek")
        self.average_time_text.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.eye_canvas = customtkinter.CTkFrame(master=self,
                                                 width=350,
                                                 height=100)

        self.eye_canvas.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.open_eye_canvas_item_1 = self.eye_canvas.canvas.create_image(95, 50,
                                                                          image=self.closed_eye_image,
                                                                          anchor=tkinter.CENTER)
        self.open_eye_canvas_item_2 = self.eye_canvas.canvas.create_image(350-95, 50,
                                                                          image=self.closed_eye_image,
                                                                          anchor=tkinter.CENTER)

    def set_eyes_open(self):
        self.eye_canvas.canvas.itemconfig(self.open_eye_canvas_item_1, image=self.open_eye_image)
        self.eye_canvas.canvas.itemconfig(self.open_eye_canvas_item_2, image=self.open_eye_image)

    def set_eyes_closed(self):
        self.eye_canvas.canvas.itemconfig(self.open_eye_canvas_item_1, image=self.closed_eye_image)
        self.eye_canvas.canvas.itemconfig(self.open_eye_canvas_item_2, image=self.closed_eye_image)

    def pause_button_click(self):
        if not self.analyzing_started:
            self.analyzing_started = True
            self.pause_button.set_text("Stop")
            self.app_pointer.start_analyzing()

        else:
            self.analyzing_started = False
            self.pause_button.set_text("Start")
            self.app_pointer.stop_analyzing()

    def update_info_data(self, average_time, data_2=0):
        self.average_time_text.set_text(f"Durchschn. Zeit: {average_time:.2f} sek")
        #self.data_2_text.set_text(f"Info Angabe: {data_2:.2f} sek")
