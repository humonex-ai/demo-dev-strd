def loan_calculator(principal: float, annual_rate_pct: float, tenure_months: int) -> dict:
    if principal < 0:
        raise ValueError("principal must be non-negative")
    if annual_rate_pct < 0:
        raise ValueError("annual_rate_pct must be non-negative")
    if tenure_months <= 0:
        raise ValueError("tenure_months must be positive")

    r = (annual_rate_pct / 100.0) / 12.0
    n = tenure_months

    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

    total_payment = emi * n
    total_interest = total_payment - principal

    return {
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
    }
