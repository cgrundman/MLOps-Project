import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import customtkinter
from tkcalendar import Calendar
import requests
from client import query_and_date
import re

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1200x1200")
app.configure(bg='#dceaea')
app.configure(highlightthickness=0)

# get the height of app
app.update()
org_height = app.winfo_height()
org_width = app.winfo_width()

start_cal = None
end_cal = None

def select_time():
    global start_cal, end_cal, start_date, end_date

    def select_date():
        start_date = start_cal.get_date()
        end_date = end_cal.get_date()
        selected_date.configure(text='Since {} Until {}'.format(start_date, end_date))
        start_cal.destroy() # Remove calendar after time is selected
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
    query = input.get('1.0', tk.END).strip()

    # Reset the analysis button text to "Analysis"
    analysis_button.configure(text='Analysis', command=analysis_click)

    # Print the query and perform analysis
    print(f"Query: {query}")
    analysis_retrieve(query)
    print("Analysis Done!")

def analysis_retrieve(query):
    # Retrieve the query from the input box
    query = input.get('1.0', tk.END).strip()

    # Retrieve the start and end dates from the global variables
    start_date = start_cal.get_date()
    end_date = end_cal.get_date()

    # Call the query_and_date function with the query, start_date, and end_date
    query_and_date(query, start_date, end_date)
    top3, low3, top3_contents, low3_contents = query_and_date(query, start_date, end_date)

    # Create Table widget (Treeview):
    global top3_tree, low3_tree
    top3_tree = ttk.Treeview(app, columns=('Score', 'Content'), show='headings')
    low3_tree = ttk.Treeview(app, columns=('Score', 'Content'), show='headings')

    # Set style and font for score and content
    style = ttk.Style()
    style.configure('Treeview', font=('Helvetica', 12))
    style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))
    
    # Headings
    top3_tree.heading('Score', text='Highest Score')
    top3_tree.heading('Content', text='Content')
    low3_tree.heading('Score', text='Lowest Score')
    low3_tree.heading('Content', text='Content')

    # Widths
    top3_tree.column('Score', width=30)
    top3_tree.column('Content', width=500)
    low3_tree.column('Score', width=30)
    low3_tree.column('Content', width=500)

    # Location
    top3_tree.place(relx=0.05, rely=0.62, relwidth=0.4, relheight=0.2)
    low3_tree.place(relx=0.55, rely=0.62, relwidth=0.4, relheight=0.2)

    # Clear existing tables:
    top3_tree.delete(*top3_tree.get_children())
    low3_tree.delete(*top3_tree.get_children())

    # Display 5 highest and 5 lowest
    for i, score in enumerate(top3[:3]):
        score_value = round(float(score['prediction']),3)

        # Constraint the length of the content and continue in newline if it exceeds the length
        content = top3_contents[i]
        content = remove_info(content)  # Remove links and mentions
        if len(content) > 100:
            content = '\n'.join([content[i:i+100] for i in range(0, len(content), 100)])
        # Insert contents
        top3_tree.insert('', 'end', values=(f'{score_value:.3f}', content))


    for i, score in enumerate(low3[:3]):
        score_value = round(float(score['prediction']),3)        
        content = low3_contents[i]
        content = remove_info(content)  # Remove links and mentions
        if len(content) > 100:
            content = '\n'.join([content[i:i+100] for i in range(0, len(content), 100)])
        
        low3_tree.insert('', 'end', values=(f'{score_value:.3f}', content))

    # Create scrollbars for the Content column
    top3_content_scrollbar = ttk.Scrollbar(app, orient='horizontal', command=top3_tree.xview)
    low3_content_scrollbar = ttk.Scrollbar(app, orient='horizontal', command=low3_tree.xview)

    # Configure scrollbars
    top3_tree.configure(xscrollcommand=top3_content_scrollbar.set)
    low3_tree.configure(xscrollcommand=low3_content_scrollbar.set)

    # Set the scrollbar width and height
    top3_content_scrollbar.place(in_=top3_tree, relx=0, rely=1, relwidth=1, anchor=tk.SW)
    low3_content_scrollbar.place(in_=low3_tree, relx=0, rely=1, relwidth=1, anchor=tk.SW) 

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
frame.pack_propagate(0)
frame.pack(side='top', anchor=tk.CENTER)
bg_label = tk.Label(frame, image=bg_photo, background='#ABCDCD')
bg_label.place(relx=1, rely=0, anchor=tk.NE)

# Create Buttons
button2 = ttk.Button(app, text="Button 2", command=button2_click, style="RoundedButton.TButton")
calendar_button = customtkinter.CTkButton(app, text='Open Calendar', fg_color='#264040', command=select_time)
analysis_button = customtkinter.CTkButton(master=app, text='Analysis', fg_color='#de9304', command=analysis_click)
close_button = customtkinter.CTkButton(master=app, text='Close', fg_color="#b01003", command=close)

calendar_button.place(relx=0.265, rely=0.55, anchor=tk.W)
analysis_button.place(relx=0.68, rely=0.55, anchor=tk.CENTER)
close_button.place(relx=0.9, rely=0.9, anchor=tk.CENTER)

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

selected_date = tk.Label(app, text='Date Range: ', font=('Helvetica', 15),
                       fg='#1f3333', bg='#ebebeb')
selected_date.place(relx=0.38, rely=0.55, anchor=tk.W)

file_label = tk.Label(app, text='', font=('Helvetica', 15),
                      fg='white', bg='#242424')
file_label.place(relx=0.38, rely=0.49, anchor=tk.W)

input = tk.Text(app, width=60, height=2, font=('Helvetica', 20))
input.place(relx=0.5, rely=0.48, anchor=tk.CENTER)

app.mainloop()
