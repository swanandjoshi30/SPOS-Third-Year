# Pass 1 Assembler
def pass1_assembler(source_code):
    OPTAB = {
        "MOV": {"opcode": "01", "size": 2},
        "ADD": {"opcode": "02", "size": 2},
        "SUB": {"opcode": "03", "size": 2},
        "INCR": {"opcode": "04", "size": 2}
    }

    LC = 0  # Location counter
    SYMTAB = {}  # Symbol Table
    intermediate_code = []  # List to store intermediate code
    macro_def = False  # Flag to track macro definition

    for line in source_code:
        tokens = line.strip().split()  # Split the line into tokens

        # Check for macro definition
        if tokens[0] == "MACRO":
            macro_def = True
            continue
        elif macro_def:
            if tokens[0] == "MEND":
                macro_def = False
                continue
            else:
                # Process macro definition (you may want to store it)
                continue

        # Handle START directive
        if tokens[0] == "START":
            LC = int(tokens[1])  # Set location counter to the specified value
            intermediate_code.append((LC, None, "START", tokens[1]))
            continue

        # Handle END directive
        if tokens[0] == "END":
            intermediate_code.append((LC, None, "END", None))
            break

        # Handle labels and instructions
        if len(tokens) == 3:  # Label + Mnemonic + Operand
            label, mnemonic, operand = tokens
            SYMTAB[label] = LC  # Add label to symbol table
        elif len(tokens) == 2:  # Mnemonic + Operand
            label = None
            mnemonic, operand = tokens
        else:
            continue  # Ignore invalid lines

        # Increment location counter based on instruction size
        if mnemonic in OPTAB:
            LC += OPTAB[mnemonic]["size"]
            intermediate_code.append((LC, label, mnemonic, operand))

    return SYMTAB, intermediate_code

# Example source code for testing Pass 1
source_code = [
    "MACRO",
    "INCR &ARG",
    "ADD &ARG, 1",
    "MEND",
    "START 1000",
    "MOV A, B",
    "INCR A",
    "END"
]

# Run Pass 1 to get SYMTAB and Intermediate Code
SYMTAB, intermediate_code = pass1_assembler(source_code)

# Pass 2 Assembler
def pass2_assembler(SYMTAB, intermediate_code):
    OPTAB = {
        "MOV": {"opcode": "01", "size": 2},
        "ADD": {"opcode": "02", "size": 2},
        "SUB": {"opcode": "03", "size": 2},
        "INCR": {"opcode": "04", "size": 2}
    }

    machine_code = []  # List to store machine code

    for entry in intermediate_code:
        LC, label, mnemonic, operand = entry

        # Handle END directive
        if mnemonic == "END":
            machine_code.append(f"{LC:04X} {mnemonic}")
            break

        # Handle instructions
        if mnemonic in OPTAB:
            opcode = OPTAB[mnemonic]["opcode"]

            # Check if the operand is a label in the symbol table
            if operand in SYMTAB:  
                address = SYMTAB[operand]
            else:
                # Handle the case where operand is numeric or immediate value
                try:
                    address = int(operand)  # Convert operand to an integer if it's numeric
                except ValueError:
                    print(f"Error: Operand '{operand}' is not a valid numeric or label.")
                    continue  # Skip this line if operand is not valid

            machine_code.append(f"{LC:04X} {opcode} {address:04X}")
        else:
            if mnemonic == "WORD":
                machine_code.append(f"{LC:04X} {int(operand):06X}")
            elif mnemonic == "BYTE":
                # Handle BYTE pseudo-op (simplified)
                constant = operand[2:-1]  # Remove C' and '
                hex_value = ''.join([f"{ord(c):02X}" for c in constant])
                machine_code.append(f"{LC:04X} {hex_value}")
            elif mnemonic in ["RESW", "RESB"]:
                machine_code.append(f"{LC:04X} ---- (Reserved)")

    return machine_code

# Example Usage
source_code = [
    "MACRO",
    "INCR &ARG",
    "ADD &ARG, 1",
    "MEND",
    "START 1000",
    "MOV A, B",
    "INCR A",
    "END"
]

# Run Pass 1 to get SYMTAB and Intermediate Code
SYMTAB, intermediate_code = pass1_assembler(source_code)

# Run Pass 2 using the output from Pass 1
machine_code = pass2_assembler(SYMTAB, intermediate_code)

# Display the Machine Code
print("Machine Code:")
for code in machine_code:
    print(code)
