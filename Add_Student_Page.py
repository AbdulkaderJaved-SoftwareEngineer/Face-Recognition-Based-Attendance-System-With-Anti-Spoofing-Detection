import os
import cv2
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Student Management")

        # Global variables as instance variables
        self.cap = None
        self.roll_entry = None

        # Ensure the directory for storing images exists
        if not os.path.exists("ImagesBasic"):
            os.makedirs("ImagesBasic")

        self.show_main_page()

    # Function to capture the image and save it
    def capture_image(self):
        ret, frame = self.cap.read()
        roll_no = self.roll_entry.get().strip()
        if not roll_no:
            messagebox.showerror("Error", "Roll number is required to save the image.")
            return
        if ret:
            img_name = f"ImagesBasic/{roll_no}.png"
            cv2.imwrite(img_name, frame)
            messagebox.showinfo("Success", f"Image saved as {img_name}")
            # Return to the main page
            self.show_main_page()
        else:
            messagebox.showerror("Error", "Failed to capture image")

    # Function to show the form and camera feed
    def show_capture_page(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a main frame to hold everything
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create the form for student details
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Input fields for student details
        tk.Label(form_frame, text="Student Name:", bg="#2b2b2b", fg="white").grid(row=0, column=0, padx=10, pady=5,
                                                                                  sticky="w")
        name_entry = ctk.CTkEntry(form_frame)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Branch:", bg="#2b2b2b", fg="white").grid(row=1, column=0, padx=10, pady=5,
                                                                            sticky="w")
        branch_entry = ctk.CTkEntry(form_frame)
        branch_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Roll No:", bg="#2b2b2b", fg="white").grid(row=2, column=0, padx=10, pady=5,
                                                                             sticky="w")
        self.roll_entry = ctk.CTkEntry(form_frame)
        self.roll_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Year:", bg="#2b2b2b", fg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        year_entry = ctk.CTkEntry(form_frame)
        year_entry.grid(row=3, column=1, padx=10, pady=5)

        backBtn = ctk.CTkButton(form_frame, text="Back", command=self.show_main_page)
        backBtn.grid(row=4, column=1)

        # Create a frame for camera feed and capture button
        camera_frame = ctk.CTkFrame(main_frame)
        camera_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Display camera feed
        self.lmain = ctk.CTkLabel(camera_frame, text="")
        self.lmain.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Capture button below the camera feed
        capture_button = ctk.CTkButton(camera_frame, text="Capture Image", command=self.capture_image)
        capture_button.pack(pady=20)

        # Initialize camera
        self.cap = cv2.VideoCapture(0)

        self.show_frame()

    # Function to display the camera feed
    def show_frame(self):
        ret, frame = self.cap.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lmain.imgtk = imgtk
            self.lmain.configure(image=imgtk)
            self.lmain.after(10, self.show_frame)

    # Function to show the main page with Add Student button
    def show_main_page(self):
        # Release the camera if it's open
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add Student button
        add_student_button = ctk.CTkButton(self.root, text="Add Student", command=self.show_capture_page)
        add_student_button.pack(expand=True)


# Main window setup
root = ctk.CTk()
app = StudentManagementApp(root)
root.mainloop()

# Ensure the camera is released when the window is closed
if app.cap is not None:
    app.cap.release()
cv2.destroyAllWindows()
