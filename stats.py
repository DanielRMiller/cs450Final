import sys
import sqlite3 as sql
import math
import numpy as np

def comparisonMajor(c):
	# major_averages = c.execute('''
	# 	SELECT	s.major,
	# 			AVG(g.grade_point)
	# 	FROM grades AS g
	# 	LEFT JOIN students AS s
	# 	ON s.id = g.student_id
	# 	WHERE grade_point IS NOT null
	# 		AND (s.major LIKE '440%'	-- CS 
	# 		OR s.major LIKE '450%'  	-- CE
	# 		OR s.major LIKE '445%'  	-- EE
	# 		OR s.major LIKE '681%'  	-- CIT
	# 		OR s.major LIKE '443%')		-- SE
	# 	GROUP BY s.major
	# 	''').fetchall() # FETCH ALL SO WE ARE GETTING DATA NOT CURSOR
	# # print ('Major Averages: \n', major_averages)

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
	# print ('Student Grades: \n', student_grades)
	
	majors_grades=	[]
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

	print ('Major STDs: ', major_stds)
	print ('Major Means: ', major_means)
	return

def comparison101To124(c):
	return

def comparisonOnlineVsF2F(c):
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
	comparisonMajor(c)

	# Performance for students taking 101 before 124
	comparison101To124(c)

	# Performance Online vs F2F
	comparisonOnlineVsF2F(c)

	# Overall problem of credits for graduation
		# Credits before each class taken?
	creditsForGraduation(c)

	# ##ML
	# Student will go over credit limit
	# Lift between elective classes
	# Growth Rate
	# Predict student GPA
	# Cluster Students

	conn.commit()
	conn.close()
	return

if __name__ == '__main__':
	main(sys.argv)