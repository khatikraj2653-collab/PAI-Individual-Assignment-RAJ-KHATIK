# PAI-Individual-Assignment-RAJ-KHATIK

# Public Health Inference System

## Overview

This repository contains the **individual assignment** for *Programming for Artificial Intelligence*.  
The project implements a **Rule-Based Public Health Inference System** that allows users to create, update, and delete public-health scenarios and to infer health outcomes using deterministic logic.

The system emphasises **explainability**, **reproducibility**, and **database-driven analytics** without reliance on external APIs or CSV datasets.


## Author

**Raj Tejpal Khatik**  
Individual Assignment


## Project Structure

The project is implemented entirely in Python and follows a modular design:

- **User Interface:** Streamlit-based web interface  
- **Inference Engine:** Rule-based logic for outcome estimation  
- **Database Layer:** SQLite for persistent storage  
- **Analytics Module:** Summary statistics and trend analysis  
- **Testing:** Test-Driven Development (TDD) using PyTest  



## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt


```
## Task 2 – Supermarket Analysis

### Overview
Task 2 implements a statistical market basket analysis system to identify purchasing patterns from supermarket transaction data.  
The solution avoids graphical visualisation and machine learning models, focusing instead on explainable statistical metrics.

The system analyses transaction data to compute **support**, **confidence**, and **lift**, which are widely used measures in association analysis and recommendation systems.



### Approach
The analysis follows these steps:
1. Load and preprocess transaction data from CSV
2. Group items by customer identifier to form transactions
3. Compute statistical metrics (support, confidence, lift)


