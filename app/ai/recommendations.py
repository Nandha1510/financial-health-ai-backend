def build_recommendations(health_score, risks, credit_metrics, benchmark_msg):
    recs = []

    if health_score < 60:
        recs.append("Improve liquidity and reduce discretionary spending.")

    # Be defensive: `credit_metrics` may be missing DSCR in some payloads
    dscr = None
    if isinstance(credit_metrics, dict):
        dscr = credit_metrics.get("DSCR")

    if dscr is not None and dscr < 1.2:
        recs.append("Restructure debt to improve DSCR.")

    if "Receivable delay" in " ".join(risks):
        recs.append("Strengthen receivables collection policy.")

    recs.append(benchmark_msg)
    return recs
