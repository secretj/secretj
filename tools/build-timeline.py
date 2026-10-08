#!/usr/bin/env python3
"""assets/timeline.svg 를 만든다.

해마다 무엇이 쌓였는지 보여 주는 애니메이션 SVG 를 생성한다.
로고 path 는 simple-icons 에서 내려받아 tools/icons 에 캐시한 뒤 단색으로 다시 칠한다.
연도와 문구를 고치려면 아래 YEARS 만 손대면 된다.

    python3 tools/build-timeline.py                  # assets/timeline.svg 로 출력
    python3 tools/build-timeline.py out.svg          # 다른 경로로 출력
    python3 tools/build-timeline.py --icon-dir DIR   # 로고 캐시 폴더 지정
"""

import argparse
import json
import os
import re
import sys
import urllib.request

# ── 색 ─────────────────────────────────────────────────────────────────────
# 밝은 테마와 어두운 테마 양쪽에서 읽히는 중간 회색을 기본으로 쓴다.
BASE = "#8b94a3"

# 해마다 색을 달리한다. 앞이 글자용(조금 진한 쪽), 뒤가 점과 로고용(연한 쪽).
# 흰 배경과 #0d1117 양쪽에서 읽히도록 중간 밝기로 잡았다.
TONES = [
    ("#5a9ee6", "#8fc2f2"),   # 하늘
    ("#8d7ce8", "#b3a6f0"),   # 라벤더
    ("#3bb49c", "#7ad3bf"),   # 민트
    ("#e2904e", "#f0b583"),   # 살구
    ("#e07aa0", "#f0a6c0"),   # 로즈
    ("#a96fe0", "#c7a3ef"),   # 보라
    ("#95a0ad", "#b3bcc7"),   # 마지막 칸은 색을 빼 둔다
]

CDN = "https://cdn.jsdelivr.net/npm/simple-icons@13/icons/{}.svg"

ICONS = [
    "openjdk", "html5", "javascript", "spring", "dotnet",
    "php", "codeigniter", "redis", "elasticsearch",
    "anthropic", "python", "kotlin", "react", "typescript",
]


def load_grass(path):
    """연도별 잔디를 읽는다. tools/fetch-contributions.py 로 다시 받을 수 있다."""
    with open(path) as f:
        return json.load(f)


def load_icons(icon_dir):
    """로고 path 를 {이름: d} 로 돌려준다. 캐시가 없으면 내려받는다."""
    os.makedirs(icon_dir, exist_ok=True)
    out = {}
    for name in ICONS:
        path = os.path.join(icon_dir, name + ".svg")
        if not os.path.exists(path):
            with urllib.request.urlopen(CDN.format(name), timeout=20) as r:
                body = r.read().decode()
            with open(path, "w") as f:
                f.write(body)
        else:
            body = open(path).read()
        ds = re.findall(r'<path d="([^"]+)"', body)
        if not ds:
            sys.exit("로고 path 를 찾지 못했다: " + name)
        out[name] = " ".join(ds)
    return out

# ── 조각 ───────────────────────────────────────────────────────────────────
def logo(ic, name, cx, cy, size, cls="lg"):
    """simple-icons 로고를 (cx, cy) 중심으로 size 만큼 놓는다."""
    s = size / 24.0
    x, y = cx - size / 2, cy - size / 2
    return (f'<g class="{cls}" transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">'
            f'<path d="{ic[name]}"/></g>')

def text(x, y, body, cls="t", anchor="middle"):
    """라벨. 글꼴은 시스템 기본만 쓴다 (GitHub 는 외부 글꼴을 받지 않는다)."""
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{body}</text>'


def chip(cx, cy, label, cls="chip"):
    """로고가 없는 것은 글자 칩으로 둔다."""
    w = len(label) * 7.4 + 16
    return (f'<g><rect class="{cls}" x="{cx - w / 2:.1f}" y="{cy - 9}" width="{w:.1f}"'
            f' height="18" rx="9"/>'
            f'<text class="chip-t" x="{cx}" y="{cy + 4}" text-anchor="middle">{label}</text></g>')


