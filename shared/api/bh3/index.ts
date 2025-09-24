import { ofetch } from "ofetch";
import {
  checkResponse,
  getMihoYoBaseUrl,
  type BaseResponse,
} from "../../constant";
import { AnnListSchema } from "./schema/getAnnList";
import { AnnContentSchema } from "./schema/getAnnContent";

const query = {
  game: "bh3",
  game_biz: "bh3_cn",
  lang: "zh-cn",
  bundle_id: "bh3_cn",
  channel_id: "14",
  level: "88",
  platform: "pc",
  region: "bb01",
  uid: "100000000",
};

const fetch = ofetch.create({
  query: query,
  timeout: 1000,
  baseURL: getMihoYoBaseUrl("ann-api"),
  responseType: "json",
});

export async function getAnnList() {
  const resp = await fetch<BaseResponse>(
    `/common/${query.game_biz}/announcement/api/getAnnList`
  );
  checkResponse(resp);
  return AnnListSchema.loose().parse(resp);
}

export async function getAnnContent() {
  const resp = await fetch<BaseResponse>(
    `/common/${query.game_biz}/announcement/api/getAnnContent`
  );
  checkResponse(resp);
  return AnnContentSchema.loose().parse(resp);
}
