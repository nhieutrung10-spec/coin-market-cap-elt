import requests
import pandas as pd
from sqlalchemy import create_engine,text
from sqlalchemy.engine import URL
from airflow.models import Variable  #type: ignore

api_key=Variable.get("API_KEY_COINMARKETCAP")
db_pw=Variable.get('DB_PASSWORD')

def load_staging():
    try:
        url = "https://pro-api.coinmarketcap.com/v3/cryptocurrency/listings/latest"
        headers = {"X-CMC_PRO_API_KEY": api_key}
        response = requests.get(url, headers=headers)
        result=response.json()
        data=result['data']
        data_list=[]
        for coin in data:
            #Khởi tạo dòng dữ liệu phẳng cơ bản
            row = {
                "coin_id": coin.get("id"),
                "name": coin.get("name"),
                "symbol": coin.get("symbol"),
                "slug": coin.get("slug"),
                "cmc_rank": coin.get("cmc_rank"),
                "date_added": coin.get("date_added"),
                "last_updated": coin.get("last_updated")
            }
            #Xử lý mảng Tags thành chuỗi phân tách bằng dấu phẩy
            tags_list = coin.get("tags")
            row["tags"] = ",".join(tags_list) if tags_list else None
            #Trải phẳng Object Platform (Nếu rỗng thì điền thông tin mạng riêng)
            platform_data = coin.get("platform")
            if platform_data:
                row["platform_id"] = platform_data.get("id")
                row["platform_slug"] = platform_data.get("slug")
                row["platform_name"] = platform_data.get("name")
                row["platform_symbol"] = platform_data.get("symbol")
            else:
                row["platform_id"] = -1
                row["platform_slug"] = "native"
                row["platform_name"] = "Native Network"
                row["platform_symbol"] = "NATIVE"
            #Trải phẳng List/Dict Quote (Ăn thẳng vào phần tử đầu tiên của list)
            quote_list = coin.get('quote', [])
            if isinstance(quote_list, list) and len(quote_list) > 0:
            # Lấy phần tử đầu tiên vì đây là list các quote, và chỉ cái quote đầu tiên là khả dung
                usd_data = quote_list[0] 
                
                row["usd_price"] = usd_data.get("price")
                row["usd_volume_24h"] = usd_data.get("volume_24h")
                row["usd_market_cap"] = usd_data.get("market_cap")
                row["market_cap_dominance"] = usd_data.get("market_cap_dominance")
                row["pct_change_24h"] = usd_data.get("percent_change_24h")
                row["pct_change_7d"] = usd_data.get("percent_change_7d")
                row["dex_volume_24h"] = usd_data.get("dex_volume_24h")
                row["cex_volume_24h"] = usd_data.get("cex_volume_24h")
            else:
                row["usd_price"] = None
                row["usd_volume_24h"] = None
            data_list.append(row)

        print('Gọi API hoàn tất!')
    except Exception as e:
        print(f"❌ Lỗi khi gọi API: {e}")
        exit(1)

    try:
        url_coin = URL.create(
                "postgresql+psycopg2",
                username="postgres",
                password=db_pw,
                host="host.docker.internal",
                database="coin_analytics"
            )
        engine=create_engine(url=url_coin)
        df=pd.DataFrame(data_list)
        df['date_added']=pd.to_datetime(df["date_added"])
        df['last_updated']=pd.to_datetime(df["last_updated"])
        with engine.begin() as engine_coin:
            engine_coin.execute(text('truncate staging.raw_data'))
            df.to_sql(
                name='raw_data',
                con=engine_coin,
                schema='staging',
                if_exists='append',
                index=False,
                method="multi",
                chunksize=100,
            )
        print('Nạp dữ liệu hoàn tất!')
    except Exception as e:
        print(f"❌ Lỗi khi nạp dữ liệu vào Database: {e}")