# 해마다 무엇이 쌓였는지. 로고 이름이거나 ("칩", 글자) 이다.
YEARS = [
    ("2021", ["자바로 시작", "부트캠프에서 웹 전반"],
     ["openjdk", "html5", "javascript", "spring"]),
    ("2022", ["개발자로 일 시작", "C# 과 Java"],
     [("칩", "C#"), "dotnet"]),
    ("2023", ["PHP 환경으로 이직", "프레임워크 버전업", "SSR → CSR"],
     ["php", "codeigniter", "redis", "elasticsearch"]),
    ("2024", ["게시판 · 메일 API", "기능 개발과 장애 대응", "커밋 1,796"], []),
    ("2025", ["코딩 표준 · 에러 통합", "2단계 인증, 속도 개선", "Cursor 를 쓰기 시작"],
     [("칩", "Cursor")]),
    ("2026", ["Claude Code 로", "혼자 만들어 운영"],
     ["anthropic", "python", "kotlin", "react", "typescript"]),
    ("?", ["다음엔", "무엇을 쌓게 될까?"], []),
]


# 잔디 격자. 칸 하나는 CELL, 칸 사이는 GAP 만큼 띄운다.
CELL, GAP = 11, 2
GRASS_X, GRASS_Y = 96, 170


def level(count):
    """하루 커밋 수를 네 단계로 나눈다. 해마다 양이 달라 기준은 고정한다."""
    if count == 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 10:
        return 3
    return 4


def cells(weeks, want):
    """같은 단계인 칸들을 path 하나로 묶는다. rect 를 수백 개 쓰지 않으려는 것이다."""
    d = []
    for wi, col in enumerate(weeks):
        for day, c in enumerate(col):
            if level(c) != want:
                continue
            x = GRASS_X + wi * (CELL + GAP)
            y = GRASS_Y + day * (CELL + GAP)
            d.append(f"M{x},{y}h{CELL}v{CELL}h-{CELL}z")
    return "".join(d)


