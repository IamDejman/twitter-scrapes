# Twitter to Slack Job Posting Bot

Automatically fetch job postings from Twitter/X and post them to a Slack channel.

## Features

- 🔍 Searches Twitter for job postings using hashtags and keywords
- 🎯 Filters results based on your criteria (include/exclude keywords)
- 📢 Posts formatted job alerts to Slack with rich formatting
- 🚫 Prevents duplicate postings by tracking previously shared jobs
- ⏰ Runs automatically on a schedule via GitHub Actions
- 🔒 Secure credential management using environment variables

## Prerequisites

1. **Twitter/X API Access**
   - Apply at: https://developer.twitter.com/en/portal/dashboard
   - You'll need: API Key, API Secret, and Bearer Token
   - Free tier may be limited; Basic tier ($100/month) recommended for regular use

2. **Slack Workspace**
   - Admin access to create incoming webhooks
   - Target channel where jobs will be posted

3. **GitHub Account** (for automation)
   - Free account is sufficient

## Setup Instructions

### Step 1: Get Twitter/X API Credentials

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new app or use existing one
3. Navigate to "Keys and tokens" section
4. Generate/copy these credentials:
   - API Key
   - API Secret  
   - Bearer Token

### Step 2: Set Up Slack Webhook

1. Go to https://api.slack.com/messaging/webhooks
2. Click "Create New App" → "From scratch"
3. Name your app (e.g., "Job Bot") and select your workspace
4. Navigate to "Incoming Webhooks" and activate it
5. Click "Add New Webhook to Workspace"
6. Select the channel where jobs should be posted
7. Copy the webhook URL (starts with `https://hooks.slack.com/services/...`)

### Step 3: Local Setup

1. **Clone/Download this repository**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy the template
   cp .env.template .env
   
   # Edit .env and add your credentials
   nano .env  # or use any text editor
   ```

4. **Update .env file with your credentials:**
   ```bash
   TWITTER_API_KEY=your_actual_api_key
   TWITTER_API_SECRET=your_actual_api_secret
   TWITTER_BEARER_TOKEN=your_actual_bearer_token
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

5. **Customize search parameters** (optional)
   
   Edit `twitter_to_slack_jobs.py` and modify the `main()` function:
   
   ```python
   # Add your preferred hashtags and keywords
   search_keywords = [
       '#NigeriaJobs',
       '#TechJobsNigeria',
       '#ProductManager',
       # Add more...
   ]
   
   # Customize filters
   filter_config = {
       'include': ['product manager', 'fintech', 'nigeria'],
       'exclude': ['internship', 'unpaid']
   }
   ```

### Step 4: Test Locally

```bash
# Load environment variables and run
python twitter_to_slack_jobs.py
```

You should see output like:
```
============================================================
Twitter Job Bot - Running at 2025-01-14 10:30:00
============================================================

🔍 Searching for: #NigeriaJobs, #TechJobsNigeria, #hiring
📊 Found 15 total tweets
🔎 Applying filters...
✅ 8 relevant jobs after filtering
✅ Posted job 1234567890 to Slack
✅ Posted job 1234567891 to Slack

✨ Summary: Posted 8 new jobs to Slack
============================================================
```

### Step 5: Deploy to GitHub Actions (Automation)

1. **Create a new GitHub repository** and push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/twitter-job-bot.git
   git push -u origin main
   ```

2. **Add secrets to GitHub repository:**
   - Go to your repository on GitHub
   - Navigate to Settings → Secrets and variables → Actions
   - Click "New repository secret" and add each:
     - `TWITTER_API_KEY`
     - `TWITTER_API_SECRET`
     - `TWITTER_BEARER_TOKEN`
     - `SLACK_WEBHOOK_URL`

3. **Enable GitHub Actions:**
   - Go to the "Actions" tab in your repository
   - Enable workflows if prompted
   - The bot will now run automatically every 6 hours

4. **Manual trigger** (optional):
   - Go to Actions tab → Select "Twitter Job Bot" workflow
   - Click "Run workflow" to test immediately

## Configuration Options

### Adjusting Schedule

Edit `.github/workflows/job_bot.yml` to change frequency:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
    # Examples:
    # - cron: '0 9,17 * * *'  # 9 AM and 5 PM daily
    # - cron: '0 */4 * * *'   # Every 4 hours
    # - cron: '0 8 * * 1-5'   # 8 AM on weekdays
```

### Customizing Search Keywords

Common Nigerian tech job hashtags:
```python
search_keywords = [
    '#NigeriaJobs',
    '#TechJobsNigeria', 
    '#LagosJobs',
    '#AbujaJobs',
    '#RemoteNigeria',
    '#NigerianTech',
    '#hiring',
    '#JobOpening',
    '#WeAreHiring',
    'Fintech Nigeria hiring',
    'Product Manager Nigeria'
]
```

### Advanced Filtering

```python
filter_config = {
    'include': [
        'product manager',
        'product management',
        'PM role',
        'fintech',
        'payments',
        'lagos',
        'nigeria',
        'remote',
        'full-time'
    ],
    'exclude': [
        'internship',
        'intern',
        'volunteer',
        'unpaid',
        'contract only',
        'commission based'
    ]
}
```

## File Structure

```
.
├── twitter_to_slack_jobs.py    # Main bot script
├── requirements.txt             # Python dependencies
├── .env.template               # Environment template
├── .env                        # Your credentials (DO NOT COMMIT)
├── posted_jobs.json            # Tracks posted jobs (auto-generated)
├── .github/
│   └── workflows/
│       └── job_bot.yml         # GitHub Actions workflow
└── README.md                   # This file
```

## Troubleshooting

### "No tweets found"
- Check if your search keywords are too specific
- Verify Twitter API credentials are correct
- Check API rate limits in Twitter Developer Portal

### "Failed to post to Slack"
- Verify Slack webhook URL is correct
- Ensure the bot app has permission to post to the channel
- Check if webhook is still active in Slack settings

### GitHub Actions not running
- Verify secrets are added correctly (case-sensitive)
- Check Actions tab for error logs
- Ensure repository is not private (or enable Actions for private repos)

### Rate Limiting
- Twitter Free tier: 500,000 tweets/month (may be limited)
- Twitter Basic tier: Better for regular scraping
- Adjust `max_results` parameter to fetch fewer tweets per run

## Security Best Practices

- ✅ **NEVER** commit `.env` file to GitHub
- ✅ Use GitHub Secrets for credentials
- ✅ Rotate API keys regularly
- ✅ Review posted_jobs.json periodically and clean old entries
- ✅ Monitor API usage to avoid unexpected charges

## Cost Considerations

- **Twitter API Basic**: ~$100/month (recommended for regular use)
- **Twitter API Free**: Limited requests, may not be sufficient
- **Slack**: Free (webhooks are free)
- **GitHub Actions**: Free for public repos, 2000 min/month for private

## Customization Ideas

1. **Add more platforms**: Extend to search LinkedIn, Indeed APIs
2. **Email notifications**: Add email alerts for priority jobs
3. **Database storage**: Use PostgreSQL instead of JSON file
4. **Web dashboard**: Build a simple UI to manage filters
5. **ML filtering**: Add AI to better classify relevant jobs
6. **Application tracking**: Link to application status tracking

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review GitHub Actions logs
3. Test locally first before deploying

## License

MIT License - Feel free to modify and use for your needs.
