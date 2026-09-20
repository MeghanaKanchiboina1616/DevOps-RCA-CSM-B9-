# AI DevOps Copilot for Intelligent Incident Management Using Hybrid Context-Aware RAG

## 1. Project Overview

Modern cloud-native applications are continuously developed and deployed using DevOps technologies such as GitHub, Docker, Kubernetes, and monitoring platforms. These environments generate large volumes of heterogeneous operational data, including application logs, deployment events, metrics, configuration changes, and version-control information.

When an incident occurs, DevOps engineers and Site Reliability Engineers (SREs) often need to manually examine information from multiple sources to identify the actual root cause. This process is time-consuming and can result in delayed incident resolution.

This project proposes an **AI DevOps Copilot based on a Context-Aware Hybrid Retrieval-Augmented Generation (RAG) framework** for intelligent and explainable DevOps incident root cause analysis.

The system will collect and correlate project-specific operational information, detect anomalous behavior using Machine Learning, retrieve relevant evidence using both semantic and lexical retrieval, rank the retrieved evidence according to the incident context, and use a Transformer-based root-cause model and Large Language Model (LLM) to generate an evidence-grounded diagnosis and remediation recommendation.

---

## 2. Research Problem

Existing cloud-native incident management approaches face difficulties when relevant information is distributed across multiple sources such as logs, metrics, deployment events, Git commits, historical incidents, and technical documentation.

LLM-based incident analysis can also produce unreliable explanations when insufficient or irrelevant context is provided.

Therefore, the research problem addressed by this project is:

> **Can context-aware hybrid retrieval, explicit evidence reranking, and Transformer-based root-cause ranking improve the reliability and explainability of LLM-assisted DevOps incident root cause analysis?**

---

## 3. Research Hypothesis

> **A context-aware Hybrid RAG framework that combines lexical retrieval, semantic retrieval, evidence reranking, and Transformer-based root-cause ranking will provide more accurate and evidence-grounded DevOps incident diagnosis than conventional retrieval and direct LLM-based approaches.**

The hypothesis will be evaluated experimentally using controlled DevOps incidents and quantitative evaluation metrics.

---

## 4. Objectives

The major objectives of this project are:

* To collect heterogeneous DevOps observability and operational data.
* To detect abnormal system behavior using Machine Learning.
* To construct incident-specific contextual information.
* To retrieve relevant evidence using both lexical and semantic retrieval.
* To use BM25 for lexical retrieval.
* To use BAAI/bge-small-en-v1.5 for semantic retrieval.
* To use a BGE reranker to prioritize relevant evidence.
* To use DeBERTa-v3-base for candidate root-cause ranking.
* To use Qwen2.5-7B-Instruct for evidence-grounded explanation generation.
* To provide explainable root-cause analysis and remediation recommendations.
* To maintain traceability between evidence, predicted root causes, and generated explanations.
* To compare the proposed approach with suitable baseline approaches.
* To experimentally evaluate the contribution of each major component.

---

# 5. Proposed System

The proposed system will operate as an automated incident investigation platform.

### Overall Workflow

```text
Developer
    ↓
GitHub
    ↓
Jenkins
    ↓
Docker
    ↓
Kubernetes
    ↓
Running Application
    ↓
Prometheus
    ↓
Logs / Metrics / Events / Deployments
    ↓
Data Collection
    ↓
ML Anomaly Detection
    ↓
Incident Creation
    ↓
Context Builder
    ↓
Hybrid Retrieval
 ┌───────────────┐
 │               │
BM25        Semantic Search
 │               │
 └───────┬───────┘
         ↓
Hybrid Results
         ↓
BGE Reranker
         ↓
Relevant Evidence
         ↓
DeBERTa-v3-base
         ↓
Root Cause Ranking
         ↓
Qwen2.5-7B-Instruct
         ↓
Evidence-Grounded Explanation
         ↓
AI DevOps Copilot Dashboard
```

---

# 6. Implementation Plan

The project will be implemented in multiple phases.

## Phase 1 — Research and Literature Study

The first phase will focus on understanding existing research related to:

* Cloud-native observability
* DevOps incident management
* Anomaly detection
* Root cause analysis
* Microservice failure diagnosis
* Large Language Models
* Retrieval-Augmented Generation
* Hybrid retrieval
* Evidence reranking
* Explainable AI

The selected research papers will be analyzed to identify their methodologies, datasets, limitations, evaluation metrics, and research gaps.

