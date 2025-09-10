# 🐞 Debugging Guide (Basic ➝ Advanced)

Debugging is the process of identifying, analyzing, and fixing issues in code. This guide provides a **step-by-step approach** you can follow, starting from simple checks to advanced techniques.

---

## 🔹 1. Basic Debugging
- **Read the Error Message**  
  - Understand the exception, file, and line number.
  - Search documentation or the exact error message online if unclear.
- **Check Recent Changes**  
  - What did you modify before the bug appeared?
- **Print / Log Statements**  
  - Add `print()` or logging to inspect variable values and flow.
- **Simplify the Problem**  
  - Comment out or isolate parts of code to narrow down the cause.

---

## 🔹 2. Intermediate Debugging
- **Use a Debugger**  
  - Step through code line by line (`pdb`, `gdb`, IDE debuggers).
  - Inspect variable states at breakpoints.
- **Check Data Flow**  
  - Validate inputs, outputs, and assumptions.
  - Verify that functions return expected values.
- **Unit Testing**  
  - Write small tests to confirm isolated functionality.
- **Rubber Ducking**  
  - Explain the problem to someone (or even a rubber duck).  
  - Often, clarity emerges just by verbalizing the issue.

---

## 🔹 3. Advanced Debugging
- **Logging & Monitoring**  
  - Use structured logs with levels (`DEBUG`, `INFO`, `WARN`, `ERROR`).
  - Persist logs for post-crash analysis.
- **Version Control Bisecting**  
  - Use `git bisect` to identify which commit introduced the bug.
- **Static & Dynamic Analysis**  
  - Linters (`flake8`, `eslint`, `cppcheck`) catch common errors.
  - Profilers and sanitizers detect memory leaks, race conditions, performance bottlenecks.
- **Reproduce & Isolate**  
  - Ensure the bug is reproducible.
  - Minimize the failing code to the smallest test case.
- **Advanced Tools**  
  - Valgrind (C/C++ memory issues).  
  - Wireshark (network debugging).  
  - Tracing tools (`strace`, `ltrace`, `perf`) for system-level issues.

---

## 🔹 4. Mindset & Best Practices
- Stay calm and systematic — avoid random guessing.
- Fix **root causes**, not symptoms.
- Document findings and solutions for future reference.
- Always write tests after fixing a bug to prevent regressions.

---

📌 **Remember:** Debugging is not just about fixing; it’s about *understanding your system better each time*.  
# 🐞 Debugging Guide (C++ & Python)

This guide explains how to debug **C++** and **Python** programs in depth, covering basic to advanced techniques.  

---

## 🔹 Debugging in C++

### 1. Basic Debugging
- **Read Compiler Errors/Warnings**
  - Pay attention to line numbers and error descriptions.
  - Use `-Wall -Wextra` flags with `g++`/`clang++` to catch warnings.
- **Print Debugging**
  - Use `std::cout << var << std::endl;` to track values.
  - Add checkpoints to trace program flow.
- **Check Common Issues**
  - Uninitialized variables
  - Array/vector out-of-bounds access
  - Pointer misuse / dangling pointers
  - Memory leaks

### 2. Intermediate Debugging
- **Use a Debugger**
  - `gdb ./a.out` (GNU Debugger)
  - Common commands:
    - `break main` → set breakpoint  
    - `run` → start program  
    - `next` / `step` → move line by line  
    - `print var` → inspect variable  
    - `backtrace` → see call stack  
- **Valgrind for Memory Errors**
  - `valgrind --leak-check=full ./a.out`
  - Detects memory leaks, invalid reads/writes, double frees.
- **Static Analysis**
  - Use `cppcheck`, `clang-tidy` to catch undefined behavior early.

### 3. Advanced Debugging
- **Sanitizers**
  - Compile with `-fsanitize=address,undefined` (Clang/GCC).
  - Detects buffer overflows, undefined behavior, leaks.
- **Profiling**
  - Use `gprof` or `perf` to identify bottlenecks.
- **Core Dumps**
  - Enable: `ulimit -c unlimited`
  - Run program, when it crashes → `gdb ./a.out core`
- **Concurrency Issues**
  - Thread sanitizers (`-fsanitize=thread`) detect data races.
- **System-Level Debugging**
  - Use `strace ./a.out` to trace syscalls.
  - Use `ltrace ./a.out` to trace library calls.

---

## 🔹 Debugging in Python

### 1. Basic Debugging
- **Read Tracebacks Carefully**
  - Note file, line number, and exception type.
- **Print Debugging**
  - Use `print(var)` or f-strings to show variable states.
  - Add checkpoints in loops/functions.
- **Common Issues**
  - Indentation errors
  - Type errors (e.g., mixing `int` and `str`)
  - Import errors
  - Off-by-one errors in loops

### 2. Intermediate Debugging
- **Use Built-in Debugger (`pdb`)**
  - Run: `python -m pdb script.py`
  - Commands:
    - `break 10` → set breakpoint at line 10
    - `step` / `next` → move through code
    - `print(var)` → inspect variables
    - `continue` → resume execution
- **Logging Instead of Prints**
  - Use `import logging`
  - Configure levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Unit Testing**
  - Use `unittest` or `pytest` to isolate failing functionality.

### 3. Advanced Debugging
- **Traceback Analysis**
  - Use `traceback` module to print custom stack traces.
- **Profiling**
  - Use `cProfile` or `line_profiler` to find performance bottlenecks.
- **Memory Debugging**
  - Use `objgraph` to detect memory leaks.
  - `tracemalloc` for memory allocation tracking.
- **Concurrency Issues**
  - Debug multithreading deadlocks with `faulthandler`.
  - Use async debugging tools (`asyncio` debug mode).
- **Advanced Tools**
  - `pdbpp` → enhanced `pdb` with syntax highlighting.
  - `ipdb` → interactive debugging inside IPython/Jupyter.
  - Remote debugging with `debugpy` in VSCode.

---

## 🔹 Best Practices for Both
- Reproduce the bug reliably before fixing.
- Simplify the code to a minimal test case.
- Fix the **root cause**, not just the symptom.
- Add tests after fixing to avoid regressions.
- Document tricky bugs and solutions for future reference.

---

📌 **Rule of Thumb:**  
Start simple (prints/logs) ➝ step through with debugger ➝ analyze with specialized tools ➝ profile/trace system behavior.
