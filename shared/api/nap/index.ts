import { ofetch } from "ofetch";
import {
  checkResponse,
  getMihoYoBaseUrl,
  type BaseResponse,
} from "../../constant";
import { AnnListSchema } from "./schema/getAnnList";
import { AnnContentSchema } from "./schema/getAnnContent";

const query = {
  game: "nap",
  game_biz: "nap_cn",
  lang: "zh-cn",
  bundle_id: "nap_cn",
  platform: "pc",
  region: "prod_gf_cn",
  level: "60",
  channel_id: "1",
};

const fetch = ofetch.create({
  query: query,
  timeout: 1000,
  baseURL: getMihoYoBaseUrl("announcement-api"),
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
