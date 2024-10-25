import os, subprocess, time, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.step1_ytdlp import find_video_files
from rich import print as rprint
import cv2
import numpy as np

SRC_FONT_SIZE = 16
TRANS_FONT_SIZE = 18
FONT_NAME = 'Arial'
TRANS_FONT_NAME = 'Arial'
SRC_FONT_COLOR = '&HFFFFFF' 
SRC_OUTLINE_COLOR = '&H000000'
SRC_OUTLINE_WIDTH = 1
SRC_SHADOW_COLOR = '&H80000000'
TRANS_FONT_COLOR = '&H00FFFF'
TRANS_OUTLINE_COLOR = '&H000000'
TRANS_OUTLINE_WIDTH = 1 
TRANS_BACK_COLOR = '&H33000000'

def merge_subtitles_to_video():
    from config import RESOLUTION
    TARGET_WIDTH, TARGET_HEIGHT = RESOLUTION.split('x')
    video_file = find_video_files()
    output_video = "output/output_video_with_subs.mp4"
    os.makedirs(os.path.dirname(output_video), exist_ok=True)

    # Check resolution
    if RESOLUTION == '0x0':
        rprint("[bold yellow]Warning: A 0-second black video will be generated as a placeholder as Resolution is set to 0x0.[/bold yellow]")

        # Create a black frame
        frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, 1, (1920, 1080))
        out.write(frame)
        out.release()

        rprint("[bold green]Placeholder video has been generated.[/bold green]")
        return

    en_srt = "output/src_subtitles.srt"
    trans_srt = "output/trans_subtitles.srt"

    if not os.path.exists(en_srt) or not os.path.exists(trans_srt):
        print("Subtitle files not found in the 'output' directory.")
        exit(1)

    # 确定是否是macOS
    macOS = os.name == 'posix' and os.uname().sysname == 'Darwin'

    ffmpeg_cmd = [
        'ffmpeg', '-i', video_file,
        '-vf', (
            f"scale={TARGET_WIDTH}:{TARGET_HEIGHT}:force_original_aspect_ratio=decrease,"
            f"pad={TARGET_WIDTH}:{TARGET_HEIGHT}:(ow-iw)/2:(oh-ih)/2,"
            f"subtitles={en_srt}:force_style='FontSize={SRC_FONT_SIZE},FontName={FONT_NAME}," 
            f"PrimaryColour={SRC_FONT_COLOR},OutlineColour={SRC_OUTLINE_COLOR},OutlineWidth={SRC_OUTLINE_WIDTH},"
            f"ShadowColour={SRC_SHADOW_COLOR},BorderStyle=1',"
            f"subtitles={trans_srt}:force_style='FontSize={TRANS_FONT_SIZE},FontName={TRANS_FONT_NAME},"
            f"PrimaryColour={TRANS_FONT_COLOR},OutlineColour={TRANS_OUTLINE_COLOR},OutlineWidth={TRANS_OUTLINE_WIDTH},"
            f"BackColour={TRANS_BACK_COLOR},Alignment=2,MarginV=25,BorderStyle=4'"
        ).encode('utf-8'),  # 使用 UTF-8 编码
        '-y',
        output_video
    ]

    # 根据是否是macOS添加不同的参数, macOS的ffmpeg不包含preset
    if not macOS:
        ffmpeg_cmd.insert(-2, '-preset')
        ffmpeg_cmd.insert(-2, 'veryfast')

    print("🎬 Start merging subtitles to video...")
    start_time = time.time()
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')  # 指定 UTF-8 编码

    try:
        for line in process.stdout:
            print(line, end='')  # Print FFmpeg output in real-time
        
        process.wait()
        if process.returncode == 0:
            print(f"\n[Process completed in {time.time() - start_time:.2f} seconds.]")
            print("🎉🎥 Subtitles merging to video completed! Please check in the `output` folder 👀")
        else:
            print("\n[Error occurred during FFmpeg execution.]")
    except KeyboardInterrupt:
        process.kill()
        print("\n[Process interrupted by user.]")
    except Exception as e:
        print(f"\n[An unexpected error occurred: {e}]")
        if process.poll() is None:
            process.kill()

if __name__ == "__main__":
    merge_subtitles_to_video()