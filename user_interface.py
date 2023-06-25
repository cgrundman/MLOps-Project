import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import customtkinter
from tkcalendar import Calendar
import requests
import re
from client import query_and_date # from client.py
import datetime # Time tracking
import math


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1200x1500")
app.configure(bg='#dceaea')
app.configure(highlightthickness=0)

# get the height of app
app.update()
org_height = app.winfo_height()
org_width = app.winfo_width()

def select_time():
    global start_cal, end_cal

    def select_date():
        start_date = start_cal.get_date()
        end_date = end_cal.get_date()
        selected_date.configure(text='Since {} Until {}'.format(start_date, end_date))
        start_cal.destroy()  # Remove calendar after time is selected
        end_cal.destroy()
        select_button.destroy()

    start_cal = Calendar(app, selectmode='day', date_pattern='yyyy-mm-dd')
    start_cal.place(relx=0.265, rely=0.55, anchor=tk.W)
    end_cal = Calendar(app, selectmode='day', date_pattern='yyyy-mm-dd')
    end_cal.place(relx=0.395, rely=0.55, anchor=tk.W)

    select_button = ttk.Button(app, text='Select', command=select_date)
    select_button.place(relx=0.265, rely=0.65, anchor=tk.W)

def analysis_click():
    # Retrieve the query from the input box
    query = input.get('1.0', tk.END).strip() # 1.0 represents 1st character of 1st line
                                             # tk.END ending position of text

    # Reset the analysis button text to "Analysis"
    analysis_button.configure(text='Analysis', command=analysis_click)

    # Print the query and perform analysis
    print(f"Query: {query}")
    #analysis_retrieve(query)

    # Display average score in the gauge
    avg_score = analysis_retrieve(query)
    create_gauge(canvas, avg_score)

    print("Analysis Done!")


def analysis_retrieve(query):
    global start_cal, end_cal
    # Retrieve the query from the input box
    query = input.get('1.0', tk.END).strip()

    # Retrieve the start and end dates from the global variables
    start_date = start_cal.get_date()
    end_date = end_cal.get_date()

    start = datetime.datetime.now()

    # Call the query_and_date function with the query, start_date, and end_date
    query_and_date(query, start_date, end_date)
    top, low, top_contents, low_contents, avg_score = query_and_date(query, start_date, end_date)

    # Create Table widget (Treeview):
    global top_tree, low_tree
    top_tree = ttk.Treeview(app, columns=('Score', 'User', 'Content'), show='headings')
    low_tree = ttk.Treeview(app, columns=('Score', 'User', 'Content'), show='headings')

    # Set style and font for score and content
    style = ttk.Style()
    style.configure('Treeview', font=('Helvetica', 12))
    style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))
    
    # Headings
    top_tree.heading('Score', text='High Score')
    top_tree.heading('User', text='User')
    top_tree.heading('Content', text='Content')
    low_tree.heading('Score', text='Low Score')
    low_tree.heading('User', text='User')
    low_tree.heading('Content', text='Content')

    # Widths
    top_tree.column('Score', width=30)
    top_tree.column('User', width=30)
    top_tree.column('Content', width=500)
    low_tree.column('Score', width=30)
    low_tree.column('User', width=30)
    low_tree.column('Content', width=500)

    # Location
    top_tree.place(relx=0.05, rely=0.65, relwidth=0.4, relheight=0.2)
    low_tree.place(relx=0.55, rely=0.65, relwidth=0.4, relheight=0.2)

    # Hide existing tables before showing the result
    top_tree.delete(*top_tree.get_children()) # get_children: get items
    low_tree.delete(*top_tree.get_children())

    # Display 5 highest and 5 lowest
    for i, score in enumerate(top[:5]):
        score_value = round(float(score['prediction']),3)
        user = score['username']

        # Constraint the length of the content and continue in newline if it exceeds the length
        content = top_contents[i]
        content = remove_info(content)  # Remove links and mentions
        if len(content) > 100:
            content = '\n'.join([content[i:i+100] for i in range(0, len(content), 100)])
        # Insert contents
        top_tree.insert('', 'end', values=(f'{score_value:.3f}', user, content))


    for i, score in enumerate(low[:5]):
        score_value = round(float(score['prediction']),3)
        user = score['username']    
        content = low_contents[i]
        content = remove_info(content)  # Remove links and mentions
        if len(content) > 100:
            content = '\n'.join([content[i:i+100] for i in range(0, len(content), 100)])
        
        low_tree.insert('', 'end', values=(f'{score_value:.3f}', user, content))
    
    end = datetime.datetime.now()
    duration = end - start
    print(f"Duration: {duration.seconds//3600} hour, {(duration.seconds % 3600)//60} minutes,{duration.seconds%60} seconds")
    return avg_score
 
def remove_info(content):
    # Remove links
    content = re.sub(r'http\S+|www\S+', '', content)
    # Remove mentions
    content = re.sub(r'@\w+', '', content)
    return content

def clear_table(table):
    table.delete('1.0', tk.END)

def insert_row(table, score, content):
    table.insert(tk.END, f"Score: {score:.3f}\n")
    table.insert(tk.END, f"Content: {content}\n\n")
    num_lines = content.count('\n') + 1
    table.configure(height=num_lines)

def button2_click():
    print("Button 2 clicked!")

def close():
    app.destroy()


# Create Images:
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

