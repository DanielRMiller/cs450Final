library("RSQLite")
library(cluster)

# connect to the sqlite file
sqlite <- dbDriver("SQLite")
con = dbConnect(sqlite, "cs450.db")

# get a list of all tables
alltables = dbListTables(con)

# get the populationtable as a data.frame
query = paste("SELECT ",
                "s.id AS student, ",
                "AVG(g.grade_point) AS grade_point, ",
                "CASE WHEN s.major LIKE '440%' THEN 1 ELSE 0 END AS CS, ",
                "CASE WHEN s.major LIKE '445%' THEN 1 ELSE 0 END AS EE, ",
                "CASE WHEN s.major LIKE '443%' THEN 1 ELSE 0 END AS SE, ",
                "CASE WHEN s.major LIKE '450%' THEN 1 ELSE 0 END AS CE, ",
                "CASE WHEN s.major LIKE '681%' THEN 1 ELSE 0 END AS CIT, ",
                "s.cumulative_gpa, ",
                "s.high_school_gpa ",
              "FROM students AS s ",
              "LEFT JOIN grades AS g ",
              "ON g.student_id = s.id ",
              "WHERE grade_point IS NOT NULL ",
              "AND (s.major LIKE '440%' ",
              "OR s.major LIKE '450%' ",
              "OR s.major LIKE '445%' ",
              "OR s.major LIKE '681%' ",
              "OR s.major LIKE '443%') ",
              "AND s.cumulative_gpa != 'NA' AND s.high_school_gpa != 'NA' ",
              "GROUP BY s.id", sep="")

data = dbGetQuery(con, query)

samp2 <- data[,-1]
rownames(samp2) <- data[,1]

data_scaled = scale(samp2)

for (i in 1:25) {
  myClusters = kmeans(data_scaled, i)
  clusplot(data_scaled, myClusters$cluster, color=TRUE, shade=TRUE, labels=2, lines=0)
}