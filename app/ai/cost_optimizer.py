def cost_optimization(expense_ratio, industry_avg_ratio):
    if expense_ratio > industry_avg_ratio:
        return (
            f"Your cost ratio is {round(expense_ratio*100,2)}% "
            f"vs industry average {round(industry_avg_ratio*100,2)}%. "
            "Consider vendor renegotiation or process optimization."
        )
    return "Cost structure is within industry norms."
