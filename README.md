# Nagpur University Faculty Management System

Welcome to the **Nagpur University Faculty Management System**, a Python-based application designed to manage faculty details, generate resumes, and provide an efficient interface for department and faculty data management. This project is built using Tkinter for the GUI, MySQL for database management, and FPDF for PDF generation.

## Author
- **Name**: Amogh Lanjewar
- **Website**: [https://amoghlanjewar.github.io](https://amoghlanjewar.github.io)
- **Email**: [amoghlanjewar@gmail.com](mailto:amoghlanjewar@gmail.com)

## License
This project is licensed under the **MIT License**. See the [LICENSE](#License) section below for details.

## Overview
The Nagpur University Faculty Management System allows users to:
- Manage department and subfield details.
- Add, update, delete, and search faculty records.
- Generate professional PDF resumes for faculty members.
- View and edit educational qualifications, professional experience, and publications.

This application is ideal for academic institutions or administrative teams looking to streamline faculty data management.

## Features
- **Department Management**: Add and manage departments with their shortforms and subfields.
- **Faculty Management**: Add faculty details including personal information, contact details, and additional notes.
- **Subdetails Management**: Track education, experience, and publications with an intuitive interface.
- **Search Functionality**: Search faculty by name or ID with real-time results.
- **Resume Generation**: Generate customizable PDF resumes for selected faculty members.
- **Zoom Support**: Adjust font size using Ctrl + Mouse Wheel for better accessibility.
- **Data Validation**: Ensures valid input for email, contact number (e.g., +91-1234567890), and year (e.g., 2002).
- **User-Friendly Interface**: Built with Tkinter, featuring a tabbed layout and styled widgets.

## Prerequisites
Before running the application, ensure you have the following installed:
- **Python 3.x**
- **MySQL Server** (for database connectivity)
- Required Python libraries:
  - `tkinter` (usually included with Python)
  - `mysql-connector-python`
  - `fpdf`
  - `tkcalendar`

Install the dependencies using pip:
```bash
pip install mysql-connector-python fpdf tkcalendar
```

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/amoghlanjewar/nagpur-university-faculty-management.git
   cd nagpur-university-faculty-management
   ```

2. **Set Up the Database**:
   - Install and start MySQL Server.
   - Create a database named `resume`:
     ```sql
     CREATE DATABASE resume;
     ```
   - Create the necessary tables by running the following SQL commands:
     ```sql
     USE resume;

     CREATE TABLE departments (
         id INT AUTO_INCREMENT PRIMARY KEY,
         department_name VARCHAR(255) NOT NULL,
         short_code VARCHAR(10) NOT NULL
     );

     CREATE TABLE subfields (
         id INT AUTO_INCREMENT PRIMARY KEY,
         department_id INT,
         subfield_name VARCHAR(255),
         FOREIGN KEY (department_id) REFERENCES departments(id)
     );

     CREATE TABLE faculty (
         faculty_id VARCHAR(20) PRIMARY KEY,
         salutation VARCHAR(10),
         name VARCHAR(255) NOT NULL,
         department_id INT,
         subfield_id INT,
         type_of_faculty VARCHAR(100),
         email VARCHAR(255),
         google_scholar_link VARCHAR(255),
         orcid VARCHAR(50),
         linkedin VARCHAR(255),
         website VARCHAR(255),
         contact_no VARCHAR(15),
         objective TEXT,
         research_interest TEXT,
         professional_affiliation TEXT,
         awards TEXT,
         current_status TEXT,
         FOREIGN KEY (department_id) REFERENCES departments(id),
         FOREIGN KEY (subfield_id) REFERENCES subfields(id)
     );

     CREATE TABLE education (
         id INT AUTO_INCREMENT PRIMARY KEY,
         faculty_id VARCHAR(20),
         degree VARCHAR(255),
         institution VARCHAR(255),
         year VARCHAR(4),
         FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
     );

     CREATE TABLE experience (
         id INT AUTO_INCREMENT PRIMARY KEY,
         faculty_id VARCHAR(20),
         title VARCHAR(255),
         place VARCHAR(255),
         duration VARCHAR(50),
         FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
     );

     CREATE TABLE publications (
         id INT AUTO_INCREMENT PRIMARY KEY,
         faculty_id VARCHAR(20),
         title VARCHAR(255),
         journal VARCHAR(255),
         year VARCHAR(4),
         doi VARCHAR(100),
         publication_link VARCHAR(255),
         FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
     );
     ```
   - Update the database connection details in the `DatabaseHandler` class (`host`, `user`, `password`, `database`) in the script to match your MySQL setup.

3. **Run the Application**:
   - Execute the script:
     ```bash
     python main.py
     ```
   - Ensure all dependencies are installed and the database is running.

## Usage
1. **Department Management Tab**:
   - Enter the department name, shortform, and subfields (comma-separated).
   - Click "Save Department" to add a new department.

2. **Faculty Management Tab**:
   - Fill in the basic information (e.g., name, contact, email).
   - Add education, experience, and publications in the respective sub-tabs.
   - Click "Save Faculty" to store the record and generate a faculty ID.

3. **View/Search/Resume Tab**:
   - Search for faculty by name or ID.
   - Select a faculty member to update, delete, or generate a resume.
   - Use "Generate Resume PDF" to create a PDF file for the selected faculty.

4. **Zoom Functionality**:
   - Use `Ctrl + Mouse Wheel` to zoom in or out for better readability.

## Input Validation
- **Email**: Must follow a valid email format (e.g., `user@example.com`).
- **Contact Number**: Must be in the format `+XX-XXXXXXXXXX` (e.g., `+91-1234567890`), where `XX` is the country code and followed by a 10-digit number.
- **Year**: Must be a 4-digit number between 1900 and the current year (e.g., `2002`).

## Troubleshooting
- **Database Connection Issues**: Ensure MySQL is running and credentials are correct.
- **Missing Dependencies**: Verify all required libraries are installed.
- **PDF Generation Errors**: Check if the `fpdf` library is properly installed and writable directory permissions.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m "Description of changes"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## Issues
If you encounter any bugs or have feature requests, please open an issue on the [GitHub Issues page](https://github.com/yourusername/nagpur-university-faculty-management/issues).

## License
```
MIT License

Copyright (c) 2025 Amogh Lanjewar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments
- Thanks to the open-source community for tools like Tkinter, MySQL, and FPDF.
- Inspired by the need for efficient faculty management in academic institutions.

---


