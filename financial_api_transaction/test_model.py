import joblib
import numpy as np
import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from keras.layers import Dense
from collections import Counter


def load_models():
    """Carrega o modelo e o vectorizer salvos"""
    try:
        # Carrega o modelo de regressão logística
        modelo1 = joblib.load('./models/logistic_regression_model.pkl')
        print("✅ Modelo de regressão logística carregado com sucesso")
        
        # Carrega o vectorizer (logistic_regression_vectorizer)
        vectorizer1 = joblib.load('./models/logistic_regression_vectorizer.pkl')
        print("✅ Vectorizer logistic_regression_vectorizer carregado com sucesso")
        
        # Carrega o modelo Randon Forest
        modelo2 = joblib.load('./models/random_forest_model.pkl')
        print("✅ Modelo Randon Fores carregado com sucesso")
        
        # Carrega o vectorizer (TF-IDF)
        vectorizer2 = joblib.load('./models/random_forest_vectorizer.pkl')
        print("✅ Vectorizer random_forest_vectorizer carregado com sucesso")
        
        # Carrega o modelo Naive Bayes (opcional)
        modelo3 = joblib.load('./models/naive_bayes_model.pkl')
        print("✅ Modelo Naive Bayes carregado com sucesso")
                
        # Carrega o vectorizer (TF-IDF)
        vectorizer3 = joblib.load('./models/naive_bayes_vectorizer.pkl')
        print("✅ Vectorizer count_vector carregado com sucesso")
        
        # Carrega o modelo CNN (opcional)    
        modelo4 = load_model('./models/cnn_model.h5')
        modelo4.compile(
            optimizer='adam',
            loss='binary_crossentropy',  # ou 'categorical_crossentropy', dependendo do seu caso
            metrics=['accuracy']
        )
        print("✅ Modelo  CNN carregado com sucesso")
        
        with open('./models/cnn_tokenizer.pkl', 'rb') as f:
            vectorizer4 = pickle.load(f)
        print("✅ tokenizer CNN carregado com sucesso")
        
        with open('./models/cnn_label_encoder.pkl', 'rb') as f:
            encoder = pickle.load(f)
        print("✅ encoder CNN carregado com sucesso")
           
        return modelo1, modelo2, modelo3, modelo4, vectorizer1, vectorizer2, vectorizer3, vectorizer4, encoder
    
    except Exception as e:
        print(f"❌ Erro ao carregar modelos: {str(e)}")
        return None, None, None, None, None, None, None, None, None

def predict_category(description, modelo, vectorizer):
    """Faz a predição da categoria para uma descrição"""
    try:
        X = vectorizer.transform([description])
        print(type(modelo))
        predicao = modelo.predict(X)
        return predicao[0]
    
    except Exception as e:
        print(f"❌ Erro ao fazer predição: {str(e)}")
        return None

def predict_category_nb(description, modelo):
    """Faz a predição da categoria para uma descrição usando Naive Bayes"""
    try:
        if not isinstance(description, str):
            description = str(description)
        print(type(modelo))
        predicao = modelo.predict([description])
        return predicao[0]
    except Exception as e:
        print(f"❌ Erro ao fazer predição com Naive Bayes: {str(e)}")
        return None
    
def predict_category_cnn(description, modelo, tokenizer, encoder, maxlen=100):
    try:
        seq = tokenizer.texts_to_sequences([description])
        padded = pad_sequences(seq, maxlen=maxlen)
        pred = modelo.predict(padded)
        pred_index = np.argmax(pred)
        pred_label = encoder.inverse_transform([pred_index])[0]
        return pred_label
    except Exception as e:
        print(f"❌ Erro na predição com CNN: {str(e)}")
        return None
    
