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

app = web.Application()
app.add_routes([web.get('/id', get_id),
                web.get('/get_hash/{string}', get_hash)])

if __name__ == '__main__':
    web.run_app(app)
