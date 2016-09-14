This repository contains the codes and data for the capstone project of Getting and Cleaning Data course.
The original data was downloaded via https://d396qusza40orc.cloudfront.net/getdata%2Fprojectfiles%2FUCI%20HAR%20Dataset.zip

The descriptions of the documents are listed below
run_analysis.R:		the R script that performs transformation and computing on the downloaded original data, resulting in the final output data set "tidy_data.txt". By viewing the actual code, it will be easier to understand the manipulations by reading inline comments.
tidy_data.txt:		the output data set summarising the mean values of "mean()" and "std()" sensor statistics of each subject and activity.
CODEBOOK.md:		explains the variables in "tidy_data.txt".
UCI HAR Dataset/:	the downloaded original data folder, yet the "Inertial Signals" subdirectories have been removed for they are not directly related to the subsequent transformation. For its original descriptions please refer to "UCI HAR Dataset/README.txt".

#For any question, you are welcome to contact the author: wenduo.wang@hotmail.com
