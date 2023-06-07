import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image
import customtkinter
import os
import random
import PyPDF2
# import docx

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1200x1000")
app.configure(bg='#dceaea')
app.configure(highlightthickness=0)

def browse_click():
    # The buttion changes to 'Loading...' when clicking the button
    browse_button.configure(text='Loading...')
    app.update()
    
    # Give the path, filedialog from tkinter
    file = askopenfile(mode='rb', title='Choose a file', 
                       filetype=[('pdf file', '*.pdf')]) 
    
    if file:
        # Read the file
        pdf = PyPDF2.PdfReader(file)
        page = pdf.pages[0]
        content = page.extract_text()

        # If finishing upload, change the name of browser_button
        browse_button.configure(text='Done', fg_color='#538888')

        # Display the file name
        file_label.configure(text=file.name) 

    else:
        # No file is selected, revert the Browser
        browse_button.configure(text='Browse')

    print('Browse clicked')


def analysis_click():
    print("Analysis clicked!")


def button2_click():
    print("Button 2 clicked!")


def close():
    app.destroy()

# get the height of app
app.update()
org_height = app.winfo_height()
org_width = app.winfo_width()

# Load the PNG image
height = 200
width = 200
hf_image = Image.open("static/images/hugging-face.png")
hf_image = hf_image.resize((width, height))
hf_photo = ImageTk.PhotoImage(hf_image)
rp_image = Image.open("static/images/rasp-pi.png")
rp_image = rp_image.resize((width, height))
rp_photo = ImageTk.PhotoImage(rp_image)
bg_image = Image.open("static/images/emoji1.png")
bg_photo = ImageTk.PhotoImage(bg_image)

# Create three rounded buttons
button2 = ttk.Button(app, text="Button 2", command=button2_click, style="RoundedButton.TButton")

# Add buttons to the window with spacing
browse_button = customtkinter.CTkButton(app, text='Browse', fg_color='#264040', command=browse_click)
analysis_button = customtkinter.CTkButton(master=app, text="Analysis", fg_color='#de9304', command=analysis_click)
close_button = customtkinter.CTkButton(master=app, text="Close", fg_color="#b01003", command=close)

# Create a box on the left corner
frame = tk.Frame(app, width=org_width, height=344, bg='#ABCDCD')
frame.pack_propagate(0) # not resize the frame to fix the content
frame.pack(side='top', anchor=tk.CENTER)

# Create a label to display texts
header_label = tk.Label(app, text = 'SENTIMENT ANALYSIS', font=('Helvetica', 48, 'bold'), 
                        fg='#1f3333', bg='#abcdcd', bd=0) # insert text on the box
header_label.place(relx=0.3, rely=0.1, anchor=tk.CENTER)

introduction = """
Explore emotions in text, unlock hidden sentiments, 
dive deep into emotions, embrace contextual understanding,  
customize analysis, visualize with flair, and trust in data privacy.
"""
introduction_label = tk.Label(app, text=introduction, font=('Helvetica', 18),
                              fg='#1f3333', bg='#abcdcd', bd=0, highlightthickness=0) # introduction, set borderwidth bd=0 
introduction_label.place(relx=0.3, rely=0.21, anchor=tk.CENTER)

input_text = tk.Label(app, text='Please type your ideas or upload a file:', font=('Helvetica', 15),
                     fg='#1f3333', bg='#ebebeb') # instruct using text box or browse
input_text.place(relx=0.265, rely=0.42, anchor=tk.W)

instruction = tk.Label(app, text='File format: .pdf', font=('Helvetica', 15),
                       fg='#1f3333', bg='#ebebeb')
instruction.place(relx=0.39, rely=0.59, anchor=tk.W)

file_label = tk.Label(app, text='', font=('Helvetica', 15),
                      fg='white', bg='#242424') # show the file name
file_label.place(relx=0.38, rely=0.49, anchor=tk.W)

# Create text widgets
input = tk.Text(app, width=60, height=3, font=('Helvetica', 20)) # entry the text info
input.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


# Create a label to display the image
hf_label = tk.Label(app, image=hf_photo, background="#EBEBEB")
hf_label.place(relx=0.1, rely=0.5, anchor=tk.CENTER)
rp_label = tk.Label(app, image=rp_photo, background="#EBEBEB")
rp_label.place(relx=0.9, rely=0.5, anchor=tk.CENTER)
bg_label = tk.Label(frame, image=bg_photo, background='#ABCDCD')
bg_label.place(relx=1, rely=0, anchor=tk.NE)

browse_button.place(relx=0.265, rely=0.59, anchor=tk.W)
analysis_button.place(relx=0.68, rely=0.59, anchor=tk.CENTER)
close_button.place(relx=0.9, rely=0.9, anchor=tk.CENTER)

# Create sentimental states - progress bars for each state
states = ['happy', 'positive', 'neutral','negative','angry']
colors = {'happy':'#12831f', 'positive':'#1e8aec','neutral':'#ffad1e',
          'negative': '#d76213','angry': '#c31c2e'}

labels = {}
progress_bar = {}
y = 0.65 # coordinates to move the bars and states
offset = 0.05 # coordinates to move the bars and states

for state in states:

    label = tk.Label(app, text=f'{state}: 0%', fg=colors[state], font=('Helvetica', 20, 'bold'),
                     bg='#EBEBEB')
    label.place(relx=0.55, rely=y)

    canvas = tk.Canvas(app, width= 300, height= 30) # create canvas to fill in the colors
    canvas.place(relx=0.35, rely=y)

    progress = canvas.create_rectangle(0,0,0,30,fill=colors[state])

    labels[state] = label
    progress_bar[state] = (canvas,progress)

    y += offset


def update_bars():
    for state in states:
        new_value = random.randint(0,100) # stimulate values

        canvas, progress = progress_bar[state]
        canvas.coords(progress, (0,0,3*new_value,30)) # width=2*percentages

        labels[state]['text'] = f'{state}: {new_value}%' # update label
    
    app.after(500, update_bars) # update every 500ms

# Start updates
update_bars()


# Start the Tkinter event loop
app.mainloop()
