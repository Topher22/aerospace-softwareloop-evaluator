# SIL Telemetry Verification Harness
An automated, data-driven Software-in-the-Loop (SIL) Telemetry Verification Framework designed for safety-critical embedded systems (e.g., aerospace flight controllers, automotive ECUs, robotics).

This harness executes compiled control software binaries via interactive IPC pipes (stdin/stdout), evaluates physical state telemetry against defined safety boundaries across time-series scenarios, and automatically pushes JUnit XML test execution reports to Jira/Xray for regulatory compliance tracking (DO-178C / ISO 26262).