hf_label = tk.Label(app, image=hf_photo, background="#EBEBEB")
hf_label.place(relx=0.1, rely=0.5, anchor=tk.CENTER)
rp_label = tk.Label(app, image=rp_photo, background="#EBEBEB")
rp_label.place(relx=0.9, rely=0.5, anchor=tk.CENTER)

# Create Frame on top (under SENTIMENT Text)
frame = tk.Frame(app, width=org_width, height=344, bg='#ABCDCD')
frame.pack_propagate()
frame.pack(side='top', anchor=tk.CENTER)
bg_label = tk.Label(frame, image=bg_photo, background='#ABCDCD')
bg_label.place(relx=1, rely=0, anchor=tk.NE)

# Create Buttons
button2 = ttk.Button(app, text="Button 2", command=button2_click, style="RoundedButton.TButton")
calendar_button = customtkinter.CTkButton(app, text='Open Calendar', fg_color='#264040', command=select_time)
analysis_button = customtkinter.CTkButton(master=app, text='Analysis', fg_color='#de9304', command=analysis_click)
close_button = customtkinter.CTkButton(master=app, text='Close', fg_color="#b01003", command=close)

calendar_button.place(relx=0.265, rely=0.55, anchor=tk.W)
analysis_button.place(relx=0.68, rely=0.6, anchor=tk.CENTER)
close_button.place(relx=0.9, rely=0.95, anchor=tk.CENTER)

# Create text:
header_label = tk.Label(app, text='SENTIMENT ANALYSIS', font=('Helvetica', 48, 'bold'), 
                        fg='#1f3333', bg='#abcdcd', bd=0)
header_label.place(relx=0.3, rely=0.1, anchor=tk.CENTER)

introduction = """
Explore emotions in text, unlock hidden sentiments, 
dive deep into emotions, embrace contextual understanding,  
customize analysis, visualize with flair, and trust in data privacy.
"""
introduction_label = tk.Label(app, text=introduction, font=('Helvetica', 18),
                              fg='#1f3333', bg='#abcdcd', bd=0, highlightthickness=0)
introduction_label.place(relx=0.3, rely=0.21, anchor=tk.CENTER)

input_text = tk.Label(app, text='What are you searching for?', font=('Helvetica', 15),
                     fg='#1f3333', bg='#ebebeb')
input_text.place(relx=0.265, rely=0.42, anchor=tk.W)

selected_date = tk.Label(app, text='Date Range in yyyy-mm-dd', font=('Helvetica', 15),
                       fg='#1f3333', bg='#ebebeb')
selected_date.place(relx=0.38, rely=0.55, anchor=tk.W)

file_label = tk.Label(app, text='', font=('Helvetica', 15),
                      fg='white', bg='#242424')
file_label.place(relx=0.38, rely=0.49, anchor=tk.W)

input = tk.Text(app, width=60, height=2, font=('Helvetica', 20))
input.place(relx=0.5, rely=0.48, anchor=tk.CENTER)

# Craete advanced filter for languages
languages = ['English', 'German', 'French', 'Spanish', 'Italian', 'Chinese', 'Japanese',
             'Russian', 'Korean', 'Vietnamese']
languages.sort() # sort names in asc

selected_languages = tk.StringVar()
filter_language = ttk.Combobox(app, values=languages, textvariable=selected_languages,
                               font=('Helvetica', 10))
filter_language.place(relx=0.69, rely=0.55, anchor=tk.CENTER)

label_language = ttk.Label(text='Language: ', font=('Helvetica', 15))
label_language.place(relx=0.615, rely=0.55, anchor=tk.CENTER)

def select_language():
    chosen_language = select_language.get() # callback the value of language selected

# Create a gauge with average sentiment score:
def create_gauge(canvas, avg_score):
    #Convert average score to angle (radians)
    angle = math.radians(180 * avg_score)

    # Calculate coordinates of the arrow endpoint
    arrow_length = 100
    '''
    winfo_width()/2: set in center
    arrow_length * math.cos(angle):horizontal offset (x) of the endpoint based on the angle
    arrow_y with -30: distance from the canvas bottom

    arc shape: portion of a circle
    (50,50) top left corner, (250, 250) bottom right corner
    '''
    arrow_x = canvas.winfo_width() / 2 + arrow_length * math.cos(angle)
    arrow_y = canvas.winfo_width() - 25

    # Draw the gauge line with the corresponding color
    canvas.create_arc(50, 50, 250, 250, start=0, extent=60, style='arc', 
                      outline='#59B16E', width=20) # green
    canvas.create_arc(50, 50, 250, 250, start=60, extent=60, style='arc', 
                      outline='#FFD21E', width=20) # yellow
    canvas.create_arc(50, 50, 250, 250, start=120, extent=60, style='arc', 
                      outline='#C74B56', width=20) # red


    # Draw the arrow
    canvas.create_line(canvas.winfo_width() / 2, canvas.winfo_height() / 2, 
                       arrow_x, arrow_y, width=2, arrow=tk.FIRST) # show arrow towards avg

    # Display the average score
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50, 
                       text=f"Average Score: {avg_score:.2f}")

canvas = tk.Canvas(app, width=300, height=150, bg='#EBEBEB', 
                   highlightthickness=0) # thickness=0 transparent
canvas.place(relx=0.5, rely=0.9, anchor=tk.CENTER)




app.mainloop()
