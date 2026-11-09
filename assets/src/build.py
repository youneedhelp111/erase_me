"""Build the README promo images for erase-me.skill.

Writes one HTML file per image and language into this folder, then renders
each to a PNG in ../ with a headless browser (Playwright).

    python assets/src/build.py            # build HTML + PNG
    python assets/src/build.py --html     # HTML only

Rendering uses Playwright's Chromium if installed, otherwise a local
Chrome or Edge.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent

ACCENT = "#D4532B"

HEAD = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    width: {w}px; height: {h}px; background: #111111; overflow: hidden;
    font-family: 'Inter', 'Noto Sans SC', 'Microsoft YaHei', 'PingFang SC', sans-serif;
    color: #FFFFFF; -webkit-font-smoothing: antialiased;
  }}
  .label {{ color: {accent}; font-size: 11px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; }}
  .label .sub {{ color: #666; font-weight: 600; letter-spacing: 0.5px; text-transform: none; margin-left: 14px; font-size: 12px; }}
  .foot {{ position: absolute; bottom: 22px; left: 48px; right: 48px; display: flex; justify-content: space-between;
          font-size: 10px; font-weight: 600; letter-spacing: 1px; color: #3a3a3a; }}
  .redact {{ display: inline-block; background: #3a3a3a; height: 0.95em; vertical-align: -0.12em; border-radius: 1px; }}
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""

# ---------------------------------------------------------------- copy ---
T = {
    "zh": {
        "lang": "zh-CN",
        "foot_r": "AI 记忆隐私清理",
        # hero
        "hero_cat": "AGENT SKILL · AI MEMORY PRIVACY",
        "hero_sub": "让 AI 忘掉你",
        "hero_tag": "不删记录，只把细节磨平。",
        "hero_data": [("只改不删", ""), ("只概括不编造", ""), ("确认才动手", ""), ("MIT", " 开源")],
        "hero_foot": "说过的话收不回来，但可以让它变得不再具体。",
        "hero_entry": "MEMORY · m6",
        "hero_before": '三天前深夜咨询过 <span class="redact" style="width:62px"></span> 的问题，还说了起因 <span class="redact" style="width:46px"></span>',
        "hero_after": "咨询过一个健康方面的问题",
        "hero_removed": ["病种", "起因", "时间"],
        "hero_rw": "REWRITE · 往上概括",
        # rewrite
        "rw_title": "BEFORE → AFTER",
        "rw_sub": "改写只往上概括，留下的每一句都还是真的",
        "rw_h": ("改写前 · 只在你本机的对照表里", "改写后 · AI 记住的", "去掉了"),
        "rw_rows": [
            ('三天前深夜咨询过 <span class="redact" style="width:58px"></span> 检测，还说了起因', "咨询过一个健康方面的问题", ["病种", "起因", "时间"]),
            ("一天前偷偷查过伴侣手机，不信任 ta", "因为生活琐事，对 ta 有意见", ["行为", "时间"]),
            ("焦虑型性格，容易反复确认", "做事比较仔细", ["心理标签"]),
            ("年薪约 30 万", "有工作收入", ["具体金额"]),
        ],
        "rw_rule_ok": "“咨询过一个健康问题”",
        "rw_rule_bad": "“咨询过感冒”",
        "rw_rule": "不新增原文没有的事实：{ok} ✓ &nbsp;&nbsp; {bad} ✗ 那是编的",
        # workflow
        "wf_title": "WORKFLOW · 7 STEPS",
        "wf_steps": [
            ("01", "ASK", "问清需求"),
            ("02", "CHECK", "判断在哪里跑"),
            ("03", "READ", "只读 · 列清单定级"),
            ("04", "PLAN", "写改写方案"),
            ("05", "REWRITE", "更新，不删除"),
            ("06", "DILUTE", "中性话题稀释"),
            ("07", "VERIFY", "关键词核验"),
        ],
        "wf_d1": ("你说", "“确认”?"),
        "wf_d2": ("有残留?", ""),
        "wf_no1": "改选 → 重出方案",
        "wf_yes": "YES",
        "wf_no": "NO",
        "wf_loop": "有残留 · 再概括一层，重新改写",
        "wf_done": ("DONE", "对照表 · 报告"),
        "wf_stop": "STOP",
        "wf_note6": "每批 5–10 轮 · 你发“继续”",
        "wf_note1": "范围 · 轮数 · 对照表",
        "wf_foot": "两个检查点：问题答完才继续；你说“确认”才动手",
        # dilution
        "dl_label": "DILUTION ≠ DELETION",
        "dl_title": "稀释不是删除",
        "dl_body": "erase-me 能做的是改写记忆条目、冲淡上下文，效果只能尽量。平台最终记住什么，由平台决定。",
        "dl_chart": "账号记忆的构成",
        "dl_illus": "示意",
        "dl_bars": ["改写前", "改写后", "稀释后"],
        "dl_leg": ["具体细节", "笼统说法", "中性话题"],
        "dl_lever": ("改写才是主力", "平台有记忆编辑工具时，敏感条目一次就改完，稀释只是补充，建议 0–5 轮就够。"),
        "dl_still": "仍然存在",
        "dl_still_items": ["服务器日志", "备份", "你没删的聊天记录", "聊天标题本身"],
        "dl_real": "要彻底删除",
        "dl_real_body": "去平台设置里删聊天、删记忆，或按服务商隐私政策申请。",
    },
    "en": {
        "lang": "en",
        "foot_r": "AI MEMORY PRIVACY CLEANUP",
        "hero_cat": "AGENT SKILL · AI MEMORY PRIVACY",
        "hero_sub": "Make your AI forget you",
        "hero_tag": "No deleting, just sanding the details off.",
        "hero_data": [("Rewrite", ", never delete"), ("Generalize", ", never invent"), ("Confirm", " first"), ("MIT", "")],
        "hero_foot": "You can't take back what you said, but you can make it less specific.",
        "hero_entry": "MEMORY · m6",
        "hero_before": 'Asked late at night about <span class="redact" style="width:58px"></span> testing, and said why <span class="redact" style="width:46px"></span>',
        "hero_after": "Asked a health-related question",
        "hero_removed": ["condition", "reason", "time"],
        "hero_rw": "REWRITE · GENERALIZE",
        "rw_title": "BEFORE → AFTER",
        "rw_sub": "Rewrites only generalize. Every sentence that stays is still true.",
        "rw_h": ("Before · only in your local sheet", "After · what the AI remembers", "Removed"),
        "rw_rows": [
            ('Asked late at night about <span class="redact" style="width:54px"></span> testing, and said why', "Asked a health-related question", ["condition", "reason", "time"]),
            ("Secretly checked partner's phone a day ago", "Has some issues with them over everyday things", ["action", "time"]),
            ("Anxious personality, keeps double-checking", "Fairly careful", ["psych label"]),
            ("Earns about 300k a year", "Has a work income", ["amount"]),
        ],
        "rw_rule_ok": "“asked a health question”",
        "rw_rule_bad": "“asked about a cold”",
        "rw_rule": "Adds no new facts: {ok} ✓ &nbsp;&nbsp; {bad} ✗ that's made up",
        "wf_title": "WORKFLOW · 7 STEPS",
        "wf_steps": [
            ("01", "ASK", "scope · rounds · sheet"),
            ("02", "CHECK", "where it runs"),
            ("03", "READ", "read-only · rate"),
            ("04", "PLAN", "rewrite plan"),
            ("05", "REWRITE", "update, never delete"),
            ("06", "DILUTE", "neutral topics"),
            ("07", "VERIFY", "keyword check"),
        ],
        "wf_d1": ("YOU SAY", "“CONFIRM”?"),
        "wf_d2": ("RESIDUE?", ""),
        "wf_no1": "change picks → new plan",
        "wf_yes": "YES",
        "wf_no": "NO",
        "wf_loop": "Residue found · generalize one more level and rewrite",
        "wf_done": ("DONE", "sheet · report"),
        "wf_stop": "STOP",
        "wf_note6": "5–10 rounds per reply · you say “continue”",
        "wf_note1": "",
        "wf_foot": "Two checkpoints: questions answered first; nothing changes until you say “confirm”",
        "dl_label": "DILUTION ≠ DELETION",
        "dl_title": "Dilution is not deletion",
        "dl_body": "erase-me rewrites memory entries and dilutes context. It does its best, with no guarantee. The platform decides what it finally remembers.",
        "dl_chart": "Account memory",
        "dl_illus": "illustrative",
        "dl_bars": ["Before", "Rewritten", "Diluted"],
        "dl_leg": ["specific details", "vague statements", "neutral topics"],
        "dl_lever": ("Rewriting does the heavy lifting", "With a memory editing tool, sensitive entries are fixed in one pass. Dilution is extra: 0–5 rounds is usually enough."),
        "dl_still": "Still there",
        "dl_still_items": ["Server logs", "Backups", "Chats you haven't deleted", "Chat titles themselves"],
        "dl_real": "For real deletion",
        "dl_real_body": "Delete chats and memories in the platform's settings, or file a request under the provider's privacy policy.",
    },
}


def page(t, title, w, h, css, body):
    return HEAD.format(lang=t["lang"], title=title, w=w, h=h, css=css, body=body, accent=ACCENT)


def foot(t, left="erase-me.skill"):
    return f'<div class="foot"><span>{left}</span><span>{t["foot_r"]}</span></div>'


# ---------------------------------------------------------------- hero ---
def hero(t):
    css = f"""
  .rule-v {{ position:absolute; left:60px; top:48px; width:3px; height:304px; background:{ACCENT}; }}
  .rule-t {{ position:absolute; left:60px; top:48px; width:740px; height:2px; background:rgba(255,255,255,.15); }}
  .rule-b {{ position:absolute; left:60px; top:350px; width:740px; height:1px; background:rgba(255,255,255,.15); }}
  .left {{ position:absolute; left:84px; top:68px; width:720px; }}
  h1 {{ font-size:84px; font-weight:900; letter-spacing:-2px; line-height:1; margin-top:18px; }}
  h1 em {{ font-style:normal; color:{ACCENT}; }}
  .cap {{ font-size:13px; font-weight:500; letter-spacing:4px; color:#888; margin-top:12px; }}
  .sub {{ font-size:24px; font-weight:700; margin-top:18px; }}
  .tag {{ font-size:15px; color:#AAA; margin-top:8px; }}
  .data {{ font-size:14px; color:#AAA; margin-top:16px; }}
  .data b {{ color:{ACCENT}; font-weight:700; }}
  .data i {{ font-style:normal; color:#555; margin:0 8px; }}
  .hfoot {{ position:absolute; left:84px; top:362px; font-size:12px; color:#666; letter-spacing:.3px; }}
  .right {{ position:absolute; left:850px; top:76px; width:300px; }}
  .divider {{ position:absolute; left:828px; top:110px; width:1px; height:220px; background:rgba(255,255,255,.08); }}
  .card-b {{ margin-top:18px; border:1px dashed #444; padding:14px 16px; font-size:13px; line-height:1.8; color:#777; text-decoration:line-through; text-decoration-color:rgba(212,83,43,.6); }}
  .arrow {{ height:38px; position:relative; }}
  .arrow:before {{ content:''; position:absolute; left:28px; top:6px; width:2px; height:20px; background:{ACCENT}; }}
  .arrow:after {{ content:''; position:absolute; left:23px; top:24px; border:6px solid transparent; border-top:8px solid {ACCENT}; }}
  .arrow span {{ position:absolute; left:48px; top:10px; font-size:10px; font-weight:700; letter-spacing:2px; color:{ACCENT}; }}
  .card-a {{ background:#FFF; color:#111; padding:16px; font-size:15px; font-weight:800; }}
  .chips {{ margin-top:14px; display:flex; gap:8px; }}
  .chip {{ font-size:11px; font-weight:700; color:{ACCENT}; border:1px solid rgba(212,83,43,.6); padding:3px 8px; }}
"""
    data = '<i>·</i>'.join(f"<b>{a}</b>{b}" for a, b in t["hero_data"])
    chips = "".join(f'<span class="chip">− {c}</span>' for c in t["hero_removed"])
    body = f"""
<div class="rule-v"></div><div class="rule-t"></div><div class="rule-b"></div>
<div class="left">
  <div class="label">{t["hero_cat"]}</div>
  <h1>erase-me<em>.</em>skill</h1>
  <div class="cap">ERASE · ME</div>
  <div class="sub">{t["hero_sub"]}</div>
  <div class="tag">{t["hero_tag"]}</div>
  <div class="data">{data}</div>
</div>
<div class="hfoot">{t["hero_foot"]}</div>
<div class="divider"></div>
<div class="right">
  <div class="label">{t["hero_entry"]}</div>
  <div class="card-b">{t["hero_before"]}</div>
  <div class="arrow"><span>{t["hero_rw"]}</span></div>
  <div class="card-a">{t["hero_after"]}</div>
  <div class="chips">{chips}</div>
</div>
"""
    return page(t, "erase-me.skill hero", 1200, 400, css, body), (1200, 400)


# ------------------------------------------------------------- rewrite ---
def rewrite(t):
    css = f"""
  .wrap {{ position:absolute; left:48px; top:44px; right:48px; }}
  .head, .row {{ display:grid; grid-template-columns: 430px 56px 380px 1fr; align-items:stretch; }}
  .head {{ margin-top:34px; font-size:10px; font-weight:700; letter-spacing:1.5px; color:#555; text-transform:uppercase; }}
  .head div {{ padding-bottom:10px; }}
  .row {{ margin-top:14px; }}
  .b {{ border:1px dashed #3a3a3a; padding:0 18px; height:62px; display:flex; align-items:center; font-size:14px; color:#777;
        text-decoration:line-through; text-decoration-color:rgba(212,83,43,.55); }}
  .ar {{ display:flex; align-items:center; justify-content:center; }}
  .ar svg {{ display:block; }}
  .a {{ background:#FFF; color:#111; padding:0 18px; height:62px; display:flex; align-items:center; font-size:15px; font-weight:800; }}
  .rm {{ display:flex; align-items:center; gap:6px; flex-wrap:wrap; padding-left:20px; }}
  .chip {{ font-size:11px; font-weight:700; color:{ACCENT}; border:1px solid rgba(212,83,43,.6); padding:3px 8px; white-space:nowrap; }}
  .rule {{ margin-top:30px; font-size:13px; color:#888; }}
  .rule b {{ color:#DDD; font-weight:700; }}
  .rule s {{ color:#888; text-decoration-color:{ACCENT}; }}
"""
    arrow = f'<svg width="40" height="12"><line x1="2" y1="6" x2="30" y2="6" stroke="{ACCENT}" stroke-width="2"/><polygon points="28,0 40,6 28,12" fill="{ACCENT}"/></svg>'
    rows = ""
    for before, after, removed in t["rw_rows"]:
        chips = "".join(f'<span class="chip">− {c}</span>' for c in removed)
        rows += f'<div class="row"><div class="b">{before}</div><div class="ar">{arrow}</div><div class="a">{after}</div><div class="rm">{chips}</div></div>'
    h1, h2, h3 = t["rw_h"]
    rule = t["rw_rule"].format(ok=f'<b>{t["rw_rule_ok"]}</b>', bad=f'<s>{t["rw_rule_bad"]}</s>')
    body = f"""
<div class="wrap">
  <div class="label">{t["rw_title"]}<span class="sub">{t["rw_sub"]}</span></div>
  <div class="head"><div>{h1}</div><div></div><div>{h2}</div><div style="padding-left:20px">{h3}</div></div>
  {rows}
  <div class="rule">{rule}</div>
</div>
{foot(t)}
"""
    return page(t, "erase-me.skill before/after", 1200, 520, css, body), (1200, 520)


# ------------------------------------------------------------ workflow ---
def workflow(t):
    W, H = 1200, 540
    s = t["wf_steps"]
    F = "Inter, 'Noto Sans SC', 'Microsoft YaHei', sans-serif"

    def block(x, y, num, title, sub, fill="#FFFFFF", fg="#111111", sfg="#555555", w=150):
        cx = x + w / 2
        return (f'<text x="{x}" y="{y-9}" fill="{ACCENT}" font-family="{F}" font-size="10" font-weight="700">{num}</text>'
                f'<rect x="{x}" y="{y}" width="{w}" height="70" fill="{fill}"/>'
                f'<text x="{cx}" y="{y+32}" fill="{fg}" font-family="{F}" font-size="13" font-weight="800" text-anchor="middle" letter-spacing="0.5">{title}</text>'
                f'<text x="{cx}" y="{y+50}" fill="{sfg}" font-family="{F}" font-size="11" font-weight="600" text-anchor="middle">{sub}</text>')

    def harrow(x1, x2, y):
        return f'<line x1="{x1}" y1="{y}" x2="{x2-6}" y2="{y}" stroke="{ACCENT}" stroke-width="2" marker-end="url(#ao)"/>'

    def stop(x, y):
        return (f'<rect x="{x}" y="{y}" width="40" height="16" fill="none" stroke="{ACCENT}" stroke-width="1"/>'
                f'<text x="{x+20}" y="{y+11.5}" fill="{ACCENT}" font-family="{F}" font-size="9" font-weight="800" text-anchor="middle" letter-spacing="1.5">{t["wf_stop"]}</text>')

    y1, y2 = 150, 340
    xs = [48, 238, 428, 618]
    out = []
    for i, x in enumerate(xs):
        n, ti, su = s[i]
        out.append(block(x, y1, n, ti, su))
        if i < 3:
            out.append(harrow(x + 150, xs[i + 1], y1 + 35))
    # step-1 checkpoint
    out.append(stop(48 + 110, y1 - 22))
    # diamond 1
    dx, dy = 880, y1 + 35
    out.append(harrow(768, dx - 58, dy))
    out.append(f'<polygon points="{dx},{dy-56} {dx+56},{dy} {dx},{dy+56} {dx-56},{dy}" fill="{ACCENT}"/>')
    out.append(f'<text x="{dx}" y="{dy-3}" fill="#FFF" font-family="{F}" font-size="11" font-weight="800" text-anchor="middle">{t["wf_d1"][0]}</text>')
    out.append(f'<text x="{dx}" y="{dy+13}" fill="#FFF" font-family="{F}" font-size="11" font-weight="800" text-anchor="middle">{t["wf_d1"][1]}</text>')
    out.append(stop(dx + 30, dy - 72))
    # NO -> back to PLAN
    out.append(f'<path d="M{dx},{dy-56} L{dx},{y1-50} L693,{y1-50} L693,{y1-6}" stroke="#888" stroke-width="1.5" fill="none" stroke-dasharray="5,4" marker-end="url(#ag)"/>')
    out.append(f'<text x="786" y="{y1-58}" fill="#888" font-family="{F}" font-size="10" font-weight="700" text-anchor="middle" letter-spacing="1">{t["wf_no"]} · {t["wf_no1"]}</text>')
    # YES -> row 2
    yy = dy + 56
    out.append(f'<path d="M{dx},{yy} L{dx},{y2-50} L123,{y2-50} L123,{y2-6}" stroke="#2B8A3E" stroke-width="2" fill="none" marker-end="url(#agr)"/>')
    out.append(f'<text x="{dx+10}" y="{y2-58}" fill="#2B8A3E" font-family="{F}" font-size="10" font-weight="700" letter-spacing="1">{t["wf_yes"]}</text>')
    # row 2
    xs2 = [48, 238, 428]
    for i, x in enumerate(xs2):
        n, ti, su = s[4 + i]
        out.append(block(x, y2, n, ti, su))
        if i < 2:
            out.append(harrow(x + 150, xs2[i + 1], y2 + 35))
    # diamond 2
    ex, ey = 690, y2 + 35
    out.append(harrow(578, ex - 50, ey))
    out.append(f'<polygon points="{ex},{ey-50} {ex+50},{ey} {ex},{ey+50} {ex-50},{ey}" fill="#2a2a2a" stroke="{ACCENT}" stroke-width="2"/>')
    out.append(f'<text x="{ex}" y="{ey+4}" fill="#FFF" font-family="{F}" font-size="11" font-weight="800" text-anchor="middle">{t["wf_d2"][0]}</text>')
    # residue loop back to REWRITE
    out.append(f'<path d="M{ex},{ey+50} L{ex},{y2+118} L123,{y2+118} L123,{y2+76}" stroke="#C92A2A" stroke-width="2" fill="none" stroke-dasharray="6,4" marker-end="url(#ar)"/>')
    out.append(f'<text x="406" y="{y2+136}" fill="#C92A2A" font-family="{F}" font-size="10" font-weight="700" text-anchor="middle" letter-spacing="1">{t["wf_yes"]} · {t["wf_loop"]}</text>')
    # NO -> DONE
    out.append(f'<line x1="{ex+50}" y1="{ey}" x2="{850-6}" y2="{ey}" stroke="#2B8A3E" stroke-width="2" marker-end="url(#agr)"/>')
    out.append(f'<text x="{(ex+50+850)/2}" y="{ey-8}" fill="#2B8A3E" font-family="{F}" font-size="10" font-weight="700" text-anchor="middle" letter-spacing="1">{t["wf_no"]}</text>')
    out.append(block(850, y2, "", t["wf_done"][0], t["wf_done"][1], fill="#2B8A3E", fg="#FFF", sfg="rgba(255,255,255,.8)"))
    # step 6 note
    out.append(f'<text x="313" y="{y2+90}" fill="#777" font-family="{F}" font-size="10" font-weight="600" text-anchor="middle">{t["wf_note6"]}</text>')
    if t["wf_note1"]:
        out.append(f'<text x="123" y="{y1+90}" fill="#777" font-family="{F}" font-size="10" font-weight="600" text-anchor="middle">{t["wf_note1"]}</text>')

    svg = f"""<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
<defs>
<marker id="ao" markerWidth="10" markerHeight="8" refX="2" refY="4" orient="auto"><polygon points="0 0, 10 4, 0 8" fill="{ACCENT}"/></marker>
<marker id="ag" markerWidth="10" markerHeight="8" refX="2" refY="4" orient="auto"><polygon points="0 0, 10 4, 0 8" fill="#888"/></marker>
<marker id="agr" markerWidth="10" markerHeight="8" refX="2" refY="4" orient="auto"><polygon points="0 0, 10 4, 0 8" fill="#2B8A3E"/></marker>
<marker id="ar" markerWidth="10" markerHeight="8" refX="2" refY="4" orient="auto"><polygon points="0 0, 10 4, 0 8" fill="#C92A2A"/></marker>
</defs>
<rect width="{W}" height="{H}" fill="#111"/>
{''.join(out)}
</svg>"""
    css = """
  svg { position:absolute; left:0; top:0; }
  .top { position:absolute; left:48px; top:44px; z-index:2; }
"""
    body = f'{svg}<div class="top label">{t["wf_title"]}<span class="sub">{t["wf_foot"]}</span></div>{foot(t)}'
    return page(t, "erase-me.skill workflow", W, H, css, body), (W, H)


# ------------------------------------------------------------ dilution ---
def dilution(t):
    css = f"""
  .l {{ position:absolute; left:48px; top:44px; width:400px; }}
  .l h2 {{ font-size:46px; font-weight:900; letter-spacing:-1px; line-height:1.1; margin-top:26px; }}
  .l h2 span {{ color:{ACCENT}; }}
  .l p {{ font-size:14px; line-height:1.75; color:#999; margin-top:22px; }}
  .lever {{ margin-top:26px; border-left:3px solid {ACCENT}; padding:4px 0 4px 16px; font-size:13px; line-height:1.7; color:#BBB; }}
  .lever b {{ display:block; color:#FFF; font-size:14px; }}
  .m {{ position:absolute; left:500px; top:44px; width:300px; }}
  .m .t {{ font-size:12px; font-weight:700; color:#DDD; margin-top:0; }}
  .m .t i {{ font-style:normal; color:#555; font-weight:600; margin-left:8px; font-size:10px; letter-spacing:1px; text-transform:uppercase; }}
  .bars {{ display:flex; gap:34px; margin-top:22px; align-items:flex-end; }}
  .bar {{ width:62px; height:220px; display:flex; flex-direction:column-reverse; }}
  .bar div {{ width:100%; }}
  .lab {{ display:flex; gap:34px; margin-top:10px; }}
  .lab span {{ width:62px; text-align:center; font-size:11px; font-weight:600; color:#777; }}
  .leg {{ margin-top:18px; display:flex; flex-direction:column; gap:6px; font-size:11px; color:#888; }}
  .leg span:before {{ content:''; display:inline-block; width:10px; height:10px; margin-right:8px; vertical-align:-1px; background:var(--c); }}
  .vr {{ position:absolute; left:842px; top:60px; width:1px; height:340px; background:rgba(255,255,255,.08); }}
  .r {{ position:absolute; left:876px; top:44px; width:280px; }}
  .r ul {{ list-style:none; margin-top:18px; }}
  .r li {{ font-size:15px; font-weight:700; padding:11px 0; border-bottom:1px solid #222; display:flex; align-items:center; gap:12px; }}
  .r li:before {{ content:'●'; color:#C92A2A; font-size:9px; }}
  .real {{ margin-top:26px; background:#FFF; color:#111; padding:16px 18px; }}
  .real b {{ display:block; font-size:12px; font-weight:800; letter-spacing:1px; color:{ACCENT}; text-transform:uppercase; }}
  .real div {{ font-size:13px; font-weight:600; line-height:1.6; margin-top:6px; }}
"""
    C_DET, C_GEN, C_NEU = ACCENT, "#FFFFFF", "#3a3a3a"
    # illustrative shares, bottom to top
    comp = [
        [(C_DET, 55), (C_NEU, 45)],
        [(C_GEN, 55), (C_NEU, 45)],
        [(C_GEN, 25), (C_NEU, 75)],
    ]
    bars = ""
    for parts in comp:
        segs = "".join(f'<div style="height:{p}%;background:{c};border-top:2px solid #111"></div>' for c, p in parts)
        bars += f'<div class="bar">{segs}</div>'
    labs = "".join(f"<span>{b}</span>" for b in t["dl_bars"])
    leg = "".join(f'<span style="--c:{c}">{n}</span>' for c, n in zip([C_DET, C_GEN, C_NEU], t["dl_leg"]))
    items = "".join(f"<li>{x}</li>" for x in t["dl_still_items"])
    title = t["dl_title"]
    body = f"""
<div class="l">
  <div class="label">{t["dl_label"]}</div>
  <h2>{title}<span>.</span></h2>
  <p>{t["dl_body"]}</p>
  <div class="lever"><b>{t["dl_lever"][0]}</b>{t["dl_lever"][1]}</div>
</div>
<div class="m">
  <div class="label">{t["dl_chart"]}<span class="sub" style="font-size:10px;letter-spacing:1px;text-transform:uppercase">{t["dl_illus"]}</span></div>
  <div class="bars">{bars}</div>
  <div class="lab">{labs}</div>
  <div class="leg">{leg}</div>
</div>
<div class="vr"></div>
<div class="r">
  <div class="label" style="color:#C92A2A">{t["dl_still"]}</div>
  <ul>{items}</ul>
  <div class="real"><b>{t["dl_real"]}</b><div>{t["dl_real_body"]}</div></div>
</div>
{foot(t)}
"""
    return page(t, "erase-me.skill dilution", 1200, 480, css, body), (1200, 480)


PAGES = {"hero": hero, "rewrite": rewrite, "workflow": workflow, "dilution": dilution}


def main():
    jobs = []
    for lang in ("zh", "en"):
        for name, fn in PAGES.items():
            html, size = fn(T[lang])
            stem = name if lang == "zh" else f"{name}-en"
            p = HERE / f"{stem}.html"
            p.write_text(html, encoding="utf-8")
            jobs.append((p, OUT / f"{stem}.png", size))
    if "--html" in sys.argv:
        return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = None
        for kw in ({}, {"channel": "chrome"}, {"channel": "msedge"}):
            try:
                browser = pw.chromium.launch(**kw)
                break
            except Exception:
                continue
        if browser is None:
            sys.exit("No Chromium/Chrome/Edge found for Playwright")
        for src, dst, (w, h) in jobs:
            pg = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            pg.goto(src.as_uri())
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            pg.screenshot(path=str(dst), clip={"x": 0, "y": 0, "width": w, "height": h})
            pg.close()
            print("wrote", dst.name)
        browser.close()


if __name__ == "__main__":
    main()
