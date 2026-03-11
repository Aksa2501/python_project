import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import winsound

# ---------- VARIABLES ----------
remaining_seconds = 0
total_seconds = 0
running = False

# ---------- CLEAR ENTRY ----------
def clear_entry(event):
    if entry.get() == "Enter study time (minutes)":
        entry.delete(0, tk.END)
        entry.config(fg="#5a5a5a")

# ---------- START TIMER ----------
def start_timer():
    global remaining_seconds, total_seconds, running

    if not running:
        try:
            minutes = int(entry.get())

            if minutes <= 0:
                messagebox.showerror("Invalid", "Enter valid time")
                return

            remaining_seconds = minutes * 60
            total_seconds = remaining_seconds

            progress["maximum"] = total_seconds

            running = True
            update_timer()

        except:
            messagebox.showerror("Error", "Enter numbers only")

# ---------- UPDATE TIMER ----------
def update_timer():
    global remaining_seconds, running

    if running:

        mins = remaining_seconds // 60
        secs = remaining_seconds % 60

        time_label.config(text=f"{mins:02d}:{secs:02d}")

        progress["value"] = total_seconds - remaining_seconds

        if remaining_seconds > 0:
            remaining_seconds -= 1
            window.after(1000, update_timer)

        else:
            running = False

            # Alarm sound
            winsound.Beep(1000, 1000)

            messagebox.showinfo(
                "Session Complete 🌸",
                "You did amazing. Take a break 💗"
            )

# ---------- PAUSE ----------
def pause_timer():
    global running
    running = False

# ---------- RESUME ----------
def resume_timer():
    global running
    if remaining_seconds > 0:
        running = True
        update_timer()

# ---------- RESET ----------
def reset_timer():
    global running, remaining_seconds

    running = False
    remaining_seconds = 0

    time_label.config(text="00:00")
    progress["value"] = 0

# ---------- WINDOW ----------
window = tk.Tk()
window.title("Pastel Study Timer")
window.geometry("520x500")
window.configure(bg="#fdf6f0")

# ---------- CANVAS ----------
canvas = tk.Canvas(window, width=520, height=500, bg="#fdf6f0", highlightthickness=0)
canvas.place(x=0, y=0)

# Book doodles
canvas.create_rectangle(40, 380, 120, 420, fill="#ffd6e0", outline="")
canvas.create_rectangle(50, 360, 130, 400, fill="#cde7ff", outline="")
canvas.create_rectangle(60, 340, 140, 380, fill="#d7f9e9", outline="")

# Pen doodle
canvas.create_line(400, 100, 460, 160, fill="#b5ead7", width=6)
canvas.create_oval(455, 155, 465, 165, fill="#b5ead7", outline="")

# ---------- FRAME ----------
frame = tk.Frame(window, bg="#fdf6f0")
frame.place(relx=0.5, rely=0.5, anchor="center")

# ---------- TITLE ----------
title = tk.Label(
    frame,
    text="Study Session Timer",
    font=("Segoe UI", 26, "bold"),
    fg="#7b8fa1",
    bg="#fdf6f0"
)
title.pack(pady=15)

# ---------- ENTRY ----------
entry = tk.Entry(
    frame,
    font=("Segoe UI", 16),
    justify="center",
    bg="#ffffff",
    fg="#a0a0a0",
    relief="flat",
    width=22
)

entry.insert(0, "Enter study time (minutes)")
entry.bind("<FocusIn>", clear_entry)
entry.pack(pady=10)

# ---------- TIMER LABEL ----------
time_label = tk.Label(
    frame,
    text="00:00",
    font=("Segoe UI", 48, "bold"),
    fg="#9aa5b1",
    bg="#fdf6f0"
)
time_label.pack(pady=10)

# ---------- PROGRESS BAR ----------
style = ttk.Style()
style.theme_use("default")

style.configure(
    "TProgressbar",
    thickness=8,
    background="#b5ead7",
    troughcolor="#ffe5ec"
)

progress = ttk.Progressbar(frame, length=300, mode="determinate")
progress.pack(pady=15)

# ---------- BUTTON FRAME ----------
btn_frame = tk.Frame(frame, bg="#fdf6f0")
btn_frame.pack(pady=10)

def pastel_button(text, command, color):
    return tk.Button(
        btn_frame,
        text=text,
        command=command,
        font=("Segoe UI", 11, "bold"),
        bg=color,
        fg="#5a5a5a",
        relief="flat",
        width=9,
        cursor="hand2"
    )

pastel_button("Start", start_timer, "#cde7ff").grid(row=0, column=0, padx=5)
pastel_button("Pause", pause_timer, "#ffd6e0").grid(row=0, column=1, padx=5)
pastel_button("Resume", resume_timer, "#d7f9e9").grid(row=0, column=2, padx=5)
pastel_button("Reset", reset_timer, "#fff4cc").grid(row=0, column=3, padx=5)

window.mainloop()
