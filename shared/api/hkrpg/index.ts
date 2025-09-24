import { ofetch } from "ofetch";
import {
  checkResponse,
  getMihoYoBaseUrl,
  type BaseResponse,
} from "../../constant";
import { AnnListSchema } from "./schema/getAnnList";
import { AnnContentSchema } from "./schema/getAnnContent";

const query = {
  game: "hkrpg",
  game_biz: "hkrpg_cn",
  lang: "zh-cn",
  bundle_id: "hkrpg_cn",
  channel_id: "1",
  platform: "pc",
  region: "prod_gf_cn",
  level: "70",
  uid: "100000000",
};

const fetch = ofetch.create({
  query: query,
  timeout: 1000,
  baseURL: getMihoYoBaseUrl("hkrpg-ann-api"),
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
