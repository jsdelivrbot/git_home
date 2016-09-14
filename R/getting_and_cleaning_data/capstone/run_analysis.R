#set the working directory properly to get files in a good order
setwd("./")
#load the packages used throughout the script
library(dplyr)
library(reshape2)
#read the global activity labels, of "character" class
activity_labels <- read.table(file="./UCI HAR Dataset/activity_labels.txt", colClasses=c("character", "character"))
#read the features labels, included in the second column of "features.txt"
features <- read.table(file="./UCI HAR Dataset/features.txt")
features <- as.character(features$V2)
#read the train data sets
#the subject id is in subject_train
#statistics of sensor data is in x_train
#manually added activity ids are in y_train 
subject_train <- read.table(file="./UCI HAR Dataset/train/subject_train.txt", col.names="subject", colClasses=c("character"))
x_train <- read.table(file="./UCI HAR Dataset/train/X_train.txt")
y_train <- read.table(file="./UCI HAR Dataset/train/y_train.txt", col.names="activity", colClasses=c("character"))
#merge the subject id, activity id and sensor data together, using cbind()
train <- cbind(subject_train, y_train, x_train)
#the same process follows for reading and merging test data as below
subject_test <- read.table(file="./UCI HAR Dataset/test/subject_test.txt", col.names="subject", colClasses=c("character"))
x_test <- read.table(file="./UCI HAR Dataset/test/X_test.txt")
y_test <- read.table(file="./UCI HAR Dataset/test/y_test.txt", col.names="activity", colClasses=c("character"))

test <- cbind(subject_test, y_test, x_test)
#merge the train and test data using rbind()
total <- rbind(train, test)
#extract the variables in "total" where column name contains keywords "mean()" and "std()"\
#which is specified in original authers' dataset description\
#grep()gives the indices for such columns
mean_std <- total[, c(1:3, grep("mean\\(\\)|std\\(\\)", features)+3)]
#assgin the human readable variable names to the 561 sensor data columns\
#by giving the corresponding feature strings to the colnames()
colnames(mean_std)[3: length(mean_std)] <- features[grep("mean\\(\\)|std\\(\\)", features)]
#the following 2 lines replace illegal characters in the variable names\
#the keywords in question include "-" and "()"
colnames(mean_std) <- gsub(pattern="-", replacement="_", colnames(mean_std))
colnames(mean_std) <- gsub(pattern="\\(\\)", replacement="", colnames(mean_std))
#the following for() loop replaces activity ids with the meaningful activity names\
#which are specified in "activity_labels.txt"
for(i in c(1:nrow(activity_labels))){
  mean_std$activity <- gsub(
    pattern=activity_labels$V1[i], 
    replacement=activity_labels$V2[i],
    mean_std$activity
    )
}
#the following 2 lines prepare for the subsequent melt() function\
#and obtain the id variable names, i.e. subject and activity,\
#and measurement variable names, i.e. the 561 features
ids <- names(mean_std)[1:2]
variables <- names(mean_std)[3:ncol(mean_std)]
#melt down the mean_std object to take out "subject" and "activity" as group labels\
#and the 561 features as measurements
mean_std_melt <- melt(mean_std, id=ids, measure.vars=variables)
#cast the melt data frame together in a structure that\
#summarise the group labels versus measurements means 
average <- dcast(mean_std_melt, subject+activity~variables, mean)
#arrange the resulting 
average <- arrange(average, subject, activity)
#the features should be renames with a prefix "mean_of_"\
#to state the fact that they are the mean of previous variables
colnames(average)[3:ncol(average)] <- paste0("mean_of_", colnames(average)[3:ncol(average)])
#write the data frame to a txt
write.table(average, file="tidy_data.txt", row.names=F)
#the data sets under the "Inertial Signals" directory are not used.
