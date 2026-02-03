BENCHMARKS = {
    "retail": 0.65,
    "manufacturing": 0.70,
    "services": 0.60
}

def benchmark_cost(expense_ratio, industry):
    avg = BENCHMARKS.get(industry, 0.65)
    if expense_ratio > avg:
        return f"Expenses are {round((expense_ratio-avg)*100,2)}% above industry average."
    return "Expenses are within industry benchmarks."
