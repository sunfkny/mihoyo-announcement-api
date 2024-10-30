import asyncio
import datetime
import re

import pydantic

from ..models.hkrpg.content import Model as ContentModel
from ..models.hkrpg.list import Model as ListModel
from ..utils import request_async
from ..utils.datetime import get_datetime, get_humanize, get_timezone


async def get_ann_list():
    response_data = await request_async(
        "https://hkrpg-ann-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList",
        {
            "game": "hkrpg",
            "game_biz": "hkrpg_cn",
            "lang": "zh-cn",
            "bundle_id": "hkrpg_cn",
            "channel_id": "1",
            "platform": "pc",
            "region": "prod_gf_cn",
            "level": "70",
            "uid": "100000000",
        },
    )

    return ListModel.model_validate(response_data)


async def get_ann_content():
    response_data = await request_async(
        "https://hkrpg-ann-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnContent",
        {
            "game": "hkrpg",
            "game_biz": "hkrpg_cn",
            "lang": "zh-cn",
            "bundle_id": "hkrpg_cn",
            "channel_id": "1",
            "platform": "pc",
            "region": "prod_gf_cn",
            "level": "70",
            "uid": "100000000",
        },
    )
    return ContentModel.model_validate(response_data)


class HkrpgGachaInfo(pydantic.BaseModel):
    ann_id: int
    title: str
    image: str
    content: str
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    start_time_humanize: str | None
    end_time_humanize: str | None


class HkrpgProgress(pydantic.BaseModel):
    percent: float | None
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    end_time_humanize: str | None


class HkrpgResponse(pydantic.BaseModel):
    progress: HkrpgProgress
    gacha_info: list[HkrpgGachaInfo]


async def get_hkrpg_gacha_info():
    ann_list, ann_content = await asyncio.gather(get_ann_list(), get_ann_content())
    version_info = ann_list.get_version_info()
    timezone = ann_list.data.timezone
    gacha_info: list[HkrpgGachaInfo] = []
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
        t = re.search(
            r"(?:([0-9]+\.[0-9]版本更新后)|(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}(?::\d{2})?)).*?(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}(?::\d{2})?)",
            i.content,
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
            HkrpgGachaInfo(
                ann_id=i.ann_id,
                title=i.title,
                image=i.image,
                content=i.content,
                start_time=start_time,
                end_time=end_time,
                start_time_humanize=start_time_humanize,
                end_time_humanize=end_time_humanize,
            )
        )

    return HkrpgResponse(
        progress=HkrpgProgress(
            percent=progress_percent,
            start_time=progress_start_time,
            end_time=progress_end_time,
            end_time_humanize=progress_end_time_humanize,
        ),
        gacha_info=gacha_info,
    )
