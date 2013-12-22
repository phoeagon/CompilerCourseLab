#!/bin/bash
echo "Should-succeed check"
for i in `ls example/*.dl`;do echo $i;python dlcheck.py <$i | grep -n -P '(Syntax error)|(Fatal)';done

echo ""
echo "Failure Check"
for i in `ls example/fail/*.dl`;do echo $i;python dlcheck.py <$i | grep -n -P '(Syntax error)|(Fatal)';done
