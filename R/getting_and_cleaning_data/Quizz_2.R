setwd("/home/wenduowang/git/R/getting_and_cleaning_data")

library(httr)
library(XML)
library(jsonlite)
myapp <- oauth_app("github", key="5693e111dab8d0fa2945", secret="e54a9f9f03ddbf9488a6edf3e2821b8f0d922419")
github_token <- oauth2.0_token(oauth_endpoints("github"), myapp)
g_token <- config(token=github_token)
#g_token <- "c2409940403443507ccc9178e10169d5516a880f"
page_content <- with_config(
  g_token,
  GET("https://api.github.com/users/jtleek/repos")
)
stop_for_status(page_content)
page_data <- fromJSON(toJSON(content(page_content)))
names(page_data)
subset(page_data, page_data$name=="datasharing")$created_at

library(sqldf)
download.file("https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Fss06pid.csv", destfile="acs.csv", method="curl")
acs <- read.table("acs.csv", header=T, sep=",")
head(acs)
sqldf("select pwgtp1 from acs where AGEP < 50")
sqldf("select * from acs")
sqldf("select pwgtp1 from acs")
sqldf("select * from acs where AGEP < 50 and pwgtp1")
x <- unique(acs$AGEP)
y <- sqldf("select distinct AGEP from acs")
sqldf("select unique AGEP from acs")
sqldf("select AGEP where unique from acs")

con <- url("http://biostat.jhsph.edu/~jleek/contact.html")
page_lines <- readLines(con, n=101, ok=T, encoding="UTF-8")
nchar(page_lines[c(10,20,30,100)])
close(con)

#library(readr)
download.file("https://d396qusza40orc.cloudfront.net/getdata%2Fwksst8110.for", destfile="data.for", method="wget")
#col.names <- paste(c("x"), 1:9, sep=""); col.names
widths <- c(10,9,4,9,4,9,4,9,4);
data_table <- read.fwf("data.for", widths=widths, skip=4)
sum(data_table[,4])
