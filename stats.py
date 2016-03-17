import sys
import sqlite3 as sql
import math
import numpy as np

def comparisonMajor(c):
	student_grades = c.execute('''
		SELECT	s.id,
				s.major,
				g.grade_point
		FROM grades AS g
		LEFT JOIN students AS s
		ON s.id = g.student_id
		WHERE grade_point IS NOT null
			AND (s.major LIKE '440%'	-- CS
			OR s.major LIKE '450%'  	-- CE
			OR s.major LIKE '445%'  	-- EE
			OR s.major LIKE '681%'  	-- CIT
			OR s.major LIKE '443%')		-- SE
		''').fetchall()

	majors = c.execute('''
			SELECT major
			FROM students
			WHERE major LIKE '440%'	-- CS
			OR major LIKE '450%'  	-- CE
			OR major LIKE '445%'  	-- EE
			OR major LIKE '681%'  	-- CIT
			OR major LIKE '443%'
			GROUP BY major
		''').fetchall()

	majors_grades =	[]
	majors_grades.append([student[2] for student in student_grades if student[1].startswith('440')])
	majors_grades.append([student[2] for student in student_grades if student[1].startswith('443')])
	majors_grades.append([student[2] for student in student_grades if student[1].startswith('445')])
	majors_grades.append([student[2] for student in student_grades if student[1].startswith('450')])
	majors_grades.append([student[2] for student in student_grades if student[1].startswith('681')])

	major_stds = []
	major_means = []

	for major_grades in majors_grades:
		student_stds = []
		major_grades = sorted(major_grades)
		major_stds.append( np.std(major_grades) )
		major_means.append( np.mean(major_grades) )

	print('Majors: ', majors)
	print ('Major STDs: ', major_stds)
	print ('Major Means: ', major_means)
	return

def comparison101To124(c):
	cs124 = c.execute('''
		SELECT g.grade_point
		FROM grades AS g
		LEFT JOIN students AS s
		ON s.id = g.student_id
		WHERE g.course_sec LIKE "CS   124%"
			AND g.grade_point IS NOT NULL
		''').fetchall()

	cs101 = c.execute('''
		SELECT g.grade_point
		FROM grades AS g
		LEFT JOIN students AS s
		ON s.id = g.student_id
		WHERE g.course_sec LIKE "CS   101%"
			AND g.grade_point IS NOT NULL
		''').fetchall()

	print('cs124 Mean and STDs', np.mean(cs124), np.std(cs124))
	print('cs101 Mean and STDs', np.mean(cs101), np.std(cs101))
	return

def comparisonOnlineVsF2F(c):
	online = c.execute('''
		SELECT grade_point
		FROM grades
		WHERE sec_subprogram = 'ONLN' AND grade_point IS NOT NULL
		''').fetchall()

	day = c.execute('''
		SELECT grade_point
		FROM grades
		WHERE sec_subprogram = 'DAY' AND grade_point IS NOT NULL
		''').fetchall()

	print('ONLINE Mean and STDs', np.mean(online), np.std(online))
	print('DAY Mean and STDs', np.mean(day), np.std(online))
	return

def creditsForGraduation(c):
	return

def main(argv):
	if len(argv) < 1:
		print ("Please enter parameters as: <program_name>")
		return

	# Import the cs450 database
	conn = sql.connect('db/cs450.db')

	# Create the cursor that will do all the statements
	c = conn.cursor()

	# ##STATS
	# When do students decide to be a CSEE Major
		# PROBLEM: We do not have any about major by term
	# studentDecison(c)


	# Performance CS vs EE vs CE vs SE vs ....
	# comparisonMajor(c)

	# Performance for students taking 101 before 124
	# comparison101To124(c)

	# Performance Online vs F2F
	comparisonOnlineVsF2F(c)

	# Overall problem of credits for graduation
		# Credits before each class taken?
	creditsForGraduation(c)

	# ##ML
	# Student will go over credit limit # NOT ENOUGH INFO
		# Question for Brother Burton
	# Predict student's GPA for a specific class
		# Neural Network

	# Growth Rate
		# Statistical
	# Lift between elective classes
		# Association Rule Mining
	# Cluster Students
		# Clustering, kNN

	conn.commit()
	conn.close()
	return

if __name__ == '__main__':
	main(sys.argv)