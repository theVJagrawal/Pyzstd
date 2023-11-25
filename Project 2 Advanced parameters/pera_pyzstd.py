import subprocess

# Define the input file name
input_file = "E:/SAT/dataset/c10.tar"

# Define the output file name
output_file = "E:\\SAT\\PeraOutput\\compressed_custom_parameters_high70000000.zst"

# Define your custom compression parameters
custom_parameters = [
    "-27",   # windowLog: 2^()
    "-27",    # chainLog
    "-25",   # hashLog
    "-9",    # searchLog
    "-3",      #minMatch
    "-999",     #targetLength
    "-9"     # strategy (9 for max compression)
]

# Full path to the zstd executable
zstd_executable = "C:\\zstd-v1.5.5-win32\\zstd.exe"

# Run the zstd command with custom parameters
subprocess.run([zstd_executable, *custom_parameters, input_file, "-o", output_file])
