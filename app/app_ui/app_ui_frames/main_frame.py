import customtkinter
from PIL import Image, ImageTk

from app.settings import Settings


class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, app=None, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, master, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_rowconfigure(3, weight=1)

        self.app_pointer = app

        self.open_eye_image = customtkinter.CTkImage(Image.open(Settings.MAIN_PATH +
                                                     "/assets/images/eye_open.png"), size=(120, 75))
        self.closed_eye_image = customtkinter.CTkImage(Image.open(Settings.MAIN_PATH +
                                                       "/assets/images/eye_closed.png"), size=(120, 75))

        self.analyzing_started = False

        self.eye_canvas = customtkinter.CTkFrame(master=self, fg_color=("gray95", "gray26"))
        self.eye_canvas.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.eye_canvas.grid_columnconfigure((0, 1), weight=1)
        self.eye_image_label = customtkinter.CTkLabel(master=self.eye_canvas, image=self.closed_eye_image, text="")
        self.eye_image_label.grid(row=0, column=0, padx=20, pady=20)
        self.eye_image_label_2 = customtkinter.CTkLabel(master=self.eye_canvas, image=self.closed_eye_image, text="")
        self.eye_image_label_2.grid(row=0, column=1, padx=20, pady=20)

        self.data_frame = customtkinter.CTkFrame(master=self, height=50, fg_color=("gray95", "gray26"))
        self.data_frame.grid(row=1, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")

        self.average_time_text = customtkinter.CTkLabel(master=self.data_frame, width=350,
                                                        text="Average blink interval: - sec")
        self.average_time_text.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)

        self.time_bar = customtkinter.CTkProgressBar(master=self, height=8, border_width=0)
        self.time_bar.grid(row=2, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.time_bar.set(0)

        self.pause_button = customtkinter.CTkButton(master=self,
                                                    text="Start",
                                                    command=self.pause_button_click)
        self.pause_button.grid(row=3, column=0, padx=(10, 10), pady=(10, 20), sticky="s")

    def set_eyes_open(self):
        self.eye_image_label.configure(image=self.open_eye_image)
        self.eye_image_label_2.configure(image=self.open_eye_image)

    def set_eyes_closed(self):
        self.eye_image_label.configure(image=self.closed_eye_image)
        self.eye_image_label_2.configure(image=self.closed_eye_image)

    def pause_button_click(self):
        if not self.analyzing_started:
            self.analyzing_started = True
            self.pause_button.configure(text="Stop")
            self.app_pointer.start_analyzing()

        else:
            self.analyzing_started = False
            self.pause_button.configure(text="Start")
            self.app_pointer.stop_analyzing()

    def update_info_data(self, average_time):
        self.average_time_text.configure(text=f"Average blink interval: {average_time:.2f} sec")
