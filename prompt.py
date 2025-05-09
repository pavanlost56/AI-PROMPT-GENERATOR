import tkinter as tk
from tkinter import messagebox
from threading import Thread
import customtkinter as ctk
import requests
import subprocess
import time
import psutil
import sys


class OllamaPromptGenerator:
    def __init__(self, model_url="http://localhost:11434/api/generate"):
        self.model_url = model_url
        self.ollama_process = None
        self.start_ollama_server()
        self.ensure_model_loaded()

    def start_ollama_server(self):
        if not self.is_ollama_running():
            try:
                print("Starting Ollama server...")
                self.ollama_process = subprocess.Popen(
                    [r"C:\\Users\\pavan\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "serve"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                for attempt in range(20):
                    if self.is_ollama_running() and self.is_ollama_ready():
                        print(f"Ollama is ready after {attempt + 1} attempts.")
                        return
                    time.sleep(1)
                messagebox.showerror("Error", "Ollama did not start in time.")
            except FileNotFoundError:
                messagebox.showerror("Error", "Ollama executable not found. Ensure it's installed and added to PATH.")

    def is_ollama_running(self):
        for process in psutil.process_iter(['name']):
            if "ollama" in process.info['name'].lower():
                return True
        return False

    def is_ollama_ready(self):
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def ensure_model_loaded(self):
        if not self.is_ollama_ready():
            print("Starting Ollama service...")
            return False

        model_name = "tinyllama"
        try:
            # Check if model exists
            response = requests.get("http://localhost:11434/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                if not any(model.get("name") == model_name for model in models):
                    print(f"Model '{model_name}' not found. Pulling the model...")
                    # Pull the model
                    pull_response = requests.post(
                        "http://localhost:11434/api/pull",
                        json={"name": model_name},
                        timeout=600  # Longer timeout for model pulling
                    )
                    if pull_response.status_code == 200:
                        print(f"Successfully pulled {model_name} model")
                        return True
                    else:
                        print(f"Failed to pull {model_name} model")
                        return False
                return True
        except requests.RequestException as e:
            print(f"Error checking/pulling model: {e}")
            return False

    def generate_prompt(self, description):
        # Ensure model is ready before generating
        if not self.ensure_model_loaded():
            return "Error: Please ensure Ollama is running and tinyllama model is available."

        structured_prompt = f"""
        ### Task:
        Generate a **concise and thought-provoking writing prompt** based on the following description. 

        ### Description:
        {description}

        ### Instructions:
        - **Only output a single, creative writing prompt.**
        - Do **NOT** generate exercises or story outlines.
        - The prompt should be **under 50 words** and **spark imagination and storytelling.**
        - **Strictly avoid adding additional guidance or tips.**
        """

        payload = {
            "model": "tinyllama",
            "prompt": structured_prompt,
            "stream": False,
            "options": {
                "num_predict": 100,
                "temperature": 0.5,
                "top_k": 30,
                "top_p": 0.8,
            }
        }

        try:
            print("Generating prompt with tinyllama...")
            response = requests.post(
                self.model_url, 
                json=payload, 
                timeout=(30, 120)  # (connection timeout, read timeout)
            )
            response.raise_for_status()
            result = response.json().get("response", "No response generated.")
            print("Prompt generated successfully")
            return result
        except requests.Timeout:
            return "Error: Request timed out. The model is taking too long to respond."
        except requests.RequestException as e:
            return f"Error: {e}"

    def stop_ollama_server(self):
        if self.ollama_process:
            self.ollama_process.terminate()


class PromptChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PromptCraft")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.prompt_generator = OllamaPromptGenerator()
        self.create_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        frame = ctk.CTkFrame(self.root, corner_radius=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="PromptCraft", font=("Arial", 24, "bold")).pack(pady=10)

        self.description_input = ctk.CTkTextbox(frame, height=100, width=600, corner_radius=15, fg_color="#2A2D3E", text_color="white")
        self.description_input.pack(pady=10)

        self.generate_button = ctk.CTkButton(
            frame, text="Generate Prompt", command=self.generate_prompt, corner_radius=25, height=40, width=200, fg_color="#007BFF"
        )
        self.generate_button.pack(pady=10)

        self.output_text = ctk.CTkTextbox(frame, height=200, width=600, state=tk.DISABLED, corner_radius=15, fg_color="#1E1E2E", text_color="white")
        self.output_text.pack(pady=10)

        self.copy_button = ctk.CTkButton(
            frame, text="Copy to Clipboard", command=self.copy_to_clipboard, state=tk.DISABLED, corner_radius=25, height=40, width=200, fg_color="#28A745"
        )
        self.copy_button.pack(pady=5)

        self.status_label = ctk.CTkLabel(frame, text="Ready", font=("Arial", 10))
        self.status_label.pack(pady=5)

    def generate_prompt(self):
        description = self.description_input.get("1.0", tk.END).strip()
        if not description:
            messagebox.showerror("Input Error", "Please enter a description.")
            return

        self.status_label.configure(text="Generating prompt...")
        self.generate_button.configure(state=tk.DISABLED)
        self.root.update()

        def run_generation():
            prompt = self.prompt_generator.generate_prompt(description)
            self.root.after(0, lambda: self.display_prompt(prompt))

        Thread(target=run_generation).start()

    def display_prompt(self, prompt):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", prompt)
        self.output_text.configure(state=tk.DISABLED)
        self.copy_button.configure(state=tk.NORMAL)
        self.generate_button.configure(state=tk.NORMAL)
        self.status_label.configure(text="Ready")

    def copy_to_clipboard(self):
        prompt = self.output_text.get("1.0", tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(prompt)
        self.root.update()
        messagebox.showinfo("Success", "Prompt copied to clipboard!")

    def on_close(self):
        self.prompt_generator.stop_ollama_server()
        self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = PromptChatApp(root)
    root.mainloop()
