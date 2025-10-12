# 🔗 Kaggle + Google Drive Integration

**ดึงวิดีโอจาก Google Drive ไปใช้ใน Kaggle โดยไม่ต้อง upload ใหม่!**

---

## 🎯 ทำไมต้องใช้ Drive Integration?

### ปัญหาของการ upload ไปที่ Kaggle Dataset โดยตรง:

❌ **ช้า** - Upload วิดีโอขนาดใหญ่ใช้เวลานาน (1 GB = 5-10 นาที)
❌ **จำกัด** - Kaggle Dataset limit = 100 GB
❌ **ซ้ำซ้อน** - วิดีโออยู่ Drive แล้ว ต้อง upload ซ้ำ
❌ **ไม่ sync** - แก้ไขใน Drive ต้อง upload ใหม่ทั้งหมด

### ข้อดีของการใช้ Drive Integration:

✅ **เร็ว** - Mount Drive แล้วใช้เลย (30 วินาที)
✅ **ไม่จำกัด** - ใช้พื้นที่ Google Drive (15 GB ฟรี)
✅ **Sync อัตโนมัติ** - ไฟล์ใหม่ปรากฏทันที
✅ **จัดการง่าย** - จัดโฟลเดอร์บน Drive ได้เลย

---

## 🚀 Quick Setup (3 ขั้นตอน)

### ขั้นตอนที่ 1: เปิด Google Drive API (ครั้งเดียว)

1. ไปที่ https://console.cloud.google.com/
2. สร้าง Project ใหม่ หรือเลือก project ที่มี
3. Enable Google Drive API:
   - APIs & Services → Library
   - ค้นหา "Google Drive API"
   - Click **Enable**

### ขั้นตอนที่ 2: Get OAuth Credentials

1. APIs & Services → **Credentials**
2. Create Credentials → **OAuth 2.0 Client IDs**
3. Application type: **Desktop app**
4. Name: `Kaggle Video Transcriber`
5. Click **Create**
6. Download JSON → เก็บไว้ปลอดภัย

### ขั้นตอนที่ 3: Upload Credentials ไป Kaggle

**Method A: As Kaggle Secret** (Recommended - ปลอดภัยที่สุด)

1. ไปที่ https://www.kaggle.com/settings
2. Scroll ลงไปที่ **Secrets**
3. Add New Secret:
   - Label: `GDRIVE_CREDENTIALS`
   - Value: วาง JSON credentials ทั้งหมด
4. Click **Add**

**Method B: As Kaggle Dataset** (Alternative)

1. สร้าง Kaggle Dataset ชื่อ `gdrive-credentials`
2. Upload `credentials.json`
3. Set เป็น **Private**

---

## 📝 ใช้งานใน Kaggle Notebook

### Cell 1: Mount Google Drive

```python
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os

# Authenticate with Google Drive
auth.authenticate_user()

print("✅ Google Drive authenticated!")
print("   You can now access files from your Drive")
```

**หรือใช้ PyDrive** (Recommended):

```python
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# Authenticate
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

print("✅ Google Drive connected!")
```

### Cell 2: List Files in Drive

```python
# List all MP4 files in your Drive
file_list = drive.ListFile({
    'q': "mimeType='video/mp4' and trashed=false"
}).GetList()

print("📹 Videos found in Google Drive:")
print("=" * 70)

for i, file in enumerate(file_list, 1):
    file_size = int(file['fileSize']) / (1024 * 1024)  # MB
    print(f"{i}. {file['title']}")
    print(f"   Size: {file_size:.1f} MB")
    print(f"   ID: {file['id']}")
    print()

# Or list files in specific folder
folder_id = 'YOUR_FOLDER_ID_HERE'  # Get from Drive URL

file_list = drive.ListFile({
    'q': f"'{folder_id}' in parents and mimeType='video/mp4' and trashed=false"
}).GetList()
```

### Cell 3: Download Video from Drive

