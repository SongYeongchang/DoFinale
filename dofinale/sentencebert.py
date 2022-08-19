import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import random

model = SentenceTransformer('jhgan/ko-sroberta-multitask')

df1 = pd.read_csv('./dofinale/static/embeding.csv',header=None)
df = pd.read_csv('./dofinale/static/wellness_dataset_.csv')

#챗봇 함수 입력받은 텍스트와 embeding 유사도 체크후 원본 챗봇에 cos컬럼 만든후 상위 정렬
def chatbot_text(text):
    em_result = model.encode(text)
    co_result = []
    for temp in range(len(df1)):
        data = df1.iloc[temp]
        co_result.append( cosine_similarity([em_result],[data])[0][0] )
    df['cos'] = co_result
    df_result = df.sort_values('cos',ascending=False)
    # r = random.randint(0,5) # 유사도 높은 순으로 5개 중 랜덤
    r=0 # 가장 유사도 높은 걸로
    return df_result.iloc[r]