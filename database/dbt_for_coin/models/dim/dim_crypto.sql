{{
    config(
        materialized='table',
    )
}}

WITH ranked_coins AS (
    SELECT 
        coin_id,
        name,
        symbol,
        slug,
        cmc_rank,
        tags,
        date_added,
        -- Sắp xếp theo extracted_at giảm dần để lấy bản ghi mới nhất vừa cào
        ROW_NUMBER() OVER (PARTITION BY coin_id ORDER BY extracted_at DESC) as rn
    FROM {{ source('staging', 'raw_data') }}
)

SELECT 
    coin_id,
    name,
    symbol,
    slug,
    cmc_rank,
    tags,
    date_added
FROM ranked_coins
-- Ép buộc mỗi coin_id chỉ được phép lên đúng 1 dòng duy nhất
WHERE rn = 1