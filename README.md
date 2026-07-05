# 台股多空羅盤

Taiwan stock dashboard with moving average signals and technical analysis.

## 設定步驟

### 1. 建立 GitHub Repository
在 GitHub 上建立新的公開 repository(例如 `tw-dashboard`)。

### 2. 上傳檔案
將此資料夾的所有檔案上傳到 repository,包括 `.github/workflows` 目錄。

### 3. 啟用 GitHub Pages
- 前往 Repository Settings → Pages
- Source 選擇 Deploy from a branch
- Branch 選擇 main,目錄選擇 (root)
- Save

### 4. 執行第一次更新
- 前往 Actions 頁籤
- 點選 "update data" workflow
- 按下 "Run workflow" 執行第一次資料更新
- 每個交易日 14:10 (台北時間,市場收盤後) 會自動更新資料

### 5. 取得網址
Dashboard 網址: `https://<your-username>.github.io/tw-dashboard/`

## 選項:API Token

若遇到 FinMind API 速率限制,可設定個人 token:

1. 在 FinMind 註冊並取得 API token
2. Repository Settings → Secrets and variables → Actions
3. 新增 Secret 名稱 `FINMIND_TOKEN`,值為你的 token
4. Workflow 會自動使用此 token

## 技術規格

- **資料來源**: FinMind Trade API
- **追蹤標的**: TAIEX、2330、0050、0056、006208、00646
- **均線**: 5日、20日、60日、240日
- **更新頻率**: 每個交易日 14:10 (台北時間)
- **前端**: 純 HTML/CSS/JavaScript,無外部相依
- **資料**: 靜態 JSON 檔案,以 GitHub Pages 托管

## 免責聲明

資料僅供參考,非投資建議。
