import customtkinter
from PIL import Image, ImageTk
import os
import io
import tkinter as tk
from tkinter import messagebox
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

CREDENTIALS_FILE = 'credentials.json'
DRIVE_API_SCOPE = ['https://www.googleapis.com/auth/drive']  # Need full access for delete

class GoogleDriveImageGalleryApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Google Drive Image Gallery")
        self.geometry("1200x700")
        self.iconbitmap('icon.ico') 

        self.drive_service = self.authenticate_drive()
        self.all_drive_images = self.load_drive_images()
        self.thumbnail_cache = {}  # Cache for downloaded thumbnails
        self.current_enlarged_image_id = None
        self.enlarged_image_data = None

        # Left Frame for Scrollable Image Thumbnails
        self.left_frame = customtkinter.CTkFrame(self, width=400)
        self.left_frame.pack(side="left", fill="y", padx=20, pady=20)

        self.gallery_label = customtkinter.CTkLabel(self.left_frame, text="Google Drive Image Gallery", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.gallery_label.pack(pady=(20, 10))

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.left_frame, label_text="Thumbnails", width=380, height=500)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.thumbnail_buttons = []
        self.display_thumbnails()

        self.refresh_button = customtkinter.CTkButton(self.left_frame, text="Refresh Gallery", fg_color='blue', command=self.refresh_gallery)
        self.refresh_button.pack(pady=10)

        # Right Frame for Enlarged Image and Controls
        self.right_frame = customtkinter.CTkFrame(self, width=750)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.enlarged_label = customtkinter.CTkLabel(self.right_frame, text="Enlarged View", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.enlarged_label.pack(pady=(20, 10))

        self.image_display_frame = customtkinter.CTkFrame(self.right_frame, height=450)
        self.image_display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.enlarged_image_label = customtkinter.CTkLabel(self.image_display_frame, text="")
        self.enlarged_image_label.pack(fill="both", expand=True)

        self.controls_frame = customtkinter.CTkFrame(self.right_frame)
        self.controls_frame.pack(pady=10)

        self.download_button = customtkinter.CTkButton(self.controls_frame, text="Download", fg_color='blue', command=self.download_image, state="disabled")
        self.download_button.pack(side="left", padx=10)

        self.delete_button = customtkinter.CTkButton(self.controls_frame, text="Delete from Drive", fg_color="firebrick", hover_color="indianred", command=self.delete_image_dialog, state="disabled")
        self.delete_button.pack(side="left", padx=10)

    def authenticate_drive(self):
        try:
            creds = service_account.Credentials.from_service_account_file(
                CREDENTIALS_FILE, scopes=DRIVE_API_SCOPE
            )
            service = build('drive', 'v3', credentials=creds)
            print("Successfully authenticated with Google Drive.")
            return service
        except Exception as e:
            messagebox.showerror("Authentication Error", f"Failed to authenticate with Google Drive: {e}")
            return None

    def load_drive_images(self):
        if not self.drive_service:
            return []
        try:
            results = self.drive_service.files().list(
                q="mimeType contains 'image/'",
                fields="nextPageToken, files(id, name, mimeType)"
            ).execute()
            items = results.get('files', [])
            if not items:
                print("No image files found in Google Drive.")
                return []
            print(f"Found {len(items)} image files in Google Drive.")
            return items
        except Exception as e:
            messagebox.showerror("Drive Error", f"Failed to load images from Google Drive: {e}")
            return []

    def download_thumbnail(self, file_id):
        if file_id in self.thumbnail_cache:
            return self.thumbnail_cache[file_id]
        try:
            request = self.drive_service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                # print(f"Download progress for {file_id}: {int(status.progress() * 100)}%")
            fh.seek(0)
            img = Image.open(fh)
            img.thumbnail((128, 128))
            photo = ImageTk.PhotoImage(img)
            self.thumbnail_cache[file_id] = photo
            return photo
        except Exception as e:
            print(f"Error downloading thumbnail for {file_id}: {e}")
            return None

    def display_thumbnails(self):
        for button in self.thumbnail_buttons:
            button.destroy()
        self.thumbnail_buttons = []

        for i, image_data in enumerate(self.all_drive_images):
            thumbnail = self.download_thumbnail(image_data['id'])
            if thumbnail:
                button = customtkinter.CTkButton(self.scrollable_frame, image=thumbnail, text="", compound="top", width=130, height=130,
                                                command=lambda img_id=image_data['id'], name=image_data['name']: self.show_enlarged(img_id, name),
                                                hover=False, fg_color="transparent")
                button.grid(row=i // 2, column=i % 2, padx=5, pady=5)
                self.thumbnail_buttons.append(button)
            else:
                placeholder_label = customtkinter.CTkLabel(self.scrollable_frame, text="Error", width=130, height=130)
                placeholder_label.grid(row=i // 2, column=i % 2, padx=5, pady=5)
                self.thumbnail_buttons.append(placeholder_label)

    def show_enlarged(self, file_id, file_name):
        if not self.drive_service:
            return
        try:
            request = self.drive_service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                # print(f"Download progress for full image {file_name}: {int(status.progress() * 100)}%")
            fh.seek(0)
            img = Image.open(fh)
            self.enlarged_photo = ImageTk.PhotoImage(img)
            self.enlarged_image_label.configure(image=self.enlarged_photo, text="")
            self.current_enlarged_image_id = file_id
            self.enlarged_image_data = fh.getvalue()
            self.download_button.configure(state="normal")
            self.delete_button.configure(state="normal")

            # Resize the enlarged image to fit the frame
            self.resize_enlarged_image()
            self.bind("<Configure>", self.resize_enlarged_image)

        except Exception as e:
            self.enlarged_image_label.configure(text=f"Error displaying image: {e}", image=None)
            self.download_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")
            self.current_enlarged_image_id = None
            self.enlarged_image_data = None
            print(f"Error loading full image {file_name}: {e}")

    def resize_enlarged_image(self, event=None):
        if self.enlarged_image_data:
            try:
                img = Image.open(io.BytesIO(self.enlarged_image_data))
                width = self.image_display_frame.winfo_width() - 20
                height = self.image_display_frame.winfo_height() - 20
                img.thumbnail((width, height))
                self.enlarged_resized_photo = ImageTk.PhotoImage(img)
                self.enlarged_image_label.configure(image=self.enlarged_resized_photo)
            except Exception as e:
                print(f"Error resizing enlarged image: {e}")

    def refresh_gallery(self):
        self.all_drive_images = self.load_drive_images()
        self.thumbnail_cache = {}
        self.display_thumbnails()
        self.enlarged_image_label.configure(text="", image=None)
        self.download_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")
        self.current_enlarged_image_id = None
        self.enlarged_image_data = None
        self.unbind("<Configure>") # Unbind resize event when no image is shown

    def download_image(self):
        if self.current_enlarged_image_id and self.enlarged_image_data:
            try:
                file_metadata = next(item for item in self.all_drive_images if item['id'] == self.current_enlarged_image_id)
                original_filename = file_metadata.get('name', 'downloaded_image')
                save_path = tk.filedialog.asksaveasfilename(defaultextension=os.path.splitext(original_filename)[1] if '.' in original_filename else '.jpg', initialfile=original_filename, title="Save Image As")
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(self.enlarged_image_data)
                    messagebox.showinfo("Success", f"Image saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error downloading image: {e}")
        else:
            messagebox.showinfo("Info", "No image selected to download.")

    def delete_image_dialog(self):
        if self.current_enlarged_image_id:
            file_metadata = next((item for item in self.all_drive_images if item['id'] == self.current_enlarged_image_id), None)
            if file_metadata:
                image_name = file_metadata.get('name', 'this image')
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{image_name}' from Google Drive?"):
                    self.delete_image_from_drive()
            else:
                messagebox.showinfo("Info", "No image selected to delete.")
        else:
            messagebox.showinfo("Info", "No image selected to delete.")

    def delete_image_from_drive(self):
        if self.current_enlarged_image_id and self.drive_service:
            try:
                self.drive_service.files().delete(fileId=self.current_enlarged_image_id).execute()
                messagebox.showinfo("Success", "Image deleted from Google Drive.")
                self.current_enlarged_image_id = None
                self.enlarged_image_data = None
                self.enlarged_image_label.configure(text="", image=None)
                self.download_button.configure(state="disabled")
                self.delete_button.configure(state="disabled")
                self.refresh_gallery()  # Refresh the gallery to reflect the deletion
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting image from Google Drive: {e}")
        else:
            messagebox.showinfo("Info", "No image selected or Google Drive not connected.")

if __name__ == "__main__":
    app = GoogleDriveImageGalleryApp()
    if app.drive_service:
        app.mainloop()
