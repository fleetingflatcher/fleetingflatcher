import sys

# print("hex_to_c.py unimplemented.")
# exit()

# Reading the hex data from a file
with open(sys.argv[1], 'rb') as file:
    escseq_hex = file.read().strip()
    hex_data = [f'{byte:02X}' for byte in escseq_hex]

#   Formatting the values to C-style hex 
#   adding CRLF after every 8 bytes
#   separating each 8x8 byte segment into a page
#   separating each four pages with a marker
bytes_per_line = 8
lines_per_page = 8
pages_per_row = 4

row_num = 1
array_len = 0

c_byte_array = "uint8_t variableName[] = { \n\t\t// Row 0\n\t"
for index, byte in enumerate(hex_data):
    c_byte_array += f"0x{byte}"
    array_len += 1
    if (index + 1) % bytes_per_line == 0:
        c_byte_array += ",\n\t"
    else:
        c_byte_array += ", "

    if (index + 1) % (bytes_per_line*lines_per_page) == 0:
        c_byte_array += "\n\t"
    if (index + 1) % (bytes_per_line*lines_per_page*pages_per_row) == 0:
        c_byte_array += f"\n\t\t// Row {row_num}\n\t"
        row_num += 1
    

# Removing the trailing comma and space if present
if c_byte_array.endswith(", "):
    c_byte_array = c_byte_array[:-2]

c_byte_array += "\n};\n"

# Writing the C byte array to another file
with open('hex_to_c_output.txt', 'w') as file:
    file.write(c_byte_array)

print("C byte array has been written to hex_to_c_output.txt\nSize of C array is ", array_len, " bytes.")
