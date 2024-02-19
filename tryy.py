
def encode_combined_x(combined_x):
    encoded_x = []
    for value in combined_x:
        # Convert the value to an integer
        int_value = int(value)
        # Convert the integer to a binary string with 3 bits
        binary_string = format(int_value, '03b')
        # Append the binary string to the encoded_x list
        encoded_x.append(binary_string)
    return encoded_x


# Assuming you have called the quantization function and obtained the combined_x list
combined_x = [1.2, 3.5, 2.8, 4.1, 5.9]

# Encode the combined_x values into 3-bit binary
encoded_x = encode_combined_x(combined_x)

# Print the encoded_x list
print(encoded_x)