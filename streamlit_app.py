import streamlit as st
import pandas as pd

# Function for login with stored password
def login():
    """Login function."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        
    if not st.session_state.logged_in:
        username = st.sidebar.text_input("Username")  # Ask for the username
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if username == "admin" and password == "Section87":  # Verify username and password
                st.session_state.logged_in = True
                st.success("Login successful!")
            else:
                st.error("Incorrect username or password")
    return st.session_state.logged_in


# Function to calculate salary increases
def calculate_salary_increases(base_salaries, fixed_percentage, variable_percentage, budget_percentage):
    total_base_salaries = sum(base_salaries)
    total_budget = (budget_percentage / 100) * total_base_salaries
    fixed_budget = (fixed_percentage / 100) * total_budget
    variable_budget = (variable_percentage / 100) * total_budget
    fixed_increase_per_employee = fixed_budget / len(base_salaries)
    variable_increases = [(variable_budget / total_base_salaries) * base_salary for base_salary in base_salaries]

    salary_data = []
    for i, base_salary in enumerate(base_salaries):
        level = f"C{i+3}"  # Levels from C3 to C8
        fixed_increase = fixed_increase_per_employee
        variable_increase = variable_increases[i]
        total_increase = fixed_increase + variable_increase
        final_salary = base_salary + total_increase
        percent_fixed_increase = (fixed_increase / base_salary) * 100
        percent_variable_increase = (variable_increase / base_salary) * 100
        percent_total_increase = (total_increase / base_salary) * 100
        salary_data.append([level, base_salary, round(fixed_increase, 2), round(variable_increase, 2), 
                            round(total_increase, 2), round(final_salary, 2),
                            round(percent_fixed_increase, 2), round(percent_variable_increase, 2), round(percent_total_increase, 2)])

    df = pd.DataFrame(salary_data, columns=[
        'Level', 'Base Salary (€)', 'Fixed Increase (€)', 'Variable Increase (€)', 
        'Total Increase (€)', 'Final Salary (€)', 
        '% Fixed Increase', '% Variable Increase', '% Total Increase'
    ])
    
    return df

# Streamlit Interface
if login():
    st.title("Work Council Salary Increase Calculator")

    # User inputs
    st.sidebar.header("Input Parameters")

    base_salaries = [st.sidebar.number_input(f"Enter base salary for C{i+3}", value=salary) for i, salary in enumerate([33000, 37000, 44000, 54000, 70000, 86000])]

    fixed_percentage = st.sidebar.slider("Fixed Percentage", min_value=0, max_value=100, value=50)
    variable_percentage = 100 - fixed_percentage  # Automatically calculate variable percentage
    budget_percentage = st.sidebar.number_input("Budget Percentage", value=5.0)

    # Calculate when the user presses the button
    if st.button("Calculate"):
        df_result = calculate_salary_increases(base_salaries, fixed_percentage, variable_percentage, budget_percentage)
        st.write(df_result)
else:
    st.warning("Please log in to access the application.")

