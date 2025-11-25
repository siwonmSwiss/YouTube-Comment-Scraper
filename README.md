# YouTube Comment Scraper to Excel

A simple Python tool to extract all comments from any YouTube video and export them to Excel format using the YouTube Data API v3.

## Features

- 🎯 Extract all comments and replies from YouTube videos
- 📊 Export to formatted Excel file (.xlsx)
- 👤 Includes username, comment text, likes, timestamps, and reply counts
- 🔄 Automatic pagination to fetch all comments
- 📈 Real-time progress updates
- 🎨 Auto-formatted Excel columns for easy reading

## Prerequisites

- Python 3.7 or higher
- YouTube Data API v3 key from [Google Cloud Console](https://console.cloud.google.com/)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/YouTube-Comment-Scraper.git
cd YouTube-Comment-Scraper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure your API key:
   - Copy `config.example.py` to `config.py`
   - Add your YouTube Data API key in `config.py`

```bash
cp config.example.py config.py
```

## Getting a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**
4. Create credentials (API Key)
5. Copy the API key to your `config.py` file

## Usage

### Basic Usage

Run the script with a YouTube video URL:

```bash
python scraper.py
```

The script will extract all comments from the configured video and save them to an Excel file.

### Customize Video URL

Edit the `VIDEO_URL` variable in `scraper.py`:

```python
VIDEO_URL = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

Or modify `VIDEO_ID` directly:

```python
VIDEO_ID = "YOUR_VIDEO_ID"
```

## Output

The script creates an Excel file with the following format:

- **Filename**: `youtube_comments_[VIDEO_ID]_[TIMESTAMP].xlsx`
- **Sheet Name**: Comments

### Columns:

| Column | Description |
|--------|-------------|
| Username | Comment author's display name |
| Comment | Full comment text (replies indented with ↳) |
| Likes | Number of likes on the comment |
| Published At | When the comment was posted |
| Updated At | Last update timestamp |
| Reply Count | Number of replies (for top-level comments) |

## Example Output

```
============================================================
YouTube Comment Extractor
============================================================

Video: Example Video Title
Channel: Channel Name
Views: 123456
Likes: 5678
Total Comments: 890

Fetching comments for video ID: abc123...
Fetched 100 comments so far...
Fetched 234 comments so far...
Total comments fetched: 234

✓ Successfully exported 234 comments to youtube_comments_abc123_20250125_101921.xlsx
============================================================
```

## Configuration

### config.py

```python
# Your YouTube Data API Key
API_KEY = "YOUR_API_KEY_HERE"
```

**⚠️ Important**: Never commit `config.py` to version control. It's included in `.gitignore`.

## API Rate Limits

The YouTube Data API v3 has quota limits:
- Default quota: 10,000 units per day
- Each comment fetch costs approximately 1-5 units
- Monitor your usage in the [Google Cloud Console](https://console.cloud.google.com/)

## Dependencies

- `google-api-python-client` - YouTube API interaction
- `pandas` - Data manipulation
- `openpyxl` - Excel file creation

See `requirements.txt` for specific versions.

## Troubleshooting

### "API key not valid" error
- Verify your API key in `config.py`
- Ensure YouTube Data API v3 is enabled in Google Cloud Console
- Check if your API key has the correct permissions

### "Comments are disabled" error
- The video has comments disabled
- Try a different video

### Rate limit exceeded
- You've reached your daily API quota
- Wait 24 hours or request a quota increase

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Disclaimer

This tool is for educational and research purposes. Always respect YouTube's Terms of Service and the privacy of content creators and commenters.

## Author

Created for easy YouTube comment analysis and research.

## Acknowledgments

- YouTube Data API v3 by Google
- Python community for excellent libraries
