#  Football Scoreboard Video Generator

This Python script generates a **realistic American football scoreboard video** using OpenCV — complete with a live countdown clock, downs & distance, ball position, timeouts, and automatic score updates.

It’s ideal for:
- Testing **scoreboard tracking or OCR systems**
- Feeding **video input** for AI or broadcast automation
- Demonstrations of **sports graphics** or **StatCrew-style data displays**

---

## Features

Real-time **clock countdown** (1 second of game time per second of video)  
Dynamic **Down & Distance** and **Ball On** markers (update every 10s)  
**Home/Away** team display with changing scores  
**Timeout indicators** per team  
Clean, **high-contrast broadcast layout** (1920×1080)  
Adjustable **video duration** and **game start time**  

---

## Requirements

Install dependencies before running:

pip install opencv-python numpy

Running:
python scoreboard_bold.py

Output:
scoreboard_bold.mp4

You can modify key parameters near the top of the script:

Variable	Description	Example
video_length	Real video duration in seconds	60
fps	Frames per second	30
game_clock_start	Game clock start time (in seconds)	10*60 + 59
HOME_NAME, AWAY_NAME	Team names	"LIONS", "BOBCATS"
score_events	Timed score updates	[(18, "HOME", 3), (35, "AWAY", 7)]
ddb_pattern	Sequence of downs/yards/ball position	[(1,10,25), (2,6,29), ...]

Output Example
Resolution: 1920×1080 (16:9)
Format: MP4 (H.264 codec)
Style: Simplified digital scoreboard suitable for tracking systems
Behavior:
Game clock ticks down normally
Every 10s, the down & distance updates
Scores and timeouts adjust based on score_events
