#setting up the working directory
#setwd("~/git/git_home/R/MSBA/")

#include dplyr library to access advanced data.frame functions
library(dplyr)
#include neuralnet library to access neural network functions
library(neuralnet)

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

# training_set_matrix <- as.numeric(as.matrix(training_set))
# training_set_matrix[training_set_matrix == TRUE] <- 1
# training_set_matrix[training_set_matrix == FALSE] <- 0
# training_set_matrix[is.na(training_set_matrix)] <- 0
# training_set_org <- data.frame(training_set_matrix)
# dim(training_set_org)
# summary(training_set_org)

formula_expression <- "`X` ~ `trim: 320`"

for (i in c(3:ncol(training_set))){
    variable_quote <- paste("`", names(training_set)[i], "`", sep="")
    formula_expression <- paste(formula_expression, variable_quote, sep="+")
}

formula <- as.formula(formula_expression)

training_set_converted <- model.matrix(X~., training_set)

for (i in c(1:ncol(training_set_converted))){
    colnames(training_set_converted)[i] <- gsub("`|TRUE", "", colnames(training_set_converted)[i])
}

training_set_converted <- data.frame(training_set_converted)

training_set_converted$mileage <- log(training_set_converted$mileage)

training_set_converted$featureCount <- training_set_converted$featureCount^.5

formula_expression <- "price ~ `trim..320`"

for (i in c(3:(ncol(training_set_converted)-1))){
    variable_quote <- paste("`", colnames(training_set_converted)[i], "`", sep="")
    formula_expression <- paste(formula_expression, variable_quote, sep="+")
}

formula <- as.formula(formula_expression)

# counting <- 0
# 
# for (i in c(1:ncol(training_set_converted))){
#     counting <- counting + sum(is.na(training_set_converted[,i]))
# }
# 
# print(counting)

# nn <- neuralnet(
#     formula=formula,
#     data=training_set_converted,
#     hidden=10,
#     rep=5,
#     stepmax=1e+06,
#     threshold=0.01,
#     algorithm="backprop",
#     learningrate=0.01,
#     linear.output=TRUE
#     )
# 
# head(nn$response)
# 
# nn$act.fct
# summary(nn$net.result)

lm_ridge_model <- lm.ridge(price~mileage+`trim..320`, data=training_set_converted)

lm_ridge_model$coef

summary((lm_ridge_model$residuals^2)^.5)

lm_model <- lm(price~., data=training_set_converted)
summary((lm_model$residuals^2)^.5)

formula_expression <- "`X` ~ `trim: 320`"

for (i in c(3:ncol(validation_set))){
    variable_quote <- paste("`", names(validation_set)[i], "`", sep="")
    formula_expression <- paste(formula_expression, variable_quote, sep="+")
}

formula <- as.formula(formula_expression)

validation_set_converted <- model.matrix(X~., validation_set)

for (i in c(1:ncol(validation_set_converted))){
    colnames(validation_set_converted)[i] <- gsub("`|TRUE", "", colnames(validation_set_converted)[i])
}

validation_set_converted <- data.frame(validation_set_converted)

validation_set_converted$mileage <- log(validation_set_converted$mileage)

validation_set_converted$featureCount <- validation_set_converted$featureCount^.5



lm_model_RMSE <- mean((predict(lm_model, validation_set_converted) - validation_set_converted$price)^2)^.5

lm_model_RMSE
#model.matrix(X~., cars_data)

confint(lm_model, level=0.95)[,1]*confint(lm_model, level=0.95)[,2] < 0

min.model <- lm(log(price)~mileage, data=training_set_converted)

max.model <- formula(lm(log(price)~., data=training_set_converted))

fwd.model <- step(min.model, direction="forward", scope=max.model)

bwd.model <- step(fwd.model, direction="backward", scope=min.model)

#twoway.model <- step(min.model, direction="both", scope=max.model)

# confint(fwd.model)
#
# confint(bwd.model)
#
# confint(twoway.model)[,1] * confint(twoway.model)[,2] > 0

mean((exp(predict(bwd.model, data=validation_set_converted) - log(validation_set_converted$price))^2)^.5
validation_set_converted_log <- validation_set_converted
validation_set_converted_log$price <- log(validation_set_converted_log$price)
mean((exp(predict(bwd.model, data=validation_set_converted_log))-validation_set_converted$price)^2)^.5
# summary(fwd.model$residuals^2)^.5
# 
# summary(bwd.model$residuals^2)^.5
# 
# summary(twoway.model$residuals^2)^.5
