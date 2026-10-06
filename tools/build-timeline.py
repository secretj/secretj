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
import os
import re
import sys
import urllib.request

# ── 색 ─────────────────────────────────────────────────────────────────────
# 밝은 테마와 어두운 테마 양쪽에서 읽히는 중간 회색을 기본으로 쓴다.
BASE = "#8b949e"
ACC = "#4493f8"

CDN = "https://cdn.jsdelivr.net/npm/simple-icons@13/icons/{}.svg"

ICONS = [
    "openjdk", "html5", "javascript", "spring", "dotnet",
    "php", "codeigniter", "redis", "elasticsearch",
    "anthropic", "python", "kotlin", "react", "typescript",
]


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
    ("2022", ["첫 회사 입사", "C# 과 Java"],
     [("칩", "C#"), "dotnet"]),
    ("2023", ["두 번째 회사 · PHP", "CI3 → CI4 전환", "DDD · Queue"],
     ["php", "codeigniter", "redis", "elasticsearch"]),
    ("2024", ["게시판 · 메일 API", "기능 개발과 장애 대응", "커밋 1,796"], []),
    ("2025", ["코딩 표준 · 에러 통합", "2단계 인증, 속도 개선", "Cursor 를 쓰기 시작"],
     [("칩", "Cursor")]),
    ("2026", ["Claude Code 로", "혼자 만들어 운영"],
     ["anthropic", "python", "kotlin", "react", "typescript"]),
    ("?", ["다음엔", "무엇을 쌓게 될까?"], []),
]


def build_timeline(ic):
    """해마다 무엇이 쌓였는지 위에 적고, 쌓인 것을 아래에 모아 둔다."""
    W2, H2 = 880, 246
    DUR = 11
    cols = [56 + i * 122 for i in range(7)]
    axis_y, p, kf = 74, [], []

    p.append(f'<path class="axis" d="M34,{axis_y} H846"/>')

    for i, (year, lines, _) in enumerate(YEARS):
        cx = cols[i]
        last = i == len(YEARS) - 1
        g = [f'<text class="yr" x="{cx}" y="52" text-anchor="middle">{year}</text>']
        g.append(f'<circle class="{"node-q" if last else "node-y"}"'
                 f' cx="{cx}" cy="{axis_y}" r="{7 if last else 5.5}"/>')
        for j, line in enumerate(lines):
            g.append(f'<text class="{"ln" if j == 0 else "ln2"}" x="{cx}"'
                     f' y="{100 + j * 15}" text-anchor="middle">{line}</text>')
        if last:
            g.append(f'<text class="mark" x="{cx}" y="{100 + len(lines) * 15 + 16}"'
                     f' text-anchor="middle">?</text>')
        p.append(f'<g class="y{i}">' + "".join(g) + '</g>')

    # 해를 지나가는 점
    p.append(f'<circle r="4" fill="{ACC}"><animateMotion dur="{DUR}s" repeatCount="indefinite"'
             f' calcMode="linear" path="M{cols[0]},{axis_y} H{cols[-1]}"'
             f' keyTimes="0;0.04;0.79;1" keyPoints="0;0;1;1"/>'
             f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite"'
             f' values="0;1;1;0;0" keyTimes="0;0.04;0.79;0.84;1"/></circle>')

    # ── 아래: 그때까지 쌓인 것 ────────────────────────────────────────────
    stack_y = 212
    p.append(f'<path class="axis" d="M34,{stack_y - 30} H846" opacity=".55"/>')

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
        body = chip(mid, stack_y, it[1]) if isinstance(it, tuple) \
            else logo(ic, it, mid, stack_y, 21)
        p.append(f'<g class="y{i}">{body}</g>')
        x += wd + gap

    for i in range(len(YEARS)):
        begin = 0.04 + i * 0.112
        kf.append(f"@keyframes y{i}{{0%,{begin * 100:.1f}%{{opacity:0;transform:translateY(7px)}}"
                  f"{(begin + 0.03) * 100:.1f}%,92%{{opacity:1;transform:translateY(0)}}"
                  f"97%,100%{{opacity:0;transform:translateY(7px)}}}}")

    css = f"""
  text {{ font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Malgun Gothic",sans-serif; }}
  .axis {{ fill: none; stroke: {BASE}; stroke-opacity: .2; stroke-width: 1.2; }}
  .yr {{ font-size: 14px; font-weight: 700; fill: {BASE}; fill-opacity: 1; }}
  .ln {{ font-size: 11.5px; font-weight: 600; fill: {BASE}; fill-opacity: .92; }}
  .ln2 {{ font-size: 10px; font-weight: 400; fill: {BASE}; fill-opacity: .62; }}
  .node-y {{ fill: {ACC}; fill-opacity: .9; }}
  .node-q {{ fill: none; stroke: {BASE}; stroke-opacity: .5; stroke-width: 1.4; stroke-dasharray: 3 3; }}
  .lg path {{ fill: {BASE}; fill-opacity: .82; }}
  .chip {{ fill: none; stroke: {BASE}; stroke-opacity: .42; stroke-width: 1.1; }}
  .chip-t {{ font-size: 10.5px; font-weight: 600; fill: {BASE}; fill-opacity: .88; }}
  .mark {{ font-size: 26px; font-weight: 700; fill: {BASE}; fill-opacity: .45; }}
  g[class^="y"] {{ animation-duration: {DUR}s; animation-iteration-count: infinite;
    animation-timing-function: cubic-bezier(.2,.8,.2,1); }}
"""
    for i in range(len(YEARS)):
        css += f"  .y{i} {{ animation-name: y{i}; }}\n"

    alt = ("2021 년 자바로 시작해 부트캠프에서 웹 전반을 익히고, 2022 년 첫 회사에서 C# 과 자바를, "
           "2023 년 두 번째 회사에서 PHP 와 코드이그나이터, 레디스, 엘라스틱서치를 쓰고, "
           "2024 년에 가장 많이 작업했고, 2025 년 커서, 2026 년 클로드 코드를 쓴 연표. "
           "아래 줄에는 그때까지 쌓인 기술이 해마다 하나씩 더해진다. "
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
    a = ap.parse_args()
    svg = build_timeline(load_icons(a.icon_dir))
    with open(a.out, "w") as f:
        f.write(svg)
    print(f"{a.out} {len(svg)} bytes")


if __name__ == "__main__":
    main()
