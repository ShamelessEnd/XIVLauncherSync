import datetime
import hmac
import hashlib
import requests
import sys

def refreshSkPortCred(cred):
    r = requests.get("https://zonai.skport.com/web/v1/auth/refresh", headers= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0',
        'Accept': 'application/json, text/plain, */*',
        'cred': cred,
        'platform': '1',
        'vName': '1.0.0',
        'Origin': 'https://game.skport.com',
        'Referer': 'https://game.skport.com/'
    })
    token = None
    try:
        token = r.json()["data"]["token"]
    except:
        print("error refreshing cred")
        print(r.content)
    return token

def generateEndfieldCheckInSign(timestamp, token):
    str = '/web/v1/game/endfield/attendance'
    str += timestamp
    str += f'{{"platform":"1","timestamp":"{timestamp}","dId":"","vName":"1.0.0"}}'
    hmacHex = hmac.new(
        key=bytes(token, 'utf-8'),
        msg=bytes(str, 'utf-8'),
        digestmod= hashlib.sha256
    ).hexdigest()
    sign = hashlib.md5(bytes(hmacHex, 'utf-8')).hexdigest()
    return sign


def dailyEndfieldCheckIn(sk_game_role, cred):
    timestamp = str(int(datetime.datetime.now().timestamp()))
    token = refreshSkPortCred(cred)
    if not token:
        return
    sign = generateEndfieldCheckInSign(timestamp, token)
    r = requests.post('https://zonai.skport.com/web/v1/game/endfield/attendance', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://game.skport.com/',
        'Content-Type': 'application/json',
        'sk-language': 'en',
        'sk-game-role': sk_game_role,
        'cred': cred,
        'platform': "1",
        'vName': "1.0.0",
        'timestamp': timestamp,
        'sign': sign,
        'Origin': 'https://game.skport.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    })
    print(r.content)

if __name__ == '__main__':
    dailyEndfieldCheckIn(str(sys.argv[1]), str(sys.argv[2]))
