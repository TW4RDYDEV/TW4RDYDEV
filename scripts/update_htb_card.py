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
labs_rank = profile.get("rank", "N/A")
next_rank = profile.get("next_rank", "N/A")
labs_progress = float(profile.get("current_rank_progress") or 0)
ranking = profile.get("ranking", 0)
system_owns = profile.get("system_owns", 0)
user_owns = profile.get("user_owns", 0)

level = experience.get("level", 0)
level_title = experience.get("levelTitle", "N/A")
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


# Layout sizing
W = 760
H = 355

xp_bar_width = 520
xp_fill = max(0, min(xp_bar_width, xp_bar_width * level_pct / 100))

labs_bar_width = 520
labs_fill = max(0, min(labs_bar_width, labs_bar_width * labs_progress / 100))

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hack The Box profile stats">
  <defs>
    <linearGradient id="heroGlow" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#9fef00" stop-opacity="0.24"/>
      <stop offset="45%" stop-color="#9fef00" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#9fef00" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="htbBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#b6ff00"/>
      <stop offset="100%" stop-color="#8fe600"/>
    </linearGradient>

    <linearGradient id="labsBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#79b8ff"/>
      <stop offset="100%" stop-color="#58a6ff"/>
    </linearGradient>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Card -->
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="#0d1117" stroke="#30363d" stroke-width="2"/>
  <rect x="1" y="1" width="{W-2}" height="105" rx="18" fill="url(#heroGlow)"/>
  <rect x="1" y="86" width="{W-2}" height="20" fill="#0d1117"/>

  <g font-family="Segoe UI, Inter, Arial, sans-serif">
    <!-- Header -->
    <text x="34" y="40" font-size="13" font-weight="700" fill="#8b949e" letter-spacing="2">HACK THE BOX</text>
    <text x="34" y="74" font-size="29" font-weight="800" fill="#f0f6fc">{esc(name)}</text>

    <rect x="585" y="24" width="140" height="34" rx="9" fill="#161b22" stroke="#30363d"/>
    <text x="655" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="#c9d1d9">PUBLIC PROFILE</text>
    <text x="585" y="76" font-size="12" fill="#6e7681">ID {USER_ID}</text>

    <!-- Section 1 -->
    <text x="34" y="128" font-size="12" font-weight="700" fill="#8b949e" letter-spacing="1.8">HTB RANK</text>
    <text x="34" y="165" font-size="27" font-weight="900" fill="#9fef00" filter="url(#softGlow)">{esc(level_title).upper()}</text>

    <rect x="633" y="139" width="92" height="34" rx="10" fill="#161b22" stroke="#30363d"/>
    <text x="679" y="161" text-anchor="middle" font-size="18" font-weight="800" fill="#f0f6fc">LVL {esc(level)}</text>

    <rect x="34" y="183" width="{xp_bar_width}" height="10" rx="5" fill="#21262d"/>
    <rect x="34" y="183" width="{xp_fill:.1f}" height="10" rx="5" fill="url(#htbBar)"/>

    <text x="34" y="214" font-size="12" fill="#8b949e">Progress to next level</text>
    <text x="618" y="214" text-anchor="end" font-size="12" fill="#c9d1d9">{fmt_num(level_xp)} / {fmt_num(level_total)} XP</text>

    <!-- Divider -->
    <line x1="34" y1="233" x2="726" y2="233" stroke="#21262d"/>

    <!-- Section 2 -->
    <text x="34" y="258" font-size="12" font-weight="700" fill="#8b949e" letter-spacing="1.8">LABS RANK</text>
    <text x="34" y="292" font-size="23" font-weight="800" fill="#f0f6fc">{esc(labs_rank)}</text>

    <text x="726" y="292" text-anchor="end" font-size="12" font-weight="700" fill="#8b949e">{labs_progress:.1f}% TO {esc(next_rank).upper()}</text>

    <rect x="34" y="304" width="{labs_bar_width}" height="8" rx="4" fill="#21262d"/>
    <rect x="34" y="304" width="{labs_fill:.1f}" height="8" rx="4" fill="url(#labsBar)"/>

    <!-- Stats row -->
    <rect x="34" y="324" width="155" height="22" rx="8" fill="#11161d"/>
    <rect x="208" y="324" width="155" height="22" rx="8" fill="#11161d"/>
    <rect x="382" y="324" width="155" height="22" rx="8" fill="#11161d"/>
    <rect x="556" y="324" width="170" height="22" rx="8" fill="#11161d"/>

    <text x="46" y="339" font-size="10" font-weight="700" fill="#6e7681" letter-spacing="1.3">GLOBAL</text>
    <text x="98" y="339" font-size="12" font-weight="800" fill="#f0f6fc">#{fmt_num(ranking)}</text>

    <text x="220" y="339" font-size="10" font-weight="700" fill="#6e7681" letter-spacing="1.3">SYSTEM OWNS</text>
    <text x="318" y="339" font-size="12" font-weight="800" fill="#f0f6fc">{fmt_num(system_owns)}</text>

    <text x="394" y="339" font-size="10" font-weight="700" fill="#6e7681" letter-spacing="1.3">USER OWNS</text>
    <text x="474" y="339" font-size="12" font-weight="800" fill="#f0f6fc">{fmt_num(user_owns)}</text>

    <text x="568" y="339" font-size="10" font-weight="700" fill="#6e7681" letter-spacing="1.3">TOTAL XP</text>
    <text x="628" y="339" font-size="12" font-weight="800" fill="#f0f6fc">{fmt_num(total_xp)}</text>
  </g>
</svg>
"""

out = Path("assets/htb-card.svg")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(svg, encoding="utf-8")
print(f"Updated {out}")
