import asyncio
import datetime

import bs4
import pydantic

from ..models.bh3.content import Model as ContentModel
from ..models.bh3.list import Model as ListModel
from ..utils import request_async
from ..utils.datetime import get_datetime, get_humanize, get_timezone


async def get_ann_list():
    response_data = await request_async(
        "https://ann-api.mihoyo.com/common/bh3_cn/announcement/api/getAnnList",
        {
            "game": "bh3",
            "game_biz": "bh3_cn",
            "lang": "zh-cn",
            "bundle_id": "bh3_cn",
            "channel_id": "14",
            "level": "88",
            "platform": "pc",
            "region": "bb01",
            "uid": "100000000",
        },
    )
    return ListModel.model_validate(response_data)


async def get_ann_content():
    response_data = await request_async(
        "https://ann-api.mihoyo.com/common/bh3_cn/announcement/api/getAnnContent",
        {
            "game": "bh3",
            "game_biz": "bh3_cn",
            "lang": "zh-cn",
            "bundle_id": "bh3_cn",
            "channel_id": "14",
            "level": "88",
            "platform": "pc",
            "region": "bb01",
            "uid": "100000000",
        },
    )
    return ContentModel.model_validate(response_data)


class Bh3GachaInfo(pydantic.BaseModel):
    ann_id: int
    title: str
    image: str
    content: str
    info: str | None


class Bh3Progress(pydantic.BaseModel):
    percent: float | None
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    end_time_humanize: str | None


class Bh3Response(pydantic.BaseModel):
    progress: Bh3Progress
    gacha_info: list[Bh3GachaInfo]


async def get_bh3_gacha_info():
    ann_list, ann_content = await asyncio.gather(get_ann_list(), get_ann_content())
    version_info = ann_list.get_version_info()
    timezone = ann_list.data.timezone
    gacha_info: list[Bh3GachaInfo] = []
    progress_percent = None
    progress_start_time = None
    progress_end_time = None
    progress_end_time_humanize = None
    current_time = get_datetime()

    if version_info:
        progress_start_time = get_datetime(version_info.start_time, timezone)
        progress_end_time = get_datetime(version_info.end_time, timezone)
        progress_end_time_humanize = get_humanize(dt=progress_end_time, to=current_time)
        if progress_start_time <= current_time <= progress_end_time:
            progress_percent = (current_time - progress_start_time) / (progress_end_time - progress_start_time)

    for i in ann_content.get_gacha_info():
        content_soup = bs4.BeautifulSoup(i.content, "html.parser")
        elements = []
        open_time_header = content_soup.find(string=["开放时间"])
        if open_time_header and open_time_header.parent:
            elements.append(open_time_header.parent.find_next_sibling())

        info_header = content_soup.find(string=["补给信息"])
        if info_header and info_header.parent:
            info_header_next = info_header.parent.find_next_sibling()
            elements.append(info_header_next)

            if info_header_next and any(i in info_header_next.text for i in ["如下", "以下"]):
                elements.append(info_header_next.find_next_sibling())

        elements = [i for i in elements if i]
        info = None
        if elements:
            info = "".join([str(i) for i in elements])

        gacha_info.append(
            Bh3GachaInfo(
                ann_id=i.ann_id,
                title=i.title,
                image=i.image,
                content=i.content,
                info=info,
            )
        )

    return Bh3Response(
        progress=Bh3Progress(
            percent=progress_percent,
            start_time=progress_start_time,
            end_time=progress_end_time,
            end_time_humanize=progress_end_time_humanize,
        ),
        gacha_info=gacha_info,
    )
