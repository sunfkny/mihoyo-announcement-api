from fastapi import FastAPI

from app.service.bh3 import Bh3Response, get_bh3_gacha_info
from app.service.hk4e import Hk4eResponse, get_hk4e_gacha_info
from app.service.hkrpg import HkrpgResponse, get_hkrpg_gacha_info
from app.service.nap import NapResponse, get_nap_gacha_info

app = FastAPI()


@app.get("/bh3")
async def api_bh3() -> Bh3Response:
    return await get_bh3_gacha_info()


@app.get("/hk4e")
async def api_hk4e() -> Hk4eResponse:
    return await get_hk4e_gacha_info()


@app.get("/hkrpg")
async def api_hkrpg() -> HkrpgResponse:
    return await get_hkrpg_gacha_info()


@app.get("/nap")
async def api_nap() -> NapResponse:
    return await get_nap_gacha_info()
