wrap.paren <- function(f){
    # Human readable formula
    f <- rev(f)
    indices <- which(f %in% c('*', '/'))
    if (length(indices) == 0){
        return(noquote(rev(f)))
    } else {
        
        for (index in indices){
            f[index] <- paste(')', f[index], sep='')
        }
        f <- c(f, rep('(', length(indices)))
        
        return(noquote(rev(f)))
    }
}

factorize.n <- function(v, n, cache=c()){
    # Take a vector v and find a way to arrive at n by + - * /
    
    # Base case
    if (length(v) == 1){
        if (v==n){
            print(wrap.paren(c(v, cache)))
        }
        return()
    } else {
        # Otherwise do recursion
        for (elem in v){
            factorize.n(v[-which(v==elem)[1]], n-elem, c('+', elem, cache))
            factorize.n(v[-which(v==elem)[1]], n+elem, c('-', elem, cache))
            factorize.n(v[-which(v==elem)[1]], n/elem, c('*', elem, cache))
            factorize.n(v[-which(v==elem)[1]], n*elem, c('/', elem, cache))
        }
    }
}

factorize.n(c(1, 2, 3, 4), 24)

factorize.n(c(2, 2, 3, 4), 24)

x <- sample(1:13, 4, replace=T)
print(x)
Sys.sleep(10)
factorize.n(x, 24)
