# **Evaluating Language Models on Medical Question-Answering**

_Author: Hung Tran | Language and Intelligence Lab (LAILab)_

## **Overview**

This repository contains the code and resources for evaluating the performance of various large language models (LLMs) on medical question-answering tasks. Using clinical notes from DeepPhe, a natural language processing system for extracting cancer phenotypes, this project provides a comprehensive framework to test LLMs' ability to interpret and respond to medical queries accurately.

## **Key Features**

- **Integration with DeepPhe Clinical Notes:** Processes structured JSON outputs from DeepPhe and generates tailored medical question-answering datasets.
- **LLM Evaluation Framework:**
  - Models tested: GPT-4, GPT-3.5, Llama 2 (7B, 13B, 70B), Vicuna (7B, 13B, 33B), and Gemini.
  - Dual evaluation using:
    - **Natural Language Inference (NLI):** Semantic understanding.
    - **Longest Common Subsequence (LCS):** Verbatim matching.
- **Automated Testing and Scoring:** Includes a standardized system prompt, user prompts, and automated response evaluation.
- **Detailed Results Visualization:** Generates charts and statistical summaries to compare model performance by NLI and LCS scores.

## **Repository Contents**

- Python files: Core scripts for prompt generation, model interaction, and evaluation.
- `input/` and `output/`: Sample clinical notes and JSON outputs from DeepPhe.
- `evaluations/`: Results and visualizations, including bar graphs and box plots.

## **Getting Started**

### **Prerequisites**

- [uv](https://github.com/astral-sh/uv)

### **Setup**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/test-llm.git
   cd test-llm
   ```
2. Install dependencies:
   ```bash
   uv sync && source .venv/bin/activate
   ```

### **Usage**

**Run Testing Pipeline:**

```bash
python main.py
```

## **Evaluation Metrics**

1. **Natural Language Inference (NLI):** Measures semantic alignment using a cross-encoder transformer.
2. **Longest Common Subsequence (LCS):** Quantifies textual overlap with the ground truth.

## **Results**

- Models exhibited high LCS scores but varied significantly in NLI scores.
- `Gemini-Pro` achieved the highest NLI score but had lower LCS scores due to concise responses.
- Detailed bar graphs and distributions for each model and question type are available in the `evaluations/` directory.

## **Key Findings**

- **Strengths:**
  - High textual precision (LCS) across all models.
  - Consistent performance in factual recall tasks.
- **Challenges:**
  - Low semantic comprehension (NLI) in complex queries.
  - Difficulty with nuanced medical attributes and contextual understanding.

## **Future Directions**

- Train domain-specific LLMs to improve reasoning capabilities.
- Enhance evaluation metrics for medical QA tasks, focusing on reasoning accuracy and context handling.
- Explore advanced prompting strategies to enforce response consistency.

## **References**

- [DeepPhe](https://deepphe.github.io/)
- [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774)
- [Llama 2](https://arxiv.org/abs/2307.09288)
- [Vicuna](https://vicuna.lmsys.org/)
