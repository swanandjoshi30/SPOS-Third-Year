def pass2_macroprocessor(mnt, mdt, intermediate_code):
    expanded_code = []  # List to store the final expanded code

    for line in intermediate_code:
        tokens = line.split()  # Split the line into tokens (e.g., "INCR A" -> ["INCR", "A"])

        # Check if the first token is a macro name in the MNT
        if tokens[0] in mnt:
            macro_name = tokens[0]  # The macro name (e.g., "INCR")
            macro_start = mnt[macro_name]  # Get the index of the macro's definition in MDT
            actual_arg = tokens[1]  # The actual argument (e.g., "A")

            # Expand the macro by replacing formal arguments with the actual argument
            for macro_line in mdt[macro_start:]:
                # Substitute the formal parameter &ARG with the actual argument
                expanded_line = macro_line.replace("&ARG", actual_arg)
                expanded_code.append(expanded_line)

        else:
            # If it's not a macro, add the line as-is to the expanded code
            expanded_code.append(line)

    return expanded_code

# Example usage for Pass-II
source_code = [
    "MACRO", "INCR &ARG", "ADD &ARG, 1", "MEND",
    "START", "MOV A, B", "INCR A", "END"
]

mnt = {'INCR': 0}  # Macro Name Table from Pass 1
mdt = ['ADD &ARG, 1']  # Macro Definition Table from Pass 1
intermediate_code = ['START', 'MOV A, B', 'INCR A', 'END']  # Intermediate Code from Pass 1

# Running Pass 2
expanded_code = pass2_macroprocessor(mnt, mdt, intermediate_code)

# Output the expanded code
print("Expanded Code:")
for line in expanded_code:
    print(line)