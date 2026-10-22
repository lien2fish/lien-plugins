# voice-clone

用自己的克隆聲音做中文旁白。Qwen3-TTS 在 Apple Silicon 本機跑，**聲音不上任何雲端**。

## 安裝

```
/plugin marketplace add lien2fish/lien-plugins
/plugin install voice-clone@lien-plugins
```

接著跟 Claude 說「幫我設定聲音克隆」，它會帶你錄參考音、跑 `setup.py`。

## 需求

- **Apple Silicon 的 Mac**（M1 以後）——模型用 MLX 跑，Intel Mac 與 Windows 不支援
- `brew install ffmpeg uv`
- 約 5 GB 空間（套件約 2.5 GB、模型約 2.5 GB）

## 內容

- `scripts/setup.py`：建環境、登記參考音
- `scripts/say.py`：產生旁白，自動套用同音替代表與音量處理
- `scripts/check_say.py`：把產出丟回 Whisper，用拼音比對抓唸錯的字
- `scripts/pronunciation_zh-TW.json`：模型固定唸錯的 23 個詞與替代字，全部實測過
- **換參考音救不了發音**——錯在模型的文字轉音素，不在音色
- **同音字不一定有效**，每組都要回聽驗證
- 阿拉伯數字一律寫成中文（「9 月」會唸成「酒味」）
- 混音鏈上的 `loudnorm`／`sidechaincompress` 會吃掉旁白尾巴或讓字幕錯位

## ⚠️ 使用規範

**只能克隆自己的聲音，或已取得本人明確同意的聲音。**
發布到有 AI 內容揭露規範的平台時，請依平台規定標示。

## 授權

本 plugin：MIT。
使用的模型 [Qwen3-TTS-12Hz-0.6B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base)：Apache-2.0。
[mlx-audio](https://github.com/Blaizzy/mlx-audio)：MIT。
