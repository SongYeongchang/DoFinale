from flask import Blueprint, render_template, url_for, request, session, jsonify
import json

bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@bp.route('/',methods=('POST','GET'))
def chatbot():
    req = request.get_json(force=True)
    print(req)
    # return jsonify(fulfillmentText='챗봇 접속 성공')
    return jsonify(fulfillment_messages=[
        {
            "payload" : {
                "richContent" : [
                    [
                        {
                            "type" : "image",
                            "rawUrl" : "https://mblogthumb-phinf.pstatic.net/MjAyMDExMjdfNTcg/MDAxNjA2NDMyNzU0MjQx.fHN80T_vVc3OJ_xtIgYw5ods4c9n76UrQusTAMAdtRMg.3gaKaUYMXfXd1c-rSqkJtVJkell5_GEpjwoCvIcpLOgg.JPEG.rainbow8sun/20201127%EF%BC%BF081847.jpg?type=w800"
                        },
                        {
                            "type": "info",
                            "title": "피자메뉴",
                            "subtitle": "Info item subtitle",
                            "actionLink": "https://example.com"
                        },
                        {
                            "type": "description",
                            "title": "Description title",
                            "text": [
                                "This is text line 1.",
                                "This is text line 2."
                            ]
                        },
                        {
                            "type": "button",
                            "icon": {
                                "type": "chevron_right",
                                "color": "#FF9800"
                            },
                            "text": "Button text",
                            "link": "https://example.com",
                            "event": {
                                "name": "",
                                "languageCode": "",
                                "parameters": {}
                            }
                        },
                        {
                            "type": "chips",
                            "options": [
                                {
                                    "text": "Chip 1",
                                    "image": {
                                        "src": {
                                            "rawUrl": "https://example.com/images/logo.png"
                                        }
                                    },
                                    "link": "https://example.com"
                                },
                                {
                                    "text": "Chip 2",
                                    "image": {
                                        "src": {
                                            "rawUrl": "https://example.com/images/logo.png"
                                        }
                                    },
                                    "link": "https://example.com"
                                }
                            ]
                        }
                    ]
                ]
            }
        }
    ])