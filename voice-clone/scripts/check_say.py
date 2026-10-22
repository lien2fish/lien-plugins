#!/usr/bin/env python3
"""檢查 TTS 產出的發音對不對。

做法：把生成的音檔丟回 Whisper 辨識，再跟原文逐字比對。
用拼音判斷差異的性質——同音異字（紀/記）是辨識選字，不算錯；
聲母或韻母變了（現場 xianchang → 雁彈 yandan）才是真的唸錯。

用法：
    python3 check_say.py <音檔> "<原文>"
    python3 check_say.py <音檔> --text-file <文字檔>
    python3 check_say.py <音檔> "<原文>" --model large-v3   # 句子裡有數字時

起因：一支旁白，本人聽出 2 個唸錯，用這個方法一驗，實際有 15 處。
"""
import sys, os, warnings, argparse

warnings.filterwarnings("ignore")
from difflib import SequenceMatcher

# 系統 python 的 torch／numpy 版本常互相不相容，轉交給 setup.py 建的 venv 跑。
VENV = os.path.expanduser(
    os.path.join(os.environ.get("VOICE_CLONE_HOME", "~/.voice-clone"), ".venv/bin/python")
)
if os.path.exists(VENV) and sys.executable != VENV:
    os.execv(VENV, [VENV, os.path.abspath(__file__)] + sys.argv[1:])

PUNCT = "，。、！？；：「」『』（）·　 ,.!?;:\n\t"
clean = lambda s: "".join(c for c in s if c not in PUNCT)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("text", nargs="?", default=None)
    ap.add_argument("--text-file")
    ap.add_argument("--model", default="small")
    a = ap.parse_args()

    src = open(a.text_file).read() if a.text_file else a.text
    if not src:
        sys.exit("要給原文：直接當參數，或用 --text-file")

    import mlx_whisper
    from pypinyin import lazy_pinyin, Style

    r = mlx_whisper.transcribe(
        a.audio,
        path_or_hf_repo=f"mlx-community/whisper-{a.model}-mlx",
        language="zh",
        condition_on_previous_text=False,  # 不關會讓幻覺沿著前文傳染
        initial_prompt="以下是繁體中文的口述錄音。",
    )
    heard = clean("".join(s["text"] for s in r["segments"]))
    ref = clean(src)

    py = lambda s: "".join(
        c
        for c in "".join(lazy_pinyin(s, style=Style.TONE3, errors=lambda x: list(x)))
        if not c.isdigit()
    )

    def close(x, y):
        """拼音差一兩個字母＝Whisper 沒聽清（fulunshe/fulunse），不是唸錯；
        差很多才是真的發錯音（xianchang/yandan）。"""
        if not x or not y:
            return False
        r = SequenceMatcher(None, x, y).ratio()
        return r >= 0.78

    sm = SequenceMatcher(None, ref, heard, autojunk=False)
    real, benign, minor = [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        s_, g_ = ref[i1:i2], heard[j1:j2]
        if not s_.strip():
            continue
        if not any("一" <= c <= "鿿" for c in s_):
            benign.append((s_, g_, "數字或英文"))
            continue
        if not g_.strip():
            benign.append((s_, g_, "辨識漏字"))
            continue  # 沒聽到≠唸錯
        if not any("一" <= c <= "鿿" for c in g_):
            benign.append((s_, g_, "轉寫成數字或英文"))
            continue  # 三十六→36
        if len(s_) >= 4 and len(g_) <= len(s_) // 2:
            benign.append((s_, g_, "整段漏聽"))
            continue
        ps, pg = py(s_), py(g_)
        if ps == pg:
            benign.append((s_, g_, "同音異字"))
            continue
        ctx = ref[max(0, i1 - 5) : i1] + "【" + s_ + "】" + ref[i2 : i2 + 5]
        (minor if close(ps, pg) else real).append((s_, g_, ps, pg, ctx))

    print(f"辨識吻合度 {sm.ratio()*100:.1f}%")
    print(f"可忽略 {len(benign)} 處（同音異字／數字／英文）")
    print(f"辨識不清 {len(minor)} 處（拼音接近，多半是 Whisper 沒聽準）")
    print(f"🔴 確定唸錯 {len(real)} 處\n")
    if real:
        print(f"{'原文':<10}{'聽成':<10}{'應讀':<14}{'實讀':<14}上下文")
        for s_, g_, ps, pg, ctx in real:
            print(f"  {s_:<9}{g_:<10}{ps:<14}{pg:<14}…{ctx}…")
    else:
        print("沒有確定的發音錯誤。")
    if minor and os.environ.get("SHOW_MINOR"):
        print("\n拼音接近的（參考）：")
        for s_, g_, ps, pg, ctx in minor:
            print(f"  {s_:<9}{g_:<10}{ps:<14}{pg:<14}…{ctx}…")
    return 1 if real else 0


if __name__ == "__main__":
    sys.exit(main())
