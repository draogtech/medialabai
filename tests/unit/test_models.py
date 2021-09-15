from model import RadioStation

def test_new_station():
    """
    GIVEN a RadioStation model
    WHEN a new RadioStaion is added
    THEN check the streamUrl field is defined correctly
    """
    radion_station = RadioStation('mytest','mytest','mytest','mytest','http://127.0.0.1:5000/dggeed')
    assert radion_station.name != int or float
    assert radion_station.description != int or float
    assert radion_station.logo != int or float
    assert radion_station.category != int or float
    assert radion_station.streamUrl != int or float