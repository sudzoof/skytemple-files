; For use with ARMIPS
; 2021/06/09
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Implements Move Growth
; ------------------------------------------------------------------------------

.definelabel MoveLvlIconStart, 0x67
.definelabel MoveSubLvlIconStart, 0x70

.org 0x020243FC
.area 0xC
	mov  r0,r4
	mov  r1,r8
	bl ProxyExtendAccuracy
.endarea

.org 0x020244B0
.area 0xC
	mov  r0,r4
	mov  r1,r8
	bl ProxyExtendPower
.endarea

; TODO
.org 0x02098DE4
.area 0xC4
move_str_1:
	.ascii "[CS:M]%s%s[CR]",0
move_set:
	.ascii "[M:S2]",0
move_unset:
	.ascii "[M:S1]",0
move_str_2:
	.ascii "[CS:%c]%s%s%s[CLUM_SET:111]%2d[CLUM_SET:123]/[CLUM_SET:128]%2d[CR]",0
move_str_3:
	.ascii "%s %2d/%2d",0
move_level:
	.ascii "[M:B%d][M:B%d]",0
add_move_level:
	.dcb 1
.endarea

.org 0x02013478
.area 0x2E0
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r14}
	sub  r13,r13,#0x30
	mov  r6,r1
	ldrb r1,[r6, #+0x0]
	mov  r7,r0
	mov  r5,r2
	tst r1,#0x20
	movne  r4,#0x57
	bne end_choice_1
	ldrh r0,[r6, #+0x2]
	tst r0,#0x1
	movne  r4,#0x57
	moveq  r4,#0x4D
end_choice_1:
	cmp r5,#0x0
	ldreq r5,=0x02098D68
	ldrb r0,[r5, #+0x8]
	cmp r0,#0x0
	movne  r4,#0x57
	bne end_choice_2
	ldrb r0,[r5, #+0x9]
	cmp r0,#0x0
	beq end_choice_2
	ldrh r0,[r6, #+0x4]
	bl 0x02014C64
	cmp r0,#0x0
	movne  r4,#0x57
end_choice_2:
	ldrh r0,[r6, #+0x4]
	add  r0,r0,#0xEE
	add  r0,r0,#0x1F00
	bl 0x020258C4
	str r0, [r13, #+0x4]
	ldr r3,=add_move_level
	ldrb r2,[r3]
	cmp r2,#0
	streqb r2,[r13,#+0x10]
	moveq r2, #1
	streqb r2,[r3]
	beq no_move_level
	mov r0,r6
	bl GetMoveLevelProxy
	mvn r2, #0
	cmp r0,r2
	moveq r2,#0
	streqb r2,[r13,#+0x10]
	beq no_move_level
	add r2,r0,MoveLvlIconStart
	add r3,r1,MoveSubLvlIconStart
	ldr r1,=move_level
	add  r0,r13,#0x10
	bl 0x02013758
no_move_level:
	ldr r0,[r5, #+0x0]
	cmp r0,#0x5
	addls  r15,r15,r0,lsl #0x2
	b end_switch
	b case_0
	b case_1
	b case_2
	b case_3
	b case_4
	b case_5
case_0:
	mov  r0,r7
	ldr r1,=move_str_1
	add  r2,r13,#0x10
	ldr  r3,[r13, #+0x4]
	bl 0x02013758
	b end_switch
case_1:
	ldrb r1,[r6, #+0x0]
	mov  r0,r6
	tst r1,#0x8
	ldrne r8,=move_set
	ldreq r8,=move_unset
	bl GetMovePPProxy
	add  r1,r13,#0x10
	str r1,[r13]
	ldrb r3,[r6, #+0x6]
	ldr r1,=move_str_2
	mov  r2,r4
	str r3,[r13, #+0x8]
	str r0,[r13, #+0xc]
	mov  r0,r7
	mov  r3,r8
	bl 0x02013758
	b end_switch
case_2:
	ldrb r1,[r6, #+0x0]
	mov  r0,r6
	tst r1,#0x8
	ldrne r8,=move_set
	ldreq r8,=move_unset
	bl GetMovePPProxy
	add  r1,r13,#0x10
	str r1,[r13]
	ldrb r3,[r6, #+0x6]
	ldr r1,=move_str_2
	mov  r2,r4
	str r3,[r13, #+0x8]
	str r0,[r13, #+0xc]
	mov  r0,r7
	mov  r3,r8
	bl 0x02013758
	b end_switch
case_3:
	ldrb r1,[r6, #+0x0]
	mov  r0,r6
	tst r1,#0x4
	ldrne r8,=move_set
	ldreq r8,=move_unset
	bl GetMovePPProxy
	add  r1,r13,#0x10
	str r1,[r13]
	ldrb r3,[r6, #+0x6]
	ldr r1,=move_str_2
	mov  r2,r4
	str r3,[r13, #+0x8]
	str r0,[r13, #+0xc]
	mov  r0,r7
	mov  r3,r8
	bl 0x02013758
	b end_switch
case_4:
	ldrb r1,[r6, #+0x0]
	mov  r0,r6
	tst r1,#0x4
	ldrne r8,=move_set
	ldreq r8,=move_unset
	bl GetMovePPProxy
	add  r1,r13,#0x10
	str r1,[r13]
	ldrb r3,[r6, #+0x6]
	ldr r1,=move_str_2
	mov  r2,r4
	str r3,[r13, #+0x8]
	str r0,[r13, #+0xc]
	mov  r0,r7
	mov  r3,r8
	bl 0x02013758
	b end_switch
case_5:
	mov  r4,r0
	mov  r0,r6
	bl GetMovePPProxy
	str r0,[r13, #+0x0]
	ldrb r3,[r6, #+0x6]
	ldr r1,=move_str_3
	mov  r0,r7
	ldr  r2,[r13, #+0x4]
	bl 0x02013758
end_switch:
	add  r13,r13,#0x30
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r15}
ClearMoveLevel:
	ldr r3,=add_move_level
	mov r0,#0
	strb r0,[r3]
	bx r14
	.pool
.endarea


.org CopyMoveTo
.area 0x38
	stmdb  r13!,{r3,r4,r5,r14}
	mov  r5,r0
	mov  r4,r1
	mov  r2,#0x4
	bl CopyNBitsTo
	mov  r0,r5
	add  r1,r4,#0x2
	mov  r2,#0xA
	bl CopyNBitsTo
	mov  r0,#0
	strb r0,[r4, #+0x4]
	ldmia  r13!,{r3,r4,r5,r15}
	.fill 0x8, 0xCC
.endarea

.org CopyMoveFrom
.area 0x38
	stmdb  r13!,{r3,r4,r5,r14}
	mov  r5,r0
	mov  r4,r1
	mov  r2,#0x4
	bl CopyNBitsFrom
	mov  r0,r5
	add  r1,r4,#0x2
	mov  r2,#0xA
	bl CopyNBitsFrom
	ldmia  r13!,{r3,r4,r5,r15}
	.fill 0x10, 0xCC
.endarea

.org HookInitData
.area 0x4
	bl InitData
.endarea

.org HookWriteTo
.area 0x4
	bl CopyMoveLevelTo
.endarea

.org HookReadFrom
.area 0x4
	bl CopyMoveLevelFrom
.endarea

.org HookClearData
.area 0x4
	bl ClearData
.endarea

.org CopyMoveLevelTo
.area 0x44
	stmdb  r13!,{r4,r5,r6,r14}
	mov r4,r0
	mov r5,#0
	ldr r6,=MoveLevelPtr
	ldr r6,[r6]
beg_cpy_to:
	mov r0,r4
	mov r1,r6
	mov r2,#15
	bl CopyNBitsTo
	add r6,r6,#2
	add r5,r5,#1
	cmp r5,#0x400
	blt beg_cpy_to
	mov r0,r4
	bl DebugFunc
	ldmia  r13!,{r4,r5,r6,r15}
	.pool
.endarea

.org CopyMoveLevelFrom
.area 0x44
	stmdb  r13!,{r4,r5,r6,r14}
	mov r4,r0
	mov r5,#0
	ldr r6,=MoveLevelPtr
	ldr r6,[r6]
beg_cpy_from:
	mov r0,r4
	mov r1,r6
	mov r2,#15
	bl CopyNBitsFrom
	add r6,r6,#2
	add r5,r5,#1
	cmp r5,#0x400
	blt beg_cpy_from
	mov r0,r4
	bl DebugFunc
	ldmia  r13!,{r4,r5,r6,r15}
	.pool
.endarea

.org InitData
.area 0x2C
	stmdb  r13!,{r14}
	mov  r0,#0x800
	mov  r1,#0x0
	bl MemAlloc
	ldr r1,=MoveLevelPtr
	str r0, [r1]
	mov  r1,#0x800
	bl FillWithZeros4BytesArray
	bl OrgEndInit
	ldmia  r13!,{r15}
	.pool
.endarea

.org ClearData
.area 0x20
	stmdb  r13!,{r14}
	bl 0x020550E0
	ldr r1,=MoveLevelPtr
	ldr r0, [r1]
	mov  r1,#0x800
	bl FillWithZeros4BytesArray
	ldmia  r13!,{r15}
	.pool
.endarea

.org GetMoveLevelProxy
.area 0x2C
	stmdb  r13!,{r4,r14}
	mov r4,r0
	mov r0,#2
	bl 0x02003ED0
	cmp r0,#0
	mvneq r0, #0
	moveq r1, #0
	ldmeqia  r13!,{r4,r15}
	mov r0,r4
	bl GetMoveLevel
	ldmia  r13!,{r4,r15}
.endarea

.org GetMovePPProxy
.area 0x2C
	stmdb  r13!,{r4,r14}
	mov r4,r0
	mov r0,#2
	bl 0x02003ED0
	cmp r0,#0
	mov r0,r4
	bne get_actual_pp_bonus
	bl GetMovePPWithBonus
	ldmia  r13!,{r4,r15}
get_actual_pp_bonus:
	bl GetPPWithLevelBonusNoCheck
	ldmia  r13!,{r4,r15}
.endarea

.org ProxyExtendAccuracy
.area 0x2C
	stmdb  r13!,{r4,r5,r14}
	mov r4,r0
	mov r5,r1
	mov r0,#2
	bl 0x02003ED0
	cmp r0,#0
	beq no_extend_accuracy
	mov r0,r4
	mov r1,r5
	bl ExtendAccuracy
no_extend_accuracy:
	ldmia  r13!,{r4,r5,r15}
.endarea

.org ProxyExtendPower
.area 0x2C
	stmdb  r13!,{r4,r5,r14}
	mov r4,r0
	mov r5,r1
	mov r0,#2
	bl 0x02003ED0
	cmp r0,#0
	beq no_extend_power
	mov r0,r4
	mov r1,r5
	bl ExtendPower
no_extend_power:
	ldmia  r13!,{r4,r5,r15}
.endarea

.org MoveLevelPtr
.area 0x4
	.word 0x0
.endarea

.org IsLoadedFile
.area 0x4
	.word 0x0
.endarea

.org MGrowFileStream
.area 0x48
	.fill 0x48, 0x0
.endarea
