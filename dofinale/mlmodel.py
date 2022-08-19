import pickle
import pandas as pd

def ml_survey(symptom, surv_res):
    with open('./dofinale/static/aimodel/ml/'+symptom+'_model/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('./dofinale/static/aimodel/ml/'+symptom+'_model/transformer_scale.pkl', 'rb') as f:
        transformer_scale = pickle.load(f)
    with open('./dofinale/static/aimodel/ml/'+symptom+'_model/transformer_encoder.pkl', 'rb') as f:
        transformer_encoder = pickle.load(f)

    X = pd.DataFrame(surv_res)

    X = transformer_encoder.transform(X)
    X = transformer_scale.transform(X)

    result = model.predict(X)
    result_proba = model.predict_proba(X)

    return result, result_proba