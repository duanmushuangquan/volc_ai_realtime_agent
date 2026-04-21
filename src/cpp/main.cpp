#include "hello.h"
#include <iostream>

int main(int argc, char* argv[]) {
    std::string name = "World";
    if (argc > 1) {
        name = argv[1];
    }

    hello::Greeter greeter(name);
    std::cout << greeter.greet() << std::endl;
    std::cout << greeter.farewell() << std::endl;

    return 0;
}
