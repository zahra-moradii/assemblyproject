from os.path import isfile


#OPCODE Dictionary
OPCODE_DICT = {"and":(0x20, 0x21),"or" :(0x08, 0x09),"add":(0x00, 0x01), "sub":(0x28, 0x29)}

#Registers with the same size
R8 = ("ah", "al", "bh", "bl", "dh", "dl", "ch", "cl")
R16 = ("ax", "dx", "bx", "cx", "sp", "bp", "si", "di")
R32 = ("eax", "edx", "ebx", "ecx", "esp", "ebp", "esi", "edi")
AllRegisters = R8 + R16 + R32

#Register Dictionary(with the same size)
ARG_OPCODE_DICT = {("al", "al"):0xC0, ("cl", "cl"):0xC9, ("dl", "dl"):0xD2, ("bl", "bl"):0xDB,
                   ("ah", "ah"):0xE4, ("ch", "ch"):0xED, ("dh", "dh"):0xF6, ("bh", "bh"):0xFF,
                   ("al", "cl"):0xC8, ("al", "dl"):0xD0, ("al", "bl"):0xD8,
                   ("ah", "ch"):0xEC, ("ah", "dh"):0xF4, ("ah", "bh"):0xFC,
                   ("cl", "al"):0xC1, ("cl", "dl"):0xD1, ("cl", "bl"):0xD9,
                   ("ch", "ah"):0xE5, ("ch", "dh"):0xF5, ("ch", "bh"):0xFD,
                   ("dl", "al"):0xC2, ("dl", "cl"):0xCA, ("dl", "bl"):0xDA,
                   ("dh", "ah"):0xE6, ("dh", "ch"):0xEE, ("dh", "bh"):0xFE,
                   ("bl", "al"):0xC3, ("bl", "cl"):0xCB, ("bl", "dl"):0xD3,
                   ("bh", "ah"):0xE7, ("bh", "ch"):0xEF, ("bh", "dh"):0xF7,
                   ("ax", "ax"):0xF7, ("cx", "cx"):0xC9, ("dx", "dx"):0xD2, ("bx", "bx"):0xDB,
                   ("ax", "cx"):0xC8, ("ax", "dx"):0xD0, ("ax", "bx"):0xD8,
                   ("cx", "ax"):0xC1, ("cx", "dx"):0xD1, ("cx", "bx"):0xD9,
                   ("dx", "ax"):0xC2, ("dx", "cx"):0xCA, ("dx", "bx"):0xDA,
                   ("bx", "ax"):0xC3, ("bx", "cx"):0xCB, ("bx", "dx"):0xD3,
                   ("sp", "sp"):0xE4, ("bp", "bp"):0xED, ("si", "si"):0xF6, ("di", "di"):0xFF,
                   ("sp", "bp"):0xEC, ("sp", "si"):0xF4, ("sp", "di"):0xFC,
                   ("bp", "sp"):0xE5, ("bp", "si"):0xF5, ("bp", "di"):0xFD,
                   ("si", "sp"):0xE6, ("si", "bp"):0xEE, ("si", "di"):0xFE,
                   ("di", "sp"):0xE7, ("di", "bp"):0xEF, ("di", "si"):0xF7,
                   ("ax", "sp"):0xE0, ("ax", "bp"):0xE8, ("ax", "si"):0xF0, ("ax", "di"):0xF8,
                   ("cx", "sp"):0xE1, ("cx", "bp"):0xE9, ("cx", "si"):0xF1, ("cx", "di"):0xF9,
                   ("bx", "sp"):0xE3, ("bx", "bp"):0xEB, ("bx", "si"):0xF3, ("bx", "di"):0xFB,
                   ("dx", "sp"):0xE2, ("dx", "bp"):0xEA, ("dx", "si"):0xF2, ("dx", "di"):0xFA,
                   ("sp", "ax"):0xC4, ("bp", "ax"):0xC5, ("si", "ax"):0xC6, ("di", "ax"):0xC7,
                   ("sp", "cx"):0xCC, ("bp", "cx"):0xCD, ("si", "cx"):0xCE, ("di", "cx"):0xCF,
                   ("sp", "bx"):0xDC, ("bp", "bx"):0xDD, ("si", "bx"):0xDE, ("di", "bx"):0xDF,
                   ("sp", "dx"):0xd4, ("bp", "dx"):0xD5, ("si", "dx"):0xD6, ("di", "dx"):0xD7,
                   ("eax", "eax"):0xC0, ("ecx", "ecx"):0xC9, ("edx", "edx"):0xD2, ("ebx", "ebx"):0xDB,
                   ("eax", "ecx"):0xC8, ("eax", "edx"):0xD0, ("eax", "ebx"):0xD8,
                   ("ecx", "eax"):0xC1, ("ecx", "edx"):0xD1, ("ecx", "ebx"):0xD9,
                   ("edx", "eax"):0xC2, ("edx", "ecx"):0xCA, ("edx", "ebx"):0xDA,
                   ("ebx", "eax"):0xC3, ("ebx", "ecx"):0xCB, ("ebx", "edx"):0xD3,
                   ("esp", "esp"):0xE4, ("ebp", "ebp"):0xED, ("esi", "esi"):0xF6, ("edi", "edi"):0xFF,
                   ("esp", "ebp"):0xEC, ("esp", "esi"):0xF4, ("esp", "edi"):0xFC,
                   ("ebp", "esp"):0xE5, ("ebp", "esi"):0xF5, ("ebp", "edi"):0xFD,
                   ("esi", "esp"):0xE6, ("esi", "ebp"):0xEE, ("esi", "edi"):0xFE,
                   ("edi", "esp"):0xE7, ("edi", "ebp"):0xEF, ("edi", "esi"):0xF7,
                   ("eax", "esp"):0xE0, ("eax", "ebp"):0xE8, ("eax", "esi"):0xF0, ("eax", "edi"):0xF8,
                   ("ecx", "esp"):0xE1, ("ecx", "ebp"):0xE9, ("ecx", "esi"):0xF1, ("ecx", "edi"):0xF9,
                   ("edx", "esp"):0xE2, ("edx", "ebp"):0xEA, ("edx", "esi"):0xF2, ("edx", "edi"):0xFA,
                   ("ebx", "esp"):0xE3, ("ebx", "ebp"):0xEB, ("ebx", "esi"):0xF3, ("ebx", "ebi"):0xFB,
                   ("esp", "eax"):0xC4, ("ebp", "eax"):0xC5, ("esi", "eax"):0xC6, ("edi", "eax"):0xC7,
                   ("esp", "ecx"):0xCC, ("ebp", "ecx"):0xCD, ("esi", "ecx"):0xCE, ("edi", "ecx"):0xCF,
                   ("esp", "edx"):0xD4, ("ebp", "edx"):0xD5, ("esi", "edx"):0xD6, ("edi", "edx"):0xD7,
                   ("esp", "ebx"):0xDC, ("ebp", "ebx"):0xDD, ("esi", "ebx"):0xDE, ("ebi", "ebx"):0xDF
                  }


