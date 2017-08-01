#include <iostream>
#include <string>

using namespace std;

size_t LongestSubstring(const string &s){
    
    size_t flag=0, accrual=0, result=0;
    const char right_paren = ')';;

    for (auto ch: s){

        if (ch == right_paren){
            flag += -1;
        }

        else {
            flag += 1;
        }

        if (flag == -1){
            result = max(result, accrual);
            accrual = 0;
            flag = 0;
            continue;
        }

        accrual++;

        cout << flag << '\t' << accrual << '\t' << result << endl;
    }

    result = (flag >= 0) ? max(result, accrual-flag) : result;
    
    return result;
}

int main(){
    string test = "()()))))()()()()()()";
    auto len = LongestSubstring(test);
    cout << len << endl;
}
