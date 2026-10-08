#!/usr/bin/env python3
"""tools/contributions.json 을 다시 받는다.

연도별 잔디(날짜별 커밋 수)를 GitHub GraphQL 로 받아 저장한다.
해가 바뀌거나 올해 기록을 갱신할 때 돌린 뒤 build-timeline.py 를 다시 돌린다.

    python3 tools/fetch-contributions.py                 # 2021 년부터 올해까지
    python3 tools/fetch-contributions.py --from 2024     # 받을 첫 해를 지정
    python3 tools/fetch-contributions.py --user someone  # 다른 계정
"""

import argparse
import datetime
import json
import os
import subprocess
import sys

QUERY = ('{user(login:"%s"){contributionsCollection'
         '(from:"%d-01-01T00:00:00Z",to:"%d-12-31T23:59:59Z")'
         '{contributionCalendar{totalContributions weeks{contributionDays'
         '{contributionCount weekday}}}}}}')


def year_data(user, year):
    r = subprocess.run(["gh", "api", "graphql", "-f", "query=" + QUERY % (user, year, year)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"{year} 년을 받지 못했다: {r.stderr.strip()}")
    cal = json.loads(r.stdout)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = []
    for w in cal["weeks"]:
        col = [0] * 7
        for d in w["contributionDays"]:
            col[d["weekday"]] = d["contributionCount"]
        weeks.append(col)
    return {"total": cal["totalContributions"], "weeks": weeks}


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="secretj")
    ap.add_argument("--from", dest="start", type=int, default=2021)
    ap.add_argument("--out", default=os.path.join(here, "tools", "contributions.json"))
    a = ap.parse_args()

    now = datetime.date.today().year
    out = {}
    for y in range(a.start, now + 1):
        out[str(y)] = year_data(a.user, y)
        print(f"{y}: {out[str(y)]['total']:,}건")

    if a.start > 2021 and os.path.exists(a.out):   # 받지 않은 해는 그대로 둔다
        old = json.load(open(a.out))
        old.update(out)
        out = old

    with open(a.out, "w") as f:
        json.dump(out, f, separators=(",", ":"), sort_keys=True)
    print(f"{a.out} 에 {len(out)} 개 연도를 썼다")


if __name__ == "__main__":
    main()
