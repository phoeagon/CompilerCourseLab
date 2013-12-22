Dlang Features:

+ Uses `HLA` backend
+ Supports syscall via `$[hla_syscall]` interface. (Much like `syslike` in C)
+ Supports breakpoint by $[hla_brkpt]; to facilitate debugging.
+ Supports an "string" type.
+ Library support for randomization, string, input output.
+ Hexidecimal input/output.
+ Declarations must come before other statements
+ Supports `foreach` and `struct`
+ Stack based expression evaluation
+ Basic functions such as recursion, operator priorities, etc.
+ Basic try...catch.. support as:
    try { ... throw 1 ;} catch 1:{}
    Supporting const numerics as exceptions
