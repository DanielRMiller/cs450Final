library("RSQLite")
library(arules)

# connect to the sqlite file
sqlite <- dbDriver("SQLite")
con = dbConnect(sqlite, "cs450.db")

# get a list of all tables
alltables = dbListTables(con)

query = paste("SELECT s.id, ",
             "SUBSTR(g.course_sec || g.course_sec, 1, 8) AS course ",
             "FROM grades AS g ",
             "LEFT JOIN students AS s ",
             "ON s.id = g.student_id ",
             "WHERE s.major LIKE '440%' AND ",
             "(course_sec LIKE 'CS   490r%' OR ",
             "course_sec LIKE 'CS   450%' OR ",
             "course_sec LIKE 'CS   480%' OR ",
             "course_sec LIKE 'CS   460%' OR ",
             "course_sec LIKE 'CS   371%' OR ",
             "course_sec LIKE 'CS   312%' OR ",
             "course_sec LIKE 'CS   313%' OR ",
             "course_sec LIKE 'ECEN 361%' OR ",
             "course_sec LIKE 'ECEN 260%' OR ",
             "course_sec LIKE 'CIT  225%') ",
             "AND g.grade_point >= 4 ",
             "AND g.grade_point IS NOT NULL", sep="")

sqldata = dbGetQuery(con, query)
data = aggregate(course ~ id, sqldata, FUN=paste)

data = data[,2]
names(data) <- paste("Student", c(1:222), sep="")

listData <- list()
for (i in 1:length(data)) {
    listData[[i]] <- as.character(data[[i]][!duplicated(data[[i]])])
}

trans <- as(listData, "transactions")
rules <- apriori(data = trans,
                 parameter = list(support = 0.01,
                                  confidence = 0.0,
                                  minlen = 2))

inspect(sort(rules, by = "lift", decreasing = TRUE))