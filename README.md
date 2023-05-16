# LeCompiler
 
A working C-subset compiler written in python which compiles to assembly of FRISC architecture

Consists of:
Lexical Analyzer -> similar to program "Lex"
Syntactic Analyzer -> similar to program "Yacc"
Semantic Analyzer
Code Generator + Optimizer

NOTE: All stages are independent (except semantic and code generation, which are fed the same input). Output of one stage is input for the next.