#include <iostream>
#include <string>
#include <vector>

using namespace std;

vector<string> JustifyText(vector<string> text, size_t length){
    vector<string> this_line, result;
    string line;
    size_t empty_space, i=0;
    char filling = '_';

    while(i < text.size()){
        if (text[i].length() > length){
            cout << "String length out of range" << endl;
            throw "Error";
        }

        empty_space = length;

        this_line = {};

        while (i < text.size()){
            if (empty_space < text[i].length() + this_line.size()){
                line = "";
                while (empty_space > 0){
                    
                    size_t k = 0;

                    do {
                        this_line[k++].append("_");
                        empty_space--;
                    }while(k < this_line.size()-1 && empty_space > 0);
                }

                for (auto token: this_line){
                    line.append(token);
                }

                result.emplace_back(line);

                break;
            }

            this_line.emplace_back(text[i]);
            empty_space -= text[i++].length();

            if (i == text.size()){
                line = "";
                size_t k = 0;
                
                do {
                    this_line[k++].append("_");
                }while(k < this_line.size()-1);

                size_t padding = empty_space - k;
                this_line.back().append(padding, filling);

                for (auto token: this_line){
                    line.append(token);
                }

                result.emplace_back(line);

                return result;
            }
        }
    }

    return result;
}


int main(){
    vector<string> text = {"the", "quick", "brown", "fox", "jumped",\
                           "over", "the", "lazy", "dogs"};
    
    auto justified_text = JustifyText(text, 18);

    for (auto s: justified_text){
        cout << s << endl;
    }
}
