__Z8my_qsortPiii:	                       ## @_Z8my_qsortPiii
	.cfi_startproc
Lfunc_begin0:
	.loc	1 11 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:11:0
	## BB#0:
	pushq	%rbp
Ltmp2:
	.cfi_def_cfa_offset 16
Ltmp3:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp4:
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	%edx, -16(%rbp)
	.loc	1 12 0 prologue_end     ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:12:0
Ltmp5:
	movslq	-12(%rbp), %rdi
	movq	-8(%rbp), %rax
	movl	(%rax,%rdi,4), %edx
	movl	%edx, -20(%rbp)
	.loc	1 13 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:13:0
	movl	-12(%rbp), %edx
	addl	$1, %edx
	movl	%edx, -24(%rbp)
	.loc	1 14 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:14:0
	movl	-16(%rbp), %edx
	movl	%edx, -28(%rbp)
LBB0_1:	                                 ## =>This Loop Header: Depth=1
	                                        ##     Child Loop BB0_3 Depth 2
	                                        ##     Child Loop BB0_6 Depth 2
	.loc	1 16 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:16:0
	movl	-24(%rbp), %eax
	cmpl	-28(%rbp), %eax
	jg	LBB0_11
	## BB#2:                                ##   in Loop: Header=BB0_1 Depth=1
	.loc	1 17 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:17:0
Ltmp6:
	jmp	LBB0_3
LBB0_3:	                                 ##   Parent Loop BB0_1 Depth=1
	                                        ## =>  This Inner Loop Header: Depth=2
	movslq	-24(%rbp), %rax
	movq	-8(%rbp), %rcx
	movl	(%rcx,%rax,4), %edx
	cmpl	-20(%rbp), %edx
	jg	LBB0_5
	## BB#4:                                ##   in Loop: Header=BB0_3 Depth=2
	.loc	1 18 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:18:0
	movl	-24(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -24(%rbp)
	jmp	LBB0_3
LBB0_5:	                                 ##   in Loop: Header=BB0_1 Depth=1
	.loc	1 19 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:19:0
	jmp	LBB0_6
LBB0_6:	                                 ##   Parent Loop BB0_1 Depth=1
	                                        ## =>  This Inner Loop Header: Depth=2
	movslq	-28(%rbp), %rax
	movq	-8(%rbp), %rcx
	movl	(%rcx,%rax,4), %edx
	cmpl	-20(%rbp), %edx
	jle	LBB0_8
	## BB#7:                                ##   in Loop: Header=BB0_6 Depth=2
	.loc	1 20 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:20:0
	movl	-28(%rbp), %eax
	addl	$4294967295, %eax       ## imm = 0xFFFFFFFF
	movl	%eax, -28(%rbp)
	jmp	LBB0_6
LBB0_8:	                                 ##   in Loop: Header=BB0_1 Depth=1
	.loc	1 21 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:21:0
	movl	-24(%rbp), %eax
	cmpl	-28(%rbp), %eax
	jg	LBB0_10
	## BB#9:                                ##   in Loop: Header=BB0_1 Depth=1
	.loc	1 22 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:22:0
Ltmp7:
	movslq	-24(%rbp), %rax
	movq	-8(%rbp), %rcx
	movl	(%rcx,%rax,4), %edx
	movl	%edx, -32(%rbp)
	.loc	1 23 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:23:0
	movslq	-28(%rbp), %rax
	movq	-8(%rbp), %rcx
	movl	(%rcx,%rax,4), %edx
	movslq	-24(%rbp), %rax
	movq	-8(%rbp), %rcx
	movl	%edx, (%rcx,%rax,4)
	.loc	1 24 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:24:0
	movl	-32(%rbp), %edx
	movslq	-28(%rbp), %rax
	movq	-8(%rbp), %rcx
	movl	%edx, (%rcx,%rax,4)
	.loc	1 25 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:25:0
	movl	-24(%rbp), %edx
	addl	$1, %edx
	movl	%edx, -24(%rbp)
	.loc	1 26 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:26:0
	movl	-28(%rbp), %edx
	addl	$4294967295, %edx       ## imm = 0xFFFFFFFF
	movl	%edx, -28(%rbp)
Ltmp8:
LBB0_10:	                                ##   in Loop: Header=BB0_1 Depth=1
	.loc	1 28 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:28:0
	jmp	LBB0_1
Ltmp9:
LBB0_11:
	.loc	1 29 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:29:0
	movslq	-28(%rbp), %rax
	movq	-8(%rbp), %rcx
	movl	(%rcx,%rax,4), %edx
	movslq	-12(%rbp), %rax
	movq	-8(%rbp), %rcx
	movl	%edx, (%rcx,%rax,4)
	.loc	1 30 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:30:0
	movl	-20(%rbp), %edx
	movslq	-28(%rbp), %rax
	movq	-8(%rbp), %rcx
	movl	%edx, (%rcx,%rax,4)
	.loc	1 31 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:31:0
	movl	-12(%rbp), %edx
	cmpl	-28(%rbp), %edx
	jge	LBB0_13
	## BB#12:
	.loc	1 32 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:32:0
	movq	-8(%rbp), %rdi
	movl	-12(%rbp), %esi
	movl	-28(%rbp), %edx
	callq	__Z8my_qsortPiii
LBB0_13:
	.loc	1 33 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:33:0
	movl	-24(%rbp), %eax
	cmpl	-16(%rbp), %eax
	jge	LBB0_15
	## BB#14:
	.loc	1 34 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:34:0
	movq	-8(%rbp), %rdi
	movl	-24(%rbp), %esi
	movl	-16(%rbp), %edx
	callq	__Z8my_qsortPiii
LBB0_15:
	.loc	1 35 0                  ## /Users/John/Documents/workshop/compiler/compiler-qsort/compiler-qsort/main.cpp:35:0
	addq	$32, %rsp
	popq	%rbp
	ret
Ltmp10:
Lfunc_end0:
	.cfi_endproc

	.globl	_main
	.align	4, 0x90