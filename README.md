# 8085-Assembler

A simple Python based 8085 assembler.

## Quickstart
To clone this repository and assemble the demo file, open a terminal and run:
```bash
git clone https://github.com/ept221/8085-Assembler.git
cd 8085-Assembler/src/
python3 assembler.py demo.asm -s
```

## Usage
```
usage: assembler.py [-h] [-L] [-A] [-B] [-I] [-H] [-C] [-c] [-s] [-b] [-o OUT] source

A simple 8085 assembler.

positional arguments:
  source             source file

options:
  -h, --help         show this help message and exit
  -L, --lineNum      include the line number in output
  -A, --address      include the address in output
  -B, --label        include the labels in output
  -I, --instruction  include the instructions and arguments in output
  -H, --hex          include the hex code in output
  -C, --comment      include the comments in output
  -c, --compressed   don't include empty segments in output
  -s, --standard     equivalent to -A -B -I -H -C -c
  -b, --binary       output code as binary file (can only be combined with -o)
  -o OUT, --out OUT  output file name (if not specified: stdout, unless -b used, then: "out.bin")
  ```
## Source File Syntax
The assembler is case insensitive.

### Comments
Comments begin with semicolons.
```asm
MVI A, 0x5C ; This is a comment
```

### Constants
Constants are in decimal by default, but hexadecimal and binary are also supported. Constants can also be negative and are stored in two's complement form when assembled.
```asm
MVI A, 10     ; Decimal constant
MVI A, 0x0A   ; Hexadecimal constant
MVI A, 0b1010 ; Binary constant
MVI A, -10    ; Negative constant
```

### Label Definitions
Label definitions may be any string ending with a colon, where the string does not match the pattern of a constant.

```asm
  ; Example
  ;*******************************************************************************
        MVI A, 0x5C
  Foo:  DCR A         ; Label definition
        JNZ Foo       ; Jump-not-zero to Foo
  ;*******************************************************************************
        MVI A, 0x5C
  0xFD: DCR A         ; Illegal. Label definition cannot match hex constant format
        JNZ 0xFD
```
### Directives
#### ORG <16-bit-address>
Sets the origin to the given address. Only forward movement of the origin is permitted.
```asm
; Example
;*******************************************************************************
        MVI A, 0x55
        OUT 0x42
        JMP Start
 Start: ORG 0x44
        MVI A, 0x32
        OUT 0x42
;*******************************************************************************
; Assembles to the following:
; (shown in compressed mode, where empty segment isn't displayed) 

Address             Label               Instruction         Hex Code            
--------------------------------------------------------------------------------
0x0000                                  MVI A, 0X55         0x3E                
0x0001                                                      0x55                
0x0002                                  OUT 0X42            0xD3                
0x0003                                                      0x42                
0x0004                                  JMP START           0xC3                
0x0005                                                      0x44                
0x0006                                                      0x00                
0x0044              START:              MVI A, 0X32         0x3E                
0x0045                                                      0x32                
0x0046                                  OUT 0X42            0xD3                
0x0047                                                      0x42  
```
```asm
; Example
;*******************************************************************************
      ORG 0x44
      MVI A, 0xC7
      OUT 0x44
      ORG 0x00      ; Illegal. Cannot move origin backwards
      JMP 0x0044
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

#### DW <16-bit-data>, ...
Writes one or more data word sequentially into memory.
```asm
; Example
;***********************************************************
      MVI A, 33
      DW     0xDEAD, 0xBEEF
      HLT
;***********************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, 33           0x3E                
0x0001                                  0x21                
0x0002              DW                  0xAD                
0x0003              DW                  0xDE                
0x0004              DW                  0xEF                
0x0005              DW                  0xBE                
0x0006              HLT                 0x76  
```

#### \<symbol> EQU <16-bit number>
Equates a symbol with a number.
```asm
; Example
;***********************************************************
      foo EQU 0xC5F3
      MVI A,  0x33
      LXI H,  foo
;***********************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, 0X33         0x3E                
0x0001                                  0x33                
0x0002              LXI H, FOO          0x21                
0x0003                                  0xF3                
0x0004                                  0xC5      
```
#### DS <16-bit number>
Defines and reserves the next n-bytes for storage.
```asm
; Example
;*******************************************************************************
            JMP END 
Storage:    DS  0x05
            LDA Storage
END:        OUT 0x42
;*******************************************************************************
; Assembles to the following:
; (shown in compressed mode, where empty segment isn't displayed) 

Address             Label               Instruction         Hex Code            
--------------------------------------------------------------------------------
0x0000                                  JMP END             0xC3                
0x0001                                                      0x0B                
0x0002                                                      0x00                
0x0008              STORAGE:            LDA STORAGE         0x3A                
0x0009                                                      0x03                
0x000A                                                      0x00                
0x000B              END:                OUT 0X42            0xD3                
0x000C                                                      0x42              
```
#### STRING \<string>
Writes an ASCII string into memory. Double quotes and backslashes must be escaped with a backslash. The string is not null terminated by default, but can be terminated by adding \0 to the string.
```asm
; Example
;*******************************************************************************
STRING "The robot says \"Hi!\"\0"
;*******************************************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              STRING              0x54                
0x0001              STRING              0x68                
0x0002              STRING              0x65                
0x0003              STRING              0x20                
0x0004              STRING              0x72                
0x0005              STRING              0x6F                
0x0006              STRING              0x62                
0x0007              STRING              0x6F                
0x0008              STRING              0x74                
0x0009              STRING              0x20                
0x000A              STRING              0x73                
0x000B              STRING              0x61                
0x000C              STRING              0x79                
0x000D              STRING              0x73                
0x000E              STRING              0x20                
0x000F              STRING              0x22                
0x0010              STRING              0x48                
0x0011              STRING              0x69                
0x0012              STRING              0x21                
0x0013              STRING              0x22                
0x0014              STRING              0x00 
```


## Expressions
Anytime an instruction or directive requires a numerical argument, an expression can be used. Supported operations inside expressions include addition and subtraction. The location counter $ is also made available. Expressions may contain symbols, but must resolve within two passes of the assembler, and if used for directive arguments, must resolve in a single pass. All expressions must evaluate to a positive number.
```asm
; Example with expression resolution in one pass.
;***********************************************************
      foo    EQU   0x10
      MVI A, foo - 0x04
;***********************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, FOO - 0X04   0x3E                
0x0001                                  0x0C     

```
```asm
; Example with expression resolution in two passes.
;***********************************************************
      MVI A, foo + 0x04
      foo    EQU   0x30
;***********************************************************
; Assembles to the following:

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, FOO + 0X04   0x3E                
0x0001                                  0x34
```
```asm
; Example with expression resolution in two passes, and $
;***********************************************************
      MVI A,  0x55
      JMP $ + foo
      foo equ 0x05
      DB  $,  $ + 0x01, $ + foo
      DS  02
      HLT
;***********************************************************
; Assembles to the following:
; (shown in compressed mode, where empty segment isn't displayed) 

Address             Instruction         Hex Code            
------------------------------------------------------------
0x0000              MVI A, 0X55         0x3E                
0x0001                                  0x55                
0x0002              JMP $ + FOO         0xC3                
0x0003                                  0x07                
0x0004                                  0x00                
0x0005              DB                  0x05                
0x0006              DB                  0x07                
0x0007              DB                  0x0C                
0x000A              HLT                 0x76    
```
