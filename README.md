# ✈️ Humanitarian Air Cargo Optimization: A Binary Integer Programming Approach

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.20%2B-FF4B4B.svg)](https://streamlit.io/)
[![PuLP](https://img.shields.io/badge/Optimization-PuLP-green.svg)](https://coin-or.github.io/pulp/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌐 Live Demo
Access the interactive dashboard here: **[air-cargo.streamlit.app](https://air-cargo.streamlit.app/)**

## 📖 Table of Contents
- [Project Overview](#-project-overview)
- [Real-World Motivation](#-real-world-motivation)
- [Why Binary Integer Programming?](#-why-binary-integer-programming)
- [The Problem: Multi-Constraint Knapsack](#-the-problem-multi-constraint-knapsack)
- [The Mathematical Model](#-the-mathematical-model)
  - [Decision Variables](#decision-variables)
  - [Objective Function](#objective-function)
  - [Detailed Constraints Analysis](#detailed-constraints-analysis)
- [Dataset Specifications & Item Catalog](#-dataset-specifications--item-catalog)
- [Technical Architecture](#-technical-architecture)
  - [Core Logic (model.py)](#core-logic-modelpy)
  - [User Interface (app.py)](#user-interface-apppy)
- [Installation & Setup](#-installation--setup)
- [Troubleshooting & FAQ](#-troubleshooting--faq)
- [The Team](#-the-team)
- [Future Roadmap](#-future-roadmap)
- [Conclusion](#-conclusion)

---

## 📋 Project Overview

In humanitarian crises—such as earthquakes, floods, or conflicts—the first 72 hours are critical. Logistics teams must transport emergency supplies using aircraft with limited carrying capacity, volume, and budget. Choosing the wrong combination of cargo can waste resources, reduce rescue efficiency, and delay aid delivery.

This project implements an **Advanced Multi-Constraint Knapsack Problem** solver using **Binary Integer Programming (BIP)**. It determines the mathematically optimal combination of items to load onto a cargo plane to maximize the total "Humanitarian Utility" (a composite score of importance and emergency priority).

## 🌍 Real-World Motivation

Logistics in humanitarian operations differ from commercial logistics in several ways:
1. **Criticality**: Medical supplies are often high-utility but may require cooling (refrigeration).
2. **Fragility**: High-tech tools or certain medical kits are fragile and increase damage risk if too many are packed together.
3. **Diversity**: A balanced shipment must include food, medicine, and tools—not just the highest-value items.
4. **Scarcity**: Resources (aircraft weight/volume) are extremely tight.

## 🧮 Why Binary Integer Programming?

In many optimization problems, we can deal with fractions (e.g., buying 2.5 tons of grain). However, in air cargo, we often deal with discrete items: you either load a specific medical crate or you don't. 

**Binary Integer Programming (BIP)** is a subset of Linear Programming where variables are restricted to 0 or 1. This makes it perfect for "Yes/No" decision-making:
- **0**: Item is rejected.
- **1**: Item is selected.

This approach guarantees that we don't end up with "half an airplane" or "0.7 of a medical kit," ensuring the solution is physically implementable in the real world.

## 🧠 The Problem: Multi-Constraint Knapsack

While a classic knapsack problem only considers weight and value, this model extends the logic to a realistic scenario by adding multiple conflicting dimensions:
- **Volume Constraints**: Items have different physical densities.
- **Budget Constraints**: Transportation and procurement costs vary.
- **Category Balance**: Ensuring the flight isn't just "all tools" or "all food."
- **Special Handling**: Managing specialized slots for refrigerated items.

## 📐 The Mathematical Model

### Decision Variables
For each available item $i \in \{A, B, C, D, E, F, G, H\}$, we define a binary variable $x_i$:
- $x_i = 1$ if item $i$ is selected for the shipment.
- $x_i = 0$ if item $i$ is excluded.

### Objective Function
The goal is to maximize the **Total Humanitarian Utility ($Z$)**. Each item has a utility score derived from its life-saving potential and urgency:
$$ \max Z = 60x_A + 80x_B + 90x_C + 75x_D + 30x_E + 75x_F + 60x_G + 30x_H $$

### Detailed Constraints Analysis

| Constraint | Equation | Significance |
| :--- | :--- | :--- |
| **Weight** | $\sum W_i x_i \le 65$ | Prevents aircraft overloading and ensures flight safety. |
| **Volume** | $\sum V_i x_i \le 12$ | Ensures the physical cargo hold can fit all selected items. |
| **Budget** | $\sum C_i x_i \le 120$ | Keeps the operation within the allocated mission budget. |
| **Medical** | $x_A + x_B + x_C \ge 2$ | Minimum healthcare kits required for the landing zone. |
| **Food** | $x_D + x_E \ge 1$ | Ensures at least one major nutritional supply is included. |
| **Fragility**| $x_A + x_B + x_F \le 2$ | Limits sensitive equipment to prevent transit damage. |
| **Refrigeration** | $x_B + x_C \le 2$ | Matches the limited power/cooling slots on the plane. |
| **Min Load** | $\sum x_i \ge 4$ | Ensures the flight has enough cargo to be mission-effective. |

## 📊 Dataset Specifications & Item Catalog

| Item | Category | Utility | Weight (kg) | Vol ($m^3$) | Cost ($) | Fragile | Cold |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **A** | Medical Kit | 60 | 10 | 2 | 25 | ✅ | ❌ |
| **B** | Vaccines | 80 | 20 | 3 | 40 | ✅ | ✅ |
| **C** | Specialized Med | 90 | 30 | 4 | 55 | ❌ | ✅ |
| **D** | High-Energy Food | 75 | 15 | 3 | 20 | ❌ | ❌ |
| **E** | Basic Rations | 30 | 5 | 1 | 10 | ❌ | ❌ |
| **F** | Comms Gear | 75 | 18 | 3 | 35 | ✅ | ❌ |
| **G** | Shelter Tools | 60 | 12 | 2 | 30 | ❌ | ❌ |
| **H** | Water Filters | 30 | 8 | 2 | 15 | ❌ | ❌ |

## 💻 Technical Architecture

The application follows a modular design to separate the mathematical optimization from the presentation layer.

### Core Logic (`model.py`)
The backend is powered by **PuLP**, a high-level modeling library in Python.
- **Solver**: It defaults to the **CBC (Coin-or branch and cut)** solver, which is an open-source Mixed Integer Linear Programming solver.
- **Feasibility**: The logic includes checks to detect "Infeasible" states, which occur if the user sets constraints so strictly that no combination of items can satisfy them.

### User Interface (`app.py`)
The frontend is built with **Streamlit**, enabling a rapid "Vibe Coding" development cycle.
- **Reactivity**: Every time a slider or input is changed, Streamlit re-runs the optimization, providing instant feedback.
- **Sidebars**: All capacity and requirement settings are tucked into an organized sidebar for a clean main dashboard.

## 🛠️ Installation & Setup

### Local Development
1. **Clone the repository**:
   ```bash
   git clone https://github.com/4awmy/humanitarian-air-cargo-optimization.git
   cd humanitarian-air-cargo-optimization
   ```
2. **Create a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## ❓ Troubleshooting & FAQ

**Q: Why do I get "No feasible solution found"?**
A: This happens if your constraints are too tight. For example, if you set "Max Weight" to 5kg but require "At least 2 Medical Items" (which weigh at least 30kg combined), the math becomes impossible. Try relaxing your capacity limits.

**Q: Do I need a special license for the solver?**
A: No, PuLP comes bundled with the open-source CBC solver.

**Q: Can I add more items?**
A: Currently, the items are hardcoded in `model.py` and `app.py`. To add more, you would update the dictionaries in both files.

## 👥 The Team

This project was developed by a team from the **Arab Academy for Science, Technology & Maritime Transport (AASTMT)**:

| Name | ID | Primary Contribution |
| :--- | :--- | :--- |
| **AbdulRahman Mohamed Farag** | 231015031 | Project Management & Lead Dev |
| **Ziad Reda Mohamed Hafez** | 231014601 | Optimization Model Design |
| **Marwan Ehab Ibrahim** | 231006121 | Data Engineering & Backend |
| **Marwan Omar Mesbah** | 231004622 | UI/UX & Documentation |

## 🚀 Future Roadmap
- [ ] **Multi-Aircraft Support**: Extend the model to optimize multiple planes simultaneously.
- [ ] **Dynamic Pricing**: Integrate real-time fuel and handling cost fluctuations.
- [ ] **AI-Powered Utility**: Use machine learning to predict utility scores based on historical disaster data.
- [ ] **Route Optimization**: Combine cargo selection with delivery route planning.

## 🏁 Conclusion

This project successfully demonstrates how **Operations Research** and **Mathematical Optimization** can be applied to solve high-stakes logistics problems. By replacing "gut feeling" with a robust BIP model, humanitarian organizations can ensure that every flight delivers the maximum possible benefit to those in need.

---
*Developed as part of the Optimization course at AASTMT.*
