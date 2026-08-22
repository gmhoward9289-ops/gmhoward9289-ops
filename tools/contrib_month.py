#!/usr/bin/env python3
"""Render the last N days of GitHub contributions as a calendar-grid SVG.

Two files, light and dark, so the README can swap them with <picture> and
prefers-color-scheme -- camo serves one fixed file per URL, so a single
theme-aware SVG is not possible.
"""
import argparse, datetime as dt, json, subprocess, sys, os

LIGHT = dict(scale=['#ebedf0','#9be9a8','#40c463','#30a14e','#216e39'],
             bg='#ffffff', border='#d0d7de', text='#59636e', strong='#1f2328',
             empty_stroke='rgba(27,31,35,0.06)')
DARK  = dict(scale=['#151b23','#033a16','#196c2e','#2ea043','#56d364'],
             bg='#0d1117', border='#3d444d', text='#9198a1', strong='#f0f6fc',
             empty_stroke='rgba(255,255,255,0.05)')

CELL, GAP, RX = 40, 6, 8
PAD, HDR, CAP = 16, 22, 50
DOW = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


def fetch(login):
    q = ('{user(login:"%s"){contributionsCollection{contributionCalendar'
         '{weeks{contributionDays{date contributionCount}}}}}}' % login)
    out = subprocess.run(['gh', 'api', 'graphql', '-f', 'query=' + q],
                         capture_output=True, text=True, check=True).stdout
    weeks = json.loads(out)['data']['user']['contributionsCollection'][
        'contributionCalendar']['weeks']
    return [d for w in weeks for d in w['contributionDays']]


def levels(counts):
    """GitHub-style quartile thresholds over the non-zero days in view."""
    nz = sorted(c for c in counts if c > 0)
    if not nz:
        return [1, 2, 3, 4]
    return [max(1, nz[int(len(nz) * f)] if int(len(nz) * f) < len(nz) else nz[-1])
            for f in (0.0, 0.25, 0.5, 0.75)]


def level_of(count, thr):
    if count <= 0:
        return 0
    n = 1
    for t in thr[1:]:
        if count >= t:
            n += 1
    return min(n, 4)


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def render(days, theme, title):
    counts = [d['contributionCount'] for d in days]
    thr = levels(counts)
    first = dt.date.fromisoformat(days[0]['date'])
    lead = (first.weekday() + 1) % 7            # Python Mon=0 -> calendar Sun=0
    rows = -(-(lead + len(days)) // 7)
    pitch = CELL + GAP
    gw = 7 * pitch - GAP
    W = gw + 2 * PAD
    H = PAD + HDR + rows * pitch - GAP + CAP + PAD
    t = theme
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">',
         f'<style>text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",'
         f'Helvetica,Arial,sans-serif;}}</style>',
         f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}" '
         f'stroke="{t["border"]}"/>']

    for i, name in enumerate(DOW):
        x = PAD + i * pitch + CELL / 2
        o.append(f'<text x="{x:.0f}" y="{PAD + 13}" text-anchor="middle" '
                 f'font-size="11" font-weight="600" fill="{t["text"]}">{name[0]}</text>')

    for idx, d in enumerate(days):
        pos = lead + idx
        x = PAD + (pos % 7) * pitch
        y = PAD + HDR + (pos // 7) * pitch
        n = d['contributionCount']
        lv = level_of(n, thr)
        stroke = (f' stroke="{t["empty_stroke"]}"' if lv == 0 else '')
        o.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RX}" '
                 f'fill="{t["scale"][lv]}"{stroke}><title>{d["date"]}: {n} '
                 f'contribution{"" if n == 1 else "s"}</title></rect>')

    cy = PAD + HDR + rows * pitch - GAP + 20
    total, active = sum(counts), sum(1 for c in counts if c > 0)
    o.append(f'<text x="{PAD}" y="{cy}" font-size="13" font-weight="600" '
             f'fill="{t["strong"]}">{total:,} contributions in {len(days)} days</text>')
    o.append(f'<text x="{PAD}" y="{cy + 19}" font-size="11" '
             f'fill="{t["text"]}">active {active} of {len(days)} days</text>')
    lx = PAD + gw - 5 * 15 - 30
    o.append(f'<text x="{lx - 6}" y="{cy + 19}" text-anchor="end" font-size="11" '
             f'fill="{t["text"]}">Less</text>')
    for i in range(5):
        o.append(f'<rect x="{lx + i * 15}" y="{cy + 10}" width="11" height="11" '
                 f'rx="3" fill="{t["scale"][i]}"/>')
    o.append(f'<text x="{lx + 5 * 15 + 4}" y="{cy + 19}" font-size="11" '
             f'fill="{t["text"]}">More</text>')
    o.append('</svg>')
    return '\n'.join(o), total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--login', default='gmhoward9289-ops')
    ap.add_argument('--days', type=int, default=30)
    ap.add_argument('--out-dir', default='.')
    a = ap.parse_args()

    days = fetch(a.login)[-a.days:]
    total = sum(d['contributionCount'] for d in days)
    if not days or total == 0:
        sys.exit('refusing to render an empty graph: the token cannot read '
                 f'{a.login} contributions, or there really were none')
    active = sum(1 for d in days if d['contributionCount'] > 0)
    title = (f'{total:,} GitHub contributions in the last {len(days)} days, '
             f'active on {active} of them')
    for name, theme in (('light', LIGHT), ('dark', DARK)):
        svg, _ = render(days, theme, title)
        p = os.path.join(a.out_dir, f'contrib-{name}.svg')
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(svg + '\n')
        print(p)


if __name__ == '__main__':
    main()
