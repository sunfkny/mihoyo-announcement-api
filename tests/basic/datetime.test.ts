import { describe, expect, it } from "vitest";
import { formatChineseISOLocaleString, parseLocalDate } from "../../shared/datetime";


describe("parseDate", () => {
    describe("YYYY-MM-DD hh:mm:ss", () => {
        const want = new Date("2006-01-02T15:04:05+08:00");
        const data = [
            "2006-01-02 15:04:05",
            "2006-1-2 15:04:05",
            "2006/01/02 15:04:05",
            "2006/1/2 15:04:05",
            "2006-01-02 15:4:5",
            "2006-1-2 15:4:5",
            "2006/01/02 15:4:5",
            "2006/1/2 15:4:5",
            "2006年01月02日15:04:05",
            "2006年01月02日 15:04:05",
            "2006年1月2日 15:04:05",
            "2006年1月2日15:04:05",
            "2006年01月02日15:4:5",
            "2006年01月02日 15:4:5",
            "2006年1月2日 15:4:5",
            "2006年1月2日15:4:5",
            "2006-01-02  15:04:05",
            "  2006-01-02 15:04:05  ",
        ]
        for (const d of data) {
            const got = parseLocalDate(d);
            it(`"${d}"`, () => {
                expect(got).toEqual(want);
            });
        }
    })
    describe("YYYY-MM-DD hh:mm", () => {
        const want = new Date("2006-01-02T15:04:00+08:00");
        const data = [
            "2006-01-02 15:04",
            "2006-1-2 15:04",
            "2006/01/02 15:04",
            "2006/1/2 15:04",
            "2006年01月02日15:04",
            "2006年01月02日 15:04",
            "2006年1月2日 15:04",
            "2006年1月2日15:04",
            "2006年01月02日15:4",
            "2006年01月02日 15:4",
            "2006年1月2日 15:4",
            "2006年1月2日15:4",
            "2006-01-02  15:04",
            "  2006-01-02 15:04  ",
        ]
        for (const d of data) {
            const got = parseLocalDate(d);
            it(`"${d}"`, () => {
                expect(got).toEqual(want);
            });
        }
    })
    describe("YYYY-MM-DD", () => {
        const want = new Date("2006-01-02T00:00:00+08:00");
        const data = [
            "2006-01-02",
            "2006-1-2",
            "2006/01/02",
            "2006/1/2",
            "2006年01月02日",
            "2006年1月2日",
            "2006-01-02  ",
            "  2006-01-02  ",
        ]
        for (const d of data) {
            const got = parseLocalDate(d);
            it(`"${d}"`, () => {
                expect(got).toEqual(want);
            });
        }
    })
});

describe("formatChineseLocaleString", () => {
    it("Z+08:00", () => {
        const got = formatChineseISOLocaleString(new Date("2006-01-02T00:00:00+08:00"));
        expect(got).toEqual("2006-01-02 00:00:00");
    })
    it("Z", () => {
        const got = formatChineseISOLocaleString(new Date("2006-01-02T00:00:00Z"));
        expect(got).toEqual("2006-01-02 08:00:00");
    })
    it("Z-08:00", () => {
        const got = formatChineseISOLocaleString(new Date("2006-01-02T00:00:00-08:00"));
        expect(got).toEqual("2006-01-02 16:00:00");
    })
})
