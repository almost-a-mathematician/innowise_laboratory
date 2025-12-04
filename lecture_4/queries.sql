-- Table: students
-- Stores student information including personal data
-- Constraints:
--   * full_name must be unique
--   * birth_year cannot exceed 2025 

CREATE TABLE "students" (
    "id" INTEGER,
    "full_name" TEXT UNIQUE,
    "birth_year" INTEGER,
    PRIMARY KEY ("id"),
    CHECK ("birth_year" <= 2025)
);

-- Index: idx_students_birth_year
-- Improves performance for queries filtering students by birth year

CREATE INDEX idx_students_birth_year ON students (birth_year);

-- Table: grades
-- Stores student's grades for different subjects
-- Relationships:
--   * FK student_id references students(id) 
-- Constraints:
--   * grade must be between 1 and 100 

CREATE TABLE "grades" (
    "id" INTEGER,
    "student_id" INTEGER,
    "subject" TEXT,
    "grade" INTEGER,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("student_id") REFERENCES "students" ("id"),
    CHECK (1 <= grade <= 100)
);

-- Index: idx_grades_student_id
-- Improves performance for JOIN operations between students and grades tables

CREATE INDEX idx_grades_student_id ON grades (student_id);

-- Index: idx_grades_subject
-- Improves performance for grouping and filtering by subject

CREATE INDEX idx_grades_subject ON grades (subject);

-- Index: idx_grades_grade
-- Improves performance for filtering grades by numeric range

CREATE INDEX idx_grades_grade ON grades (grade);


-- Insert sample students

INSERT INTO "students" ("full_name", "birth_year") VALUES
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

-- Insert sample grades

INSERT INTO "grades" ("student_id", "subject", "grade") VALUES
(1, 'Math', 88),
(1, 'English', 92),
(1, 'Science', 85),
(2, 'Math', 75),
(2, 'History', 83),
(2, 'English', 79),
(3, 'Science', 95),
(3, 'Math', 91),
(3, 'Art', 89),
(4, 'Math', 84),
(4, 'Science', 88),
(4, 'Physical Education', 93),
(5, 'English', 90),
(5, 'History', 85),
(5, 'Math', 88),
(6, 'Science', 72),
(6, 'Math', 78),
(6, 'English', 81),
(7, 'Art', 94),
(7, 'Science', 87),
(7, 'Math', 90),
(8, 'History', 77),
(8, 'Math', 83),
(8, 'Science', 80),
(9, 'English', 96),
(9, 'Math', 89),
(9, 'Art', 92);


-- Query 1: Get all grades for a specific student
-- Returns: student name, subject and grade for each subject

SELECT
    students.full_name,
    grades.subject,
    grades.grade
FROM
    students
INNER JOIN
    grades ON students.id = grades.student_id
WHERE
    students.full_name = 'Alice Johnson';

-- Query 2: Calculate average grade per student
-- Returns: student id, name and their average grade (rounded to 2 decimals)

SELECT
    students.id,
    students.full_name,
    round(avg(grades.grade), 2) AS average_grade
FROM
    grades
INNER JOIN
    students ON grades.student_id = students.id
GROUP BY
    grades.student_id;

-- Query 3: Find all students born after 2004
-- Returns: student name and birth year

SELECT
    students.full_name,
    students.birth_year
FROM
    students
WHERE
    students.birth_year > 2004;

-- Query 4: Calculate average grade per subject
-- Returns: subject name and average grade across all students

SELECT
    grades.subject,
    round(avg(grades.grade), 2) AS average_grade
FROM
    grades
GROUP BY
    grades.subject;

-- Query 5: Get top 3 performers
-- Returns: student id, name and average grade

SELECT
    students.id,
    students.full_name,
    round(avg(grades.grade), 2) AS average_grade
FROM
    grades
INNER JOIN
    students ON grades.student_id = students.id
GROUP BY
    grades.student_id, students.full_name
ORDER BY
    average_grade DESC
LIMIT 3;

-- Query 6: Get students with a scored below 80 in any subject
-- Returns: student id, name, subject and grade 

SELECT
    students.id,
    students.full_name,
    grades.subject,
    grades.grade
FROM
    students
INNER JOIN
    grades ON students.id = grades.student_id
WHERE
    grades.grade < 80
GROUP BY
    students.id;
