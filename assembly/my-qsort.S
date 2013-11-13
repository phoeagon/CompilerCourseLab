.data	
strtag1:
	.ascii	"%d "
strtag2:
	.ascii	"\n"
	
.text
.globl _my_qsort
_my_qsort:
	pushl	%ebp
	movl	%esp, %ebp
	movl	(%edi, %esi, 4), %eax
#;;;i = begin
	movl	%esi, %ebx
#;;; j = end
	movl	%edx, %ecx
start_loop:	
#;;; while (i <= j)
	cmpl	%ebx, %ecx
	jl	end_loop

#;;; while (a[i] <= pivot)
loop1:
	cmpl	(%edi, %ebx, 4), %eax
	jle	end1
	incl	%ebx
	jmp	start_loop
end1:
#;;; while (a[j] > pivot)
loop2:
	cmpl	(%edi, %ecx, 4), %eax
	jge	end2
	decl	%ecx	
	jmp	start_loop
end2:
	cmpl	%ebx, %ecx
	jl	no_swap
	pushl	%eax
	pushl	%esi
	movl	(%edi, %ebx, 4), %eax
	movl	(%edi, %ecx, 4), %esi
	movl	%esi, (%edi, %ebx, 4)
	movl	%eax, (%edi, %ecx, 4)
	popl	%esi
	popl	%eax

	incl	%ebx
	decl	%ecx

no_swap:
	jmp	start_loop
	
end_loop:

#;;; if (begin < j)
	cmpl	%esi, %ecx
	jle	skip1
	pushl	%edx
	pushl	%ebx
	pushl	%ecx
	movl	%ecx, %edx
	call	_my_qsort
	popl	%ecx
	popl	%ebx
	popl	%edx
skip1:
#;;; if (i < end)
	cmpl	%ebx, %edx
	jle	skip2
	pushl	%ebx
	pushl	%ecx
	pushl	%esi
	movl	%ebx, %esi
	call	_my_qsort
	popl	%esi
	popl	%ecx
	popl	%ebx
skip2:
	leave
	ret

.globl	main
main:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$0x40, %esp
	leal	0x4(%esp), %ebx
	movl	$strtag1, %edi
	movl	$0, %eax
read_loop:	
	cmpl	$10, %eax
	jge	for_loop_over1
	leal	(%ebx, %eax, 4), %esi
	pushl	%eax
	pushl	%esi
	pushl	%edi
	call	__isoc99_scanf
	popl	%edi
	popl	%esi
	popl	%eax
	addl	$1, %eax
	jmp	read_loop
for_loop_over1:
	movl	%ebx, %edi
	pushl	%ebx
	movl	$0, %esi
	movl	$9, %edx
	call	_my_qsort
	popl	%ebx

	movl	$0, %eax
	movl	$strtag1, %edi
write_loop:	
	cmpl	$10, %eax
	jge	for_loop_over2
	movl	(%ebx, %eax, 4), %esi
	pushl	%eax
	pushl	%esi
	pushl	%edi
	call	printf
	popl	%edi
	popl	%esi
	popl	%eax
	addl	$1, %eax
	jmp	write_loop
for_loop_over2:	
	
	movl	$0, %eax
	leave
	ret