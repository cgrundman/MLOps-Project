import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1200x600")


def button_click():
    print("Button 1 clicked!")


def button2_click():
    print("Button 2 clicked!")


def close():
    app.destroy()


# Load the PNG image
height = 200
width = 200
hf_image = Image.open("static/images/hugging-face.png")
hf_image = hf_image.resize((width, height))
hf_photo = ImageTk.PhotoImage(hf_image)
rp_image = Image.open("static/images/rasp-pi.png")
rp_image = rp_image.resize((width, height))
rp_photo = ImageTk.PhotoImage(rp_image)

# Create three rounded buttons
button2 = ttk.Button(app, text="Button 2", command=button2_click, style="RoundedButton.TButton")

# Add buttons to the window with spacing
button1 = customtkinter.CTkButton(master=app, text="Button 1", command=button_click)
close_button = customtkinter.CTkButton(master=app, text="Close", fg_color="red", command=close)

# Create a label to display the image
hf_label = tk.Label(app, image=hf_photo, background="#242424")
hf_label.place(relx=0.25, rely=0.5, anchor=tk.CENTER)
rp_label = tk.Label(app, image=rp_photo, background="#242424")
rp_label.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

button1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
close_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Start the Tkinter event loop
app.mainloop()