def build_timeline(ic, grass):
    """위에 연표, 가운데 그해 잔디, 아래에 그때까지 쌓인 것을 둔다."""
    W2, H2 = 880, 336
    DUR = 6
    cols = [56 + i * 122 for i in range(7)]
    axis_y, p, kf = 74, [], []

    stops = "".join(
        f'<stop offset="{i / (len(TONES) - 1) * 100:.0f}%" stop-color="{t[1]}"/>'
        for i, t in enumerate(TONES))
    p.append(f'<defs><linearGradient id="ax" x1="0" y1="0" x2="1" y2="0">{stops}'
             f'</linearGradient></defs>')
    p.append(f'<path d="M34,{axis_y} H846" fill="none" stroke="url(#ax)"'
             f' stroke-opacity=".8" stroke-width="2" stroke-linecap="round"/>')

    for i, (year, lines, _) in enumerate(YEARS):
        cx = cols[i]
        last = i == len(YEARS) - 1
        ink, soft = TONES[i]
        g = [f'<text class="yr" x="{cx}" y="52" text-anchor="middle"'
             f' fill="{ink}">{year}</text>']
        if last:
            g.append(f'<circle class="node-q" cx="{cx}" cy="{axis_y}" r="7"/>')
        else:
            g.append(f'<circle cx="{cx}" cy="{axis_y}" r="11" fill="{soft}"'
                     f' fill-opacity=".22"/>')
            g.append(f'<circle cx="{cx}" cy="{axis_y}" r="5" fill="{soft}"/>')
        for j, line in enumerate(lines):
            g.append(f'<text class="{"ln" if j == 0 else "ln2"}" x="{cx}"'
                     f' y="{100 + j * 15}" text-anchor="middle">{line}</text>')
        if last:
            g.append(f'<text class="mark" x="{cx}" y="{100 + len(lines) * 15 + 16}"'
                     f' text-anchor="middle" fill="{soft}">?</text>')
        p.append(f'<g class="y{i}">' + "".join(g) + '</g>')

    # ── 가운데: 그해 잔디 ────────────────────────────────────────────────
    weeks_n = max(len(g["weeks"]) for g in grass.values())
    empty = []
    for wi in range(weeks_n):
        for day in range(7):
            x = GRASS_X + wi * (CELL + GAP)
            y = GRASS_Y + day * (CELL + GAP)
            empty.append(f"M{x},{y}h{CELL}v{CELL}h-{CELL}z")
    p.append(f'<path d="{"".join(empty)}" fill="{BASE}" fill-opacity=".09"/>')

    for i, (year, _, _) in enumerate(YEARS):
        if year not in grass:
            continue
        ink, soft = TONES[i]
        g = grass[year]
        box = []
        for lv, (color, op) in enumerate(
                [(soft, .4), (soft, .66), (soft, .9), (ink, .95)], start=1):
            d = cells(g["weeks"], lv)
            if d:
                box.append(f'<path d="{d}" fill="{color}" fill-opacity="{op}"/>')
        box.append(f'<text class="ln2" x="{GRASS_X}" y="{GRASS_Y - 9}"'
                   f' text-anchor="start" fill="{ink}">{g["total"]:,} contributions</text>')
        p.append(f'<g class="g{i}">' + "".join(box) + '</g>')

    # 해를 지나가는 점
    hop = ";".join(t[1] for t in TONES)
    p.append(f'<circle r="4.5" fill="{TONES[0][1]}">'
             f'<animate attributeName="fill" dur="{DUR}s" fill="freeze"'
             f' values="{hop}" calcMode="discrete"/>'
             f'<animateMotion dur="{DUR}s" fill="freeze"'
             f' calcMode="linear" path="M{cols[0]},{axis_y} H{cols[-1]}"'
             f' keyTimes="0;0.05;0.86;1" keyPoints="0;0;1;1"/>'
             f'<animate attributeName="opacity" dur="{DUR}s" fill="freeze"'
             f' values="0;1;1;0;0" keyTimes="0;0.05;0.86;0.93;1"/></circle>')

    # ── 아래: 그때까지 쌓인 것 ────────────────────────────────────────────
    stack_y = 300
    p.append(f'<path d="M34,{stack_y - 30} H846" fill="none" stroke="url(#ax)"'
             f' stroke-opacity=".45" stroke-width="1.4" stroke-linecap="round"/>')

    flat = []                      # (연도 순번, 항목)
    for i, (_, _, items) in enumerate(YEARS):
        for it in items:
            flat.append((i, it))

    widths = [len(it[1]) * 7.4 + 16 if isinstance(it, tuple) else 21 for _, it in flat]
    left, right = 44, 836
    gap = (right - left - sum(widths)) / (len(flat) - 1)
    x = left
    for (i, it), wd in zip(flat, widths):
        mid = x + wd / 2
        ink, soft = TONES[i]
        if isinstance(it, tuple):
            body = (chip(mid, stack_y, it[1])
                    .replace('class="chip"', f'class="chip" stroke="{soft}"')
                    .replace('class="chip-t"', f'class="chip-t" fill="{ink}"'))
        else:
            body = logo(ic, it, mid, stack_y, 21).replace('class="lg"',
                                                          f'class="lg" fill="{soft}"')
        p.append(f'<g class="y{i}">{body}</g>')
        x += wd + gap

    for i in range(len(YEARS)):
        if str(YEARS[i][0]) in grass:
            a = (0.04 + i * 0.112) * 100
            nxt = 0.04 + (i + 1) * 0.112
            if str(YEARS[i + 1][0]) in grass:
                b = nxt * 100
                kf.append(f"@keyframes g{i}{{0%,{a:.1f}%{{opacity:0}}"
                          f"{a + 2.5:.1f}%,{b:.1f}%{{opacity:1}}"
                          f"{b + 2.5:.1f}%,100%{{opacity:0}}}}")
            else:                       # 마지막 해는 끝까지 남는다
                kf.append(f"@keyframes g{i}{{0%,{a:.1f}%{{opacity:0}}"
                          f"{a + 2.5:.1f}%,100%{{opacity:1}}}}")
    for i in range(len(YEARS)):
        begin = 0.04 + i * 0.112
        kf.append(f"@keyframes y{i}{{0%,{begin * 100:.1f}%{{opacity:0;transform:translateY(7px)}}"
                  f"{(begin + 0.035) * 100:.1f}%,100%{{opacity:1;transform:translateY(0)}}}}")

    css = f"""
  text {{ font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Malgun Gothic",sans-serif; }}
  .axis {{ fill: none; stroke: {BASE}; stroke-opacity: .2; stroke-width: 1.2; }}
  .yr {{ font-size: 14px; font-weight: 700; }}
  .ln {{ font-size: 11.5px; font-weight: 600; fill: {BASE}; fill-opacity: .92; }}
  .ln2 {{ font-size: 10px; font-weight: 400; fill: {BASE}; fill-opacity: .62; }}
  .node-q {{ fill: none; stroke: {BASE}; stroke-opacity: .45; stroke-width: 1.4; stroke-dasharray: 3 3; }}
  .lg path {{ fill: inherit; }}
  .lg {{ fill-opacity: .95; }}
  .chip {{ fill: none; stroke-opacity: .8; stroke-width: 1.1; }}
  .chip-t {{ font-size: 10.5px; font-weight: 600; }}
  .mark {{ font-size: 26px; font-weight: 700; fill-opacity: .7; }}
  g[class^="y"], g[class^="g"] {{ animation-duration: {DUR}s; animation-iteration-count: 1;
    animation-fill-mode: both; animation-timing-function: cubic-bezier(.2,.8,.2,1); }}
"""
    for i in range(len(YEARS)):
        css += f"  .y{i} {{ animation-name: y{i}; }}\n"
        if str(YEARS[i][0]) in grass:
            css += f"  .g{i} {{ animation-name: g{i}; }}\n"

    alt = ("2021 년 자바로 시작해 부트캠프에서 웹 전반을 익히고, 2022 년 첫 회사에서 C# 과 자바를, "
           "2023 년 두 번째 회사에서 PHP 와 코드이그나이터, 레디스, 엘라스틱서치를 쓰고, "
           "2024 년에 가장 많이 작업했고, 2025 년 커서, 2026 년 클로드 코드를 쓴 연표. "
           "아래 줄에는 그때까지 쌓인 기술이 해마다 하나씩 더해진다. "
           "가운데에는 그해 커밋을 날짜별로 칠한 잔디가 해마다 바뀌며 나타난다. "
           "마지막 칸은 다음엔 무엇을 쌓게 될까라는 물음")

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" '
            f'viewBox="0 0 {W2} {H2}" role="img" aria-label="{alt}">\n'
            f'<style>{css}  ' + "\n  ".join(kf) + '\n</style>\n'
            + "\n".join(p) + "\n</svg>\n")



def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?", default=os.path.join(here, "assets", "timeline.svg"))
    ap.add_argument("--icon-dir", default=os.path.join(here, "tools", "icons"))
    ap.add_argument("--grass", default=os.path.join(here, "tools", "contributions.json"))
    a = ap.parse_args()
    svg = build_timeline(load_icons(a.icon_dir), load_grass(a.grass))
    with open(a.out, "w") as f:
        f.write(svg)
    print(f"{a.out} {len(svg)} bytes")


if __name__ == "__main__":
    main()
