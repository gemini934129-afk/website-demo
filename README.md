# 老闆的自動更新網站

這是一個示範靜態網站，展示如何使用 GitHub Pages + GitHub Actions 自動更新。

## 🌐 網站網址
部署後：`https://gemini934129.github.io/website-demo/`

## 🔄 自動更新機制
- **每小時自動更新**（透過 GitHub Actions schedule）
- **手動觸發**（workflow_dispatch）
- **推送更新**（push to main branch）

## 📁 檔案結構
```
.
├── .github/
│   └── workflows/
│       └── auto-update.yml    # 自動更新腳本
├── index.html                  # 主要網頁
├── README.md                   # 說明文件
└── .gitignore
```

## 🚀 如何修改
1. 修改 `index.html` 內容
2. 推送至 GitHub：`git push origin main`
3. GitHub Actions 會自動部署

## 🦐 由小蝦協助設定
