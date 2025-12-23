# Carbonsight  
**Carbon-Aware Agentic AI Platform built on AWS**

Carbonsight is a generative AI orchestration platform that makes AI usage **measurable, optimizable, and sustainable**.  
It introduces carbon-aware routing, semantic caching, and agent-driven prompt intelligence to reduce the environmental cost of large language models without sacrificing user experience.

This project was built as part of an **AWS-sponsored Generative AI hackathon**, using Amazon Bedrock, AWS Lambda, DynamoDB, and a modern React frontend.

---

## Problem Statement

As generative AI adoption grows, its **energy consumption and carbon footprint remain largely invisible** to users and organizations. Most AI systems optimize for speed or cost, but not sustainability.

Carbonsight addresses this gap by making AI systems **carbon-aware by design**.

---

## Core Idea

Carbonsight helps developers and organizations:
- Measure the energy and CO₂ impact of AI usage
- Actively reduce carbon emissions through intelligent agents
- Visualize and incentivize sustainable AI behavior

---

## Key Features

### 1. Carbon-Aware Model Routing
Each request is dynamically routed to the **lowest-carbon viable model** based on task complexity.

- Micro → Lite → Pro model selection
- Token-aware and complexity-aware routing
- Prevents unnecessary use of high-carbon models

---

### 2. Semantic & Embedding-Based Caching
Carbonsight avoids redundant LLM calls by:

- Generating embeddings for incoming prompts
- Performing semantic similarity matching
- Serving cached responses when similarity exceeds a threshold

This directly saves compute, cost, and carbon emissions.

---

### 3. R-EcoWrite (Prompt Optimization Agent)
An agent that rewrites user prompts to be:

- Shorter
- Less redundant
- Semantically equivalent

The optimized prompt is used internally, while the user always sees their original input.  
Carbon savings are transparently displayed in the UI.

---

### 4. Prompt Coach (Pre-Send Guidance)
A lightweight agent that runs **before** a prompt is sent:

- Analyzes clarity and redundancy
- Estimates energy usage
- Suggests improvements without triggering an LLM call

This reduces wasted tokens and improves output quality.

---

### 5. Eco-Plan Agent (Structured Reasoning)
For medium and complex queries, Carbonsight can:

- Generate a step-by-step execution plan
- Display the plan to the user
- Inject the plan into the final LLM request

This improves reasoning quality, reduces hallucinations, and controls carbon usage.

---

### 6. Carbon Forecasting (Pluggable)
The system supports:

- Historical energy tracking
- Carbon usage forecasting
- Dashboard-level sustainability insights

A forecasting agent is included as an extensible module.

---

## Architecture Overview

### Frontend
- React + Vite
- TailwindCSS
- Interactive chat interface
- Carbon visualizations and agent toggles

### Backend
- AWS Lambda (Python)
- Amazon Bedrock (Nova models)
- DynamoDB for semantic caching
- Agent-based orchestration layer

---

## Repository Structure

### Backend (`carbonsight-backend/`)

```text
bedrock_client.py        # Bedrock model & embedding invocation
carbon_agent.py          # Energy & CO₂ estimation
carbon_forecast_agent.py # Forecasting logic
coach_agent.py           # Prompt Coach agent
eco_rewrite_agent.py     # Prompt optimization (R-EcoWrite)
eco_plan_agent.py        # Execution plan generator
embedding_agent.py       # Embedding & similarity pipeline
routing_agent.py         # Complexity classification & model routing
thinking_agent.py        # Token budget allocation
dynamo_cache.py          # Semantic cache persistence
similarity.py            # Vector similarity utilities
lambda_function.py       # API router (/ask, /optimize, /coach, /plan)
utils.py                 # Shared helpers
Frontend (carbonsight-frontend/)
text
Copy code
src/
  components/
    CarbonTooltip.jsx
    OptimizedChip.jsx
    PromptSuggestor.jsx
    CarbonForecastPanel.jsx
    Navbar.jsx
    Sidebar.jsx
  App.jsx
public/
index.html
tailwind.config.js
vite.config.js
```