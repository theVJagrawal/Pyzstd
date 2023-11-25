import sys
import os
import pyzstd as pz
import time
import csv
import subprocess

# Set the output folder path
output_folder = "E:\\SAT\\RESULTS"

def clear_caches():
    try:
        # Clear the page cache, dentries, and inodes
        subprocess.call(["sync"])
        subprocess.call(["echo", "1", ">", "/proc/sys/vm/drop_caches"])
        subprocess.call(["echo", "2", ">", "/proc/sys/vm/drop_caches"])
    except Exception as e:
        print(f"An error occurred while clearing caches: {e}")

def get_cpu_utilization(pid):
    try:
        # Run the 'ps' command to get CPU utilization
        ps_output = subprocess.check_output(["ps", "-p", str(pid), "-o", "%cpu"]).decode("utf-8")
        lines = ps_output.strip().split('\n')
        if len(lines) > 1:
            cpu_percent = float(lines[1])
            return cpu_percent
    except Exception as e:
        print(f"An error occurred while getting CPU utilization: {e}")
    return 0.0

def get_memory_utilization(pid):
    try:
        # Run the 'ps' command to get memory utilization
        ps_output = subprocess.check_output(["ps", "-p", str(pid), "-o", "%mem"]).decode("utf-8")
        lines = ps_output.strip().split('\n')
        if len(lines) > 1:
            memory_percent = float(lines[1])
            return memory_percent
    except Exception as e:
        print(f"An error occurred while getting memory utilization: {e}")
    return 0.0

def compress_and_measure(input_file_path, compression_level):
    try:
        # Read the input file
        with open(input_file_path, 'rb') as input_file:
            original_data = input_file.read()

        # Measure CPU time
        start_time = time.process_time()
        compressed_data = pz.richmem_compress(original_data, compression_level)
        end_time = time.process_time()

        # Calculate compression ratio
        compression_ratio = len(original_data) / len(compressed_data)

        # Calculate CPU time in seconds
        cpu_time = end_time - start_time

        # Get the PID of the current process
        current_process_pid = os.getpid()

        # Measure CPU utilization using 'ps' command
        cpu_percent = get_cpu_utilization(current_process_pid)
        
        # Measure memory utilization using 'ps' command
        memory_percent = get_memory_utilization(current_process_pid)

        return (
            compression_level,
            compression_ratio,
            cpu_time,
            cpu_percent,
            memory_percent
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compress_file.py <input_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]

    # Create a CSV file to store the results
    csv_filename = os.path.join(output_folder, "cmp1000_2compression_results.csv")
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            "Compression Level",
            "Compression Ratio",
            "CPU Time (s)",
            "CPU Utilization",
            "Memory Utilization"
        ])

        # Loop through compression levels from 1 to 22
        for compression_level in range(1, 23):
            # Clear caches before each compression level
            clear_caches()

            # Add a 2-second sleep
            time.sleep(2)

            # Perform compression and measurement
            result = compress_and_measure(input_file_path, compression_level)

            if result is not None:
                (
                    compression_level,
                    compression_ratio,
                    cpu_time,
                    cpu_percent,
                    memory_percent
                ) = result

                # Write results to the main CSV file
                csv_writer.writerow([
                    compression_level,
                    compression_ratio,
                    cpu_time,
                    cpu_percent,
                    memory_percent
                ])

                print(f"Results for Compression Level {compression_level}:")
                print(f"Compression Ratio: {compression_ratio:.2f}")
                print(f"CPU Time (s): {cpu_time:.2f}")
                print(f"CPU Utilization: {cpu_percent:.2f}%")
                print(f"Memory Utilization: {memory_percent:.2f}%")
                print("-" * 30)

    print(f"All compression and measurement levels completed. Results saved to {csv_filename}")
