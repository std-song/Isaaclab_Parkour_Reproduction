"""Create compact animated WebP previews for the supplementary MP4 videos."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import imageio_ffmpeg


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video_dir", type=Path)
    parser.add_argument("--width", type=int, default=480)
    parser.add_argument("--fps", type=int, default=6)
    parser.add_argument("--quality", type=int, default=58)
    args = parser.parse_args()

    preview_dir = args.video_dir / "previews"
    preview_dir.mkdir(exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    videos = sorted(args.video_dir.glob("*.mp4"))
    if not videos:
        raise SystemExit(f"No MP4 videos found in {args.video_dir}")

    for video in videos:
        output = preview_dir / f"{video.stem}.webp"
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-i",
                str(video),
                "-vf",
                f"fps={args.fps},scale={args.width}:-2:flags=lanczos",
                "-an",
                "-loop",
                "0",
                "-c:v",
                "libwebp",
                "-quality",
                str(args.quality),
                str(output),
            ],
            check=True,
        )
        print(output)


if __name__ == "__main__":
    main()
