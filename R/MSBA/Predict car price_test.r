rm(list=ls())
gc()
#include dplyr library to access advanced data.frame functions
library(dplyr)
#include glmnet library to do Ridge and Lasso regression
library(glmnet)

##########################################################################################################
##################################### All functions are listed below #####################################
##########################################################################################################

#this function will unfold categorical variables into different levels, NA noted as "unknown"
unfold_name <- function(variable, var_name=c("")){
    subset <- as.character(unique(variable))
    
    for (i in c(1:length(subset))){
        if (is.na(subset[i])){
            subset[i] <- paste(as.character(var_name), ": unknown", sep="")
        }
        
        else {
            subset[i] <- paste(as.character(var_name), ": ", subset[i], sep="")
        }
    }
    
    subset <- sort(subset)
    
    return(subset)
}

#define a helper function to create interaction terms
matrix_product <- function(A, multiply_cols){
    B <- matrix(rep(0, nrow(A)), nrow=nrow(A))
    terminal <- ncol(A)
    for (i in multiply_cols){
        B <- cbind(B, A[, -c(1, terminal, multiply_cols)]*A[, i])
    }
    return(B[, -1])
}

# create a helper function to convert the data.frame to matrix
scaling_data <- function(original_matrix){
    scaled_matrix <- original_matrix
    scaled_matrix[, "mileage"] <- log(as.numeric(original_matrix[, "mileage"]))/5
    scaled_matrix[, "featureCount"] <- as.numeric(original_matrix[, "featureCount"])^.5/5
    return(scaled_matrix)
}

#define a data pruning function to transform the raw data.frame into a matrix ready for ridge regression
data_pruning <- function(new_data){
    
    #create an empty vector to store the unfolded feature names
    feature_names <- c()
    
    #store the original variable names
    original_names <- colnames(new_data)
    
    #store the names of numerical variables
    numeric_vars <- c("X", "mileage", "featureCount", "price")
    
    #this function joins the unfolded variable names. Numeric variables remain unchanged,
    #unfolded categorical variables will be expanded horizontally
    for (i in c(1:ncol(new_data))){
        if (original_names[i] %in% numeric_vars){
            feature_name <- original_names[i]
        }
        
        else {
            feature_name <- unfold_name(new_data[, i], original_names[i])
        }
        
        feature_names <- c(feature_names, feature_name)
    }
    
    ########################################################################
    #### the code below constructs new columns for unfolded variables ######
    #### and a new data frame is created, including the price column. ######
    #### tried to package the code in a function, but performance is  ######
    #### terrible - seems multi-threading doesn't work.               ######
    ########################################################################
    
    varnames_logic <- feature_names[!(feature_names %in% numeric_vars)]
    varnames_logic <- gsub("^.+: ", "", varnames_logic)
    varnames_logic[endsWith(varnames_logic, "unknown")] <- NA
    new_dataset <- data.frame(new_data[, 1])
    k <- 0
    
    for (i in c(1:dim(new_data)[2])){
        if (colnames(new_data)[i] %in% numeric_vars){
            new_dataset <- cbind(new_dataset, new_data[, i])
        } else {
            for (j in c(1:length(unique(new_data[,i])))){
                pending_col <- new_data[, i]
                if (is.na(varnames_logic[j+k])){
                    pending_col[!is.na(pending_col)] <- FALSE
                    pending_col[is.na(pending_col)] <- TRUE
                } else {
                    pending_col[is.na(pending_col)] <- FALSE
                    pending_col <- (pending_col == varnames_logic[j+k])
                }
                new_dataset <- cbind(new_dataset, pending_col)
            }
            k <- k + j
        }
    }
    ########################################################################
    ########################################################################
    ########################################################################
    ########################################################################
    clean_dataset <- new_dataset[, 2:ncol(new_dataset)]
    
    colnames(clean_dataset) <- feature_names
    
    rm(new_dataset)
    gc()
    
    data_matrix <- model.matrix(~., data=clean_dataset[, -1])
    
    rm(clean_dataset)
    gc()
    
    for (i in c(1:ncol(data_matrix))){
        colnames(data_matrix)[i] <- gsub("`|TRUE", "", colnames(data_matrix)[i])
    }
    
    ridge_matrix <- scaling_data(data_matrix)
    
    return(ridge_matrix)
}

