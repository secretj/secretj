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

W, H = 880, 600
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@13/icons/{}.svg"

ICONS = [
    "openjdk", "spring", "php", "postgresql", "mariadb", "redis",
    "elasticsearch", "react", "typescript", "vite", "kotlin",
    "jetpackcompose", "githubactions", "cloudflare", "vercel", "python",
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


def text(x, y, body, cls="t", anchor="middle"):
    """라벨. 글꼴은 시스템 기본만 쓴다 (GitHub 는 외부 글꼴을 받지 않는다)."""
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{body}</text>'


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
    for i, n in enumerate(["react", "typescript", "vite"]):
        p.append(logo(ic, n, 79 + i * 20, 98, 14))
    p.append(phone(76, 128, 46, 80))
    for i, n in enumerate(["kotlin", "jetpackcompose"]):
        p.append(logo(ic, n, 99, 170 + i * 20, 14))
    p.append(text(99, 230, "웹 · 앱"))

    # API 서버 — 안쪽에 서버 쪽 로고
    p.append(text(370, 72, "API 서버", "tb"))
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
        (44, "데이터베이스", lambda: logo(ic, "postgresql", 782, 44, 18)
         + logo(ic, "mariadb", 812, 44, 18)),
        (90, "캐시", lambda: logo(ic, "redis", 812, 90, 20)),
        (136, "검색", lambda: logo(ic, "elasticsearch", 812, 136, 19)),
        (182, "정해진 시간에 도는 작업", lambda: clock(812, 182, 9)),
    ]
    for i, (cy, label, draw) in enumerate(rows):
        p.append(f'<rect class="node n2" x="600" y="{cy - 18}" width="260" height="36" rx="18"/>')
        p.append(text(620, cy + 4, label, "t", "start"))
        p.append(draw())

    # 선
    wires = [
        ("M158,78 C210,78 240,114 296,114", 0.02, 0.15),       # 브라우저 → 서버
        ("M122,168 C190,168 230,114 296,114", 0.03, 0.16),      # 휴대폰 → 서버
    ]
    fan = [f"M444,114 C498,114 540,{cy} 600,{cy}" for cy, _, _ in rows]
    back = [f"M600,{cy} C540,{cy} 498,114 444,114" for cy, _, _ in rows]
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

    p.append('<path class="rule" d="M40,250 H860"/>')

    # ============ 2. 이관: 옮기고 하나씩 맞춰 본다 ============
    D2 = 12
    p.append(cylinder(120, 300, 46, 50))
    p.append(cylinder(760, 300, 46, 50))
    p.append(text(120, 350, "옮기기 전"))
    p.append(text(760, 350, "옮긴 뒤"))
    p.append(text(440, 272, "데이터 이관, 옮긴 뒤 하나씩 맞춰 보기"))
    p.append('<path class="wire" d="M152,300 H728"/>')
    p.append('<rect class="bar-bg" x="152" y="326" width="576" height="4" rx="2"/>')
    p.append(f'<rect class="bar" x="152" y="326" width="576" height="4" rx="2">'
             f'<animate attributeName="width" dur="{D2}s" repeatCount="indefinite"'
             f' values="0;0;576;576;0;0" keyTimes="0;0.06;0.78;0.92;0.93;1" calcMode="linear"/>'
             f'</rect>')

    # 덩어리 여섯 묶음이 차례로 건너간다
    for i in range(6):
        t0 = 0.05 + i * 0.12
        d = "M152,300 H728"
        p.append(f'<rect class="chunk" x="-5" y="-5" width="10" height="10" rx="2.5">'
                 f'<animateMotion dur="{D2}s" repeatCount="indefinite" calcMode="linear"'
                 f' path="{d}" keyTimes="0;{t0:.4f};{t0 + 0.1:.4f};1" keyPoints="0;0;1;1"/>'
                 f'<animate attributeName="opacity" dur="{D2}s" repeatCount="indefinite"'
                 f' values="0;0;1;1;0;0"'
                 f' keyTimes="0;{t0 - 0.004:.4f};{t0 + 0.006:.4f};{t0 + 0.094:.4f};{t0 + 0.1:.4f};1"/>'
                 f'</rect>')
        # 도착한 만큼 체크가 하나씩 쌓인다
        cx = 690 + (i % 3) * 26
        cy = 362 if i < 3 else 380
        p.append(tick(cx, cy, 0.62, "tick small",
                      f'<animate attributeName="opacity" dur="{D2}s" repeatCount="indefinite"'
                      f' values="0;0;1;1;0;0"'
                      f' keyTimes="0;{t0 + 0.1:.4f};{t0 + 0.115:.4f};0.9;0.93;1"/>'))

    # 옮기는 동안 따라가며 들여다본다
    p.append(f'<g><animateTransform attributeName="transform" type="translate"'
             f' dur="{D2}s" repeatCount="indefinite"'
             f' values="0,0;0,0;486,0;486,0;0,0" keyTimes="0;0.06;0.78;0.9;1"'
             f' calcMode="linear"/>{magnifier(196, 288, 9)}</g>')

    # 다 옮긴 뒤 한 번 더 맞춰 본다
    p.append(tick(760, 252, 1.25, "tick big",
                  dash_draw(34, D2, 0.80, 0.88)))

    p.append('<path class="rule" d="M40,410 H860"/>')

    # ============ 3. 혼자 만들어 운영 중인 것들 ============
    D3 = 12
    CY3 = 492
    p.append(brackets(60, CY3, "box"))                  # 코드를 쓴다
    p.append(text(60, CY3 + 30, "코드"))
    p.append(text(152, CY3 + 30, "빌드"))
    p.append(f'<path class="wire" d="M76,{CY3} H132"/>')
    p.append(f'<circle class="pad" cx="152" cy="{CY3}" r="18"/>')
    p.append(logo(ic, "githubactions", 152, CY3, 22))   # 빌드해서 내보낸다
    p.append(packet(f"M76,{CY3} H132", 0.02, 0.1, D3, 3))

    cols = [330, 490, 650, 810]
    t = [0.32 + i * 0.03 for i in range(4)]
    rail = CY3 - 60
    for i, cx in enumerate(cols):
        d = (f"M170,{CY3} C196,{CY3} 196,{rail} 222,{rail} "
             f"H{cx} V{CY3 - 42}")
        p.append(f'<path class="wire" d="{d}"/>')
        p.append(packet(d, 0.14 + i * 0.03, 0.3 + i * 0.03, D3, 3))

    # 체키 — 같이 보는 예산. 막대가 차오른다
    cx = cols[0]
    p.append(phone(cx - 21, CY3 - 38, 42, 60))
    p.append(f'<path class="hair2" d="M{cx - 13},{CY3 - 26} h26"/>')
    for j in range(4):
        p.append(f'<circle class="dot" cx="{cx - 12 + j * 8}" cy="{CY3 - 18}" r="1.5"/>')
    base = CY3 + 11
    for bx, h0, h1 in [(-11, 5, 16), (0, 11, 8), (11, 8, 19)]:
        kt = f"0;{t[0]:.3f};{t[0] + 0.08:.3f};0.9;1"
        ks = ".4 0 .2 1;.4 0 .2 1;0 0 1 1;.4 0 .2 1"
        p.append(f'<rect class="fill-acc" x="{cx + bx - 3}" width="6" rx="1.5" y="{base - h0}" height="{h0}">'
                 f'<animate attributeName="height" dur="{D3}s" repeatCount="indefinite"'
                 f' values="{h0};{h0};{h1};{h1};{h0}" keyTimes="{kt}" calcMode="spline" keySplines="{ks}"/>'
                 f'<animate attributeName="y" dur="{D3}s" repeatCount="indefinite"'
                 f' values="{base - h0};{base - h0};{base - h1};{base - h1};{base - h0}"'
                 f' keyTimes="{kt}" calcMode="spline" keySplines="{ks}"/></rect>')

    # 품앗이 — 봉투에 한 장 넣는다
    cx = cols[1]
    p.append(phone(cx - 21, CY3 - 38, 42, 60))
    p.append(f'<rect class="fill-acc" x="{cx - 7}" width="14" height="10" rx="1.5" y="{CY3 - 30}">'
             f'<animate attributeName="y" dur="{D3}s" repeatCount="indefinite"'
             f' values="{CY3 - 30};{CY3 - 30};{CY3 - 10};{CY3 - 10}"'
             f' keyTimes="0;{t[1]:.3f};{t[1] + 0.07:.3f};1" calcMode="spline"'
             f' keySplines="0 0 1 1;.4 0 .2 1;0 0 1 1"/>'
             f'<animate attributeName="opacity" dur="{D3}s" repeatCount="indefinite"'
             f' values="0;0;1;1;0;0"'
             f' keyTimes="0;{t[1] - 0.01:.3f};{t[1] + 0.01:.3f};{t[1] + 0.06:.3f};{t[1] + 0.075:.3f};1"/></rect>')
    p.append(f'<g class="box"><rect x="{cx - 15}" y="{CY3 - 10}" width="30" height="20" rx="2.5"/>'
             f'<path d="M{cx - 15},{CY3 - 10} l15,11 15,-11"/></g>')

    # 여행 일정표 — 들른 곳을 선으로 잇는다
    cx = cols[2]
    p.append(browser(cx - 32, CY3 - 36, 64, 58))
    route = (f"M{cx - 20},{CY3 + 10} C{cx - 13},{CY3 - 4} {cx - 3},{CY3 + 12} {cx + 5},{CY3 - 2} "
             f"S{cx + 15},{CY3 - 13} {cx + 20},{CY3 - 11}")
    p.append(f'<path class="wire" d="{route}"/>')
    p.append(f'<path class="route-lit" d="{route}" stroke-dasharray="70" stroke-dashoffset="70">'
             + dash_draw(70, D3, t[2], t[2] + 0.1) + '</path>')
    p.append(f'<circle class="fill-acc" r="2.6"><animateMotion dur="{D3}s" repeatCount="indefinite"'
             f' calcMode="linear" path="{route}" keyTimes="0;{t[2]:.3f};{t[2] + 0.1:.3f};1"'
             f' keyPoints="0;0;1;1"/></circle>')

    # ot-job — 모아서 알린다
    cx = cols[3]
    p.append(browser(cx - 32, CY3 - 36, 64, 58))
    for j in range(3):
        st = t[3] + j * 0.03
        ly = CY3 - 12 + j * 11
        p.append(f'<g opacity="0"><animate attributeName="opacity" dur="{D3}s"'
                 f' repeatCount="indefinite" values="0;0;1;1;0;0"'
                 f' keyTimes="0;{st:.3f};{st + 0.02:.3f};0.92;0.95;1"/>'
                 f'<circle class="fill-acc" cx="{cx - 19}" cy="{ly}" r="2.2"/>'
                 f'<path class="hair2" d="M{cx - 12},{ly} h26"/></g>')
    pivot = f"{cx + 23} {CY3 + 10}"
    p.append(f'<g class="bell"><circle class="pad-solid" cx="{cx + 23}" cy="{CY3 + 17}" r="11"/>'
             f'<g class="box"><path d="M{cx + 17},{CY3 + 20} a6,6 0 0 1 12,0 v3 l1.8,2.8 h-15.6 l1.8,-2.8 Z"/>'
             f'<path d="M{cx + 21.2},{CY3 + 27} a1.8,1.8 0 0 0 3.6,0"/></g>'
             f'<animateTransform attributeName="transform" type="rotate" dur="{D3}s"'
             f' repeatCount="indefinite"'
             f' values="0 {pivot};0 {pivot};-12 {pivot};10 {pivot};-6 {pivot};0 {pivot};0 {pivot}"'
             f' keyTimes="0;{t[3] + 0.09:.3f};{t[3] + 0.12:.3f};{t[3] + 0.15:.3f};'
             f'{t[3] + 0.18:.3f};{t[3] + 0.21:.3f};1"/></g>')

    # 각 결과물이 선 기술
    names4 = ["체키", "품앗이", "여행 일정표", "ot-job"]
    notes = ["가계부 · 캘린더", "경조사비 장부", "여행 계획 기록", "공고 모아 알림"]
    decks = [["react", "typescript", "spring"], ["kotlin", "jetpackcompose"],
             ["cloudflare"], ["python", "vercel"]]
    for cx, nm, note, names in zip(cols, names4, notes, decks):
        p.append(text(cx, CY3 + 42, nm, "tb"))
        p.append(text(cx, CY3 + 58, note, "ts"))
        x0 = cx - (len(names) - 1) * 13
        for j, n in enumerate(names):
            p.append(logo(ic, n, x0 + j * 26, CY3 + 78, 18))

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
  text {{ font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Malgun Gothic",sans-serif; }}
  .t {{ font-size: 11.5px; font-weight: 400; fill: {BASE}; fill-opacity: .9; }}
  .tb {{ font-size: 12.5px; font-weight: 600; fill: {BASE}; fill-opacity: 1; }}
  .ts {{ font-size: 10.5px; font-weight: 400; fill: {BASE}; fill-opacity: .66; }}
  .pad {{ fill: {BASE}; fill-opacity: .055; stroke: {BASE}; stroke-opacity: .16; stroke-width: 1; }}
  .lg path {{ fill: {BASE}; fill-opacity: .82; }}
  .pulse {{ stroke: {BASE}; stroke-opacity: .2; stroke-width: 1.2; stroke-linejoin: round; }}
  .pulse-lit {{ stroke: {ACC}; stroke-opacity: .95; stroke-width: 1.5; stroke-linejoin: round; fill: none; }}
  .chunk {{ fill: {ACC}; fill-opacity: .85; }}
  .fill-acc {{ fill: {ACC}; fill-opacity: .8; }}
  .pad-solid {{ fill: #0d1117; fill-opacity: 0; }}
  .route-lit {{ fill: none; stroke: {ACC}; stroke-opacity: .95; stroke-width: 1.6; stroke-linecap: round; }}
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
