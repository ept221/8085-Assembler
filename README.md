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

LXI H, 0x03B7
LXI H, 03B7    ; The "0x" is optional
LXI H, 3B7     ; Illegal. 16-bit constants must have four digits
```
If an 8-bit constant is given where a 16-bit constant is expected, the 8-bit constant will be converted to a 16-bit constant, with the upper 8-bits all zero.
```asm
JNZ 0x3FC7  ; Jump-not-zero to 0x3FC7
JMP FF      ; JMP takes a 16-bit argument, but given 8-bits. Will JMP to 0x00FF
```

### Label Definitions
Label definitions may be any string ending with a colon, where the string does not match the pattern of an 8 or 16-bit constant.

```asm
  ; Example
  ;*******************************************************************************
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
      MVI A, 33
      DB     0x44, 0xFE, 0x9C
      HLT
;***********************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, 33           0x3E                
0x0001                                  0x33                
0x0002              DB                  0x44                
0x0003              DB                  0xFE                
0x0004              DB                  0x9C                
0x0005              HLT                 0x76  
```
#### \<symbol> EQU <8 or 16-bit number>
Equates a symbol with a number.
```asm
; Example
;***********************************************************
      foo EQU 0xC5F3
      MVI A,  33
      LXI H,  foo
;***********************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, 33           0x3E                
0x0001                                  0x33                
0x0002              LXI H, FOO          0x21                
0x0003                                  0xF3                
0x0004                                  0xC5      
```
#### DS <8 or 16-bit number>
Defines and reserves the next n-bytes for storage.
```asm
; Example
;*******************************************************************************
            JMP END 
Storage:    DS  0x05
            LDA Storage
END:        OUT 42
;*******************************************************************************
; Assembles to the following:

Address             Label               Instruction         Hex Code            
--------------------------------------------------------------------------------
0x0000                                  JMP END             0xC3                
0x0001                                                      0x0B                
0x0002                                                      0x00                
0x0008              STORAGE:            LDA STORAGE         0x3A                
0x0009                                                      0x03                
0x000A                                                      0x00                
0x000B              END:                OUT 42              0xD3                
0x000C                                                      0x42              
```

## Expressions
Anytime an instruction or directive requires a numerical argument, an expression can be used. Supported operations inside expressions include addition and and subtraction, and the location counter $ is also made available. Expressions may contain symbols, but must resolve within two passes of the assembler, and if used for directive arguments, must resolve in a single pass. All expressions must evaluate to a positive number.
```asm
; Example with expression resolution in one pass.
;***********************************************************
      foo    EQU   10
      MVI A, foo - 04
;***********************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, FOO - 04     0x3E                
0x0001                                  0x0C     


;###########################################################
; Example with expression resolution in two passes.
;***********************************************************
      MVI A, foo + 04
      foo    EQU   30
;***********************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, FOO + 04     0x3E                
0x0001                                  0x34


;###########################################################
; Example with expression resolution in two passes, and $
;***********************************************************
      MVI A,  55
      JMP $ + foo
      foo equ 05
      DB  $,  $ + 01, $ + foo
      DS  02
      HLT
;***********************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, 55           0x3E                
0x0001                                  0x55                
0x0002              JMP $ + FOO         0xC3                
0x0003                                  0x07                
0x0004                                  0x00                
0x0005              DB                  0x05                
0x0006              DB                  0x07                
0x0007              DB                  0x0C                
0x000A              HLT                 0x76    
```
