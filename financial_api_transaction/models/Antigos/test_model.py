import pytest
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer

@pytest.fixture(scope="module")
def loaded_models():
    try:
        # Carrega o modelo de regressão logística
        modelo1 = joblib.load('.\\models\\logistic_regression_model.pkl')
        modelo2 = joblib.load('.\\models\\naive_bayes_model.pkl')
        modelo3 = joblib.load('.\\models\\naive_bayes_model.pkl')
        vectorizer = joblib.load('.\\models\\tfidf_vectorizer.pkl')

        return modelo1, modelo2, modelo3, vectorizer
    except Exception as e:
        pytest.fail(f"Falha ao carregar modelos: {str(e)}")

def test_model_loading(loaded_models):
    """Testa o carregamento dos modelos"""
    modelo1, modelo2, modelo3, vectorize = loaded_models

    assert modelo1 is not None, "Modelo de regressão logística não carregado"
    assert modelo2 is not None, "Modelo Naive Bayes não carregado"
    assert modelo3 is not None, "Modelo Naive Bayes não carregado"
    assert vectorize is not None, "Vectorizer não carregado"
    assert hasattr(modelo1, 'predict'), "Modelo1 não tem método predict"
    assert hasattr(modelo2, 'predict'), "Modelo2 não tem método predict"
    assert hasattr(modelo3, 'predict'), "Modelo2 não tem método predict"

@pytest.mark.parametrize("description, expected_category", [
    ("Compra no supermercado", "MER"),
    ("Pagamento DAE", "AGU"),
    ("Restaurante japones", "BAR"), 
    ("Posto Shell Avenida", "ABS"),
    ("Posto BR Central", "ABS"),
    ("Posto Ipiranga Norte", "ABS"),
    ("Posto EcoFuel KM 37", "ABS"),
    ("rshop-posto teixe", "ABS"),
    ("bki sabesp", "AGU"), 
    ("int dae american", "AGU"), 
    ("int sabesp","AGU"), 
    ("cof aplicacao cdb", "APL"), 
    ("dinheiro guardado com resgate planejado", "APL"), 
    ("Netflix Streaming de filmes", "ASS"), 
    ("Spotify Música por assinatura","ASS"), 
    ("Dropbox Armazenamento em nuvem","ASS"), 
    ("google duolingo","ASS"),       
    ("Restaurante Saboroso","BAR"), 
    ("Café Colonial","BAR"), 
    ("adega de fartura","BAR"), 
    ("compra no débito - coxinha de ouro","BAR"), 
    ("Faxina pesada – Limpeza geral","CAS"), 
    ("Montagem de móveis","CAS"), 
    ("Chaveiro residencial","CAS"), 
    ("bandini lar construcao", "CAS"), 
    ("crédito de parcelamento", "CRD"), 
    ("crédito de rotativo", "CRD"), 
    ("Fatura Banco Inter", "CRD"), 
    ("dentelie","DEN"), 
    ("dentista","DEN"), 
    ("Curso técnico – Senai","EDU"), 
    ("Plataforma de estudos – Descomplica","EDU"), 
    ("farma centro fartura","FAR"), 
    ("rshop-drogafar",  "FAR"),    
    ("rshop-farm homeop","FAR"), 
    ("iof","IMP"), 
    ("cofins","IMP"), 
    ("ipva","IMP"), 
    ("juros atraso lim conta","JUR"), 
    ("lis/juros","JUR"), 
    ("hotel imperial", "LAZ"), 
    ("rshop-new bowling","LAZ"), 
    ("Excursão para parque aquático","LAZ"), 
    ("americana informat","LOJ"), 
    ("compra no débito - cristal produtos natur","LOJ"), 
    ("compra no débito - dang peng comercio","LOJ"), 
    ("cpfl paulista", "LUZ"), 
    ("int cpfl", "LUZ"), 
    ("int elektro", "LUZ"), 
    ("Troca de óleo", "MAN"), 
    ("mecanica possobom", "MAN"), 
    ("portal de poa auto pos",  "MAN"), 
    ("Supermercado Extra","MER"), 
    ("Carrefour Bairro","MER"), 
    ("cobasi sb oeste tivoli","MER"), 
    ("deb autor sem parar","PED"), 
    ("estacionamento","PED"), 
    ("Rendimento freelancer","SAL"), 
    ("Folha de pagamento – Departamento pessoal","SAL"), 
    ("Consulta médica – Clínica popular","SAU"), 
    ("Exame de sangue – Laboratório XYZ","SAU"), 
    ("itau seguros", "SEG" ), 
    ("seguro residencial","SEG" ), 
    ("Tarifa bancária – DOC","TAR"), 
    ("Anuidade cartão Visa","TAR"), 
    ("Consulta veterinária – PetVita","PET"), 
    ("Banho e tosa – PetShop Alegria","PET"), 
    ("rshop-manoel rodr","TRP"), 
    ("uber pending","TRP")
])

def test_predictions(loaded_models, description, expected_category):
    """Testa diferentes descrições."""
    modelo1, modelo2, modelo3, vectorize = loaded_models

    X = vectorize.transform([description])

    pred1 = modelo1.predict(X)
    assert pred1[0] == expected_category, \
        f"Modelo1 previu {pred1[0]} para '{description}', esperado {expected_category}"
    
    pred2 = modelo2.predict(X)
    assert pred2[0] == expected_category, \
        f"Modelo2 previu {pred2[0]} para '{description}', esperado {expected_category}"
        
    pred3 = modelo3.predict(X)
    assert pred3[0] == expected_category, \
        f"Modelo3 previu {pred3[0]} para '{description}', esperado {expected_category}"  
          
@pytest.mark.parametrize("modelo_nome", ["modelo1", "modelo2", "modelo3"])
@pytest.mark.parametrize("entrada", ["", "123 456 789"])
def test_input_handling(loaded_models, modelo_nome, entrada):
    """Testa os modelos com entradas vazias e numéricas, garantindo que o tipo de saída seja inteiro."""
    modelo1, modelo2, modelo3, vectorize = loaded_models
    modelos = {
        "modelo1": modelo1,
        "modelo2": modelo2,
        "modelo3": modelo3
    }

    modelo = modelos[modelo_nome]
    pred = modelo.predict(vectorize.transform([entrada]))
    assert isinstance(pred[0], (int, np.integer)), f"A previsão do {modelo_nome} para a entrada '{entrada}' deve ser do tipo inteiro"

def test_model_consistency(loaded_models):
    """Testa se o modelo retorna resultados consistentes"""
    modelo1, modelo2, modelo3, vectorize = loaded_models

    desc = "Compra no mercado"

    pred1 = modelo1.predict(vectorize.transform([desc]))
    pred2 = modelo1.predict(vectorize.transform([desc]))
    assert pred1[0] == pred2[0], "Modelo1 retornou resultados diferentes para a mesma entrada"

    pred1 = modelo2.predict(vectorize.transform([desc]))
    pred2 = modelo2.predict(vectorize.transform([desc]))
    assert pred1[0] == pred2[0], "Modelo2 retornou resultados diferentes para a mesma entrada"
    
    pred1 = modelo3.predict(vectorize.transform([desc]))
    pred2 = modelo3.predict(vectorize.transform([desc]))
    assert pred1[0] == pred2[0], "Modelo3 retornou resultados diferentes para a mesma entrada"