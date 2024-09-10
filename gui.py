import customtkinter as ctk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np

# Initialize CustomTkinter theme
ctk.set_appearance_mode("System")  # System, Dark, or Light
ctk.set_default_color_theme("green")  # Optional: can use other themes like 'green', 'dark-blue'

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")
        self.root.geometry("1000x600")

        # Main frame
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True)

        # Left side frame
        left_frame = ctk.CTkFrame(main_frame, width=300, corner_radius=10)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # # Logo
        self.logo_image = ctk.CTkImage(Image.open("logo.png"), size=(80, 80))  # Replace with your logo
        logo_label = ctk.CTkLabel(left_frame, image=self.logo_image)
        logo_label.pack(pady=10)

        # Buttons for left side
        btn_take_attendance = ctk.CTkButton(left_frame, text="Take Attendance", command=self.take_attendance)
        btn_take_attendance.pack(pady=10)

        btn_add_people = ctk.CTkButton(left_frame, text="Add People", command=self.add_people)
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

        btn_camera = ctk.CTkButton(right_frame, text="Open Camera", command=self.open_camera)
        btn_camera.pack(pady=10)

        name_label = ctk.CTkLabel(right_frame, text="Name of the Student")
        name_label.pack(pady=5)

        # Display student name
        self.student_name_display = ctk.CTkLabel(right_frame, text="Student Name Will Be Displayed Here")
        self.student_name_display.pack(pady=10)

        # Mark Attendance
        mark_attendance_button = ctk.CTkButton(right_frame, text="Mark My Attendance", command=self.mark_attendance)
        mark_attendance_button.pack(pady=10)

        # Keyboard shortcut for marking attendance
        self.root.bind('<Control-m>', self.mark_attendance_shortcut)

    def take_attendance(self):
        messagebox.showinfo("Take Attendance", "This feature will handle attendance taking.")
    
    def add_people(self):
        messagebox.showinfo("Add People", "This feature will allow adding people.")
    
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
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.imshow('Camera', frame)
            
            # Press 'q' to quit the camera
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def mark_attendance(self):
        messagebox.showinfo("Attendance", "Attendance marked successfully!")

    def mark_attendance_shortcut(self, event):
        self.mark_attendance()

# Create the main window
root = ctk.CTk()
app = AttendanceSystem(root)
root.mainloop()
