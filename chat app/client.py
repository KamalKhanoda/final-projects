import socket
import threading
import json
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
import os

HOST = "127.0.0.1"
PORT = 4444

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("ChatiPY")
        self.master.geometry("800x650")
        self.master.resizable(False, False)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")
            self.master.destroy()
            return

        self.username = None
        self.profile_pic = None
        self.online_users = []
        self.user_photos = {}

        self.setup_login_ui()

        self.listener_thread = threading.Thread(target=self.listen_server, daemon=True)
        self.listener_thread.start()

    def setup_login_ui(self):
        self.frame = tk.Frame(self.master, bg="#f7f7f7")
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=350, height=380)

        tk.Label(self.frame, text="Login/Signup", font=("Segoe UI", 18, "bold"), bg="#f7f7f7").pack(pady=(10, 15))

        tk.Label(self.frame, text="Username:", font=("Segoe UI", 12), bg="#f7f7f7").pack(anchor="w", padx=30)
        self.entry_username = tk.Entry(self.frame, font=("Segoe UI", 12))
        self.entry_username.pack(padx=30, fill="x")

        tk.Label(self.frame, text="Password:", font=("Segoe UI", 12), bg="#f7f7f7").pack(anchor="w", padx=30, pady=(10,0))
        self.entry_password = tk.Entry(self.frame, show='*', font=("Segoe UI", 12))
        self.entry_password.pack(padx=30, fill="x")

        tk.Label(self.frame, text="Profile Photo (optional):", font=("Segoe UI", 12), bg="#f7f7f7").pack(anchor="w", padx=30, pady=(10,0))
        self.entry_photo = tk.Entry(self.frame, font=("Segoe UI", 12))
        self.entry_photo.pack(padx=30, fill="x")

        self.style = {
            "font": ("Segoe UI", 11, "bold"),
            "bd": 1,
            "relief": "groove",
            "highlightthickness": 0,
            "activebackground": "#d0d0d0",
            "cursor": "hand2"
        }

        browse_btn_frame = tk.Frame(self.frame, bg="#f7f7f7")
        browse_btn_frame.pack(padx=30, pady=(4, 10), anchor="w")
        tk.Button(
            browse_btn_frame, text="Browse", command=self.browse_photo, bg="#e0e0e0", fg="#222",
            width=10, **self.style,
        ).pack(side="left")

        btn_frame = tk.Frame(self.frame, bg="#f7f7f7")
        btn_frame.pack(pady=8)
        tk.Button(
            btn_frame, text="Login", command=self.on_login, bg="#4CAF50", fg="white",
            width=12, **self.style
        ).pack(side="left", padx=10, pady=5)
        tk.Button(
            btn_frame, text="Signup", command=self.on_signup, bg="#2196F3", fg="white",
            width=12, **self.style
        ).pack(side="left", padx=10)

    def browse_photo(self):
        filename = filedialog.askopenfilename(
            title="Select Profile Photo",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if filename:
            self.entry_photo.delete(0, tk.END)
            self.entry_photo.insert(0, filename)

    def on_login(self):
        uname = self.entry_username.get().strip()
        pwd = self.entry_password.get().strip()
        if not uname or not pwd:
            messagebox.showerror("Error", "Username and password required.")
            return
        req = {"action": "login", "username": uname, "password": pwd}
        self.sock.sendall(json.dumps(req).encode())

    def on_signup(self):
        uname = self.entry_username.get().strip()
        pwd = self.entry_password.get().strip()
        pic = self.entry_photo.get().strip()
        if not uname or not pwd:
            messagebox.showerror("Error", "Username and password required.")
            return
        pic_filename = os.path.basename(pic) if pic else ""
        req = {"action": "signup", "username": uname, "password": pwd, "profile_pic": pic_filename}
        self.sock.sendall(json.dumps(req).encode())
        
    def setup_main_ui(self):
        self.clear_window()
        sidebar_width = int(0.3 * 800)
        chat_width = 800 - sidebar_width
        chat_height = 650

        # Sidebar
        self.sidebar = tk.Frame(self.master, bg="#B9B5B5")
        self.sidebar.place(x=0, y=0, width=sidebar_width, height=chat_height)
        self.users_canvas = tk.Canvas(self.sidebar, bg="#B9B5B5", highlightthickness=0)
        self.users_canvas.pack(fill=tk.BOTH, expand=True)
        self.users_frame = tk.Frame(self.users_canvas, bg="#F7F7F7", width=int(sidebar_width))
        self.users_canvas.create_window((0, 0), window=self.users_frame, anchor="nw", width=int(sidebar_width))
        self.users_frame.bind("<Configure>", lambda e: self.users_canvas.configure(scrollregion=self.users_canvas.bbox("all")))
        self.users_scroll = tk.Scrollbar(self.sidebar, orient="vertical", command=self.users_canvas.yview)
        self.users_canvas.configure(yscrollcommand=self.users_scroll.set)
        self.users_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Chat area with a visible border and background
        self.chat_frame = tk.Frame(self.master, bg="#f7f7f7", bd=1, relief="ridge")
        self.chat_frame.place(x=sidebar_width + 2, y=2, width=chat_width - 10, height=chat_height - 5)

        # Message display area with a border
        self.messages_area = tk.Text(
            self.chat_frame, bg="#f7f7f7", fg="#222", font=("Segoe UI", 11),
            bd=0, relief="groove", wrap=tk.WORD, state=tk.DISABLED
        )
        self.messages_area.place(x=8, y=8, width=chat_width-30, height=chat_height-110)

        # Configure tags for alignment
        self.messages_area.tag_configure("left", justify="left", lmargin1=10, lmargin2=10)
        self.messages_area.tag_configure("right", justify="right", rmargin=10)

        # Message input area
        self.input_canvas = tk.Canvas(
            self.chat_frame, width=chat_width-50, height=50, bg="#f7f7f7", highlightthickness=0
        )
        self.input_canvas.place(x=8, y=chat_height-86)

        # Rounded rectangle for entry
        self.round_rect(self.input_canvas, 0, 0, chat_width-130, 40, radius=18, fill="#fff", outline="#bbb")
        self.entry_msg = tk.Entry(
            self.chat_frame, font=("Segoe UI", 11), bd=0, bg="#fff", fg="#222"
        )
        self.entry_msg.place(x=30, y=chat_height-80, width=chat_width-170, height=30)
        self.entry_msg.bind("<Return>", lambda e: self.send_message())

        # Send button with a visible border and color
        self.send_btn_canvas = tk.Canvas(
            self.chat_frame, width=60, height=40, bg="#e9e9e9", highlightthickness=0
        )
        self.send_btn_canvas.place(x=chat_width-95, y=chat_height-87)
        self.round_rect(self.send_btn_canvas, 0, 0, 60, 40, radius=24, fill="#4CAF50", outline="#388E3C")
        self.send_btn = tk.Button(
            self.chat_frame, text="Send", font=("Segoe UI", 10, "bold"), fg="#fff", bg="#4CAF50",
            bd=0, relief="ridge", activebackground="#388E3C", cursor="hand2", command=self.send_message
        )
        self.send_btn.place(x=chat_width-85, y=chat_height-83, width=40, height=28)

        # Recipients selection
        self.selected_users = []
        self.select_all_var = tk.BooleanVar(value=False)
        self.select_all_cb = tk.Checkbutton(
            self.sidebar, text="Select All", variable=self.select_all_var, bg="#464141", fg="white",
            command=self.toggle_select_all
        )
        self.select_all_cb.pack(anchor="w", padx=10, pady=(10, 0))

        self.refresh_users()

    def round_rect(self, canvas, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def listen_server(self):
        while True:
            try:
                data = self.sock.recv(4096).decode()
                if not data:
                    break
                try:
                    msg = json.loads(data)
                except Exception:
                    continue
                self.handle_server_message(msg)
            except Exception:
                break

    def handle_server_message(self, msg):
        action = msg.get("action")
        if action is None and "status" in msg:
            # Login/Signup response
            if msg["status"] == "ok":
                if "profile_pic" in msg:
                    self.profile_pic = msg["profile_pic"]
                self.username = self.entry_username.get().strip()
                self.setup_main_ui()
                self.request_users()
                self.append_message("System", "Login/Signup successful.")
            else:
                messagebox.showerror("Error", msg.get("message", "Unknown error"))
        elif action == "user_list":
            self.online_users = msg["users"]
            self.refresh_users()
        elif action == "user_online":
            self.request_users()
            self.append_message("System", f"{msg['username']} is online.")
        elif action == "user_offline":
            self.request_users()
            self.append_message("System", f"{msg['username']} went offline.")
        elif action == "message":
            sender = msg.get("from", "Unknown")
            text = msg.get("message", "")
            self.append_message(sender, text)
        else:
            pass  # Ignore unknown actions

    def append_message(self, sender, text):
        self.messages_area.config(state=tk.NORMAL)
        if sender == "You":
            self.messages_area.insert(tk.END, f"{sender}: {text}\n", "right")
        else:
            self.messages_area.insert(tk.END, f"{sender}: {text}\n", "left")
        self.messages_area.see(tk.END)
        self.messages_area.config(state=tk.DISABLED)

    def request_users(self):
        req = {"action": "get_users"}
        self.sock.sendall(json.dumps(req).encode())

    def refresh_users(self):
        for widget in self.users_frame.winfo_children():
            widget.destroy()
        self.user_photos.clear()
        self.user_vars = {}  # <-- Add this line to keep track of user variables
        for user in self.online_users:
            uname = user["username"]
            pic = user.get("profile_pic", "")
            frame = tk.Frame(self.users_frame, bg="#F7F7F7")
            frame.pack(fill=tk.X, padx=10, pady=5)
            # Load profile pic if exists
            img = None
            if pic and os.path.exists(pic):
                try:
                    pil_img = Image.open(pic).resize((36, 36))
                    img = ImageTk.PhotoImage(pil_img)
                except Exception:
                    img = None
            if not img:
                pil_img = Image.new("RGB", (36, 36), color="#888")
                img = ImageTk.PhotoImage(pil_img)
            self.user_photos[uname] = img
            lbl_img = tk.Label(frame, image=img, bg="#F7F7F7")
            lbl_img.pack(side=tk.LEFT, padx=(0, 10))
            var = tk.BooleanVar()
            self.user_vars[uname] = var  # <-- Store the variable
            cb = tk.Checkbutton(
                frame, text=uname, variable=var,
                bg="#F7F7F7", fg="black", selectcolor="#F7F7F7",
                command=self.update_selected_users
            )
            cb.pack(side=tk.LEFT)
        self.update_selected_users()

    def update_selected_users(self):
        self.selected_users = [uname for uname, var in self.user_vars.items() if var.get()]
        self.select_all_var.set(len(self.selected_users) == len(self.online_users))

    def toggle_select_all(self):
        if self.select_all_var.get():
            for var in self.user_vars.values():
                var.set(True)
        else:
            for var in self.user_vars.values():
                var.set(False)
        self.update_selected_users()

    def send_message(self):
        msg = self.entry_msg.get().strip()
        if not msg:
            return
        # Use the selected_users list directly
        recipients = self.selected_users if not self.select_all_var.get() and self.selected_users else "all"
        req = {
            "action": "send_message",
            "message": msg,
            "recipients": recipients
        }
        self.sock.sendall(json.dumps(req).encode())
        self.append_message("You", msg)
        self.entry_msg.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()