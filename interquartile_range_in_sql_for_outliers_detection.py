import sqlite3
import pandas as pd

"""
The outlier detection uses the Interquartile Range (IQR) method:

First Quartile (Q1): 25th percentile (value below which 25% of data falls)
Third Quartile (Q3): 75th percentile
IQR: Q3 - Q1
Outlier Boundaries:
    Lower bound = Q1 - 1.5 × IQR
    Upper bound = Q3 + 1.5 × IQR
"""

# Sample data
data = [3, 5, 7, 8, 10, 12, 14, 15, 18, 24, 50]  # 50 is an obvious outlier

# Create in-memory SQLite database
conn = sqlite3.connect(":memory:")

# Create table and insert data
conn.execute("CREATE TABLE numbers(value REAL)")
conn.executemany("INSERT INTO numbers VALUES(?)", [(x,) for x in data])

# Calculate outliers using NTILE approach
query = """
WITH data_with_quartiles AS (
  SELECT 
    value,
    NTILE(4) OVER (ORDER BY value) AS quartile_group
  FROM numbers
),
quartile_values AS (
  SELECT
    MAX(CASE WHEN quartile_group = 1 THEN value END) AS q1,
    MAX(CASE WHEN quartile_group = 3 THEN value END) AS q3,
    MAX(CASE WHEN quartile_group = 3 THEN value END) - 
    MAX(CASE WHEN quartile_group = 1 THEN value END) AS iqr
  FROM data_with_quartiles
)
SELECT 
  n.value,
  CASE
    WHEN n.value < (q.q1 - 1.5 * q.iqr) THEN 'Low Outlier'
    WHEN n.value > (q.q3 + 1.5 * q.iqr) THEN 'High Outlier'
    ELSE 'Normal'
  END AS outlier_status,
  q.q1,
  q.q3,
  q.iqr,
  (q.q1 - 1.5 * q.iqr) AS lower_bound,
  (q.q3 + 1.5 * q.iqr) AS upper_bound
FROM numbers n
CROSS JOIN quartile_values q
"""

results = pd.read_sql(query, conn)
print(results)
conn.close()