def test_models(modelo1, modelo2, modelo3, modelo4, vectorizer1, vectorizer2, vectorizer3, vectorizer4, encoder):
    """Testa os modelos com exemplos de descrições"""
    # Exemplos de descrições para testar
    test_descriptions = [
        "Compra no supermercado",
        "Pagamento de conta de luz",
        "Transferência recebida",
        "Restaurante japonês",
        "Assinatura Netflix",
        "Combustível posto Shell",
        "Consulta médica",
        "Passagem aérea para SP"
    ]
    
    print("\n🔍 Testando modelos com descrições de exemplo:")
    print("-" * 60)
    
    for desc in test_descriptions:
        # Predição com modelo1 (Regressão Logística)
        cat1 = predict_category(desc, modelo1, vectorizer1)
        
        # Predição com modelo2 (Randon Forest)
        cat2 = predict_category(desc, modelo2, vectorizer2)
        
        # Predição com modelo3 (Naive Bayes)
        cat3 = predict_category_nb(desc, modelo3)
        
        # Predição com modelo4 (CNN)
        cat4 = predict_category_cnn(desc, modelo4, vectorizer4, encoder)
        
        print(f"Descrição: {desc}")
        print(f"  Regressão Logística: Categoria {cat1}")
        print(f"  Randon Forest: Categoria {cat2}")
        print(f"  Naive Bayes: Categoria {cat3}")
        print(f"  CNN: Categoria {cat4}")
        print("-" * 60)

def vote_category(description, modelo1, modelo2, modelo3, modelo4, vectorizer1, vectorizer2, vectorizer3, vectorizer4, encoder):
    """Faz a predição da categoria com votação entre três modelos"""
    try:

        # Obtém as predições dos três modelos
        pred1 = predict_category(description, modelo1, vectorizer1)
        pred2 = predict_category(description, modelo2, vectorizer2)
        pred3 = predict_category_nb(description, modelo3)
        pred4 = predict_category_cnn(description, modelo4, vectorizer4, encoder)

        # Conta quantas vezes cada categoria apareceu
        vote = Counter([pred1, pred2, pred3, pred4])
        category_more_comum, contagem = vote.most_common(1)[0]

        # Verifica se ao menos dois modelos concordaram
        if contagem >= 2:
            return category_more_comum
        else:
            return "CND" 
    except Exception as e:
        return "CND"

def main():
    print("\n🔧 Iniciando teste dos modelos de predição")
    
    # Carrega os modelos
    modelo1, modelo2, modelo3,  modelo4, vectorizer1, vectorizer2, vectorizer3, vectorizer4, encoder = load_models()
    
    if modelo1 is None or vectorizer1 is None:
        print("❌ Não foi possível carregar os modelos. Verifique os arquivos.")
        return
    
    # Testa os modelos
    test_models(modelo1, modelo2, modelo3, modelo4, vectorizer1, vectorizer2, vectorizer3, vectorizer4, encoder)
    
    # Teste interativo
    print("\n🔮 Modo interativo (digite 'sair' para encerrar)")
    while True:
        descricao = input("\nDigite uma descrição de transação: ").strip()
        if descricao.lower() == 'sair':
            break
           
        cat1 = predict_category(descricao, modelo1, vectorizer1)
        cat2 = predict_category(descricao, modelo2, vectorizer1)
        cat3 = predict_category_nb(descricao, modelo3)
        cat4 = predict_category_cnn(descricao, modelo4, vectorizer4, encoder)
        #cat5 = vote_category(descricao, modelo1, modelo2, modelo3, modelo4, vectorizer1, vectorizer2, vectorizer3, vectorizer4, encoder)
        
        print(f"\nResultados para: '{descricao}'")
        print(f"  Regressão Logística: Categoria {cat1}")
        print(f"  Naive Bayes: Categoria {cat2}")
        print(f"  Randon Forest: Categoria {cat3}")
        print(f"  CNN: Categoria {cat4}")
        #print(f"  Resultado da votação: {cat5}")
        
    print("\n✅ Teste concluído")

if __name__ == "__main__":
    main()