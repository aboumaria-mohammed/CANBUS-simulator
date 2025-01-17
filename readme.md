# CAN Bus Simulator

## Description
CAN Bus Simulator is an educational tool designed to simulate and visualize Controller Area Network (CAN) communications. It provides a graphical interface to observe and interact with different types of sensors and nodes in a CAN network.

## Features
- Real-time CAN signal visualization
- Multiple sensor simulations:
  - Kerosene Level Sensor
  - Temperature Sensor
  - Pressure Sensor
- Master node controller with remote frame capabilities
- Interactive waveform display
- Visual representation of CAN frame fields
- Real-time message broadcasting between nodes

## System Requirements
- Python 3.x
- Tkinter (usually comes with Python)

## Installation
1. Clone the repository
```bash
git clone https://github.com/aboumaria-mohammed/CANBUS-simulator.git
cd CANBUS-simulator
```

2. Install required dependencies (if any additional packages are needed)
```bash
pip install -r requirements.txt
```

## Usage
To run the simulator:
```bash
python main.py
```

### Components
1. **Master Node**
   - Can request data from any sensor
   - Displays received messages
   - Shows communication history

2. **Sensors**
   - Kerosene Level Sensor (ID: 0x123)
   - Temperature Sensor (ID: 0x124)
   - Pressure Sensor (ID: 0x125)
   - Each sensor has its own control interface

3. **Waveform Visualizer**
   - Shows real-time CAN signals
   - Color-coded frame fields
   - Interactive bit information display

## Project Structure
```
can-bus-simulator/
├── main.py
├── base_sensor.py
├── kerosene_sensor.py
├── temperature_sensor.py
├── pressure_sensor.py
├── master_node.py
├── waveform_visualizer.py
└── can_message.py
```

## Architecture
The simulator architecture :
- Each sensor can broadcast messages
- The master node can request data from sensors
- All messages are broadcast to all nodes
- The waveform visualizer displays each message in real-time

## Educational Purpose
This simulator is designed to help students:
- Understand CAN bus communication principles
- Visualize CAN frame structure
- Learn about different types of CAN frames (data frames and remote frames)

## Authors
- Abooumaria Mohammed Habiballah
- Messrar Mouad
- Loubani Douaa
- Salaheddine Khazzar

## Acknowledgments
- Special thanks to Pr.Mohamed Ennaji and Pr.Ghita Zaz
