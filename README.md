# AVIF Converter

這是一個基於 Flask 建立的網頁版圖片轉 AVIF 工具。
支援將各種常見的圖片格式（如 PNG, JPG, GIF 等）快速轉換成次世代高壓縮比的 AVIF 格式，並自動打包成 ZIP 檔下載。

## 功能特色
- 支援多檔同時上傳與批次轉換。
- 支援透明背景圖片轉換（RGBA 完美保留透明度）。
- 支援自訂轉換壓縮品質（0-100）。
- 支援自訂下載 ZIP 檔名（留空則自動套用時間戳記）。
- 提供直覺、現代化、支援拖曳上傳的優美介面。

## 本機開發與測試

1. 確保已安裝 Python 3。
2. 建立並啟動虛擬環境：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. 安裝相依套件：
   ```bash
   pip3 install -r requirements.txt
   ```
4. 啟動伺服器：
   ```bash
   python3 app.py｀
   ```
   接著在瀏覽器開啟 `http://127.0.0.1:5000` 即可測試。

## 伺服器部署 (Docker)

本專案已配置好 Dockerfile 與 docker-compose.yml，可一鍵啟動：
```bash
docker-compose up -d --build
```
服務會預設運行於背景的 5000 port。

## Nginx 部署設定參考

建議在正式環境使用 Nginx 作為反向代理，並記得設定 `client_max_body_size` 以允許多檔上傳：

```nginx
server {
    listen 80;
    listen 443 ssl;
    server_name avif-converter.your-domain.com;

    # SSL 憑證路徑
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 50M;
    }
}
```