#File path input
while True:
    try:
        FileAddress = input("Please enter a file name with extension or full address: ")
        if not FileAddress:
            print("Error: Please enter a proper file name or address.");continue;
        if not isfile(FileAddress):
            print("Error: File not found! Please try again.");continue;
        break;
    except KeyboardInterrupt:
        print("\nCanceled.");exit();


#Main Process
try:
    print("\nOpening file...")
    with open(FileAddress, "r") as SourceFileObject:
        print("Reading content...")
        SourceCode = SourceFileObject.readlines()
except FileNotFoundError:
    input("Error: File not found during process!");exit();
except PermissionError:
    input("Unsuccess: Permission denied!");exit();
except MemoryError:
    input("Unsuccess: Out of memory!");exit();
except KeyboardInterrupt:
    input("Process canceled!");exit();
except EOFError:
    input("Unsuccess: Incompatible file due to EOF.");exit();
except Exception as ex:
    input(f"Error: There was an error during process: {ex}");exit();
print("[Process] Starting to compile")

if not [Line for Line in SourceCode if Line.strip()]:
    print("Empty file.");exit();

CompiledBytes = ""
Successful_Operation = True
i = 1

for Line in SourceCode:
    if ";" in Line:
        Line = Line[:Line.index(";")] #Discarding comment
    Line = Line.strip()
    if " " in Line:
        Instruction = Line[:Line.index(" ")].lower()
        Operands = Line[Line.index(" ") + 1:].lower().replace(" ", "")
        if Instruction not in OPCODE_DICT:
            print(f"Syntax Error: Unsupported instruction or syntax error at line:{i}")
            Successful_Operation = False
            break;
        if "," not in Operands:
            print(f"Syntax Error: Inadequate number of operands at line:{i}\nTwo operands are required.")
            Successful_Operation = False
            break;
        Operands = Operands.split(",")
        Operands[1] = Operands[1].replace("\n", "")
        if len(Operands) > 2:
            print(f"Syntax Error: Excessive number of operands at line:{i}\nOnly two operands are supported.")
            Successful_Operation = False
            break;
        if not (Operands[0] in AllRegisters and Operands[1] in AllRegisters):
            print(f"Syntax Error: At line:{i} operands are not properly defined.\nPlease use register names.")
            Successful_Operation = False
            break;
        if not ((Operands[0] in R8 and Operands[1] in R8) or\
        (Operands[0] in R16 and Operands[1] in R16) or\
        (Operands[0] in R32 and Operands[1] in R32)):
            print(f"Incompatible Source/Destination Error: At line:{i} operands must be the same size.")
            Successful_Operation = False
            break;
        if Operands[0] in R16 and Operands[1] in R16:
            CompiledBytes += "66 "
        OPCODE_INDEX = int((Operands[0] in R16 and Operands[1] in R16) or (Operands[0] in R32 and Operands[1] in R32))
        ByteAboutSave = hex(OPCODE_DICT[Instruction][OPCODE_INDEX])[2:]
        if len(ByteAboutSave) < 2:
            ByteAboutSave = "0" + ByteAboutSave
        CompiledBytes += ByteAboutSave + " "
        ByteAboutSave = hex(ARG_OPCODE_DICT[(Operands[0], Operands[1])])[2:]
        if len(ByteAboutSave) < 2:
            ByteAboutSave = "0" + ByteAboutSave
        CompiledBytes += ByteAboutSave + " "
    elif len(Line) > 0:
        print(f"Syntax Error: Unsupported instruction or syntax error at line:{i}")
        Successful_Operation = False
        break;
    i += 1
if Successful_Operation:
    CompiledBytes = CompiledBytes.upper()
    print("\nSuccessful Compile: Process completed!")
    print("Output:\n")
    print(CompiledBytes)
try:
    input("\nPress ENTER to continue...")
except KeyboardInterrupt:
    pass