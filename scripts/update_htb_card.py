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


def esc(value):
    return html.escape(str(value))


def fmt_num(value):
    try:
        return f"{int(value):,}"
    except Exception:
        return str(value)


# ── Fetch HTB data ────────────────────────────────────────────────

user_info = get_json(f"{BASE}/v4/user/info")

profile = get_json(
    f"{BASE}/v4/user/profile/basic/{USER_ID}"
)["profile"]

account_id = user_info["info"]["account_id"]

experience = get_json(
    f"{BASE}/experience/v1/account/{account_id}"
)


# ── Profile ───────────────────────────────────────────────────────

name = profile.get("name", "Twardowski")
country = profile.get("country_code", "CA")

labs_rank = profile.get("rank", "N/A")
next_rank = profile.get("next_rank", "N/A")
labs_progress = float(
    profile.get("current_rank_progress") or 0
)

ranking = profile.get("ranking", 0)
system_owns = profile.get("system_owns", 0)
user_owns = profile.get("user_owns", 0)


# ── Experience ────────────────────────────────────────────────────

level = experience.get("level", 0)
level_title = experience.get("levelTitle", "N/A")

total_xp = int(
    experience.get("totalExperiencePoints") or 0
)

level_xp = int(
    experience.get("levelExperiencePoints") or 0
)

xp_remaining = int(
    experience.get("experienceUntilNextLevel") or 0
)

level_total = level_xp + xp_remaining

level_progress = (
    level_xp / level_total * 100
    if level_total
    else 0
)


# ── Layout calculations ──────────────────────────────────────────

WIDTH = 820
HEIGHT = 410

RANK_BAR_WIDTH = 490
LABS_BAR_WIDTH = 490

rank_fill = max(
    0,
    min(
        RANK_BAR_WIDTH,
        RANK_BAR_WIDTH * level_progress / 100,
    ),
)

labs_fill = max(
    0,
    min(
        LABS_BAR_WIDTH,
        LABS_BAR_WIDTH * labs_progress / 100,
    ),
)


# ── SVG ──────────────────────────────────────────────────────────

