#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>

using namespace std;

class Board {
    public:
        Board(){
            rooks_ = safe_ = vector<vector<int>>(size_, vector<int>(size_, 1));
        }

        void placement(const tuple<size_t, size_t> &index){
            rooks_[get<0>(index)][get<1>(index)] = 1;
        }

        void PrintBoard(){
            // Print the matrix on screen
        }
    
    private:
        const size_t size_ = 8;
        vector<vector<int>> rooks_, safe_;
};

int main(){
    tuple<size_t, size_t> index {0, 0};
    Board b;
    b.placement(index);
}
