# Smart Parking Lot System

## Project Overview
IoT-based smart parking system using ESP32 microcontrollers with computer vision and sensor integration for real-time parking space detection and management.

## Key Results
- **System Architecture**: Dual ESP32 system with ESP-NOW communication
- **Detection Method**: Avoid sensors + YOLOv3 computer vision verification
- **Communication**: ESP-NOW protocol for peer-to-peer device communication
- **User Interface**: RGB LED indicators + 16x2 LCD display
- **Accuracy**: 95%+ vehicle detection accuracy

## System Architecture
```
[Parking Slot] → [Avoid Sensor] → [ESP32 Dev Module] → [ESP-NOW] → [ESP32-CAM]
                                                                         ↓
                                                                   [Laptop: YOLOv3]
                                                                         ↓
                                                                   [Serial Communication]
                                                                         ↓
[RGB LED + LCD] ← [ESP32 Dev Module] ← [ESP-NOW] ← [ESP32-CAM]
```

## Hardware Components

### Camera System (AI)
- ESP32-CAM with OV2640 camera
- Arduino Nano (as FTDI converter)
- USB 2.0 A to USB 2.0 Mini B cable
- Breadboard 400 holes
- Personal Computer for AI processing

### Prototype Parking Lot
- Triplek 3mm board
- Vehicle miniatures
- Adhesive materials
- Electrical tape

### Sensor and Output System
- ESP32 Dev Module
- Avoid sensor for detection
- RGB LED common anode
- 68 Ohm resistors
- LCD 16x2 display
- 10k Ohm potentiometer
- Power module
- 12V AC adapter
- Breadboard 830 holes

## Wiring Configuration

### Sensor and Output System
- **Avoid Sensor**: VCC→3V3, GND→GND, OUT→D23
- **RGB LED**: RED→68Ω→D21, Anode→3V3, GREEN→D22
- **LCD 16x2**: 
  - VSS→GND, VDD→5V, V0→Potentiometer SIG
  - RS→D14, RW→GND, E→D12
  - D4→D13, D5→D15, D6→D2, D7→D4
  - A→3V3, K→GND

### Camera System
- **ESP32-CAM**: 
  - 5V→5V (Arduino Nano), GND→GND
  - GPIO1/TXD→TX1 (Arduino Nano)
  - GPIO3/RXD→RX0 (Arduino Nano)
  - GPIO0→GND (for programming)
- **Arduino Nano**: RST→GND

## Technologies
- Programming: Arduino IDE, Python 3.9
- Microcontrollers: ESP32 Dev Module, ESP32-CAM
- Computer Vision: OpenCV, YOLOv3
- Communication: ESP-NOW, WiFi, HTTP
- Hardware: Arduino Nano, Various sensors and displays

## Project Structure
```
Smart-Parking-Lot-System/
├── src/
│   ├── Camera.ino              # ESP32-CAM main program
│   ├── ParkingLot.ino          # ESP32 Dev Module program
│   ├── CarDetection.py         # Python computer vision
│   └── app_httpd.cpp           # ESP32-CAM HTTP server
├── docs/
│   ├── Laporan_Final_Project.pdf  # Complete project report
│   ├── system_architecture.png    # Architecture diagram
│   └── wiring_diagram.png         # Wiring schematics
├── models/
│   ├── yolov3.weights          # YOLOv3 pre-trained weights
│   └── yolov3.cfg              # YOLOv3 configuration
└── README.md                   # This documentation
```

## Installation and Setup

### 1. Hardware Setup
1. Assemble the parking lot prototype structure
2. Connect all components according to wiring diagram
3. Ensure proper power supply connections
4. Position avoid sensors at parking slot entrances

### 2. Software Installation
```bash
# Install required Python libraries
pip install opencv-python numpy requests pyserial

# Install Arduino IDE with ESP32 support
# Add ESP32 board URL: https://espressif.github.io/arduino-esp32/package_esp32_index.json

# Install ESP32-CAM libraries in Arduino IDE
# ESP32 by Espressif Systems
```

