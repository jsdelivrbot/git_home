library(ggplot2)
library(gridExtra)

pred_lasso <- read.csv("Cars_out_price.csv", header=T)
dim(pred_lasso)
pred_boost <- read.csv("Cars_X_out_matt.csv", header=T)
dim(pred_boost)
pred_xgboost <- read.csv("Cars_X_out_summer.csv", header=T)
dim(pred_xgboost)

actual <- read.csv("Cars_Price2_out.txt", header=F)

dim(actual)

pred_summary <- cbind(pred_lasso$price,
                   pred_boost$price,
                   pred_xgboost$price,
                   actual,
                   pred_lasso$X)

colnames(pred_summary) <- c("lasso", "boosting", "xgboost", "Actual", "X")

RMSE <- integer(3)

RMSE_calc <- function(X, Y){
    rmse <- mean((X-Y)^2)^.5
}

for (i in 1:3){RMSE[i] <- RMSE_calc(pred_summary[, i], pred_summary[, 4])}

# cat("The RMSE with Lasso is:", RMSE[1])
# cat("The RMSE with Boosting is:", RMSE[2])

pred_summary <- as.data.frame(pred_summary)

which.max(pred_summary$boosting - pred_summary$Actual)

p1 <- ggplot(data=pred_summary, aes(x=X, y=lasso-Actual)) + geom_point()
p2 <- ggplot(data=pred_summary, aes(x=X, y=boosting-Actual)) + geom_point()
# p3 <- ggplot(data=pred_summary, aes(x=X, y=xgboost-Actual)) + geom_point()
grid.arrange(p1, p2, ncol = 1, nrow = 2)

cat("The RMSE with Lasso is:", RMSE[1])
cat("The RMSE with Boosting is:", RMSE[2])