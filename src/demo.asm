;*********************************************************************************          
; Robot Pet Obstacle Avoidance Program                                           *
;                                                                                *
; Ezra Thomas                                                                    *
;*********************************************************************************

            MVI A, 0x00       ; Setup timer B
            OUT 0x44

            MVI A, 0x42       ; Setup timer B
            OUT 0x45

            MVI A, 0xCE       ; Start timer B and set up port BB and BC to OUTPUT
            OUT 0x40

            MVI A, 0x02       ; Enable front sonar
            OUT 0x43

            LXI SP, 0x40FF    ; Set stack pointer

            JMP PRE

            ORG 0x44
PRE:        MVI A, 0x0C       ; Set Servo Port to OUTPUT
            OUT 0x00

            MVI A, 0x20       ; Center Shaft
            OUT 0x03

CENTER:     IN 0x41           ; Wait until shaft is centered
            ANI 0x08
            JZ CENTER

START:      MVI A, 0x21       ; Move shaft forward and drive
            OUT 0x03

            MVI A, 0x02       ; Enable front sonar
            OUT 0x43

PING_POLL:  CALL SUB_PING   ; Poll for obstical
            CPI 0x4F
            JNC PING_POLL

            MVI A, 0x20       ; Stop
            OUT 0x03

            MVI A, 0x01       ; Enable left sonar
            OUT 0x43
            CALL SUB_PING   ; Read left distance
            MOV L,A         ; Store left distance in L

            MVI A, 0x03       ; Enable right sonar
            OUT 0x43
            CALL SUB_PING   ; Read right distance

            CMP L           ; Compare right distance to left distance
            JC LEFT         ; Turn left if there is more room to the left
            JZ FLIP         ; Turn left or right if distances are equal

            MVI A, 0x3C           ; Turn shaft right
            OUT 0x03
            JMP TURN

LEFT:       MVI A, 0x00           ; Turn shaft left
            OUT 0x03
            JMP TURN

FLIP:       LDA TurnDir
            XRI 0x3C
            STA TurnDir
            OUT 0x03

TURN:       IN 0x41               ; Wait for shaft to finish turning
            ANI 0x08
            JZ TURN

            IN 0x03               ; Turn on drive motor to turn
            INR A
            OUT 0x03

            CALL SUB_TURN_DELAY ; Wait for turn to finish 
            JMP START           ; Loop back to START

SUB_PING:   ; Ping subroutine
            CALL SUB_DELAY  ; Rest delay
            LXI B, 0x800A     ; Setup timeout timer
            CALL SUB_TMR

POLL:       IN 0x41           ; Poll for echo or timout
            ANI 0x05
            CPI 0x05
            JZ POLL

            CPI 0x01          ; If timout reached jump to set max distance
            JZ CLEAR

            IN 0x44           ; If echo, calculate distance
            MOV B,A
            MVI A, 0xFF
            SUB B
            JMP WRITE

CLEAR:      MVI A, 0xFF       ; Set distance to max if no object detected

WRITE:      OUT 0x42          ; Write distance to LED readout
            RET             ; Return, note that distance is in A

SUB_TMR:    MOV A,B         ; Timer subroutine
            OUT 0x05
            MOV A,C
            OUT 0x04
            MVI A, 0xcc
            OUT 0x00
            RET             ; Return

SUB_DELAY:  LXI B,0x0C37      ; Delay subroutine for PING refresh (50ms)
DELAYLoop:  DCX B
            MOV A,B
            ORA C
            JNZ DELAYLoop
            RET             ; Return

SUB_TURN_DELAY: 
            MVI B, 0x08       ; Delay subroutine for turning (2s)
LOOP1:      MVI C, 0xD6
LOOP2:      MVI D, 0x7C
LOOP3:      DCR D
            JNZ LOOP3
            DCR C
            JNZ LOOP2
            DCR B
            JNZ LOOP1
            RET             ; Return

            ORG 0xF4          
TurnDir:    DB 0x3C