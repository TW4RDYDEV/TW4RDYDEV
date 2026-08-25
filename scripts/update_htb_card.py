import html
import json
import os
import urllib.request
from pathlib import Path

TOKEN = os.environ["HTB_TOKEN"].strip()
USER_ID = "3331404"
BASE = "https://labs.hackthebox.com/api"

def get_json(url):
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/json",
            "User-Agent": "TW4RDYDEV-GitHub-Profile/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)

user_info = get_json(f"{BASE}/v4/user/info")
profile = get_json(f"{BASE}/v4/user/profile/basic/{USER_ID}")["profile"]

account_id = user_info["info"]["account_id"]
experience = get_json(f"{BASE}/experience/v1/account/{account_id}")

name = profile.get("name", "Twardowski")
labs_rank = profile.get("rank", "—")
next_rank = profile.get("next_rank", "—")
labs_progress = float(profile.get("current_rank_progress") or 0)
ranking = profile.get("ranking")
system_owns = profile.get("system_owns", 0)
user_owns = profile.get("user_owns", 0)

level = experience.get("level", "—")
level_title = experience.get("levelTitle", "—")
total_xp = int(experience.get("totalExperiencePoints") or 0)
level_xp = int(experience.get("levelExperiencePoints") or 0)
xp_remaining = int(experience.get("experienceUntilNextLevel") or 0)
level_total = level_xp + xp_remaining
level_pct = (level_xp / level_total * 100) if level_total else 0

def esc(v):
    return html.escape(str(v))

def fmt_num(v):
    try:
        return f"{int(v):,}"
    except Exception:
        return str(v)

xp_bar_width = 486
xp_fill = max(0, min(xp_bar_width, xp_bar_width * level_pct / 100))
labs_bar_width = 486
labs_fill = max(0, min(labs_bar_width, labs_bar_width * labs_progress / 100))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="330" viewBox="0 0 760 330" role="img" aria-label="Hack The Box profile stats">
  <defs>
    <linearGradient id="topFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#9fef00" stop-opacity=".20"/>
      <stop offset="55%" stop-color="#9fef00" stop-opacity=".03"/>
      <stop offset="100%" stop-color="#9fef00" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect x="1" y="1" width="758" height="328" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="2"/>
  <rect x="1" y="1" width="758" height="92" rx="16" fill="url(#topFade)"/>
  <rect x="1" y="76" width="758" height="17" fill="#0d1117"/>

  <g font-family="Segoe UI, Inter, Arial, sans-serif">
    <text x="32" y="39" font-size="13" font-weight="700" fill="#8b949e" letter-spacing="1.8">HACK THE BOX</text>
    <text x="32" y="70" font-size="27" font-weight="700" fill="#f0f6fc">{esc(name)}</text>

    <text x="574" y="39" font-size="12" font-weight="600" fill="#8b949e">PUBLIC PROFILE</text>
    <text x="574" y="67" font-size="12" fill="#6e7681">ID {USER_ID}</text>

    <text x="32" y="122" font-size="12" font-weight="700" fill="#8b949e" letter-spacing="1.4">EXPERIENCE</text>
    <text x="32" y="156" font-size="25" font-weight="800" fill="#9fef00">{esc(level_title).upper()}</text>
    <text x="620" y="156" font-size="18" font-weight="700" fill="#f0f6fc">LVL {esc(level)}</text>

    <rect x="32" y="174" width="{xp_bar_width}" height="8" rx="4" fill="#21262d"/>
    <rect x="32" y="174" width="{xp_fill:.1f}" height="8" rx="4" fill="#9fef00"/>
    <text x="536" y="183" font-size="12" fill="#8b949e">{fmt_num(level_xp)} / {fmt_num(level_total)} XP</text>

    <text x="32" y="213" font-size="12" font-weight="700" fill="#8b949e" letter-spacing="1.4">LABS</text>
    <text x="32" y="244" font-size="20" font-weight="700" fill="#f0f6fc">{esc(labs_rank)}</text>
    <text x="620" y="244" font-size="12" font-weight="600" fill="#8b949e">{labs_progress:.1f}% to {esc(next_rank)}</text>

    <rect x="32" y="257" width="{labs_bar_width}" height="6" rx="3" fill="#21262d"/>
    <rect x="32" y="257" width="{labs_fill:.1f}" height="6" rx="3" fill="#58a6ff"/>

    <line x1="32" y1="282" x2="728" y2="282" stroke="#21262d"/>

    <text x="32" y="306" font-size="11" font-weight="600" fill="#6e7681">GLOBAL</text>
    <text x="82" y="306" font-size="13" font-weight="700" fill="#c9d1d9">#{fmt_num(ranking)}</text>

    <text x="240" y="306" font-size="11" font-weight="600" fill="#6e7681">SYSTEM OWNS</text>
    <text x="334" y="306" font-size="13" font-weight="700" fill="#c9d1d9">{fmt_num(system_owns)}</text>

    <text x="458" y="306" font-size="11" font-weight="600" fill="#6e7681">USER OWNS</text>
    <text x="538" y="306" font-size="13" font-weight="700" fill="#c9d1d9">{fmt_num(user_owns)}</text>

    <text x="650" y="306" font-size="11" fill="#6e7681">XP {fmt_num(total_xp)}</text>
  </g>
</svg>
'''

out = Path("assets/htb-card.svg")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(svg, encoding="utf-8")
print(f"Updated {out}")
