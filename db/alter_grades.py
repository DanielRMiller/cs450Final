import sys
import sqlite3 as sql

###############################################
# main
#   Driver program.
###############################################
def main(argv):
     # Import the cs450 database
    conn = sql.connect('cs450.db')

    # Create the cursor that will do all the statements
    c = conn.cursor()

    # Create the grades object
    grade_enum = {
        'P' : 12,
        'A+' : 12,
        'A' : 12,
        'A-' : 11,
        'B+' : 10,
        'B' : 9,
        'B-' : 8,
        'C+' : 7,
        'C' : 6,
        'C-' : 5,
        'D+' : 4,
        'D' : 3,
        'F' : 0
    }

    grades = c.execute('''
        Select id, grade from grades
        ''')

    grade_points = grades.fetchall()
    for grade in grade_points:
        c.execute ('''
            Update grades Set grade_point = ? Where id = ?
            ''', (grade_enum.get(grade[1], None), grade[0]))

    conn.commit()
    conn.close()
    return


if __name__ == "__main__":
    main(sys.argv)