# EcoProof – AI-Powered Industrial Pollution Monitoring

EcoProof is an intelligent environmental monitoring system designed to **simulate, analyze, and monitor industrial pollution data** using machine learning, anomaly detection, automated alerts, and blockchain-based data verification.

The system processes sensor data, identifies abnormal pollution patterns, generates alerts, and maintains a tamper-resistant record of environmental data.

---

## Overview

Industrial environments generate continuous streams of sensor data related to environmental conditions and pollutant levels. Monitoring this data manually can make it difficult to identify abnormal patterns and respond quickly to potential environmental risks.

EcoProof addresses this by combining:

* Sensor data simulation
* Anomaly detection
* Pollution monitoring
* Automated alerts
* Blockchain-based data logging
* Report generation
* A Python-based application interface

The project demonstrates how **AI/ML and blockchain technologies can be combined for environmental monitoring and data integrity**.

> **Hackathon Project:** Trustistics was developed collaboratively during a hackathon with my teammate, focusing on solving cold-chain integrity and traceability challenges through IoT, blockchain, and cryptographic verification.

---

## Key Features

### Pollution Monitoring

The application processes environmental sensor data and provides a centralized way to monitor pollution-related measurements.

### Anomaly Detection

Anomaly detection is used to identify unusual patterns in incoming sensor data.

The system can distinguish between normal measurements and potentially abnormal readings that may require further investigation.

### Automated Alerts

The alert module monitors detected conditions and generates notifications when predefined abnormal conditions occur.

This enables faster identification of potentially hazardous pollution events.

### Blockchain-Based Data Integrity

EcoProof maintains environmental records using a lightweight blockchain implementation.

Sensor records can be stored as blockchain entries to provide a tamper-evident history of recorded data.

### Sensor Data Simulation

The project includes a sensor simulator that generates environmental readings for testing and demonstration purposes.

This allows the monitoring and anomaly-detection pipeline to be tested without requiring physical IoT sensors.

### Reporting

The application includes report generation functionality for analyzing and presenting collected environmental data.

---

## System Architecture

```text
                 ┌─────────────────────┐
                 │   Sensor Simulator   │
                 │    simulator.py     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Sensor Data      │
                 │   sensor_data.csv   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Anomaly Detection  │
                 │   anomaly_model.py  │
                 └──────────┬──────────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
       ┌──────────────────┐   ┌──────────────────┐
       │  Alert System    │   │    Blockchain    │
       │    alerts.py     │   │  blockchain.py   │
       └────────┬─────────┘   └────────┬─────────┘
                │                      │
                └──────────┬───────────┘
                           ▼
                 ┌─────────────────────┐
                 │   Application /     │
                 │    Dashboard        │
                 │      app.py         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Reports & Monitoring│
                 │     report.py       │
                 └─────────────────────┘
```

---

## Technology Stack

### Programming Language

* Python

### Machine Learning / Data Processing

* Anomaly detection
* Sensor data processing
* CSV-based data handling

### Data Integrity

* Custom blockchain implementation
* Hash-based block verification
* JSON-based blockchain storage

### Application

* Python application interface
* Monitoring and reporting components

### Testing

* Python test modules

### Deployment

* `Procfile` for application deployment
* `requirements.txt` for dependency management

---

## Project Structure

```text
EcoProof/
│
├── app.py
├── frontend.py
├── anomaly_model.py
├── alerts.py
├── blockchain.py
├── report.py
├── simulator.py
├── test_upload.py
│
├── sensor_data.csv
├── blockchain_data.json
├── requirements.txt
├── Procfile
│
└── README.md
```

### File Responsibilities

| File                   | Purpose                                        |
| ---------------------- | ---------------------------------------------- |
| `app.py`               | Main application entry point                   |
| `frontend.py`          | Application interface / frontend functionality |
| `anomaly_model.py`     | Pollution anomaly detection logic              |
| `alerts.py`            | Alert generation and monitoring                |
| `blockchain.py`        | Blockchain creation and data verification      |
| `report.py`            | Report generation                              |
| `simulator.py`         | Simulated sensor data generation               |
| `test_upload.py`       | Application testing                            |
| `sensor_data.csv`      | Sample sensor dataset                          |
| `blockchain_data.json` | Stored blockchain data                         |
| `requirements.txt`     | Python dependencies                            |
| `Procfile`             | Deployment configuration                       |

---

## Workflow

```text
Sensor Data
     ↓
Data Processing
     ↓
Anomaly Detection
     ↓
Abnormal Reading?
   ↙       ↘
 Yes        No
  ↓          ↓
Alert      Continue
  ↓
Blockchain Record
  ↓
Report Generation
  ↓
Environmental Monitoring
```

---

## Getting Started

### Prerequisites

Make sure the following are installed:

* Python 3.x
* Git
* pip

### Clone the Repository

```bash
git clone https://github.com/avcusnatsova/Ecoproof.git
cd Ecoproof
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

If the project uses the frontend module as the primary interface, run the corresponding application entry point configured in the repository.

---

## Data Flow

EcoProof uses simulated sensor readings to demonstrate the monitoring pipeline.

```text
Simulated Sensor Readings
          ↓
     Data Storage
          ↓
   Anomaly Detection
          ↓
   ┌──────┴──────┐
   ↓             ↓
Normal        Anomalous
   ↓             ↓
Continue       Alert
                 ↓
          Blockchain Record
                 ↓
             Reporting
```

---

## Blockchain Implementation

The project includes a custom blockchain component for maintaining environmental records.

Each block can contain environmental data along with information used to maintain the relationship between blocks.

This provides a **tamper-evident record** of stored sensor information and demonstrates the application of blockchain concepts to environmental monitoring.

---

## Testing

The repository includes `test_upload.py` for testing application functionality.

Testing can be performed using:

```bash
python test_upload.py
```

Additional test coverage can be added as the application evolves.

---

## Future Improvements

Potential improvements include:

* Integration with real IoT sensors
* Real-time sensor streaming
* Cloud-based data storage
* Advanced ML models for pollution prediction
* Interactive environmental analytics
* Geographic pollution visualization
* Role-based access control
* Real-time notification services
* Production-grade blockchain integration
* Automated model retraining

---

## Learning Outcomes

Developing EcoProof provided practical experience with:

* Python application development
* Machine learning and anomaly detection
* Environmental sensor data processing
* Blockchain fundamentals
* Data integrity and verification
* Alert-driven monitoring systems
* Data visualization and reporting
* Application testing
* Structuring a multi-module software project

---

## Author

**A V Cusnat Sova**
B.E. Computer Science and Engineering
Panimalar Engineering College

GitHub: https://github.com/avcusnatsova

---

## License

This project is available under the MIT License.
