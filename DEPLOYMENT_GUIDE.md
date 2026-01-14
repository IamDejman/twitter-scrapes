# Deployment Guide - Twitter Job Bot to Slack

Follow these steps to deploy your bot and automate job posting to Slack.

## Prerequisites Checklist

- [ ] Twitter/X Developer Account
- [ ] Slack Workspace (with admin access)
- [ ] GitHub Account

---

## Step 1: Get Twitter/X API Credentials

1. Visit https://developer.twitter.com/en/portal/dashboard
2. Sign in or create a developer account
3. Create a new Project and App (or use existing)
4. Navigate to your app's "Keys and tokens" section
5. Copy these credentials (keep them safe):
   ```
   API Key: xxxxxxxxxxxxxxxxxxxxxxxx
   API Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   Bearer Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**Note:** Twitter's Free tier has limitations. Basic tier ($100/month) is recommended for regular use.

---

## Step 2: Set Up Slack Webhook

1. Go to https://api.slack.com/messaging/webhooks
2. Click **"Create New App"** → **"From scratch"**
3. App Name: `Job Bot` (or your preferred name)
4. Select your workspace
5. Click **"Incoming Webhooks"** from the left menu
6. Toggle **"Activate Incoming Webhooks"** to ON
7. Click **"Add New Webhook to Workspace"**
8. Select the channel where jobs should be posted (e.g., `#jobs`, `#opportunities`)
9. Copy the Webhook URL:
   ```
   https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
   ```

---

## Step 3: Test Locally (Recommended)

### 3.1 Create .env file

```bash
# In your project directory
cp .env.template .env
```

### 3.2 Edit .env file with your credentials

Open `.env` in a text editor and add your credentials:

```bash
TWITTER_API_KEY=your_actual_api_key_here
TWITTER_API_SECRET=your_actual_api_secret_here
TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 3.3 Install dependencies

```bash
pip install -r requirements.txt
```

### 3.4 Run the bot

```bash
python twitter_to_slack_jobs.py
```

You should see output like:
```
============================================================
Twitter Job Bot - Running at 2026-01-14 10:30:00
============================================================

🔍 Searching for: #NigeriaJobs, #TechJobsNigeria, #hiring...
📊 Found 25 total tweets
🔎 Applying filters...
✅ 15 relevant jobs after filtering
✅ Posted job 1234567890 to Slack
...

✨ Summary: Posted 15 new jobs to Slack
============================================================
```

Check your Slack channel to see if jobs were posted successfully!

---

## Step 4: Deploy to GitHub for Automation

### 4.1 Initialize Git Repository

```bash
# In your project directory
git init
git add .
git commit -m "Initial commit: Twitter job bot with all career pathways"
```

### 4.2 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `twitter-job-bot` (or your preferred name)
3. Make it **Private** (recommended) or Public
4. **DO NOT** initialize with README (we already have one)
5. Click **"Create repository"**

### 4.3 Push Code to GitHub

```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/twitter-job-bot.git
git branch -M main
git push -u origin main
```

---

## Step 5: Add Secrets to GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add each of these:

   **Secret 1:**
   - Name: `TWITTER_API_KEY`
   - Value: [Your Twitter API Key]

   **Secret 2:**
   - Name: `TWITTER_API_SECRET`
   - Value: [Your Twitter API Secret]

   **Secret 3:**
   - Name: `TWITTER_BEARER_TOKEN`
   - Value: [Your Twitter Bearer Token]

   **Secret 4:**
   - Name: `SLACK_WEBHOOK_URL`
   - Value: [Your Slack Webhook URL]

---

## Step 6: Enable GitHub Actions

1. Go to the **"Actions"** tab in your repository
2. If prompted, click **"I understand my workflows, go ahead and enable them"**
3. You should see the workflow: **"Twitter Job Bot"**

---

## Step 7: Test the Automated Workflow

### Option A: Manual Trigger (Recommended for first test)

1. Go to **Actions** tab
2. Click on **"Twitter Job Bot"** workflow
3. Click **"Run workflow"** dropdown
4. Click the green **"Run workflow"** button
5. Wait 1-2 minutes and refresh the page
6. Click on the running workflow to see logs
7. Check your Slack channel for new job postings

### Option B: Wait for Scheduled Run

The bot will automatically run every 6 hours based on this schedule:
- 12:00 AM UTC
- 6:00 AM UTC
- 12:00 PM UTC
- 6:00 PM UTC

---

## Step 8: Customize Schedule (Optional)

Edit `.github/workflows/job_bot.yml` to change the schedule:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Current: Every 6 hours
    # Examples:
    # - cron: '0 9,17 * * *'   # 9 AM and 5 PM daily
    # - cron: '0 */4 * * *'    # Every 4 hours
    # - cron: '0 8 * * 1-5'    # 8 AM on weekdays only
    # - cron: '0 */2 * * *'    # Every 2 hours
```

