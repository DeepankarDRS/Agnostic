
## Overview

This document summarizes idiomatic and robust error-handling techniques in modern C++ (C++11 → C++23+). It covers philosophy, language features, design patterns, practical examples, and debugging/testing strategies. The goal: write code that is safe, maintainable, performant, and easy to reason about.

## Table of contents

* Principles & philosophy
* Fundamental mechanisms
* Exception safety levels
* `noexcept` and move semantics
* `std::error_code` / `std::error_condition` and `std::error_category`
* `std::optional`, `std::variant`, `std::expected` (or roll-your-own)
* When to use exceptions vs error-values
* Interfacing with C / system APIs
* Concurrency, threads, and exceptions
* Debugging, sanitizers & testing
* Practical examples & patterns
* Quick checklist / best practices

---

# Principles & philosophy

* **Fail-fast when correctness is violated.** Use assertions in debug builds for internal invariants. Use exceptions or error-results for recoverable runtime errors.
* **Prefer RAII** for resource management — avoid manual acquire/release in error paths.
* **Make API decisions explicit:** library boundaries should document whether functions throw, return error codes, or use `expected`-like types.
* **Favor simple, composable error types.** Prefer small error enums or categories rather than huge ad‑hoc `std::string` messages for programmatic handling.

---

# Fundamental mechanisms

### Exceptions

* `throw` expression, `try { ... } catch(const std::exception& e) { ... }`.
* Prefer `throw` objects deriving from `std::exception` so `what()` is available.
* Do not use exceptions for control flow in hot paths.

Example:

```cpp
struct file_error : std::runtime_error {
  explicit file_error(std::string msg): std::runtime_error(std::move(msg)){}
};

std::string read_all(const std::filesystem::path& p) {
  if (!std::filesystem::exists(p))
    throw file_error("missing file: " + p.string());
  // ... read and return
}

try {
  auto s = read_all("foo.txt");
} catch (const std::exception& e) {
  std::cerr << "I/O failed: " << e.what() << '\n';
}
```

### Error-values / Out-parameters

* Return `std::optional<T>` when absence is expected. Use `std::variant` or `std::expected<T, E>` when you need rich error information.

---

# Exception safety levels

* **No-throw (nothrow):** operation guarantees it will not throw; often required by destructors and swap.
* **Basic guarantee:** invariants hold, no resource leaks; object may be in valid but unspecified state.
* **Strong guarantee:** operation is transactional — either completes or has no effect.

Design for the weakest useful guarantee and document it.

Example (strong guarantee using copy-and-swap):

```cpp
void container::insert_safe(const value_type& v) {
  Container tmp = *this; // copy may throw
  tmp.insert_noexcept(v); // assume this version provides basic/no-throw
  swap(tmp, *this); // noexcept swap
}
```

---

# `noexcept` and move semantics

* Mark move constructors/assignments `noexcept` when they truly cannot throw. This enables better optimizations (e.g., in `std::vector` reallocation will prefer moves over copies only if move is `noexcept`).
* Prefer conditional `noexcept(...)` expressions that reflect inner operations:

```cpp
MyType(MyType&&) noexcept(std::is_nothrow_move_constructible_v<Member>) = default;
```

* `noexcept` on destructors: default destructors are `noexcept(true)`; only mark them `noexcept(false)` if you intentionally want exceptions to propagate (rare).

---

# `std::error_code`, `std::error_condition`, and `std::error_category`

* Use these for library-level, portable error reporting that interoperates with system errors (`errno`) and `std::system_error`.
* `std::error_code` is lightweight and copyable; `std::system_error` wraps an `error_code` and can be thrown.

Example pattern:

```cpp
enum class MyErr { Ok=0, NotFound=1, BadFormat=2 };

class MyErrCategory : public std::error_category {
public:
  const char* name() const noexcept override { return "myerr"; }
  std::string message(int ev) const override {
    switch(static_cast<MyErr>(ev)){
      case MyErr::NotFound: return "not found";
      case MyErr::BadFormat: return "bad format";
      default: return "unknown";
    }
  }
};

inline const std::error_category& myerr_category() {
  static MyErrCategory c; return c;
}

inline std::error_code make_error_code(MyErr e) {
  return {static_cast<int>(e), myerr_category()};
}
```

(Also consider ADL customization to allow `std::error_code ec = MyErr::NotFound;`)

---

# `std::optional`, `std::variant`, `std::expected` and Result types

