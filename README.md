Carbonsight

Carbon-Aware Agentic AI Platform built on AWS

Carbonsight is a generative-AI orchestration platform that makes AI usage measurable, optimizable, and sustainable.
It introduces carbon-aware routing, semantic caching, and agent-driven prompt intelligence to reduce the environmental cost of large language models without sacrificing user experience.

This project was built as part of an AWS-sponsored Generative AI hackathon, using Amazon Bedrock, AWS Lambda, DynamoDB, and a modern React frontend.

Core Idea

As generative AI adoption grows, its energy and carbon footprint remains largely invisible to users and organizations.

Carbonsight addresses this gap by:

Measuring energy and CO₂ impact of each AI interaction

Actively reducing carbon usage through intelligent agents

Making sustainability observable, actionable, and incentivized

Key Features
1. Carbon-Aware Model Routing

Each request is dynamically routed to the lowest-carbon viable model based on task complexity:

Micro → Lite → Pro model selection

Token-aware and complexity-aware routing

Prevents unnecessary use of high-carbon models

2. Semantic & Embedding-Based Caching

Carbonsight avoids redundant LLM calls by:

Generating embeddings for incoming prompts

Performing similarity matching against cached responses

Serving cached answers when semantic similarity exceeds a threshold

This directly saves compute, cost, and carbon emissions.

3. R-EcoWrite (Prompt Optimization Agent)

An agent that rewrites user prompts to be:

Shorter

Less redundant

Semantically equivalent

The optimized prompt is used internally, while the user always sees their original input.
Carbon savings are transparently displayed.

4. Prompt Coach (Pre-Send Guidance)

A lightweight agent that:

Analyzes prompt clarity and redundancy

Estimates energy usage before execution

Suggests improvements without sending a model request

This reduces wasted tokens and improves output quality.

5. Eco-Plan Agent (Structured Reasoning)

For medium and complex queries, Carbonsight can:

Generate a step-by-step execution plan

Display the plan to the user

Inject the plan into the final LLM call

This improves reasoning quality and reduces hallucinations while keeping usage controlled.

6. Carbon Forecasting (Pluggable)

The system is designed to support:

Historical energy tracking

Carbon usage forecasting

Dashboard-level insights (user, team, org)

A forecasting agent is included as an extensible module.

Architecture Overview

Frontend

React + Vite

TailwindCSS

Interactive chat UI

Carbon visualizations

Agent toggles (Optimize, Coach, Eco-Plan)

Backend

AWS Lambda (Python)

Amazon Bedrock (Nova models)

DynamoDB (semantic cache)

Agent-based orchestration layer

Repository Structure
Backend (carbonsight-backend/)
bedrock_client.py        # Bedrock model + embedding invocation
carbon_agent.py          # Energy & CO₂ estimation
carbon_forecast_agent.py # Forecasting logic
coach_agent.py           # Prompt Coach agent
eco_rewrite_agent.py     # Prompt optimization (R-EcoWrite)
eco_plan_agent.py        # Execution plan generator
embedding_agent.py       # Embedding + similarity pipeline
routing_agent.py         # Complexity classification & model routing
thinking_agent.py        # Token budget allocation
dynamo_cache.py          # Semantic cache persistence
similarity.py            # Vector similarity utilities
lambda_function.py       # API router (/ask, /optimize, /coach, /plan)
utils.py                 # Shared helpers

Frontend (carbonsight-frontend/)
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

API Endpoints
Endpoint	Description
/ask	Main AI response endpoint
/optimize	Prompt rewriting (R-EcoWrite)
/coach	Prompt coaching & energy estimation
/plan	Eco-Plan generation
/forecast	Carbon usage forecasting
Running Locally
Frontend
cd carbonsight-frontend
npm install
npm run dev

Backend

Deployed on AWS Lambda

Uses Amazon Bedrock (Nova models)

Requires AWS credentials with Bedrock access

Why This Is a Strong Hackathon Project

Uses real AWS GenAI infrastructure

Tackles climate + AI sustainability, a critical emerging problem

Goes beyond a chat app into agentic system design

Demonstrates production-ready thinking (routing, caching, observability)

Easily extensible to enterprise dashboards (User / Team / Admin)

Future Extensions

Organization-wide ESG reporting

Carbon-aware cost optimization dashboards

Model usage heatmaps

Blockchain-based sustainability credits (optional)

SageMaker-based forecasting models

Team

Built by Advita Shrivastava
AWS ImpactX / Generative AI Innovate & Build Challenge
