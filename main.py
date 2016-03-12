########################################################
# Program:
#   main.py
# Author:
#   Samuel Hibbard, Daniel Miller, Daniel Marsden
# Summary:
#   This will be our main project for cs450.
########################################################

import sys
import sqlite3 as sql
import xlrd

###########################################
# check_student
###########################################
def check_student(id, c):
    # Check the student if it already has been inserted
    student = c.execute("SELECT id FROM students WHERE id = ?", (id,))

    return student.fetchone() != None

###########################################
# check_grade
###########################################
def check_grade(c, id, course_sec, term):
    grade = c.execute("SELECT student_id, course_sec, term FROM grades WHERE student_id = ? AND course_sec = ? AND term = ?", (id, course_sec, term))

    return grade.fetchone() != None

###########################################
# insert_into_students
#   This will insert new rows into the
#       students table.
###########################################
def insert_into_students(data, c):
    # Start the for loop
    course_sec = ''
    id = -1
    for row_index in range(1, data.nrows):
        # Grab the row
        row = data.row_values(row_index)

        duplicate = True

        # Replace empty strings with None values
        #  this is equivalent to NULL
        row = [None if not c else c for c in row]

        if row[0] is not None:
            # Check if the id is different. If so change to the new id
            if id == -1 or id != row[0]:
                student = row[:-5]
                id = student[0]

                duplicate = check_student(id, c)

                if not duplicate:
                    # Insert into the table
                    c.execute('''INSERT INTO students
                                (
                                  id,
                                  gender,
                                  ethnicity,
                                  country,
                                  birth_year,
                                  martial_status,
                                  served_mission,
                                  subprogram_code,
                                  classification,
                                  track,
                                  act_composite,
                                  act_english,
                                  act_math,
                                  act_reading,
                                  act_science,
                                  total_act,
                                  has_transfer_credit,
                                  transfer_credit,
                                  high_school_gpa,
                                  cumulative_gpa,
                                  major,
                                  minor,
                                  emphasis,
                                  cluster
                                )
                                VALUES
                                (
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?
                                );''',
                                tuple(student))
                else:
                    print("Duplicate student id " + id)

            # Insert the grades
            row = row[-5:]

            # Append the id
            row.append(id)

            duplicate = check_grade(c, id, row[0], row[3])

            if not duplicate:
                # Create a new insert statement
                c.execute('''INSERT INTO grades
                            (
                              course_sec,
                              credits,
                              sec_subprogram,
                              term,
                              grade,
                              student_id
                            )
                            VALUES
                            (
                              ?,
                              ?,
                              ?,
                              ?,
                              ?,
                              ?
                            );''',
                            tuple(row))
            else:
                print("Duplicate grade for student id " + id)
    return

###########################################
# insert_into_majors
#   This will insert new rows into the majors
#       table.
###########################################
def insert_into_majors(data, c, semester):
    # Start the for loop
    course_sec = ''
    for row_index in range(1, data.nrows):
        # Grab the row
        row = data.row_values(row_index)

        # Replace empty strings with None values
        #  this is equivalent to NULL
        row = [None if not c else c for c in row]

        # Save the course value. This will let us know when we have change
        # course sections.
        if row[1] is not None:
            if row[0] is not None:
                course_sec = row[0]

            # Create the insert statment
            c.execute('''INSERT INTO majors
                        (
                          major,
                          course_sec,
                          student_id,
                          semester
                        )
                        VALUES
                        (
                          ?,
                          ?,
                          ?,
                          ?
                        );''',
                        (course_sec,
                        row[1],
                        row[2],
                        semester))
    return

###############################################
# main
#   Driver program.
###############################################
def main(argv):
    # Grab the arguments for the file and the semester name
    if len(argv) < 2:
        print("ERROR: You must pass these arguments <file>")
    else:
        file = argv[1]
        # table_name = argv[2]

        if len(argv) > 3:
            semester = argv[3]

        # Import the cs450 database
        conn = sql.connect('cs450.db')

        # Create the cursor that will do all the statements
        c = conn.cursor()

        # Grab the file the from the specified argument
        book = xlrd.open_workbook(file)

        first_sheet = book.sheet_by_index(0)

        # Call the function that will insert into the correct database
        # if table_name == 'majors':
        #     insert_into_majors(first_sheet, c, semester)
        insert_into_students(first_sheet, c)

        conn.commit()
        conn.close()
    return


if __name__ == "__main__":
    main(sys.argv)