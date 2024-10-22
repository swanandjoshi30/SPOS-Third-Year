def pass1_macroprocessor(source_code):
    mnt = {}  # Macro Name Table
    mdt = []  # Macro Definition Table
    intermediate_code = []  # Lines of code without macros being expanded
    macro_def = False  # Flag to check if we're inside a macro definition
    macro_name = None  # To hold the current macro name

    # Process each line of the source code
    for line in source_code:
        tokens = line.strip().split()

        # Check if the line starts a macro definition
        if tokens[0] == "MACRO":
            macro_def = True  # We're inside a macro definition now
        elif macro_def and not macro_name:
            # First line after 'MACRO' is the macro name
            macro_name = tokens[0]
            mnt[macro_name] = len(mdt)  # Add the macro to the MNT with MDT index
        elif macro_def and tokens[0] == "MEND":
            # End of macro definition
            macro_def = False  # Exit the macro definition block
            macro_name = None  # Reset the macro name
        elif macro_def:
            # If we're inside a macro definition, add the line to the MDT
            mdt.append(line.strip())
        else:
            # For non-macro lines, add them to intermediate code
            intermediate_code.append(line.strip())

    return mnt, mdt, intermediate_code

# Example usage of the Pass 1 macroprocessor
source_code = [
    "MACRO", 
    "INCR &ARG", 
    "ADD &ARG, 1", 
    "MEND",
    "START", 
    "MOV A, B", 
    "INCR A", 
    "END"
]

mnt, mdt, intermediate_code = pass1_macroprocessor(source_code)

# Output the results of Pass 1
print("MNT:", mnt)  # Macro Name Table
print("MDT:", mdt)  # Macro Definition Table
print("Intermediate Code:", intermediate_code)  # Intermediate code