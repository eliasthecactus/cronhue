
# Philips Hue Scheduler

## Overview

The **Philips Hue Scheduler** is a Python script that allows you to control Philips Hue lights and rooms on a scheduled interval. You can specify individual devices (by name or ID) or entire rooms (by name or ID) to turn on and off automatically. The script supports case-insensitive matching for device and room names.

---

## Features

- **Control Individual Devices**: Specify device names or IDs to control specific lights.
- **Control Entire Rooms**: Use room names or IDs to control all lights in a room.
- **Flexible Scheduling**: Define the ON duration and the total cycle interval (both in minutes).
- **Case-Insensitive Matching**: Device and room names are case-insensitive.
- **Debug Mode**: Print all available lights and their details (including IDs, names, room names, and brightness) without turning anything on/off.
- **Environment Variables**: Use environment variables instead of arguments for configuration.

---

## Requirements

- **Python**: Version 3.6 or later
- **phue Library**: Install using `pip install phue`
- **Philips Hue Bridge**: Ensure the bridge is connected to your network.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/eliasthecactus/cronhue.git
   cd cronhue
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Basic Command

```
python main.py --bridge-ip <BRIDGE_IP> --device-ids <DEVICE_IDS> --interval <INTERVAL> --duration <DURATION>
```

### Arguments

| Argument         | Description                                                                                       | Example                          |
|-------------------|---------------------------------------------------------------------------------------------------|----------------------------------|
| `--bridge-ip`     | **Required**. The IP address of the Philips Hue Bridge.                                           | `192.168.1.100`                 |
| `--device-ids`    | Comma-separated list of light IDs to control.                                                     | `9,13`                          |
| `--device-names`  | Comma-separated list of light names (case-insensitive) to control.                                | `"Lamp1,Lamp2"`                 |
| `--room-ids`      | Comma-separated list of room IDs to control.                                                      | `81,82`                         |
| `--room-names`    | Comma-separated list of room names (case-insensitive) to control.                                 | `"Living room,Bedroom"`         |
| `--interval`      | Total time (in minutes) for one cycle (lights ON + lights OFF).                                   | `15`                            |
| `--duration`      | Time (in minutes) for which the lights remain ON during each cycle.                               | `5`                             |
| `--debug`         | Prints details of all lights (IDs, names, room names, etc.) without turning lights ON or OFF.     | N/A                             |

## Docker Deployment

### Debug Mode for Setup

1. Edit the debug.docker-compose.yml file and set the BRIDGE_IP environment variable to the IP address of your Hue Bridge.
2. Press the button on the Philips Hue Bridge to authorize the app.
3. Run the following command to fetch the lights:
```bash
docker-compose -f debug.docker-compose.yml up
```
4. This will output the available lights, including their IDs, names, and room assignments.

### Run the Scheduler

After verifying the lights, configure docker-compose.yml with your desired settings:
1. Open docker-compose.yml and edit the following environment variables:
- BRIDGE_IP: IP address of the Hue Bridge.
- DEVICE_IDS, DEVICE_NAMES, ROOM_IDS, ROOM_NAMES: Specify lights or rooms to control.
- INTERVAL, DURATION: Scheduling interval and duration in minutes.
2. Start the scheduler:
```bash
docker-compose up -d
```
3. Stop the scheduler:
```bash
docker-compose down
```

### Docker Environment Variables

| Variable            | Description                                                                                              | Example                          |
|---------------------|----------------------------------------------------------------------------------------------------------|----------------------------------|
| `BRIDGE_IP`         | **Required**: The IP address of your Philips Hue Bridge.                                                | `192.168.1.100`                 |
| `DEVICE_IDS`        | Comma-separated list of light IDs to control.                                                           | `9,13`                          |
| `DEVICE_NAMES`      | Comma-separated list of light names (case-insensitive) to control.                                      | `Lamp1,Lamp2`                   |
| `ROOM_IDS`          | Comma-separated list of room IDs to control.                                                            | `81,82`                         |
| `ROOM_NAMES`        | Comma-separated list of room names (case-insensitive) to control.                                       | `Living room,Bedroom`           |
| `INTERVAL`          | **Required**: Total time (in minutes) for one cycle (lights ON + lights OFF).                           | `15`                            |
| `DURATION`          | **Required**: Time (in minutes) for which the lights remain ON during each cycle.                       | `5`                             |

---

### Examples

#### Turn Lights On and Off
1. Turn on lights with IDs `9` and `13` for 1 minute every 2 minutes:
   ```bash
   python main.py --bridge-ip 192.168.1.100 --device-ids 9,13 --interval 2 --duration 1
   ```

2. Turn on all lights in the "Living room" for 5 minutes every 15 minutes:
   ```bash
   python main.py --bridge-ip 192.168.1.100 --room-names "Living room" --interval 15 --duration 5
   ```

3. Turn on lights in the "Bedroom" and "Office" using room IDs for 10 minutes every 30 minutes:
   ```bash
   python main.py --bridge-ip 192.168.1.100 --room-ids 81,83 --interval 30 --duration 10
   ```

#### Debug Mode
To print all available lights and their details:
   ```bash
   python main.py --bridge-ip 192.168.1.100 --debug
   ```

---

## Notes

1. **Time Units**:
   - The `--interval` and `--duration` arguments are in **minutes**.

2. **Default Values**:
   - If no device or room is specified, the script will throw an error (unless in debug mode).

3. **Case-Insensitive Matching**:
   - Device and room names are compared case-insensitively. For example, `Lamp1` and `lamp1` are treated the same.

4. **Environment Variables**:
   - Instead of passing arguments, you can set environment variables like `BRIDGE_IP`, `DEVICE_IDS`, etc.

---

## Troubleshooting

### Error: "No valid devices found..."
Ensure the device IDs, device names, room IDs, or room names are correct. Use `--debug` to list all available devices and their details.

### Error: "BRIDGE_IP is required..."
Provide the IP address of your Hue Bridge using the `--bridge-ip` argument or the `BRIDGE_IP` environment variable.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Enjoy automating your Philips Hue lights! 🌟 Let me know if you have any issues or feature requests. 😊
