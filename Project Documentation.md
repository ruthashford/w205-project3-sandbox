# Overview 
*Section to include overview of project and problem statement.*

# Goals 
*Here we can list what we're trying to accomplish. This can include what's in scope and out of scope for this project, in addition to the business questions we aim to answer.*

# Step by Step Instructions 
*List steps that analysts need to do to reproduce results (this can be similar to what's in the course content slide shows). 

# Output
*Add ERD diagram of the tables, and a link to the python notebook.* 

## Example Queries 

Guild Stats - How many people are in the guild? 
```{sql}
WITH
  guild_headcount AS (
    SELECT
      CASE
        WHEN action = 'Join' THEN 1
        WHEN action = 'Leave' THEN - 1
        ELSE 0
      END AS guild_hc_change
    FROM event_guild )
    
SELECT
  SUM(guild_hc_change) AS guild_size
FROM guild_headcount; 
```

Guild Stats - How many people joined the guild in the past year? 
```{sql}
SELECT
  COUNT(*) AS num_guild_joins
FROM event_guild
WHERE
  action = 'Join'
  AND timestamp BETWEEN TIMESTAMP_SUB(timestamp, INTERVAL 365 DAY) AND CURRENT_TIMESTAMP();
```

Horse Stats - How many horses have been purchased by size? 
```{sql}
SELECT
  size AS horse_size,
  COUNT(*) AS num_horses
FROM event_purchase_horse
GROUP BY 1;
```

Sword Stats - How many swords have been purchased by color? 
```{sql}
SELECT
  color AS sword_color,
  COUNT(*) AS num_swords
FROM event_purchase_sword
GROUP BY 1;
```

Sword Stats - How many swords have been purchased in the past year? 
```{sql}
SELECT
  COUNT(*) AS num_swords_purchased
FROM event_purchase_sword
WHERE
  timestamp BETWEEN TIMESTAMP_SUB(timestamp, INTERVAL 365 DAY) AND CURRENT_TIMESTAMP();
```
