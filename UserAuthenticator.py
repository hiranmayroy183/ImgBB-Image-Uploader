import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import random
import string
import sqlite3

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

class UserAuthenticatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Authenticator")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.username_label = tk.Label(self.root, text="Enter Username:")
        self.username_label.pack(pady=10)
        
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=10)
        
        self.password_label = tk.Label(self.root, text="Enter Password:")
        self.password_label.pack(pady=10)
        
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=10)
        
        self.auth_button = tk.Button(self.root, text="Generate Token", command=self.authenticate)
        self.auth_button.pack(pady=10)
        
        self.token_label = tk.Label(self.root, text="")
        self.token_label.pack(pady=10)
        
        self.copy_button = tk.Button(self.root, text="Copy Token", command=self.copy_token)
        self.copy_button.pack(pady=10)
        
        self.generated_token = ""

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            password_hash = hash_password(password)
            conn = sqlite3.connect('images.db')
            c = conn.cursor()
            c.execute("SELECT id, token_count FROM users WHERE username=? AND password=?", (username, password_hash))
            user = c.fetchone()
            if user:
                user_id, token_count = user
                if token_count < 3:
                    self.generated_token = generate_token()
                    self.token_label.config(text=f"Generated Token: {self.generated_token}")
                    c.execute("UPDATE users SET token=?, token_count=token_count+1 WHERE id=?", (self.generated_token, user_id))
                    conn.commit()
                else:
                    messagebox.showerror("Error", "Token generation limit reached.")
            else:
                messagebox.showerror("Error", "Invalid username or password.")
            conn.close()
        else:
            messagebox.showerror("Error", "Please enter username and password.")

    def copy_token(self):
        if self.generated_token:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.generated_token)
            messagebox.showinfo("Info", "Token copied to clipboard.")
        else:
            messagebox.showerror("Error", "No token to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserAuthenticatorApp(root)
    root.mainloop()
