import sys

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
    grades = {}

    conn.commit()
    conn.close()
    return


if __name__ == "__main__":
    main(sys.argv)