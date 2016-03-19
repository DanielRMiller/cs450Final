library("RSQLite")

# connect to the sqlite file
sqlite <- dbDriver("SQLite")
con = dbConnect(sqlite, "cs450.db")

# get a list of all tables
alltables = dbListTables(con)

# get the populationtable as a data.frame
query = paste("SELECT ",
                "grade_point ",
              "FROM grades ",
              ""
              "WHERE grade_point IS NOT NULL", sep="")
grades = dbGetQuery(con, query)

print(grades)

# Clear the results of the last query
dbClearResult(p3)