# 📸 Google Drive Image Gallery

A modern, fully-featured desktop application that brings your Google Drive image collection to life. This app uses a polished GUI built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), offering an intuitive experience for viewing, downloading, and managing your images stored on Google Drive.

Whether you're organizing photos, managing shared folders, or simply browsing your Drive visually, **Google Drive Image Gallery** is the elegant interface you've been missing.

---

## 🎯 Key Features

* 🔐 **Secure Google Drive Authentication**
  Connects securely using Google’s official service account credentials, with support for Drive API scopes.

* 🖼️ **Auto-Loading Image Thumbnails**
  Automatically fetches and caches thumbnails for all images in your Drive. Scrollable grid layout enables quick browsing.

* 🔍 **Enlarged Image View**
  Click any thumbnail to view the full-resolution version in the right pane. The view automatically resizes with your window.

* 💾 **Download to Local System**
  Save any image directly from Google Drive to your computer in a single click, using the original file format and name.

* 🗑️ **Delete from Google Drive**
  Permanently remove images from your Drive with confirmation prompts to avoid accidental deletions.

* 🔄 **Refresh Button**
  Updates the gallery with newly added or removed images instantly.

* 💡 **Responsive GUI**
  Clean layout with resizable frames and auto-scaling images, built with `CustomTkinter` for a native-like experience.

---

## ⚙️ Requirements

* Python 3.8+
* A Google Cloud Project with the **Google Drive API** enabled
* A **Service Account** with credentials JSON file
* Basic familiarity with managing files on Google Drive

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/google-drive-image-gallery.git
cd google-drive-image-gallery
```

### 2. Install dependencies

You can install the required packages with pip:

```bash
pip install customtkinter pillow google-api-python-client google-auth google-auth-oauthlib
```

Or use a `requirements.txt` file:

```txt
customtkinter
pillow
google-api-python-client
google-auth
google-auth-oauthlib
```

Save this as `requirements.txt` and run:

```bash
pip install -r requirements.txt
```

### 3. Add Google Drive API credentials

* Visit [Google Cloud Console](https://console.cloud.google.com/)
* Create a **Service Account**
* Enable the **Google Drive API**
* Download the JSON credentials file
* Rename the file to `credentials.json`
* Place it in the root directory of the project

### 4. Share your Drive folder (if needed)

If the Drive you're accessing does not belong to the service account, share the necessary folder or files with the email address of the service account.

### 5. Add an icon (optional)

Include an `icon.ico` file in the project root if you want a custom window icon. If not provided, the app still runs fine.

---

## ▶️ Usage

Launch the app with:

```bash
python Memories.py
```

Once running:

* The left pane shows thumbnails of all image files in your Google Drive
* Click any thumbnail to view a larger version
* Use the **Download** button to save the image
* Use the **Delete** button to permanently remove the image from Google Drive
* Click **Refresh Gallery** to reload the latest state of your Drive

---

## 📁 Project Structure

```bash
google-drive-image-gallery/
│
├── Memories.py           # Main application script
├── credentials.json      # Google API credentials file (not committed)
├── README.md             # You're here!
└── requirements.txt      
```

---

## ❗ Important Notes

* 🔐 **Security**: Never share your `credentials.json` file publicly.
* 🗑️ **Permanent Deletions**: Use the delete option with care — there's no undo.
* 🖼️ **Image Files Only**: The app filters and displays only files with `mimeType` starting with `image/`.
* 📦 **Thumbnail Caching**: Improves performance by reusing downloaded thumbnails in memory.

---

## 🧠 Future Improvements (You can work on)

* ✏️ Image renaming and metadata display
* 📂 Folder view and navigation
* 🗃️ Image categorization
* 🔍 Search by name or type
* 🌐 OAuth-based user authentication (non-service account)

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Support

Found a bug? Have a feature request?
Feel free to open an issue or submit a pull request.

## 🧑‍💻 Author
Made with ❤️ by Vaibhav Pandey

