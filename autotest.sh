#!/bin/bash
for prog in {'dlcheck.py','dlgrammar.py'}
do
	echo "-----------------------------Testing "$prog' ----------------------------------------'
	
	echo "Should-succeed check"
	for i in `ls example/*.dl`;do echo $i;python ${prog} <$i | grep -n -P '(Syntax error)|(Fatal)';done

	echo ""
	echo "Failure Check"
	for i in `ls example/fail/*.dl`;do echo $i;python ${prog} <$i | grep -n -P '(Syntax error)|(Fatal)';done
done

#for prog in {'dlcheck2.py',''}
#do
prog='dlcheck2.py'
	echo "-----------------------------Testing "$prog' ----------------------------------------'
	
	echo "Should-succeed check"
	for i in `ls example/*.dl`;do echo $i;python ${prog} <$i | grep -n -P '(Syntax error)|(Fatal)';done

#done
