# CoinMarketCap ELT Module (dbt & Data Pipeline)

Thư mục này chứa toàn bộ logic xử lý dữ liệu (ELT) cho dự án CoinMarketCap, bao gồm các script Python để thu thập dữ liệu (Extract/Load) và project dbt để biến đổi dữ liệu (Transform) trong Data Warehouse.

## 📁 Cấu trúc thư mục
* `docker-compose.yaml`: File cấu hình kích hoạt cụm hạ tầng Airflow & Postgres.
* `dag/`: Chứa file định nghĩa luồng Airflow DAG (`elt_coin.py`) để copy vào thư mục dags của Airflow.
* `scripts/`: Chứa mã nguồn Python (`load_staging.py`) bóc tách dữ liệu từ API.
* `database/dbt_for_coin/`: Toàn bộ source code của dbt (models, seeds, snapshots) dùng để transform dữ liệu.
* `config/`: Nơi lưu trữ file cấu hình kết nối `profiles.yml`.

---

## 🛠️ Hướng dẫn tích hợp vào Airflow

Để chạy module này trên một cụm Airflow độc lập, hãy làm theo các bước sau:

### 1. Cấu hình Bảo mật trên Airflow UI (Variables)
Do các thông tin nhạy cảm đã bị loại bỏ khỏi mã nguồn trước khi đẩy lên GitHub, bạn cần cấu hình lại chúng trên giao diện Airflow:
1. Truy cập vào **Airflow Web UI -> Admin -> Variables**.
2. Tạo mới biến thứ nhất: Key là `DB_PASSWORD` (Điền mật khẩu Postgres để dbt sử dụng).
3. Tạo mới biến thứ hai: Key là `API_KEY_COINMARKETCAP` (Điền API Key của CoinMarketCap để script Python sử dụng).

> *Lưu ý trong code Python:* Khi viết script gọi API, sử dụng `Variable.get("API_KEY_COINMARKETCAP")` hoặc truyền qua `env` trong Bash/Python Operator để đảm bảo bảo mật.

### 2. Copy DAG và Scripts vào Airflow Worker
Đảm bảo rằng toàn bộ thư mục `CoinMarketCap` này được đặt tại đường dẫn `/opt/airflow/projects/CoinMarketCap` trên môi trường Airflow của bạn (hoặc sửa lại biến `project_dir` và `profile_dir` trong file `dag/elt_coin.py` cho đúng với đường dẫn thực tế).

### 3. Cài đặt thư viện bắt buộc cho Airflow Worker
Môi trường Airflow của bạn cần được cài đặt sẵn:
* `dbt-postgres`

---
