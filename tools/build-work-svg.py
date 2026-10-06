#!/usr/bin/env python3
"""assets/work.svg 를 만든다.

글자 없이 도형과 공식 로고만으로 하는 일을 보여 주는 애니메이션 SVG 를 생성한다.
로고 path 는 simple-icons 에서 내려받아 캐시한 뒤 단색으로 다시 칠한다.

    python3 tools/build-work-svg.py                  # assets/work.svg 로 출력
    python3 tools/build-work-svg.py out.svg          # 다른 경로로 출력
    python3 tools/build-work-svg.py --icon-dir DIR   # 로고 캐시 폴더 지정
"""

import argparse
import math
import os
import re
import sys
import urllib.request

# ── 색 ─────────────────────────────────────────────────────────────────────
# 밝은 테마와 어두운 테마 양쪽에서 읽히는 중간 회색을 기본으로 쓴다.
BASE = "#8b949e"
ACC = "#4493f8"
OK = "#3fb950"

W, H = 880, 584
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@13/icons/{}.svg"

ICONS = [
    "openjdk", "spring", "php", "postgresql", "mariadb", "redis",
    "elasticsearch", "react", "typescript", "astro", "vite", "kotlin",
    "jetpackcompose", "git", "githubactions", "docker", "nginx",
    "cloudflare", "vercel", "python", "anthropic", "obsidian",
    "jirasoftware", "intellijidea",
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


def clamp(v):
    return max(0.0, min(1.0, v))


def packet(path, t0, t1, dur, r=3.2, fill=ACC):
    """경로를 t0~t1 구간에만 지나가는 점 하나."""
    o = [0, clamp(t0 - 0.004), clamp(t0 + 0.008), clamp(t1 - 0.008), clamp(t1 + 0.004), 1]
    kt = ";".join(f"{v:.4f}" for v in o)
    return (f'<circle r="{r}" fill="{fill}">'
            f'<animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear"'
            f' path="{path}" keyTimes="0;{t0:.4f};{t1:.4f};1" keyPoints="0;0;1;1"/>'
            f'<animate attributeName="opacity" dur="{dur}s" repeatCount="indefinite"'
            f' values="0;0;1;1;0;0" keyTimes="{kt}"/></circle>')


def browser(x, y, w, h):
    """브라우저 창 모양."""
    g = [f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="7"/>',
         f'<path class="hair" d="M{x},{y + 17} H{x + w}"/>']
    for i in range(3):
        g.append(f'<circle class="dot" cx="{x + 11 + i * 9}" cy="{y + 8.5}" r="2"/>')
    return "".join(g)


def phone(x, y, w, h):
    return (f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="7"/>'
            f'<path class="hair" d="M{x + w / 2 - 7},{y + h - 6} h14"/>')


def cylinder(cx, cy, w, h, cls="box"):
    """데이터베이스 원통."""
    rx, ry = w / 2, w / 6
    top, bot = cy - h / 2, cy + h / 2
    return (f'<g class="{cls}">'
            f'<ellipse cx="{cx}" cy="{top}" rx="{rx}" ry="{ry}"/>'
            f'<path d="M{cx - rx},{top} V{bot - ry * 0.2} A{rx},{ry} 0 0 0 {cx + rx},{bot - ry * 0.2} V{top}"/>'
            f'<path d="M{cx - rx},{top + (bot - top) * 0.45} A{rx},{ry} 0 0 0 {cx + rx},{top + (bot - top) * 0.45}"/>'
            f'</g>')


def magnifier(cx, cy, r=7.5, cls="box"):
    d = r * 0.72
    return (f'<g class="{cls}"><circle cx="{cx - 1}" cy="{cy - 1}" r="{r}"/>'
            f'<path d="M{cx - 1 + r * 0.72},{cy - 1 + r * 0.72} l{d},{d}"/></g>')


def bolt(cx, cy, cls="box"):
    return (f'<path class="{cls}" d="M{cx + 2},{cy - 9} L{cx - 6},{cy + 1} '
            f'H{cx - 0.5} L{cx - 2},{cy + 9} L{cx + 6},{cy - 1} H{cx + 0.5} Z"/>')


def clock(cx, cy, r=9.5, dur=6):
    """시계. 분침이 한 바퀴 돈다 — 정해진 시간에 도는 작업."""
    return (f'<g class="box"><circle cx="{cx}" cy="{cy}" r="{r}"/>'
            f'<path d="M{cx},{cy} v{-r * 0.62}">'
            f'<animateTransform attributeName="transform" type="rotate" dur="{dur}s"'
            f' repeatCount="indefinite" values="0 {cx} {cy};360 {cx} {cy}"/></path>'
            f'<path d="M{cx},{cy} h{r * 0.44}" opacity=".55"/></g>')


def doc(cx, cy, cls="box"):
    x, y, w, h = cx - 7, cy - 9, 14, 18
    out = [f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="2.5"/>']
    for i in range(3):
        out.append(f'<path class="hair2" d="M{x + 3.5},{y + 5 + i * 4.5} h{w - 7}"/>')
    return "".join(out)


def brackets(cx, cy, cls="box"):
    """구현 — 코드 괄호."""
    return (f'<g class="{cls}">'
            f'<path d="M{cx - 3},{cy - 9} l-6,9 6,9"/>'
            f'<path d="M{cx + 3},{cy - 9} l6,9 -6,9"/></g>')


def tick(cx, cy, scale=1.0, cls="tick", extra=""):
    """체크 표시. 선을 그려 나가는 애니메이션을 붙일 수 있다."""
    d = (f'M{cx - 7 * scale},{cy + 0.5 * scale} l{5 * scale},{5.5 * scale} '
         f'l{9 * scale},{-11 * scale}')
    return f'<path class="{cls}" d="{d}">{extra}</path>'


def dash_draw(length, dur, t0, t1):
    """stroke 를 t0~t1 사이에 그려 넣고 나머지 시간에는 숨긴다."""
    kt = f"0;{clamp(t0 - 0.001):.4f};{t1:.4f};{clamp(t1 + 0.14):.4f};{clamp(t1 + 0.141):.4f};1"
    return (f'<animate attributeName="stroke-dashoffset" dur="{dur}s" repeatCount="indefinite"'
            f' values="{length};{length};0;0;{length};{length}" keyTimes="{kt}"'
            f' calcMode="spline" keySplines="0 0 1 1;.2 .8 .2 1;0 0 1 1;0 0 1 1;0 0 1 1"/>')


def ring_path(cx, cy, r):
    """위에서 시작해 시계 반대 방향으로 도는 원."""
    return (f"M{cx},{cy - r} A{r},{r} 0 1 0 {cx},{cy + r} "
            f"A{r},{r} 0 1 0 {cx},{cy - r}")


def on_ring(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


# ── 본문 ───────────────────────────────────────────────────────────────────
def build(ic):
    p = []          # 그림 조각
    kf = []         # 추가 keyframes

    # ============ 1. 서비스: 요청이 들어와서 저장소를 거쳐 나간다 ============
    D1 = 6          # 한 바퀴 6초

    # 클라이언트 — 브라우저와 휴대폰, 각자 쓰는 것 로고를 안에 넣는다
    p.append(browser(40, 40, 118, 76))
    for i, n in enumerate(["react", "typescript", "astro", "vite"]):
        p.append(logo(ic, n, 69 + i * 20, 98, 13))
    p.append(phone(76, 128, 46, 80))
    for i, n in enumerate(["kotlin", "jetpackcompose"]):
        p.append(logo(ic, n, 99, 170 + i * 20, 14))

    # API 서버 — 안쪽에 서버 쪽 로고
    p.append('<rect class="node n1" x="296" y="84" width="148" height="60" rx="14"/>')
    for i, n in enumerate(["openjdk", "spring", "php"]):
        p.append(logo(ic, n, 336 + i * 34, 114, 22))

    # 멈추지 않게 지킨다 — 서버 아래 맥박
    beat = ("M300,168 h26 l7,-11 6,22 7,-11 h24 l6,-9 5,18 5,-9 h22 l7,-13 6,26 7,-13 h12")
    p.append(f'<path class="pulse" d="{beat}"/>')
    p.append(f'<path class="pulse-lit" d="{beat}" stroke-dasharray="46 1000">'
             f'<animate attributeName="stroke-dashoffset" dur="2.4s" repeatCount="indefinite"'
             f' values="46;-1000" calcMode="linear"/></path>')

    # 저장소·작업 네 줄
    rows = [
        (44, lambda: cylinder(676, 44, 22, 24) + logo(ic, "postgresql", 712, 44, 18)
         + logo(ic, "mariadb", 748, 44, 18)),
        (90, lambda: bolt(694, 90) + logo(ic, "redis", 730, 90, 20)),
        (136, lambda: magnifier(694, 136) + logo(ic, "elasticsearch", 730, 136, 19)),
        (182, lambda: clock(700, 182) + logo(ic, "python", 736, 182, 18)),
    ]
    for i, (cy, draw) in enumerate(rows):
        p.append(f'<rect class="node n2" x="600" y="{cy - 18}" width="240" height="36" rx="18"/>')
        p.append(draw())

    # 선
    wires = [
        ("M158,78 C210,78 240,114 296,114", 0.02, 0.15),       # 브라우저 → 서버
        ("M122,168 C190,168 230,114 296,114", 0.03, 0.16),      # 휴대폰 → 서버
    ]
    fan = [f"M444,114 C498,114 540,{cy} 600,{cy}" for cy, _ in rows]
    back = [f"M600,{cy} C540,{cy} 498,114 444,114" for cy, _ in rows]
    for d, _, _ in wires:
        p.append(f'<path class="wire" d="{d}"/>')
    for d in fan:
        p.append(f'<path class="wire" d="{d}"/>')

    for d, t0, t1 in wires:
        p.append(packet(d, t0, t1, D1))
    for i, d in enumerate(fan):
        p.append(packet(d, 0.20 + i * 0.015, 0.36 + i * 0.015, D1))
    for i, d in enumerate(back):
        p.append(packet(d, 0.50 + i * 0.015, 0.66 + i * 0.015, D1))
    p.append(packet("M296,114 C240,114 210,78 158,78", 0.74, 0.88, D1))
    p.append(packet("M296,114 C230,114 190,168 122,168", 0.75, 0.90, D1))

    # 켜지는 순서
    kf.append("@keyframes n1{0%,4%{stroke:" + ACC + "}14%,70%{stroke:" + BASE
              + "}76%,86%{stroke:" + ACC + "}96%,100%{stroke:" + BASE + "}}")
    kf.append("@keyframes n2{0%,30%{stroke:" + BASE + "}36%,44%{stroke:" + ACC
              + "}56%,100%{stroke:" + BASE + "}}")

    p.append('<path class="rule" d="M40,232 H840"/>')

    # ============ 2. 이관: 옮기고 하나씩 맞춰 본다 ============
    D2 = 12
    p.append(cylinder(120, 286, 46, 50))
    p.append(cylinder(760, 286, 46, 50))
    p.append('<path class="wire" d="M152,286 H728"/>')
    p.append('<rect class="bar-bg" x="152" y="312" width="576" height="4" rx="2"/>')
    p.append(f'<rect class="bar" x="152" y="312" width="576" height="4" rx="2">'
             f'<animate attributeName="width" dur="{D2}s" repeatCount="indefinite"'
             f' values="0;0;576;576;0;0" keyTimes="0;0.06;0.78;0.92;0.93;1" calcMode="linear"/>'
             f'</rect>')

    # 덩어리 여섯 묶음이 차례로 건너간다
    for i in range(6):
        t0 = 0.05 + i * 0.12
        d = "M152,286 H728"
        p.append(f'<rect class="chunk" x="-5" y="-5" width="10" height="10" rx="2.5">'
                 f'<animateMotion dur="{D2}s" repeatCount="indefinite" calcMode="linear"'
                 f' path="{d}" keyTimes="0;{t0:.4f};{t0 + 0.1:.4f};1" keyPoints="0;0;1;1"/>'
                 f'<animate attributeName="opacity" dur="{D2}s" repeatCount="indefinite"'
                 f' values="0;0;1;1;0;0"'
                 f' keyTimes="0;{t0 - 0.004:.4f};{t0 + 0.006:.4f};{t0 + 0.094:.4f};{t0 + 0.1:.4f};1"/>'
                 f'</rect>')
        # 도착한 만큼 체크가 하나씩 쌓인다
        cx = 690 + (i % 3) * 26
        cy = 346 if i < 3 else 364
        p.append(tick(cx, cy, 0.62, "tick small",
                      f'<animate attributeName="opacity" dur="{D2}s" repeatCount="indefinite"'
                      f' values="0;0;1;1;0;0"'
                      f' keyTimes="0;{t0 + 0.1:.4f};{t0 + 0.115:.4f};0.9;0.93;1"/>'))

    # 옮기는 동안 따라가며 들여다본다
    p.append(f'<g><animateTransform attributeName="transform" type="translate"'
             f' dur="{D2}s" repeatCount="indefinite"'
             f' values="0,0;0,0;486,0;486,0;0,0" keyTimes="0;0.06;0.78;0.9;1"'
             f' calcMode="linear"/>{magnifier(196, 262, 9)}</g>')

    # 다 옮긴 뒤 한 번 더 맞춰 본다
    p.append(tick(760, 238, 1.25, "tick big",
                  dash_draw(34, D2, 0.80, 0.88)))

    p.append('<path class="rule" d="M40,392 H840"/>')

    # ============ 3. 일하는 순서와 배포 ============
    D3 = 12
    CX, CY, R = 212, 486, 86
    p.append(f'<path class="ring" d="{ring_path(CX, CY, R)}"/>')

    # 가운데 — 찾아보는 일을 여러 갈래로 나눠 돌린다
    p.append(logo(ic, "anthropic", CX, CY, 26, "lg core"))
    for i, deg in enumerate([-150, -90, -30]):
        ex, ey = on_ring(CX, CY, R - 26, deg)
        d = f"M{CX},{CY} L{ex:.1f},{ey:.1f}"
        p.append(f'<path class="spoke" d="{d}"/>')
        p.append(packet(d, 0.02 + i * 0.02, 0.09 + i * 0.02, D3, 2.4))
        p.append(packet(f"M{ex:.1f},{ey:.1f} L{CX},{CY}", 0.12 + i * 0.02, 0.18 + i * 0.02, D3, 2.4))

    # 다섯 자리 — 찾아보고 · 계획하고 · 고치고 · 확인하고 · 올린다
    stations = [-90, 198, 126, 54, -18]
    pts = [on_ring(CX, CY, R, d) for d in stations]
    glyphs = []
    (sx, sy) = pts[0]
    glyphs.append(magnifier(sx, sy, 8, "box st s0"))
    (sx, sy) = pts[1]
    glyphs.append(doc(sx, sy, "box st s1"))
    (sx, sy) = pts[2]
    glyphs.append(brackets(sx, sy, "box st s2"))
    (sx, sy) = pts[3]
    glyphs.append(tick(sx, sy, 1.05, "tick st-tick",
                       dash_draw(28, D3, 0.60, 0.70)))
    (sx, sy) = pts[4]
    glyphs.append(logo(ic, "git", sx, sy, 22, "lg st s4"))
    for i, (px, py) in enumerate(pts):
        p.append(f'<circle class="pad" cx="{px:.1f}" cy="{py:.1f}" r="17"/>')
    p.extend(glyphs)

    # 자리를 지나가는 점
    p.append(f'<circle r="4" fill="{ACC}"><animateMotion dur="{D3}s" repeatCount="indefinite"'
             f' calcMode="linear" path="{ring_path(CX, CY, R)}"/></circle>')
    for i in range(5):
        a, b = i * 20, i * 20 + 7
        kf.append(f"@keyframes st{i}{{0%,{a}%{{stroke:{BASE};opacity:.7}}"
                  f"{a + 2}%,{b}%{{stroke:{ACC};opacity:1}}"
                  f"{b + 7}%,100%{{stroke:{BASE};opacity:.7}}}}")
        kf.append(f"@keyframes sf{i}{{0%,{a}%{{fill:{BASE};opacity:.7}}"
                  f"{a + 2}%,{b}%{{fill:{ACC};opacity:1}}"
                  f"{b + 7}%,100%{{fill:{BASE};opacity:.7}}}}")

    # 쓰는 도구 — 고리 왼쪽에 붙여 둔다
    for i, n in enumerate(["jirasoftware", "obsidian", "intellijidea"]):
        ty = 430 + i * 56
        p.append(f'<path class="hair2 dashed" d="M78,{ty} H{CX - R - 10:.0f}"/>')
        p.append(f'<circle class="pad" cx="58" cy="{ty}" r="16"/>')
        p.append(logo(ic, n, 58, ty, 19))

    # 올린 뒤 배포까지 — 오른쪽으로 빠지는 길
    # 올리기 자리에서 배포 길로 빠져나간다
    gx, gy = pts[4]
    lead = f"M{gx:.1f},{gy:.1f} C{gx + 30:.1f},{gy:.1f} {gx + 34:.1f},{CY} {gx + 62:.1f},{CY}"
    rail = f"M{gx + 62:.1f},{CY} H846"
    p.append(f'<path class="wire" d="{lead}"/>')
    p.append(f'<path class="wire" d="{rail}"/>')
    p.append(packet(lead, 0.785, 0.815, D3, 3.4))
    for i, n in enumerate(["githubactions", "docker", "nginx", "cloudflare", "vercel"]):
        lx = 388 + i * 86
        p.append(f'<circle class="pad" cx="{lx}" cy="{CY}" r="17"/>')
        p.append(logo(ic, n, lx, CY, 21))
    p.append(packet(rail, 0.80, 0.95, D3, 3.4))
    p.append(f'<circle class="lamp" cx="846" cy="{CY}" r="5"/>')
    p.append(f'<circle class="lamp-ping" cx="846" cy="{CY}" r="5">'
             f'<animate attributeName="r" dur="{D3}s" repeatCount="indefinite"'
             f' values="5;5;14;14" keyTimes="0;0.95;0.995;1" calcMode="spline"'
             f' keySplines="0 0 1 1;.2 .7 .3 1;0 0 1 1"/>'
             f'<animate attributeName="opacity" dur="{D3}s" repeatCount="indefinite"'
             f' values="0;0;.5;0;0" keyTimes="0;0.95;0.96;0.999;1"/></circle>')

    css = f"""
  .box, .wire, .ring, .spoke, .pulse, .hair, .hair2, .node, .tick {{ fill: none; }}
  .box {{ stroke: {BASE}; stroke-opacity: .7; stroke-width: 1.3; stroke-linecap: round; stroke-linejoin: round; }}
  .node {{ stroke: {BASE}; stroke-opacity: .42; stroke-width: 1.3; }}
  .wire {{ stroke: {BASE}; stroke-opacity: .22; stroke-width: 1.2; }}
  .ring {{ stroke: {BASE}; stroke-opacity: .2; stroke-width: 1.2; }}
  .spoke {{ stroke: {BASE}; stroke-opacity: .16; stroke-width: 1; }}
  .rule {{ stroke: {BASE}; stroke-opacity: .11; stroke-width: 1; fill: none; }}
  .hair {{ stroke: {BASE}; stroke-opacity: .4; stroke-width: 1.1; }}
  .hair2 {{ stroke: {BASE}; stroke-opacity: .28; stroke-width: 1; }}
  .dashed {{ stroke-dasharray: 2 4; }}
  .dot {{ fill: {BASE}; fill-opacity: .4; }}
  .pad {{ fill: {BASE}; fill-opacity: .055; stroke: {BASE}; stroke-opacity: .16; stroke-width: 1; }}
  .lg path {{ fill: {BASE}; fill-opacity: .82; }}
  .pulse {{ stroke: {BASE}; stroke-opacity: .2; stroke-width: 1.2; stroke-linejoin: round; }}
  .pulse-lit {{ stroke: {ACC}; stroke-opacity: .95; stroke-width: 1.5; stroke-linejoin: round; fill: none; }}
  .chunk {{ fill: {ACC}; fill-opacity: .85; }}
  .bar-bg {{ fill: {BASE}; fill-opacity: .12; }}
  .bar {{ fill: {ACC}; fill-opacity: .55; }}
  .tick {{ stroke: {OK}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
  .tick.small {{ stroke-width: 2.4; opacity: 0; }}
  .tick.big {{ stroke-dasharray: 34; stroke-dashoffset: 34; }}
  .st-tick {{ stroke-dasharray: 28; stroke-dashoffset: 28; }}
  .lamp {{ fill: {OK}; fill-opacity: .25; }}
  .lamp-ping {{ fill: none; stroke: {OK}; stroke-width: 1.4; opacity: 0; }}
  .node, .st, .core {{ animation-duration: {D1}s; animation-iteration-count: infinite; animation-timing-function: ease-out; }}
  .n1 {{ animation-name: n1; }}
  .n2 {{ animation-name: n2; }}
  .st {{ animation-duration: {D3}s; }}
  .core {{ animation-duration: {D3}s; animation-name: core; }}
  .s0 {{ animation-name: st0; }}
  .s1 {{ animation-name: st1; }}
  .s2 {{ animation-name: st2; }}
  .s4 path {{ animation: sf4 {D3}s infinite ease-out; }}
  .core path {{ animation: corefill {D3}s infinite ease-out; }}
  @keyframes core {{ 0%{{opacity:1}}100%{{opacity:1}} }}
  @keyframes corefill {{ 0%,2%{{fill:{BASE}}}6%,16%{{fill:{ACC}}}24%,100%{{fill:{BASE}}} }}
"""
    kf_css = "\n  ".join(kf)

    alt = ("웹과 앱에서 들어온 요청이 API 서버를 거쳐 데이터베이스, 캐시, 검색, "
           "정해진 시간에 도는 작업까지 퍼졌다가 돌아나가고, 쌓인 데이터를 다른 저장소로 "
           "옮기며 하나씩 맞춰 보고, 찾아보기에서 계획, 구현, 확인, 올리기로 도는 작업 "
           "순서를 지나 배포까지 이어지는 그림")

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" aria-label="{alt}">\n'
            f'<style>{css}  {kf_css}\n</style>\n'
            + "\n".join(p) + "\n</svg>\n")


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?", default=os.path.join(here, "assets", "work.svg"))
    ap.add_argument("--icon-dir", default=os.path.join(here, "tools", "icons"))
    a = ap.parse_args()
    svg = build(load_icons(a.icon_dir))
    with open(a.out, "w") as f:
        f.write(svg)
    print(f"{a.out} {len(svg)} bytes")


if __name__ == "__main__":
    main()
