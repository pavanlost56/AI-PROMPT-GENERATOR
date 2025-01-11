import tkinter as tk
from tkinter import messagebox
from textblob import TextBlob
import qrcode
from PIL import Image, ImageTk

# Function to autocorrect and generate AI prompt
def generate_prompt():
    description = description_input.get("1.0", tk.END).strip()
    if not description:
        messagebox.showerror("Input Error", "Please enter a description.")
        return

    # Autocorrect the description
    try:
        corrected_description = str(TextBlob(description).correct())
    except Exception as e:
        messagebox.showerror("Autocorrect Error", f"Could not autocorrect text: {e}")
        corrected_description = description  # Use original description if autocorrection fails

    # Generate the AI prompt
    prompt = f"Write a detailed and creative response for: {corrected_description}"
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

# Function to generate and display a QR code
def generate_qr():
    description = description_input.get("1.0", tk.END).strip()
    if not description:
        messagebox.showerror("Input Error", "Please enter a description.")
        return

    # Generate a smaller, square QR Code
    qr = qrcode.QRCode(
        version=1,  # Version 1 creates a 21x21 matrix
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,  # Smaller box size for compact QR codes
        border=2,    # Smaller border for compact design
    )
    qr.add_data(description)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR Code to a file
    qr_image.save("qr_code.png")
    
    # Display QR Code in the UI
    qr_image_tk = ImageTk.PhotoImage(Image.open("qr_code.png"))
    qr_label.config(image=qr_image_tk)
    qr_label.image = qr_image_tk
    qr_label.pack(pady=10)


# Initialize the main application window
app = tk.Tk()
app.title("AI Prompt Generator with Autocorrect and QR Code")
app.geometry("600x700")
app.resizable(False, False)

# UI Elements
title_label = tk.Label(app, text="AI Prompt Generator with QR Code", font=("Helvetica", 16, "bold"))
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

qr_button = tk.Button(app, text="Generate QR Code", command=generate_qr, font=("Helvetica", 12, "bold"), bg="green", fg="white")
qr_button.pack(pady=10)

qr_label = tk.Label(app, bg="white")
qr_label.pack()

# Run the application
app.mainloop()
