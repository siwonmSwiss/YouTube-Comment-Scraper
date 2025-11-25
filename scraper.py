"""
YouTube Comment Scraper to Excel
Extracts all comments from a YouTube video and exports to Excel
"""
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
from config import API_KEY

# Video Configuration
VIDEO_URL = "https://www.youtube.com/watch?v=BTmH6aKenK0"
VIDEO_ID = "BTmH6aKenK0"  # You can also change this directly

# Initialize YouTube API
youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_all_comments(video_id):
    """
    Fetches all comments (including replies) from a YouTube video
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        list: List of dictionaries containing comment data
    """
    comments_data = []
    
    print(f"Fetching comments for video ID: {video_id}...")
    
    try:
        # Initial request
        request = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        )
        
        response = request.execute()
        
        while response:
            for item in response['items']:
                # Top-level comment
                comment = item['snippet']['topLevelComment']['snippet']
                
                comments_data.append({
                    'Username': comment['authorDisplayName'],
                    'Comment': comment['textDisplay'],
                    'Likes': comment['likeCount'],
                    'Published At': comment['publishedAt'],
                    'Updated At': comment['updatedAt'],
                    'Reply Count': item['snippet']['totalReplyCount']
                })
                
                # Get replies if they exist
                if 'replies' in item:
                    for reply in item['replies']['comments']:
                        reply_snippet = reply['snippet']
                        comments_data.append({
                            'Username': f"  ↳ {reply_snippet['authorDisplayName']}",
                            'Comment': reply_snippet['textDisplay'],
                            'Likes': reply_snippet['likeCount'],
                            'Published At': reply_snippet['publishedAt'],
                            'Updated At': reply_snippet['updatedAt'],
                            'Reply Count': 0
                        })
            
            # Check if there are more comments
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=100,
                    pageToken=response['nextPageToken']
                )
                response = request.execute()
                print(f"Fetched {len(comments_data)} comments so far...")
            else:
                break
        
        print(f"Total comments fetched: {len(comments_data)}")
        return comments_data
    
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return []


def get_video_info(video_id):
    """
    Fetches basic information about the video
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: Video information including title, channel, stats
    """
    try:
        request = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        )
        response = request.execute()
        
        if response['items']:
            video = response['items'][0]
            return {
                'title': video['snippet']['title'],
                'channel': video['snippet']['channelTitle'],
                'views': video['statistics'].get('viewCount', 'N/A'),
                'likes': video['statistics'].get('likeCount', 'N/A'),
                'comments': video['statistics'].get('commentCount', 'N/A')
            }
    except Exception as e:
        print(f"Error fetching video info: {e}")
    
    return None


def export_to_excel(comments, video_id):
    """
    Exports comments to Excel file with formatting
    
    Args:
        comments (list): List of comment dictionaries
        video_id (str): Video ID for filename
        
    Returns:
        str: Filename of created Excel file
    """
    # Convert to DataFrame
    df = pd.DataFrame(comments)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filename = f"youtube_comments_{video_id}_{timestamp}.xlsx"
    
    # Export to Excel with formatting
    print(f"\nExporting to Excel: {excel_filename}")
    
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Comments', index=False)
        
        # Get the worksheet
        worksheet = writer.sheets['Comments']
        
        # Adjust column widths for readability
        worksheet.column_dimensions['A'].width = 25  # Username
        worksheet.column_dimensions['B'].width = 80  # Comment
        worksheet.column_dimensions['C'].width = 10  # Likes
        worksheet.column_dimensions['D'].width = 20  # Published At
        worksheet.column_dimensions['E'].width = 20  # Updated At
        worksheet.column_dimensions['F'].width = 12  # Reply Count
    
    return excel_filename


def main():
    """
    Main execution function
    """
    print("=" * 60)
    print("YouTube Comment Scraper to Excel")
    print("=" * 60)
    
    # Get video info
    video_info = get_video_info(VIDEO_ID)
    if video_info:
        print(f"\nVideo: {video_info['title']}")
        print(f"Channel: {video_info['channel']}")
        print(f"Views: {video_info['views']}")
        print(f"Likes: {video_info['likes']}")
        print(f"Total Comments: {video_info['comments']}")
        print()
    
    # Fetch all comments
    comments = get_all_comments(VIDEO_ID)
    
    if not comments:
        print("No comments found or error occurred.")
        return
    
    # Export to Excel
    excel_file = export_to_excel(comments, VIDEO_ID)
    
    print(f"✓ Successfully exported {len(comments)} comments to {excel_file}")
    print(f"\nFile saved in current directory")
    print("=" * 60)


if __name__ == "__main__":
    main()