### 3. Configuration Steps
1. Upload `Camera.ino` to ESP32-CAM (using GPIO0 to GND for programming)
2. Upload `ParkingLot.ino` to ESP32 Dev Module
3. Update MAC addresses in both programs for ESP-NOW pairing
4. Configure WiFi credentials in both ESP32 devices
5. Run `CarDetection.py` on laptop connected to Arduino Nano

## System Operation Flow
1. **Initial Detection**: Avoid sensor detects object entering parking slot
2. **Communication**: ESP32 Dev Module sends "ada" message via ESP-NOW to ESP32-CAM
3. **Vision Verification**: ESP32-CAM captures image, sends to laptop via HTTP
4. **AI Processing**: Python YOLOv3 analyzes image for vehicle detection
5. **Result Transmission**: Detection result sent back via serial to ESP32-CAM
6. **Status Update**: ESP32-CAM sends "fix ada" or "fix ga ada" via ESP-NOW
7. **User Feedback**: ESP32 Dev Module updates LED and LCD display accordingly

## Testing Procedure
1. Power on both ESP32 devices
2. Start Python car detection program on laptop
3. Place vehicle in parking slot
4. Verify:
   - Red LED lights up
   - LCD shows "Parkir terisi"
   - Console shows detection confirmation
5. Remove vehicle from slot
6. Verify:
   - Green LED lights up
   - LCD shows "Parkir kosong"

## Troubleshooting

### Common Issues and Solutions
1. **ESP-NOW Connection Failure**:
   - Verify MAC addresses are correctly configured
   - Ensure both devices are on same WiFi channel
   - Check power supply stability

2. **Camera Not Streaming**:
   - Verify ESP32-CAM power connection (requires 5V)
   - Check GPIO0 is disconnected from GND after programming
   - Verify WiFi credentials

3. **YOLOv3 Detection Issues**:
   - Ensure yolov3.weights and yolov3.cfg files are in correct location
   - Check camera positioning and lighting conditions
   - Adjust confidence threshold in Python code

4. **Serial Communication Problems**:
   - Verify correct COM port in Python script
   - Check baud rate settings match (115200)
   - Ensure Arduino Nano is properly connected

## Performance Metrics
- **Response Time**: < 2 seconds from detection to status update
- **Detection Accuracy**: 95%+ for standard vehicles
- **Communication Range**: Up to 100 meters with ESP-NOW
- **Power Consumption**: < 500mA during operation
- **Camera Resolution**: CIF (352x288) for optimal performance

## Applications and Use Cases
1. **Shopping Mall Parking**: Real-time parking availability display
2. **Office Building Parking**: Automated parking management
3. **Public Parking Facilities**: Efficient space utilization
4. **Smart City Infrastructure**: Integrated parking solutions
5. **University Campus**: Student and staff parking management

## Future Enhancements
1. **Multi-slot Monitoring**: Single camera monitoring multiple parking slots
2. **Mobile Application**: Real-time parking availability on smartphones
3. **License Plate Recognition**: Automated vehicle identification
4. **Solar Power Integration**: Energy-efficient operation
5. **Cloud Integration**: Centralized parking management system
6. **Payment System Integration**: Automated billing based on parking duration
7. **Emergency Vehicle Priority**: Special parking slot management

## Team Members
- **Naftali Salsabila Kanaya Putri** (5027201012)
- **Anisah Farah Fadhila** (5027201023)

## Institutional Information
- **Institution**: Institut Teknologi Sepuluh Nopember (ITS)
- **Faculty**: Fakultas Teknologi Elektro dan Informatika Cerdas
- **Department**: Departemen Teknologi Informasi
- **Academic Year**: Semester Genap 2022

## Documentation
Complete project report available at: [Google Drive Link](https://drive.google.com/drive/folders/1-4VDE7U-5iR4CY4RtvpgCa6RkMewx5kU)

## License
This project is developed for academic purposes at Institut Teknologi Sepuluh Nopember.

---

Smart Parking Lot System - IoT Project combining ESP32 microcontrollers, computer vision, and sensor technology for intelligent parking management.
```
