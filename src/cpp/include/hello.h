#ifndef HELLO_H
#define HELLO_H

#include <string>

namespace hello {

class Greeter {
public:
    Greeter(const std::string& name);
    std::string greet() const;
    std::string farewell() const;

private:
    std::string name_;
};

}  // namespace hello

#endif  // HELLO_H
