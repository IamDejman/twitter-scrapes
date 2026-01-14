#!/usr/bin/env python3
"""
Twitter Job Posting to Slack Bot
Fetches job postings from Twitter/X and posts them to a Slack channel
"""

import os
import json
import tweepy
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Set
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TwitterJobBot:
    def __init__(self):
        """Initialize the bot with API credentials from environment variables"""
        # Twitter/X API credentials
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # Slack webhook URL
        self.slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
        
        # Storage file for posted job IDs
        self.posted_jobs_file = 'posted_jobs.json'
        
        # Initialize Twitter client
        self.client = tweepy.Client(bearer_token=self.bearer_token)
        
        # Load previously posted jobs
        self.posted_jobs = self._load_posted_jobs()
    
    def _load_posted_jobs(self) -> Set[str]:
        """Load previously posted job IDs from file"""
        if os.path.exists(self.posted_jobs_file):
            with open(self.posted_jobs_file, 'r') as f:
                data = json.load(f)
                return set(data.get('posted_ids', []))
        return set()
    
    def _save_posted_jobs(self):
        """Save posted job IDs to file"""
        with open(self.posted_jobs_file, 'w') as f:
            json.dump({
                'posted_ids': list(self.posted_jobs),
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
    
    def search_jobs(self, keywords: List[str], max_results: int = 20) -> List[Dict]:
        """
        Search Twitter for job postings
        
        Args:
            keywords: List of keywords/hashtags to search for
            max_results: Maximum number of results to return
        
        Returns:
            List of tweet dictionaries
        """
        # Build search query
        query = ' OR '.join(keywords)
        
        # Search for tweets from the last 24 hours
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'entities'],
                expansions=['author_id'],
                user_fields=['username', 'name']
            )
            
            if not tweets.data:
                print("No tweets found")
                return []
            
            # Create user lookup dictionary
            users = {}
            if tweets.includes and 'users' in tweets.includes:
                users = {user.id: user for user in tweets.includes['users']}
            
            # Format results
            results = []
            for tweet in tweets.data:
                # Skip if already posted
                if tweet.id in self.posted_jobs:
                    continue
                
                author = users.get(tweet.author_id)
                results.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'author_name': author.name if author else 'Unknown',
                    'author_username': author.username if author else 'unknown',
                    'url': f"https://twitter.com/{author.username}/status/{tweet.id}" if author else None,
                    'likes': tweet.public_metrics['like_count'] if tweet.public_metrics else 0,
                    'retweets': tweet.public_metrics['retweet_count'] if tweet.public_metrics else 0
                })
            
            return results
        
        except Exception as e:
            print(f"Error searching tweets: {e}")
            return []
    
    def filter_relevant_jobs(self, tweets: List[Dict], filters: Dict) -> List[Dict]:
        """
        Filter tweets to only include relevant job postings
        
        Args:
            tweets: List of tweet dictionaries
            filters: Dictionary with 'include' and 'exclude' keyword lists
        
        Returns:
            Filtered list of tweets
        """
        relevant = []
        
        include_keywords = [k.lower() for k in filters.get('include', [])]
        exclude_keywords = [k.lower() for k in filters.get('exclude', [])]
        
        for tweet in tweets:
            text_lower = tweet['text'].lower()
            
            # Check if tweet contains any include keywords
            has_include = any(keyword in text_lower for keyword in include_keywords) if include_keywords else True
            
            # Check if tweet contains any exclude keywords
            has_exclude = any(keyword in text_lower for keyword in exclude_keywords)
            
            if has_include and not has_exclude:
                relevant.append(tweet)
        
        return relevant
    
    def post_to_slack(self, tweet: Dict) -> bool:
        """
        Post a job to Slack
        
        Args:
            tweet: Tweet dictionary
        
        Returns:
            True if successful, False otherwise
        """
        # Format the Slack message
        message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🎯 New Job Posting Found"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Posted by:*\n{tweet['author_name']} (@{tweet['author_username']})"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Date:*\n{tweet['created_at'].strftime('%Y-%m-%d %H:%M UTC')}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Job Description:*\n{tweet['text'][:500]}{'...' if len(tweet['text']) > 500 else ''}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"💙 {tweet['likes']} | 🔁 {tweet['retweets']}"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View on Twitter"
                            },
                            "url": tweet['url'],
                            "style": "primary"
                        }
                    ]
                },
                {
                    "type": "divider"
                }
            ]
        }
        
        try:
            response = requests.post(
                self.slack_webhook,
                json=message,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"✅ Posted job {tweet['id']} to Slack")
                return True
            else:
                print(f"❌ Failed to post to Slack: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            print(f"❌ Error posting to Slack: {e}")
            return False
    
    def run(self, search_keywords: List[str], filter_config: Dict, max_results: int = 20):
        """
        Main execution method
        
        Args:
            search_keywords: Keywords to search for on Twitter
            filter_config: Filter configuration with 'include' and 'exclude' lists
            max_results: Maximum number of tweets to fetch
        """
        print(f"\n{'='*60}")
        print(f"Twitter Job Bot - Running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Search for jobs
        print(f"🔍 Searching for: {', '.join(search_keywords)}")
        tweets = self.search_jobs(search_keywords, max_results)
        print(f"📊 Found {len(tweets)} total tweets")
        
        if not tweets:
            print("No new tweets found. Exiting.")
            return
        
        # Filter relevant jobs
        print(f"🔎 Applying filters...")
        relevant_tweets = self.filter_relevant_jobs(tweets, filter_config)
        print(f"✅ {len(relevant_tweets)} relevant jobs after filtering")
        
        # Post to Slack
        posted_count = 0
        for tweet in relevant_tweets:
            if self.post_to_slack(tweet):
                self.posted_jobs.add(tweet['id'])
                posted_count += 1
                time.sleep(1)  # Rate limiting
        
        # Save posted jobs
        self._save_posted_jobs()
        
        print(f"\n✨ Summary: Posted {posted_count} new jobs to Slack")
        print(f"{'='*60}\n")


def main():
    """Main entry point"""
    # Initialize bot
    bot = TwitterJobBot()

    # Configure search keywords (hashtags and terms) covering all career pathways
    # Note: Twitter API has a 512 character limit for search queries
    # Using most popular and broad hashtags to capture maximum jobs
    search_keywords = [
        '#NigeriaJobs',
        '#TechJobsNigeria',
        '#LagosJobs',
        '#RemoteJobs',
        '#hiring',
        '#JobOpening',
        '#FintechJobs',
        '#DataScience',
        '#DevOps',
        '#ProductManager',
        '#UIUX',
        '#SalesJobs',
        '#Marketing',
        '#HealthcareJobs'
    ]

    # Configure filters - comprehensive list covering all pathways
    filter_config = {
        'include': [
            # Tech & Digital
            'AI', 'ML', 'machine learning', 'artificial intelligence',
            'animation', 'animator', '3D artist', 'motion graphics',
            'cyber security', 'security analyst', 'penetration tester', 'InfoSec',
            'game developer', 'game designer', 'unity', 'unreal',
            'data scientist', 'data analyst', 'data engineer',
            'cloud', 'AWS', 'Azure', 'GCP', 'DevOps',
            'data visualization', 'business intelligence', 'BI',
            'product manager', 'product management', 'PM',
            'UI designer', 'UX designer', 'product designer',
            'DevOps engineer', 'SRE', 'infrastructure',
            'software developer', 'software engineer', 'programmer',
            'frontend', 'backend', 'full stack', 'fullstack',
            'QA', 'quality assurance', 'test engineer', 'SDET',
            'blockchain', 'web3', 'smart contract', 'solidity',
            'IoT', 'embedded systems', 'firmware',
            'robotics', 'automation engineer',

            # Business & Sales
            'sales', 'business development', 'account manager',
            'customer service', 'customer support', 'client relations',
            'hospitality', 'hotel', 'tourism', 'travel',
            'marketing', 'digital marketing', 'content marketing',
            'social media', 'brand manager', 'advertising',
            'NGO', 'non profit', 'nonprofit', 'development sector',

            # Finance & Accounting
            'banking', 'finance', 'financial analyst', 'fintech',
            'accounting', 'accountant', 'auditor', 'tax',
            'audit', 'internal audit', 'external audit',

            # Industry-specific
            'agriculture', 'agribusiness', 'farming', 'agritech',
            'retail', 'FMCG', 'consumer goods',
            'logistics', 'supply chain', 'procurement', 'operations',
            'climate', 'sustainability', 'ESG', 'renewable energy',
            'policy', 'public sector', 'government', 'civil service',
            'healthcare', 'medical', 'nursing', 'pharmacy', 'doctor',
            'care', 'caregiver', 'health worker',
            'education', 'teacher', 'instructor', 'training',
            'EdTech', 'learning',
            'construction', 'infrastructure', 'civil engineer',
            'project manager', 'site engineer',
            'manufacturing', 'industrial', 'production', 'factory',
            'mining', 'oil and gas', 'petroleum', 'geologist',
            'renewable', 'solar', 'wind energy', 'clean energy',
            'real estate', 'property', 'facility management',

            # General terms
            'hiring', 'job opening', 'vacancy', 'we are hiring',
            'nigeria', 'lagos', 'abuja', 'port harcourt',
            'remote', 'hybrid', 'full-time', 'permanent'
        ],
        'exclude': [
            'internship',  # Remove if you want internships
            'volunteer',
            'unpaid',
            'commission only'
        ]
    }

    # Run the bot
    bot.run(
        search_keywords=search_keywords,
        filter_config=filter_config,
        max_results=100  # Increased to fetch more tweets covering all pathways
    )


if __name__ == '__main__':
    main()
