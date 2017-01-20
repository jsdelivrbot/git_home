#include <iostream>
#include <vector>

using namespace std;

struct Terminals {
    size_t begin, end, len;
    Terminals(size_t x, size_t y, size_t z) : begin(x), end(y), len(z) {}
};

Terminals FindLongestIncreasingSequence(const vector<int> &v){
    
    vector<int> vec = v;
    Terminals result(0, 0, 0), current(0, 0, 0);

    for (size_t i=1; i < vec.size(); i++){
        if (vec[i] <= vec[i-1]){
            if (current.len > result.len){
                result = current;
            }
            current.begin = i;
        }
        
        current.end = i;
        current.len = current.end - current.begin;
    }

    result = current.len > result.len ? current : result;

    return result;
}

int main(){
    vector<int> a = {2,11,3,5,13,7,19,17,23};
    auto sequence = FindLongestIncreasingSequence(a);
    cout << sequence.begin << "\t" << sequence.end << endl;
}
