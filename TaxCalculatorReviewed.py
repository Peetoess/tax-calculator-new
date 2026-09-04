#Jeremy Ge and Peter Wang
#TaxCalculatorReviewed.py
#September 3, 2026
#A tax calculator for people living in Ontario in the year of 2026.

import sys

#Function that prompts user to enter in their annual income.
def get_income():
    user_income = float(input("Enter your annual income in Canadian Dollars: "))
    if user_income < 12989:
        print("You owe $0 tax, making under the Ontario BPA in 2026.")
        sys.exit(0)
    return user_income

#Function that allows user to enter in deductions.
def get_eligible_deductions():
    while True:
        choice = input("Enter eligible deductions 'one by one' or as a 'total'?: ").strip().lower()
        
        if choice == "one by one":
            deductions: list[float] = []
            while True:
                user_input = input("Enter a deduction amount (Type DONE to finish): ").strip()
                if user_input.upper() == "DONE":
                    return sum(deductions)
                try:
                    deductions.append(float(user_input))
                except ValueError:
                    print("Invalid input. Please enter a number or DONE.")
                    
        elif choice == "total":
            return float(input("Please enter your total eligible deductions: "))
        else:
            print("Invalid choice, please try again.")

#Function that calculates Federal Tax.
def calc_federal_tax(taxable_income):
    tax_rates = [0.14, 0.205, 0.26, 0.29, 0.33]
    brackets = [58523, 117045, 181440, 258482]

    if taxable_income <= brackets[0]:
        return taxable_income * tax_rates[0]
    elif taxable_income <= brackets[1]:
        return (brackets[0] * tax_rates[0]) + ((taxable_income - brackets[0]) * tax_rates[1])
    elif taxable_income <= brackets[2]:
        return (brackets[0] * tax_rates[0]) + ((brackets[1] - brackets[0]) * tax_rates[1]) + ((taxable_income - brackets[1]) * tax_rates[2])
    elif taxable_income <= brackets[3]:
        return (brackets[0] * tax_rates[0]) + ((brackets[1] - brackets[0]) * tax_rates[1]) + ((brackets[2] - brackets[1]) * tax_rates[2]) + ((taxable_income - brackets[2]) * tax_rates[3])
    else:
        return (brackets[0] * tax_rates[0]) + ((brackets[1] - brackets[0]) * tax_rates[1]) + ((brackets[2] - brackets[1]) * tax_rates[2]) + ((brackets[3] - brackets[2]) * tax_rates[3]) + ((taxable_income - brackets[3]) * tax_rates[4])

#Function that calculates Ontario Tax.
def calc_ontario_tax(taxable_income):
    tax_rates = [0.0505, 0.0915, 0.1116, 0.1216, 0.1316]
    brackets = [53891, 107785, 150000, 220000]
    
    if taxable_income <= brackets[0]:
        return taxable_income * tax_rates[0]
    elif taxable_income <= brackets[1]:
        return (brackets[0] * tax_rates[0]) + ((taxable_income - brackets[0]) * tax_rates[1])
    elif taxable_income <= brackets[2]:
        return (brackets[0] * tax_rates[0]) + ((brackets[1] - brackets[0]) * tax_rates[1]) + ((taxable_income - brackets[1]) * tax_rates[2])
    elif taxable_income <= brackets[3]:
        return (brackets[0] * tax_rates[0]) + ((brackets[1] - brackets[0]) * tax_rates[1]) + ((brackets[2] - brackets[1]) * tax_rates[2]) + ((taxable_income - brackets[2]) * tax_rates[3])
    else:
        return (brackets[0] * tax_rates[0]) + ((brackets[1] - brackets[0]) * tax_rates[1]) + ((brackets[2] - brackets[1]) * tax_rates[2]) + ((brackets[3] - brackets[2]) * tax_rates[3]) + ((taxable_income - brackets[3]) * tax_rates[4])

#Function that calculates the Ontario surtax.
def calc_surtax(ont_tax):
    if ont_tax <= 5818:
        return 0
    elif ont_tax <= 7446:
        return (ont_tax - 5818) * 0.2
    else:
        return 325.6 + ((ont_tax - 7446) * 0.56)

#Function that calculates the federal BPA.
def calc_federal_bpa(total_income):
    if total_income <= 181440:
        return 16452
    elif total_income < 258482:
        return 16452 - ((total_income - 181440) * (1623 / 77042))
    else:
        return 14829

#Function that calculates the total calculated tax.
def calc_total_tax(fed_tax, ont_tax, surtax_amt, fed_bpa_amount):
    fed_credits = fed_bpa_amount * 0.14
    #The Ontario BPA credits.
    ont_credits = 12989 * 0.0505
    
    calculated_tax = fed_tax + ont_tax + surtax_amt - fed_credits - ont_credits
    #Makes sure that the calculated tax is not below zero.
    return max(0, calculated_tax)

# Main Execution
if __name__ == "__main__":
    income_val = get_income()
    deductions_val = get_eligible_deductions()
    
    #This line makes sure that the taxable_income_val cannot be a negative value.
    taxable_income_val = max(0, income_val - deductions_val)
    
    fed_tax_val = calc_federal_tax(taxable_income_val)
    ont_tax_val = calc_ontario_tax(taxable_income_val)
    surtax_val = calc_surtax(ont_tax_val)
    
    fed_bpa_val = calc_federal_bpa(income_val)
    
    final_tax = calc_total_tax(fed_tax_val, ont_tax_val, surtax_val, fed_bpa_val)
    
    print(f'Total Tax Owed: ${final_tax:.2f}')