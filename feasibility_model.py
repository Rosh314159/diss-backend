import numpy as np
import math

# Helper function to calculate monthly mortgage payment
def calculate_monthly_payment(principal, annual_rate, term_years):
    monthly_rate = annual_rate / 12 / 100
    num_payments = term_years * 12
    if monthly_rate == 0:
        return principal / num_payments
    return principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)

# Helper function to calculate stamp duty
def calculate_stamp_duty(house_price, is_first_home):
    if is_first_home:
        if house_price <= 300000:
            return 0
        elif house_price <= 500000:
            return (house_price - 300000) * 0.05
        else:
            return (200000 * 0.05) + ((house_price - 500000) * 0.10)
    else:
        if house_price <= 125000:
            return 0
        elif house_price <= 250000:
            return (house_price - 125000) * 0.02
        elif house_price <= 925000:
            return (125000 * 0.02) + ((house_price - 250000) * 0.05)
        elif house_price <= 1500000:
            return (125000 * 0.02) + (675000 * 0.05) + ((house_price - 925000) * 0.10)
        else:
            return (125000 * 0.02) + (675000 * 0.05) + (575000 * 0.10) + ((house_price - 1500000) * 0.12)

# Feasibility assessment function
def get_feasibility(system_inputs, user_inputs):
    house_price = float(system_inputs['house_price'])
    loan_term_years = int(system_inputs['loan_term_years'])
    interest_rate = float(system_inputs['interest_rate'])
    property_tax = float(system_inputs['property_tax'])
    insurance = float(system_inputs['insurance'])
    utility_bills = float(system_inputs['utility_bills'])

    annual_income = float(user_inputs['annual_income'])
    debt_obligations = float(user_inputs['debt_obligations'])
    savings = float(user_inputs['savings'])
    is_first_home = bool(user_inputs['is_first_home'])

    monthly_income = annual_income / 12
    loan_amount = house_price - savings
    monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term_years)
    stamp_duty = calculate_stamp_duty(house_price, is_first_home)
    total_housing_costs = monthly_payment + property_tax + insurance + utility_bills

    dti_ratio = (debt_obligations + total_housing_costs) / monthly_income * 100
    ltv_ratio = (loan_amount / house_price) * 100
    mortgage_to_income_ratio = loan_amount / annual_income
    meets_mortgage_income_threshold = mortgage_to_income_ratio <= 4.5

    is_affordable = dti_ratio < 36 and total_housing_costs / monthly_income < 0.28 and meets_mortgage_income_threshold
    meets_ltv_threshold = ltv_ratio <= 80

    recommendations = []
    if not is_affordable:
        recommendations.append("Reduce monthly debt obligations, increase income, or choose a less expensive house.")
    if not meets_ltv_threshold:
        recommendations.append("Increase your deposit to lower the loan-to-value ratio.")
    if not meets_mortgage_income_threshold:
        recommendations.append("Consider a house with a lower price or increase your savings to reduce the required mortgage.")

    return {
        'monthly_payment': round(monthly_payment, 2),
        'total_housing_costs': round(total_housing_costs, 2),
        'stamp_duty': round(stamp_duty, 2),
        'dti_ratio': round(dti_ratio, 2),
        'ltv_ratio': round(ltv_ratio, 2),
        'mortgage_to_income_ratio': round(mortgage_to_income_ratio, 2),
        'is_affordable': is_affordable,
        'meets_ltv_threshold': meets_ltv_threshold,
        'meets_mortgage_income_threshold': meets_mortgage_income_threshold,
        'recommendations': recommendations
    }
