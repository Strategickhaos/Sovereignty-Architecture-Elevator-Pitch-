# Optimization Module - The 880x Cost Reduction Compiler

## Purpose
This directory implements pre-compiler optimization passes based on the **880x Cost Reduction Model**. It automatically flags functions that would be cheaper to run on local Qwen2.5 nodes versus paid cloud APIs.

## Cost Model

The 880x reduction comes from:
1. **Local Inference**: Qwen2.5 on RTX 4090 vs GPT-4 API
2. **Batch Processing**: Group similar operations
3. **Caching**: Avoid redundant LLM calls
4. **Quantization**: 4-bit models for routine tasks
5. **Prompt Compression**: Reduce token usage by 90%

## Structure

```
optimization/
├── passes/
│   ├── cost_analysis.flame       # Analyze compute cost per function
│   ├── model_router.flame        # Route to cheapest model
│   ├── prompt_compressor.flame   # Compress prompts
│   └── cache_optimizer.flame     # Intelligent caching
├── models/
│   ├── local_qwen.yaml          # Local Qwen2.5 config
│   ├── cloud_apis.yaml          # OpenAI/Anthropic pricing
│   └── cost_database.json       # Historical cost data
└── README.md
```

## Pre-Compiler Pass

The optimization pass runs during compilation:

```flame
fn optimize_function(func: Function) -> OptimizationDecision {
    let cost_local = estimate_local_cost(func);
    let cost_cloud = estimate_cloud_cost(func);
    
    if cost_local < cost_cloud / 880.0 {
        return OptimizationDecision::UseLocal(Qwen2_5);
    } else if can_batch(func) {
        return OptimizationDecision::Batch(func);
    } else if is_cacheable(func) {
        return OptimizationDecision::Cache(func);
    } else {
        return OptimizationDecision::UseCloud(select_cheapest_api(func));
    }
}
```

## Cost Analysis Factors

1. **Token Count**: Input + expected output tokens
2. **Latency Requirement**: Real-time vs batch
3. **Quality Requirement**: Does it need GPT-4 or is Qwen2.5 sufficient?
4. **Frequency**: How often is this function called?
5. **Context Size**: Large context = prefer local models

## Example

```flame
// This function will be flagged for local execution
@optimize(target = "local")
fn generate_code_comment(code: String) -> String {
    // Cost Analysis:
    // - Input tokens: ~100
    // - Output tokens: ~50
    // - Quality: Medium (Qwen2.5 sufficient)
    // - Frequency: High (thousands/day)
    // Decision: Use local Qwen2.5 = $0.00 vs GPT-4 = $0.15/call
    llm_query("Generate comment", code)
}

// This function will use cloud API
@optimize(target = "cloud", model = "gpt-4")
fn solve_complex_architecture(problem: String) -> Architecture {
    // Cost Analysis:
    // - Input tokens: ~5000
    // - Output tokens: ~2000
    // - Quality: High (needs GPT-4)
    // - Frequency: Low (few/day)
    // Decision: Use GPT-4 = $1.40/call (worth the quality)
    llm_query("Architect solution", problem)
}
```

## Compiler Flags

During build, the optimizer generates warnings:

```
⚠️  COST WARNING: Function `generate_summary` would cost $450/day on GPT-4 API
    Suggestion: Use local Qwen2.5 to save $449.50/day (99.9% savings)
    Estimated 880x cost reduction: $164,250/year → $186/year

✅  Function `critical_analysis` properly routed to GPT-4 API
    This function requires high-quality reasoning: $42/day (acceptable)
```

## Integration with Legion of Minds

The cost optimizer integrates with `src/council/` to:
1. Route simple tasks to Qwen2.5 (local)
2. Route medium tasks to Claude Sonnet (API)
3. Route complex tasks to GPT-4 (API)
4. Batch operations across all models

This creates a **hierarchical compute strategy** that maximizes quality while minimizing cost.
