import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from plyer import notification
import pygame
import threading
import time

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder Application")
        
        self.reminders = []
        
        tk.Label(root, text="Reminder Title:").pack(pady=5)
        self.title_entry = tk.Entry(root)
        self.title_entry.pack(pady=5)
        
        tk.Label(root, text="Reminder Time (HH:MM):").pack(pady=5)
        self.time_entry = tk.Entry(root)
        self.time_entry.pack(pady=5)
        
        tk.Button(root, text="Add Reminder", command=self.add_reminder).pack(pady=10)
        
        self.reminder_list = tk.Listbox(root, width=50, height=10)
        self.reminder_list.pack(pady=20)
        
        tk.Button(root, text="Delete Selected Reminder", command=self.delete_reminder).pack(pady=5)
        
        pygame.mixer.init()
        
        # Start the reminder checking thread
        threading.Thread(target=self.check_reminders, daemon=True).start()
        
    def add_reminder(self):
        title = self.title_entry.get()
        time_str = self.time_entry.get()
        
        try:
            reminder_time = datetime.strptime(time_str, "%H:%M").time()
            self.reminders.append((title, reminder_time))
            self.update_reminder_list()
            
            self.title_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Time Format", "Please enter the time in HH:MM format.")
    
    def delete_reminder(self):
        selected_index = self.reminder_list.curselection()
        if selected_index:
            self.reminders.pop(selected_index[0])
            self.update_reminder_list()
    
    def update_reminder_list(self):
        self.reminder_list.delete(0, tk.END)
        for title, time in self.reminders:
            self.reminder_list.insert(tk.END, f"{title} at {time.strftime('%H:%M')}")
    
    def check_reminders(self):
        while True:
            now = datetime.now().time()
            for reminder in self.reminders:
                if now >= reminder[1] and (datetime.combine(datetime.today(), now) - datetime.combine(datetime.today(), reminder[1])).seconds < 60:
                    self.show_notification(reminder[0])
                    self.reminders.remove(reminder)
                    self.update_reminder_list()
                    self.play_sound()
            time.sleep(2)  
    
    def play_sound(self):
        pygame.mixer.music.load('alarm.mp3.wav')
        pygame.mixer.music.play()
    
    def show_notification(self, title):
        notification.notify(
            title="Reminder",
            message=title,
            timeout=10
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
