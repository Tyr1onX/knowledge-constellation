# External Auditor — source-only notes

Case: `2026-08-18-burntsushi-01`

The strongest public structure is not simply “Rust expertise.” It is a set of long-lived developer tools and libraries where performance, correctness and API constraints are repeatedly explicit: ripgrep search, Jiff datetime design, and memchr low-level string-search primitives.

Strongly supported: ripgrep project stewardship; search benchmark/workload judgment; Jiff API/dependency/stability design; direct recent Jiff maintenance and test correction; memchr as a real low-level search-library context with explicit multi-method testing.

Boundaries: do not attribute regex/PCRE2/crossbeam or every SIMD/search algorithm solely to the subject; do not infer rustc/compiler internals; do not generalize search-specific performance judgment to arbitrary systems domains.
