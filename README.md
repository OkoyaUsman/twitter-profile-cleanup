# Twitter Profile Cleanup Bot

A simple Python tool to clean up your entire Twitter/X profile by deleting all tweets and unretweeting all retweets.

## Features

- 🗑️ Delete all tweets from your account
- 🔄 Unretweet all retweets
- ⚡ Batch processing with automatic rate limiting
- 🔒 Uses your own credentials (no third-party authentication)

## Requirements

- Python 3.x
- `curl_cffi` library

Install dependencies:
```bash
pip install curl_cffi
```

## Getting Your Credentials

To use this bot, you need three pieces of information:

1. **Username**: Your Twitter/X username (without the @)
2. **Auth Token**: Your account's authentication token
3. **CT0 Token**: Your CSRF token (also called ct0)

### How to Get Your Tokens

1. Open your browser and log in to [Twitter/X](https://x.com)
2. Open Developer Tools (F12 or right-click → Inspect)
3. Go to the **Application** tab (Chrome) or **Storage** tab (Firefox)
4. In the left sidebar, expand **Cookies** → `https://x.com`
5. Find and copy the following cookies:
   - `auth_token` - This is your authentication token
   - `ct0` - This is your CSRF token
6. Note your username (without the @ symbol)

⚠️ **Important**: Keep these credentials secure and never share them publicly!

## Usage

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd twitter-profile-cleanup
   ```

2. Install dependencies:
   ```bash
   pip install curl_cffi
   ```

3. Open `bot.py` and fill in your credentials at the top of the file:
   ```python
   username = "your_username"
   token = "your_auth_token"
   ct0 = "your_ct0_token"
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## How It Works

The bot processes your account in batches:

1. **Deleting Tweets**:
   - Fetches your tweets in batches of 20
   - Deletes each tweet with a 5-10 second delay between deletions
   - Waits 15-20 seconds between batches
   - Continues until all tweets are deleted

2. **Unretweeting**:
   - Fetches all your retweets in batches of 20
   - Unretweets each one with a 5-10 second delay
   - Waits 15-20 seconds between batches
   - Continues until all retweets are removed

The delays are built-in to avoid rate limiting by Twitter's API.

## Important Notes

- ⚠️ **This action is irreversible** - Once tweets are deleted, they cannot be recovered
- The bot includes rate limiting to avoid being blocked by Twitter
- Processing time depends on how many tweets/retweets you have
- Make sure your credentials are valid and up-to-date
- The bot will pause and wait for you to press Enter before exiting

## Troubleshooting

- **"Failed to get tweet details"**: Check that your credentials are correct and not expired
- **Rate limiting**: The bot includes delays, but if you still hit limits, wait a bit and try again
- **Token expired**: Re-fetch your tokens from browser cookies if they expire

## License

See [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for personal use only. Use at your own risk. The authors are not responsible for any account restrictions or actions taken by Twitter/X.