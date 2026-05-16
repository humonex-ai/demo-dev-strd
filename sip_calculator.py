def sip_calculator(monthly_investment: float, annual_rate_pct: float, years: int) -> dict:
    if monthly_investment < 0:
        raise ValueError("monthly_investment must be non-negative")
    if annual_rate_pct < 0:
        raise ValueError("annual_rate_pct must be non-negative")
    if years < 0:
        raise ValueError("years must be non-negative")

    n = years * 12
    r = (annual_rate_pct / 100.0) / 12.0

    if r == 0:
        future_value = monthly_investment * n
    else:
        future_value = monthly_investment * (((1 + r) ** n - 1) / r) * (1 + r)

    total_invested = monthly_investment * n
    total_gains = future_value - total_invested

    return {
        "future_value": round(future_value, 2),
        "total_invested": round(total_invested, 2),
        "total_gains": round(total_gains, 2),
    }
