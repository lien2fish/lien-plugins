# lien-plugins

四個 Claude Code plugin，內容是實際踩過坑換來的做法——不是通用教學，
是「這樣做會出事，所以要那樣做」。

## 安裝

```
/plugin marketplace add lien2fish/lien-plugins
/plugin install <plugin-name>@lien-plugins
```

## Plugins

| Plugin | 解決什麼 |
|--------|---------|
| **[line-assistant](./line-assistant)** | 部署一個只有自己能用的 LINE AI 助理。含範本連結、設定流程，以及**兩道非設不可的防護機制**與驗收方式 |
| **[print-cmyk](./print-cmyk)** | 大圖／防水布／異形看板送印。**不要交 CMYK TIFF**（RIP 會反相成負片）、驗色要走 ICC 不能用近似公式 |
| **[reel](./reel)** | ffmpeg 剪輯產線。**YouTube「處理完才說無法上傳」的三個真因**、Whisper 幻覺、雲端同步靜默回收素材 |
| **[safe-commit](./safe-commit)** | commit 前的敏感資料檢查。**中文檔名讓 git 的 grep 永遠 0 命中且不報錯**、完整外洩止血流程 |

## 這些內容的來源

一個經營多品牌的小公司自建營運自動化的過程中累積的。
每條規則背後都有一次實際的損失：印壞的布、上傳不了的影片、
公開了三個月才發現的客戶名單。

因此內容偏「陷阱清單」而非「入門教學」——
入門的部分官方文件都有，這裡收的是文件不會寫的那些。

## 授權

MIT。可自由使用、修改、再散布，包含商業用途。
內容按「現狀」提供，不附任何形式的擔保。
