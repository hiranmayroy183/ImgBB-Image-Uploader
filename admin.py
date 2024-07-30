import tkinter as tk
from tkinter import messagebox
import sqlite3
import logging

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin - Manage Images")
        
        self.create_widgets()
        self.load_images()
        self.load_users()
        
    def create_widgets(self):
        self.image_list = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=50, height=20)
        self.image_list.pack(pady=10)
        
        self.delete_button = tk.Button(self.root, text="Delete Selected", command=self.delete_images)
        self.delete_button.pack(pady=10)
        
        self.user_list = tk.Listbox(self.root, selectmode=tk.SINGLE, width=50, height=10)
        self.user_list.pack(pady=10)
        
        self.delete_user_button = tk.Button(self.root, text="Delete User", command=self.delete_user)
        self.delete_user_button.pack(pady=10)
    
    def load_images(self):
        try:
            self.image_list.delete(0, tk.END)
            conn = sqlite3.connect('images.db')
            c = conn.cursor()
            c.execute("SELECT images.id, images.url, users.username FROM images JOIN users ON images.user_id = users.id")
            images = c.fetchall()
            conn.close()
            
            for img in images:
                self.image_list.insert(tk.END, f"{img[0]} - {img[1]} - {img[2]}")
        except Exception as e:
            logging.error(f"An error occurred while loading images: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def load_users(self):
        try:
            self.user_list.delete(0, tk.END)
            conn = sqlite3.connect('images.db')
            c = conn.cursor()
            c.execute("SELECT id, username, is_premium, image_count FROM users")
            users = c.fetchall()
            conn.close()
            
            for user in users:
                status = "Premium" if user[2] else "Free"
                self.user_list.insert(tk.END, f"{user[0]} - {user[1]} - {status} - {user[3]} images")
        except Exception as e:
            logging.error(f"An error occurred while loading users: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def delete_images(self):
        selected_indices = self.image_list.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "No images selected")
            return
        
        conn = sqlite3.connect('images.db')
        c = conn.cursor()
        
        try:
            for index in selected_indices[::-1]:
                item = self.image_list.get(index)
                img_id = int(item.split(' - ')[0])
                c.execute("DELETE FROM images WHERE id = ?", (img_id,))
                self.image_list.delete(index)
            
            conn.commit()
            self.load_images()
        except Exception as e:
            logging.error(f"An error occurred while deleting images: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()
    
    def delete_user(self):
        selected_index = self.user_list.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No user selected")
            return
        
        conn = sqlite3.connect('images.db')
        c = conn.cursor()
        
        try:
            item = self.user_list.get(selected_index)
            user_id = int(item.split(' - ')[0])
            c.execute("DELETE FROM users WHERE id = ?", (user_id,))
            c.execute("DELETE FROM images WHERE user_id = ?", (user_id,))
            
            conn.commit()
            self.load_users()
            self.load_images()
        except Exception as e:
            logging.error(f"An error occurred while deleting user: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    logging.basicConfig(filename='admin_app.log', level=logging.ERROR)
    root = tk.Tk()
    app = AdminApp(root)
    root.mainloop()
