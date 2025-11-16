{{ config(
    materialized='incremental',
    unique_key='trip_id'
) }}

{% set except_col = ['payment_method', 'trip_status'] %}
{% set all_cols = adapter.get_columns_in_relation(source('bronze_source', 'trips')) %}
{% set selected_cols = [] %}

{% for col in all_cols %}
  {% if col.name not in except_col %}

    {% do selected_cols.append(col.name) %}

  {% endif %}


{% endfor %}




select
  {{ selected_cols | join(', ') }} , current_timestamp() as process_timestamp
from {{ source('bronze_source', 'trips') }}

{% if is_incremental() %}
where last_updated_timestamp > (
  select coalesce(max(last_updated_timestamp), timestamp '1900-01-01 00:00:00')
  from {{ this }}
)
{% endif %}
