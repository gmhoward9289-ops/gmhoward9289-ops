#!/usr/bin/env python3
"""Render the last N days of GitHub contributions as a wide single-row SVG.

One small box per day in a horizontal strip, week tick labels underneath,
totals and the Less..More legend on one caption line. Two files, light and
dark, so the README can swap them with <picture> and prefers-color-scheme --
camo serves one fixed file per URL, so a single theme-aware SVG is not
possible.
"""
import argparse, datetime as dt, json, subprocess, sys, os

LIGHT = dict(scale=['#ebedf0','#9be9a8','#40c463','#30a14e','#216e39'],
             bg='#ffffff', border='#d0d7de', text='#59636e', strong='#1f2328',
             empty_stroke='rgba(27,31,35,0.06)')
DARK  = dict(scale=['#21262d','#033a16','#196c2e','#2ea043','#56d364'],
             bg='#0d1117', border='#3d444d', text='#9198a1', strong='#f0f6fc',
             empty_stroke='rgba(255,255,255,0.09)')

CELL, GAP, RX = 16, 4, 4
PAD = 16
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def fetch(login):
    q = ('{user(login:"%s"){contributionsCollection{contributionCalendar'
         '{weeks{contributionDays{date contributionCount}}}}}}' % login)
    out = subprocess.run(['gh', 'api', 'graphql', '-f', 'query=' + q],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)['data']['user']['contributionsCollection'][
        'contributionCalendar']['weeks']


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
    pitch = CELL + GAP
    gw = len(days) * pitch - GAP
    W = gw + 2 * PAD
    cell_y = PAD
    tick_y = cell_y + CELL + 14                 # week tick labels
    cap_y = tick_y + 22                         # totals + legend line
    H = cap_y + 6 + PAD - 6
    t = theme
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">',
         f'<style>text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",'
         f'Helvetica,Arial,sans-serif;}}</style>',
         f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}" '
         f'stroke="{t["border"]}"/>']

    for idx, d in enumerate(days):
        x = PAD + idx * pitch
        n = d['contributionCount']
        lv = level_of(n, thr)
        stroke = (f' stroke="{t["empty_stroke"]}"' if lv == 0 else '')
        o.append(f'<rect x="{x}" y="{cell_y}" width="{CELL}" height="{CELL}" '
                 f'rx="{RX}" fill="{t["scale"][lv]}"{stroke}><title>{d["date"]}: '
                 f'{n} contribution{"" if n == 1 else "s"}</title></rect>')

    for idx in range(0, len(days), 7):          # one tick per week
        date = dt.date.fromisoformat(days[idx]['date'])
        x = PAD + idx * pitch
        o.append(f'<text x="{x}" y="{tick_y}" font-size="10" '
                 f'fill="{t["text"]}">{MONTHS[date.month - 1]} {date.day}</text>')

    total, active = sum(counts), sum(1 for c in counts if c > 0)
    o.append(f'<text x="{PAD}" y="{cap_y}" font-size="12" font-weight="600" '
             f'fill="{t["strong"]}">{total:,} contributions in the last '
             f'{len(days)} days<tspan font-weight="400" fill="{t["text"]}">'
             f'&#160;&#183; active {active} of {len(days)}</tspan></text>')
    lx = PAD + gw - 5 * 14 - 11
    o.append(f'<text x="{lx - 6}" y="{cap_y}" text-anchor="end" font-size="11" '
             f'fill="{t["text"]}">Less</text>')
    for i in range(5):
        o.append(f'<rect x="{lx + i * 14}" y="{cap_y - 9}" width="10" '
                 f'height="10" rx="3" fill="{t["scale"][i]}"/>')
    o.append(f'<text x="{lx + 5 * 14 + 3}" y="{cap_y}" font-size="11" '
             f'fill="{t["text"]}">More</text>')
    o.append('</svg>')
    return '\n'.join(o), total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--login', default='gmhoward9289-ops')
    ap.add_argument('--weeks', type=int, default=5)
    ap.add_argument('--out-dir', default='.')
    a = ap.parse_args()

    weeks = fetch(a.login)[-a.weeks:]
    days = [d for w in weeks for d in w['contributionDays']]
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
