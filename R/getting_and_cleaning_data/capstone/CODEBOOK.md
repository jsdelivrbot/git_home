The variables obtained in the "tidy_data.txt" inherits the original data by D. Anguita et al. in their study "Human Activity Recognition Using Smartphones Dataset"[1]. The original authors' records have been herein inclued in the subfolders, with dropping certain unused files (details provided in README.md).

Before continuing reading, please refer to the 2 explanatory documents in "UCI HAR Dataset/" folder, i.e. "README.txt" and "features_info.txt". The meanings of variable names are retained.

Then comes a couple of notice points to understand the variables in the "tidy_data.txt" file.
1.	The first column "subject" represents the id number of the research subjects, ranging from (number) 1 to 30.
2.	The second column "activity" provides the activity label with 6 options, in strict accordance with the original authors annotation(specified in "activity_labels.txt").
3.	From the third column on, there are 561 variables, prefixed by "mean_of_" to indicate they are the mean of following feature names, which were extracted from the "X_train.txt" and "X_test.txt" files. From the 2 files, only the mean() and std() variables are selected and labeled according to "features.txt". The selected columns are grouped by "subject" and "activity", and their respective means are calculated.

Reference:
[1] Davide Anguita, Alessandro Ghio, Luca Oneto, Xavier Parra and Jorge L. Reyes-Ortiz. Human Activity Recognition on Smartphones using a Multiclass Hardware-Friendly Support Vector Machine. International Workshop of Ambient Assisted Living (IWAAL 2012). Vitoria-Gasteiz, Spain. Dec 2012