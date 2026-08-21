#include <iostream>
#include <string>
#include <iomanip>

int main() {
    // Internal physical state variables
    double battery_voltage = 26.0;
    double core_temperature = 25.0;

    std::string line;
    // Interactive loop reading line-by-line from stdin
    while (std::getline(std::cin, line)) {
        if (line.empty() || line == "QUIT") {
            break;
        }

        // Extract "throttle_pct" input parameter from incoming JSON string
        double throttle = 0.0;
        size_t pos = line.find("\"throttle_pct\":");
        if (pos != std::string::npos) {
            throttle = std::stod(line.substr(pos + 15));
        }

        // Extract "dt_sec" input parameter
        double dt = 1.0;
        pos = line.find("\"dt_sec\":");
        if (pos != std::string::npos) {
            dt = std::stod(line.substr(pos + 9));
        }

        // Controller logic & physics simulation step
        battery_voltage -= (throttle * 0.03) * dt;
        core_temperature += (throttle * 0.20) * dt;

        // Output telemetry JSON to stdout
        // Note: std::endl automatically flushes the output stream to prevent pipe deadlocks
        std::cout << std::fixed << std::setprecision(2)
                  << "{"
                  << "\"battery_voltage\": {\"value\": " << battery_voltage << ", \"unit\": \"V\"}, "
                  << "\"core_temperature\": {\"value\": " << core_temperature << ", \"unit\": \"C\"}"
                  << "}" << std::endl;
    }

    return 0;
}