from main import run_program
import tkinter as tk
from tkinter import simpledialog, messagebox
import csv
import os
import threading    


# Declare global variables
global root, visualizer_listbox, listbox, tickers

def update_visualization():
    global visualizer_listbox
    try:
        with open('results.csv', mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        visualizer_listbox.delete(0, tk.END)
        for row in data:
            visualizer_listbox.insert(tk.END, row)
    except FileNotFoundError:
        visualizer_listbox.delete(0, tk.END)

def check_for_updates():
    global root
    update_visualization()
    root.after(5000, check_for_updates)  # Check every 5 seconds

def load_tickers():
    with open('stocks.csv', mode='r') as file:
        reader = csv.reader(file)
        return list(reader)

def save_tickers(tickers):
    with open('stocks.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(tickers)

def add_ticker():
    global tickers
    ticker = simpledialog.askstring("Input", "Enter ticker symbol:")
    if ticker:
        tickers.append([ticker])
        update_listbox()
        save_tickers(tickers)

def remove_ticker():
    global tickers
    selected = listbox.curselection()
    if selected:
        tickers.pop(selected[0])
        update_listbox()
        save_tickers(tickers)
    else:
        messagebox.showwarning("Warning", "No ticker selected.")

def update_listbox():
    global listbox, tickers
    listbox.delete(0, tk.END)
    for ticker in tickers:
        listbox.insert(tk.END, ticker[0])
        
def start_background_task():
    thread = threading.Thread(target=run_program)
    thread.daemon = True
    thread.start()

def check_api_key():
    global login_window
    api_key = simpledialog.askstring("API Key", "Enter your OpenAI API key:")
    if api_key:
        with open('api_key.txt', 'w') as file:
            file.write(api_key)
        login_window.destroy()
        main_app()

def change_api_key():
    global visualizer_listbox
    new_api_key = simpledialog.askstring("API Key", "Enter new OpenAI API key:")
    if new_api_key:
        with open('api_key.txt', 'w') as file:
            file.write(new_api_key)
        messagebox.showinfo("Info", "API key updated.")

def main_app():
    global listbox, add_button, remove_button, change_key_button, visualizer_listbox, root

    # Create GUI
    root = tk.Tk()
    root.title("Stock Ticker Manager")
    root.configure(bg="#2E343A")
    root.geometry("800x600")

    # Configure grid layout
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=4)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(0, weight=4)
    root.rowconfigure(1, weight=1)

    # Listboxes
    listbox = tk.Listbox(root, font=("Arial", 10), bg="#317968", fg="#FFFFFF", justify='center', highlightbackground="#071828", highlightcolor="#071828", highlightthickness=2)
    listbox.grid(row=0, column=0, sticky="nsew", padx=(25, 10), pady=25)

    visualizer_listbox = tk.Listbox(root, font=("Arial", 10), bg="#081C31", fg="#FFFFFF", highlightbackground="#071828", highlightcolor="#071828", highlightthickness=2)
    visualizer_listbox.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=(10, 25), pady=25)

  
    # Buttons
    add_button = tk.Button(root, text="Add Ticker", command=add_ticker, font=("Arial", 12), bg="#29CC29", height=3)
    add_button.grid(row=1, column=0, padx=25, pady=5, sticky="ew")

    remove_button = tk.Button(root, text="Remove Ticker", command=remove_ticker, font=("Arial", 12), bg="#CC2929", height=3)
    remove_button.grid(row=1, column=2, padx=25, pady=5, sticky="ew")

    change_key_button = tk.Button(root, text="Change API Key", command=change_api_key, font=("Arial", 12), bg="#317968", height=3)
    change_key_button.grid(row=1, column=1, padx=25, pady=5, sticky="ew")

    # Update listbox and start background task
    update_listbox()
    start_background_task()
    check_for_updates()
    root.mainloop()

# Load tickers after API key is entered
try:
    with open('stocks.csv', mode='r') as file:
        tickers = list(csv.reader(file))
except FileNotFoundError:
    tickers = []

if os.path.exists('api_key.txt') and os.path.getsize('api_key.txt') > 0:
    # API key exists, load the app
    main_app()
else:
    # Create login window
    login_window = tk.Tk()
    login_window.title("API Key Required")

    login_message = tk.Label(login_window, text="You need to enter your OpenAI API key to use this application.")
    login_message.pack(padx=10, pady=10)

    login_button = tk.Button(login_window, text="Enter API Key", command=check_api_key)
    login_button.pack(padx=10, pady=25)

    login_window.mainloop()
