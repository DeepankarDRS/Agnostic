
## Types of Errors in C++

Error handling in C++ involves understanding the categories of errors that can occur during different phases of a program:

1. **Compile-time errors**

   * Detected by the compiler.
   * Examples: syntax errors, missing headers, type mismatches, undeclared identifiers.
   * Fix: Correct code before compilation.

2. **Link-time errors**

   * Detected by the linker after successful compilation.
   * Examples: unresolved symbols, multiple definitions, missing object files/libraries.
   * Fix: Ensure proper declarations, definitions, and linking against the right libraries.

3. **Runtime errors**

   * Detected during execution.
   * Examples: division by zero, invalid memory access, null pointer dereference, file-not-found, failed network connection.
   * Fix: Use exceptions, error codes, `std::expected`, or validation checks.

4. **Logical errors**

   * Program compiles and runs, but output is incorrect.
   * Examples: wrong algorithm, incorrect condition, off-by-one errors.
   * Fix: Careful design, testing, debugging, and code reviews.

---

## Quick Examples

```cpp
// Compile-time error: undeclared variable
int main() {
    x = 10; // error: 'x' was not declared
}

// Link-time error: missing definition
void foo();
int main() { foo(); } // error: undefined reference to `foo`

// Runtime error: division by zero
int main() {
    int x = 5 / 0; // undefined behavior
}

// Logical error: incorrect output
int factorial(int n) {
    return n * factorial(n-1); // missing base case → infinite recursion
}
```

---

## Best Practice Summary

* **Catch compile-time errors early** with modern compilers, static analyzers, and strict warning levels.
* **Link-time errors** indicate missing or misconfigured components — automate builds with CMake or similar tools.
* **Runtime errors** should be anticipated; use exceptions, error codes, or `expected`.
* **Logical errors** require testing, debugging tools, and formal verification when possible.

---

<!-- End of README -->
