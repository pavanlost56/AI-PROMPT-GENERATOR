import tkinter as tk
from tkinter import messagebox

# Function to generate AI prompt based on user input
def generate_prompt():
    description = description_input.get("1.0", tk.END).strip()
    if not description:
        messagebox.showerror("Input Error", "Please enter a description.")
        return
    
    # Generate the AI prompt
    prompt = f"Write a detailed and creative response for: {description}"
    output_label.config(text=prompt)
    copy_button.config(state=tk.NORMAL)  # Enable the copy button

# Function to copy the generated prompt to clipboard
def copy_to_clipboard():
    prompt = output_label.cget("text")
    if prompt:
        app.clipboard_clear()
        app.clipboard_append(prompt)
        app.update()  # Ensures the clipboard gets updated
        messagebox.showinfo("Copied", "Prompt copied to clipboard!")

# Initialize the main application window
app = tk.Tk()
app.title("AI Prompt Generator")
app.geometry("500x450")
app.resizable(False, False)

# UI Elements
title_label = tk.Label(app, text="AI Prompt Generator", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

description_label = tk.Label(app, text="Enter your description below:", font=("Helvetica", 12))
description_label.pack()

description_input = tk.Text(app, height=8, width=50, font=("Helvetica", 10))
description_input.pack(pady=10)

generate_button = tk.Button(app, text="Generate Prompt", command=generate_prompt, font=("Helvetica", 12, "bold"), bg="blue", fg="white")
generate_button.pack(pady=10)

output_label = tk.Label(app, text="", font=("Helvetica", 10), wraplength=480, justify="left", bg="lightgrey", relief="solid", padx=5, pady=5)
output_label.pack(pady=20)

copy_button = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard, font=("Helvetica", 12), state=tk.DISABLED, bg="black", fg="white")
copy_button.pack(pady=10)

# Run the application
app.mainloop()
