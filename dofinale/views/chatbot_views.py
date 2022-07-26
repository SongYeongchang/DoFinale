from flask import Blueprint, render_template, url_for, request, session, jsonify, g
import json
from geopy.geocoders import Nominatim # 가까운 병원 위경도 값으로 찾기
from haversine import haversine
import os.path

from dofinale.models import Members

bp = Blueprint('chatbot', __name__, url_prefix='/chatbot_test')

current_user_table={} # 사용자 아이디 : df 세션 연결하는 테이블
tmp_list=[] # 큐 자료구조로 선입선출을 위한 변수

# session_user = Members.query.filter_by(id=int(session.get('user_id'))).first()

def get_lat_and_log(address):
    '''
    주소 입력 시 위경도 값 출력하는 함수
    https://wonhwa.tistory.com/29
    :param address: 주소값
    :return: 위도값, 경도값
    '''
    try:
        geo_local = Nominatim(user_agent='South Korea')

        while(not geo_local.geocode(address)):
            # 마지막 어절 하나씩 제거
            address = address[:-len(address.split(' ')[-1])-1]
        geo=geo_local.geocode(address)

        return geo.latitude, geo.longitude # 위도, 경도 순으로 반환
    except:
        print(address,'에러!!!')
        return (0.0,0.0)

@bp.route('/')
def index():
    if session.get('user_id'):
        global current_user_table, tmp_list
        tmp_list.append(session.get('user_id'))
        if tmp_list: # 리스트에 원소 존재 할때
            print('tmp_list > ', tmp_list)
            for i, item in enumerate(tmp_list):
                print('current_user_table(추가 전) >',current_user_table)
                current_user_table[item] = 'accessed user'  # current_user_table에 추가
                print('current_user_table(추가 후) >', current_user_table)
        # print('current_user_table(추가 전) >',current_user_table)
        # current_user_table[session.get('user_id')] = 'accessed user'  # current_user_table에 추가
        # print('current_user_table(추가 후) >', current_user_table)
        return render_template('chatbot_test/chatbot_test.html')
    else:
        return "로그인 확인 <br> <a href='https://3da1-112-221-224-124.jp.ngrok.io/auth/login/'>로그인 하러가기</a>"



