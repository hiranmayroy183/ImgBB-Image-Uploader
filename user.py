import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import requests
import sqlite3
import hashlib
import pyperclip
import logging

IMGBB_API_KEY = 'YOUR_IMGBB_API_KEY'
MAX_FREE_UPLOADS = 100

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_db():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, token_count INTEGER DEFAULT 0, image_count INTEGER DEFAULT 0, is_premium INTEGER DEFAULT 0, token TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY, url TEXT, delete_url TEXT, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

class UserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User - Image Uploader")
        self.user_id = None
        self.is_premium = False
        self.image_count = 0

        self.create_widgets()
        
    def create_widgets(self):
        self.tab_control = tk.Frame(self.root)
        self.tab_control.pack(expand=1, fill="both")
        
        self.register_button = tk.Button(self.tab_control, text="Register", command=self.register_user)
        self.register_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.login_button = tk.Button(self.tab_control, text="Login", command=self.login_user)
        self.login_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.activate_button = tk.Button(self.tab_control, text="Activate", command=self.activate_user)
        self.activate_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.select_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        self.select_button.pack(pady=10)
        
        self.upload_button = tk.Button(self.root, text="Upload Images", command=self.upload_images)
        self.upload_button.pack(pady=10)
        
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)
        
        self.links_text = scrolledtext.ScrolledText(self.root, width=50, height=10)
        self.links_text.pack(pady=10)
        
        self.copy_button = tk.Button(self.root, text="Copy Links", command=self.copy_links)
        self.copy_button.pack(pady=10)
        
        self.selected_files = []

    def register_user(self):
        username = simpledialog.askstring("Register", "Enter your username:")
        password = simpledialog.askstring("Register", "Enter your password:", show='*')
        if username and password:
            password_hash = hash_password(password)
            conn = sqlite3.connect('images.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password, token_count, image_count, is_premium) VALUES (?, ?, 0, 0, 0)", (username, password_hash))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful.")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")
            finally:
                conn.close()

    def login_user(self):
        username = simpledialog.askstring("Login", "Enter your username:")
        password = simpledialog.askstring("Login", "Enter your password:", show='*')
        if username and password:
            password_hash = hash_password(password)
            conn = sqlite3.connect('images.db')
            c = conn.cursor()
            c.execute("SELECT id, is_premium, image_count FROM users WHERE username=? AND password=?", (username, password_hash))
            user = c.fetchone()
            if user:
                self.user_id, self.is_premium, self.image_count = user
                messagebox.showinfo("Success", "Login successful.")
            else:
                messagebox.showerror("Error", "Invalid username or password.")
            conn.close()

    def activate_user(self):
        if self.user_id is None:
            messagebox.showerror("Error", "You must be logged in to activate.")
            return
        token = simpledialog.askstring("Activate", "Enter your activation token:")
        if token:
            conn = sqlite3.connect('images.db')
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE token=? AND id=?", (token, self.user_id))
            user = c.fetchone()
            if user:
                c.execute("UPDATE users SET is_premium=1, token=NULL WHERE id=?", (self.user_id,))
                conn.commit()
                self.is_premium = True
                messagebox.showinfo("Success", "You are now a premium user.")
            else:
                messagebox.showerror("Error", "Invalid token.")
            conn.close()

    def select_images(self):
        if self.user_id is None:
            messagebox.showerror("Error", "You must be logged in to select images.")
            return

        max_files = 10 if self.is_premium else 5
        self.selected_files = filedialog.askopenfilenames(
            title=f"Select up to {max_files} images", 
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if len(self.selected_files) > max_files:
            messagebox.showerror("Error", f"You can select up to {max_files} images only")
            self.selected_files = []
        else:
            self.status_label.config(text=f"{len(self.selected_files)} images selected")
    
    def upload_images(self):
        if self.user_id is None:
            messagebox.showerror("Error", "You must be logged in to upload images.")
            return

        if not self.selected_files:
            messagebox.showerror("Error", "No images selected")
            return
        
        if not self.is_premium and self.image_count + len(self.selected_files) > MAX_FREE_UPLOADS:
            messagebox.showerror("Error", "Upload limit reached for free users.")
            return

        uploaded_links = []
        conn = sqlite3.connect('images.db')
        c = conn.cursor()
        
        try:
            for image in self.selected_files:
                with open(image, 'rb') as img:
                    response = requests.post(
                        "https://api.imgbb.com/1/upload",
                        data={"key": IMGBB_API_KEY},
                        files={"image": img})
                    
                    if response.status_code == 200:
                        data = response.json()['data']
                        link = data['url']
                        delete_url = data['delete_url']
                        uploaded_links.append(link)
                        c.execute("INSERT INTO images (url, delete_url, user_id) VALUES (?, ?, ?)", 
                                  (link, delete_url, self.user_id))
                        self.image_count += 1
                    else:
                        self.status_label.config(text=f"Failed to upload: {image}")
                        break
            
            c.execute("UPDATE users SET image_count=? WHERE id=?", (self.image_count, self.user_id))
            conn.commit()

            if uploaded_links:
                self.links_text.delete(1.0, tk.END)
                for link in uploaded_links:
                    self.links_text.insert(tk.END, link + '\n')
                self.status_label.config(text="Upload complete")
            else:
                self.status_label.config(text="No images uploaded")
            
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()
    
    def copy_links(self):
        try:
            links = self.links_text.get(1.0, tk.END).strip()
            pyperclip.copy(links)
            messagebox.showinfo("Info", "Links copied to clipboard")
        except Exception as e:
            logging.error(f"An error occurred while copying links: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    logging.basicConfig(filename='user_app.log', level=logging.ERROR)
    create_db()
    root = tk.Tk()
    app = UserApp(root)
    root.mainloop()
