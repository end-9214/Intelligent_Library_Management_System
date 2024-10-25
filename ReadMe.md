# IntelliLib - Intelligent Library Management System

📚 **IntelliLib** is an intelligent library management system designed to help users manage library activities such as book issuance, checking book availability, managing due dates, and calculating fines. This GUI-based application uses Python's Tkinter for the user interface and MongoDB for the backend database.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Technologies Used](#technologies-used)

## Features
- 📚 **Check Books Issued**: View the books that have been issued to a student.
- ⏳ **Check Deadlines**: View overdue books and their due dates.
- 💸 **Check Fine**: Calculate fines for overdue books.
- 📚 **Issue Book**: Issue books to a student by entering their enrollment number.
- 📦 **Return Book**: Return books and calculate fines if applicable.

## Installation

### Prerequisites
- **Python 3.7 or higher**: The application requires Python to run.
- **MongoDB Atlas**: A MongoDB cluster to store the data. You can use MongoDB Atlas to create a free-tier database.

### Steps
1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/Intelligent_Library_Management_System.git
    cd Intelligent_Library_Management_System
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:
    - **Windows**:
      ```sh
      .\venv\Scripts\activate
      ```
    - **Linux/macOS**:
      ```sh
      source venv/bin/activate
      ```

4. **Install the Required Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Create a `.env` File**:
   - Create a `.env` file in the root directory.
   - Add the MongoDB URI to connect to your MongoDB Atlas instance:
     ```plaintext
     MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/intellib?retryWrites=true&w=majority
     ```
   Replace `<username>` and `<password>` with your MongoDB credentials.

6. **Run the Application**:
    ```sh
    python main.py
    ```

## Usage

1. **Launching the Application**:
    - After running `main.py`, the application window will open.
    - The application is designed with a dark color scheme similar to Discord for better aesthetics.

2. **Features**:
    - **Enter Enrollment Number**: Enter the student's enrollment number to perform different operations.
    - **Check Books Issued**: Click on 📚 **Check Books Issued** to view books issued to the student.
    - **Check Deadlines**: Click on ⏳ **Check Deadlines** to view overdue books.
    - **Check Fine**: Click on 💸 **Check Fine** to calculate the fine for overdue books.
    - **Issue Book**: Click on 📚 **Issue Book** to issue a book to the student.
    - **Return Book**: Click on 📦 **Return Book** to return a book and calculate the fine if applicable.

## Environment Variables

The application uses a `.env` file to securely store sensitive information. Make sure to add the following information to your `.env` file:

```plaintext
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/intellib?retryWrites=true&w=majority
```

## Technologies Used
- **Python**: Core programming language used.
- **Tkinter**: GUI library used to create the interface.
- **MongoDB Atlas**: Database used to store student and book records.
- **Pymongo**: Python library to interact with MongoDB.
- **dotenv**: Used for environment variable management.

