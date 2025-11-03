import pytest
import pandas as pd  # <-- Import pandas for our mock
from melorec.models import predict

@pytest.fixture(autouse=True)
def mock_model_and_data(monkeypatch):
    
    # 1. Mock the 'surprise' model's prediction object
    class MockPrediction:
        def __init__(self, est):
            self.est = est
            
    # 2. Mock the 'model.predict' function
    def mock_predict(uid, iid):
        if iid == 'song_1':
            return MockPrediction(est=5.0)
        elif iid == 'song_2':
            return MockPrediction(est=1.0)
        else:
            return MockPrediction(est=3.0)

    # 3. Mock the list of all songs
    mock_all_songs = ['song_1', 'song_2', 'song_3']
    
    # 4. Mock the database 'get_song_details' function
    def mock_get_details(song_ids: list) -> pd.DataFrame:
        # Create a fake DataFrame that matches what the function expects
        data = {
            'song_1': {'title': 'Mock Song 1', 'artist': 'Mock Artist 1'},
            'song_2': {'title': 'Mock Song 2', 'artist': 'Mock Artist 2'},
            'song_3': {'title': 'Mock Song 3', 'artist': 'Mock Artist 3'},
        }
        
        results = []
        for sid in song_ids:
            if sid in data:
                results.append({
                    'song_id': sid,
                    'title': data[sid]['title'],
                    'artist': data[sid]['artist']
                })
        return pd.DataFrame(results)

    # --- Apply all the mocks ---
    if hasattr(predict, 'model'):
        monkeypatch.setattr(predict.model, 'predict', mock_predict)
    
    monkeypatch.setattr(predict, 'ALL_SONG_IDS', mock_all_songs)
    
    monkeypatch.setattr(predict, 'get_song_details', mock_get_details)


def test_generate_recommendations_format():
    """
    Tests that the function returns the correct data structure.
    """
    user_id = "test_user"
    recs = predict.generate_recommendations(user_id, n=2)

    assert isinstance(recs, list)
    assert len(recs) == 2
    assert recs[0]['title'] == 'Mock Song 1'

def test_generate_recommendations_sorting():
    """
    Tests that the recommendations are correctly sorted by score.
    Our fake model predicts song_1 (5.0) > song_3 (3.0) > song_2 (1.0)
    """
    user_id = "test_user"
    recs = predict.generate_recommendations(user_id, n=3)

    assert len(recs) == 3
    assert recs[0]['song_id'] == 'song_1'
    assert recs[1]['song_id'] == 'song_3'
    assert recs[2]['song_id'] == 'song_2'
