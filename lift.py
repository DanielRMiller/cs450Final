import sqlite3 as sql

def main():

    conn = sql.connect('db/cs450.db')

    c = conn.cursor()

    data =    c.execute('''SELECT s.id,
                 SUBSTR(g.course_sec || g.course_sec, 1, 8) AS course
                 FROM grades AS g
                 LEFT JOIN students AS s
                 ON s.id = g.student_id
                 WHERE s.major LIKE '440%' AND
                 (course_sec LIKE 'CS   490r%' OR
                 course_sec LIKE 'CS   450%' OR
                 course_sec LIKE 'CS   480%' OR
                 course_sec LIKE 'CS   460%' OR
                 course_sec LIKE 'CS   371%' OR
                 course_sec LIKE 'CS   312%' OR
                 course_sec LIKE 'CS   313%' OR
                 course_sec LIKE 'ECEN 361%' OR
                 course_sec LIKE 'ECEN 260%' OR
                 course_sec LIKE 'CIT  225%')
                 AND g.grade_point >= 4
                 AND g.grade_point IS NOT NULL''').fetchall()

    print(data)



if __name__ == '__main__':
	main()