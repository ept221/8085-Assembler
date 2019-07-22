;*********************************************************************************          
; Robot Pet Obstacle Avoidance Program                                           *
;                                                                                *
; Ezra Thomas                                                                    *
;*********************************************************************************

            MVI A, 00       ; Setup timer B
            OUT 44

            MVI A, 42       ; Setup timer B
            OUT 45

            MVI A, CE       ; Start timer B and set up port BB and BC to OUTPUT
            OUT 40

            MVI A, 02       ; Enable front sonar
            OUT 43

            LXI SP, 40FF    ; Set stack pointer

            JMP PRE

            ORG 44
PRE:        MVI A, 0C       ; Set Servo Port to OUTPUT
            OUT 00

            MVI A, 20       ; Center Shaft
            OUT 03

CENTER:     IN 41           ; Wait until shaft is centered
            ANI 08
            JZ CENTER

START:      MVI A, 21       ; Move shaft forward and drive
            OUT 03

            MVI A, 02       ; Enable front sonar
            OUT 43

PING_POLL:  CALL SUB_PING   ; Poll for obstical
            CPI 4F
            JNC PING_POLL

            MVI A, 20       ; Stop
            OUT 03

            MVI A, 01       ; Enable left sonar
            OUT 43
            CALL SUB_PING   ; Read left distance
            MOV L,A         ; Store left distance in L

            MVI A, 03       ; Enable right sonar
            OUT 43
            CALL SUB_PING   ; Read right distance

            CMP L           ; Compare right distance to left distance
            JC LEFT         ; Turn left if there is more room to the left
            JZ FLIP         ; Turn left or right if distances are equal

            MVI A, 3C           ; Turn shaft right
            OUT 03
            JMP TURN

LEFT:       MVI A, 00           ; Turn shaft left
            OUT 03
            JMP TURN

FLIP:       LDA TurnDir
            XRI 3C
            STA TurnDir
            OUT 03

TURN:       IN 41               ; Wait for shaft to finish turning
            ANI 08
            JZ TURN

            IN 03               ; Turn on drive motor to turn
            INR A
            OUT 03

            CALL SUB_TURN_DELAY ; Wait for turn to finish 
            JMP START           ; Loop back to START

SUB_PING:   ; Ping subroutine
            CALL SUB_DELAY  ; Rest delay
            LXI B, 800A     ; Setup timeout timer
            CALL SUB_TMR

POLL:       IN 41           ; Poll for echo or timout
            ANI 05
            CPI 05
            JZ POLL

            CPI 01          ; If timout reached jump to set max distance
            JZ CLEAR

            IN 44           ; If echo, calculate distance
            MOV B,A
            MVI A, FF
            SUB B
            JMP WRITE

CLEAR:      MVI A, FF       ; Set distance to max if no object detected

WRITE:      OUT 42          ; Write distance to LED readout
            RET             ; Return, note that distance is in A

SUB_TMR:    MOV A,B         ; Timer subroutine
            OUT 05
            MOV A,C
            OUT 04
            MVI A, CC
            OUT 00
            RET             ; Return

SUB_DELAY:  LXI B,0C37      ; Delay subroutine for PING refresh (50ms)
DELAYLoop:  DCX B
            MOV A,B
            ORA C
            JNZ DELAYLoop
            RET             ; Return

SUB_TURN_DELAY: 
            MVI B, 08       ; Delay subroutine for turning (2s)
LOOP1:      MVI C, D6
LOOP2:      MVI D, 7C
LOOP3:      DCR D
            JNZ LOOP3
            DCR C
            JNZ LOOP2
            DCR B
            JNZ LOOP1
            RET             ; Return

            ORG F4          
TurnDir:    DB 3C
