# Radio Link Monitoring System 

## Overview
A comprehensive web-based monitoring system for radio link networks, specifically designed for [...] infrastructure in [...] . This application provides real-time monitoring and management of radio bridges (ponti radio) across different locations.

## Features
- **Real-time Monitoring**: Live monitoring of radio link status and performance metrics
- **Multi-vendor Support**: Compatible.
- **SNMP Integration**: Uses SNMP protocol for equipment data retrieval
- **Interactive UI**: Modern, responsive web interface with filtering capabilities
- **Network Topology**: Complete visualization of the radio link network
- **Performance Metrics**: Monitoring of key parameters including:
  - Signal strength (RX Field)
  - Transmission power (TX Power)
  - LDPC Stress levels
  - Bitrate measurements
  - Equipment alarms and status

## Technical Specifications

### Backend
- **Framework**: Flask (Python)
- **SNMP Library**: pysnmp
- **GUI Interface**: FlaskWebGUI
- **Network Protocol**: SNMP v1

### Frontend
- **Framework**: Bootstrap 5
- **Styling**: Custom CSS with responsive design
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Icons**: Font Awesome

### Network Features
- Bidirectional link monitoring
- IP-based equipment access

## System Requirements
- Python 3.x
- Flask
- pysnmp
- flaskwebgui
- Modern web browser with JavaScript enabled
- Network access to radio equipment

### Monitoring Features
- Real-time data extraction via SNMP
- Color-coded status indicators
- Performance thresholds monitoring
- Equipment-specific parameter display
![pontiscan](https://github.com/user-attachments/assets/4ebd66ee-4b4c-4641-900a-371d84c272cd)
