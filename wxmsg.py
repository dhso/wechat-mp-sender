#-*- coding: utf-8 -*-
#/usr/bin/python

#使用方法 python ./wxmsg.py "appid" "appsecret"

import sys
import requests
import json
from bottle import request, run, post, install
from bottle_sqlite import SQLitePlugin

install(SQLitePlugin(dbfile='wxmsg.db'))

@post('/wechat/template/send')
def wechat_template_send(db):
    users = request.json['users']
    template_id = request.json['template_id']
    url = request.json.get('url', None)
    template_data = request.json.get('template_data', {})
    appid = request.json.get('appid', sys.argv[1])
    appsecret = request.json.get('appsecret', sys.argv[2])
    access_token = getAccessToken(db, appid, appsecret)
    for user in users:
        message_data = { 
                "touser": user,
                "template_id": template_id,
                "url": url,
                "data": template_data
                }
        sendTemplateMessage(db, access_token, message_data)
    return {'result':'success'}

def getAccessToken(db, appid, appsecret):
    row = db.execute("SELECT * FROM access_tokens WHERE appid = ? and expires_date > datetime('now','localtime')", [appid] ).fetchone()
    if row:
        return row['access_token']
    token_data = requestAccessToken(appid, appsecret)
    access_token = token_data['access_token']
    sql = "REPLACE INTO access_tokens VALUES (?, ?, datetime('now', 'localtime', '+{} seconds'))".format(token_data['expires_in'])
    db.execute(sql, [appid, access_token])
    return access_token

def requestAccessToken(appid, appsecret):
    access_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(appid, appsecret)
    access_token_response = requests.get(access_token_url)
    return json.loads(access_token_response.content)

def sendTemplateMessage(db, access_token, message_data):
    send_message_url="https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    json_headers = {'Content-Type': 'application/json'}
    result = requests.post(url=send_message_url, headers=json_headers, data=json.dumps(message_data))
    db.execute("INSERT INTO message_send_logs VALUES (?, ?, datetime('now', 'localtime'))", [json.dumps(message_data), result.content])
    return json.loads(result.content)

run(host='0.0.0.0', port=8080, reloader=True, debug=False)