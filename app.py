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

app = web.Application()
app.add_routes([web.get('/id', get_id),
                web.get('/hash/{string}', get_hash),
                web.get('/server', get_server_url),
                web.get('/schema', get_schema)])

if __name__ == '__main__':
    web.run_app(app, port=8088)