After editing, commit and push:
```bash
git add .github/workflows/job_bot.yml
git commit -m "Update schedule"
git push
```

---

## Troubleshooting

### No tweets found
- Search keywords may be too specific
- Check Twitter API credentials
- Verify API rate limits in Twitter Developer Portal

### Failed to post to Slack
- Verify Slack webhook URL is correct
- Check if webhook is still active
- Ensure bot has permission to post to channel

### GitHub Actions not running
- Verify all 4 secrets are added correctly (names are case-sensitive)
- Check Actions tab for error logs
- For private repos, ensure Actions are enabled

### Rate Limiting
- Twitter Free tier: Limited requests
- Twitter Basic tier: $100/month, better for regular use
- Reduce `max_results` in code if hitting limits

---

## Monitoring Your Bot

### View Execution History
1. Go to **Actions** tab
2. See all workflow runs with status (success/failure)
3. Click any run to see detailed logs

### Check Posted Jobs
- File `posted_jobs.json` tracks all posted job IDs
- Prevents duplicate postings
- Automatically updated by GitHub Actions

### Slack Notifications
- All new jobs appear in your selected channel
- Formatted with job details, author, and "View on Twitter" button

---

## Customization Tips

### Include Internships
Edit `twitter_to_slack_jobs.py` line 388-392:
```python
'exclude': [
    # 'internship',  # Commented out to include internships
    'volunteer',
    'unpaid'
]
```

### Add More Keywords
Add to `search_keywords` list (line 276) or `filter_config['include']` (line 334).

### Change Locations
Edit line 385:
```python
'nigeria', 'lagos', 'abuja', 'port harcourt', 'ibadan', 'kano'
```

---

## Cost Summary

- **Twitter API Basic**: ~$100/month (recommended)
- **Twitter API Free**: Limited requests
- **Slack**: Free (webhooks included)
- **GitHub Actions**: Free for public repos, 2000 min/month for private

---

## Security Best Practices

✅ Never commit `.env` file to GitHub
✅ Use GitHub Secrets for all credentials
✅ Keep repository private if storing sensitive configs
✅ Rotate API keys regularly
✅ Monitor API usage to avoid unexpected charges

---

## Success Checklist

- [ ] Twitter API credentials obtained
- [ ] Slack webhook created
- [ ] Bot tested locally successfully
- [ ] Code pushed to GitHub
- [ ] All 4 secrets added to GitHub
- [ ] GitHub Actions enabled
- [ ] First manual workflow run successful
- [ ] Jobs appearing in Slack channel

---

## Next Steps

Once deployed, your bot will:
1. Run automatically every 6 hours
2. Search Twitter for jobs across 35+ career pathways
3. Filter relevant postings
4. Post new jobs to your Slack channel
5. Track posted jobs to avoid duplicates

**You're all set! 🎉**

For issues, check the Troubleshooting section or review GitHub Actions logs.
