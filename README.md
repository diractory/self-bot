# 🤖 RADHEY Selfbot — Telegram Userbot (Telethon)

A feature-rich **Telegram userbot (selfbot)** built with [Telethon](https://github.com/LonamiWebs/Telethon). It runs on your own Telegram account and lets you control it via dot-commands (`.help`, `.info`, `.mute`, `.gc`, etc.) sent from any chat. Includes a built-in web server for 24/7 hosting on platforms like Render.

> ⚠️ **This is a userbot, not a Bot API bot.** It automates a *personal* Telegram account using its API credentials. See [Disclaimer](#-disclaimer--read-before-use) before deploying.

---

## ✨ Features

| Category | Commands |
|---|---|
| **Help & Reliability** | `.help`, `.owner`, `.fix` (auto-retry + error logging), `.fixlog` |
| **User Info & OSINT** | `.info` / `.tinfo`, `.id`, `.chatinfo`, `.insta` / `.iginfo` (Instagram profile lookup) |
| **Moderation** | `.mute`, `.unmute`, `.ban`, `.unban`, `.block`, `.unblock`, `.kick`, `.admin`, `.demote` |
| **Messaging & Broadcast** | `.dm`, `.frwd` (forward to all DMs), `.gc` (broadcast to admin groups), `.broad` (text-blast all users), `.frwdall`, `.say` (ghost-send) |
| **Group Tools** | `.tag` (mention all members), `.autoaccept`, `.mm` (create middleman group) |
| **Utilities** | `.calc` (SymPy-powered calculator), `.tr` / `.translate`, `.count` (countdown timer), `.purge`, `.close`, `.del` |
| **Anti-ban** | Randomized delays (5–10s) + forced 40s cooldown every 15 messages during broadcasts |
| **Hosting** | Built-in `aiohttp` health-check server (`/` and `/health`) for uptime monitors / Render keep-alive |

---

## 🛠️ Tech Stack

- **[Telethon](https://docs.telethon.dev/)** — Telegram MTProto client
- **aiohttp** — lightweight keep-alive web server
- **requests** — Instagram GraphQL fallback + translation API calls
- **sympy** — safe math expression evaluation for `.calc`
- **instaloader** — primary Instagram profile scraper
- **Flask** — listed dependency (optional/legacy web layer)

---

## 📦 Installation

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
pip install -r requirements.txt
```

### Environment Variables

**Never hardcode credentials in `bot.py`.** Set these instead:

| Variable | Description |
|---|---|
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API hash from [my.telegram.org](https://my.telegram.org) |
| `PHONE` | Your account's phone number (with country code) |
| `SESSION_STRING` | (Optional) Base64-encoded Telethon session, for headless/server deploys without interactive login |
| `PORT` | (Optional) Port for the health-check server, defaults to `8080` |

Create a `.env` file or export them in your shell/host dashboard:

```bash
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export PHONE="+1XXXXXXXXXX"
```

### Run

```bash
python bot.py
```

On first run you'll be prompted for a login code (and 2FA password if enabled). A `.session` file is generated so future runs skip the login step.

### Deploy (Render / VPS / Docker)

1. Generate a session string locally, base64-encode it, and set it as `SESSION_STRING` on your host — this skips interactive login on restart.
2. The app binds an HTTP health endpoint on `$PORT`, so it works out-of-the-box with Render's web service health checks.

---

## 💬 Usage

Send any command as a message from your own account (it works because `outgoing=True` events are captured):

```
.help
.info          (reply to a user)
.mute @someone
.gc            (reply to a message to broadcast it to groups you admin)
.calc sqrt(144) + 5
.tr hi Hello there
```

Full command list is always available in-app via `.help`.

---

## ⚠️ Disclaimer — Read Before Use

- **Telegram's Terms of Service prohibit automating a personal user account** (userbots/selfbots). Only bots created via [@BotFather](https://t.me/BotFather) using the official Bot API are officially sanctioned. Using this script **can get your account limited or banned** — use at your own risk, ideally on a secondary/throwaway account.
- **Mass-messaging features (`.frwd`, `.gc`, `.broad`, `.frwdall`) send unsolicited messages to your contacts/groups.** Misuse of these can constitute spam and may violate Telegram's anti-spam policies as well as the platform policies of any group you're a member of. Use responsibly and only with recipients' consent.
- **Remove all hardcoded secrets before publishing this repo.** The original script contains a default `API_ID`, `API_HASH`, and `PHONE` inline in the source — treat any credentials that were ever committed as compromised, rotate them at [my.telegram.org](https://my.telegram.org), and rely on environment variables going forward (see above). Also add `*.session`, `selfbot_data.json`, and `errors.log` to `.gitignore`, since they can contain live session tokens, muted/banned user IDs, and stack traces.
- Instagram scraping (`.insta`) uses unofficial/private endpoints and may break or get rate-limited if Instagram changes its API.

---

## 📁 Project Structure

```
.
├── bot.py              # Main userbot logic (commands, handlers, web server)
├── requirements.txt    # Python dependencies
├── selfbot_data.json   # Auto-generated: muted/banned user IDs (gitignore this)
└── errors.log          # Auto-generated: .fix error logs (gitignore this)
```

---

## 📝 License

Add a license of your choice (MIT recommended for open-source projects).

---

## 🏷️ Suggested GitHub Topics / Tags

```
telegram-bot  telethon  userbot  selfbot  telegram-userbot  python
telegram-automation  telegram-api  mtproto  automation-bot  osint-tool
```

---

## 🙋 Support

Questions or issues? Open a GitHub Issue in this repository.
<!-- hacktoberfest update 20260709155341576785 -->
<!-- run 1 @ 20260709155359253708 -->
<!-- run 2 @ 20260709155410909872 -->
<!-- run 3 @ 20260709155422550116 -->
<!-- run 4 @ 20260709155434782254 -->
<!-- run 5 @ 20260709155446965015 -->
<!-- run 6 @ 20260709155459230712 -->
<!-- run 7 @ 20260709155511760876 -->
<!-- run 8 @ 20260709155525509589 -->
<!-- run 9 @ 20260709155537592940 -->
<!-- run 10 @ 20260709155549937394 -->
<!-- run 11 @ 20260709155602860503 -->
<!-- run 12 @ 20260709155614807832 -->
<!-- run 13 @ 20260709155626409134 -->
<!-- run 14 @ 20260709155639461398 -->
<!-- run 15 @ 20260709155651034312 -->
<!-- run 16 @ 20260709155702847225 -->
<!-- run 17 @ 20260709155715197008 -->
<!-- run 18 @ 20260709155726622719 -->
<!-- run 19 @ 20260709155738833080 -->
<!-- run 20 @ 20260709155751508844 -->
<!-- run 21 @ 20260709155803450168 -->
<!-- run 22 @ 20260709155820537383 -->
<!-- run 23 @ 20260709155832362320 -->
<!-- run 24 @ 20260709155844299510 -->
<!-- run 25 @ 20260709155857215764 -->
<!-- run 26 @ 20260709155909979827 -->
<!-- run 27 @ 20260709155922462128 -->
<!-- run 28 @ 20260709155935508019 -->
<!-- run 29 @ 20260709155949524100 -->
<!-- run 30 @ 20260709160003752266 -->
<!-- run 31 @ 20260709160016843638 -->
<!-- run 32 @ 20260709160029504046 -->
<!-- run 33 @ 20260709160043249844 -->
<!-- run 34 @ 20260709160055486480 -->
<!-- run 35 @ 20260709160107614429 -->
<!-- run 36 @ 20260709160118969518 -->
<!-- run 37 @ 20260709160130595289 -->
<!-- run 38 @ 20260709160141903623 -->
<!-- run 39 @ 20260709160155465484 -->
<!-- run 40 @ 20260709160207754278 -->
<!-- run 41 @ 20260709160221511067 -->
<!-- run 42 @ 20260709160233876106 -->
<!-- run 43 @ 20260709160246645454 -->
<!-- run 44 @ 20260709160258660787 -->
<!-- run 45 @ 20260709160310470732 -->
<!-- run 46 @ 20260709160322935981 -->
<!-- run 47 @ 20260709160334711704 -->
<!-- run 48 @ 20260709160346012935 -->
<!-- run 49 @ 20260709160357549287 -->
<!-- run 50 @ 20260709160410808908 -->
<!-- run 51 @ 20260709160423840525 -->
<!-- run 52 @ 20260709160435294874 -->
<!-- run 53 @ 20260709160446574263 -->
<!-- run 54 @ 20260709160458880674 -->
<!-- run 55 @ 20260709160510082694 -->
<!-- run 56 @ 20260709160522174833 -->
<!-- run 57 @ 20260709160534218348 -->
<!-- run 58 @ 20260709160546101126 -->
<!-- run 59 @ 20260709160558589793 -->
<!-- run 60 @ 20260709160612224317 -->
<!-- run 61 @ 20260709160625031851 -->
<!-- run 62 @ 20260709160637596553 -->
<!-- run 63 @ 20260709160651317367 -->
<!-- run 64 @ 20260709160704854167 -->
<!-- run 65 @ 20260709160718645768 -->
<!-- run 66 @ 20260709160731232153 -->
<!-- run 67 @ 20260709160743691061 -->
<!-- run 68 @ 20260709160756615417 -->
<!-- run 69 @ 20260709160810680205 -->
<!-- run 70 @ 20260709160822822498 -->
<!-- run 71 @ 20260709160834410168 -->
<!-- run 72 @ 20260709160846035775 -->
<!-- run 73 @ 20260709160857597561 -->
<!-- run 74 @ 20260709160909490353 -->
<!-- run 75 @ 20260709160921985841 -->
<!-- run 76 @ 20260709160935311553 -->
<!-- run 77 @ 20260709160948336306 -->
<!-- run 78 @ 20260709161002245131 -->
<!-- run 79 @ 20260709161015582641 -->
