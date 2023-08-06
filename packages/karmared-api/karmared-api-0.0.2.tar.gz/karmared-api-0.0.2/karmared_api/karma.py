import asyncio
import json
from aiohttp import ClientSession

from graphql import get_introspection_query

loop = asyncio.get_event_loop()


async def fetch(url, **kwargs):
    async with ClientSession(loop=loop) as session:
        async with session.post(url, **kwargs) as response:
            text = await response.text()
            try:
                json_data = json.loads(text)
            except Exception:
                raise Exception(text)

            return json_data


DEFAULT_URL = "https://my.karma.red/graphql"
LOGIN_MUTATION = "mutation Login($input: LoginWithEmailAndPasswordInput!) { loginWithEmailAndPassword(input: $input) { token } }"


class Karma:
    def __init__(self, token, url=DEFAULT_URL):
        self.token = token
        self.url = url

    async def login(email, password, url=DEFAULT_URL):
        res = await fetch(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                'query': LOGIN_MUTATION,
                'variables': {'input': {'email': email, 'password': password}},
            }))

        token = res.get('data', {}).get(
            'loginWithEmailAndPassword', {}).get('token')

        if token is None:
            raise Exception(res)

        return Karma(token, url)

    async def schema(self):
        return await fetch(
            self.url,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            params={
                'query': get_introspection_query(descriptions=False)
            }
        )

    async def request(self, query, variables={}):
        return await fetch(
            self.url,
            headers={
                'authorization': f"Bearer {self.token}",
                'content-type': 'application/json'
            },
            data=json.dumps({
                'query': query,
                'variables': variables
            }, ensure_ascii=False)
        )
