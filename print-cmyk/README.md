# print-cmyk

大圖、防水布、異形看板的 CMYK 送印產線。

## 安裝

**一次貼一行、各按一次 Enter**（兩行一起貼會被當成同一個指令而失敗）：

第一步，加入這個 plugin 倉庫：

```
/plugin marketplace add lien2fish/lien-plugins
```

第二步，安裝：

```
/plugin install print-cmyk@lien-plugins
```

第一步如果失敗，改用完整網址：`/plugin marketplace add https://github.com/lien2fish/lien-plugins.git`

## 內容

踩過的坑換來的實務知識：

- **不要交 CMYK TIFF**——RIP 可能反相成負片，改交自組 CMYK PDF
- **驗色要走 ICC**，`(1-C)(1-K)` 近似式會算出差 76 的假爆色
- 殘差 20~30 是 CMYK 色域極限，不是流程有誤
- 大圖的 dpi 該怎麼選（外牆 100dpi 就夠）
- 出血／裁切／安全線，以及加工會再吃掉多少邊
- 字級用觀看距離回推
- 異形版面：採信好量的邊，用幾何反推
- 送印前檢查清單，含 QR code 必須實掃

MIT
