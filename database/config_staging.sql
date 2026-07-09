create staging.raw_data(

    coin_id int ,

    name varchar,

    symbol varchar,

    slug varchar,

    cmc_rank int,

    date_added timestamp,

    last_updated timestamp,

    tags varchar,

    platform_id int,

    platform_slug varchar,

    platform_name varchar,

    platform_symbol varchar,

    usd_price decimal,

    usd_volume_24h decimal,

    usd_market_cap decimal,

    market_cap_dominance decimal,

    pct_change_24h decimal,

    pct_change_7d decimal,

    dex_volume_24h decimal,

    cex_volume_24h decimal,

    extracted_at timestamp default now()

) 

