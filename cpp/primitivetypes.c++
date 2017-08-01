#include<iostream>
using namespace std;

const int kNumUnsignBits = 64;

unsigned long ClosestIntSameBitCount(unsigned long x){
    for(int i=0; i<kNumUnsignBits-1; ++i){
        if(((x>>i) & 1) != ((x>>(i+1) & 1))){
            x ^= (1UL<<i) | (1UL << (i+1));
            return x;
        }
    }
}

int main(){
    cout << ClosestIntSameBitCount(7) << endl;
}
