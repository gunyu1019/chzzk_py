# chzzkpy

![PyPI - Version](https://img.shields.io/pypi/v/chzzkpy?style=flat)
![PyPI - Downloads](https://img.shields.io/pypi/dm/chzzkpy?style=flat)
![PyPI - License](https://img.shields.io/pypi/l/chzzkpy?style=flat)

파이썬 기반의 치지직(네이버 라이브 스트리밍 서비스)의 비공식 라이브러리 입니다.<br/>
채팅 기능을 중점으로 개발하였으며, 다른 기능도 개발될 예정입니다.

An unofficial python library for [Chzzk(Naver Live Streaming Service)](https://chzzk.naver.com/).<br/>
This library focused on chat. However, other feature will be developed.

#### Available Features

* 채팅
    * 사용자 상호 채팅 (`on_chat` <-> `client.send_chat`)
    * 사용자 후원 (`on_donation`)
    * 메시지 상단 고정하기 (`on_pin`, `on_unpin`)
    * 시스템 메시지 (`on_system_message`)
    * 메시지 관리
* 로그인 (쿠키 값 `NID_AUT`, `NID_SES` 사용)
* 검색 (채널, 영상, 라이브, 자동완성)
* 방송 상태 조회

## Installation

**Python 3.10 or higher is required.**

```bash
# Linux/MacOS
python3 -m pip install chzzkpy

# Windows
py -3 -m pip install chzzkpy
```

## Quick Example

`chzzkpy`를 사용한 예제는 [Examples](examples)에서 확인하실 수 있습니다.<br/>
아래는 간단한 예제입니다.

#### 방송인 검색

```py
import asyncio
import chzzkpy

loop = asyncio.get_event_loop()
client = chzzkpy.Client(loop=loop)

async def main():
    result = await client.search_channel("건유1019")
    if len(result) == 0:
        print("검색 결과가 없습니다 :(")
        return
    print(result[0].name)
    print(result[0].id)
    print(result[0].image)
    await client.close()

loop.run_until_complete(main())
```

#### 챗봇 (Chat-Bot)

```py
from chzzkpy.chat import ChatClient, ChatMessage, DonationMessage

client = ChatClient("channel_id")


@client.event
async def on_chat(message: ChatMessage):
    if message.content == "!안녕":
        await client.send_chat("%s님, 안녕하세요!" % message.profile.nickname)


@client.event
async def on_donation(message: DonationMessage):
    await client.send_chat("%s님, %d원 후원 감사합니다." % (message.profile.nickname, message.extras.pay_amount))


client.run("NID_AUT", "NID_SES")
```

## Contributions 
`chzzkpy`의 기여는 언제든지 환영합니다!<br/>
버그 또는 새로운 기능은 `Pull Request`로 진행해주세요.
