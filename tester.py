import math
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
import pandas as pd
import datetime
from keras.api.preprocessing.image import img_to_array
from keras.api.models import model_from_json
from FaceDetectionModule import faceCascade, detect
from ultralytics import YOLO
import AttendanceSummarizer


ctk.set_appearance_mode("Dark")  # System, Dark, or Light
ctk.set_default_color_theme("dark-blue")  # Optional: can use other themes like 'green', 'dark-blue'

json_file = open('antispoofing_models/finalyearproject_antispoofing_model_mobilenet.json','r')
loaded_model_json = json_file.read()
json_file.close()

model = model_from_json(loaded_model_json)
# load antispoofing model weights
model.load_weights('antispoofing_models/finalyearproject_antispoofing_model_66-1.000000.weights.h5')
print("Anti Spoofing Model loaded")







class StudentManagementApp:
    
    def __init__(self, root):

        ctk.set_appearance_mode("Dark")  # System, Dark, or Light
        ctk.set_default_color_theme("dark-blue")  # Optional: can use other themes like 'green', 'dark-blue'

        self.root = root
        self.root.geometry("800x600")
        self.root.title("Student Management")

        # Global variables as instance variables
        self.cap = None
        self.roll_entry = None
        self.faceShown = False

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
        elif not self.faceShown:
            messagebox.showerror("Face Not Detected", "Please make sure your face is properly and then try to capture the image ")
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
        self.form_frame = ctk.CTkFrame(main_frame)
        self.form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Input fields for student details
        ctk.CTkLabel(self.form_frame, text="Student Name:").grid(row=0, column=0, padx=10, pady=5,
                                                                                  sticky="w")
        name_entry = ctk.CTkEntry(self.form_frame)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text="Branch:").grid(row=1, column=0, padx=10, pady=5,
                                                                            sticky="w")
        branch_entry = ctk.CTkEntry(self.form_frame)
        branch_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.form_frame, text="Roll No:").grid(row=2, column=0, padx=10, pady=5,
                                                                             sticky="w")
        self.roll_entry = ctk.CTkEntry(self.form_frame)
        self.roll_entry.grid(row=2, column=1, padx=10, pady=5)


        ctk.CTkLabel(self.form_frame, text="Year:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        year_entry = ctk.CTkEntry(self.form_frame)
        year_entry.grid(row=3, column=1, padx=10, pady=5)

        backBtn = ctk.CTkButton(self.form_frame, text="Back", command=self.go_to_back_page,width= 150,
             height = 40)
        backBtn.grid(row=4, column=1)



        year_entry = ctk.CTkEntry(self.form_frame)
        year_entry.grid(row=3, column=1, padx=10, pady=5)




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
            myFrame, face = detect(cv2image, faceCascade)
            if face:
                self.faceShown = True
            else:
                self.faceShown = False
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lmain.imgtk = imgtk
            self.lmain.configure(image=imgtk)
            self.lmain.after(10, self.show_frame)

        # Function to show the main page with Add Student button
    def go_to_back_page(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        self.show_main_page()




    def show_main_page(self):
        # Release the camera if it's open
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        backgrodundImage = Image.open('logo.png')
        bgImage2 = ImageTk.PhotoImage(backgrodundImage,size=(20,20))
        label = ctk.CTkLabel(self.root,image=bgImage2,text="")
        label.pack()


        # Add Student button
        add_student_button = ctk.CTkButton(self.root, text="Add Student", command=self.show_capture_page,width= 150,
             height = 40)
        add_student_button.pack(expand=True)


class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")
        self.root.geometry("1000x600")
        self.isCameraStarted = False
        self.encodelistknown = []
        json_file = open('antispoofing_models/finalyearproject_antispoofing_model_mobilenet.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        # load antispoofing model weights
        self.model.load_weights('antispoofing_models/finalyearproject_antispoofing_model_66-1.000000.weights.h5')
        print("Model loaded from disk")

        """self.classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]
"""

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

        btn_view_graph = ctk.CTkButton(left_frame, text="Graphs", command=self.attendance_summarizer)
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

    def is_spoof(self,frame):

        resized_face = cv2.resize(frame, (160, 160))
        resized_face = resized_face.astype("float") / 255.0
        # resized_face = img_to_array(resized_face)
        resized_face = np.expand_dims(resized_face, axis=0)
        # pass the face ROI through the trained liveness detector
        # model to determine if the face is "real" or "fake"
        preds = model.predict(resized_face)[0]
        print(preds)
        if preds > 0.4:
            label = 'spoof'
            print(f"Showing Spoof Image {preds}")
            messagebox.showwarning("Spoof Face Detected", "You are trying to Spoof the system")



    def checkPhone(self, img):
        results = self.phone(img, stream=True)
        org = False
        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values
                cls = int(box.cls[0])
                print("Class name -->", self.classNames[cls])
                if self.classNames[cls] == "cell phone":
                    # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    print(self.classNames[cls])
                    # confidence
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    print("Confidence --->", confidence)

                    # class name

                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    org = True
        return org
    def show_main_page(self):
        # Release the camera if it's open
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        backgrodundImage = Image.open('logo.png')
        bgImage2 = ImageTk.PhotoImage(backgrodundImage,size=(20,20))
        label = ctk.CTkLabel(self.root,image=bgImage2,text="")
        label.pack()


        # Add Student button
        add_student_button = ctk.CTkButton(self.root, text="Add Student", command=self.show_capture_page,width= 150,
             height = 40)
        add_student_button.pack(expand=True)

    def go_to_back_page(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        self.show_main_page()
    def show_page(self):
        self.Attendance_Summarizer(self.window)  # Use correct function name

        back_button = ctk.CTkButton(self.window, text="Back", command=self.window.destroy)
        back_button.pack(pady=10)

    def attendance_summarizer(self):
        AttendanceSummarizer.AttendanceSummarizerPage(self.root, self.go_to_back_page)

    def view_people(self):
        messagebox.showinfo("View People", "This feature will list all people.")


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
                    # Get face coordinates
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4,  y2 * 4, x1 * 4
                    face_img = img[y1:y2, x1:x2]


                    # Perform anti-spoofing check

                    if self.is_spoof(frame=frame) == "Spoof":  # Spoof detected
                        label = 'Spoof'
                        print("Showing Spoof Image")
                        self.student_name_display.configure(text="Spoof Detected!", font=('Arial', 25))

                        # Draw bounding box and label for the spoofed face
                        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    # Perform face recognition if the face is not a spoof
                    matches = face_recognition.compare_faces(self.encodelistknown, encodeFace)
                    faceDis = face_recognition.face_distance(self.encodelistknown, encodeFace)
                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex]:
                        name = self.className[matchIndex].upper()
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        self.student_name_display.configure(text=f'Now Showing: {name}', font=('Arial', 25))

                        with open('Attendance.csv', 'a+') as f:
                            mydataList = f.readlines()
                            namelist = [line.split(',')[0] for line in mydataList]

                            if name not in namelist:
                                now1 = datetime.datetime.now()
                                dateString = now1.strftime('%I:%M:%S')
                                taarik = now1.strftime('%Y/%m/%d')
                                f.writelines(f'\n{name},{dateString},Present,{taarik}')
                                f.flush()

                    else:
                        name = "UNKNOWN"
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        self.student_name_display.configure(text=f'Now Showing: {name}')

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