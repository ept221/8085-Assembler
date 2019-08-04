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
    'ADI',
    'ACI',
    'SUI',
    'SBI',
    'STA',
    'LDA',
    'SHLD',
    'LHLD',
    'JMP',
    'JC',
    'JNC',
    'JZ',
    'JNZ',
    'JP',
    'JM',
    'JPE',
    'JPO',
    'CALL',
    'CC',
    'CNC',
    'CZ',
    'CNZ',
    'CP',
    'CM',
    'CPE',
    'CPO',
    'IN',
    'OUT',
    'ANI',
    'XRI', 
    'ORI',
    'CPI',
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
	'MVI',
    'LXI',
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
}

reserved =  bin_op | uni_op | mnm_0 | mnm_0_e | mnm_1 | mnm_1_e | mnm_2 | drct_1 | drct_p | drct_w | reg 