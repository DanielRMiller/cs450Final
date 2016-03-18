import sys
import sqlite3 as sql
import math
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

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

###########################################
# growthRate
###########################################
def growthRate(c):
	students = c.execute('''
		SELECT term, COUNT(term)
		FROM grades
		WHERE (term LIKE 'WI%' OR term LIKE 'FA%' OR term LIKE 'SP%')
		AND (term NOT LIKE '%08' OR term NOT LIKE '%09')
		GROUP BY term
		''').fetchall()

	# students = np.array(students)

	terms = {'FA' : 0, 'WI' : 3, 'SP' : 6}
	array = []
	for s in students:
		array.append([str(s[0][2:4]) + str(terms[s[0][0:2]]), s[1]])

	array = sorted(array)

	new_array = [i for i in array if int(i[0]) >= 100]

	x = [int(i[0]) for i in new_array]
	y = [int(i[1]) for i in new_array]

	plt.plot(x, y, 'ro', x, y, 'k')
	plt.plot(x, np.poly1d(np.polyfit(x, y, 3))(x))
	plt.show()

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
	# comparisonOnlineVsF2F(c)

	# Growth Rate
		# Statistical
	growthRate(c)

	# ##ML
	# Student will go over credit limit # NOT ENOUGH INFO
		# Question for Brother Burton
	# Predict student's GPA for a specific class
		# Neural Network
		# Decision Tree

	# Lift between elective classes, take the class based off grade,
		# Association Rule Mining
	# Cluster Students
		# Clustering, kNN

	conn.commit()
	conn.close()
	return

if __name__ == '__main__':
	main(sys.argv)