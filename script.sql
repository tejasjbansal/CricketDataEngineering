--top 5 stadiums by capacity --
SELECT top 5 rank, stadium, capacity
FROM stadiums
ORDER BY capacity DESC

-- average capacity by country --
SELECT country, AVG(capacity) as avg_capacity
FROM stadiums
GROUP BY country
ORDER BY avg_capacity DESC;

--count of stadiums in each country--
SELECT country, count(country) stadium_count
FROM stadiums
GROUP BY country
ORDER BY stadium_count desc, country asc

--stadium ranking within each country--
SELECT rank, stadium, country,
    RANK() OVER(PARTITION BY country ORDER BY capacity DESC) as country_rank
FROM stadiums;

--top 3 stadium ranking within each country--
SELECT rank, stadium, country, capacity, country_rank
FROM (
    SELECT rank, stadium, country, capacity,
           RANK() OVER (PARTITION BY country ORDER BY capacity DESC) as country_rank
    FROM stadiums
) ranked_stadiums
WHERE country_rank <= 3;

-- stadiums with capacity above average --
SELECT stadium, t2.country, capacity, avg_capacity
FROM stadiums, (SELECT country, AVG(capacity) avg_capacity FROM stadiums GROUP BY country) t2
WHERE t2.country = stadiums.country
and capacity > avg_capacity
ORDER BY country

--stadiums with the closest capacity to country median--
WITH MedianCTE AS (
    SELECT
        country, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY capacity) OVER (PARTITION BY country) AS median_capacity
    FROM stadiums
)
SELECT rank, stadium, country, capacity, ranked_stadiums.median_rank
FROM (
    SELECT
        s.rank, s.stadium, s.country, s.capacity,
        ROW_NUMBER() OVER (PARTITION BY s.country ORDER BY ABS(s.capacity - m.median_capacity)) AS median_rank
    FROM stadiums s JOIN MedianCTE m ON s.country = m.country
) ranked_stadiums
WHERE median_rank = 1;
