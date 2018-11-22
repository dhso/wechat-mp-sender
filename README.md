# wechat-enterprise-sender
微信公众平台发送服务

## run

```
docker run -dt \
--name wechat-mp-sender \
-p 8080:8080 \
-e APPID='YOUR APPID' \
-e APPSECRET="YOUR APPSECRET" \
dhso/wechat-mp-sender
```
## api

- 模板消息

```
<domain>/wechat/template/send

{
    "users":["openid1","openid2"],
    "template_id":"asdasdadsasd",
	"url":"https://www.qq.com",
    "template_data":{
		"first": {
			"value":"恭喜你购买成功！",
			"color":"#173177"
		},
		"keyword1":{
			"value":"巧克力",
			"color":"#173177"
		},
		"keyword2": {
			"value":"39.8元",
			"color":"#173177"
		},
		"keyword3": {
			"value":"2014年9月22日",
			"color":"#173177"
		},
		"remark":{
			"value":"欢迎再次购买！",
			"color":"#173177"
		}
	}
}
```
