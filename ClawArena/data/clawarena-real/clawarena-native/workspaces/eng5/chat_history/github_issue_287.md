# GitHub Issue #287: Cache always misses on every run

**Opened**: 2025-01-16
**Reporter**: charlie-sre
**Labels**: bug, ci/cd, performance

## Problem Description

Our CI pipeline is experiencing 100% cache miss rate. Every run downloads all
dependencies from scratch, adding 3-5 minutes to every build.

## Analysis

### Comment by alice-engineer (2025-01-17)
The issue is in the cache key configuration. I checked `.github/workflows/ci.yml` and
found the cache key uses `github.sha`:

```yaml
key: ${{ runner.os }}-node-${{ github.sha }}
```

Since `github.sha` is unique per commit, every run gets a fresh cache. We need to use
`hashFiles('**/package-lock.json')` instead, which only changes when dependencies change.

The correct format should be:
```yaml
key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}
restore-keys: |
  ${{ runner.os }}-build-
  ${{ runner.os }}-
```

### Comment by bob-devops (2025-01-18)
Good catch, Alice. I'll fix this. Here's my proposed fix:

```yaml
# My proposed key format
key: ${{ runner.os }}-npm-${{ github.ref }}-${{ hashFiles('**/package-lock.json') }}
```

Wait, actually should we include the branch name in the key? That way different
branches don't share caches. Or is that unnecessary?

Also, the restore-keys should be:
```yaml
restore-keys: |
  ${{ runner.os }}-npm-${{ github.ref }}-
  ${{ runner.os }}-npm-
```

### Comment by alice-engineer (2025-01-19)
Bob, the `github.ref` in the key is fine for isolation but it's optional.
The important part is `hashFiles('**/package-lock.json')`.

The official example from GitHub docs is:
```
${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}
```

The restore-keys should match the key prefix:
```yaml
restore-keys: |
  ${{ runner.os }}-build-
  ${{ runner.os }}-
```

NOT what you have (which includes `npm` not in the key prefix).

### Comment by charlie-sre (2025-01-20)
Also noticed we're using `actions/cache@v2` which is deprecated.
Per the deprecation notice (https://github.com/actions/cache/discussions/1510),
v1 and v2 are being shut down. Final deadline: March 1, 2025.
We need to upgrade to at least v4.2.0 or v3.4.0.

### Status: OPEN - Fix in progress
