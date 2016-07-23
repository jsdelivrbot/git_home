#setting up the working directory
#setwd("~/git/git_home/R/MSBA/")
rm(list=ls())
gc()
#include dplyr library to access advanced data.frame functions
library(dplyr)
#include neuralnet library to access neural network functions
#library(neuralnet)
#include glmnet library to do Ridge and Lasso regression
library(glmnet)

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
            subset[i] <- paste(as.character(var_name), ": unknown", sep="")
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

varnames_logic <- feature_names[!(feature_names %in% numeric_vars)]

varnames_logic <- gsub("^.+: ", "", varnames_logic)

varnames_logic[endsWith(varnames_logic, "unknown")] <- NA

new_dataset <- data.frame(cars_data[, 1])

k <- 0

for (i in c(1:dim(cars_data)[2])){
    
    if (colnames(cars_data)[i] %in% numeric_vars){
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

#now split the training data and test data

training_index <- sample(nrow(clean_dataset), round(nrow(clean_dataset)*0.8))

training_set <- clean_dataset[training_index,]

test_set <- clean_dataset[-training_index,]

training_set_matrix <- model.matrix(~., data=training_set[, -1])

for (i in c(1:ncol(training_set_matrix))){
    colnames(training_set_matrix)[i] <- gsub("`|TRUE", "", colnames(training_set_matrix)[i])
}

####################################################################
######################## Try Neural Network ########################
####################################################################
# formula_expression <- "price ~ `trim: 320`"
# 
# for (i in c(3:(ncol(training_set_matrix)-1))){
#     variable_quote <- paste("`", colnames(training_set_matrix)[i], "`", sep="")
#     formula_expression <- paste(formula_expression, variable_quote, sep="+")
# }
# 
# formula <- as.formula(formula_expression)

# counting <- 0
# 
# for (i in c(1:ncol(training_set_converted))){
#     counting <- counting + sum(is.na(training_set_converted[,i]))
# }
# 
# print(counting)

# Try neural network
# nn <- neuralnet(
#     formula,
#     data=training_set_matrix,
#     hidden=10,
#     rep=5,
#     stepmax=1e+06,
#     threshold=0.01,
#     algorithm="backprop",
#     learningrate=0.01,
#     linear.output=TRUE
#     )

# head(nn$response)
# 
# nn$act.fct
# summary(nn$net.result)

####################################################################
####################################################################
####################################################################

rm(clean_dataset)
rm(cars_data)
rm(new_dataset)
gc()

#define a helper function to create interaction terms
matrix_product <- function(A, multiply_cols){
    B <- matrix(rep(0, nrow(A)), nrow=nrow(A))
    for (i in multiply_cols){
        B <- cbind(B, A[, -c(1, 164, multiply_cols)]*A[, i])
    }
    return(B[, -1])
}

training_set_4ridge <- training_set_matrix

training_set_4ridge[, "mileage"] <- log(training_set_matrix[, "mileage"])/5

training_set_4ridge[, "featureCount"] <- training_set_matrix[, "featureCount"]^.5/5

interact_trim <- matrix_product(training_set_4ridge, 2:14)
# interact_subtrim <- matrix_product(training_set_4ridge, 15:16)
interact_condition <- matrix_product(training_set_4ridge, 17:19)
# interact_owner <- matrix_product(training_set_4ridge, 20:21)
interact_mileage <- matrix_product(training_set_4ridge, 22)
interact_year <- matrix_product(training_set_4ridge, 23:45)
# interact_color <- matrix_product(training_set_4ridge, 46:60)
interact_displacement <- matrix_product(training_set_4ridge, 61:76)
interact_fuel <- matrix_product(training_set_4ridge, 77:80)
# interact_state <- matrix_product(training_set_4ridge, 81:132)
# interact_region <- matrix_product(training_set_4ridge, 133:142)
# interact_soundsystem <- matrix_product(training_set_4ridge, 143:149)
# interact_wheeltype <- matrix_product(training_set_4ridge, 150:154)
interact_wheelsize <- matrix_product(training_set_4ridge, 155:162)
# interact_featurecount <- matrix_product(training_set_4ridge, 163)

# use ridge regression to generate a linear model including interaction terms
ridge_model <- cv.glmnet(y=training_set_4ridge[, "price"], x=cbind(
    training_set_4ridge[, -c(1, 164)],
    interact_trim,
    interact_condition,
    interact_mileage,
    interact_year,
    interact_displacement,
    interact_wheelsize),
    nfolds=10, alpha=0)

# clean up variables to free memory
rm(interact_trim)
rm(interact_condition)
rm(interact_mileage)
rm(interact_year)
rm(interact_displacement)
rm(interact_wheelsize)
gc()

# lasso_model <- cv.glmnet(y=training_set_4ridge[, "price"], x=cbind(training_set_4ridge[, -c(1, 164)], training_set_4ridge[, -c(1, 22, 164)]*training_set_4ridge[, 22], matrix_product(training_set_4ridge[, -c(1, 22:45, 164)], training_set_4ridge[, 23:45])), nfolds=10, alpha=1)

# calculate in sample RMSE
RMSE_in <- mean((predict(ridge_model, cbind(
                        training_set_4ridge[, -c(1, 164)],
                        interact_trim,
                        interact_condition,
                        interact_mileage,
                        interact_year,
                        interact_displacement,
                        interact_wheelsize)) - training_set_4ridge[, "price"])^2)^.5
##############################################################################################
# transform test set data to matrix and generate interaction terms, the same as training set #
##############################################################################################

# create a helper function to convert the data.frame to matrix
formatting_data <- function(original_df){
    df_matrix <- model.matrix(~., data=original_df[, -1])
    df_matrix_4ridge <- df_matrix
    df_matrix_4ridge[, "mileage"] <- log(df_matrix[, "mileage"])/5
    df_matrix_4ridge[, "featureCount"] <- df_matrix[, "featureCount"]^.5/5
    return(df_matrix_4ridge)
}

test_set_4ridge <- formatting_data(test_set)

interact_trim <- matrix_product(test_set_4ridge, 2:14)
# interact_subtrim <- matrix_product(test_set_4ridge, 15:16)
interact_condition <- matrix_product(test_set_4ridge, 17:19)
# interact_owner <- matrix_product(test_set_4ridge, 20:21)
interact_mileage <- matrix_product(test_set_4ridge, 22)
interact_year <- matrix_product(test_set_4ridge, 23:45)
# interact_color <- matrix_product(test_set_4ridge, 46:60)
interact_displacement <- matrix_product(test_set_4ridge, 61:76)
interact_fuel <- matrix_product(test_set_4ridge, 77:80)
# interact_state <- matrix_product(test_set_4ridge, 81:132)
# interact_region <- matrix_product(test_set_4ridge, 133:142)
# interact_soundsystem <- matrix_product(test_set_4ridge, 143:149)
# interact_wheeltype <- matrix_product(test_set_4ridge, 150:154)
interact_wheelsize <- matrix_product(test_set_4ridge, 155:162)
# interact_featurecount <- matrix_product(test_set_4ridge, 163)

##############################################################################################
##############################################################################################
##############################################################################################

RMSE_out <- mean((predict(ridge_model, cbind(
    test_set_4ridge[, -c(1, 164)],
    interact_trim,
    interact_condition,
    interact_mileage,
    interact_year,
    interact_displacement,
    interact_wheelsize)) - test_set_4ridge[, "price"])^2)^.5

print(RMSE_out)

X_test <- cbind(test_set_4ridge[, -c(1, 164)], test_set_4ridge[, -c(1, 22, 164)]*test_set_4ridge[, 22], matrix_product(test_set_4ridge[, -c(1, 22:45, 164)], test_set_4ridge[, 23:45]))
ridge_RMSE <- mean((predict(ridge_model, X_test) - test_set_4ridge[, "price"])^2)^.5
print(ridge_RMSE)


# lasso_RMSE <- mean((predict(lasso_model, test_set_4ridge[, -c(1, 164)]) - test_set_4ridge[, "price"])^2)^.5
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
