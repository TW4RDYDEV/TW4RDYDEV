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
country_code = profile.get("country_code", "N/A")

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


W = 820
H = 420

xp_bar_width = 470
xp_fill = max(0, min(xp_bar_width, xp_bar_width * level_pct / 100))

labs_bar_width = 470
labs_fill = max(0, min(labs_bar_width, labs_bar_width * labs_progress / 100))

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hack The Box profile stats">
  <defs>
    <linearGradient id="bgGlow" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#9fef00" stop-opacity="0.22"/>
      <stop offset="38%" stop-color="#9fef00" stop-opacity="0.07"/>
      <stop offset="100%" stop-color="#9fef00" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="heroOverlay" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#9fef00" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#9fef00" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="htbBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#bfff00"/>
      <stop offset="100%" stop-color="#95eb00"/>
    </linearGradient>

    <linearGradient id="labsBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8bc1ff"/>
      <stop offset="100%" stop-color="#58a6ff"/>
    </linearGradient>

    <pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse">
      <path d="M 18 0 L 0 0 0 18" fill="none" stroke="#1f2630" stroke-width="1"/>
    </pattern>

    <filter id="glowGreen" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="shadowSoft" x="-20%" y="-20%" width="160%" height="160%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
  </defs>

  <!-- Outer card -->
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22" fill="#0d1117" stroke="#30363d" stroke-width="2"/>

  <!-- Hero top -->
  <rect x="1" y="1" width="{W-2}" height="112" rx="22" fill="url(#bgGlow)"/>
  <rect x="1" y="1" width="{W-2}" height="112" rx="22" fill="url(#heroOverlay)"/>
  <rect x="1" y="1" width="{W-2}" height="112" rx="22" fill="url(#grid)" opacity="0.30"/>
  <rect x="1" y="90" width="{W-2}" height="24" fill="#0d1117"/>

  <!-- Main inner panel -->
  <rect x="20" y="22" width="{W-40}" height="{H-44}" rx="20" fill="none" stroke="#21262d"/>

  <g font-family="Segoe UI, Inter, Arial, sans-serif">
    <!-- Header -->
    <text x="38" y="48" font-size="13" font-weight="700" fill="#9aa4b2" letter-spacing="2.6">HACK THE BOX</text>
    <text x="38" y="88" font-size="31" font-weight="900" fill="#f0f6fc">{esc(name)}</text>

    <rect x="640" y="34" width="140" height="36" rx="11" fill="#161b22" stroke="#30363d"/>
    <text x="710" y="57" text-anchor="middle" font-size="12" font-weight="800" fill="#f0f6fc">PUBLIC PROFILE</text>

    <rect x="640" y="80" width="78" height="24" rx="8" fill="#11161d" stroke="#21262d"/>
    <text x="679" y="96" text-anchor="middle" font-size="11" font-weight="700" fill="#8b949e">ID {USER_ID}</text>

    <rect x="726" y="80" width="54" height="24" rx="8" fill="#11161d" stroke="#21262d"/>
    <text x="753" y="96" text-anchor="middle" font-size="11" font-weight="700" fill="#8b949e">{esc(country_code)}</text>

    <!-- Left feature block -->
    <text x="38" y="142" font-size="12" font-weight="700" fill="#8b949e" letter-spacing="1.8">HTB RANK</text>
    <text x="38" y="188" font-size="29" font-weight="900" fill="#a8ff00" filter="url(#glowGreen)">{esc(level_title).upper()}</text>

    <text x="38" y="216" font-size="12" fill="#8b949e">Progress to next level</text>

    <rect x="38" y="230" width="{xp_bar_width}" height="12" rx="6" fill="#1f2630"/>
    <rect x="38" y="230" width="{xp_fill:.1f}" height="12" rx="6" fill="url(#htbBar)"/>

    <text x="38" y="262" font-size="12" fill="#c9d1d9">{fmt_num(level_xp)} / {fmt_num(level_total)} XP</text>

    <!-- Right feature box -->
    <rect x="560" y="142" width="220" height="122" rx="18" fill="#0f1620" stroke="#21262d" filter="url(#shadowSoft)"/>
    <text x="582" y="170" font-size="11" font-weight="700" fill="#8b949e" letter-spacing="1.6">LEVEL</text>
    <text x="582" y="210" font-size="42" font-weight="900" fill="#f0f6fc">46</text>
    <text x="582" y="234" font-size="13" font-weight="700" fill="#8b949e">Current HTB progression</text>

    <line x1="582" y1="248" x2="758" y2="248" stroke="#21262d"/>
    <text x="582" y="286" font-size="11" font-weight="700" fill="#8b949e" letter-spacing="1.6">TOTAL XP</text>
    <text x="758" y="286" text-anchor="end" font-size="18" font-weight="800" fill="#f0f6fc">{fmt_num(total_xp)}</text>

    <!-- Divider -->
    <line x1="38" y1="286" x2="780" y2="286" stroke="#21262d"/>

    <!-- Labs section -->
    <text x="38" y="316" font-size="12" font-weight="700" fill="#8b949e" letter-spacing="1.8">LABS RANK</text>
    <text x="38" y="356" font-size="24" font-weight="900" fill="#f0f6fc">{esc(labs_rank)}</text>
    <text x="510" y="356" text-anchor="end" font-size="12" font-weight="800" fill="#8b949e">{labs_progress:.1f}% TO {esc(next_rank).upper()}</text>

    <rect x="38" y="368" width="{labs_bar_width}" height="10" rx="5" fill="#1f2630"/>
    <rect x="38" y="368" width="{labs_fill:.1f}" height="10" rx="5" fill="url(#labsBar)"/>

    <!-- Bottom premium stat pills -->
    <rect x="560" y="318" width="220" height="60" rx="16" fill="#0f1620" stroke="#21262d"/>
    <text x="582" y="340" font-size="10" font-weight="700" fill="#6e7681" letter-spacing="1.4">GLOBAL</text>
    <text x="582" y="364" font-size="18" font-weight="900" fill="#f0f6fc">#{fmt_num(ranking)}</text>

    <text x="670" y="340" font-size="10" font-weight="700" fill="#6e7681" letter-spacing="1.4">SYSTEM</text>
    <text x="670" y="364" font-size="18" font-weight="900" fill="#f0f6fc">{fmt_num(system_owns)}</text>

    <text x="736" y="340" text-anchor="end" font-size="10" font-weight="700" fill="#6e7681" letter-spacing="1.4">USER</text>
    <text x="736" y="364" text-anchor="end" font-size="18" font-weight="900" fill="#f0f6fc">{fmt_num(user_owns)}</text>
  </g>
</svg>
"""

out = Path("assets/htb-card.svg")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(svg, encoding="utf-8")
print(f"Updated {out}")
