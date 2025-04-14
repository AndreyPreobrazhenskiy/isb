#include <iostream>
#include <fstream>
#include <random>
using namespace std;

int main() {
    ofstream fout("cpp_sequence.txt");
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 1);

    for (int i = 0; i < 128; ++i) {
        fout << dis(gen);
    }

    fout.close();
    return 0;
}
