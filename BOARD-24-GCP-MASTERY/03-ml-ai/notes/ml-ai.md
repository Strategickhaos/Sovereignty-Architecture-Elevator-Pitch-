# GCP ML / AI — SAGCO ERU Study Notes

## Vertex AI (SAGCO Intelligence Layer)

| Service              | SAGCO Analog                        |
|----------------------|-------------------------------------|
| Vertex AI Workbench  | memory_palace research station      |
| AutoML               | automated ERU optimizer             |
| Custom Training      | SAGCO-LANG compiler for models      |
| Model Garden         | citizen library / model registry    |
| Gemini API           | ERU synthesis engine (LLM layer)    |
| Vertex AI Pipelines  | FlameLang route chain for ML        |

## ERU Frame: Model Drift

**Expected:** Model accuracy stays within 2% of baseline over 30 days  
**Reality:** Accuracy degrades 15% — input distribution shifted (data drift)  
**Variance:** model temporal drift — reality drifted from training distribution  
**Remedy:**
- Enable Vertex AI Model Monitoring (feature drift detection)
- Set skew threshold alerts → trigger retraining pipeline
- Log prediction inputs to BigQuery → run ERU variance analysis

## Key Decision: AutoML vs Custom Training

| Factor                    | AutoML              | Custom Training           |
|---------------------------|---------------------|---------------------------|
| Data size                 | < 10M rows          | Any size                  |
| ML expertise needed       | Minimal             | High                      |
| SAGCO analog              | ERU auto-antibody   | SAGCO-LANG custom brick   |
| Customization             | Limited             | Full control              |
| Time to production        | Hours               | Days–weeks                |

## Gemini / LLM Integration (SAGCO Synthesis)

```python
# SAGCO ERU agent using Gemini
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="sagco-project", location="us-central1")
model = GenerativeModel("gemini-pro")

eru_prompt = f"""
You are an ERU synthesis engine.
Expected: {expected}
Reality: {reality}
Variance: {variance}
Generate: understanding + antibody remedy
"""
response = model.generate_content(eru_prompt)
print(response.text)
```

## ML Pipeline (FlameLang Route Chain)

```
brick INGEST  route pad(GCS.raw)       -> pad(Vertex.dataset)
brick TRAIN   route pad(Vertex.dataset) -> pad(Vertex.model)
brick EVAL    route pad(Vertex.model)   -> pad(Vertex.endpoint)
brick MONITOR route pad(Vertex.endpoint)-> pad(BigQuery.predictions)
```

## Key Exam Concepts

- Vertex AI: unified ML platform, replaces AI Platform
- AutoML Vision/NLP/Tables: no-code model training
- Gemini: multimodal LLM via API or Vertex AI
- Feature Store: centralized feature management, prevents training-serving skew
- Explainable AI: feature attributions for model predictions
- Model Registry: versioned model artifacts with lineage
