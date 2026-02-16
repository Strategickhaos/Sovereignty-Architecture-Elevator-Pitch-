#!/usr/bin/env python3
"""
FlameLang M1 Automated Test Suite
Strategickhaos DAO LLC | EIN 39-2900295
Inventor: Domenic Gabriel Garza (Me10101)

Verifies every M1 feature against expected output.
"""

import sys
sys.path.insert(0, '.')
from flamec import Lexer, Parser, Interpreter, run

PASS = 0
FAIL = 0

def test(name: str, source: str, expected: list[str]):
    global PASS, FAIL
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interp = Interpreter()
    
    # Capture output
    import io, contextlib
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        interp.interpret(program)
    
    actual = [line for line in f.getvalue().split('\n') if line]
    
    if actual == expected:
        print(f"  ✅ {name}")
        PASS += 1
    else:
        print(f"  ❌ {name}")
        print(f"     Expected: {expected}")
        print(f"     Got:      {actual}")
        FAIL += 1

# ═══════════════════════════════════════════════════════════════
print("═══ LITERALS ═══")
test("Integer", 'print(42);', ["42"])
test("Float", 'print(3.14);', ["3.14"])
test("String", 'print("hello");', ["hello"])
test("Boolean true", 'print(true);', ["true"])
test("Boolean false", 'print(false);', ["false"])

print("\n═══ ARITHMETIC ═══")
test("Addition", 'print(2 + 3);', ["5"])
test("Subtraction", 'print(10 - 4);', ["6"])
test("Multiplication", 'print(6 * 7);', ["42"])
test("Division", 'print(20 / 4);', ["5"])
test("Modulo", 'print(17 % 5);', ["2"])
test("Precedence", 'print(2 + 3 * 4);', ["14"])
test("Parentheses", 'print((2 + 3) * 4);', ["20"])
test("Unary minus", 'print(-5);', ["-5"])
test("Nested arith", 'print((10 - 2) * (3 + 1));', ["32"])

print("\n═══ COMPARISON ═══")
test("Less than", 'print(3 < 5);', ["true"])
test("Greater than", 'print(5 > 3);', ["true"])
test("Equal", 'print(5 == 5);', ["true"])
test("Not equal", 'print(5 != 3);', ["true"])
test("LTE", 'print(5 <= 5);', ["true"])
test("GTE", 'print(5 >= 6);', ["false"])

print("\n═══ LOGICAL ═══")
test("And true", 'print(true and true);', ["true"])
test("And false", 'print(true and false);', ["false"])
test("Or true", 'print(false or true);', ["true"])
test("Or false", 'print(false or false);', ["false"])
test("Not", 'print(not false);', ["true"])

print("\n═══ VARIABLES ═══")
test("Let + print", 'let x = 42; print(x);', ["42"])
test("Let + expr", 'let x = 2 + 3; print(x);', ["5"])
test("Let + ref", 'let a = 10; let b = a * 2; print(b);', ["20"])
test("Reassign", 'let x = 1; x = 2; print(x);', ["2"])

print("\n═══ STRINGS ═══")
test("String concat", 'print("Hello, " + "World!");', ["Hello, World!"])
test("String + var", 'let n = "SAGCO"; print("System: " + n);', ["System: SAGCO"])

print("\n═══ IF/ELSE ═══")
test("If true", 'if (true) { print("yes"); }', ["yes"])
test("If false", 'if (false) { print("yes"); } else { print("no"); }', ["no"])
test("If cond", 'let h = 85; if (h > 70) { print("NOMINAL"); } else { print("DEGRADED"); }', ["NOMINAL"])
test("If else-if", '''
let x = 2;
if (x == 1) { print("one"); }
else if (x == 2) { print("two"); }
else { print("other"); }
''', ["two"])

print("\n═══ WHILE ═══")
test("While loop", 'let i = 0; while (i < 5) { i = i + 1; } print(i);', ["5"])
test("While accum", '''
let sum = 0;
let i = 1;
while (i <= 10) {
    sum = sum + i;
    i = i + 1;
}
print(sum);
''', ["55"])

print("\n═══ FUNCTIONS ═══")
test("Simple fn", 'fn add(a, b) { return a + b; } print(add(3, 4));', ["7"])
test("Factorial", '''
fn factorial(n) {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}
print(factorial(6));
''', ["720"])
test("Fibonacci", '''
fn fib(n) {
    if (n <= 1) { return n; }
    return fib(n - 1) + fib(n - 2);
}
print(fib(10));
''', ["55"])
test("Closures", '''
fn make_adder(x) {
    fn adder(y) { return x + y; }
    return adder;
}
let add5 = make_adder(5);
print(add5(3));
''', ["8"])
test("String fn", '''
fn greet(who) { return "Hello, " + who + "!"; }
print(greet("Dom"));
''', ["Hello, Dom!"])

print("\n═══ BUILTINS ═══")
test("len()", 'print(len("hello"));', ["5"])
test("abs()", 'print(abs(-42));', ["42"])
test("min()", 'print(min(3, 1, 4));', ["1"])
test("max()", 'print(max(3, 1, 4));', ["4"])

print("\n═══ COMMENTS ═══")
test("Line comment", '// this is ignored\nprint(1);', ["1"])
test("Block comment", '/* multi\nline */ print(2);', ["2"])

print("\n═══ KHAOS METRIC ═══")
test("khaos_health", '''
fn khaos_health(h, d, r, f) {
    let score = (h * 40) + (r * 30) + (f * 20) - (d * 10);
    return score;
}
print(khaos_health(1, 0, 1, 1));
''', ["90"])

# ═══════════════════════════════════════════════════════════════
print(f"\n{'═' * 50}")
print(f"  RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
if FAIL == 0:
    print(f"  🔥 ALL TESTS PASS — M1 VERIFIED")
else:
    print(f"  ⚠️  {FAIL} FAILURES")
print(f"{'═' * 50}")

sys.exit(1 if FAIL else 0)
