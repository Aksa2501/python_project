import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import winsound
import datetime
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------- VARIABLES ----------
remaining_seconds = 0
total_seconds = 0
running = False
sessions_file = "study_sessions.csv"

# Initialize sessions file if it doesn't exist
if not os.path.exists(sessions_file):
    pd.DataFrame(columns=["Date", "Duration_Minutes"]).to_csv(sessions_file, index=False)

# ---------- MOTIVATION MESSAGES ----------
messages = [
    "Great work! Keep going 🌟",
    "You're doing amazing 📚",
    "Stay focused 💡",
    "Small progress is still progress 💪",
    "Success is built on discipline 🔥"
]

# ---------- CLEAR ENTRY ----------
def clear_entry(event):
    if entry.get() == "Enter study time (minutes)":
        entry.delete(0, tk.END)

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

            finish_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            finish_label.config(text="Ends at: " + finish_time.strftime("%H:%M"))

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

            # Play louder/longer beeps
            for i in range(3):
                winsound.Beep(1000, 500)
                window.update()

            # Save session to CSV
            save_session(total_seconds // 60)

            messagebox.showinfo(
                "Session Complete 🌸",
                random.choice(messages)
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

# ---------- SAVE SESSION ----------
def save_session(minutes):
    df = pd.read_csv(sessions_file)
    new_session = pd.DataFrame({
        "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M")],
        "Duration_Minutes": [minutes]
    })
    df = pd.concat([df, new_session], ignore_index=True)
    df.to_csv(sessions_file, index=False)

# ---------- SHOW STATISTICS ----------
def show_statistics():
    try:
        df = pd.read_csv(sessions_file)
        
        # Create a new window for statistics
        stats_window = tk.Toplevel(window)
        stats_window.title("Study Statistics")
        stats_window.geometry("700x550")
        stats_window.configure(bg="#fdf6f0")
        
        if len(df) == 0:
            # Show empty state with instructions
            empty_label = tk.Label(
                stats_window, 
                text="📊 No Study Sessions Yet!\n\nComplete a study session to see your statistics here.",
                font=("Segoe UI", 14),
                bg="#fdf6f0",
                fg="#7b8fa1"
            )
            empty_label.pack(pady=50)
            return
        
        # Convert duration to numeric
        df["Duration_Minutes"] = pd.to_numeric(df["Duration_Minutes"], errors='coerce')
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))
        fig.patch.set_facecolor('#fdf6f0')
        
        # Chart 1: Total hours studied
        total_hours = df["Duration_Minutes"].sum() / 60
        ax1.bar(["Total Hours"], [total_hours], color="#cde7ff", edgecolor="#7b8fa1", linewidth=2)
        ax1.set_ylabel("Hours", fontsize=10)
        ax1.set_title("Total Study Hours", fontweight="bold", fontsize=11)
        ax1.set_ylim(0, max(total_hours * 1.2, 1))
        
        # Chart 2: Session durations
        ax2.bar(range(len(df)), df["Duration_Minutes"].values, color="#d7f9e9", edgecolor="#7b8fa1", linewidth=2)
        ax2.set_xlabel("Session", fontsize=10)
        ax2.set_ylabel("Duration (min)", fontsize=10)
        ax2.set_title("Session Durations", fontweight="bold", fontsize=11)
        
        # Chart 3: Average session duration
        avg_duration = df["Duration_Minutes"].mean()
        ax3.bar(["Average"], [avg_duration], color="#ffd6e0", edgecolor="#7b8fa1", linewidth=2)
        ax3.set_ylabel("Minutes", fontsize=10)
        ax3.set_title("Average Session Duration", fontweight="bold", fontsize=11)
        ax3.set_ylim(0, max(avg_duration * 1.5, 10))
        
        # Chart 4: Session count
        session_count = len(df)
        ax4.bar(["Sessions"], [session_count], color="#fff4cc", edgecolor="#7b8fa1", linewidth=2)
        ax4.set_ylabel("Count", fontsize=10)
        ax4.set_title("Total Sessions Completed", fontweight="bold", fontsize=11)
        ax4.set_ylim(0, max(session_count * 1.2, 1))
        
        plt.tight_layout()
        
        # Embed matplotlib in tkinter
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add stats text
        stats_text = f"📊 Quick Stats:\n• Total Sessions: {session_count}\n• Total Hours: {total_hours:.2f}h\n• Average Duration: {avg_duration:.1f} min"
        stats_label = tk.Label(stats_window, text=stats_text, font=("Segoe UI", 11), bg="#fdf6f0", justify="left")
        stats_label.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not load statistics: {str(e)}")

# ---------- RESET ----------
def reset_timer():
    global running, remaining_seconds

    running = False
    remaining_seconds = 0

    time_label.config(text="00:00")
    progress["value"] = 0
    finish_label.config(text="")

# ---------- WINDOW ----------
window = tk.Tk()
window.title("Pastel Study Timer")
window.geometry("520x520")
window.configure(bg="#fdf6f0")

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
    width=22
)

entry.insert(0, "Enter study time (minutes)")
entry.bind("<FocusIn>", clear_entry)
entry.pack(pady=10)

# ---------- TIMER ----------
time_label = tk.Label(
    frame,
    text="00:00",
    font=("Segoe UI", 48, "bold"),
    fg="#9aa5b1",
    bg="#fdf6f0"
)
time_label.pack(pady=10)

# ---------- FINISH TIME ----------
finish_label = tk.Label(
    frame,
    text="",
    font=("Segoe UI", 12),
    bg="#fdf6f0"
)
finish_label.pack()

# ---------- PROGRESS ----------
progress = ttk.Progressbar(
    frame,
    length=300,
    mode="determinate"
)
progress.pack(pady=15)

# ---------- BUTTON FRAME ----------
btn_frame = tk.Frame(frame, bg="#fdf6f0")
btn_frame.pack(pady=10)

# ---------- BUTTON STYLE ----------
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

# ---------- BUTTONS ----------
pastel_button("Start", start_timer, "#cde7ff").grid(row=0,column=0,padx=5)
pastel_button("Pause", pause_timer, "#ffd6e0").grid(row=0,column=1,padx=5)
pastel_button("Resume", resume_timer, "#d7f9e9").grid(row=0,column=2,padx=5)
pastel_button("Reset", reset_timer, "#fff4cc").grid(row=0,column=3,padx=5)

# Add statistics button on a new row
tk.Button(
    btn_frame,
    text="📊 Statistics",
    command=show_statistics,
    font=("Segoe UI", 11, "bold"),
    bg="#f0e6ff",
    fg="#5a5a5a",
    relief="flat",
    width=38,
    cursor="hand2"
).grid(row=1, column=0, columnspan=4, padx=5, pady=5)

window.mainloop()
