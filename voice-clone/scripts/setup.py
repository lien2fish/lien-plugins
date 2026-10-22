#!/usr/bin/env python3
"""第一次使用：建 venv、裝套件、登記參考音。

    python3 setup.py --ref 我的錄音.m4a --ref-text "錄音裡講的那一句話"

參考音的挑法（實測結論）：
  * 一句、5~6 秒、平常說話的語氣——參考音的語氣就是產出的語氣
  * 安靜的房間、手機貼近嘴巴錄就夠，不要有背景音樂
  * 不是越長越好：12 秒串接輸給 6 秒單句
  * --ref-text 要跟錄音一字不差

⚠️ 只能用自己的聲音，或已取得本人明確同意的聲音。
"""

import argparse, json, os, platform, shutil, subprocess, sys

HOME = os.path.expanduser(os.environ.get("VOICE_CLONE_HOME", "~/.voice-clone"))
PKGS = ["mlx-audio==0.5.3", "mlx-whisper==0.4.3", "pypinyin==0.55.0"]

p = argparse.ArgumentParser()
p.add_argument("--ref", required=True, help="參考音（wav／m4a／mp3 皆可）")
p.add_argument("--ref-text", required=True, help="參考音裡講的話，一字不差")
p.add_argument("--skip-install", action="store_true", help="venv 已裝好，只換參考音")
a = p.parse_args()

if platform.system() != "Darwin" or platform.machine() != "arm64":
    sys.exit("❌ 需要 Apple Silicon 的 Mac（M1 以後）：模型用 MLX 跑")
if not shutil.which("ffmpeg"):
    sys.exit("❌ 找不到 ffmpeg，先 brew install ffmpeg")
if not os.path.exists(a.ref):
    sys.exit(f"❌ 找不到參考音 {a.ref}")

os.makedirs(HOME, exist_ok=True)
venv_py = os.path.join(HOME, ".venv/bin/python")

if not a.skip_install:
    uv = shutil.which("uv")
    if uv:
        subprocess.run(
            [uv, "venv", "--python", "3.12", os.path.join(HOME, ".venv")], check=True
        )
        subprocess.run([uv, "pip", "install", "--python", venv_py, *PKGS], check=True)
    else:
        py312 = shutil.which("python3.12")
        if not py312:
            sys.exit(
                "❌ 需要 Python 3.12：brew install uv（建議）或 brew install python@3.12"
            )
        subprocess.run([py312, "-m", "venv", os.path.join(HOME, ".venv")], check=True)
        subprocess.run([venv_py, "-m", "pip", "install", *PKGS], check=True)

# 統一轉成 24 kHz 單聲道 wav，模型吃這個格式最穩
ref = os.path.join(HOME, "ref.wav")
subprocess.run(
    ["ffmpeg", "-y", "-v", "error", "-i", a.ref, "-ar", "24000", "-ac", "1", ref],
    check=True,
)
dur = float(
    subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            ref,
        ],
        capture_output=True,
        text=True,
    ).stdout
)
if not 3 <= dur <= 10:
    print(f"⚠️ 參考音 {dur:.1f} 秒，建議 5~6 秒的單句")

json.dump(
    {"ref_audio": ref, "ref_text": a.ref_text, "python": venv_py},
    open(os.path.join(HOME, "config.json"), "w"),
    ensure_ascii=False,
    indent=1,
)
print(f"✅ 設定完成：{HOME}/config.json（參考音 {dur:.1f} 秒）")
print('   試一句：python3 say.py "今天天氣很好"（第一次會下載約 2.5 GB 模型）')