@bp.route('/agent1/',methods=('POST','GET'))
def chatbot():
    print('chatbot accessed')
    if request.method == "POST":
        global current_user_table, tmp_list

        # 사용자가 챗봇에 입력 시 데이터 받기
        req = request.get_json(force=True)


        # df 세션값 저장
        print("df 세션값 > ",req['session'].split('/')[4])

        df_session=req['session'].split('/')[4]


        if tmp_list:
            # value로 'accessed user' 값을 df 세션값으로 변경
            # while (len([k for k, v in current_user_table.items() if v == 'accessed user']) > 1):
            #     print("current_user_table 대기('accessed user') 1개 이상  > ",current_user_table)
            if len([k for k, v in current_user_table.items() if v == 'accessed user']) > 0: # value 값으로 'accessed user' 존재할 경우
                print('변경전 > ',current_user_table)
                # current_user_table[[k for k, v in current_user_table.items() if v == 'accessed user'][0]] = df_session # 접근한 사용자 key에 df 세션을 value로 입력
                current_user_table[tmp_list[0]] = df_session # 접근한 사용자 key에 df 세션을 value로 입력
                print('변경후 > ',current_user_table)
                del tmp_list[0]

        if df_session:
            # df 세션값 사용자 id 저장
            print("[k for k, v in current_user_table.items() if v == df_session] > ",[k for k, v in current_user_table.items() if v == df_session])
            current_user_id=[k for k, v in current_user_table.items() if v == df_session][0] # 현재 df세션 value 값으로 사용자 id인 key값
            print('current_user_id > ',current_user_id)

    # 각 사용자별 다이얼로그 플로우 세션 값 저장 ----------------------------------------------------------------------------------

    if (req['queryResult']['intent']['displayName'] == "Default Welcome Intent"):
        print("접속 인텐트: Default Welcome Intent")
        return jsonify(fulfillment_messages=[
            {
                "payload":{
                  "richContent": [
                    [
                      {
                        "rawUrl": "https://t1.daumcdn.net/cfile/tistory/99559F435DEEDFCB1D",
                        "type": "image",
                        "accessibilityText": "두피 진단 예측 welcome"
                      },
                      {
                        "title": "두피 진단 예측 서비스",
                        "type": "info",
                        "subtitle": "당신의 두피를 최고의 AI 기술을 이용해 진단해드립니다."
                      },
                      {
                        "options": [
                          {
                            "text": "진단결과 확인하기",
                            "image": {
                              "src": {
                                "rawUrl": "https://github.com/SongYeongchang/DoFinale/blob/master/dofinale/static/images/icons/chatbot_icon.png?raw=true"
                              }
                            }
                          }
                        ],
                        "type": "chips"
                      }
                    ]
                  ]
                }
            }
        ])

    if (req['queryResult']['intent']['displayName'] == "Default Fallback Intent"):
        print("접속 인텐트: Default Fallback Intent")
        return jsonify(fulfillment_messages=[
            {
                "payload":{
                  "richContent": [
                    [
                      {
                        "rawUrl": "https://www.sciencetimes.co.kr/wp-content/uploads/2020/10/GettyImages-1222023758-scaled.jpg",
                        "type": "image",
                        "accessibilityText": "두피 진단 예측"
                      },
                      {
                        "subtitle": "예측된 두피 진단 결과로 다음과 같은 서비스를 이용해보세요",
                        "title": "당신의 두피 상태는 '"+ Members.query.get(current_user_id).scalp_type +"'입니다.",
                        "type": "info"
                      },
                      {
                        "type": "chips",
                        "options": [
                          {
                            "image": {
                              "src": {
                                "rawUrl": "https://github.com/SongYeongchang/DoFinale/blob/master/dofinale/static/images/icons/chatbot_icon.png?raw=true"
                              }
                            },
                            "text": "제품 추천 무료로 받기"
                          },
                          {
                            "image": {
                              "src": {
                                "rawUrl": "https://github.com/SongYeongchang/DoFinale/blob/master/dofinale/static/images/icons/chatbot_icon.png?raw=true"
                              }
                            },
                            "text": "가까운 병원 무료로 찾기"
                          },
                          {
                            "link": "https://3323-112-221-224-124.jp.ngrok.io/",
                            "text": "두피 진단 다시 해보기",
                            "image": {
                              "src": {
                                "rawUrl": "https://github.com/SongYeongchang/DoFinale/blob/master/dofinale/static/images/icons/chatbot_icon.png?raw=true"
                              }
                            }
                          }
                        ]
                      }
                    ]
                  ]
                }
            }
        ])


    # 제품 추천
    # intent Recomend_Products 확인
    if(req['queryResult']['intent']['displayName']=="Recomend_Products"):
        print("접속 인텐트: Recomend_Products")
        #with open('./static/json_data/products.json', 'r', encoding="UTF-8") as file:
        print(os.getcwd())
        with open('./dofinale/static/json_data/products.json', 'r', encoding="UTF-8") as file:
            products = json.load(file)
            # print('제품 정보:', products)
            return jsonify(fulfillment_messages=[
                {
                    "payload": {
                      "richContent": [
                        [
                          {
                            "type": "description",
                            "title": "브랜드평판지수"
                          },
                          {
                            "subtitle": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['브랜드평판지수'][0]['line'],
                            "image": {
                              "src": {
                                "rawUrl": url_for('static', filename='images/products/')+products['scalp_type'][Members.query.get(current_user_id).scalp_type]['브랜드평판지수'][0]['image']
                              }
                            },
                            "type": "info",
                            "title": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['브랜드평판지수'][0]['product_name']
                          },
                          {
                            "subtitle": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['브랜드평판지수'][1]['line'],
                            "image": {
                              "src": {
                                "rawUrl": url_for('static', filename='images/products/')+products['scalp_type'][Members.query.get(current_user_id).scalp_type]['브랜드평판지수'][1]['image']
                              }
                            },
                            "type": "info",
                            "title": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['브랜드평판지수'][1]['product_name']
                          },
                          {
                            "subtitle": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['브랜드평판지수'][2]['line'],
                            "type": "info",
                            "title": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['브랜드평판지수'][2]['product_name'],
                            "image": {
                              "src": {
                                "rawUrl": url_for('static', filename='images/products/')+products['scalp_type'][Members.query.get(current_user_id).scalp_type]['브랜드평판지수'][2]['image']
                              }
                            }
                          }
                        ],
                        [
                          {
                              "type": "description",
                              "title": "의사 추천"
                          },
                          {
                              "image": {
                                  "src": {
                                      "rawUrl": url_for('static', filename='images/products/')+products['scalp_type'][Members.query.get(current_user_id).scalp_type]['의사추천'][0]['image']
                                  }
                              },
                              "title": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['의사추천'][0]['product_name'],
                              "type": "info",
                              "subtitle": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['의사추천'][0]['line']
                          },
                          {
                              "subtitle": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['의사추천'][1]['line'],
                              "image": {
                                  "src": {
                                      "rawUrl": url_for('static', filename='images/products/')+products['scalp_type'][Members.query.get(current_user_id).scalp_type]['의사추천'][1]['image']
                                  }
                              },
                              "title": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['의사추천'][0]['product_name'],
                              "type": "info"
                          },
                          {
                              "type": "info",
                              "image": {
                                  "src": {
                                      "rawUrl": url_for('static', filename='images/products/')+products['scalp_type'][Members.query.get(current_user_id).scalp_type]['의사추천'][2]['image']
                                  }
                              },
                              "title": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['의사추천'][2]['product_name'],
                              "subtitle": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['의사추천'][2]['line']
                          }
                        ],
                        [
                            {
                                "type": "description",
                                "title": "화해 랭킹순"
                            },
                            {
                                "type": "info",
                                "image": {
                                    "src": {
                                        "rawUrl": url_for('static', filename='images/products/')+products['scalp_type'][Members.query.get(current_user_id).scalp_type]['화해 랭킹순'][0]['image']
                                    }
                                },
                                "subtitle": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['화해 랭킹순'][0]['line'],
                                "title": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['화해 랭킹순'][0]['product_name']
                            },
                            {
                                "image": {
                                    "src": {
                                        "rawUrl": url_for('static', filename='images/products/')+products['scalp_type'][Members.query.get(current_user_id).scalp_type]['화해 랭킹순'][1]['image']
                                    }
                                },
                                "type": "info",
                                "subtitle": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['화해 랭킹순'][1]['line'],
                                "title": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['화해 랭킹순'][1]['product_name']
                            },
                            {
                                "type": "info",
                                "image": {
                                    "src": {
                                        "rawUrl": url_for('static', filename='images/products/')+products['scalp_type'][Members.query.get(current_user_id).scalp_type]['화해 랭킹순'][2]['image']
                                    }
                                },
                                "title": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['화해 랭킹순'][2]['product_name'],
                                "subtitle": products['scalp_type'][Members.query.get(current_user_id).scalp_type]['화해 랭킹순'][2]['line'],
                            }
                        ],
                        [
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://github.com/SongYeongchang/DoFinale/blob/master/dofinale/static/images/icons/chatbot_icon.png?raw=true"
                                            }
                                        },
                                        "text": "가까운 병원 무료로 찾기"
                                    },
                                    {
                                        "link": "https://c3be-112-221-224-124.jp.ngrok.io/",
                                        "text": "두피 진단 다시 해보기",
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://github.com/SongYeongchang/DoFinale/blob/master/dofinale/static/images/icons/chatbot_icon.png?raw=true"
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                      ]
                    }
                }
            ])


    # 병원 추천
    # intent Recomend_Hospitals 확인
    if(req['queryResult']['intent']['displayName']=="Recomend_Hospitals"):
        print("접속 인텐트: Recomend_Hospitals")
        return jsonify(fulfillment_messages=[
            {
                "payload":{
                  "richContent": [
                    [
                      {
                        "type": "description",
                        "title": "현재 주소를 입력해 주세요.",
                        "text": [
                          "입력하신 주소와 가장 가까운 두피, 모발 전문병원을 추천해드립니다.",
                            "입력받은 주소의 위경도 값을 계산하여 가장 가까운 병원을 소개해드립니다."
                        ]
                      }
                    ]
                  ]
                }
            }
        ])

    # 병원 추천 > 주소 입력받고 > db에 저장된 병원 위경도값 비교해서 최단거리 병원 출력
    if (req['queryResult']['intent']['displayName'] == "Closest_Hospitals"):
        print("접속 인텐트: Closest_Hospitals")

        # 현재 위치 위경도값 계산
        current_position = get_lat_and_log(req['queryResult']['queryText'])
        # print(current_position)

        # 병원 json파일 열기
        with open('./hospitals.json', 'r', encoding="UTF-8") as file:
            hospitals = json.load(file)
            # print('병원 정보:',hospitals)
            # print('병원 위경도:',type(list(hospitals.keys())))
            # print('병원 개수:',len(hospitals.keys()))

            tmp_dic={} # 딕셔너리 키(병원 위경도):값(거리)
            for i, hospital_lat_lon in enumerate(hospitals):
                # print(hospital_lat_lon) # hospitals의 키
                # print(tuple(list(map(float, hospital_lat_lon.split(',')))))
                # print(tuple(hospital_lat_lon))
                # print(type(hospital_lat_lon))
                # print("거리:",haversine(current_position,tuple(list(map(float, hospital_lat_lon.split(','))))))

                # 딕셔너리 저장 키(병원 위경도):값(거리)
                tmp_dic[hospital_lat_lon]=haversine(current_position,tuple(list(map(float, hospital_lat_lon.split(',')))))

            # 오름차순 정렬, 최단거리 순으로 정렬
            tmp_dic=dict(sorted(tmp_dic.items(), key=lambda x: x[1]))
            # print(tmp_dic)

            # # 최단거리 3개만 출력
            # for i in range(0,3):
            #     print(list(tmp_dic.keys())[i])
            #     print(hospitals[list(tmp_dic.keys())[i]]['병원명'])
            #     print(hospitals[list(tmp_dic.keys())[i]]['병원 주소'])
            #     print(hospitals[list(tmp_dic.keys())[i]]['병원 홈페이지'])
            #     print(hospitals[list(tmp_dic.keys())[i]]['병원 전화번호'])

            return jsonify(fulfillment_messages=[
                {
                    "payload":{
                      "richContent": [
                        [
                          {
                            "type": "info",
                            "title": hospitals[list(tmp_dic.keys())[0]]['병원명'],
                            "subtitle": hospitals[list(tmp_dic.keys())[0]]['병원 전화번호'] + '/' + hospitals[list(tmp_dic.keys())[0]]['병원 주소'],
                            "actionLink": hospitals[list(tmp_dic.keys())[0]]['병원 홈페이지']
                          }
                        ],
                        [
                          {
                            "type": "info",
                            "title": hospitals[list(tmp_dic.keys())[1]]['병원명'],
                            "subtitle": hospitals[list(tmp_dic.keys())[1]]['병원 전화번호'] + '/' + hospitals[list(tmp_dic.keys())[1]]['병원 주소'],
                            "actionLink": hospitals[list(tmp_dic.keys())[1]]['병원 홈페이지']
                          }
                        ],
                        [
                          {
                            "type": "info",
                            "title": hospitals[list(tmp_dic.keys())[2]]['병원명'],
                            "subtitle": hospitals[list(tmp_dic.keys())[2]]['병원 전화번호'] + '/' + hospitals[list(tmp_dic.keys())[2]]['병원 주소'],
                            "actionLink": hospitals[list(tmp_dic.keys())[2]]['병원 홈페이지']
                          }
                        ],
                        [
                              {
                                "type": "chips",
                                "options": [
                                    {
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://github.com/SongYeongchang/DoFinale/blob/master/dofinale/static/images/icons/chatbot_icon.png?raw=true"
                                            }
                                        },
                                        "text": "제품 추천 무료로 받기"
                                    },
                                    {
                                        "link": "https://c3be-112-221-224-124.jp.ngrok.io/",
                                        "text": "두피 진단 다시 해보기",
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://github.com/SongYeongchang/DoFinale/blob/master/dofinale/static/images/icons/chatbot_icon.png?raw=true"
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                      ]
                    }
                }

            ])




'''
https://dialogflow.cloud.google.com/
https://cloud.google.com/dialogflow#section-5
# 응답 메세지로 버튼, 이미지 등
https://cloud.google.com/dialogflow/es/docs/intents-rich-messages?hl=ko#where
https://cloud.google.com/dialogflow/cx/docs/concept/integration/dialogflow-messenger#df-request-sent
'''