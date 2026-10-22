#!/usr/bin/env python3
"""用自己的克隆聲音產生旁白（Qwen3-TTS，Apple Silicon 本機跑，不上雲）。

選型結論，改動前先看清楚：
  * 參考音的「語氣」決定產出的語氣，文本寫法影響很小
    （刻意寫成「欸跟你講」這類口語反而更差，正常寫就好）
  * 不要指定 --lang_code zh，會變成念稿／機器人腔；不指定最自然
  * 參考音要「單句、口語」，5~6 秒最好；串長到 12 秒沒有比較好
  * 有些詞一定唸錯，**換參考音沒有用**，要靠發音替代表餵同音字繞過

設定讀 ~/.voice-clone/config.json（第一次用先跑 setup.py）。
"""

import argparse, json, os, subprocess, sys, wave

HOME = os.path.expanduser(os.environ.get("VOICE_CLONE_HOME", "~/.voice-clone"))
HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = "mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16"
BUILTIN_TABLE = os.path.join(HERE, "pronunciation_zh-TW.json")
USER_TABLE = os.path.join(HOME, "pronunciation.json")

cfg_path = os.path.join(HOME, "config.json")
if not os.path.exists(cfg_path):
    sys.exit(f"❌ 找不到 {cfg_path}，請先跑 setup.py 設定參考音")
cfg = json.load(open(cfg_path))
py = os.path.expanduser(cfg.get("python", os.path.join(HOME, ".venv/bin/python")))

p = argparse.ArgumentParser()
p.add_argument("text")
p.add_argument("-o", "--out", default=os.path.join(HOME, "out/say"))
p.add_argument("--speed", default="1.0", help="語速（0.9 慢、1.1 快）")
p.add_argument("--ref", default=os.path.expanduser(cfg["ref_audio"]))
p.add_argument("--ref-text", default=cfg["ref_text"])
p.add_argument("--norm", type=int, default=1, help="1=gate＋壓縮＋響度正規化，0=不處理")
p.add_argument("--no-fix", action="store_true", help="不要套用發音替代表")
a = p.parse_args()


def load_table(path):
    if not os.path.exists(path):
        return {}
    return {k: v for k, v in json.load(open(path)).items() if not k.startswith("_")}


# 模型對某些字的發音就是錯的，餵同音替代字繞過。
# 只換餵給 TTS 的文字，字幕與文案一律用原字。使用者自己的表會蓋過內建表。
text = a.text
if not a.no_fix:
    table = {**load_table(BUILTIN_TABLE), **load_table(USER_TABLE)}
    hit = [
        (k, v) for k, v in sorted(table.items(), key=lambda t: -len(t[0])) if k in text
    ]
    for k, v in hit:
        text = text.replace(k, v)
    if hit:
        print("🔤 發音替代：" + "　".join(f"{k}→{v}" for k, v in hit))

os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
subprocess.run(
    [
        py,
        "-m",
        "mlx_audio.tts.generate",
        "--model",
        MODEL,
        "--text",
        text,
        "--ref_audio",
        a.ref,
        "--ref_text",
        a.ref_text,
        "--speed",
        a.speed,
        "--output_path",
        os.path.dirname(a.out) or ".",
        "--file_prefix",
        os.path.basename(a.out),
    ],
    check=True,
)

wav = f"{a.out}_000.wav"
if not os.path.exists(wav):
    sys.exit(f"❌ 沒有產出 {wav}")

if a.norm:
    # ⛔ 不要用峰值正規化——它只看最大值，管不了段內起伏。
    # Qwen3 的句首常弱起（實測比同句主體小 17.8 dB），聽起來像斷了一下。
    # 處理鏈的順序不能換：
    #   agate        先壓住安靜段，否則後面的壓縮會把底噪一起拉上來（實測 −68 → −49 dB）
    #   acompressor  把弱音提上來，落差 17.8 → 7.2 dB
    #   loudnorm     EBU R128 統一到 −16 LUFS（社群影片慣用）
    # dynaudnorm 試過，落差反而變 19.7 dB，不要用。
    chain = (
        "agate=threshold=-52dB:ratio=4:attack=8:release=200,"
        "acompressor=threshold=-30dB:ratio=5:attack=3:release=180:makeup=4,"
        "loudnorm=I=-16:TP=-1.5:LRA=7"
    )
    tmp = wav + ".norm.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            wav,
            "-af",
            chain,
            "-ar",
            "24000",
            "-ac",
            "1",
            tmp,
        ],
        check=True,
    )
    os.replace(tmp, wav)
    print("🔊 已套用 gate＋壓縮＋響度正規化（−16 LUFS）")

with wave.open(wav) as w:
    print(f"✅ {wav}  {w.getnframes()/w.getframerate():.2f}s")
