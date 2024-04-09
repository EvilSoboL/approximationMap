import pytest

from control.database import DatabaseHandler

db = DatabaseHandler()


@pytest.mark.parametrize("input_value, expected", [
    ('diesel', 1),
    ('crude_oil', 2),
    ('heavy_oil', 3),
    ('kerosene', 4),
    ('waste_oil', 5),
])
def test_get_fuel_id_from_name(input_value, expected):
    result = db.get_fuel_id_from_name(input_value)
    assert result == expected
