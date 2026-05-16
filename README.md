# ✈️ Humanitarian Air Cargo Optimization

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.0%2B-FF4B4B.svg)](https://streamlit.io/)
[![PuLP](https://img.shields.io/badge/Optimization-PuLP-green.svg)](https://coin-or.github.io/pulp/)

## 📋 Project Overview

In the wake of natural disasters or humanitarian crises, efficient logistics can be the difference between life and death. This project implements a **Binary Integer Programming (BIP)** model to solve a real-world multi-constraint knapsack problem for air cargo logistics.

The objective is to **Maximize Humanitarian Utility**—a metric representing the critical importance and emergency priority of items—while respecting the physical and financial limitations of the cargo aircraft.

## 🚀 Key Features

- **Mathematical Optimization**: Uses the CBC solver via PuLP to find the mathematically optimal cargo mix.
- **Interactive Dashboard**: Real-time adjustment of constraints (Weight, Volume, Budget) via Streamlit.
- **Humanitarian Constraints**: Integrated logic for medical minimums, food requirements, fragile item handling, and cold storage limits.
- **Visual Analytics**: Instant feedback on capacity utilization and utility scores.

## 🧠 The Mathematical Model

### Objective Function
Maximize the total humanitarian utility $Z$:
$$ \max Z = \sum_{i \in Items} \text{Utility}_i \cdot x_i $$
Where $x_i \in \{0, 1\}$ is a binary variable indicating if item $i$ is selected.

### Primary Constraints
1.  **Weight Capacity**: $\sum \text{Weight}_i \cdot x_i \le 65$ kg
2.  **Volume Capacity**: $\sum \text{Volume}_i \cdot x_i \le 12$ units
3.  **Budget**: $\sum \text{Cost}_i \cdot x_i \le \$120$
4.  **Medical Priority**: At least 2 medical items must be included.
5.  **Food Security**: At least 1 food package must be included.
6.  **Fragile Handling**: Maximum 2 fragile items allowed.
7.  **Cold Chain**: Maximum 2 refrigerated slots available.

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/4awmy/humanitarian-air-cargo-optimization.git
   cd humanitarian-air-cargo-optimization
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## 👥 The Team

| Name | Role / ID |
| :--- | :--- |
| **AbdulRahman Mohamed Farag** | Lead Developer |
| **Ziad Reda Mohamed Hafez** | Optimization Analyst |
| **Marwan Ehab Ibrahim** | Data Engineer |
| **Marwan Omar Mesbah** | UI/UX & Documentation |

---
*Developed for the Arab Academy for Science, Technology & Maritime Transport (AASTMT).*
