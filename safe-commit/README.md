# safe-commit

commit／push 前的敏感資料檢查與外洩止血流程。

## 安裝

**一次貼一行、各按一次 Enter**（兩行一起貼會被當成同一個指令而失敗）：

第一步，加入這個 plugin 倉庫：

```
/plugin marketplace add lien2fish/lien-plugins
```

第二步，安裝：

```
/plugin install safe-commit@lien-plugins
```

第一步如果失敗，改用完整網址：`/plugin marketplace add https://github.com/lien2fish/lien-plugins.git`

## 內容

- 三步驟：判敏感等級 → **實查目的地公開程度**（repo 名稱不代表可見性）→ 掃暫存區
- 附 `scripts/check_staged.py` 掃描腳本
- **中文檔名讓 git 輸出八進位跳脫，grep 永遠 0 命中且不報錯**——
  任何用 git 列檔名的指令都要加 `-c core.quotepath=false`
- `.gitignore` 不會取消追蹤、`git rm` 不會清歷史、
  force push 後 GitHub 仍以 SHA 提供舊 commit
- 完整止血流程（含最常被漏掉的：寫信請 GitHub 清快取）

MIT
