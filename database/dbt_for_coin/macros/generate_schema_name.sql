`sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {# Policy:
       - prod:    ANALYTICS
       - nonprod: dev_analytics, ci_analytics, etc.
    #}
    {%- if target.name == 'prod' -%}
        {{ custom_schema_name | trim }}
    {%- else -%}
        {{ (custom_schema_name) | lower | replace(' ', '_') }}
    {%- endif -%}
{%- endmacro %}