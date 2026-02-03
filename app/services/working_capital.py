# Working Capital Management and Optimization

def analyze_working_capital(revenue, receivables_days, payables_days, inventory_days):
    """Analyze working capital efficiency and optimization opportunities"""
    
    # Calculate working capital metrics
    daily_revenue = revenue / 365
    
    # Days Sales Outstanding (DSO)
    dso = receivables_days
    receivables_amount = daily_revenue * dso
    
    # Days Payable Outstanding (DPO)
    dpo = payables_days
    
    # Days Inventory Outstanding (DIO)
    dio = inventory_days
    
    # Cash Conversion Cycle (CCC) = DSO + DIO - DPO
    cash_conversion_cycle = dso + dio - dpo
    
    # Working capital requirement (approximate)
    daily_cost = (revenue * 0.65) / 365  # Assuming 65% cost of goods
    wc_requirement = (dso + dio - dpo) * daily_cost
    
    # Generate recommendations
    recommendations = []
    
    if dso > 60:
        recommendations.append({
            "category": "Receivables",
            "issue": f"High DSO ({dso} days) - receivables taking too long",
            "action": "Implement early payment discounts, stricter credit terms",
            "potential_savings": round(daily_revenue * min(dso - 30, 20), 2)
        })
    
    if dio > 45:
        recommendations.append({
            "category": "Inventory",
            "issue": f"High inventory levels ({dio} days) - slow-moving stock",
            "action": "Optimize inventory levels, implement just-in-time",
            "potential_savings": round(daily_cost * min(dio - 30, 15), 2)
        })
    
    if dpo < 30:
        recommendations.append({
            "category": "Payables",
            "issue": f"Low DPO ({dpo} days) - paying suppliers too quickly",
            "action": "Negotiate longer payment terms with suppliers",
            "potential_savings": round(daily_cost * min(40 - dpo, 15), 2)
        })
    
    return {
        "dso": dso,  # Days Sales Outstanding
        "dio": dio,  # Days Inventory Outstanding
        "dpo": dpo,  # Days Payable Outstanding
        "cash_conversion_cycle": round(cash_conversion_cycle, 1),
        "working_capital_requirement": round(wc_requirement, 2),
        "recommendations": recommendations,
        "total_potential_savings": round(sum([r.get("potential_savings", 0) for r in recommendations]), 2)
    }

def optimize_receivables(total_receivables, current_dso, target_dso=45):
    """Optimize receivables collection"""
    daily_sales = total_receivables / current_dso
    
    # Calculate cash release from DSO improvement
    dso_reduction = current_dso - target_dso
    cash_freed = daily_sales * dso_reduction
    
    strategies = [
        {
            "strategy": "Early Payment Discount",
            "description": "Offer 2% discount for payment within 10 days",
            "estimated_impact": round(cash_freed * 0.20, 2),
            "implementation_time": "1-2 weeks"
        },
        {
            "strategy": "Automated Reminders",
            "description": "Send automated payment reminders at 15, 20, 25 days",
            "estimated_impact": round(cash_freed * 0.15, 2),
            "implementation_time": "1 week"
        },
        {
            "strategy": "Online Payment Portal",
            "description": "Enable quick online payment options (UPI, cards)",
            "estimated_impact": round(cash_freed * 0.10, 2),
            "implementation_time": "2-3 weeks"
        },
        {
            "strategy": "Credit Policy Review",
            "description": "Tighten credit terms, implement credit scoring",
            "estimated_impact": round(cash_freed * 0.25, 2),
            "implementation_time": "3-4 weeks"
        }
    ]
    
    return {
        "current_dso": current_dso,
        "target_dso": target_dso,
        "total_receivables": total_receivables,
        "cash_freed_potential": round(cash_freed, 2),
        "strategies": strategies,
        "total_impact": round(sum([s.get("estimated_impact", 0) for s in strategies]), 2)
    }

def optimize_inventory(annual_cogs, current_dio, target_dio=30):
    """Optimize inventory levels"""
    daily_cogs = annual_cogs / 365
    
    # Calculate cash release from inventory optimization
    dio_reduction = current_dio - target_dio
    cash_freed = daily_cogs * dio_reduction
    
    strategies = [
        {
            "strategy": "ABC Analysis",
            "description": "Classify inventory items by value and optimize stock levels",
            "estimated_cash_release": round(cash_freed * 0.30, 2)
        },
        {
            "strategy": "Just-In-Time (JIT)",
            "description": "Reduce safety stock, increase order frequency",
            "estimated_cash_release": round(cash_freed * 0.25, 2)
        },
        {
            "strategy": "Demand Forecasting",
            "description": "Implement better forecasting to reduce overstock",
            "estimated_cash_release": round(cash_freed * 0.20, 2)
        },
        {
            "strategy": "Supplier Coordination",
            "description": "Work with suppliers on consignment basis",
            "estimated_cash_release": round(cash_freed * 0.25, 2)
        }
    ]
    
    return {
        "current_dio": current_dio,
        "target_dio": target_dio,
        "annual_cogs": annual_cogs,
        "cash_freed_potential": round(cash_freed, 2),
        "strategies": strategies
    }

def optimize_payables(annual_cogs, current_dpo, target_dpo=45):
    """Optimize payables period"""
    daily_cogs = annual_cogs / 365
    
    # Calculate additional cash availability
    dpo_increase = target_dpo - current_dpo
    additional_cash = daily_cogs * dpo_increase
    
    strategies = [
        {
            "strategy": "Supplier Negotiation",
            "description": "Negotiate longer payment terms (Net 45-60)",
            "potential_impact": round(additional_cash * 0.40, 2)
        },
        {
            "strategy": "Payment Consolidation",
            "description": "Consolidate suppliers to gain negotiating power",
            "potential_impact": round(additional_cash * 0.30, 2)
        },
        {
            "strategy": "Supply Chain Financing",
            "description": "Use supplier financing options when available",
            "potential_impact": round(additional_cash * 0.30, 2)
        }
    ]
    
    return {
        "current_dpo": current_dpo,
        "target_dpo": target_dpo,
        "annual_cogs": annual_cogs,
        "additional_cash_available": round(additional_cash, 2),
        "strategies": strategies
    }
