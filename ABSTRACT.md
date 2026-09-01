 
MAJOR PROJECT REGISTRATION FORM 
                                                                       Date: 
Project 
Category:  
☐  Research oriented    ☐  Application oriented      
☐  Product oriented      ☐  Other (please specify)  
Specify if others: 
Batch ID:  CSM-B9 
. 
Title of the Project: Context-Aware DevOps Root Cause Analysis Using Hybrid RAG, Transformers, and LLMs 
Abstract 
DevOps and cloud-native environments generate large volumes of heterogeneous 
operational data, including logs, deployment events, metrics, traces, configuration changes, 
and version-control information. Although recent approaches use Machine Learning, Large 
Language Models (LLMs), and probabilistic reasoning for anomaly detection and root cause 
analysis, incident diagnosis remains challenging because relevant evidence is distributed 
across multiple sources, historical incidents are often underutilized, and LLM-generated 
diagnoses may lack systematic evidence selection. This project proposes a Context-Aware 
Hybrid Retrieval-Augmented Generation (RAG) framework for explainable DevOps 
incident root cause analysis. The research is motivated by recent work on cloud-native 
anomaly detection and root cause analysis using LLMs and Bayesian Networks, as well as 
research highlighting the importance of observability in cloud-native applications.The 
proposed framework integrates semantic retrieval using BAAI/bge-small-en-v1.5 and 
lexical retrieval using BM25 to retrieve relevant technical documentation, historical 
incidents, logs, deployment information, and project-specific evidence. A BGE reranker 
prioritizes the retrieved evidence according to the current incident context. A fine-tuned 
DeBERTa-v3-base Transformer then analyzes the selected evidence and ranks candidate 
root causes with confidence scores. Finally, Qwen2.5-7B-Instruct generates an evidence
grounded explanation and recommends appropriate remediation steps. The system will be 
implemented as a full-stack AI DevOps platform using React, FastAPI, PostgreSQL with 
pgvector, Docker, Kubernetes, Jenkins, GitHub, and Prometheus, enabling automated 
collection and analysis of DevOps telemetry.The framework will be evaluated using 
RCAEval together with controlled domain-specific incidents involving Kubernetes, Docker, 
Jenkins, Git, and application failures. Experiments will compare conventional retrieval, 
LLM-based diagnosis, and the proposed Hybrid RAG approach using root-cause ranking 
accuracy, Precision, Recall, F1-Score, evidence relevance, response time, and explanation 
quality. Ablation experiments will further examine the individual contribution of hybrid 
retrieval, reranking, and Transformer-based root-cause ranking. The expected outcome is an 
explainable AI-assisted DevOps incident management system that provides traceable 
relationships between retrieved evidence, predicted root causes, and generated explanations, 
thereby improving the reliability and effectiveness of automated root cause analysis. 
 

References (Category specific) 
1. Alharthi, A., Alsubhi, M., et al., Anomaly Detection and Root Cause Analysis in 
Cloud-Native Environments Using Large Language Models and Bayesian 
Networks, IEEE Access, Vol. 13, 2025. 
https://ieeexplore.ieee.org/document/10943534 
 
2. LLM-Augmented Knowledge Base Construction for Root Cause Analysis,” IEEE 
Access, 2026.  
https://doi.org/10.1109/ACCESS.2026.3658655 
 
3. Semi-Supervised and Disentangled Causal Discovery for Analyzing Fault 
Propagation in Microservices — IEEE Access, 2026. 
           https://ieeexplore.ieee.org/document/11182465 
 
4. Soares, A., et al., Toward the Observability of Cloud-Native Applications: The 
Overview of the State-of-the-Art, IEEE Access, Vol. 11, 2023. 
https://ieeexplore.ieee.org/document/10143912 
 
5. X. Liu, Y. Liu, M. Wei, and P. Xu, “LMGD: Log-Metric Combined Microservice 
Anomaly Detection Through Graph-Based Deep Learning,” IEEE Access, vol. 12, 
pp. 186510–186519, 2024. 
https://ieeexplore.ieee.org/document/10742168 
 
Project Team Members 
S. No. Regd. No. Name of the Student Signature 
1 23BQ1A4273 Kanchiboyina Meghana  
2 23BQ1A4282 Kodavatiganti Venkata 
Anantha Deepanjali 
3 23BQ1A42A9  Movva Poojitha  
    
    
 
Project Guide 
Name: Mrs. K. Deepika Signature:  
 