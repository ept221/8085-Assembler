bin_op = {
    '+',
    '-',
}

uni_op = {
    '+',
    '-'
}

mnm_0 = {
	'XCHG',
	'XTHL',
	'SPHL',
	'PCHL',
	'RET',
	'RC',
	'RNC',
	'RZ',
	'RNZ',
	'RP',
	'RM',
	'RPE',
	'RPO',
	'RLC',
	'RRC',
	'RAL',
	'RAR',
	'CMA',
	'STC',
	'CMC',
	'DAA',
	'EI',
	'DI',
	'NOP',
	'HLT',
	'RIM',
	'SIM',
}

mnm_0_e = {
    'ADI': "data",
    'ACI': "data",
    'SUI': "data",
    'SBI': "data",
    'STA': "address",
    'LDA': "address",
    'SHLD': "address",
    'LHLD': "address",
    'JMP': "address",
    'JC': "address",
    'JNC': "address",
    'JZ': "address",
    'JNZ': "address",
    'JP': "address",
    'JM': "address",
    'JPE': "address",
    'JPO': "address",
    'CALL': "address",
    'CC': "address",
    'CNC': "address",
    'CZ': "address",
    'CNZ': "address",
    'CP': "address",
    'CM': "address",
    'CPE': "address",
    'CPO': "address",
    'IN': "data",
    'OUT': "data",
    'ANI': "data",
    'XRI': "data", 
    'ORI': "data",
    'CPI': "data",
}

mnm_1 = {
    'STAX',
    'LDAX',
    'PUSH',
    'POP',
    'RST',
    'INR',
    'DCR',
    'INX',
    'DCX',
    'ADD',
    'ADC',
    'DAD', 
    'SUB',
    'SBB',
    'ANA',
    'XRA',
    'ORA',
    'CMP',
}

mnm_1_e = {
	'MVI': "data",
    'LXI': "address",
}

mnm_2 = {
	'MOV',
}

drct_1 = {
	'ORG',
	'DS'
}

drct_p = {
	'DB',
}

drct_w = {
	'EQU'
}

drct_s = {
    'STRING'
}

reg = {
    'A',
    'B',
    'C',
    'D',
    'E',
    'H',
    'L',
    'SP',
    'PSW',
    'M',
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7'
}

reserved_mnm_0_e = {key for key in mnm_0_e}
reserved_mnm_1_e = {key for key in mnm_1_e}
reserved =  bin_op | uni_op | mnm_0 | reserved_mnm_0_e | mnm_1 | reserved_mnm_1_e | mnm_2 | drct_1 | drct_p | drct_w | reg 