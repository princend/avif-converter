# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- 專案初始化，建立基於 Flask 與 Pillow-avif-plugin 的圖片轉 AVIF 核心功能。
- 支援多檔同時上傳，並自動打包成 ZIP 檔下載。
- 支援透明背景圖片轉換（RGBA 保留透明度）。
- 提供自訂轉換壓縮品質（0-100）功能與自訂 ZIP 檔名。
- 實作直覺、現代化且支援「點擊或拖曳」上傳的優美介面。
- 新增 `Dockerfile` 與 `docker-compose.yml`，支援快速容器化部署。
- 新增詳細的 `README.md` 專案說明文件與 `Nginx` 反向代理設定教學。
- 新增 `.gitignore` 排除不必要的虛擬環境與系統快取檔。

### Fixed
- 修正「拖曳檔案」至上傳區時，瀏覽器會因為預設行為而開新分頁顯示圖片的問題（加入 drag & drop 事件攔截與視覺回饋效果）。
