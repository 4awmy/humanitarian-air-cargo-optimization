# Humanitarian Air Cargo Optimization

## Project Overview
This project focuses on optimizing the selection of humanitarian cargo items for air transport. Using **Binary Integer Programming (PuLP)**, the model aims to maximize the total humanitarian utility while adhering to critical constraints such as weight capacity, volume limits, budget restrictions, and specific humanitarian requirements (e.g., minimum medical and food items).

The project features an interactive **Streamlit** dashboard that allows users to adjust constraints and visualize the optimal cargo selection in real-time.

## Technologies Used
- **Python**: Core programming language.
- **PuLP**: Linear programming library used for the optimization model.
- **Streamlit**: Framework for building the interactive web interface.

## Team Members
- AbdulRahman Mohamed Farag
- Ziad Reda Mohamed Hafez
- Marwan Ehab Ibrahim
- Marwan Omar Mesbah

## How to Run
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the Streamlit app:
   ```bash
   streamlit run app.py
   ```
