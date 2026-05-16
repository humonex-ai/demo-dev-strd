import pytest

from loan_calculator import loan_calculator


def test_known_value_case():
    # 1,00,000 @ 10% annual / 12 months -> EMI ~ 8791.59
    result = loan_calculator(100000, 10, 12)
    assert result["emi"] == pytest.approx(8791.59, abs=0.01)
    assert result["total_payment"] == pytest.approx(8791.59 * 12, abs=0.5)
    assert result["total_interest"] == pytest.approx(
        result["total_payment"] - 100000, abs=0.01
    )


def test_zero_rate():
    result = loan_calculator(120000, 0, 12)
    assert result["emi"] == 10000.00
    assert result["total_payment"] == 120000.00
    assert result["total_interest"] == 0.00


def test_zero_tenure_rejected():
    with pytest.raises(ValueError):
        loan_calculator(100000, 10, 0)


@pytest.mark.parametrize(
    "principal,rate,months",
    [(-1000, 10, 12), (100000, -1, 12), (100000, 10, -3)],
)
def test_negative_inputs_raise(principal, rate, months):
    with pytest.raises(ValueError):
        loan_calculator(principal, rate, months)
