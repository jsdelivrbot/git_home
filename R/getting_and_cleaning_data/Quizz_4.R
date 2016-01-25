setwd("/home/wenduowang/git/R/getting_and_cleaning_data")

library(dplyr)

idaho <- tbl_df(read.csv("idaho.csv"))
(strsplit(names(idaho), split=c("wgtp")))[123]

GDP <- tbl_df(read.csv("GDP.csv", na.strings=c("", ".."), skip=4))
GDP <- select(GDP, ranking=X.1, countrycode=X, country=X.3, gdp=X.4)
GDP$gdp <- gsub(pattern=",| *", replacement="", GDP$gdp)
GDP <- mutate(GDP, ranking=as.numeric(as.character(ranking)), gdp=as.numeric(as.character(gdp)))
GDP <- GDP[!is.na(GDP$ranking),]
print(mean(GDP$gdp))
print(
  length(
    grep("^United", GDP$country)
  )
)

education <- tbl_df(read.csv("education.csv", na.strings=c("")))

GDP_education <- merge(GDP, education, by.x="countrycode", by.y="CountryCode")

GDP_education[
  grep("[Ff][Ii][Ss][Cc][Aa][Ll].*[Yy][Ee][Aa][Rr].*[Ee][Nn][Dd].*[Jj][Uu][Nn][Ee]", GDP_education$Special.Notes),
]

library(quantmod)
amzn = getSymbols("AMZN",auto.assign=FALSE)
sampleTimes = index(amzn)
library(lubridate)
length(
  subset(sampleTimes, year(sampleTimes)==2012 & weekdays(sampleTimes)=="Monday")
)

