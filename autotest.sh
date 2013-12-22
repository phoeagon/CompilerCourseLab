#!/bin/bash
echo "Should-succeed check"
for i in `ls example/*.dl`;do echo $i;python dlcheck.py <$i | grep -n "Fatal";done
echo "Failure Check"
for i in `ls example/fail/*.dl`;do echo $i;python dlcheck.py <$i | grep -n "Fatal";done
