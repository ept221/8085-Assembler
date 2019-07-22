
# symbol: [number of bytes instruction and arguments will take] [number of bound arguments] [number of non-bound arguments]
mnemonics = {
    #Move, Load, Store
    'MOV':  [1, 2, "none"],
    'MVI':  [2, 1, "data"],
    'LXI':  [3, 1, "address"],
    'STAX': [1, 1, "none"],
    'LDAX': [1, 1, "none"],
    'STA':  [3, 0, "address"],
    'LDA':  [3, 0, "address"],
    'SHLD': [3, 0, "address"],
    'LHLD': [3, 0, "address"],
    'XCHG': [1, 0, "none"],

    #Stack
    'PUSH': [1, 1, "none"],
    'POP':  [1, 1, "none"],
    'XTHL': [1, 0, "none"],
    'SPHL': [1, 0, "none"],

    #Jump
    'JMP':  [3, 0, "address"],
    'JC':   [3, 0, "address"],
    'JNC':  [3, 0, "address"],
    'JZ':   [3, 0, "address"],
    'JNZ':  [3, 0, "address"],
    'JP':   [3, 0, "address"],
    'JM':   [3, 0, "address"],
    'JPE':  [3, 0, "address"],
    'JPO':  [3, 0, "address"],
    'PCHL': [1, 0, "none"],

    #Call
    'CALL': [3, 0, "address"],
    'CC':   [3, 0, "address"],
    'CNC':  [3, 0, "address"],
    'CZ':   [3, 0, "address"],
    'CNZ':  [3, 0, "address"],
    'CP':   [3, 0, "address"],
    'CM':   [3, 0, "address"],
    'CPE':  [3, 0, "address"],
    'CPO':  [3, 0, "address"],

    #Return
    'RET':  [1, 0, "none"],
    'RC':   [1, 0, "none"],
    'RNC':  [1, 0, "none"],
    'RZ':   [1, 0, "none"],
    'RNZ':  [1, 0, "none"],
    'RP':   [1, 0, "none"],
    'RM':   [1, 0, "none"],
    'RPE':  [1, 0, "none"],
    'RPO':  [1, 0, "none"],

    #Restart
    'RST':  [1, 1, "none"],

    #Input, Output
    'IN':   [1, 0, "data"],
    'OUT':  [1, 0, "data"],

    #Increment, Decrement
    'INR':  [1, 1, "none"],
    'DCR':  [1, 1, "none"],
    'INX':  [1, 1, "none"],
    'DCX':  [1, 1, "none"],

    #Add
    'ADD':  [1, 1, "none"],
    'ADC':  [1, 1, "none"],
    'ADI':  [2, 0, "data"],
    'ACI':  [2, 0, "data"],
    'DAD':  [1, 1, "none"], 

    #Subtract
    'SUB':  [1, 1, "none"],
    'SBB':  [1, 1, "none"],
    'SUI':  [2, 0, "data"],
    'SBI':  [2, 0, "data"],

    #Logical
    'ANA':  [1, 1, "none"],
    'XRA':  [1, 1, "none"],
    'ORA':  [1, 1, "none"],
    'CMP':  [1, 1, "none"],
    'ANI':  [2, 0, "data"],
    'XRI':  [2, 0, "data"], 
    'ORI':  [2, 0, "data"],
    'CPI':  [2, 0, "data"],

    #Rotate
    'RLC':  [1, 0, "none"],
    'RRC':  [1, 0, "none"],
    'RAL':  [1, 0, "none"],
    'RAR':  [1, 0, "none"],
    
    #Specials
    'CMA':  [1, 0, "none"],
    'STC':  [1, 0, "none"],
    'CMC':  [1, 0, "none"],
    'DAA':  [1, 0, "none"],

    #Control
    'EI':   [1, 0, "none"],
    'DI':   [1, 0, "none"],
    'NOP':  [1, 0, "none"],
    'HLT':  [1, 0, "none"],

    #New
    'RIM':  [1, 0, "none"],
    'SIM':  [1, 0, "none"],
}

reserved = {
    'A': 1,
    'B': 1,
    'C': 1,
    'D': 1,
    'E': 1,
    'H': 1,
    'L': 1,
    'SP': 1,
    'PSW': 1,
    'M': 1,
}

def numOfArgs(mnemonic):
    n = mnemonics[mnemonic][1]
    if(mnemonics[mnemonic][2] != "none"):
        n += 1
    return n

def numOfMArgs(mnemonic):
    n = mnemonics[mnemonic][1];
    return n

directives = {
    "ORG": 1,
    "DB":  2,
    "EQU": 3,
    "DS":  4,
}

    
