# required spotipy
# pip install spotipy
import spotipy
import asyncio
from typing import Any
from pydantic import BaseModel

from chzzkpy.chat import ChatClient, ChatMessage

# Configuration
channel_id = "channel_id"
prefix = "$"


# Naver Authorization
NID_AUT = "NID_AUTHORIZATION_KEY"
NID_SES = "NID_SESSION_KEY"


# Spotify Authorization
client_id = 'Spotify App Client ID'
secret = 'Spotify App Client Secrect ID'
redirect_uri = 'http://localhost:8888/redirect'
scope = "user-modify-playback-state"
oauth_manager = spotipy.SpotifyOAuth(
    client_id=client_id,
    client_secret=secret,
    redirect_uri=redirect_uri,
    scope=scope
)

oauth_manager.get_auth_response()

chzzk_client = ChatClient(channel_id)
spotify_client = spotipy.Spotify(oauth_manager=oauth_manager)


class SpotifyMusicInfo(BaseModel):
    name: str
    artists: str
    uri: str

    @classmethod
    def from_spotify(cls, data: dict[str, Any]):
        artists = ", ".join([x['name'] for x in data['artists']])
        return cls(
            name=data['name'],
            artists=artists,
            uri=data['uri']
        )


@chzzk_client.event
async def on_connect():
    print("Ready bot.")


@chzzk_client.event
async def on_chat(message: ChatMessage):
    if not message.content.startswith("%s선곡" % prefix):
        return

    music_name = message.content.split()[1:]
    search_result = spotify_client.search(q=music_name, type="track", limit=5)
    tracks_result = search_result['tracks']
    items = [SpotifyMusicInfo.from_spotify(x) for x in tracks_result['items']]

    if len(items) <= 0:
        await chzzk_client.send_chat("검색 결과가 없습니다 :(")
        return
    item = items[0]
    spotify_client.add_to_queue(item.uri)
    await chzzk_client.send_chat("%s - %s 노래가 추가되었습니다." % (item.name, item.artists))
    return

chzzk_client.run(NID_AUT, NID_SES)