### Expected Output

* Literature review
* Research gap
* Research question
* Research hypothesis
* Final methodology

---

# Phase 2 — Controlled DevOps Environment

A controlled cloud-native environment will be created for experimentation.

Technologies:

* GitHub
* Jenkins
* Docker
* Kubernetes
* Prometheus

A sample microservice/application environment will be deployed on Kubernetes.

Controlled failures will be introduced to create realistic incident scenarios.

Examples:

* Application crash
* Kubernetes pod failure
* CrashLoopBackOff
* ImagePullBackOff
* Incorrect Docker image
* Database connection failure
* Invalid configuration
* High CPU utilization
* High memory utilization
* Deployment failure
* Increased application latency

Each experiment will maintain the actual root cause as ground truth.

---

# Phase 3 — DevOps Data Collection

The system will automatically collect operational information from the controlled DevOps environment.

### GitHub

The system will collect:

* Commit information
* Changed files
* Branch information
* Pull request information

### Jenkins

The system will collect:

* Build status
* Build logs
* Deployment status
* Build duration

### Kubernetes

The system will collect:

* Pod status
* Pod logs
* Kubernetes events
* Restart counts
* Deployment status

### Prometheus

The system will collect:

* CPU utilization
* Memory utilization
* Request rate
* Error rate
* Response latency

This information will form the operational evidence used during incident investigation.

---

# Phase 4 — Data Storage and Knowledge Base

PostgreSQL will be used for structured application and incident information.

PostgreSQL with pgvector will be used to store vector embeddings for semantic retrieval.

The knowledge base will contain:

* Technical documentation
* Kubernetes documentation
* Docker documentation
* Jenkins documentation
* Project-specific documentation
* Historical incidents
* Incident resolutions
* Organizational runbooks
* Relevant operational logs

The system will preserve metadata such as:

* Project
* Service
* Timestamp
* Incident ID
* Data source
* Deployment version

This metadata will help the retrieval system identify contextually relevant information.

---

# Phase 5 — Machine Learning Anomaly Detection

A Machine Learning-based anomaly detection component will identify abnormal system behavior.

The initial implementation will investigate **Isolation Forest** for detecting anomalies in numerical operational metrics.

Input features may include:

* CPU utilization
* Memory utilization
* Request latency
* Error rate
* Pod restart count
* Request rate

The output will identify whether the observed system behavior is normal or anomalous.

```text
Metrics
   ↓
Feature Extraction
   ↓
Isolation Forest
   ↓
Normal / Anomaly
   ↓
Incident Creation
```

The model will be evaluated using appropriate anomaly-detection metrics.

---

# Phase 6 — Incident Context Construction

When an anomaly or deployment failure is detected, an incident context will be constructed.

The context will combine information related to the same incident.

Example:

```text
Incident ID: INC-102

Service: Payment API

Time: 10:42 AM

Kubernetes:
CrashLoopBackOff

Prometheus:
CPU = 95%

Jenkins:
Build #54 Failed

GitHub:
Latest commit changed configuration

Historical Incident:
Similar failure occurred previously
```

The purpose of this stage is to prevent the retrieval system from searching the entire knowledge base without considering the current incident.

---

# Phase 7 — Hybrid Retrieval

The project will implement two complementary retrieval methods.

### Lexical Retrieval

**BM25** will retrieve evidence containing important technical terms.

For example:

```text
CrashLoopBackOff
OOMKilled
connection refused
ImagePullBackOff
```

### Semantic Retrieval

**BAAI/bge-small-en-v1.5** will generate embeddings and perform semantic similarity retrieval.

This allows conceptually similar evidence to be retrieved even when exact keywords are different.

### Hybrid Retrieval

The results from both retrieval methods will be combined.

```text
Incident Context
       ↓
 ┌─────┴─────┐
 ↓           ↓
BM25       BGE
 ↓           ↓
Lexical    Semantic
Results    Results
 └─────┬─────┘
       ↓
Hybrid Evidence
```

---

# Phase 8 — Evidence Reranking

The retrieved evidence will be passed through a **BGE reranker**.

The reranker will consider the current incident context and determine which retrieved documents or evidence are most relevant.

Instead of providing every retrieved result to the LLM, only the highest-ranked evidence will be selected.

```text
Retrieved Evidence
        ↓
BGE Reranker
        ↓
Relevance Scores
        ↓
Top-K Evidence
```