#this function takes in a matrix and implement Ridge regression, and returns the model
ridge_fit <- function(ridge_matrix){
    interact_trim <- matrix_product(ridge_matrix, 2:14)
    # interact_subtrim <- matrix_product(ridge_matrix, 15:16)
    interact_condition <- matrix_product(ridge_matrix, 17:19)
    # interact_owner <- matrix_product(ridge_matrix, 20:21)
    interact_mileage <- matrix_product(ridge_matrix, 22)
    interact_year <- matrix_product(ridge_matrix, 23:45)
    # interact_color <- matrix_product(ridge_matrix, 46:60)
    interact_displacement <- matrix_product(ridge_matrix, 61:75)
    # interact_fuel <- matrix_product(ridge_matrix, 76:79)
    # interact_state <- matrix_product(ridge_matrix, 80:131)
    # interact_region <- matrix_product(ridge_matrix, 132:141)
    # interact_soundsystem <- matrix_product(ridge_matrix, 142:148)
    # interact_wheeltype <- matrix_product(ridge_matrix, 149:153)
    interact_wheelsize <- matrix_product(ridge_matrix, 154:161)
    # interact_featurecount <- matrix_product(ridge_matrix, 162)
    
    # use ridge regression to generate a linear model including interaction terms
    ridge_model <- cv.glmnet(y=ridge_matrix[, "price"], x=cbind(
        ridge_matrix[, -c(1, 163)],
        interact_trim,
        interact_condition,
        interact_mileage,
        interact_year,
        interact_displacement,
        interact_wheelsize),
        nfolds=10,
        alpha=0
        )
    
    RMSE_in <- mean((predict(ridge_model, cbind(
        training_set_4ridge[, -c(1, 163)],
        interact_trim,
        interact_condition,
        interact_mileage,
        interact_year,
        interact_displacement,
        interact_wheelsize)) - training_set_4ridge[, "price"])^2)^.5
    
    cat("In sample RMSE:", RMSE_in)
    
    # clean up variables to free memory
    rm(interact_trim)
    rm(interact_condition)
    rm(interact_mileage)
    rm(interact_year)
    rm(interact_displacement)
    rm(interact_wheelsize)
    rm(RMSE_in)
    gc()
    
    return(ridge_model)
}

#this function takes a Ridge regression model and a test data set
#and then returns out of sample RMSE
ridge_prediction_RMSE <- function(ridge_model, ridge_set){
    ridge_matrix <- matrix(as.numeric(ridge_set), ncol=ncol(ridge_set))
    
    colnames(ridge_matrix) <- colnames(ridge_set)
    
    interact_trim <- matrix_product(ridge_matrix, 2:14)
    # interact_subtrim <- matrix_product(ridge_matrix, 15:16)
    interact_condition <- matrix_product(ridge_matrix, 17:19)
    # interact_owner <- matrix_product(ridge_matrix, 20:21)
    interact_mileage <- matrix_product(ridge_matrix, 22)
    interact_year <- matrix_product(ridge_matrix, 23:45)
    # interact_color <- matrix_product(ridge_matrix, 46:60)
    interact_displacement <- matrix_product(ridge_matrix, 61:75)
    # interact_fuel <- matrix_product(ridge_matrix, 76:79)
    # interact_state <- matrix_product(ridge_matrix, 80:131)
    # interact_region <- matrix_product(ridge_matrix, 132:141)
    # interact_soundsystem <- matrix_product(ridge_matrix, 142:148)
    # interact_wheeltype <- matrix_product(ridge_matrix, 149:153)
    interact_wheelsize <- matrix_product(ridge_matrix, 154:161)
    # interact_featurecount <- matrix_product(ridge_matrix, 162)
    
    # use ridge regression to generate a linear model including interaction terms
    RMSE <- mean((predict(ridge_model, cbind(
        ridge_matrix[, -c(1, 163)],
        interact_trim,
        interact_condition,
        interact_mileage,
        interact_year,
        interact_displacement,
        interact_wheelsize)) - ridge_matrix[, "price"])^2)^.5
    
    # clean up variables to free memory
    rm(interact_trim)
    rm(interact_condition)
    rm(interact_mileage)
    rm(interact_year)
    rm(interact_displacement)
    rm(interact_wheelsize)
    gc()
    
    return(RMSE)
}

