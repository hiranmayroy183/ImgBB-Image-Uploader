# ImgBB Image Uploading In Python
 Upload your images to imgbb for free from your local computer

# Image Uploader Application

## Overview

This project is a Python GUI application built using Tkinter that facilitates users in uploading local images from their computers to the ImgBB server. It consists of three main parts:

1. **User Application**: Allows users to select and upload images to ImgBB.
2. **Premium Account Token Generator**: Generates premium account tokens for registered users.
3. **Admin Panel**: Provides administrative functionalities to track uploads, manage users, and perform actions such as deletion or editing of uploads.

The application also includes a local database system to manage user data, upload records, and admin activities.

## Features

- **User Interface**: Utilizes Tkinter for a user-friendly graphical interface.
- **Image Upload**: Enables users to select images from their local machine and upload them to ImgBB.
- **Premium Account**: Allows registered users to generate tokens for premium account features.
- **Admin Dashboard**: Provides admin functionalities including:
  - Viewing all uploads
  - Managing user accounts
  - Editing or deleting uploads as necessary
- **Local Database**: Stores user data, upload records, and admin actions locally.

## Installation

To run the application locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/hiranmayroy183/ImgBB-Image-Uploading-In-Python.git
   ```
   
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   
3. Run the application:
   ```
   python main.py
   ```

## Usage

1. **User Application**:
   - Launch the application and select the option to upload images.
   - Choose images from your local directory.
   - Click 'Upload' to send the selected images to ImgBB.

2. **Premium Account Token Generator**:
   - Access the token generator section.
   - Input required details to generate a premium account token.

3. **Admin Panel**:
   - Log in to the admin panel using appropriate credentials.
   - View uploads, manage users, and perform admin actions.

## Screenshots

![Screenshot 1](screenshots/screenshot1.png)
*Caption for screenshot 1.*

![Screenshot 2](screenshots/screenshot2.png)
*Caption for screenshot 2.*

## Technologies Used

- Python
- Tkinter
- SQLite (or specify your local database system)
- ImgBB API (provide link if applicable)
- Other dependencies listed in `requirements.txt`

## Contributing

Contributions are welcome! If you'd like to contribute:
- Fork the repository
- Create your feature branch (`git checkout -b feature/your-feature`)
- Commit your changes (`git commit -am 'Add some feature'`)
- Push to the branch (`git push origin feature/your-feature`)
- Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
