# Monika.exe - DDLC Prank Game

A Doki Doki Literature Club inspired prank program featuring Monika.

**This is a HARMLESS prank program. It does NOT:**
- Corrupt any files
- Install actual malware
- Damage your computer
- It only creates .txt files on your desktop (which you can delete)

## Features

### Escalation System

| Stage | Duration | Behaviors |
|-------|----------|-----------|
| **1** | 30 sec | Greeting popups, "Just Monika" errors, mouse avoidance |
| **2** | 45 sec | Opens browser tabs, creates poem .txt files on desktop |
| **3** | 45 sec | More tabs, aggressive warning messages |
| **4** | 60 sec | Jumpscares, poems get spammed, weird/glitchy text |
| **5** | 2 min | Maximum escalation of everything |

After Stage 5: "Stay with me forever?" prompt
- **Yes** → Game closes peacefully with a thank you message
- **No** → Jumpscare sequence, then Stage 5 repeats

## Required Files

Place these in the same folder as `monika.py`:

### 1. `monika.png` - Transparent Overlay
**Recommended specs:**
- Size: ~300x400 pixels (or will be resized)
- Transparent background (PNG with alpha)
- Shows in bottom-right corner of screen

**Suggested image:** A cute/creepy Monika sprite looking at the viewer. Something like:
- Monika leaning forward with a smile
- Monika's "staring" pose from the game
- Can be slightly glitchy/corrupted looking

### 2. `jumpscare.png` - Main Jumpscare
**Recommended specs:**
- High resolution (will be stretched to fullscreen)
- Creepy/startling Monika image

**Suggested images:**
- Monika with glitched/distorted face
- Monika with realistic eyes edited in
- Monika with "yandere" expression
- Black background with red Monika silhouette
- Glitched classroom with Monika staring

### 3. `jumpscare1.png`, `jumpscare2.png` (Optional)
Extra jumpscare variants for variety.

## 🔧 Installation

### Step 1: Install Python
Download from https://python.org (make sure to check "Add to PATH")

### Step 2: Install Dependencies
Open Command Prompt in the game folder and run:
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install pyautogui pillow
```

### Step 3: Add Your Images
Put your image files in the same folder:
- `monika.png`
- `jumpscare.png`
- (optional) `jumpscare1.png`, `jumpscare2.png`

### Step 4: Customize (Optional)
Edit `monika.py` to:
- Add your own websites to `WEBSITES` list
- Change poem texts in `POEMS_STAGE2` and `POEMS_AGGRESSIVE`
- Adjust stage durations in `stage_duration`
- Modify error messages

## Running the Game

### Option A: Run Python directly
```bash
python monika.py
```

### Option B: Build to .exe
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   build.bat
   ```
   
   Or manually:
   ```bash
   python -m PyInstaller --onefile --noconsole --name "Monika" --icon "monika.ico" --add-data "monika.png;." --add-data "jumpscare.png;." --add-data "jumpscare1.png;." --add-data "jumpscare2.png;." --add-data "jumpscare.wav;." --add-data "error.wav;." --add-data "ambient.wav;." --add-data "laugh.wav;." --add-data "glitch.wav;." monika.py
   ```

3. Find your .exe in the `dist` folder

## Emergency Stop

- **Ctrl+C** in the terminal/command prompt
- **Task Manager** → End "Python" or "Monika.exe"
- **Alt+F4** might work on some windows

## Customization Tips

### Adding Websites
```python
WEBSITES = [
    "https://www.youtube.com/watch?v=YOUR_VIDEO_ID",
    "https://example.com",
    # Add more here
]
```

### Changing Timing
```python
self.stage_duration = {
    1: 30,   # Stage 1 lasts 30 seconds
    2: 45,   # Stage 2 lasts 45 seconds
    3: 45,   # etc.
    4: 60,
    5: 120,  # Final stage is 2 minutes
}
```

### Custom Poems
Add your own creepy poems to `POEMS_STAGE2` or `POEMS_AGGRESSIVE` lists.

## Where to Find Images

You can search for:
- "DDLC Monika sprite" (for overlay)
- "DDLC Monika jumpscare" (for scares)
- "Monika glitch" or "Monika creepy edit"
- Create your own edits using image editors

**Fair use note:** This is a fan project. Use fan-made sprites or create your own edits.

## Disclaimer

This is intended as a harmless prank for friends who enjoy DDLC horror elements.
- Don't use on people with heart conditions
- Don't use on people who don't like horror
- The recipient should be able to laugh about it afterward
- You are responsible for how you use this

---

*Just Monika.*