test_data_pruning <- function(test_data, training_data, varnames){
    test_set_matrix <- matrix(0, nrow=nrow(test_data), ncol=length(varnames))
    colnames(test_set_matrix) <- varnames
    
    # test_data[is.na(test_data)] <- "unknown"
    test_data_matrix <- as.matrix(test_data)
    
    #store the names of numerical variables
    numeric_vars <- c("mileage", "featureCount", "price")
    
    #######################################################################
    #### the code below constructs new columns for unfolded variables #####
    #### and a new data frame is created, including the price column. #####
    #### tried to package the code in a function, but performance is  #####
    #### terrible - seems multi-threading doesn't work.               #####
    #######################################################################
    
    for (i in c(1:ncol(test_data))){
        if (colnames(test_data)[i] %in% numeric_vars){
            test_set_matrix[, colnames(test_data)[i]] <-  as.numeric(test_data_matrix[, i])
            next
        }
        
        test_data[is.na(test_data[, i]), i] <- "unknown"
        
        if (paste(colnames(test_data)[i], ": unknown") %in% varnames){
            mask <- test_data_matrix[, i] %in% unique(training_data[, colnames(test_data)[i]])
            test_set_matrix[!mask, paste(colnames(test_data)[i], ": unknown")] <- 1
            next
        }
        for (j in c(1:length(varnames))){
            if (startsWith(varnames[j], colnames(test_data)[i])){
                pattern <- gsub("^.+: ", "", varnames[j])
                row_mask <- which(test_data_matrix[, i] == pattern)
                test_set_matrix[row_mask, j] <- 1
            }
        }
    }
    
#     col_num <- dim(test_set_matrix)[2]
# 
#     test_set_matrix <- model.matrix(~., test_set_matrix)
#     print(dim(test_set_matrix))
#     print(length(varnames))
#     print(colnames(test_set_matrix))
    colnames(test_set_matrix) <- varnames
    test_set_matrix <- scaling_data(test_set_matrix)

    return(test_set_matrix)
}
##########################################################################################################
####################################### End of function definition #######################################
##########################################################################################################

#define the column variable types
col_classes <- c("factor",
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
input_data <- read.csv("group_train.csv", header = T, sep = ",", na.strings = "unsp",
                       colClasses=col_classes)

training_set_4ridge <- data_pruning(input_data)
rm(input_data)
gc()

ridge_model <- ridge_fit(training_set_4ridge)

##########################################################################################
############################ Make predictions on the test data ###########################
##########################################################################################
test_set <- read.csv("group_test.csv", header = T, sep = ",", na.strings = "unsp",
                     colClasses=col_classes)

input_data <- read.csv("group_train.csv", header = T, sep = ",", na.strings = "unsp",
                       colClasses=col_classes)

test_set_4ridge <- test_data_pruning(test_set, input_data, colnames(training_set_4ridge))

rm(test_set)
rm(input_data)
rm(training_set_4ridge)
gc()

RMSE_out <- ridge_prediction_RMSE(ridge_model, test_set_4ridge)
cat("Out of sample RMSE:", RMSE_out)
# 
# RMSE_out <- ridge_prediction_RMSE(ridge_model, training_set_4ridge)
# cat("Out of sample RMSE:", RMSE_out)

# lasso_RMSE <- mean((predict(lasso_model, test_set_4ridge[, -c(1, 163)]) - test_set_4ridge[, "price"])^2)^.5
# print(lasso_RMSE)

# min.model <- lm(log(price)~mileage, data=training_set_converted)
# 
# max.model <- formula(lm(log(price)~., data=training_set_converted))
# 
# fwd.model <- step(min.model, direction="forward", scope=max.model)
# 
# bwd.model <- step(fwd.model, direction="backward", scope=min.model)

#twoway.model <- step(min.model, direction="both", scope=max.model)

# confint(fwd.model)
#
# confint(bwd.model)
#
# confint(twoway.model)[,1] * confint(twoway.model)[,2] > 0

# mean((exp(predict(bwd.model, data=test_set_converted) - log(test_set_converted$price))^2)^.5
# test_set_converted_log <- test_set_converted
# test_set_converted_log$price <- log(test_set_converted_log$price)
# mean((exp(predict(bwd.model, data=test_set_converted_log))-test_set_converted$price)^2)^.5
# summary(fwd.model$residuals^2)^.5
# 
# summary(bwd.model$residuals^2)^.5
# 
# summary(twoway.model$residuals^2)^.5
