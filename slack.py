from getpass import getpass
import os
import urllib
import urllib.request
import json
import websocket

TOKEN_NAME = "GPM_SLACK_TOKEN"

def makeUrl(token, method, params={}):
    url = "https://slack.com/api/"
    params["token"] = token
    return url + method + "?" + urllib.parse.urlencode(params)

def getJson(url):
    return json.loads(urllib.request.urlopen(url).read())


if __name__ == "__main__":
    btoken = os.getenv(TOKEN_NAME) or getpass(TOKEN_NAME)

    def getWsUrl():
        jsn = getJson(makeUrl(btoken, "rtm.connect"))
        return jsn["url"]

    def post(channel, mes):
        url = makeUrl(btoken, "chat.postMessage", {
            "channel": channel,
            "text": mes,
            })
        js = getJson(url)
        print(js)


    def on_message(ws, mes):
        print("recieved: " + mes)
        js = json.loads(mes)
        if js["type"] == "message" and not "bot_id" in js:
            print("post to " + js["channel"] + " " + js["text"])
            post(js["channel"], js["text"])
            

    def on_error(ws, err):
        print(err)

    def on_close(ws):
        print("closed")

    def on_open(ws):
        print("open")

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(getWsUrl(),
            on_message = on_message,
            on_error = on_error,
            on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    
