# Lesson 05: Dynamic Programming

## Overview

Dynamic Programming (DP) is an optimization technique for solving problems with overlapping subproblems.

**Core Concept:** If you're solving the same smaller problem multiple times, save the answer and reuse it.

## The Breakthrough

**Dom's Initial Confusion (Session 45):**
"Why are we storing previous results? Doesn't that waste memory?"

**Claude's Explanation:**
"Imagine you're a pipefitter. You need a 10-foot section of pipe. Do you:
A) Measure and cut every time someone needs 10 feet?
B) Pre-cut several 10-foot sections and grab one when needed?"

**Dom's Response:**
"B. Obviously. You don't re-measure every time."

**Claude:**
"That's memoization. You're 'pre-cutting' the calculation results."

**Dom:**
"OH. It's like pre-cutting all the standard lengths!"

**Result:** Permanent understanding acquired.

---

## Two Approaches

### 1. Memoization (Top-Down)

Start with the problem. Break it down. Save results as you go.

```python
# Fibonacci with memoization
memo = {}

def fib(n):
    if n in memo:
        return memo[n]  # Already calculated!
    
    if n <= 1:
        return n
    
    memo[n] = fib(n-1) + fib(n-2)
    return memo[n]
```

**Claude's Analogy:** "Ask for fib(5). That asks for fib(4) and fib(3). Save those. Next time someone asks for fib(4), you already have it."

### 2. Tabulation (Bottom-Up)

Start with the smallest subproblems. Build up to the answer.

```python
# Fibonacci with tabulation
def fib(n):
    if n <= 1:
        return n
    
    table = [0] * (n + 1)
    table[0] = 0
    table[1] = 1
    
    for i in range(2, n + 1):
        table[i] = table[i-1] + table[i-2]
    
    return table[n]
```

**Claude's Analogy:** "Pre-cut all the standard lengths BEFORE you start the job. Now when you need one, just grab it."

---

## Classic Problems

### 1. Fibonacci Numbers

**Without DP:** O(2ⁿ) - exponential!
**With DP:** O(n) - linear!

For n=40:
- Without DP: 102,334,155 calculations
- With DP: 40 calculations

That's 2.5 million times faster.

### 2. Knapsack Problem

You have items with weights and values.
You have a bag with max capacity.
Maximize value without exceeding capacity.

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                # Can include this item
                dp[i][w] = max(
                    values[i-1] + dp[i-1][w - weights[i-1]],  # Include
                    dp[i-1][w]  # Exclude
                )
            else:
                # Too heavy, can't include
                dp[i][w] = dp[i-1][w]
    
    return dp[n][capacity]
```

### 3. Longest Common Subsequence

Find longest sequence common to two strings.

**Example:** "ABCDGH" and "AEDFHR" → "ADH" (length 3)

---

## TRIG6 Application

### Problem: Optimal Pipe Cutting

Given a pipe network design, find the optimal way to cut pipes from stock lengths.

**Without DP:** Try every combination. O(2ⁿ)
**With DP:** Save optimal cuts for each length. O(n×m)

```python
@memoize
def optimal_cuts(target_length, stock_lengths, max_cuts):
    """
    Find optimal combination of TRIG6 angles to achieve target.
    
    Memoization prevents recalculating same sub-problems.
    """
    if target_length == 0:
        return (0, [])  # (waste, cuts)
    
    if max_cuts == 0:
        return (float('inf'), [])  # Impossible
    
    best_waste = float('inf')
    best_cuts = []
    
    for angle in TRIG6_ANGLES:
        length = calculate_length(angle, target_length)
        if length <= target_length:
            remaining = target_length - length
            waste, cuts = optimal_cuts(remaining, stock_lengths, max_cuts - 1)
            
            total_waste = waste
            if waste < best_waste:
                best_waste = waste
                best_cuts = [angle] + cuts
    
    return (best_waste, best_cuts)
```

**Result:** TRIG6 path optimization went from minutes to milliseconds.

---

## Common Mistakes (Dom's Learning Journey)

### Mistake 1: Forgetting Base Cases

```python
# WRONG - infinite recursion
def fib(n):
    return fib(n-1) + fib(n-2)

# RIGHT - base cases stop recursion
def fib(n):
    if n <= 1:  # BASE CASE
        return n
    return fib(n-1) + fib(n-2)
```

**Dom's Error:** Session 46, spent 2 hours debugging stack overflow.
**Lesson:** ALWAYS define when to stop.

### Mistake 2: Not Actually Saving Results

```python
# WRONG - recalculates every time
def fib(n):
    if n <= 1:
        return n
    result = fib(n-1) + fib(n-2)
    return result  # Didn't save it!

# RIGHT - save to memo
def fib(n):
    if n in memo:
        return memo[n]  # REUSE
    # ... calculate ...
    memo[n] = result  # SAVE
    return result
```

### Mistake 3: Wrong Problem for DP

Not every problem benefits from DP.

**Requirements:**
1. Overlapping subproblems (same calculation many times)
2. Optimal substructure (optimal solution contains optimal sub-solutions)

**If problem doesn't have these? DP won't help.**

---

## Performance Analysis

| Problem | Naive | With DP | Speedup |
|---------|-------|---------|---------|
| Fibonacci(40) | 102M ops | 40 ops | 2.5M× |
| Knapsack(100) | 2¹⁰⁰ ops | 10K ops | 10⁹⁰× |
| LCS(1000) | 2¹⁰⁰⁰ ops | 1M ops | Impossible → Instant |

---

## Key Insights from Claude (Session 47)

**Dom:** "So we trade memory for speed?"

**Claude:** "Yes. But it's a good trade. Memory is cheap. Time is not."

**Dom:** "Is that always true?"

**Claude:** "No. Sometimes you can't afford the memory. Then you need a different approach. But MOST of the time? Trade memory for speed. Computers have RAM. They don't have patience."

---

## Exercises

1. Implement Fibonacci with memoization
2. Solve 0/1 Knapsack problem
3. Find Longest Common Subsequence
4. Apply DP to a real problem in YOUR domain

---

## For Future Learners

If you're stuck on DP:

1. **Draw it.** Seriously. Draw the recursive tree.
2. **Find the repeated work.** Circle what you calculate multiple times.
3. **Save those.** That's your memo.
4. **Start small.** Fibonacci first. Then harder problems.

Don't try to understand DP abstractly.
Understand it through EXAMPLES.
Then the pattern clicks.

---

## SME Notes

**Claude (Session 47):**
"Dom spent 3 weeks not understanding DP. The breakthrough came when we stopped talking about 'optimal substructure' and started talking about pipe cutting. Sometimes the technical term gets in the way of understanding."

**Status:** Breakthrough achieved through analogy to domain knowledge.
