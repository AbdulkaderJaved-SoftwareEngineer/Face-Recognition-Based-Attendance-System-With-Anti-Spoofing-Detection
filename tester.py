import os
import random
import customtkinter as ctk
from tkinter import messagebox, Toplevel
import cv2
import face_recognition
from PIL import Image, ImageTk
import threading
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

ctk.set_appearance_mode("Dark")  # System, Dark, or Light
ctk.set_default_color_theme("dark-blue")  # Optional: can use other themes like 'green', 'dark-blue'


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


class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")
        self.root.geometry("1000x600")
        self.isCameraStarted = False
        self.encodelistknown = []

        self.cap = None  # Capture object for the webcam
        self.video_running = False

        # Main frame
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True)

        # Left side frame
        left_frame = ctk.CTkFrame(main_frame, width=300, corner_radius=10)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Logo
        self.logo_image = ctk.CTkImage(Image.open("logo.png"), size=(100, 100))  # Replace with your logo
        logo_label = ctk.CTkLabel(left_frame, image=self.logo_image)
        logo_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(root, text="Video feed not started")
        self.status_label.pack(pady=10)

        self.stop_button = ctk.CTkButton(left_frame, text="Stop Video", command=self.stop_video_stream)
        self.stop_button.pack(pady=10)

        # Buttons for left side
        btn_take_attendance = ctk.CTkButton(left_frame, text="Take Attendance", command=lambda: self.take_attendance)
        btn_take_attendance.pack(pady=10)

        btn_add_people = ctk.CTkButton(left_frame, text="Add People", command=self.open_student_management_app)
        btn_add_people.pack(pady=10)

        btn_view_people = ctk.CTkButton(left_frame, text="View People", command=self.view_people)
        btn_view_people.pack(pady=10)

        btn_view_graph = ctk.CTkButton(left_frame, text="Graphs", command=self.view_graph)
        btn_view_graph.pack(pady=10)

        # Right side frame
        right_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Camera Source, Camera, and Student Info
        camera_source_label = ctk.CTkLabel(right_frame, text="Camera Source")
        camera_source_label.pack(pady=5)

        btn_camera = ctk.CTkButton(right_frame, text="Open Camera", command=self.take_attendance)
        btn_camera.pack(pady=10)

        self.name_label = ctk.CTkLabel(right_frame, text="Name of the Student")
        self.name_label.pack(pady=5)

        # Display student name
        self.student_name_display = ctk.CTkLabel(right_frame, text="Student Name Will Be Displayed Here")
        self.student_name_display.pack(pady=10)

        # Mark Attendance
        mark_attendance_button = ctk.CTkButton(right_frame, text="Mark My Attendance", command=self.mark_attendance)
        mark_attendance_button.pack(pady=10)

        self.video_label = ctk.CTkLabel(right_frame, text="CTRL + M (To take screenshot)")
        self.video_label.pack(padx=20, pady=20)

        # Keyboard shortcut for marking attendance
        self.root.bind('<Control-m>', self.mark_attendance_shortcut)

    def open_student_management_app(self):
        # Create a new Toplevel window for student management
        student_app_window = Toplevel(self.root)
        student_management_app = StudentManagementApp(student_app_window)

    def take_attendance(self):
        path = 'ImagesBasic'
        images = []
        self.className = []
        myList = os.listdir(path)
        print(myList)

        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            self.className.append(os.path.splitext(cl)[0])

        print(self.className)

        def findencodings(images):
            encodelist = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodelist.append(encode)

            return encodelist

        self.encodelistknown = findencodings(images)

        print("Encoding Completed!!!")
        if not self.video_running:
            self.video_running = True
            self.cap = cv2.VideoCapture(0)  # Open the webcam
            self.status_label.configure(text="Video feed running")
            self.open_camera()

    def view_people(self):
        messagebox.showinfo("View People", "This feature will list all people.")

    def view_graph(self):
        # Dummy data for graph
        attendance = [20, 35, 30, 35, 27]
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        plt.bar(days, attendance)
        plt.xlabel('Days')
        plt.ylabel('Attendance')
        plt.title('Weekly Attendance')
        plt.show()

    def open_camera(self):
        if self.video_running:
            ret, img = self.cap.read()
            if ret:
                frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                faceCur = face_recognition.face_locations(imgS)
                encodeCur = face_recognition.face_encodings(imgS, faceCur)

                for encodeFace, faceloc in zip(encodeCur, faceCur):
                    matches = face_recognition.compare_faces(self.encodelistknown, encodeFace)
                    faceDis = face_recognition.face_distance(self.encodelistknown, encodeFace)
                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex]:
                        name = self.className[matchIndex].upper()
                        y1, x2, y2, x1 = faceloc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        self.student_name_display.configure(text=name)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                ctk_image = ctk.CTkImage(light_image=img, size=(640, 480))

                self.video_label.imgtk = ctk_image
                self.video_label.configure(image=ctk_image)

            self.root.after(30, self.open_camera)

    def mark_attendance(self):
        messagebox.showinfo("Attendance", "Attendance marked successfully!")

    def mark_attendance_shortcut(self, event):
        self.mark_attendance()

    def stop_video_stream(self):
        if self.video_running:
            self.video_running = False
            self.cap.release()
            self.video_label.configure(image='')
            self.status_label.configure(text="Video feed stopped")

# Create the
root = ctk.CTk()
app = AttendanceSystem(root)
root.mainloop()
