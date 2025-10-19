import cv2
import numpy as np

# ================= CONFIG =================
video_length = 60          # seconds of *video* to export (change freely)
fps = 30
game_clock_start = 10*60 + 59  # 10:59 of game time, ticks at 1:1 speed
width, height = 1920, 1080

HOME_NAME = "HOME"
AWAY_NAME = "AWAY"

# Optional: starting scores and planned score events (time in seconds since video start)
home_score_start = 14
away_score_start = 10
score_events = [
    # (time_in_seconds, "HOME"/"AWAY", points)
    (18, "HOME", 3),   # HOME FG at 0:18
    (35, "AWAY", 7),   # AWAY TD at 0:35
    (52, "HOME", 7),   # HOME TD at 0:52
]
home_timeouts = 3
away_timeouts = 3
# ==========================================

font = cv2.FONT_HERSHEY_DUPLEX
total_frames = int(fps * video_length)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("scoreboard_generalized.mp4", fourcc, fps, (width, height))

# ---- 10-second cycle for Down/Distance & Ball Spot ----
# This pattern advances every 10 seconds of real time.
# It loops if your video is longer than the pattern.
ddb_pattern = [
    (1, 10, 25),
    (2, 6, 29),
    (3, 2, 33),
    (1, 10, 35),  # new set of downs
    (2, 8, 42),
    (3, 5, 47),
    (4, 1, 48),
    (1, 10, 32),  # possession plausibly flipped, but we keep it simple
]

def ordinal(n:int)->str:
    return f"{n}{'st' if n==1 else 'nd' if n==2 else 'rd' if n==3 else 'th'}"

def calc_scores(elapsed_s: float):
    """Compute scores based on threshold events without keeping mutable state."""
    home = home_score_start
    away = away_score_start
    for t, side, pts in score_events:
        if elapsed_s >= t:
            if side.upper() == "HOME":
                home += pts
            else:
                away += pts
    return home, away

for frame_num in range(total_frames):
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # ----- Timekeeping -----
    elapsed = frame_num / fps
    remaining_seconds = max(int(game_clock_start - elapsed), 0)
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    timer_text = f"{minutes}:{seconds:02d}"

    # ----- Down/Distance/Ball spot every 10s -----
    segment = int(elapsed // 10)  # 0,1,2,... advanced each 10 seconds
    d, ytg, ball = ddb_pattern[segment % len(ddb_pattern)]

    # ----- Scores (based on elapsed) -----
    home_score, away_score = calc_scores(elapsed)

    # ----- Panels -----
    cv2.rectangle(frame, (200, 250), (900, 550), (40, 40, 40), -1)     # HOME bg
    cv2.rectangle(frame, (1020, 250), (1720, 550), (40, 40, 40), -1)   # AWAY bg
    cv2.rectangle(frame, (200, 250), (900, 550), (200, 200, 200), 3)
    cv2.rectangle(frame, (1020, 250), (1720, 550), (200, 200, 200), 3)

    # ----- Team names & scores -----
    cv2.putText(frame, HOME_NAME, (230, 340), font, 3, (255, 255, 255), 6)
    cv2.putText(frame, str(home_score), (670, 500), font, 5, (255, 255, 255), 10)

    cv2.putText(frame, AWAY_NAME, (1040, 340), font, 3, (255, 255, 255), 6)
    cv2.putText(frame, str(away_score), (1460, 500), font, 5, (255, 255, 255), 10)

    # ----- Quarter & Clock -----
    cv2.putText(frame, "4TH QUARTER", (760, 640), font, 2, (255, 255, 255), 5)
    cv2.putText(frame, timer_text, (860, 760), font, 3, (255, 255, 255), 8)

    # ----- Down/Distance & Ball -----
    dd_text = f"{ordinal(d)} & {ytg}"
    cv2.putText(frame, dd_text, (400, 900), font, 2, (255, 255, 0), 5)
    cv2.putText(frame, f"Ball on {ball}", (920, 900), font, 2, (255, 255, 0), 5)

    # ----- Timeouts -----
    def draw_timeouts(x_start, y, count):
        for i in range(3):
            cx = x_start + i * 50
            filled = i < count
            cv2.circle(frame, (cx, y), 15, (255, 255, 255), -1 if filled else 3)

    draw_timeouts(280, 190, home_timeouts)
    draw_timeouts(1520, 190, away_timeouts)
    cv2.putText(frame, "TO", (220, 200), font, 1, (255, 255, 255), 2)
    cv2.putText(frame, "TO", (1660, 200), font, 1, (255, 255, 255), 2)

    # ----- Final flag if clock reaches 0 -----
    if remaining_seconds == 0:
        cv2.putText(frame, "FINAL", (830, 950), font, 3, (0, 255, 0), 8)

    out.write(frame)

out.release()
print("✅ scoreboard_generalized.mp4 created successfully.")
