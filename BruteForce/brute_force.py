import itertools
import string
import time
import tkinter as tk
from tkinter import ttk
import re


# Function to load common passwords from a file with UTF-8 encoding
def load_common_passwords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except UnicodeDecodeError:
        print(f"Error decoding the file: {file_path}. Please check the file encoding.")
        return []


# Load the common passwords from a file
common_passwords = load_common_passwords('common_passwords.txt')

# Fallback to a default list if the file is not found or empty
if not common_passwords:
    common_passwords = [
        "123456", "password", "123456789", "12345678", "12345",
        "1234567", "1234", "qwerty", "1234567890", "letmein",
        "password1", "welcome", "ninja", "abc123", "sunshine",
        "password123", "admin", "iloveyou", "monkey", "123321",
        "football", "123", "000000", "1qaz2wsx", "qwertyuiop"
    ]


# Function to estimate time to crack a password using brute force
def estimate_brute_force_time(password, charset):
    combinations = sum(len(charset) ** length for length in range(1, len(password) + 1))
    # Assuming 1 million attempts per second as a rough estimate
    attempts_per_second = 1_000_000
    time_to_crack = combinations / attempts_per_second
    return time_to_crack


# Function to convert seconds to days, hours, minutes, and seconds
def convert_seconds_to_time(seconds):
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return days, hours, minutes, seconds


# Function to check if password is in dictionary
def check_dictionary(password):
    return password in common_passwords


# Function to check if the password follows common patterns
def check_common_patterns(password):
    # Regular expressions for common patterns
    patterns = [
        r'(.)\1\1',  # Repeated characters
        r'(012|123|234|345|456|567|678|789|890)',  # Sequential digits
        r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',
        # Sequential letters
        r'qwerty',  # Keyboard patterns
    ]
    for pattern in patterns:
        if re.search(pattern, password):
            return True
    return False


# Function to evaluate password strength
def evaluate_password(password):
    # Basic criteria
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    # Check dictionary
    if check_dictionary(password):
        return "Weak", 0, True

    # Check common patterns
    if check_common_patterns(password):
        return "Weak", 0, True

    # Password strength evaluation based on criteria
    if length >= 8 and sum([has_lower, has_upper, has_digit, has_symbol]) >= 3:
        charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        brute_force_time = estimate_brute_force_time(password, charset)
        return "Strong", brute_force_time, False
    elif length >= 6:
        return "Moderate", 0, False
    else:
        return "Weak", 0, False


# Function to update the progress bar color and label
def update_strength_meter(strength):
    if strength == "Weak":
        strength_meter["value"] = 25
        strength_meter_label.config(text="Weak", foreground="red")
    elif strength == "Moderate":
        strength_meter["value"] = 50
        strength_meter_label.config(text="Moderate", foreground="orange")
    elif strength == "Strong":
        strength_meter["value"] = 100
        strength_meter_label.config(text="Strong", foreground="green")


# Function to update UI based on password evaluation
def update_ui(event=None):
    password = password_entry.get()
    strength, time_to_crack, in_dictionary_or_pattern = evaluate_password(password)

    update_strength_meter(strength)

    if in_dictionary_or_pattern:
        result_label.config(text=f"Password is in the common passwords list or follows a common pattern! Very Weak!")
        suggestion_label.config(text="Suggestions: Use a longer password with a mix of letters, numbers, and symbols.")
    else:
        days, hours, minutes, seconds = convert_seconds_to_time(time_to_crack)
        result_label.config(
            text=f"Password Strength: {strength}\nEstimated time to crack: {days} days, {hours} hours, {minutes} minutes, {seconds:.2f} seconds")
        if strength == "Weak" or strength == "Moderate":
            suggestion_label.config(
                text="Suggestions: Use a longer password with a mix of letters, numbers, and symbols.")
        else:
            suggestion_label.config(text="Your password is strong!")


# Function to initialize the UI
def setup_ui():
    root = tk.Tk()
    root.title("Password Strength Checker")

    tk.Label(root, text="Enter your password:").pack(pady=5)
    global password_entry
    password_entry = tk.Entry(root, width=30, show="*")  # Mask the password input
    password_entry.pack(pady=5)
    password_entry.bind("<KeyRelease>", update_ui)

    global strength_meter
    strength_meter = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    strength_meter.pack(pady=5)

    global strength_meter_label
    strength_meter_label = tk.Label(root, text="Strength")
    strength_meter_label.pack(pady=5)

    global result_label
    result_label = tk.Label(root, text="")
    result_label.pack(pady=10)

    global suggestion_label
    suggestion_label = tk.Label(root, text="")
    suggestion_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    setup_ui()
