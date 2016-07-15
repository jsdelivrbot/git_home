#setting up the working directory
setwd("~/git/git_home/R/MSBA/")

#include necessary libraries
library(dplyr)

#define the column variable types
col_classes <- c("integer",
                 "character",
                 "character",
                 "character",
                 "character",
                 "numeric",
                 "character",
                 "character",
                 "character",
                 "character",
                 "character",
                 "character",
                 "character",
                 "character",
                 "character",
                 "numeric",
                 "numeric")

#read in the whole data set
cars_data <- read.csv("Cars.csv", header = T, sep = ",", na.strings = "unsp",
                      colClasses=col_classes)

#this function will unfold categorical variables into different levels, NA noted as "unknown"
unfold_name <- function(variable, var_name=c("")){
    subset <- as.character(unique(variable))
    
    for (i in c(1:length(subset))){
        if (is.na(subset[i])){
            subset[i] <- paste("unknownn ", as.character(var_name), sep="")
        }
        
        else {
            subset[i] <- paste(as.character(var_name), ": ", subset[i], sep="")
        }
    }
    
    subset <- sort(subset)
    
    return(subset)
}

#create an empty vector to store the unfolded feature names
feature_names <- c()

#store the original variable names
original_names <- colnames(cars_data)

#store the names of numerical variables
numeric_vars <- c("X", "mileage", "featureCount", "price")

#this function joins the unfolded variable names. Numeric variables remain unchanged,
#unfolded categorical variables will be expanded horizontally
for (i in c(1:ncol(cars_data))){
    if (original_names[i] %in% numeric_vars){
        feature_name <- original_names[i]
    }
    
    else {
        feature_name <- unfold_name(cars_data[, i], original_names[i])
    }
    
    feature_names <- c(feature_names, feature_name)
}

########################################################################
#### the code below constructs new columns for unfolded variables ######
#### and a new data frame is created, including the price column. ######
#### tried to package the code in a function, but performance is  ######
#### terrible - seems multi-threading doesn't work.               ######
########################################################################

varnames <- colnames(cars_data)

varnames_logic <- feature_names[!(feature_names %in% numeric_vars)]

varnames_logic <- gsub("^.+: ", "", varnames_logic)

varnames_logic[startsWith(varnames_logic, "unknown")] <- NA

dimension <- dim(cars_data)

new_dataset <- data.frame(cars_data[, 1])

k <- 0

for (i in c(1:dimension[2])){
    
    if (varnames[i] %in% numeric_vars){
        new_dataset <- cbind(new_dataset, cars_data[, i])
    }
    
    else {
        for (j in c(1:length(unique(cars_data[,i])))){
            pending_col <- cars_data[, i]
            if (is.na(varnames_logic[j+k])){
                pending_col[!is.na(pending_col)] <- FALSE
                pending_col[is.na(pending_col)] <- TRUE
            }
            
            else {
                pending_col[is.na(pending_col)] <- FALSE
                pending_col <- (pending_col == varnames_logic[j+k])
            }
            
            new_dataset <- cbind(new_dataset, pending_col)
        }
        k <- k + j
    }
    
}

clean_dataset <- new_dataset[, 2:ncol(new_dataset)]

colnames(clean_dataset) <- feature_names

########################################################################
########################################################################
########################################################################
########################################################################

#first scale variables


#now split the training data and cross-validation data
counts <- nrow(clean_dataset)

col_num <- ncol(clean_dataset)

training_index <- sample(counts, round(counts*0.8))

training_set <- clean_dataset[training_index,]

validation_set <- clean_dataset[-training_index,]

#now split X and Y
X_train <- training_set[, -col_num]
Y_train <- training_set[, c(1, col_num)]

X_cv <- validation_set[, -col_num]
Y_cv <- validation_set[, c(1, col_num)]

summary(lm(Y_train[,2]~X_train[,-1]))
