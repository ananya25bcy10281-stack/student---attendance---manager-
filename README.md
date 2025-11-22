# student---attendance---manager-
"Flask-based Student Attendance &amp; Performance Manager"
# Student Management System

A Flask-based web application for managing student records, attendance tracking, and marks management with separate dashboards for teachers and students.

## Features

### Teacher Features
- Secure login authentication
- Add and manage student records
- Mark daily attendance
- Record and manage student marks by subject
- View comprehensive reports with attendance percentages
- Attendance visualization via chart API

### Student Features
- Login using roll number
- View personal dashboard
- Access attendance and marks records

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Authentication**: Werkzeug password hashing
- **Session Management**: Flask sessions

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Steps

1. **Clone or download the project files**

2. **Install required dependencies**
```bash
pip install flask werkzeug
```

3. **Run the application**
```bash
python app.py
```

4. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:5000/`

## Database Structure

The application automatically creates a SQLite database (`database.db`) with the following tables:

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password`: Hashed password
- `role`: User role (teacher/student)

### Students Table
- `id`: Primary key
- `name`: Student name
- `roll`: Unique roll number

### Attendance Table
- `id`: Primary key
- `roll`: Student roll number
- `date`: Attendance date
- `status`: Present/Absent

### Marks Table
- `id`: Primary key
- `roll`: Student roll number
- `subject`: Subject name
- `marks`: Marks obtained

## Default Credentials

**Teacher Login:**
- Username: `teacher1`
- Password: `teacher123`

**Student Login:**
- Use roll number (must be added by teacher first)

## Usage Guide

### For Teachers

1. **Login** using teacher credentials at `/teacher-login`
2. **Add Students** via the "Add Student" option
3. **Mark Attendance** daily for all students
4. **Enter Marks** by subject for assessments
5. **View Reports** to see attendance percentages and student performance

### For Students

1. **Login** using your roll number at `/student-login`
2. **View Dashboard** to see your attendance and marks

## API Endpoints

### Public Routes
- `GET /` - Home page
- `GET/POST /teacher-login` - Teacher authentication
- `GET/POST /student-login` - Student authentication

### Teacher Routes (Authentication Required)
- `GET /teacher-dashboard` - Teacher dashboard
- `GET/POST /add-student` - Add new student
- `GET /view-students` - View all students
- `GET/POST /attendance` - Mark attendance
- `GET/POST /marks` - Enter marks
- `GET /teacher-report` - View comprehensive report
- `GET /attendance-chart-api` - Get attendance data for charts (JSON)

### Student Routes (Authentication Required)
- `GET /student-dashboard` - Student dashboard

### General Routes
- `GET /logout` - Clear session and logout

## Security Notes

⚠️ **Important**: This is a basic implementation for educational purposes. For production use, consider:

- Changing the `app.secret_key` to a secure random value
- Using environment variables for sensitive configuration
- Implementing HTTPS
- Adding CSRF protection
- Enhancing input validation
- Implementing rate limiting
- Using a production-grade database (PostgreSQL/MySQL)
- Adding proper error handling and logging

## Project Structure

```
student-management-system/
│
├── app.py                      # Main application file
├── database.db                 # SQLite database (auto-generated)
│
└── templates/                  # HTML templates
    ├── home.html
    ├── teacher_login.html
    ├── student_login.html
    ├── teacher_dashboard.html
    ├── student_dashboard.html
    ├── add_student.html
    ├── view_students.html
    ├── attendance.html
    ├── marks.html
    └── report_teacher.html
```

## Troubleshooting

**Database not found error:**
- The database is created automatically on first run
- Ensure write permissions in the project directory

**Login issues:**
- Verify credentials match the default or added users
- Check if the database was initialized properly

**Port already in use:**
- Change the port in `app.run()` to another value (e.g., `app.run(port=5001, debug=True)`)

## Future Enhancements

- Student self-registration
- Email notifications
- Export reports to PDF/Excel
- Multi-teacher support
- Parent login portal
- Assignment management
- Timetable management

## License

This project is open-source and available for educational purposes.

## Support

For issues or questions, please review the code documentation or create an issue in the project repository.
