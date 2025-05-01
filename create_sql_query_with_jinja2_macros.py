from jinja2 import Template

# Define the Jinja template with macros and whitespace control
template = Template("""
{% macro calculate_differences(columns) -%}
    WITH ColumnDifferences AS (
        SELECT
            {%- for column in columns %}
            MAX({{ column }}) - MIN({{ column }}) AS diff_{{ column }}{% if not loop.last %},{% endif %}
            {%- endfor %}
        FROM
            your_table
    )
{%- endmacro %}

{% macro check_thresholds(columns, thresholds) -%}
    SELECT
        {%- for column in columns %}
        diff_{{ column }},
        {%- endfor %}
        CASE
            {%- for column in columns %}
            WHEN diff_{{ column }} > {{ thresholds[column]['max'] }} OR diff_{{ column }} < {{ thresholds[column]['min'] }} THEN 'Error: {{ column }} out of range'
            {%- if not loop.last %}WHEN {% endif %}
            {%- endfor %}
            ELSE 'All columns within thresholds'
        END AS status
    FROM
        ColumnDifferences
{%- endmacro %}

{% set columns = ['column1', 'column2', 'column3'] -%}
{% set thresholds = {
    'column1': {'min': 10, 'max': 100},
    'column2': {'min': 20, 'max': 200},
    'column3': {'min': 30, 'max': 300}
} -%}

{{ calculate_differences(columns) }}
{{ check_thresholds(columns, thresholds) }};
""")

# Render the SQL query
sql_query = template.render()

# Print the generated query
print("Generated SQL Query:\n", sql_query)
