# 🔄 Hal Restoration Guide

If something happens to Hal's Docker container or workspace, follow this guide to restore everything.

## Quick Restore (5 minutes)

### Step 1: Clone the backup repo on your VPS

```bash
cd /tmp
git clone https://github.com/compuxparts1-svg/arcadegamecave-dashboard.git hal-backup
cd hal-backup
```

### Step 2: Copy files back to workspace

```bash
cp -r /tmp/hal-backup/* ~/.openclaw/workspace/
cd ~/.openclaw/workspace
```

### Step 3: Verify files restored

```bash
ls -lah MEMORY.md projects.md dashboard.html
cat MEMORY.md | head -20
```

You should see all three files intact.

### Step 4: Restart dashboard service

```bash
sudo systemctl restart dashboard.service
```

### Step 5: Check dashboard loads

Visit: `http://187.124.93.142:8000/dashboard.html`

Should load normally.

---

## Full Restoration (if Docker container lost)

If the entire Docker container is gone, you'll need to restore the whole OpenClaw workspace:

### Step 1: Install OpenClaw (if not already)

```bash
npm install -g openclaw
openclaw init
```

### Step 2: Clone backup to OpenClaw workspace

```bash
rm -rf ~/.openclaw/workspace
git clone https://github.com/compuxparts1-svg/arcadegamecave-dashboard.git ~/.openclaw/workspace
cd ~/.openclaw/workspace
```

### Step 3: Set up git auto-pull (if needed)

```bash
chmod +x ~/.openclaw/workspace/auto-pull.sh
nohup ~/.openclaw/workspace/auto-pull.sh > /tmp/auto-pull.log 2>&1 &
```

### Step 4: Start dashboard service

```bash
sudo systemctl start dashboard.service
```

### Step 5: Verify

```bash
sudo systemctl status dashboard.service
curl http://localhost:8000/dashboard.html | head
```

---

## What's Backed Up

✅ **MEMORY.md** — Long-term memory + business context
✅ **projects.md** — All 11 active projects with status
✅ **dashboard.html** — Visual project dashboard
✅ **AGENTS.md, SOUL.md, IDENTITY.md, USER.md, etc.** — OpenClaw workspace files
✅ **Git history** — Full version control (can restore any past version)

---

## What's NOT Backed Up (Secrets)

❌ `.env` files (API keys, tokens)
❌ `ebay-config.js` (eBay OAuth token)
❌ `.agentmail-api-key` (AgentMail credentials)
❌ SSH keys

**These need to be re-added manually after restore.**

### Re-add Secrets After Restore

1. **eBay OAuth token:** Ask Jason for the token, then:
   ```bash
   openclaw models auth paste-token --provider openrouter
   ```

2. **AgentMail API key:** Create new at https://console.agentmail.to and save:
   ```bash
   echo "your-api-key" > ~/.agentmail-api-key
   chmod 600 ~/.agentmail-api-key
   ```

3. **GitHub SSH key:** Re-generate if needed:
   ```bash
   ssh-keygen -t ed25519 -C "hal@arcadegamecave.local" -f ~/.ssh/github_key -N ""
   cat ~/.ssh/github_key.pub
   # Add to https://github.com/settings/ssh/new
   ```

---

## Rollback to Previous Version

If you need to restore a specific past version:

```bash
cd ~/.openclaw/workspace
git log --oneline
git checkout <commit-hash>
```

Example:
```bash
git checkout 1c6bd60  # Restore to "Remove eBay secrets" version
```

---

## Emergency Contacts

- **GitHub Repo:** https://github.com/compuxparts1-svg/arcadegamecave-dashboard
- **Dashboard:** http://187.124.93.142:8000/dashboard.html
- **VPS:** srv1468259.hstgr.cloud (187.124.93.142)

---

## Maintenance Reminders

- ✅ **Auto-sync:** Git pulls every 60 seconds (auto-pull.sh)
- ✅ **Dashboard Service:** Runs automatically on VPS reboot (systemd)
- ✅ **GitHub:** Primary backup — always check here first
- ✅ **Version History:** Can restore any commit from git history

---

**Last Updated:** 2026-03-07 14:17 EST
**Backup Status:** ✅ Live and synced to GitHub
