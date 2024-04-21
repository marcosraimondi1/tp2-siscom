from server import process_values, get_data, filter_by_country, get_values_and_dates

def test_process_values():

    values = [1.5, 2.75, 3.9]
    expected = [3, 4, 5]

    results = process_values(values)

    assert results[0] == expected[0]
    assert results[1] == expected[1]
    assert results[2] == expected[2]

def test_get_data():

    data = get_data()

    assert len(data) > 0  # check if data is empty

    total = data[0]["total"]

    assert total > 0

def test_filter_by_country():

    data = [
        {"country":{"value":"argentina"}}, 
        {"country":{"value":"Argentina"}}, 
        {"country":{"value":"austria"}}
    ]

    filtered = filter_by_country(data, "argentina")
    assert len(filtered) == 2
    assert filtered[0]["country"]["value"] == "argentina"

    filtered = filter_by_country(data, "austria")
    assert len(filtered) == 1
    assert filtered[0]["country"]["value"] == "austria"

    filtered = filter_by_country(data, "none")
    assert len(filtered) == 0

def test_get_values():
    data = [
        {"value": 3, "date": "2019"},
        {"value": None, "date": "2020"},
        {"value": 300, "date": "2021"},
    ]

    values, dates = get_values_and_dates(data)

    assert len(dates) == len(values)
    assert len(values) == 2
    assert values[0] == 3
    assert values[1] == 300
    assert dates[0] == "2019"
    assert dates[1] == "2021"

