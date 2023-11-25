import pyzstd

# Define the input file name
input_file = "E:/SAT/dataset/c10.tar"

# Define the output file name
output_file = "E:\\SAT\\PeraOutput\\compressed_custom_level_22222.zst"

# Choose a predefined compression level
# The following constants are available: FAST, DEFAULT, MAX, COMPRESSION_LEVEL_1, ..., COMPRESSION_LEVEL_19
compression_level = 22  # Adjust the level as needed

# Read the input file
with open(input_file, 'rb') as f:
    input_data = f.read()

# Compress data using the chosen compression level
compressed_data = pyzstd.compress(input_data, compression_level)

# Print the parameter values
print(f"Compression Level: {compression_level}")
print(f"Window Log: {compression_level.windowLog}")
print(f"Chain Log: {compression_level.chainLog}")
print(f"Hash Log: {compression_level.hashLog}")
print(f"Search Log: {compression_level.searchLog}")
print(f"Target Length: {compression_level.targetLength}")


# Calculate the compression ratio
compression_ratio = len(input_data) / len(compressed_data)

# Write the compressed data to an output file
with open(output_file, 'wb') as f:
    f.write(compressed_data)

print("Compression Level:")
print(f"Original Data Length: {len(input_data)} bytes")
print(f"Compressed Data Length: {len(compressed_data)} bytes")
print(f"Compression Ratio: {compression_ratio:.2f}")

# To decompress the data, you can use a similar approach.
# Remember to change the file paths and compression level accordingly.
