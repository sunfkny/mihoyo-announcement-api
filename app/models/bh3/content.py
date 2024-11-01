from __future__ import annotations

from pydantic import BaseModel


class ListItem(BaseModel):
    ann_id: int
    title: str
    subtitle: str
    banner: str
    content: str
    lang: str

    @property
    def image(self):
        return self.banner


class Data(BaseModel):
    list: list[ListItem]
    pic_list: list
    total: int
    pic_total: int


class Model(BaseModel):
    retcode: int
    message: str
    data: Data

    def get_gacha_info(self):
        return [
            i
            for i in self.data.list
            if "补给" in i.subtitle
            and any(
                t in i.content
                for t in [
                    "补给信息",
                    "补给规则",
                ]
            )
        ]
