import pytest
from melorec.models import predict

# We need to mock the model and its dependencies
# This is an advanced testing technique.
# For a simpler test, we'd need a tiny, saved test model.

# Let's mock the 'predict' function inside the model object
# This is a bit complex, so a simpler 'smoke test' might be better.

@pytest.fixture(autouse=True)
def mock_model_and_data(monkeypatch):
    """
    This 'fixture' automatically runs for all tests in this file.
    It replaces the real model and data with fakes.
    """
    
    # Fake a simple prediction object from the 'surprise' library
    class MockPrediction:
        def __init__(self, est):
            self.est = est
            
    # Fake the model's 'predict' method
    def mock_predict(uid, iid):
        # Return a high score for song_1 and low for song_2
        if iid == 'song_1':
            return MockPrediction(est=5.0)
        elif iid == 'song_2':
            return MockPrediction(est=1.0)
        else:
            return MockPrediction(est=3.0)

    # Fake the list of all songs
    mock_all_songs = ['song_1', 'song_2', 'song_3']
    
    # 'monkeypatch' is a pytest tool to swap real objects with fakes
    if hasattr(predict, 'model'):
        monkeypatch.setattr(predict.model, 'predict', mock_predict)
    
    monkeypatch.setattr(predict, 'ALL_SONG_IDS', mock_all_songs)

def test_generate_recommendations_format():
    """
    Tests that the function returns the correct data structure.
    """
    user_id = "test_user"
    recs = predict.generate_recommendations(user_id, n=2)
    
    assert isinstance(recs, list)
    assert len(recs) == 2
    
    # Check the first recommendation
    first_rec = recs[0]
    assert isinstance(first_rec, dict)
    assert "song_id" in first_rec
    assert "estimated_score" in first_rec

def test_generate_recommendations_sorting():
    """
    Tests that the recommendations are correctly sorted by score.
    Our fake model predicts song_1 (5.0) > song_3 (3.0) > song_2 (1.0)
    """
    user_id = "test_user"
    recs = predict.generate_recommendations(user_id, n=3)
    
    assert recs[0]['song_id'] == 'song_1'
    assert recs[0]['estimated_score'] == 5.0
    
    assert recs[1]['song_id'] == 'song_3'
    assert recs[1]['estimated_score'] == 3.0
    
    assert recs[2]['song_id'] == 'song_2'
    assert recs[2]['estimated_score'] == 1.0