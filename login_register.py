import tkinter as tk
from tkinter import messagebox
from utils import login_user, register_user
from userdashboard import show_user_dashboard
from hotel_owner import show_owner_panel
from admin_panel import show_admin_panel

def show_login_register():
    root = tk.Tk()
    root.title("Login / Register")
    root.geometry("450x500")
    root.configure(bg="#f7f9fc")

    # Header
    header = tk.Frame(root, bg="#3e64ff", height=70)
    header.pack(fill="x")

    tk.Label(header, text="🔐 Login / Register", font=("Helvetica", 18, "bold"),
             fg="white", bg="#3e64ff").pack(pady=20)

    # Main Frame
    frame = tk.Frame(root, bg="#f7f9fc")
    frame.pack(pady=30)

    def create_labeled_entry(row, label_text, entry_var=None, show=None):
        tk.Label(frame, text=label_text, font=("Arial", 11), bg="#f7f9fc", fg="#333").grid(row=row, column=0, pady=8, sticky='e')
        entry = tk.Entry(frame, font=("Arial", 11), width=25, textvariable=entry_var, show=show)
        entry.grid(row=row, column=1, pady=8, padx=5)
        return entry

    name_entry = create_labeled_entry(0, "Name")
    email_entry = create_labeled_entry(1, "Email")
    password_entry = create_labeled_entry(2, "Password", show="*")

    tk.Label(frame, text="Role", font=("Arial", 11), bg="#f7f9fc", fg="#333").grid(row=3, column=0, pady=8, sticky='e')
    role_var = tk.StringVar(value="user")
    tk.OptionMenu(frame, role_var, "user", "owner", "admin").grid(row=3, column=1, pady=8, sticky='w')

    # Action Buttons
    button_frame = tk.Frame(root, bg="#f7f9fc")
    button_frame.pack(pady=20)

    def on_register():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        role = role_var.get()
        register_user(name, email, password, role)

    def on_login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        user = login_user(email, password)
        if user:
            messagebox.showinfo("Login Success", f"Welcome {user[1]}!")
            root.destroy()
            if user[4] == "user":
                show_user_dashboard(user)
            elif user[4] == "owner":
                show_owner_panel(user)
            elif user[4] == "admin":
                show_admin_panel(user)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    tk.Button(button_frame, text="Register", command=on_register, font=("Arial", 11),
              bg="#28a745", fg="black", width=15).pack(side="left", padx=10)

    tk.Button(button_frame, text="Login", command=on_login, font=("Arial", 11),
              bg="#007bff", fg="black", width=15).pack(side="right", padx=10)

    # Footer
    tk.Label(root, text="🔒 Secure access to hotel booking system", font=("Arial", 9),
             bg="#f7f9fc", fg="#666").pack(side="bottom", pady=15)

    root.mainloop()

# Run standalone
if __name__ == "__main__":
    show_login_register()
