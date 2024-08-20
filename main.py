import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3

# Initialize database connection
conn = sqlite3.connect('reminders.db')
c = conn.cursor()

# Create table for reminders if it doesn't already exist
c.execute('''
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    reminder TEXT
)
''')
conn.commit()

# Function to add a reminder
def add_reminder():
    selected_date = cal.get_date()
    reminder_text = reminder_entry.get()
    
    if reminder_text:
        c.execute('INSERT INTO reminders (date, reminder) VALUES (?, ?)', (selected_date, reminder_text))
        conn.commit()
        messagebox.showinfo("Reminder Added", f"Reminder added for {selected_date}: {reminder_text}")
        reminder_entry.delete(0, tk.END)
        display_reminders(selected_date)
    else:
        messagebox.showwarning("Input Error", "Please enter a reminder")

# Function to display reminders for a selected date
def display_reminders(date):
    reminders_list.delete(0, tk.END)
    c.execute('SELECT reminder FROM reminders WHERE date = ?', (date,))
    reminders = c.fetchall()
    for reminder in reminders:
        reminders_list.insert(tk.END, reminder[0])

# Function to delete a reminder
def delete_reminder():
    selected_date = cal.get_date()
    selected_reminder = reminders_list.get(tk.ACTIVE)
    
    if selected_reminder:
        c.execute('DELETE FROM reminders WHERE date = ? AND reminder = ?', (selected_date, selected_reminder))
        conn.commit()
        messagebox.showinfo("Reminder Deleted", f"Deleted reminder for {selected_date}: {selected_reminder}")
        display_reminders(selected_date)
    else:
        messagebox.showwarning("Selection Error", "Please select a reminder to delete")

# Function to update a reminder
def update_reminder():
    selected_date = cal.get_date()
    selected_reminder = reminders_list.get(tk.ACTIVE)
    new_reminder_text = reminder_entry.get()
    
    if selected_reminder and new_reminder_text:
        c.execute('UPDATE reminders SET reminder = ? WHERE date = ? AND reminder = ?', 
                  (new_reminder_text, selected_date, selected_reminder))
        conn.commit()
        messagebox.showinfo("Reminder Updated", f"Updated reminder for {selected_date}: {new_reminder_text}")
        reminder_entry.delete(0, tk.END)
        display_reminders(selected_date)
    else:
        messagebox.showwarning("Input Error", "Please select a reminder and enter the new text")

# Function to handle date change in the calendar
def on_date_change(event):
    selected_date = cal.get_date()
    display_reminders(selected_date)

# Create main application window
root = tk.Tk()
root.title("Calendar and Reminder App")

# Create a Calendar widget
cal = Calendar(root, selectmode='day', year=2024, month=8, day=10)
cal.pack(pady=20)

# Entry box for adding/updating a reminder
reminder_entry = tk.Entry(root, width=50)
reminder_entry.pack(pady=10)

# Button to add the reminder
add_reminder_btn = tk.Button(root, text="Add Reminder", command=add_reminder)
add_reminder_btn.pack(pady=5)

# Button to update the reminder
update_reminder_btn = tk.Button(root, text="Update Reminder", command=update_reminder)
update_reminder_btn.pack(pady=5)

# Button to delete the reminder
delete_reminder_btn = tk.Button(root, text="Delete Reminder", command=delete_reminder)
delete_reminder_btn.pack(pady=5)

# Listbox to display reminders for the selected date
reminders_list = tk.Listbox(root, width=50, height=10)
reminders_list.pack(pady=10)

# Bind the calendar to display reminders when the date changes
cal.bind("<<CalendarSelected>>", on_date_change)

# Run the application
root.mainloop()

# Close the database connection when the application is closed
conn.close()
