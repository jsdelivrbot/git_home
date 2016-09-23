/*Part A Coffee Sales*/

/*1. Extract the total sales for each product for each month. List all months (like January, February, etc) in the columns.*/
SELECT prodname, EXTRACT(MONTH FROM factdate) AS month, SUM(actsales) AS sales
FROM prodcoffee, factcoffee
WHERE prodcoffee.productid = factcoffee.productid
GROUP BY prodname, EXTRACT(MONTH FROM factdate)
ORDER BY prodname ASC, month ASC;

/*2*/

WITH temp AS (
  SELECT state, prodname, EXTRACT(YEAR FROM factdate) AS year, SUM(actsales) AS sales
  FROM statecoffee, areacoffee, prodcoffee, factcoffee
  WHERE statecoffee.stateid = areacoffee.stateid
        AND areacoffee.area_code = factcoffee.areaid
        AND prodcoffee.productid = factcoffee.productid
  GROUP BY state, prodname, EXTRACT(YEAR FROM factdate)),
sales_2012 AS (
  SELECT temp_2012.*, ROW_NUMBER() OVER (PARTITION BY state ORDER BY sales DESC) AS rn
  FROM (
    SELECT *
    FROM temp
    WHERE year = 2012) temp_2012),
sales_2013 AS (
  SELECT temp_2013.*, ROW_NUMBER() OVER (PARTITION BY state ORDER BY sales DESC) AS rn
  FROM (
    SELECT *
    FROM temp
    WHERE year = 2013) temp_2013),
top_sales_2012 AS (
  SELECT state, prodname, sales
  FROM sales_2012
  WHERE rn = 1),
top_sales_2013 AS (
  SELECT state, prodname, sales
  FROM sales_2013
  WHERE rn = 1)
SELECT top_sales_2012.state, top_sales_2012.prodname, top_sales_2012.sales AS FY2012, top_sales_2013.sales AS FY2013
FROM top_sales_2012, top_sales_2013
WHERE top_sales_2012.state = top_sales_2013.state
      AND top_sales_2012.prodname <> top_sales_2013.prodname
ORDER BY state ASC;

WITH temp AS (
  SELECT state, prodname, EXTRACT(YEAR FROM factdate) AS year, SUM(actsales) AS sales
  FROM statecoffee, areacoffee, prodcoffee, factcoffee
  WHERE statecoffee.stateid = areacoffee.stateid
        AND areacoffee.area_code = factcoffee.areaid
        AND prodcoffee.productid = factcoffee.productid
  GROUP BY state, prodname, EXTRACT(YEAR FROM factdate)),
sales_2012 AS (
  SELECT temp_2012.*, ROW_NUMBER() OVER (PARTITION BY state ORDER BY sales DESC) AS rn
  FROM (
    SELECT *
    FROM temp
    WHERE year = 2012) temp_2012),
sales_2013 AS (
  SELECT temp_2013.*, ROW_NUMBER() OVER (PARTITION BY state ORDER BY sales DESC) AS rn
  FROM (
    SELECT *
    FROM temp
    WHERE year = 2013) temp_2013),
top_sales_2012 AS (
  SELECT state, prodname, sales
  FROM sales_2012
  WHERE rn = 1),
top_sales_2013 AS (
  SELECT state, prodname, sales
  FROM sales_2013
  WHERE rn = 1)
SELECT top_sales_2012.prodname, COUNT(top_sales_2012.prodname) AS count
FROM top_sales_2012, top_sales_2013
WHERE top_sales_2012.state = top_sales_2013.state
      AND top_sales_2012.prodname = top_sales_2013.prodname
GROUP BY top_sales_2012.prodname
ORDER BY count DESC;

WITH total_sales AS (
  SELECT SUM(actsales) as total
  FROM factcoffee
),
cumulative_sales AS (
  SELECT state_sales.*, SUM(sales) OVER (ORDER BY sales DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumsales
  FROM (
    SELECT state, SUM(actsales) AS sales
    FROM statecoffee, areacoffee, factcoffee
    WHERE statecoffee.stateid = areacoffee.stateid
          AND areacoffee.area_code = factcoffee.areaid
    GROUP BY state
  ) state_sales
)
SELECT state, sales, ROUND(cumsales/total,2) AS cumpercent, ROW_NUMBER() OVER (ORDER BY sales DESC) AS sales_rank
FROM cumulative_sales, total_sales;

WITH total_profit AS (
  SELECT SUM(actprofit) as total
  FROM factcoffee
),
cumulative_profit AS (
  SELECT state_profit.*, SUM(profit) OVER (ORDER BY profit DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumprofit
  FROM (
    SELECT state, SUM(actprofit) AS profit
    FROM statecoffee, areacoffee, factcoffee
    WHERE statecoffee.stateid = areacoffee.stateid
          AND areacoffee.area_code = factcoffee.areaid
    GROUP BY state
  ) state_profit
)
SELECT state, profit, ROUND(cumprofit/total,2) AS cumpercent, ROW_NUMBER() OVER (ORDER BY profit DESC) AS profit_rank
FROM cumulative_profit, total_profit;