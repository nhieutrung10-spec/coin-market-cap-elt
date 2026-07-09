{{
    config(
        materialized='incremental',
        unique_key=['coin_id', 'last_updated']
    )
}}

select row_number() over(order by coin_id) as fact_id, coin_id, platform_id, usd_price, usd_volume_24h, usd_market_cap, market_cap_dominance, pct_change_24h, pct_change_7d, dex_volume_24h, cex_volume_24h, last_updated
from {{ source('staging', 'raw_data') }}


