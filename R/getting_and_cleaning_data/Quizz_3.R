setwd("/home/wenduowang/git/R/getting_and_cleaning_data/")
library(dplyr)

#Download the 2006 microdata survey about housing for the state of Idaho
download.file(url="https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Fss06hid.csv", destfile="idaho.csv", method="wget")
idaho_csv <- read.csv(file="idaho.csv")
idaho_tbl <- tbl_df(idaho_csv)
idaho_tbl %>% mutate(agricultureLogical=(ACR=="3" & AGS=="6")) %>% head(which(agricultureLogical))

library(jpeg)
download.file(url="https://d396qusza40orc.cloudfront.net/getdata%2Fjeff.jpg", destfile="instructor.jpeg", method="wget")

#education.csv
download.file(url="https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FEDSTATS_Country.csv", destfile="education.csv", method="wget")
education <- tbl_df(read.csv(file="education.csv", na.strings=c("")))
#GDP.csv
download.file(url="https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FGDP.csv", destfile="GDP.csv", method="wget")
GDP <- tbl_df(read.csv(file="GDP.csv", na.strings=c("", "..")))
GDP <- GDP %>%
  select(Ranking=Gross.domestic.product.2012, CountryCode=X, Country=X.2, GDP_MUSD=X.3) %>%
  mutate(Ranking=as.numeric(as.character(Ranking)))
#removes unranked countries
GDP <- GDP[
  !is.na(GDP$Ranking),
]
GDP <- arrange(GDP, desc(Ranking))
sum(GDP$CountryCode %in% education$CountryCode, na.rm=T)
#select shared countries between GDP and education
education <- education[education$CountryCode %in% GDP$CountryCode,]
education <- select(education, CountryCode, income_group=Income.Group, Region)
GDP <- GDP[GDP$CountryCode %in% education$CountryCode,]
#merge GDP and education
GDP_education <- merge(GDP, education, by.x="CountryCode", by.y="CountryCode", all=T)
GDP_education_group <- group_by(GDP_education, income_group)
summarise(GDP_education_group, list(income_group))
summarise(GDP_education_group, average_ranking=mean(Ranking))

library(Hmisc)
GDP_education$Ranking_group <- cut2(GDP_education$Ranking, g=5)
table(GDP_education$Ranking_group, GDP_education$income_group)
