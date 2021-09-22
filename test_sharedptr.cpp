#include <iostream>
#include <memory>
using namespace std;

struct test {
    int a=4;
};

void tester(shared_ptr<test> ptr) {
    cout<<ptr << " " << (ptr == nullptr) << " " << ptr.get() << endl;
}

int main() {
    tester({});
    tester(nullptr);
    return 0;
}