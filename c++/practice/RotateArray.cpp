#include <iostream>
#include <vector>

using namespace std;

void Rotate(vector<int> &v, size_t pivot, size_t from){
    // How to use recursion?
    size_t to = pivot;
    swap(v[from++], v[to++]);

    if (from == pivot && to == v.size()){
        return;
    }
    else if (from == pivot || to == v.size()){
        Rotate(v, to - 1, from);
    }
    else {
        Rotate(v, to, from);
    }

    return;
}

ostream& operator << (ostream &os, const vector<int> &v){
    for (auto x: v){
        os << " " << x;
    }
    return os;
}

int main(){
    vector<int> v = {0,1,2,3,4,5,6};
    cout << v << endl;
    //Rotate()
    Rotate(v, 3, 0);
    cout << v << endl;
}
