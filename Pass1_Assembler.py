# Pass 1 Assembler
def pass1_assembler(source_code):
    # Define the operation table (OPTAB) with instruction sizes
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

# Run Pass 1
SYMTAB, intermediate_code = pass1_assembler(source_code)
print("Symbol Table (SYMTAB):", SYMTAB)
print("Intermediate Code:")
for entry in intermediate_code:
    print(entry)
