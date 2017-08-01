#include <iostream>
#include <limits>

using namespace std;

unsigned int Finder(const int (&A)[5]){
    
    unsigned int min_pos = numeric_limits<unsigned int>::max();

    for (int i: A){
        min_pos = min_pos>i && i>0 ? i : min_pos;
    }

    return min_pos - 1;
}

int main(){
    int A[5] = {-1,2,3,4,5};
    cout << Finder(A) << endl;
}
