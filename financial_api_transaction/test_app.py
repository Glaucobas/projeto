import pytest

from datetime import datetime
from unittest.mock import MagicMock, patch
from app import app, parse_date
from models import Session
from models.table import Transactions
from app import predict_category, predict_category_nb, predict_category_cnn, vote_category
from collections import Counter


@pytest.fixture
def mock_vectorizer():
    mock = MagicMock()
    mock.transform.return_value = [[0.1, 0.2, 0.3]]
    return mock

@pytest.fixture
def mock_model():
    mock = MagicMock()
    mock.predict.return_value = ["CAT1"]
    return mock

@pytest.fixture
def mock_nb_model():
    mock = MagicMock()
    mock.predict.return_value = ["CAT2"]
    return mock

@pytest.fixture
def mock_tokenizer():
    mock = MagicMock()
    mock.texts_to_sequences.return_value = [[1, 2, 3]]
    return mock

@pytest.fixture
def mock_encoder():
    mock = MagicMock()
    mock.inverse_transform.return_value = ["CAT3"]
    return mock

@pytest.fixture
def mock_cnn_model():
    mock = MagicMock()
    mock.predict.return_value = [[0.1, 0.9, 0.0]]
    return mock
    
	# Testes para funções auxiliares
def test_parse_date():
	"""Testa a função de parse de datas"""
	assert parse_date("") == datetime.today().date()
	assert parse_date(None) == datetime.today().date()
	assert parse_date("01/01/2023") == datetime(2023, 1, 1).date()
	assert parse_date("01-01-2023") == datetime(2023, 1, 1).date()
	assert parse_date("2023-01-01") == datetime(2023, 1, 1).date()
	assert parse_date("invalid-date") == datetime.today().date()
	
def test_predict_category_success(mock_model, mock_vectorizer):
	result = predict_category("descricao teste", mock_model, mock_vectorizer)
	assert result == "CAT1"
 
def test_predict_category_nb_success(mock_nb_model):
	result = predict_category_nb("descricao teste", mock_nb_model)
	assert result == "CAT2"

def test_predict_category_cnn_success(mock_cnn_model, mock_tokenizer, mock_encoder):
	result = predict_category_cnn("descricao teste", mock_cnn_model, mock_tokenizer, mock_encoder, maxlen=10)
	assert result == "CAT3"	

def test_predict_category_handles_exception(mock_vectorizer):
    # Modelo lança exceção
    class FailingModel:
        def predict(self, X):
            raise Exception("erro")
    result = predict_category("desc", FailingModel(), mock_vectorizer)
    assert result is None
    
def test_predict_category_nb_handles_exception():
	class FailingModel:
		def predict(self, X):
			raise Exception("erro")
	result = predict_category_nb("desc", FailingModel())
	assert result is None
	
def test_predict_category_cnn_handles_exception(mock_tokenizer, mock_encoder):
	class FailingModel:
		def predict(self, X):
			raise Exception("erro")
	result = predict_category_cnn("desc", FailingModel(), mock_tokenizer, mock_encoder)
	assert result is None
 
def test_vote_category_majority(monkeypatch):
	monkeypatch.setattr("app.predict_category", lambda desc, m, v: "A")
	monkeypatch.setattr("app.predict_category_nb", lambda desc, m=None: "A")
	monkeypatch.setattr("app.predict_category_cnn", lambda desc, m, t, e, maxlen=100: "B")
	monkeypatch.setattr("app.modelo1", None)
	monkeypatch.setattr("app.modelo2", None)
	monkeypatch.setattr("app.modelo3", None)
	monkeypatch.setattr("app.modelo4", None)
	monkeypatch.setattr("app.vectorizer1", None)
	monkeypatch.setattr("app.vectorizer2", None)
	monkeypatch.setattr("app.vectorizer3", None)
	monkeypatch.setattr("app.vectorizer4", None)
	monkeypatch.setattr("app.encoder", None)
	result = vote_category("qualquer coisa")
	assert result == "A"
 
def test_vote_category_no_majority(monkeypatch):
	monkeypatch.setattr("app.predict_category", lambda desc, m, v: "A")
	monkeypatch.setattr("app.predict_category_nb", lambda desc, m=None: "B")
	monkeypatch.setattr("app.predict_category_cnn", lambda desc, m, t, e, maxlen=100: "C")
	monkeypatch.setattr("app.modelo1", None)
	monkeypatch.setattr("app.modelo2", None)
	monkeypatch.setattr("app.modelo3", None)
	monkeypatch.setattr("app.modelo4", None)
	monkeypatch.setattr("app.vectorizer1", None)
	monkeypatch.setattr("app.vectorizer2", None)
	monkeypatch.setattr("app.vectorizer3", None)
	monkeypatch.setattr("app.vectorizer4", None)
	monkeypatch.setattr("app.encoder", None)
	original_predict_category = predict_category
	def fake_predict_category(desc, m, v): return "A"
	def fake_predict_category_nb(desc, m=None): return "B"
	def fake_predict_category_cnn(desc, m, t, e, maxlen=100): return "C"
	monkeypatch.setattr("app.predict_category", fake_predict_category)
	monkeypatch.setattr("app.predict_category_nb", fake_predict_category_nb)
	monkeypatch.setattr("app.predict_category_cnn", fake_predict_category_cnn)
	monkeypatch.setattr("collections.Counter", lambda x: Counter(["A", "B", "C", "D"]))
	result = vote_category("qualquer coisa")
	assert result == "CND"