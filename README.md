# 8085-Assembler

A simple 8085 assembler.

## Usage
```
usage: assembler.py [-h] [-L] [-A] [-B] [-I] [-H] [-C] [-s] [-o OUT] source

A simple 8085 assembler.

positional arguments:
  source             source file

optional arguments:
  -h, --help         show this help message and exit
  -L, --lineNum      include the line number in output
  -A, --address      include the address in output
  -B, --label        include the labels in output
  -I, --instruction  include the instructions and arguments in output
  -H, --hex          include the hex code in output
  -C, --comment      include the comments in output
  -s, --standard     equivalent to -A -B -I -H -C
  -o OUT, --out OUT  output file name (stdout, if not specified)
  ```
## Source File Syntax
The assembler is case insensitive.

### Comments
Comments begin with semicolons.
```asm
MVI A, 0x5C ; This is a comment
```

### Constants
8 and 16-bit constants are given in hex. 8-bit constants must have two digits, and 16-bit constants must have 4-digits.
```asm
MVI A, 0x0C
MVI A, 0C   ; The "0x" is optional
MVI A, 7    ; Illegal. 8-bit constants must have two digits

LXI 0x03B7
LXI 03B7    ; The "0x" is optional
LXI 3B7     ; Illegal. 16-bit constants must have four digits
```
If an 8-bit constant is given where a 16-bit constant is expected, the 8-bit constant will be converted to a 16-bit constant, with the upper 8-bits all zero.
```asm
JNZ 0x3FC7  ; Jump-not-zero to 0x3FC7
JMP FF      ; JMP takes a 16-bit argument, but given 8-bits. Will JMP to 0x00FF
```

### Label Definitions
Label definitions may be any string ending with a colon, where the string does not match the pattern of an 8 or 16-bit constant.

```asm
  ; A simple loop
  
        MVI A, 0x5C
  Foo:  DCR A         ; Label definition
        JNZ Foo       ; Jump-not-zero to Foo
  ;*******************************************************************************
  
        MVI A, 0x5C
  FD:   DCR A         ; Illegal. Label definition cannot match hex constant format
        JNZ FD
```
### Directives
#### ORG <16-bit-address>
Sets the origin to the given address.
```asm
; Example
;*******************************************************************************
        MVI A, 55
        OUT 42
        JMP Start
        ORG 0x44
Start:  MVI A, 32
        OUT 42
;*******************************************************************************
; Assembles to the following:

Address             Label               Instruction         Hex Code            
--------------------------------------------------------------------------------
0x0000                                  MVI A, 55           0x3E                
0x0001                                                      0x55                
0x0002                                  OUT 42              0xD3                
0x0003                                                      0x42                
0x0004                                  JMP START           0xC3                
0x0005                                                      0x44                
0x0006                                                      0x00                
0x0044              START:              MVI A, 32           0x3E                
0x0045                                                      0x32                
0x0046                                  OUT 42              0xD3                
0x0047                                                      0x42  
```
#### DB <8-bit-data>, ...
Writes one or more data bytes sequentially into memory.
```asm
; Example
;***********************************************************
      MVI A, 0x33
      DB     0x44, 0xFE, 0x9C
      HLT
;***********************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, 0X33         0x3E                
0x0001                                  0x33                
0x0002              DB                  0x44                
0x0003              DB                  0xFE                
0x0004              DB                  0x9C                
0x0005              HLT                 0x76  
```
#### EQU
```asm
; Example
;***********************************************************
foo equ 0x55
MVI A, 0x33
JMP foo
;***********************************************************
;
```
#### DS
### Expressions
