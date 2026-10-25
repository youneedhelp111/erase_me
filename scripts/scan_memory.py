#!/usr/bin/env python3
"""erase-me 只读扫描器：列出本机 AI 助手可能保存"关于你"的文件，可选按关键词统计命中。

只读：不修改、不删除、不上传任何东西。只用标准库。

用法：
  python scan_memory.py                      # 列出所有已知位置
  python scan_memory.py -k 前任 -k 抑郁       # 统计关键词命中，并给出截断后的上下文
  python scan_memory.py --root /path/project  # 额外扫描某个项目目录里的 CLAUDE.md / AGENTS.md 等
  python scan_memory.py --json               # 输出 JSON，便于后续处理
"""
import argparse
import glob
import json
import os
import sys
from datetime import datetime

HOME = os.path.expanduser("~")

# (类别, glob 模式, 说明)。只列 agent 本地可读写的存储。
LOCATIONS = [
    ("memory", ".claude/CLAUDE.md", "Claude Code 全局指令/记忆"),
    ("memory", ".claude/projects/*/memory/*.md", "Claude Code 自动记忆文件"),
    ("history", ".claude/history.jsonl", "Claude Code 输入历史（你打过的话）"),
    ("transcript", ".claude/projects/*/*.jsonl", "Claude Code 会话记录"),
    ("trace", ".claude/todos/*", "Claude Code 待办残留"),
    ("trace", ".claude/shell-snapshots/*", "Claude Code shell 快照"),
    ("trace", ".claude/file-history/**/*", "Claude Code 文件编辑历史"),
    ("memory", ".codex/AGENTS.md", "Codex 全局指令/记忆"),
    ("memory", ".codex/memories/**/*", "Codex 记忆"),
    ("history", ".codex/history.jsonl", "Codex 输入历史"),
    ("transcript", ".codex/sessions/**/*.jsonl", "Codex 会话记录"),
    ("memory", ".gemini/GEMINI.md", "Gemini CLI 全局记忆"),
    ("memory", ".cursor/rules/**/*", "Cursor 规则"),
]

PROJECT_FILES = ["CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", "GEMINI.md", ".cursorrules"]

MAX_HITS_PER_FILE = 5
SNIPPET = 60  # 命中关键词前后各保留的字符数


def collect(root):
    found = []
    for cat, pattern, desc in LOCATIONS:
        for p in glob.glob(os.path.join(HOME, pattern), recursive=True):
            if os.path.isfile(p):
                found.append((cat, p, desc))
    if root:
        for name in PROJECT_FILES:
            p = os.path.join(root, name)
            if os.path.isfile(p):
                found.append(("memory", p, "项目级指令/记忆"))
    return found


def grep(path, keywords):
    hits = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for lineno, line in enumerate(f, 1):
                for kw in keywords:
                    i = line.find(kw)
                    if i >= 0:
                        s = line[max(0, i - SNIPPET): i + len(kw) + SNIPPET].strip()
                        hits.append({"line": lineno, "keyword": kw, "snippet": s})
                        break
                if len(hits) >= MAX_HITS_PER_FILE:
                    break
    except OSError as e:
        hits.append({"error": str(e)})
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-k", "--keyword", action="append", default=[], help="要查找的关键词，可重复")
    ap.add_argument("--root", help="额外扫描的项目目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    rows = []
    for cat, path, desc in collect(args.root):
        st = os.stat(path)
        row = {
            "category": cat,
            "path": path,
            "desc": desc,
            "bytes": st.st_size,
            "modified": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
        }
        if args.keyword:
            row["hits"] = grep(path, args.keyword)
            if not row["hits"]:
                continue
        rows.append(row)

    if args.json:
        json.dump(rows, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return

    if not rows:
        print("没有找到匹配的本地存储。")
        return
    for r in rows:
        print(f"[{r['category']}] {r['path']}  ({r['bytes']} B, {r['modified']})  {r['desc']}")
        for h in r.get("hits", []):
            if "error" in h:
                print(f"    ! {h['error']}")
            else:
                print(f"    L{h['line']} 「{h['keyword']}」 …{h['snippet']}…")


if __name__ == "__main__":
    main()
