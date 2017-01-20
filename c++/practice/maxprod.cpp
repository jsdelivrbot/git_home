#include <iostream>
#include <limits>

using namespace std;

long long prod(long long A[], size_t skip, size_t size){
    long long product = 1;
    for (size_t i=0; i<size; i++){
        if (i != skip){
            product *= A[i];
        }
    }
    return product;
}

long long maxprod(long long A[], size_t size){
    
    // Keep track of the # of positive, negative and zero elements
    // For pos/neg elements, also record min/max values
    size_t count_neg = 0;
    size_t minindex_nonneg, maxindex_neg;
    long long max_neg = numeric_limits<long long>::min();
    long long min_nonneg = numeric_limits<long long>::max(), min_neg = 0;


    for (size_t i = 0; i<size; i++){
        if (A[i] >= 0 && A[i] < min_nonneg){
            min_nonneg = A[i];
            minindex_nonneg = i;
            cout << "Minimum non-negative element: " << min_nonneg << endl;
        }

        else if (A[i] < 0){
            count_neg += 1;
            if (A[i] > max_neg){
                max_neg = A[i];
                maxindex_neg = i;
            }
        }
    }

    if (count_neg & 1){
        cout << "Skip element (maximum negative):" << A[maxindex_neg] << endl;
        return prod(A, maxindex_neg, size);
    }
    else {
        cout << "Skip element (minimum positive):" << A[minindex_nonneg] << endl;
        return prod(A, minindex_nonneg, size);
    } 
}

int main(){
    long long A[] = {-2,-1,0,1,2,3};
    long long product = maxprod(A, sizeof(A)/sizeof(A[0]));

    cout << product << "\t" << (product==12 ? "True" : "False") << endl;
}
