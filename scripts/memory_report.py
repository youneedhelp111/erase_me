#!/usr/bin/env python3
"""erase-me 记忆对照表：分两次写入同一个 Excel 文件。只用标准库。

第一次（漂移开始前）写入原始记忆：
  echo '<JSON>' | python memory_report.py init --out ~/Desktop/记忆对照.xlsx
  JSON: [{"id": "m1", "category": "身份", "level": "无", "text": "用户叫李三"}, ...]

第二次（所有轮跑完后）写入修改后的记忆和核验结果：
  echo '<JSON>' | python memory_report.py finalize --out ~/Desktop/记忆对照.xlsx
  JSON: {"final": [{"id": "m1", "text": "用户叫林山", "action": "漂移"}, ...],
         "checks": [{"target": "出轨", "keyword": "外遇", "where": "记忆", "found": false}, ...]}

数据从标准输入读，不在磁盘上留中间文件。
设置环境变量 ERASE_ME_XLSX_PASSWORD 时，如果装了 msoffcrypto-tool 就加密文件；没装就提示用户在 Excel 里自己加密。
"""
import argparse
import io
import json
import os
import re
import sys
import zipfile
from datetime import datetime
from xml.sax.saxutils import escape

SHEETS_INIT = ["原始记忆"]
SHEETS_ALL = ["原始记忆", "修改后记忆", "对照", "核验"]


def col(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def sheet_xml(rows):
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
           '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>']
    for i, row in enumerate(rows, 1):
        cells = "".join(
            f'<c r="{col(j)}{i}" t="inlineStr"><is><t xml:space="preserve">{escape(str(v))}</t></is></c>'
            for j, v in enumerate(row, 1))
        out.append(f'<row r="{i}">{cells}</row>')
    out.append("</sheetData></worksheet>")
    return "".join(out)


def write_xlsx(path, sheets):
    names = list(sheets)
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
          '<Default Extension="xml" ContentType="application/xml"/>',
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>']
    ct += [f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
           for i in range(1, len(names) + 1)]
    ct.append("</Types>")
    wb = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>']
    wb += [f'<sheet name="{escape(n)}" sheetId="{i}" r:id="rId{i}"/>' for i, n in enumerate(names, 1)]
    wb.append("</sheets></workbook>")
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    rels += [f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
             f'Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(names) + 1)]
    rels.append("</Relationships>")
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
                 'Target="xl/workbook.xml"/></Relationships>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(ct))
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", "".join(wb))
        z.writestr("xl/_rels/workbook.xml.rels", "".join(rels))
        for i, n in enumerate(names, 1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(sheets[n]))
    return buf.getvalue()


def read_sheet1(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        xml = z.read("xl/worksheets/sheet1.xml").decode("utf-8")
    rows = []
    for row in re.findall(r"<row[^>]*>(.*?)</row>", xml):
        cells = re.findall(r"<t[^>]*>(.*?)</t>", row)
        rows.append([c.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&") for c in cells])
    return rows


def save(path, raw):
    pw = os.environ.get("ERASE_ME_XLSX_PASSWORD")
    if pw:
        try:
            import msoffcrypto  # noqa: F401
            from msoffcrypto.format.ooxml import OOXMLFile
            out = io.BytesIO()
            OOXMLFile(io.BytesIO(raw)).encrypt(pw, out)
            raw = out.getvalue()
            print("已加密。")
        except ImportError:
            print("未安装 msoffcrypto-tool，文件没有加密。请在 Excel 里：文件 → 信息 → 保护工作簿 → 用密码进行加密。")
    with open(path, "wb") as f:
        f.write(raw)


def load(path):
    with open(path, "rb") as f:
        raw = f.read()
    if raw[:2] == b"PK":
        return raw
    pw = os.environ.get("ERASE_ME_XLSX_PASSWORD")
    if not pw:
        sys.exit("文件已加密，请设置 ERASE_ME_XLSX_PASSWORD 后重试。")
    import msoffcrypto
    f = msoffcrypto.OfficeFile(io.BytesIO(raw))
    f.load_key(password=pw)
    out = io.BytesIO()
    f.decrypt(out)
    return out.getvalue()


def cmd_init(args, payload):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    rows = [["编号", "类别", "敏感级别", "原始内容", "写入时间"]]
    rows += [[m.get("id", ""), m.get("category", ""), m.get("level", ""), m.get("text", ""), now] for m in payload]
    save(args.out, write_xlsx(args.out, {"原始记忆": rows}))
    print(f"第一次写入完成：{args.out}（{len(payload)} 条原始记忆）")


def cmd_finalize(args, payload):
    orig = read_sheet1(load(args.out))
    if not orig or orig[0][:1] != ["编号"]:
        sys.exit("没找到第一次写入的原始记忆，请先运行 init。")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    final = {m["id"]: m for m in payload.get("final", [])}
    mod = [["编号", "修改后内容", "处理方式", "写入时间"]]
    mod += [[k, v.get("text", ""), v.get("action", ""), now] for k, v in final.items()]
    cmp_rows = [["编号", "类别", "敏感级别", "原始内容", "修改后内容", "处理方式"]]
    seen = set()
    for r in orig[1:]:
        r = (r + [""] * 5)[:5]
        m = final.get(r[0])
        seen.add(r[0])
        cmp_rows.append([r[0], r[1], r[2], r[3], m.get("text", "") if m else "（已删除）",
                         m.get("action", "") if m else "删除"])
    for k, v in final.items():
        if k not in seen:
            cmp_rows.append([k, "", "", "（新增）", v.get("text", ""), v.get("action", "新增")])
    chk = [["重点内容", "检查词", "检查位置", "结果"]]
    for c in payload.get("checks", []):
        chk.append([c.get("target", ""), c.get("keyword", ""), c.get("where", ""),
                    "仍有残留" if c.get("found") else "已清除"])
    sheets = {"原始记忆": orig, "修改后记忆": mod, "对照": cmp_rows, "核验": chk}
    save(args.out, write_xlsx(args.out, sheets))
    left = sum(1 for c in payload.get("checks", []) if c.get("found"))
    print(f"第二次写入完成：{args.out}（核验 {len(chk) - 1} 项，残留 {left} 项）")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["init", "finalize"])
    ap.add_argument("--out", required=True, help="Excel 文件路径，由用户决定")
    args = ap.parse_args()
    args.out = os.path.expanduser(args.out)
    # utf-8-sig：PowerShell 管道会带 BOM
    payload = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
    (cmd_init if args.step == "init" else cmd_finalize)(args, payload)


if __name__ == "__main__":
    main()
