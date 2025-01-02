import os
import sys
import time
import argparse
from phue import Bridge

def get_config():
    """Parse arguments and environment variables for configuration."""
    parser = argparse.ArgumentParser(description="Control Philips Hue devices on a schedule.")
    
    # Command-line arguments
    parser.add_argument("--bridge-ip", help="IP address of the Hue Bridge")
    parser.add_argument("--device-ids", help="Comma-separated list of device IDs to control")
    parser.add_argument("--device-names", help="Comma-separated list of device names to control")
    parser.add_argument("--room-ids", help="Comma-separated list of room IDs to control")
    parser.add_argument("--room-names", help="Comma-separated list of room names to control")
    parser.add_argument("--interval", type=int, help="Interval in minutes between ON cycles")
    parser.add_argument("--duration", type=int, help="Duration in minutes to keep devices ON")
    parser.add_argument("--debug", action="store_true", help="Log details of all lights and exit")

    args = parser.parse_args()

    # Configuration priority: Arguments > Environment Variables
    config = {
        "bridge_ip": args.bridge_ip or os.getenv("BRIDGE_IP"),
        "device_ids": args.device_ids.split(",") if args.device_ids else os.getenv("DEVICE_IDS", "").split(","),
        "device_names": args.device_names.split(",") if args.device_names else os.getenv("DEVICE_NAMES", "").split(","),
        "room_ids": args.room_ids.split(",") if args.room_ids else os.getenv("ROOM_IDS", "").split(","),
        "room_names": args.room_names.split(",") if args.room_names else os.getenv("ROOM_NAMES", "").split(","),
        "interval": args.interval or os.getenv("INTERVAL"),
        "duration": args.duration or os.getenv("DURATION"),
        "debug": args.debug,
    }

    # Validate configuration
    if not config["bridge_ip"]:
        print("Error: BRIDGE_IP is required (set as --bridge-ip or environment variable).")
        sys.exit(1)
    if not config["debug"] and not (config["device_ids"] or config["device_names"] or config["room_ids"] or config["room_names"]):
        print("Error: At least one of DEVICE_IDS, DEVICE_NAMES, ROOM_IDS, or ROOM_NAMES must be provided unless using --debug.")
        sys.exit(1)
    if not config["interval"] and not config["debug"]:
        print("Error: INTERVAL is required (set as --interval or environment variable).")
        sys.exit(1)
    if not config["duration"] and not config["debug"]:
        print("Error: DURATION is required (set as --duration or environment variable).")
        sys.exit(1)

    if not config["debug"]:
        try:
            config["interval"] = int(config["interval"])
            config["duration"] = int(config["duration"])
        except ValueError:
            print("Error: INTERVAL and DURATION must be integers.")
            sys.exit(1)

    return config

def log_light_details(lights, bridge):
    """Logs details of all lights in one line per device, including room names and room IDs."""
    # Fetch all groups (rooms) from the bridge
    groups = bridge.get_group()

    # Create a mapping of light IDs to room names and room IDs
    light_to_room = {}
    for group_id, group_data in groups.items():
        room_name = group_data['name']
        for light_id in group_data['lights']:
            light_to_room[light_id] = {"room_name": room_name, "room_id": group_id}

    # Log details of each light
    print("Available lights:")
    for light in lights:
        try:
            brightness = light.brightness  # Access brightness if it exists
        except KeyError:
            brightness = "N/A"  # If brightness is not available, mark it as N/A

        # Get the room details, default to "Unassigned" if not in a group
        room_details = light_to_room.get(
            str(light.light_id), {"room_name": "Unassigned", "room_id": "N/A"}
        )

        # Print all details in one line
        print(
            f"ID: {light.light_id}, Name: {light.name}, Room: {room_details['room_name']} (ID: {room_details['room_id']}), "
            f"On: {light.on}, Brightness: {brightness}"
        )

def main():
    # Get configuration
    config = get_config()

    # Connect to the bridge
    bridge = Bridge(config["bridge_ip"])
    bridge.connect()

    # Get all groups (rooms) and lights
    groups = bridge.get_group()
    all_lights_by_id = {str(light.light_id): light for light in bridge.lights}
    all_lights_by_name = {light.name.lower(): light for light in bridge.lights}

    # Debug mode: Log light details and exit
    if config["debug"]:
        log_light_details(bridge.lights, bridge)
        sys.exit(0)

    # Resolve devices by ID, name, and rooms
    devices = {}

    # Add devices by ID
    for device_id in config["device_ids"]:
        if device_id in all_lights_by_id:
            devices[device_id] = all_lights_by_id[device_id]
        else:
            print(f"Warning: No device found with ID {device_id}")

    # Add devices by name
    for device_name in config["device_names"]:
        if device_name.lower() in all_lights_by_name:
            devices[device_name] = all_lights_by_name[device_name.lower()]
        else:
            print(f"Warning: No device found with name '{device_name}'")

    # Add lights from specified room IDs
    for room_id in config["room_ids"]:
        if room_id in groups:
            for light_id in groups[room_id]['lights']:
                if light_id in all_lights_by_id:
                    devices[light_id] = all_lights_by_id[light_id]
            print(f"Added lights from room ID: {room_id} ({groups[room_id]['name']})")
        else:
            print(f"Warning: No room found with ID '{room_id}'")

    # Add lights from specified room names
    for room_name in config["room_names"]:
        for group_id, group_data in groups.items():
            if room_name.lower() == group_data['name'].lower():
                for light_id in group_data['lights']:
                    if light_id in all_lights_by_id:
                        devices[light_id] = all_lights_by_id[light_id]
                print(f"Added lights from room: {group_data['name']} (ID: {group_id})")
                break
        else:
            print(f"Warning: No room found with name '{room_name}'")

    if not devices:
        print("Error: No valid devices found from the provided DEVICE_IDS, DEVICE_NAMES, ROOM_IDS, or ROOM_NAMES.")
        sys.exit(1)

    # Control devices in a loop
    while True:
        # Turn devices on
        for device in devices.values():
            device.on = True
        print("Devices turned on")

        time.sleep(config["duration"] * 60)

        # Turn devices off
        for device in devices.values():
            device.on = False
        print("Devices turned off")

        time.sleep((config["interval"] - config["duration"]) * 60)

if __name__ == "__main__":
    main()
