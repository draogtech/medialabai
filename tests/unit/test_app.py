# from tests.conftest import new_station


def test_new_station_with_fixture(new_station):
    """
    GIVEN a RadioStation model
    WHEN a new RadioStaion is added
    THEN check the required fields are defined correctly
    """
    assert new_station.name != int or float
    assert new_station.description != int or float
    # assert radion_station.logo != int or float
    assert new_station.category != int or float
    assert new_station.streamUrl == 'http://127.0.0.1:5000/dggeed'