import sys
import sqlite3 as sql

def comparisonMajor(c):
	return

def comparison101To124():
	return

def comparisonOnlineVsF2F():
	return

def creditsForGraduation():
	return

def main(argv):
	if len(argv) < 1:
		print ("Please enter parameters as: <program_name>")
		return

	# Import the cs450 database
    conn = sql.connect('cs450.db')

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