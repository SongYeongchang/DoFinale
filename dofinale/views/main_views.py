from flask import Blueprint, render_template, url_for, session, request, jsonify, g
import json
from werkzeug.utils import redirect
from geopy.geocoders import Nominatim # 가까운 병원 위경도 값으로 찾기
from haversine import haversine


from dofinale import db
from dofinale.models import Members, Boards, Userpost
from dofinale.sentencebert import chatbot_text


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    return redirect(url_for('main.intro'))

@bp.route('/intro/')
def intro():
    board_list = Boards.query.order_by(Boards.id.asc())
    return render_template('intro.html',
                           board_list=board_list,
                           isbgvid=True)

@bp.route('/chatbot/',methods=('POST','GET'))
def chatbot():
    print('chatbot accessed')
    # 사용자가 챗봇에 입력 시 데이터 받기
    req = request.get_json(force=True)
    print(req)
    current_user_id = req['originalDetectIntentRequest']['payload']['userId']

    print('*'*100)
    print("사용자 입력값:", req['queryResult']['queryText'])
    print("접속 인텐트: ",req['queryResult']['intent']['displayName'])

    # 각 사용자별 다이얼로그 플로우 세션 값 저장 ----------------------------------------------------------------------------------

    if (req['queryResult']['intent']['displayName'] == "Default Welcome Intent"):
        if current_user_id != "no_user":
            return jsonify(fulfillment_messages=[
                {
                    "payload":{
                      "richContent": [
                        [
                          {
                            "rawUrl": "https://img.freepik.com/free-vector/chatbot-artificial-intelligence-abstract-concept-illustration_335657-3723.jpg?w=740&t=st=1660823759~exp=1660824359~hmac=1863a0ac158d30806388159e3696d831db9c59bcbe54f6f5d2cf4b6adfa2985f",
                            "type": "image",
                            "accessibilityText": "두피 진단 예측 welcome"
                          },
                          {
                            "title": f"안녕하세요, {Members.query.get(current_user_id).userid}님!",
                            "type": "info",
                            "subtitle": "무엇을 도와드릴까요?"
                          },
                          {
                            "options": [
                                {
                                    "text": "AI 두피분석 결과 확인하기",
                                    "image": {

                                        "src": {
                                            './dofinale/static/images/icons/ai.png'
                                        }
                                    }
                                },
                                {
                                    "text": "자가진단 결과 확인하기",
                                    "image": {
                                        "src": {
                                            "rawUrl": "https://github.com/SongYeongchang/DoFinale/blob/master/dofinale/static/images/icons/chatbot_icon.png?raw=true"
                                        }
                                    }
                                },
                                {
                                    "text": "DooFy에게 고민 걱정 이야기하기",
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
        else:
            return jsonify(fulfillment_messages=[
                {
                    "payload": {
                        "richContent": [
                            [
                                {
                                    "rawUrl": "https://img.freepik.com/free-vector/chatbot-artificial-intelligence-abstract-concept-illustration_335657-3723.jpg?w=740&t=st=1660823759~exp=1660824359~hmac=1863a0ac158d30806388159e3696d831db9c59bcbe54f6f5d2cf4b6adfa2985f",
                                    "type": "image",
                                    "accessibilityText": "두피 진단 예측 welcome"
                                },
                                {
                                    "title": f"안녕하세요, 서비스를 이용하려면 로그인해주세요!",
                                    "type": "info",
                                    "subtitle": "무엇을 도와드릴까요?"
                                },
                                {
                                    "options": [
                                        {
                                            "text": "로그인하러 가기",
                                            "link": url_for('auth.login'),
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
                                "rawUrl": "https://raw.githubusercontent.com/SongYeongchang/DoFinale/master/dofinale/static/images/icons/chatbot.png"
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

    # -------------------------------------------------------------------------------------------------

    # 위로 챗봇 연결
    if (req['queryResult']['intent']['displayName'] == "chat with Doofy"):
            return jsonify(fulfillment_messages=[
                {
                    "payload": {
                        "richContent": [
                            [
                                {
                                    "type": "description",
                                    "title": "고민을 이야기 해주세요",
                                    "text": [
                                        "고민, 걱정거리 스트레스 등"

                                    ]
                                }
                            ]
                        ]
                    }
                }
            ])

    if (req['queryResult']['intent']['displayName'] == "chat with Doofy - SentenceBERT"):
            return jsonify(fulfillment_messages=[
                {
                    "payload": {
                        "richContent": [
                            [
                                {
                                    "type": "description",
                                    "title": chatbot_text(req['queryResult']['queryText'])["챗봇"]

                                }
                            ]
                        ]
                    }
                }
            ])


    # -------------------------------------------------------------------------------------------------

    # 자가 진단 결과 확인하기
    if (req['queryResult']['intent']['displayName'] == "survey"):
        return jsonify(fulfillment_messages=[
            {
                "payload": {
                    "richContent": [
                        [
                            {
                                "rawUrl": "https://www.sciencetimes.co.kr/wp-content/uploads/2020/10/GettyImages-1222023758-scaled.jpg",
                                "type": "image",
                                "accessibilityText": "두피 진단 예측"
                            },
                            {
                                "subtitle": "더 정확한 진단 결과를 원하시면, AI분석 서비스를 이용해주세요",
                                "title": "자가 진단 결과: '" + Members.query.get(current_user_id).ml_result + "'입니다.",
                                "type": "info"
                            },
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "link": url_for('service.scalp_diagnosis'),
                                        "text": "AI 분석 서비스 이용하러 가기",
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


    # -------------------------------------------------------------------------------------------------

    # 진단 결과 확인하기
    if (req['queryResult']['intent']['displayName'] == "scalp type diagnosis"):
        return jsonify(fulfillment_messages=[
            {
                "payload": {
                    "richContent": [
                        [
                            {
                                "rawUrl": "https://www.sciencetimes.co.kr/wp-content/uploads/2020/10/GettyImages-1222023758-scaled.jpg",
                                "type": "image",
                                "accessibilityText": "두피 진단 예측"
                            },
                            {
                                "subtitle": "예측된 두피 진단 결과로 다음과 같은 서비스를 이용해보세요",
                                "title": "당신의 두피 상태는 '" + Members.query.get(current_user_id).scalp_type + "'입니다.",
                                "type": "info"
                            },
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://raw.githubusercontent.com/SongYeongchang/DoFinale/master/dofinale/static/images/icons/chatbot.png"
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
                                        "link": url_for('service.scalp_diagnosis'),
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

    # 진단 결과 확인하기 - 제품 추천
    if(req['queryResult']['intent']['displayName']=="scalp type diagnosis - Recommend_Products"):
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
                                        "link": url_for('service.scalp_diagnosis'),
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

    # 진단 결과 확인하기 - 병원 추천
    if(req['queryResult']['intent']['displayName']=="scalp type diagnosis - Recomend_Hospitals"):
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
    if (req['queryResult']['intent']['displayName'] == "scalp type diagnosis - Recomend_Hospitals - Closest_Hospitals"):

        # 현재 위치 위경도값 계산
        current_position = get_lat_and_log(req['queryResult']['queryText'])
        # print(current_position)

        # 병원 json파일 열기
        with open('./dofinale/static/json_data/hospitals.json', 'r', encoding="UTF-8") as file:
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
                                        "link": url_for('service.scalp_diagnosis'),
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