```python
# Option A: Download by File ID
file_id = 'YOUR_FILE_ID_HERE'  # From previous cell

file = drive.CreateFile({'id': file_id})
filename = file['title']

print(f"📥 Downloading: {filename}")
print(f"   Size: {int(file['fileSize'])/(1024*1024):.1f} MB")

# Download to Kaggle working directory
output_path = f"/kaggle/working/{filename}"
file.GetContentFile(output_path)

print(f"✅ Downloaded: {output_path}")

# Option B: Download by filename
def download_video_by_name(video_name):
    """Download video from Drive by filename"""
    file_list = drive.ListFile({
        'q': f"title='{video_name}' and mimeType='video/mp4' and trashed=false"
    }).GetList()

    if not file_list:
        print(f"❌ Video not found: {video_name}")
        return None

    file = file_list[0]
    output_path = f"/kaggle/working/{video_name}"

    print(f"📥 Downloading: {video_name}")
    file.GetContentFile(output_path)

    print(f"✅ Downloaded: {output_path}")
    return output_path

# Use it
video_path = download_video_by_name("ep-01-19-12-24.mp4")
```

### Cell 4: Transcribe (ใช้ไฟล์จาก Drive)

```python
from whisper_kaggle_optimized import KaggleWhisperTranscriber

# Now use the downloaded video
transcriber = KaggleWhisperTranscriber(
    model_name="large-v3",
    device="auto",
    checkpoint_dir="/kaggle/working/checkpoints"
)

result = transcriber.transcribe_with_resume(
    video_path=video_path  # From Drive!
)

print(f"\n✅ Transcription complete!")
print(f"   Output: {result['final_file']}")
```

---

## 🎯 Complete Workflow: Drive → Kaggle → Transcribe

### Full Example Notebook Cell

```python
# ===================================================================
# COMPLETE WORKFLOW: Google Drive → Kaggle → Transcribe
# ===================================================================

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
from pathlib import Path

print("=" * 70)
print("KAGGLE + GOOGLE DRIVE TRANSCRIPTION")
print("=" * 70)

# Step 1: Authenticate Google Drive
print("\n[1/5] Authenticating Google Drive...")
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
print("✅ Connected to Google Drive")

# Step 2: Configure video
VIDEO_NAME = "ep-01-19-12-24.mp4"  # ← Change this!
# OR use folder ID:
# DRIVE_FOLDER_ID = "YOUR_FOLDER_ID"

print(f"\n[2/5] Searching for video: {VIDEO_NAME}")

# Search for video
file_list = drive.ListFile({
    'q': f"title='{VIDEO_NAME}' and mimeType='video/mp4' and trashed=false"
}).GetList()

if not file_list:
    print(f"❌ Video not found: {VIDEO_NAME}")
    print("\nAvailable videos:")

    all_videos = drive.ListFile({
        'q': "mimeType='video/mp4' and trashed=false"
    }).GetList()

    for f in all_videos[:10]:
        print(f"  - {f['title']}")

else:
    file = file_list[0]
    file_size = int(file['fileSize']) / (1024 * 1024)

    print(f"✅ Found: {file['title']}")
    print(f"   Size: {file_size:.1f} MB")
    print(f"   ID: {file['id']}")

    # Step 3: Download from Drive
    print(f"\n[3/5] Downloading from Google Drive...")
    output_path = f"/kaggle/working/{VIDEO_NAME}"

    file.GetContentFile(output_path)

    downloaded_size = Path(output_path).stat().st_size / (1024 * 1024)
    print(f"✅ Downloaded: {downloaded_size:.1f} MB")
    print(f"   Path: {output_path}")

    # Step 4: Transcribe
    print(f"\n[4/5] Starting transcription...")

    from whisper_kaggle_optimized import KaggleWhisperTranscriber

    transcriber = KaggleWhisperTranscriber(
        model_name="large-v3",
        device="auto",
        checkpoint_dir="/kaggle/working/checkpoints"
    )

    result = transcriber.transcribe_with_resume(video_path=output_path)

    # Step 5: Upload transcript back to Drive (optional)
    print(f"\n[5/5] Uploading transcript to Google Drive...")

    transcript_file = drive.CreateFile({
        'title': f"{Path(VIDEO_NAME).stem}_transcript.json",
        'parents': [{'id': file['parents'][0]['id']}]  # Same folder
    })

    transcript_file.SetContentFile(result['final_file'])
    transcript_file.Upload()

    print(f"✅ Uploaded transcript to Google Drive")
    print(f"   File ID: {transcript_file['id']}")

    # Final summary
    print("\n" + "=" * 70)
    print("✅ COMPLETE!")
    print("=" * 70)
    print(f"Video: {VIDEO_NAME}")
    print(f"Segments: {len(result['segments'])}")
    print(f"Duration: {result['metadata']['duration']:.1f}s")
    print(f"\nLocal file: {result['final_file']}")
    print(f"Google Drive: {transcript_file['title']}")
    print("=" * 70)
```

