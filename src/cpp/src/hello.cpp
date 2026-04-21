#include "hello.h"
#include <iostream>

namespace hello {

Greeter::Greeter(const std::string& name) : name_(name) {}

std::string Greeter::greet() const {
    return "Hello, " + name_ + "!";
}

std::string Greeter::farewell() const {
    return "Goodbye, " + name_ + "!";
}

}  // namespace hello
