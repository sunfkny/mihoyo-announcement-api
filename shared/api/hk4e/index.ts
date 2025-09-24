import { ofetch } from "ofetch";
import {
  checkResponse,
  getMihoYoBaseUrl,
  type BaseResponse,
} from "../../constant";
import { AnnListSchema } from "./schema/getAnnList";
import { AnnContentSchema } from "./schema/getAnnContent";

const query = {
  game: "hk4e",
  game_biz: "hk4e_cn",
  lang: "zh-cn",
  from_cloud_web: "1",
  bundle_id: "hk4e_cn",
  channel_id: "1",
  level: "60",
  platform: "pc",
  region: "cn_gf01",
  uid: "100000000",
};

const fetch = ofetch.create({
  query: query,
  timeout: 1000,
  baseURL: getMihoYoBaseUrl("hk4e-ann-api"),
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
