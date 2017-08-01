#include<iostream>

using namespace std;

unsigned long gcd(unsigned long a, unsigned long b){

    if (a == b){
        return a;
    }

    else if ( a == 1 || b == 1){
        return gcd(1, 1);
    }
    
    else if (!(a & 1 || b & 1)){
        // If a and b are both even numbers
        return gcd(a>>1, b>>1) << 1;
    }
    
    else if (!(a & 1) && b & 1){
        return gcd(a>>1, b);
    }

    else if (a & 1 && !(b & 1)){
        return gcd(a, b>>1);
    }

    else if (a > b){
        return gcd(a-b, b);
    }

    else {
        return gcd(a, b-a);
    }
}

int main(){
    long unsigned x, y;
    cin >> x >> y;

    auto k = gcd(x, y);
    
    cout << k << endl;
}
