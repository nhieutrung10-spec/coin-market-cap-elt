with staging_platforms as (
    select distinct platform_id,platform_slug,platform_name,platform_symbol
    from {{ source('staging', 'raw_data') }}
)
select *
from staging_platforms
WHERE platform_id NOT IN (SELECT platform_id FROM {{ this }})
