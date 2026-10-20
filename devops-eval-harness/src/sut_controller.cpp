
#include <iostream>
#include <string>
#include <algorithm>

int main() {
    double temp = 35.0;   double volt = 24.0;
    std::string line;

    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;

        if (line.find("\"inject_fault\": true") != std::string::npos || 
            line.find("\"inject_fault\":true") != std::string::npos) {
            temp = std::min(temp + 10.0, 150.0);
            volt = std::max(volt - 2.0, 0.0);
        } else {
            temp = std::max(35.0, temp - 5.0);
            volt = std::min(24.0, volt + 2.0);
        }

        std::cout << "{\"core_temperature\":{\"value\":" << temp 
                  << ",\"unit\":\"C\"},\"battery_voltage\":{\"value\":" << volt 
                  << ",\"unit\":\"V\"}}\n" << std::flush;
    }
    return 0;
}