* `std::optional<T>` — use when absence is the only failure mode.
* `std::variant<T, E>` — when you want a union of result or error, but less ergonomic than `expected`.
* `std::expected<T, E>` (C++23) — best-fit for non-exception control-flow: explicit, composable, and expressive. If your toolchain lacks it, implement a tiny `expected` or use `outcome`/`tl::expected`.

Example (pseudo `expected` usage):

```cpp
std::expected<int, MyErr> parse_int(std::string_view s) {
  if (s.empty()) return std::unexpected(MyErr::BadFormat);
  // parse -> success or unexpected
}

if (auto r = parse_int("42"); r)
  use(*r);
else
  handle_error(r.error());
```

---

# When to use exceptions vs error-values

* **Exceptions**: API-level errors that are exceptional, recovery is difficult or impossible locally, and caller-level stack unwinding simplifies cleanup. Good for application code and internal libraries.
* **Error-values / `expected`**: Public API boundaries, performance-critical code, or when exceptions are disallowed by policy (embedded systems, kernels). Also good for modeling recoverable domain errors.
* **Rule of thumb:** exceptions for truly exceptional conditions; `expected` for routine validation/failure that the caller should branch on.

---

# Interfacing with C and system APIs

* C APIs typically return `errno` or negative integral error codes. Wrap them immediately into `std::error_code`/`std::system_error` or an `expected<T,E>`.
* Do not `throw` across C callbacks or C library boundaries unless the boundary explicitly supports it.

Example wrapper:

```cpp
std::expected<std::string, std::error_code> read_file_capi(const char* path) {
  FILE* f = fopen(path, "rb");
  if(!f) return std::unexpected(std::error_code(errno, std::generic_category()));
  // read, close, return
}
```

---

# Concurrency, threads, and exceptions

* Exceptions thrown on a thread that is not joined/caught will call `std::terminate()` if uncaught.
* Use `std::promise`/`std::future` or explicit `std::exception_ptr` to propagate exceptions between threads.

Pattern:

```cpp
std::packaged_task<void()> task([&](){
  try { do_work(); }
  catch(...) { /* capture via promise or rethrow into the future */ throw; }
});
```

Or capture exception and send via `promise.set_exception(std::current_exception());`.

---

# Debugging, sanitizers & testing

* Use `assert()` / `gsl::Expects` for precondition checks in debug builds.
* Use runtime checks and clear error types for user-facing errors.
* Tools: AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan), LeakSanitizer, Valgrind (where appropriate), and platform-specific profilers.
* Unit-test all failure paths. Use mocks/fakes to force error conditions.

---

# Practical patterns & examples

### 1) Small custom exception type

```cpp
struct parse_error : std::runtime_error {
  int position;
  parse_error(std::string msg, int pos)
    : std::runtime_error(std::move(msg)), position(pos) {}
};
```

### 2) Lightweight `Result` emulation (if `expected` missing)

```cpp
template <class T, class E>
struct Result {
  union { T val; E err; };
  bool ok;
  explicit Result(T v): val(std::move(v)), ok(true) {}
  explicit Result(E e): err(std::move(e)), ok(false) {}
  ~Result() { if(ok) val.~T(); else err.~E(); }
};
```

(This is skeletal; prefer `tl::expected` or `std::expected`.)

### 3) Map `errno` to `std::system_error`

```cpp
if (fd == -1) throw std::system_error(std::error_code(errno, std::generic_category()));
```

---

# Performance considerations

* Exception throwing has a cost at throw-time (stack unwinding) but little or no overhead at normal execution on most modern ABIs; however, dynamic linking and platform differences exist.
* Avoid throwing in tight loops on expected failure paths; prefer `expected` or error-code returns there.
* Making move operations `noexcept` often yields measurable performance improvements in container operations.

---

# Best practices (quick checklist)

* [ ] Document whether functions may throw and what exceptions they throw.
* [ ] Prefer RAII for resources; destructors must not throw.
* [ ] Use `noexcept` on move ctors when safe.
* [ ] Use `std::error_code` for portable, programmatic error handling.
* [ ] Use `std::expected` (or equivalent) for return-based error handling.
* [ ] Test error paths explicitly; use sanitizers.
* [ ] Keep error types small and semantically meaningful.

---

# Further reading (terms to search)

* RAII, Exception safety (Basic/Strong/No-throw), `std::error_code`, `std::system_error`, `std::expected`, `tl::expected`, Outcome library, ASan/UBSan, `std::terminate` and `std::exception_ptr`.

---
