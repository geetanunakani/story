import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import re

# ---------------- Blacklist (Worst Passwords) ---------------- #
blacklist = [
    "password", "123456", "qwerty", "admin", "letmein",
    "welcome", "abc123", "iloveyou"
]

# ---------------- Dictionary Words Avoid ---------------- #
dictionary_words = [
    "name", "user", "hello", "login", "india", "school"
]

# ---------------- Strength Meter Function ---------------- #
def check_strength(pw):
    score = 0
    if len(pw) >= 8: score += 1
    if re.search(r"[A-Z]", pw): score += 1
    if re.search(r"[a-z]", pw): score += 1
    if re.search(r"[0-9]", pw): score += 1
    if re.search(r"[@#$%&!]", pw): score += 1
    if len(set(pw)) > len(pw) / 2: score += 1

    if score <= 2:
        return "Weak", "red"
    elif score <= 4:
        return "Medium", "orange"
    else:
        return "Strong", "green"

# ---------------- Password Generator ---------------- #
def generate_password():
    length = random.randint(10, 16)

    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("@#$%&!")
    remaining = ''.join(random.choices(
        string.ascii_letters + string.digits + "@#$%&!",
        k=length-4))

    pw_list = list(upper + lower + digit + special + remaining)
    random.shuffle(pw_list)
    password = "".join(pw_list)

    entry_pass.delete(0, tk.END)
    entry_pass.insert(0, password)
    entry_confirm.delete(0, tk.END)
    entry_confirm.insert(0, password)

    strength, color = check_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)

    result_label.config(text="Password Generated Successfully!", fg="cyan")
    progress['value'] = 0

# ---------------- Validation Function ---------------- #
def validate_password():
    pw = entry_pass.get()
    cpw = entry_confirm.get()

    # Empty Check
    if pw == "" or cpw == "":
        result_label.config(text="Fields cannot be empty!", fg="red")
        progress['value'] = 10
        return

    # Length Check
    if not (8 <= len(pw) <= 16):
        result_label.config(text="Password must be 8–16 characters!", fg="red")
        progress['value'] = 20
        return

    # Uppercase
    if not re.search(r"[A-Z]", pw):
        result_label.config(text="Missing uppercase letter!", fg="red")
        progress['value'] = 30
        return

    # Lowercase
    if not re.search(r"[a-z]", pw):
        result_label.config(text="Missing lowercase letter!", fg="red")
        progress['value'] = 40
        return

    # Digit
    if not re.search(r"[0-9]", pw):
        result_label.config(text="Missing digit!", fg="red")
        progress['value'] = 50
        return

    # Special Character
    if not re.search(r"[@#$%&!]", pw):
        result_label.config(text="Missing special character!", fg="red")
        progress['value'] = 60
        return

    # Only Allowed Characters
    if not re.fullmatch(r"[A-Za-z0-9@#$%&!]+", pw):
        result_label.config(text="Invalid characters used!", fg="red")
        progress['value'] = 70
        return

    # Confirm Password
    if pw != cpw:
        result_label.config(text="Passwords do not match!", fg="red")
        progress['value'] = 80
        return

    # Blacklist check
    if pw.lower() in blacklist:
        result_label.config(text="Password is too common!", fg="red")
        progress['value'] = 85
        return

    # Dictionary word check
    for word in dictionary_words:
        if word in pw.lower():
            result_label.config(text="Password contains dictionary word!", fg="red")
            progress['value'] = 88
            return

    # Repeated chars (e.g., aaaaa)
    if re.search(r"(.)\1{3,}", pw):
        result_label.config(text="Too many repeated characters!", fg="red")
        progress['value'] = 90
        return

    # Sequential pattern (1234, abcd)
    if re.search(r"(0123|1234|2345|abcd|bcde)", pw.lower()):
        result_label.config(text="Password contains sequential pattern!", fg="red")
        progress['value'] = 92
        return

    # Final Success
    result_label.config(text="All validations passed ✓ Strong Password!", fg="green")
    progress['value'] = 100

    open_login_page()

# ---------------- Login Page ---------------- #
def open_login_page():
    login = tk.Toplevel(root)
    login.title("Login Page")
    login.geometry("350x250")
    login.configure(bg="#1e1e2f")

    tk.Label(login, text="Login Successful!",
             font=("Arial", 14, "bold"),
             fg="lightgreen", bg="#1e1e2f").pack(pady=10)

    tk.Label(login, text="Enter Username:",
             font=("Arial", 11),
             fg="white", bg="#1e1e2f").pack()

    tk.Entry(login, width=25, font=("Arial", 12)).pack(pady=5)

    tk.Button(login, text="Continue",
              font=("Arial", 11, "bold"),
              bg="#4CAF50", fg="white").pack(pady=10)

# ---------------- Toggle Password Show/Hide ---------------- #
def toggle_show():
    if show_var.get():
        entry_pass.config(show="")
        entry_confirm.config(show="")
    else:
        entry_pass.config(show="*")
        entry_confirm.config(show="*")

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("Advanced Password Validator System")
root.geometry("600x550")
root.config(bg="#1e1e2f")
root.resizable(False, False)

title = tk.Label(root, text="Advanced Password Generator & Validator",
                 font=("Helvetica", 17, "bold"), fg="white", bg="#1e1e2f")
title.pack(pady=20)

frame = tk.Frame(root, bg="#2c2c3e", padx=35, pady=25)
frame.pack()

# UI components
tk.Label(frame, text="Enter Password:", fg="white", bg="#2c2c3e",
         font=("Arial", 12)).grid(row=0, column=0, sticky="w")
entry_pass = tk.Entry(frame, show="*", width=35, font=("Arial", 12))
entry_pass.grid(row=1, column=0, pady=10)

tk.Label(frame, text="Confirm Password:", fg="white", bg="#2c2c3e",
         font=("Arial", 12)).grid(row=2, column=0, sticky="w")
entry_confirm = tk.Entry(frame, show="*", width=35, font=("Arial", 12))
entry_confirm.grid(row=3, column=0, pady=10)

show_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Show Password", variable=show_var,
               command=toggle_show, bg="#2c2c3e", fg="white",
               selectcolor="#2c2c3e").grid(row=4, column=0, sticky="w", pady=5)

strength_label = tk.Label(root, text="Strength: ", fg="white",
                          bg="#1e1e2f", font=("Arial", 12, "bold"))
strength_label.pack()

tk.Button(root, text="Generate Password", command=generate_password,
          font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
          width=20).pack(pady=10)

tk.Button(root, text="Validate Password", command=validate_password,
          font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
          width=20).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"),
                        bg="#1e1e2f")
result_label.pack(pady=10)

progress = ttk.Progressbar(root, length=420, mode="determinate")
progress.pack(pady=10)

tk.Label(root, text="© 2026 Secured Authentication System",
         fg="#aaaaaa", bg="#1e1e2f", font=("Arial", 8)).pack(side="bottom", pady=10)

root.mainloop()