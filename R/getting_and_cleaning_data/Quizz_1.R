library(data.table)
setwd("/home/wenduowang/git/R/getting_and_cleaning_data")
#link to the survery data CSV
file_url <- "https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Fss06hid.csv"
download.file(file_url, destfile="./survey2006.csv", quiet=FALSE, method="wget")
#link to the data description PDF
file_url <- "https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FPUMSDataDict06.pdf"
download.file(file_url, destfile="./survey2006.pdf", quiet=FALSE, method="wget")
survey_data <- read.table("./survey2006.csv", sep=",", header=TRUE, na.strings=c("bb"))
#convert survey data to data.table
survey_table <- data.table(survey_data)
#if property value > 1M, then VAL > 23. In this case there are 53 properties above that level.
survey_table[VAL>23,.N]
survey_table[,.N,by=FES]

library(xlsx)
#link to the  Natural Gas Aquisition Program spreadsheet
file_url <- "https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FDATA.gov_NGAP.xlsx"
download.file(file_url, destfile="./NGAP.xlsx", quiet=FALSE, method="wget")
dat <- data.table(read.xlsx("./NGAP.xlsx", sheetIndex=1, header=TRUE, rowIndex=c(18:23), colIndex=c(7:15), encoding="UTF-8"))
sum(dat$Zip*dat$Ext, na.rm=T)

library(XML)
#link to the Baltimore restaurants data
file_url <- "https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Frestaurants.xml"
download.file(file_url, destfile="./baltimore_restaurants.xml", quiet=FALSE, method="wget")
restaurant_data <- xmlTreeParse("./baltimore_restaurants.xml", useInternalNodes=T)
root_node = xmlRoot(restaurant_data)
restaurant_summary <- xpathSApply(root_node,"//zipcode", xmlValue)
table(restaurant_summary)

#link to the Idaho housing data CSV
file_url <- "https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Fss06pid.csv"
download.file(file_url, destfile="./idaho_housing.csv", quiet=FALSE, method="wget")
DT <- fread("./idaho_housing.csv", sep=",", header=T)
t <- array(0,dim=c(1,10))
t1 <- system.time(tapply(DT$pwgtp15,DT$SEX,mean)); t[1] <- t1[3]
t2 <- system.time(mean(DT[DT$SEX==1,]$pwgtp15)) + system.time(mean(DT[DT$SEX==2,]$pwgtp15)); t[2] <- t2[3]
t3 <- system.time(DT[,mean(pwgtp15),by=SEX]); t[3] <- t3[3]
t4 <- system.time(sapply(split(DT$pwgtp15,DT$SEX),mean)); t[4] <- t4[3]
t5 <- system.time(mean(DT$pwgtp15,by=DT$SEX)); t[5] <- t5[3]
#t6 <- system.time(rowMeans(DT)[DT$SEX==1]) + system.time(rowMeans(DT)[DT$SEX==2]); t[6] <- t6
for(i in 1:5){
  print(t[i])
}
