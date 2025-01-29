import os
import re
import tkinter as tk
from tkinter import PhotoImage, messagebox, simpledialog

import cv2
import pyfiglet
import pyttsx3
from PIL import Image, ImageTk

from email_credentials import email, password
from send_email import send_emails 

# Initializing the required variables
password_attempts = 
max_attempts = 3
warning = pyttsx3.init()

# Function to record and store the face of a thief
save_path = 'pictures of unauthorized persons'
os.makedirs(save_path, exist_ok=True)
existing_images = [f for f in os.listdir(save_path) if f.endswith('.png')]
numeric_parts = [int(re.search(r'\d+', f).group()) for f in existing_images if re.search(r'\d+', f)]
highest_count = max(numeric_parts, default=0)
email_from = email
email_list = [email]

# Global variable for image count
image_count = highest_count

#This function initialize the camera module
def capture_face():
    global image_count
    image_capture = cv2.VideoCapture(0)
    _, frame = image_capture.read()
    image_capture.release()
    image_count += 1
    image_name = f'captured_image_{image_count}.png'
    image_path = os.path.join(save_path, image_name)
    cv2.imwrite(image_path, frame)

# Gives warning to the thief
def warn():
    warning.say("Leave my device, you are already captured..")
    print(pyfiglet.figlet_format("LOGIN UNSUCCESSFUL"))
    warning.runAndWait()


#defining a function to initialize message_box
def show_custom_message(title, message):
    messagebox.showinfo(title, message)

#Main logic drive to capture the face when it requires:
def login_attempt():
    global password_attempts

    password = simpledialog.askstring("Login", "Enter password:", parent=root, show='*')

    if password == "password":
        warning.say("Good job , you are successfully logged into your device.")
        warning.runAndWait()
        print(pyfiglet.figlet_format("Login Successfull"))
        show_custom_message("Login Successful\n",
                            "you have successfully logged into your device.")
        
        return True
    else:
        warning.say("please kindly enter your correct password.")
        warning.runAndWait()
        password_attempts += 1

        if password_attempts == max_attempts:
            capture_face()
            warn()
            send_emails(email_list)
            show_custom_message("Login unsuccessfull ", "login unsuccessfull You can't hide your face.")

            return False
        else:
            show_custom_message("Login Failed",
                                f"wrong password \nmake sure you entered the correct password!\n Attempts left: {max_attempts - password_attempts}")
            return False

#Main function where the dailogue boxes run
def main():
    global root
    root = tk.Tk()
    root.title("login page")
    root.geometry("800x600")

    # Background Image
    bg_image_path = "files\\bg6.jpg"
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((1000, 800))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Capture Face Button
    capture_button = tk.Button(root, text="", command=capture_face, bg="cyan", fg="black")
    capture_button.place(relx=0.5, rely=0.8, anchor="center")

    # Login Attempt Loop
    print(pyfiglet.figlet_format("Enter your password"))
    while password_attempts < max_attempts:
        result = login_attempt()
        if result:
            break
    root.destroy()
if __name__ == "__main__":
    main()