svg = f"""
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
    role="img"
    aria-label="Hack The Box profile"
>

<defs>

    <linearGradient id="header" x1="0" x2="1">
        <stop
            offset="0%"
            stop-color="#9fef00"
            stop-opacity="0.22"
        />

        <stop
            offset="48%"
            stop-color="#9fef00"
            stop-opacity="0.055"
        />

        <stop
            offset="100%"
            stop-color="#9fef00"
            stop-opacity="0"
        />
    </linearGradient>

    <linearGradient id="rankBar" x1="0" x2="1">

        <stop
            offset="0%"
            stop-color="#b5ff00"
        />

        <stop
            offset="100%"
            stop-color="#8fe600"
        />

    </linearGradient>

    <linearGradient id="labsBar" x1="0" x2="1">

        <stop
            offset="0%"
            stop-color="#79b8ff"
        />

        <stop
            offset="100%"
            stop-color="#58a6ff"
        />

    </linearGradient>

    <pattern
        id="grid"
        width="20"
        height="20"
        patternUnits="userSpaceOnUse"
    >
        <path
            d="M20 0H0V20"
            fill="none"
            stroke="#9fef00"
            stroke-opacity="0.045"
        />
    </pattern>

</defs>


<!-- BASE -->

<rect
    x="1"
    y="1"
    width="818"
    height="408"
    rx="20"
    fill="#0d1117"
    stroke="#30363d"
    stroke-width="2"
/>


<!-- HEADER -->

<rect
    x="1"
    y="1"
    width="818"
    height="100"
    rx="20"
    fill="url(#header)"
/>

<rect
    x="1"
    y="1"
    width="818"
    height="100"
    rx="20"
    fill="url(#grid)"
/>

<rect
    x="1"
    y="82"
    width="818"
    height="20"
    fill="#0d1117"
/>


<g
    font-family="Segoe UI, Arial, sans-serif"
>


<!-- TITLE -->

<text
    x="36"
    y="40"
    font-size="12"
    font-weight="700"
    letter-spacing="2.2"
    fill="#8b949e"
>
HACK THE BOX
</text>

<text
    x="36"
    y="76"
    font-size="30"
    font-weight="800"
    fill="#f0f6fc"
>
{esc(name)}
</text>


<!-- PROFILE CHIPS -->

<rect
    x="626"
    y="27"
    width="154"
    height="38"
    rx="11"
    fill="#161b22"
    stroke="#30363d"
/>

<text
    x="703"
    y="51"
    text-anchor="middle"
    font-size="12"
    font-weight="700"
    fill="#f0f6fc"
>
PUBLIC PROFILE
</text>


<rect
    x="626"
    y="72"
    width="98"
    height="25"
    rx="8"
    fill="#11161d"
    stroke="#21262d"
/>

<text
    x="675"
    y="89"
    text-anchor="middle"
    font-size="10"
    font-weight="600"
    fill="#8b949e"
>
ID {USER_ID}
</text>


<rect
    x="732"
    y="72"
    width="48"
    height="25"
    rx="8"
    fill="#11161d"
    stroke="#21262d"
/>

<text
    x="756"
    y="89"
    text-anchor="middle"
    font-size="10"
    font-weight="700"
    fill="#8b949e"
>
{esc(country)}
</text>


<!-- HTB RANK -->

<text
    x="36"
    y="134"
    font-size="12"
    font-weight="700"
    letter-spacing="1.8"
    fill="#8b949e"
>
HTB RANK
</text>


<text
    x="36"
    y="174"
    font-size="28"
    font-weight="900"
    fill="#9fef00"
>
{esc(level_title).upper()}
</text>


<text
    x="36"
    y="199"
    font-size="11"
    fill="#8b949e"
>
Progress to level {int(level) + 1}
</text>


<!-- RANK BAR -->

<rect
    x="36"
    y="213"
    width="{RANK_BAR_WIDTH}"
    height="10"
    rx="5"
    fill="#21262d"
/>

<rect
    x="36"
    y="213"
    width="{rank_fill:.1f}"
    height="10"
    rx="5"
    fill="url(#rankBar)"
/>


<text
    x="36"
    y="245"
    font-size="11"
    fill="#c9d1d9"
>
{fmt_num(level_xp)} / {fmt_num(level_total)} XP
</text>


<text
    x="526"
    y="245"
    text-anchor="end"
    font-size="11"
    font-weight="700"
    fill="#8b949e"
>
{level_progress:.1f}%
</text>


<!-- LEVEL CARD -->

<rect
    x="560"
    y="124"
    width="220"
    height="130"
    rx="17"
    fill="#101720"
    stroke="#21262d"
/>


<text
    x="582"
    y="151"
    font-size="10"
    font-weight="700"
    letter-spacing="1.5"
    fill="#8b949e"
>
LEVEL
</text>


<text
    x="582"
    y="194"
    font-size="44"
    font-weight="900"
    fill="#f0f6fc"
>
{esc(level)}
</text>


<line
    x1="582"
    y1="211"
    x2="758"
    y2="211"
    stroke="#21262d"
/>


<text
    x="582"
    y="235"
    font-size="10"
    font-weight="700"
    letter-spacing="1.3"
    fill="#8b949e"
>
TOTAL XP
</text>


<text
    x="758"
    y="236"
    text-anchor="end"
    font-size="18"
    font-weight="800"
    fill="#f0f6fc"
>
{fmt_num(total_xp)}
</text>


<!-- MAIN DIVIDER -->

<line
    x1="36"
    y1="274"
    x2="780"
    y2="274"
    stroke="#21262d"
/>


<!-- LABS -->

<text
    x="36"
    y="305"
    font-size="12"
    font-weight="700"
    letter-spacing="1.8"
    fill="#8b949e"
>
LABS RANK
</text>


<text
    x="36"
    y="342"
    font-size="23"
    font-weight="800"
    fill="#f0f6fc"
>
{esc(labs_rank)}
</text>


<text
    x="526"
    y="342"
    text-anchor="end"
    font-size="11"
    font-weight="700"
    fill="#8b949e"
>
{labs_progress:.1f}% TO {esc(next_rank).upper()}
</text>


<!-- LABS BAR -->

<rect
    x="36"
    y="355"
    width="{LABS_BAR_WIDTH}"
    height="9"
    rx="4.5"
    fill="#21262d"
/>

<rect
    x="36"
    y="355"
    width="{labs_fill:.1f}"
    height="9"
    rx="4.5"
    fill="url(#labsBar)"
/>


<!-- LAB STATS -->

<rect
    x="560"
    y="294"
    width="220"
    height="70"
    rx="17"
    fill="#101720"
    stroke="#21262d"
/>


<line
    x1="633"
    y1="309"
    x2="633"
    y2="349"
    stroke="#21262d"
/>

<line
    x1="707"
    y1="309"
    x2="707"
    y2="349"
    stroke="#21262d"
/>


<!-- GLOBAL -->

<text
    x="596"
    y="316"
    text-anchor="middle"
    font-size="9"
    font-weight="700"
    letter-spacing="1"
    fill="#6e7681"
>
GLOBAL
</text>

<text
    x="596"
    y="343"
    text-anchor="middle"
    font-size="17"
    font-weight="800"
    fill="#f0f6fc"
>
#{fmt_num(ranking)}
</text>


<!-- SYSTEM -->

<text
    x="670"
    y="316"
    text-anchor="middle"
    font-size="9"
    font-weight="700"
    letter-spacing="1"
    fill="#6e7681"
>
SYSTEM
</text>

<text
    x="670"
    y="343"
    text-anchor="middle"
    font-size="17"
    font-weight="800"
    fill="#f0f6fc"
>
{fmt_num(system_owns)}
</text>


<!-- USER -->

<text
    x="744"
    y="316"
    text-anchor="middle"
    font-size="9"
    font-weight="700"
    letter-spacing="1"
    fill="#6e7681"
>
USER
</text>

<text
    x="744"
    y="343"
    text-anchor="middle"
    font-size="17"
    font-weight="800"
    fill="#f0f6fc"
>
{fmt_num(user_owns)}
</text>


<!-- FOOTER -->

<text
    x="36"
    y="394"
    font-size="10"
    fill="#484f58"
>
LIVE HTB PROFILE DATA
</text>


<text
    x="780"
    y="394"
    text-anchor="end"
    font-size="10"
    fill="#484f58"
>
TW4RDYDEV
</text>


</g>

</svg>
"""


# ── Write ─────────────────────────────────────────────────────────

output = Path("assets/htb-card.svg")

output.parent.mkdir(
    parents=True,
    exist_ok=True,
)

output.write_text(
    svg,
    encoding="utf-8",
)

print(f"Updated {output}")