This stage is an important component of the proposed research because it explicitly investigates whether better evidence selection improves RCA performance.

---

# Phase 9 — Transformer-Based Root Cause Ranking

A **DeBERTa-v3-base Transformer** will be investigated for analyzing the selected evidence.

The model will produce ranked candidate root causes.

Example:

```text
Candidate Root Causes

1. Invalid Docker image tag       0.94
2. Kubernetes configuration error 0.03
3. Application code failure       0.02
4. Network failure                0.01
```

The model will therefore perform explicit root-cause ranking instead of relying entirely on the generative LLM.

---

# Phase 10 — LLM Explanation Generation

The ranked root cause and supporting evidence will be supplied to **Qwen2.5-7B-Instruct**.

The LLM will generate:

* Root-cause explanation
* Failure mechanism
* Supporting evidence
* Confidence information
* Recommended remediation
* Relevant commands where appropriate

The LLM will be instructed to base its response on the retrieved evidence rather than relying only on its pretrained knowledge.

---

# Phase 11 — Full-Stack Application

The research pipeline will be integrated into a full-stack web application.

### Frontend

**React + Material UI**

The dashboard will provide:

* Project overview
* Deployment history
* Incident list
* Monitoring information
* Incident details
* Root-cause analysis
* Evidence used for diagnosis
* AI recommendations
* Research evaluation results

### Backend

**FastAPI**

The backend will provide:

* Authentication
* Project management
* DevOps integrations
* Incident management
* Data collection APIs
* ML inference
* RAG pipeline
* LLM integration
* Evaluation APIs

### Database

**PostgreSQL + pgvector**

The database will store:

* Users
* Organizations
* Projects
* Deployments
* Incidents
* Logs
* Metrics
* Historical incidents
* Documents
* Embeddings
* RCA results

---

# Phase 12 — Experimental Evaluation

The proposed approach will not be evaluated only by demonstrating that the application works.

Controlled experiments will be conducted to determine whether the proposed methodology improves RCA performance.

### Baselines

The project will compare:

```text
Baseline 1
Direct LLM
        ↓
Root Cause

Baseline 2
Conventional RAG
        ↓
LLM
        ↓
Root Cause

Baseline 3
Hybrid RAG
        ↓
LLM
        ↓
Root Cause

Proposed
Hybrid RAG
    ↓
BGE Reranker
    ↓
DeBERTa RCA Ranking
    ↓
Qwen LLM
    ↓
Root Cause
```

### Evaluation Metrics

The evaluation will investigate:

* Root Cause Accuracy
* Precision
* Recall
* F1-Score
* Evidence Relevance
* Retrieval performance
* Response Time
* Explanation Quality
* Hallucination Rate

---

# Phase 13 — Ablation Study

An ablation study will be performed to determine the contribution of individual components.

Examples:

```text
Full System

vs.

Without BM25

vs.

Without Semantic Retrieval

vs.

Without Reranker

vs.

Without DeBERTa

vs.

Direct LLM
```

This will help determine which components actually contribute to the final RCA performance.

---

# 7. Technology Stack

## AI / Machine Learning

* Python
* Scikit-learn
* Isolation Forest
* PyTorch
* Hugging Face Transformers
* DeBERTa-v3-base
* Qwen2.5-7B-Instruct

## RAG

* BAAI/bge-small-en-v1.5
* BM25
* BGE Reranker
* pgvector
* LangChain or LlamaIndex

## Backend

* FastAPI
* Python
* SQLAlchemy
* PostgreSQL

## Frontend

* React
* TypeScript
* Material UI

## DevOps

* GitHub
* Jenkins
* Docker
* Kubernetes
* Prometheus

## Development / Deployment

* Git
* GitHub
* Docker
* Kubernetes

---

# 8. Expected Research Contribution

The project will investigate whether combining:

1. Context-aware incident construction,
2. Lexical and semantic hybrid retrieval,
3. Explicit evidence reranking,
4. Transformer-based root-cause ranking, and
5. Evidence-grounded LLM reasoning

can improve the reliability and explainability of DevOps incident root cause analysis.

The system will maintain a traceable relationship between:

```text
Incident
   ↓
Retrieved Evidence
   ↓
Evidence Ranking
   ↓
Predicted Root Cause
   ↓
LLM Explanation
   ↓
Recommended Remediation
```

This traceability will allow the generated diagnosis to be examined against the evidence used to produce it.

---

# 9. Project Scope

