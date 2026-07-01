# source_code/ index

Four language packages comprising the MASE simulation engine:

- `rust_pkg/` — Cargo.toml + Cargo.lock + src/lib.rs (+ subsystem modules).
  **lib-tinypath@1.4.2** declared in Cargo.toml (CVE-2026-21847).
- `go_pkg/` — go.mod + go.sum + main.go (+ helper modules).
- `py_pkg/` — pyproject.toml + poetry.lock + src/mase_sim/*.py.
  **colorz@2.3.1** declared in pyproject.toml (suspected typosquat of colorz-py).
- `js_pkg/` — package.json + package-lock.json + src/*.js.