---

## 📁 Organize Videos in Google Drive

### Recommended Folder Structure:

```
My Drive/
└── Thai Videos/
    ├── 2024/
    │   ├── 01-January/
    │   │   ├── ep-01-19-12-24.mp4
    │   │   └── ep-02-20-12-24.mp4
    │   └── 02-February/
    │       └── ep-03-01-02-25.mp4
    │
    └── Transcripts/  ← Kaggle uploads here
        ├── ep-01-19-12-24_transcript.json
        ├── ep-02-20-12-24_transcript.json
        └── ep-03-01-02-25_transcript.json
```

### Get Folder ID from URL:

```
https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j
                                         ↑
                                    This is Folder ID
```

### List Videos in Folder:

```python
FOLDER_ID = "1a2b3c4d5e6f7g8h9i0j"  # Your folder ID

videos = drive.ListFile({
    'q': f"'{FOLDER_ID}' in parents and mimeType='video/mp4' and trashed=false"
}).GetList()

for video in videos:
    print(f"📹 {video['title']}")
    print(f"   Size: {int(video['fileSize'])/(1024*1024):.1f} MB")
    print(f"   ID: {video['id']}")
    print()
```

---

## 🎛️ Advanced: Batch Process All Videos in Folder

```python
def process_all_videos_in_folder(folder_id, output_folder_id=None):
    """
    Process all MP4 videos in a Google Drive folder

    Args:
        folder_id: Google Drive folder ID with videos
        output_folder_id: Google Drive folder ID for transcripts (optional)
    """
    from whisper_kaggle_optimized import KaggleWhisperTranscriber

    # List all videos
    videos = drive.ListFile({
        'q': f"'{folder_id}' in parents and mimeType='video/mp4' and trashed=false"
    }).GetList()

    print(f"📹 Found {len(videos)} videos in folder")
    print("=" * 70)

    # Initialize transcriber once
    transcriber = KaggleWhisperTranscriber(
        model_name="large-v3",
        device="auto",
        checkpoint_dir="/kaggle/working/checkpoints"
    )

    results = []

    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] Processing: {video['title']}")
        print("-" * 70)

        # Download
        local_path = f"/kaggle/working/{video['title']}"
        video.GetContentFile(local_path)
        print(f"✅ Downloaded: {video['title']}")

        # Transcribe
        result = transcriber.transcribe_with_resume(local_path)
        print(f"✅ Transcribed: {len(result['segments'])} segments")

        # Upload transcript back to Drive
        if output_folder_id:
            transcript_name = f"{Path(video['title']).stem}_transcript.json"

            transcript_file = drive.CreateFile({
                'title': transcript_name,
                'parents': [{'id': output_folder_id}]
            })

            transcript_file.SetContentFile(result['final_file'])
            transcript_file.Upload()

            print(f"✅ Uploaded to Drive: {transcript_name}")

        results.append({
            'video': video['title'],
            'segments': len(result['segments']),
            'duration': result['metadata']['duration'],
            'transcript': result['final_file']
        })

        # Clean up local file to save space
        os.remove(local_path)
        print(f"🧹 Cleaned up: {video['title']}")

    print("\n" + "=" * 70)
    print(f"✅ BATCH COMPLETE: {len(results)} videos processed")
    print("=" * 70)

    for r in results:
        print(f"📹 {r['video']}")
        print(f"   Segments: {r['segments']}")
        print(f"   Duration: {r['duration']:.1f}s")
        print()

    return results

# Use it
VIDEO_FOLDER_ID = "YOUR_VIDEO_FOLDER_ID"
TRANSCRIPT_FOLDER_ID = "YOUR_TRANSCRIPT_FOLDER_ID"

results = process_all_videos_in_folder(
    folder_id=VIDEO_FOLDER_ID,
    output_folder_id=TRANSCRIPT_FOLDER_ID
)
```

---

## 💡 Pro Tips

### Tip 1: Share Drive Folder Link

แทนที่จะใส่ Folder ID, ใช้ link:

