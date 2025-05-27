import logging

# Average passing times per vehicle class (customized by region/intersection)
average_times = {
    "car": 2.5,
    "minibus": 3.5,
    "auto": 2.0,
    "bus": 4.5,
    "motorbike": 1.5,
    "pickup": 3.0,
    "suv": 2.7,
    "taxi": 2.5,
    "truck": 5.0,
    "van": 3.0,
    "three_wheeler": 2.0,
}


# Calculate Green Signal Time (GST) based on the number of lanes and vehicle counts
def calculate_green_signal_time(vehicle_counts, num_lanes, average_times):
    numerator = sum(
        vehicle_counts.get(vehicle, 0) * average_times.get(vehicle, 0)
        for vehicle in vehicle_counts
    )

    green_signal_time = numerator / (num_lanes + 1)

    # Enforce minimum and maximum green times
    MIN_GREEN_TIME = 10  # seconds
    MAX_GREEN_TIME = 60  # seconds
    return max(MIN_GREEN_TIME, min(green_signal_time, MAX_GREEN_TIME))


# Simulate traffic signal control in cyclic fashion
def signal_controller_cycle(
    intersections,
    average_times=average_times,
    num_lanes=2,
):

    vehicle_counts = intersections  # Directly using passed vehicle counts
    logging.info(f"Detected vehicles: {vehicle_counts}")

    gst = calculate_green_signal_time(vehicle_counts, num_lanes, average_times)
    logging.info(f"Signal is GREEN for {gst} seconds.")

    # Simulate green signal

    # Yellow signal for 3 seconds
    logging.info("Signal is YELLOW for 3 seconds.")

    # Red signal by default when not green or yellow
    logging.info("Signal is RED.\n")

    return gst  # Return the green signal time for further processing if needed
