from gmr import data


def test_reset_drivers():
    # Modify drivers
    original_constructor = data.drivers[0]["constructor"]
    data.drivers[0]["constructor"] = "Modified"
    assert data.drivers[0]["constructor"] == "Modified"

    # Reset
    data.reset_drivers()

    # Check if reset
    assert data.drivers[0]["constructor"] == original_constructor
    # Check list length/integrity
    assert len(data.drivers) > 0
