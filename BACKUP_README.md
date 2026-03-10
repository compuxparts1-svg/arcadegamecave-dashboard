# 🚨 Backup Recovery Guide

**Last Updated:** 2026-03-04 21:30 MST  
**Backup Location:** `/home/jason/.openclaw/workspace/.git`

If something happens to me (Hal) or OpenClaw, this guide will help you restore your workspace.

---

## Quick Recovery (If Git Still Works)

```bash
cd /home/jason/.openclaw/workspace
git log --oneline              # See all recent backups
git checkout <commit-hash>     # Restore to a specific backup
```

---

## What's Backed Up

### Core Files (✅ Restore First)
- **MEMORY.md** — Your long-term memories & project context
- **PROJECTS.md** — All active/planning projects
- **DASHBOARD.html** — Your projects dashboard (with calendar & reminders)
- **SOUL.md** — Your assistant personality
- **USER.md** — User info (name, timezone, etc.)
- **IDENTITY.md** — Your name & identity
- **HEARTBEAT.md** — Periodic check reminders
- **TOOLS.md** — Local tool notes (SSH hosts, cameras, etc.)

### Config & Scripts
- **gws-client.js** — Google Workspace client (Gmail, Calendar, Drive, Sheets)
- **gws-calendar-month.js** — Calendar viewer script
- **gws-simple-auth.js** — Google OAuth setup
- **package.json** — Node.js dependencies
- **skills/** — Agent skills installed from ClawHub

### Important NOT Backed Up (⚠️ Must Restore Manually)
- **~/.gws-token.json** — Google OAuth token (required for Gmail/Calendar)
  - Location: `/home/jason/.gws-token.json`
  - If lost: Re-run `node gws-simple-auth.js` with your auth code
- **Downloads/client_secret_*.json** — Google OAuth credentials
  - Source: Google Cloud Console
  - If lost: Download again from https://console.cloud.google.com/

### Skills (Auto-installed)
These are in `.git` but need re-setup:
- **gog** — Google Workspace CLI
- **qmd** — Local search/indexing
- **ebay** — eBay automation (NOT INSTALLED - needs approval first)
- **find-skills** — Skill discovery
- **smart-model-switching** — Cost optimization

---

## Full Restore Process

### Step 1: Restore Files from Git
```bash
cd /home/jason/.openclaw/workspace
git status                     # Check what's missing
git restore .                  # Restore all tracked files
git checkout HEAD -- .         # Alternative if above doesn't work
```

### Step 2: Restore Google Workspace Access
```bash
# Check if token still exists
ls -la ~/.gws-token.json

# If missing, re-authenticate:
cd /home/jason/.openclaw/workspace
npm install                    # Reinstall deps
node gws-simple-auth.js        # Paste your auth code
```

### Step 3: Verify Dashboard Works
```bash
cd /home/jason/.openclaw/workspace
node -e "const {Gmail} = require('./gws-client'); Gmail.search('newer_than:7d', 5).then(r => console.log('✅ Gmail works:', r.length, 'emails'))"
```

### Step 4: Reinstall Node Dependencies
```bash
cd /home/jason/.openclaw/workspace
npm install                    # Minimal install
npm install --production       # If speed matters
```

### Step 5: Reinstall Skills
```bash
cd /home/jason/.openclaw/workspace
clawhub install find-skills
clawhub install smart-model-switching
# Others as needed (see MEMORY.md)
```

---

## Emergency Recovery (Without Git)

If `.git` is corrupted/missing:

### Recover from Last Known Good Commit
```bash
# If you have a copy of the workspace on USB/external drive:
cp -r /mnt/usb/workspace/* /home/jason/.openclaw/workspace/

# Restore node_modules
npm install
```

### Minimal Restore (Just the Essentials)
Focus on these files first:
1. MEMORY.md
2. PROJECTS.md
3. DASHBOARD.html
4. gws-client.js

Then recreate:
```bash
cd /home/jason/.openclaw/workspace
npm install googleapis google-auth-library
touch .clawhub/
```

---

## Key Credentials & Secrets

⚠️ **NEVER commit these to git (they're already safe):**

- `~/.gws-token.json` — Google OAuth refresh token
  - **If lost:** Run `node gws-simple-auth.js` with auth code from browser
  - **Location:** `/home/jason/.gws-token.json`

- `~/Downloads/client_secret_*.json` — Google OAuth client credentials
  - **If lost:** Download from Google Cloud Console
  - **URL:** https://console.cloud.google.com/apis/credentials

- `.openclaw/openclaw.json` — Gateway config (redacted in backups)
  - **Important fields:** OpenRouter API key, Telegram bot token
  - **If lost:** Run `openclaw configure` to regenerate

---

## Testing the Backup

Run this weekly to verify backup is good:

```bash
#!/bin/bash
cd /home/jason/.openclaw/workspace

echo "✅ Testing git repository..."
git status

echo "✅ Testing MEMORY.md..."
[ -f MEMORY.md ] && echo "   Found ($(wc -l < MEMORY.md) lines)" || echo "   ❌ MISSING"

echo "✅ Testing PROJECTS.md..."
[ -f PROJECTS.md ] && echo "   Found ($(wc -l < PROJECTS.md) lines)" || echo "   ❌ MISSING"

echo "✅ Testing dashboard..."
[ -f DASHBOARD.html ] && echo "   Found" || echo "   ❌ MISSING"

echo "✅ Testing Google Workspace access..."
[ -f ~/.gws-token.json ] && echo "   Token found" || echo "   ⚠️  Token missing (will need to re-auth)"

echo "✅ Testing node_modules..."
[ -d node_modules ] && echo "   Found" || echo "   ❌ MISSING (run: npm install)"

echo ""
echo "Backup status: GOOD ✅"
```

---

## Common Issues & Fixes

### Issue: `.git` is corrupted
```bash
cd /home/jason/.openclaw/workspace
git fsck --full              # Check integrity
git gc --aggressive          # Repair index
```

### Issue: Files are deleted
```bash
cd /home/jason/.openclaw/workspace
git log --diff-filter=D --summary | grep delete  # Find deleted files
git checkout HEAD~1 -- <filename>                 # Restore from previous commit
```

### Issue: Wrong branch
```bash
cd /home/jason/.openclaw/workspace
git branch -a                # List branches
git checkout master          # Switch to main branch
```

### Issue: npm install fails
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## Restore Timeline

**Fastest (if .git intact):** ~30 seconds
```bash
git checkout HEAD -- .
```

**Full restore (with npm install):** ~2 minutes
```bash
git checkout HEAD -- .
npm install
npm install googleapis google-auth-library
```

**Complete recovery (with re-auth):** ~5 minutes
```bash
git checkout HEAD -- .
npm install
node gws-simple-auth.js    # Paste auth code when prompted
```

---

## Backup Verification Checklist

- [ ] MEMORY.md restored (contains long-term memory)
- [ ] PROJECTS.md restored (contains project status)
- [ ] DASHBOARD.html restored (web dashboard)
- [ ] ~/.gws-token.json exists (Google Workspace token)
- [ ] node_modules installed (`npm install` completed)
- [ ] Google Workspace access works (`node gws-test.js` passes)
- [ ] Skills available (`clawhub list` shows installed skills)

---

## Important Reminders

📌 **This backup contains:**
- Your projects and memories ✅
- Scripts and automation ✅
- Dashboard configuration ✅
- Google Workspace setup ✅

⚠️ **This backup does NOT contain:**
- Your actual email (only access token) ⚠️
- Your actual files on Google Drive ⚠️
- Your eBay credentials ⚠️
- Live database contents ⚠️

If you lose these, you'll need to:
1. Re-authenticate with Google (still have credentials in Downloads/)
2. Fetch data from source (eBay, Drive, etc.)
3. Rebuild actively-managed data

---

## One-Liner Restore

```bash
cd /home/jason/.openclaw/workspace && git checkout HEAD -- . && npm install && echo "✅ Restore complete" || echo "❌ Restore failed"
```

---

## Questions?

Check these files:
- **MEMORY.md** — Your project context
- **TOOLS.md** — Your setup details
- **USER.md** — Your user info

---

**You've got this. 🚀**

*- Hal*
