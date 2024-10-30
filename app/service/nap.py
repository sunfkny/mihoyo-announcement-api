import asyncio
import datetime
import re

import bs4
import pydantic

from ..models.nap.content import Model as ContentModel
from ..models.nap.list import Model as ListModel
from ..utils import request_async
from ..utils.datetime import get_datetime, get_humanize, get_timezone


async def get_ann_list():
    response_data = await request_async(
        "https://announcement-api.mihoyo.com/common/nap_cn/announcement/api/getAnnList",
        {
            "game": "nap",
            "game_biz": "nap_cn",
            "lang": "zh-cn",
            "bundle_id": "nap_cn",
            "platform": "pc",
            "region": "prod_gf_cn",
            "level": 40,
            "channel_id": 1,
            "uid": 10000000,
        },
    )

    return ListModel.model_validate(response_data)


async def get_ann_content():
    response_data = await request_async(
        "https://announcement-api.mihoyo.com/common/nap_cn/announcement/api/getAnnContent",
        {
            "game": "nap",
            "game_biz": "nap_cn",
            "lang": "zh-cn",
            "bundle_id": "nap_cn",
            "platform": "pc",
            "region": "prod_gf_cn",
            "level": 40,
            "channel_id": 1,
            "uid": 10000000,
        },
    )
    return ContentModel.model_validate(response_data)


class NapGachaInfo(pydantic.BaseModel):
    ann_id: int
    title: str
    image: str
    content: str
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    start_time_humanize: str | None
    end_time_humanize: str | None


class NapProgress(pydantic.BaseModel):
    percent: float | None
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    end_time_humanize: str | None


class NapResponse(pydantic.BaseModel):
    progress: NapProgress
    gacha_info: list[NapGachaInfo]


async def get_nap_gacha_info():
    ann_list, ann_content = await asyncio.gather(get_ann_list(), get_ann_content())
    version_info = ann_list.get_version_info()
    timezone = ann_list.data.timezone
    gacha_info: list[NapGachaInfo] = []
    progress_percent = None
    progress_start_time = None
    progress_end_time = None
    progress_end_time_humanize = None
    current_time = get_datetime()

    if version_info:
        progress_start_time = get_datetime(version_info.start_time, timezone)
        progress_end_time = get_datetime(version_info.end_time, timezone)
        progress_end_time_humanize = get_humanize(progress_end_time, current_time)
        if progress_start_time <= current_time <= progress_end_time:
            progress_percent = (current_time - progress_start_time) / (progress_end_time - progress_start_time)

    for i in ann_content.get_gacha_info():
        # 常驻频段
        stable_channel = "「热门卡司」调频说明"
        # 邦布频段
        bangboo_channel = "「卓越搭档」调频说明"
        # 永久频段
        permanent_channel_list = [
            stable_channel,
            bangboo_channel,
        ]
        if i.subtitle in permanent_channel_list:
            continue

        content_soup = bs4.BeautifulSoup(i.content, "html.parser")
        info_table_time = content_soup.select_one("table tr:nth-child(2) td")
        text = info_table_time.text if info_table_time else ""
        t = re.search(
            r"(?:(.*?后)|(.*?)（服务器时间）)~(.*?)（服务器时间）",
            text,
            re.MULTILINE,
        )
        start_time = None
        end_time = None
        start_time_humanize = None
        end_time_humanize = None
        match t.groups() if t else None:
            case [start_str, None, end_time]:
                end_time = get_datetime(end_time, timezone)
                end_time_humanize = get_humanize(end_time, current_time)
                start_time_humanize = f"{start_str}"
            case [None, start_time, end_time]:
                start_time = get_datetime(start_time, timezone)
                end_time = get_datetime(end_time, timezone)
                start_time_humanize = get_humanize(start_time, current_time)
                end_time_humanize = get_humanize(end_time, current_time)

            case _:
                pass

        gacha_info.append(
            NapGachaInfo(
                ann_id=i.ann_id,
                title=i.subtitle,
                image=i.banner,
                content=i.content,
                start_time=start_time,
                end_time=end_time,
                start_time_humanize=start_time_humanize,
                end_time_humanize=end_time_humanize,
            )
        )

    return NapResponse(
        progress=NapProgress(
            percent=progress_percent,
            start_time=progress_start_time,
            end_time=progress_end_time,
            end_time_humanize=progress_end_time_humanize,
        ),
        gacha_info=gacha_info,
    )
