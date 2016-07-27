library(lattice)
library(dummies)
library(numpy)
library(dplyr)
library(DAAG)
library( Rcmdr)
library(caret)


Cars_Better <- read.csv("Cars_Better.csv")
#View(Cars_Better)
ca = Cars_Better  #Temp Cars Dataset
#attach(ca)
#names(ca)

#Clean up data and set variable types
factortypes = sapply(ca, class) #Determine the automatic variable types when we imported the Cars.csv file

ca[ca=="unsp"]=NA   #Replace unsp values with NA before converting column variable types
#View(ca)
ca$price = as.numeric(ca$price)   #convert price to numeric variable
ca$disp_cont = as.numeric(ca$disp_cont)   #convert displacement to numeric variable
ca$wheelSize = as.numeric(ca$wheelSize)   #convert Wheel size to numeric variable
sapply(ca, class)   #double check conversion
factortypes = sapply(ca, class)  #save factor types in dataframe

ca = subset(ca, select=-c(wheelSize))  #Drop Wheel size

#Scale variables before creating dummies and splitting
#Variables to scale 
#Price, age, disp_cont, mileage
ca_scaled = ca
attach(ca_scaled)
head(ca_scaled)
ca_scaled[c("price","age","disp_cont","mileage")] = lapply(ca_scaled[c("price", "age", "disp_cont","mileage")], function(x) log(x))                            #scaled continuous columns by ln()

summary(ca_scaled)
summary(ca) #Verify scaling went as expected

#create dummy variables for categorical data using dummies() package
x.f.s = dummy.data.frame(ca_scaled, sep = "#", omit.constants = TRUE)
get.dummy(x.f.s)
sapply(x.f.s, class)   #double check conversion
summary(x.f.s)   #All good at this point
#--------------------------------------------------
#    dataset = x.f.s  All data remains
#    Setup K-folds
#Setup cross validation
counts <- nrow(x.f.s)
col_num <- ncol(x.f.s)
training_index <- sample(counts, round(counts*0.8)) #Generate a random 20% Same to leave out as test, by idx vec

class(x.f.s)
y.s = x.f.s["price",drop=FALSE]
class(y.s)
names(y.s)
dim(y.s)

attach(x.f.s)
final = subset(x.f.s, select= - c(id)) #Drop id don't take a subset  **********important
x.train = subset(x.f.s, select= - c(id,price)) #Drop id and price
class(x.train)
dim(x.train)
names(x.train)
#Commenting out because using DAAg package you don't even need to leave anything out.
x.train <- x.train[training_index,]
x.cv <- x.f.s[-training_index,]
y.train <- as.data.frame(y.s[training_index,,drop=FALSE])
y.cv <- as.data.frame(y.s[-training_index,,drop=FALSE])

#carmodel = lm(x.f.s$price[folds$train,] ~ .,data=x.f.s[folds$train,])
#summary(carmodel)
#confint(carmodel$residuals)
#plot(ca_scaled$price,carmodel$res,pch=19,col=2,ylab="residuals",main="Residual Plot")
#predictions = fitted(carmodel)
#Stepwise Regression to eliminate variables
#full = glm(y.train$price~., data=x.train)
#### Careful this could freeze an old computer
#### ###########################################################################
#regBoth = step(carmodel, scope=formula(carmodel), direction="both", k=log(length(training_index)))
###########################################################################3#####
summary(regBoth)
final_variables = names(regBoth$coefficients)
final_variables
regBoth$anova
names(regBoth)
regBoth$coefficients


#To rerun test you only need to rerun this part and below
training_index <- sample(counts, round(counts*0.8))
x.train <- x.train[training_index,]
x.cv <- x.f.s[-training_index,]
y.train <- as.data.frame(y.s[training_index,,drop=FALSE])
y.cv <- as.data.frame(y.s[-training_index,,drop=FALSE])
x.train$pred_price = predict(regBoth,data=x.train)
x.train$price  = y.train$price
#View(x.train[c("pred_price","price")])
x.train[c("price_dollars", "pred_price_dollars")] = lapply(x.train[c("price", "pred_price")], function(x) exp(x)) 
x.train$error_dollars = x.train$price_dollars - x.train$pred_price_dollars
View(x.train[c("pred_price","price","pred_price_dollars","price_dollars","error_dollars")])
#-------------------------------------------------------------------------------
x.cv$pred_price = predict(regBoth,newdata=x.cv)
x.cv$price  = y.cv$price
#View(x.cv[c("pred_price","price")])
x.cv[c("price_dollars", "pred_price_dollars")] = lapply(x.cv[c("price", "pred_price")], function(x) exp(x)) 
x.cv$error_dollars = x.cv$price_dollars - x.cv$pred_price_dollars
View(x.cv[c("pred_price","price","pred_price_dollars","price_dollars","error_dollars")])

train.RMSE <- sqrt(mean((x.train$error_dollars)^2))
train.RMSE  #$2146.399  #3825.908
x.cv.RMSE = sqrt(mean((x.cv$error_dollars)^2))
x.cv.RMSE




