```python
def get_folder_id_from_url(drive_url):
    """Extract folder ID from Google Drive URL"""
    if '/folders/' in drive_url:
        return drive_url.split('/folders/')[1].split('?')[0]
    return None

# Use it
drive_url = "https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j"
folder_id = get_folder_id_from_url(drive_url)
```

### Tip 2: Cache Downloaded Videos

```python
# Check if already downloaded
if os.path.exists(f"/kaggle/working/{video_name}"):
    print(f"✅ Using cached: {video_name}")
    video_path = f"/kaggle/working/{video_name}"
else:
    # Download from Drive
    video_path = download_from_drive(video_name)
```

### Tip 3: Resume Download (for large files)

```python
from googleapiclient.http import MediaIoBaseDownload

def download_large_file(file_id, output_path):
    """Download large files with progress bar"""
    request = drive.auth.service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Download {int(status.progress() * 100)}%")

    print(f"✅ Downloaded: {output_path}")
```

### Tip 4: Auto-detect New Videos

```python
# Get last processed timestamp
last_check = "2025-10-04T00:00:00Z"

# Find new videos since last check
new_videos = drive.ListFile({
    'q': f"mimeType='video/mp4' and modifiedDate > '{last_check}' and trashed=false"
}).GetList()

print(f"🆕 Found {len(new_videos)} new videos since {last_check}")
```

---

## 🔒 Security Best Practices

### 1. Never Share Credentials Publicly

```python
# ❌ WRONG - Don't hardcode
CREDENTIALS = {"client_id": "secret123"}

# ✅ RIGHT - Use Kaggle Secrets
from kaggle_secrets import UserSecretsClient
secrets = UserSecretsClient()
credentials = secrets.get_secret("GDRIVE_CREDENTIALS")
```

### 2. Use Kaggle Secrets for Folder IDs

```python
# Store folder IDs as secrets
VIDEO_FOLDER_ID = secrets.get_secret("VIDEO_FOLDER_ID")
TRANSCRIPT_FOLDER_ID = secrets.get_secret("TRANSCRIPT_FOLDER_ID")
```

### 3. Set Correct Permissions

- Credentials: **Private** Kaggle Dataset
- Video folder: **Private** or **Shared with specific people**
- Transcript folder: **Private**

---

## 🐛 Troubleshooting

### Issue 1: "Authentication failed"

**Solution**:
```python
# Re-authenticate
from google.colab import auth
auth.authenticate_user()

# Clear and re-create auth
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
```

### Issue 2: "File not found"

**Check**:
```python
# List all files to verify name
all_files = drive.ListFile({'q': "trashed=false"}).GetList()
for f in all_files:
    if 'ep-01' in f['title']:
        print(f"Found: {f['title']}")
```

### Issue 3: "Permission denied"

**Fix**:
1. Check file sharing settings in Google Drive
2. Make sure file is not "Restricted"
3. Re-authenticate with correct Google account

### Issue 4: Slow download

**Optimize**:
```python
# Use parallel download for multiple files
from concurrent.futures import ThreadPoolExecutor

def download_parallel(video_list, max_workers=3):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(download_video, v)
            for v in video_list
        ]

        for future in futures:
            future.result()
```

---

## 📊 Performance Comparison

| Method | Upload Time (1 GB) | Setup Time | Total Time |
|--------|-------------------|------------|------------|
| **Kaggle Dataset** | 5-10 min | 1 min | 6-11 min |
| **Google Drive** | 0 min (already there!) | 30 sec | 30 sec |

**Winner**: Google Drive (10-20x faster!)

---

## ✅ Complete Integration Checklist

### Setup (One-time):
- [ ] Enable Google Drive API
- [ ] Create OAuth credentials
- [ ] Add credentials to Kaggle Secrets
- [ ] Test authentication
- [ ] Organize videos in Drive folders

### Per Video:
- [ ] Open Kaggle notebook
- [ ] Run Drive authentication cell
- [ ] List/search for video
- [ ] Download from Drive (30 sec)
- [ ] Transcribe (3-6 min)
- [ ] Upload transcript back to Drive
- [ ] Clean up local files

**Total time**: 4-7 minutes (vs 15-20 with upload)

---

**Happy Transcribing with Google Drive + Kaggle! 🚀**

*No more duplicate uploads • Instant access • Sync automatically*

---

**Created**: 2025-10-04
**Version**: 1.0
**Purpose**: Google Drive integration for Kaggle transcription
