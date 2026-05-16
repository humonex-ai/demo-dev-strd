import pytest

from sip_calculator import sip_calculator


def test_known_value_case():
    # 5000/month, 12% annual, 10 years -> ~1,161,695.40 (industry-standard SIP formula)
    result = sip_calculator(5000, 12, 10)
    assert result["total_invested"] == 600000.00
    assert result["future_value"] == pytest.approx(1161695.40, abs=1.0)
    assert result["total_gains"] == pytest.approx(
        result["future_value"] - result["total_invested"], abs=0.01
    )


def test_zero_rate():
    result = sip_calculator(1000, 0, 5)
    assert result["future_value"] == 60000.00
    assert result["total_invested"] == 60000.00
    assert result["total_gains"] == 0.00


def test_zero_years():
    result = sip_calculator(1000, 12, 0)
    assert result["future_value"] == 0.00
    assert result["total_invested"] == 0.00
    assert result["total_gains"] == 0.00


@pytest.mark.parametrize(
    "monthly,rate,years",
    [(-100, 12, 5), (1000, -5, 5), (1000, 12, -1)],
)
def test_negative_inputs_raise(monthly, rate, years):
    with pytest.raises(ValueError):
        sip_calculator(monthly, rate, years)
