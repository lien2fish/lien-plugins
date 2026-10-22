# lien-plugins

五個 Claude Code plugin，內容是實際踩過坑換來的做法——不是通用教學，
是「這樣做會出事，所以要那樣做」。

## 安裝

**一次貼一行、各按一次 Enter**（兩行一起貼會被當成同一個指令而失敗）：

第一步，加入這個 plugin 倉庫：

```
/plugin marketplace add lien2fish/lien-plugins
```

第二步，安裝：

```
/plugin install <plugin-name>@lien-plugins
```

第一步如果失敗，改用完整網址：`/plugin marketplace add https://github.com/lien2fish/lien-plugins.git`

## Plugins

| Plugin | 解決什麼 |
|--------|---------|
| **[line-assistant](./line-assistant)** | 部署一個只有自己能用的 LINE AI 助理。含範本連結、設定流程，以及**兩道非設不可的防護機制**與驗收方式 |
| **[print-cmyk](./print-cmyk)** | 大圖／防水布／異形看板送印。**不要交 CMYK TIFF**（RIP 會反相成負片）、驗色要走 ICC 不能用近似公式 |
| **[reel](./reel)** | ffmpeg 剪輯產線。**YouTube「處理完才說無法上傳」的三個真因**、Whisper 幻覺、雲端同步靜默回收素材 |
| **[safe-commit](./safe-commit)** | commit 前的敏感資料檢查。**中文檔名讓 git 的 grep 永遠 0 命中且不報錯**、完整外洩止血流程 |
| **[voice-clone](./voice-clone)** | 用自己的克隆聲音做中文旁白（Apple Silicon 本機跑）。**換參考音救不了發音**、模型固定唸錯的 23 個詞與替代字、Whisper 回聽驗收 |

## 這些內容的來源

一個經營多品牌的小公司自建營運自動化的過程中累積的。
每條規則背後都有一次實際的損失：印壞的布、上傳不了的影片、
公開了三個月才發現的客戶名單。

因此內容偏「陷阱清單」而非「入門教學」——
入門的部分官方文件都有，這裡收的是文件不會寫的那些。

## 授權

MIT。可自由使用、修改、再散布，包含商業用途。
內容按「現狀」提供，不附任何形式的擔保。
