import os.path
import datetime
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import cv2
import face_recognition
import sqlite3
import util


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+100+100")
        self.main_window.title("Smart Attendance System")

        self.login_button_main_window = util.get_button(self.main_window,
                                                        image_path="C:/Users/HP/PycharmProjects/SmartAttendanceSystemUsingFacialRecognition/login_button.svg.png",
                                                        command=self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(self.main_window,
                                                         image_path="C:/Users/HP/PycharmProjects/SmartAttendanceSystemUsingFacialRecognition/logout_button.svg.png",
                                                         command=self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window,
                                                                    image_path="C:/Users/HP\PycharmProjects/SmartAttendanceSystemUsingFacialRecognition/register_new_user.svg.png",
                                                                    command=self.register_new_user)
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.cap = cv2.VideoCapture(0)  # Initialize the camera capture object

        if not self.cap.isOpened():  # Check if the camera is available
            util.msg_box('Error', 'Camera not available.')
            return

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

        self.most_recent_capture_arr = None
        self.most_recent_capture_pil = None
        self.register_new_user_capture = None

        self.entry_text_register_new_user = None

        # Connect to the SQLite database
        self.conn = sqlite3.connect(os.path.join(os.getcwd(), 'db', 'attendance.db'))
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance_log (
                id INTEGER PRIMARY KEY,
                Name TEXT,
                Date TEXT,
                Time TEXT,
                Attendance TEXT
            )
        ''')

        self.conn.commit()

    def add_attendance_record(self, Name, Date, Time, Attendance):
        cursor = self.conn.cursor()

        cursor.execute('''
            INSERT INTO attendance_log (Name, Date, Time, Attendance)
            VALUES (?, ?, ?, ?)
        ''', (Name, Date, Time, Attendance))

        self.conn.commit()

    def delete_attendance_record(self, record_id):
        cursor = self.conn.cursor()

        cursor.execute('''
            DELETE FROM attendance_log
            WHERE id = ?
        ''', (record_id,))

        self.conn.commit()

    def add_webcam(self, label):
        self._label = label
        self.process_webcam()

    def destroy_webcam(self):
        self.cap.release()

    def destroy_window(self):
        self.destroy_webcam()
        self.main_window.destroy()

    def destroy_register_new_user_window(self):
        self.destroy_webcam()
        self.register_new_user_window.destroy()

    def process_webcam(self):
        ret, frame = self.cap.read()

        if ret:
            self.most_recent_capture_arr = frame

            # Detect faces in the captured frame
            face_locations = face_recognition.face_locations(frame)

            # Draw green boxes around the detected faces
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)

            # Create a rounded rectangle mask
            mask = Image.new("L", self.most_recent_capture_pil.size, 0)
            width, height = mask.size
            radius = 20  # Adjust this value to change the roundness of corners
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, width, height), radius, fill=255)

            # Apply the mask to the image
            self.most_recent_capture_pil.putalpha(mask)

            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.configure(image=imgtk)
            self._label.image = imgtk

        self._label.after(20, self.process_webcam)

    def login(self):
        if self.most_recent_capture_arr is None:
            util.msg_box('Error', 'No captured image found.')
            return

        # Make sure the 'recognize' function is properly defined in the 'util' module
        name = util.recognize(self.most_recent_capture_arr, self.db_dir)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ups...', 'Unknown user. Please register a new user or try again.')
        else:
            util.msg_box('Welcome back!', 'Attendance Marked, {}.'.format(name))
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            time = datetime.datetime.now().strftime("%H:%M:%S")
            self.add_attendance_record(name, date, time, "Present")

    def logout(self):
        if self.most_recent_capture_arr is None:
            util.msg_box('Error', 'No captured image found.')
            return

        name = util.recognize(self.most_recent_capture_arr, self.db_dir)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ups...', 'Unknown user. Please register a new user or try again.')
        else:
            util.msg_box('Goodbye!', 'You have logged out successfully, {}.'.format(name))
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            time = datetime.datetime.now().strftime("%H:%M:%S")
            self.add_attendance_record(name, date, time, "logout")

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+130+120")
        self.register_new_user_window.title("Register New User")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window,
                                                                      image_path="C:/Users/HP/PycharmProjects/SmartAttendanceSystemUsingFacialRecognition/accept_button.svg.png",
                                                                      command=self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window,
                                                                         image_path="C:/Users/HP/PycharmProjects/SmartAttendanceSystemUsingFacialRecognition/try_again.svg.png",
                                                                         command=self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,
                                                                'Please, \nenter username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        if self.most_recent_capture_pil is None:
            util.msg_box('Error', 'No captured image found.')
            return

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.configure(image=imgtk)
        label.image = imgtk

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        if self.register_new_user_capture is None:
            util.msg_box('Error', 'No captured image found.')
            return

        name = self.entry_text_register_new_user.get(1.0, "end-1c").strip()

        if name:
            embeddings = face_recognition.face_encodings(self.register_new_user_capture)
            if len(embeddings) > 0:
                file_path = os.path.join(self.db_dir, '{}.jpg'.format(name))
                cv2.imwrite(file_path, self.register_new_user_capture)
                util.msg_box('Success!', 'User was registered successfully!')
            else:
                util.msg_box('Error', 'No face detected. Please try again with a clear face.')
        else:
            util.msg_box('Error', 'Please enter a valid username.')


        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()















