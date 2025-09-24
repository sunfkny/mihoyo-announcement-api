import { describe, expect, it } from "vitest";
import {
  getAnnContent as getBh3AnnContent,
  getAnnList as getBh3AnnList,
} from "../shared/api/bh3";
import {
  getAnnContent as getHk4eAnnContent,
  getAnnList as getHk4eAnnList,
} from "../shared/api/hk4e";
import {
  getAnnContent as getHkrpgAnnContent,
  getAnnList as getHkrpgAnnList,
} from "../shared/api/hkrpg";
import {
  getAnnContent as getNapAnnContent,
  getAnnList as getNapAnnList,
} from "../shared/api/nap";

describe("api", () => {
  it.concurrent("getBh3AnnList", async () => {
    const r = await getBh3AnnList();
    expect(r.retcode).toBe(0);
    expect(r.data.total).toBeGreaterThan(0);
  });
  it.concurrent("getBh3AnnContent", async () => {
    const r = await getBh3AnnContent();
    expect(r.retcode).toBe(0);
    expect(r.data.total).toBeGreaterThan(0);
  });
  it.concurrent("getHk4eAnnList", async () => {
    const r = await getHk4eAnnList();
    expect(r.retcode).toBe(0);
    expect(r.data.total).toBeGreaterThan(0);
  });
  it.concurrent("getHk4eAnnContent", async () => {
    const r = await getHk4eAnnContent();
    expect(r.retcode).toBe(0);
    expect(r.data.total).toBeGreaterThan(0);
  });
  it.concurrent("getHkrpgAnnList", async () => {
    const r = await getHkrpgAnnList();
    expect(r.retcode).toBe(0);
    expect(r.data.total).toBeGreaterThan(0);
  });
  it.concurrent("getHkrpgAnnContent", async () => {
    const r = await getHkrpgAnnContent();
    expect(r.retcode).toBe(0);
    expect(r.data.total).toBeGreaterThan(0);
  });
  it.concurrent("getNapAnnList", async () => {
    const r = await getNapAnnList();
    expect(r.retcode).toBe(0);
    expect(r.data.total).toBeGreaterThan(0);
  });
  it.concurrent("getNapAnnContent", async () => {
    const r = await getNapAnnContent();
    expect(r.retcode).toBe(0);
    expect(r.data.total).toBeGreaterThan(0);
  });
});
