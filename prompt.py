import tkinter as tk
from tkinter import messagebox
from threading import Thread
import ollama


class PromptChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Prompt Generator with Chatbot Interface")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1E1E2E")

        # Set up UI
        self.create_menu()
        self.create_main_ui()

    def create_menu(self):
        """Create a menu bar."""
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

    def create_main_ui(self):
        """Create UI for prompt generator and chatbot."""
        main_frame = tk.Frame(self.root, bg="#1E1E2E")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Prompt and Chatbot Panels
        self.create_prompt_ui(main_frame)
        self.create_chatbot_ui(main_frame)

    def create_prompt_ui(self, parent):
        prompt_frame = tk.Frame(parent, bg="#1E1E2E")
        prompt_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        title_label = tk.Label(prompt_frame, text="PromptCraft Generator", font=("Helvetica", 16, "bold"), fg="#CDD6F4", bg="#1E1E2E")
        title_label.pack(pady=10)

        description_label = tk.Label(prompt_frame, text="Enter your description below:", font=("Helvetica", 12), fg="#A6ADC8", bg="#1E1E2E")
        description_label.pack()

        self.description_input = tk.Text(prompt_frame, height=8, width=50, font=("Helvetica", 10), bg="#313244", fg="#CDD6F4")
        self.description_input.pack(pady=10)

        generate_button = tk.Button(prompt_frame, text="Generate Prompt", command=self.generate_prompt, font=("Helvetica", 16, "bold"), bg="#89B4FA", fg="#1E1E2E", width=15, height=2)
        generate_button.pack(pady=10)

        self.loading_label = tk.Label(prompt_frame, text="", font=("Helvetica", 10, "italic"), fg="#F38BA8", bg="#1E1E2E")
        self.loading_label.pack_forget()

        result_frame = tk.Frame(prompt_frame, bg="#1E1E2E")
        result_frame.pack(pady=20)

        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(result_frame, height=10, width=50, font=("Helvetica", 10), wrap=tk.WORD, bg="#313244", fg="#CDD6F4", yscrollcommand=scrollbar.set)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.output_text.yview)
        self.output_text.config(state=tk.DISABLED)

        self.copy_button = tk.Button(prompt_frame, text="Copy to Clipboard", command=self.copy_to_clipboard, font=("Helvetica", 12), state=tk.DISABLED, bg="#F5C2E7", fg="#1E1E2E")
        self.copy_button.pack(pady=10)

    def create_chatbot_ui(self, parent):
        chatbot_frame = tk.Frame(parent, bg="#45475A")
        chatbot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

        chatbot_label = tk.Label(chatbot_frame, text="Chatbot Interface", font=("Helvetica", 14, "bold"), fg="#CDD6F4", bg="#45475A")
        chatbot_label.pack(pady=5)

        result_frame = tk.Frame(chatbot_frame, bg="#45475A")
        result_frame.pack(pady=10, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_history = tk.Text(result_frame, height=20, width=50, font=("Helvetica", 10), wrap=tk.WORD, bg="#313244", fg="#CDD6F4", yscrollcommand=scrollbar.set)
        self.chat_history.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.chat_history.yview)
        self.chat_history.config(state=tk.DISABLED)

        chat_entry_frame = tk.Frame(chatbot_frame, bg="#45475A")
        chat_entry_frame.pack(fill=tk.X)

        # Medium-sized input box
        self.chat_entry = tk.Text(chat_entry_frame, height=2, width=40, font=("Helvetica", 12), bg="#313244", fg="#CDD6F4")
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        chat_send_button = tk.Button(chat_entry_frame, text="Send", command=self.send_chat, bg="#A6E3A1", fg="#1E1E2E", width=10)
        chat_send_button.pack(side=tk.RIGHT, padx=5)

    def generate_prompt(self):
        """Handle prompt generation."""
        description = self.description_input.get("1.0", tk.END).strip()
        if not description:
            messagebox.showerror("Input Error", "Please enter a description.")
            return

        self.animate_loading(True)

        def process():
            try:
                print(f"Input to LLaMA: {description}")
                response = ollama.chat("llama3", messages=[{"role": "user", "content": description}])
                prompt = response.get("message", {}).get("content", "No valid response from LLaMA")

                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", prompt)
                self.output_text.config(state=tk.DISABLED)
                self.copy_button.config(state=tk.NORMAL)
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Generation Error", f"Error generating prompt: {e}")
            finally:
                self.animate_loading(False)

        Thread(target=process).start()

    def copy_to_clipboard(self):
        """Copy generated prompt to clipboard."""
        prompt = self.output_text.get("1.0", tk.END).strip()
        if prompt:
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt)
            self.root.update()
            messagebox.showinfo("Copied", "Prompt copied to clipboard!")

    def animate_loading(self, state):
        """Animate loading indicator."""
        if state:
            self.loading_label.pack()
            self.loading_label.config(text="Generating...")
        else:
            self.loading_label.pack_forget()

    def send_chat(self):
        """Handle chatbot message sending."""
        user_message = self.chat_entry.get("1.0", tk.END).strip()
        if user_message:
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.insert(tk.END, "You: " + user_message + "\n")
            self.chat_history.config(state=tk.DISABLED)
            self.chat_entry.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = PromptChatApp(root)
    root.mainloop()
