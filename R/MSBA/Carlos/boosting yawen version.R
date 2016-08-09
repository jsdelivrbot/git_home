### install all of the packages
# install.packages("Hmisc")
# ninstall.packages("psych")
# install.packages("car")
# install.packages("VIM")
# install.packages('caret')
# install.packages('mboost')
# install.packages('gbm')

library(Hmisc)
library(MASS)
library(VIM)
library(caret)
library(mboost)
library(gbm)
## Read the cars.csv dataset
cars <- read.csv(file = "Cars.csv", header = TRUE, na.strings = "") 

# Select a subset of variable for regression
cars.sel <- subset(cars, select = c(trim, mileage, displacement, featureCount, color, condition, wheelType, year, state, region, soundSystem, isOneOwner, fuel, price))


### See how much Missing data we have in each variables and how much they take percentage ###
pMiss <- function(x){sum(is.na(x))/length(x)*100}
apply(cars.sel, 2, pMiss)
apply(cars, 1, pMiss)

#impute all the missing value by the mode of given variable
fuel.impute <- impute(cars.sel["fuel"], "mode")
trim.impute <- impute(cars.sel["trim"], "mode")
wheelType.impute <- impute(cars.sel["wheelType"], "mode")
region.impute <- impute(cars.sel["region"], "mode")
state.impute <- impute(cars.sel["state"], "mean")
soundSystem.impute <- impute(cars.sel["soundSystem"], "mode")
displace.impute <- impute(cars.sel["displacement"], "mode")
color.impute <- impute(cars.sel["color"], "mode")

cars.sel$fuel <- unlist(fuel.impute)
cars.sel$color <- unlist(color.impute)
cars.sel$displacement <- unlist(displace.impute)
cars.sel$region <- unlist(region.impute)
cars.sel$soundSystem <- unlist(soundSystem.impute)
cars.sel$state <-unlist(state.impute)
cars.sel$wheelType <- unlist(wheelType.impute)
cars.sel$trim <- unlist(trim.impute)

cars.sel$fuel.impute <- NULL
cars.sel$color.impute <- NULL
cars.sel$sound <- NULL


# split data into training and validation samples
# we will use (train.size)% for traiing and (100 - train.size)% for validation
set.seed(2017)
train.size <- 0.8
train.index <- sample.int(length(cars.sel$price), round(length(cars.sel$price) * train.size))
train.sample <- cars.sel[train.index,]
valid.sample <- cars.sel[-train.index,]


boost.model <- gbm(price ~ trim + mileage + displacement + featureCount + color + condition + wheelType + year + state + region + soundSystem + isOneOwner + fuel,
    data = train.sample,
    n.trees = ,
    interaction.depth = 2,
    n.minobsinnode = 10,
    shrinkage = 0.2)

boost.predict = predict(boost.model,
         newdata = train.sample,
         n.trees = 100,
         type="link",
         single.tree=FALSE)

train.RMSE <- round(sqrt(mean((boost.predict - train.sample$price)^2)))
train.RMSE




