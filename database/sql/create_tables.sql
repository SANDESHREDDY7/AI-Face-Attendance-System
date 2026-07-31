-- ==========================================
-- AI Face Attendance System Database Schema
-- ==========================================

-- USERS TABLE
CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- STUDENTS TABLE
CREATE TABLE students (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    admission_number VARCHAR(30) UNIQUE,
    student_name VARCHAR(100) NOT NULL,
    class VARCHAR(20) NOT NULL,
    section VARCHAR(10) NOT NULL,
    gender VARCHAR(10),
    dob DATE,
    parent_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    photo1 TEXT,
    photo2 TEXT,
    photo3 TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FACE ENCODINGS TABLE
CREATE TABLE face_encodings (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    photo_number INT NOT NULL,
    encoding JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ATTENDANCE SESSIONS TABLE
CREATE TABLE attendance_sessions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    class VARCHAR(20) NOT NULL,
    section VARCHAR(10) NOT NULL,
    uploaded_image TEXT,
    attendance_date DATE NOT NULL,
    attendance_time TIME NOT NULL,
    total_students INT DEFAULT 0,
    present_count INT DEFAULT 0,
    absent_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ATTENDANCE TABLE
CREATE TABLE attendance (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES attendance_sessions(id) ON DELETE CASCADE,
    student_id BIGINT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL,
    confidence DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INDEXES
CREATE INDEX idx_students_roll ON students(roll_number);
CREATE INDEX idx_students_class_section ON students(class, section);
CREATE INDEX idx_face_student_id ON face_encodings(student_id);
CREATE INDEX idx_attendance_student_id ON attendance(student_id);
CREATE INDEX idx_attendance_session_id ON attendance(session_id);