The project will be developed as a research prototype for a controlled cloud-native environment supporting multiple demonstration organizations/projects.

The project will focus on:

* Automated telemetry collection
* Anomaly detection
* Incident creation
* Context construction
* Hybrid retrieval
* Evidence reranking
* Root-cause ranking
* LLM-based explanation
* AI-assisted remediation recommendations
* Experimental evaluation

The project will not attempt:

* Fully autonomous production remediation
* Enterprise-scale deployment
* Supporting unlimited organizations
* Complete production-grade observability infrastructure
* Automatic execution of potentially destructive remediation commands

---

# 10. Expected Outcome

The expected outcome is a full-stack research prototype that can automatically investigate controlled DevOps incidents and provide:

* Probable root cause
* Confidence score
* Supporting evidence
* Explanation of the failure
* Recommended remediation

The research will determine whether the proposed Context-Aware Hybrid RAG approach improves root-cause analysis compared with conventional retrieval and direct LLM-based approaches.

---

# 11. Project Development Milestones

### Review 0

* Finalize research problem
* Select base paper
* Complete initial literature review
* Finalize research question and hypothesis
* Create GitHub repository
* Add abstract
* Add project README
* Finalize technology stack

### Review 1

* Complete detailed literature review
* Finalize system methodology
* Prepare DevOps experimental environment
* Set up GitHub, Jenkins, Docker, Kubernetes, and Prometheus
* Collect initial incident data
* Design database and knowledge base

### Review 2

* Implement telemetry collection
* Implement anomaly detection
* Implement incident context construction
* Implement BM25 and semantic retrieval
* Implement vector database
* Implement evidence reranking

### Review 3

* Implement DeBERTa root-cause ranking
* Integrate Qwen2.5-7B-Instruct
* Complete Hybrid RAG pipeline
* Integrate the React frontend and FastAPI backend
* Conduct controlled experiments

### Final Review

* Complete baseline comparisons
* Perform ablation studies
* Analyze results
* Prepare graphs and tables
* Complete research paper
* Complete project documentation
* Prepare final demonstration and presentation

---

# 12. Repository Structure

The repository will gradually be organized as follows:

```text
context-aware-devops-rca/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── projects.py
│   │   │   ├── integrations.py
│   │   │   ├── incidents.py
│   │   │   └── rca.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── integration.py
│   │   │   ├── event.py
│   │   │   ├── incident.py
│   │   │   └── evidence.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── integration.py
│   │   │   ├── incident.py
│   │   │   └── rca.py
│   │   │
│   │   ├── services/
│   │   │   ├── project_service.py
│   │   │   ├── incident_service.py
│   │   │   ├── correlation_service.py
│   │   │   └── evidence_service.py
│   │   │
│   │   ├── integrations/
│   │   │   ├── github/
│   │   │   │   └── client.py
│   │   │   ├── kubernetes/
│   │   │   │   └── client.py
│   │   │   ├── prometheus/
│   │   │   │   └── client.py
│   │   │   └── opentelemetry/
│   │   │       └── client.py
│   │   │
│   │   ├── rca_engine/
│   │   │   ├── preprocessing.py
│   │   │   ├── hybrid_retrieval.py
│   │   │   ├── reranker.py
│   │   │   ├── root_cause_ranker.py
│   │   │   ├── explanation.py
│   │   │   └── pipeline.py
│   │   │
│   │   └── utils/
│   │       └── logger.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── ProjectCard.jsx
│   │   │   ├── IncidentCard.jsx
│   │   │   └── EvidencePanel.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Projects.jsx
│   │   │   ├── ProjectDetails.jsx
│   │   │   ├── Incidents.jsx
│   │   │   └── RCAResult.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── public/
│   ├── package.json
│   └── index.html
│
└── database/
    ├── schema.sql
    ├── tables/
    │   ├── users.sql
    │   ├── projects.sql
    │   ├── integrations.sql
    │   ├── events.sql
    │   ├── incidents.sql
    │   └── evidence.sql
    │
    └── indexes/
        └── pgvector_indexes.sql
```

---

# 13. Team Development Approach

The project will be developed collaboratively using GitHub.

Each team member will work on assigned modules using separate branches.

Example:

```text
main
 │
 ├── backend
 ├── frontend
 ├── ml
 ├── rag
 └── devops
```

Changes will be submitted through pull requests and reviewed before being merged into the main branch.

The repository will maintain the development history, research documentation, implementation progress, experiments, and final results.
