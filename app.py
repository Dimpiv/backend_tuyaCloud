from tuya import Core
from aiohttp import web

tuya = Core()


async def get_hash(request):
    tuya.check_token()
    data = request.match_info.get('string', "")
    result = tuya.gen_sign(data)
    return web.Response(text=result)


async def get_id(request):
    return web.Response(text=tuya.AccessId)


async def get_server_url(request):
    return web.Response(text=tuya.ServerUrl)


async def get_schema(request):
    return web.Response(text=tuya.Schema)


async def get_easy_token(request):
    return web.Response(text=tuya.easy_token)

app = web.Application()
app.add_routes([web.get('/api/id', get_id),
                web.get('/api/sign/{string}', get_hash),
                web.get('/api/server', get_server_url),
                web.get('/api/schema', get_schema),
                web.get('/api/easy_token', get_easy_token)])

if __name__ == '__main__':
    web.run_app(app, port=8088)
