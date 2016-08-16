library(compiler)
enableJIT(3)
rm(list=ls())
gc()

library(tm)
library(plyr)
library(dplyr)

readArticle <- function(article_url){
    article_list <- lapply(article_url,
                           function(article_url) readPlain(
                               elem=list(content=readLines(article_url)),
                               language="en",
                               id=article_url
                           ))
    return(article_list)
}

get_corpus <- function(article){
    corp <- Corpus(VectorSource(article))
    return(corp)
}

clean_corpus <- function(corp, tfidf=0){
    corp <- tm_map(corp, content_transformer(tolower))
    corp <- tm_map(corp, content_transformer(removeNumbers))
    corp <- tm_map(corp, content_transformer(removePunctuation))
    corp <- tm_map(corp, content_transformer(stripWhitespace))
    corp <- tm_map(corp, content_transformer(removeWords), stopwords("en"))
    
    # define an optional "control" parameter
    # to weight the terms according to their tfidf index
    if (tfidf) {
        control <- list(weighting=function(x) weightTfIdf(x, normalize=FALSE))
        corp_DTM <- DocumentTermMatrix(corp, control=control)
    } else {
        corp_DTM <- DocumentTermMatrix(corp)
    }
    
    corp_DTM <- removeSparseTerms(corp_DTM, 0.8)
    
    corp_mat <- as.matrix(corp_DTM)
    
    return(corp_mat)
}

get_mat <- function(url){
    author_list <- Sys.glob(url)
    folder_list <- Sys.glob(paste(author_list, "/*", sep=""))
    articles <- lapply(folder_list, readArticle)
    corpus_list <- lapply(articles, get_corpus)
    corpus_list <- lapply(corpus_list, clean_corpus)
    
    corpus_mat <- do.call(rbind.fill.matrix, corpus_list)
    
    corpus_mat[is.na(corpus_mat)] <- 0
    
    return(corpus_mat)
    
}


get_cosine <- function(mat1, mat2){
    mat1_conform <- mat1[, colnames(mat1) %in% colnames(mat2)]
    mat2_conform <- mat2[, colnames(mat2) %in% colnames(mat1)]
    mat1_conform <- mat1_conform[, order(colnames(mat1_conform))]
    mat2_conform <- mat2_conform[, order(colnames(mat2_conform))]
    len1 <- diag(sqrt(mat1_conform%*%t(mat1_conform)))
    len2 <- diag(sqrt(mat2_conform%*%t(mat2_conform)))
    print(sum(colnames(mat1_conform)!=colnames(mat2_conform)))
    cosine_mat <- (mat1_conform %*% t(mat2_conform)) / as.vector(len1*len2)
    cosine_df <- data.frame(cosine_mat)
    return(cosine_df)
}

pred_author <- function(pred){
    article_index <- lapply(pred, which.max)
    author_index <- lapply(article_index, function(ind) ceiling(ind/50))
    return(author_index)
}

pred_accuracy <- function(author_list){
    target <- rep(1:50, each=50)
    len <- length(author_list)
    accuracy <- mean(author_list==target[1:len])
    return(accuracy)
}

get_frequency <- function(mat){
    frequency_mat <- log(mat) / as.vector(rowSums(mat))
}

get_product <- function(v1, v2){
    v1_conform <- v1[colnames(v1) %in% colnames(v2)]
    v2_conform <- v2[colnames(v2) %in% colnames(v1)]
    if (length(v1_conform)*length(v2_conform)==0){
        return(0)
    } else {
        product <- t(v1_conform) %*% v2_conform
        return(product)
    }
}

train_mat <- get_mat("data/ReutersC50/C50train/*")
test_mat <- get_mat("data/ReutersC50/C50test/*")

cosine_df <- get_cosine(train_mat, test_mat)

pred <- sapply(cosine_df, which.max)
accuracy <- mean(ceiling(pred/50)==rep(1:50, each=50))
accuracy

author_list_1 <- pred_author(cosine_df)
accuracy_1 <- pred_accuracy(author_list_1)
accuracy_1 # 54%

train_freq <- lapply(train_mat, get_frequency)
prob_mat <- lapply(test_mat[1:100],
                   function (v) lapply(train_freq, function(x) get_product(x, v)))
author_list_2 <- pred_author(prob_mat)
accuracy_2 <- pred_accuracy(author_list_2)
accuracy_2 # 47%

