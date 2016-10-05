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

WITH temp AS (
  SELECT *
  FROM (
    SELECT areaid, EXTRACT(YEAR FROM factdate) AS year, SUM(actsales) AS sales
    FROM factcoffee
    GROUP BY areaid, EXTRACT(YEAR FROM factdate) 
  )
  PIVOT (
   SUM(sales) FOR year in (2012 AS sales2012, 2013 AS sales2013)
  )
  ORDER BY areaid
)
SELECT temp.*, ROUND((sales2013-sales2012)/sales2012*100, 2) AS percentage_decline
FROM temp
WHERE sales2013 < sales2012
ORDER BY (sales2013-sales2012)/sales2012 ASC;

WITH temp AS (
  SELECT *
  FROM (
    SELECT prodname, EXTRACT(YEAR FROM factdate) AS year, SUM(actsales) AS sales
    FROM prodcoffee, factcoffee
    WHERE prodcoffee.productid = factcoffee.productid
    GROUP BY prodname, EXTRACT(YEAR FROM factdate) 
  )
  PIVOT (
   SUM(sales) FOR year in (2012 AS sales2012, 2013 AS sales2013)
  )
  ORDER BY prodname
)
SELECT temp.*, ROUND((sales2013-sales2012)/sales2012*100, 2) AS percentage_growth
FROM temp
ORDER BY (sales2013-sales2012)/sales2012 ASC;

WITH temp AS (
  SELECT *
  FROM (
    SELECT prodname, EXTRACT(YEAR FROM factdate) AS year, SUM(actprofit) AS profit
    FROM prodcoffee, factcoffee
    WHERE prodcoffee.productid = factcoffee.productid
    GROUP BY prodname, EXTRACT(YEAR FROM factdate) 
  )
  PIVOT (
   SUM(profit) FOR year in (2012 AS profit2012, 2013 AS profit2013)
  )
  ORDER BY prodname
)
SELECT temp.*, ROUND((profit2013-profit2012)/profit2012*100, 2) AS percentage_growth
FROM temp
ORDER BY (profit2013-profit2012)/profit2012 ASC;
-------
WITH product_expense AS (
  SELECT prodname AS product, EXTRACT(YEAR FROM factdate) AS YEAR, SUM(actmarkcost) AS mktexpense, SUM(actsales) AS sales
  FROM prodcoffee, factcoffee
  WHERE prodcoffee.productid = factcoffee.productid
  GROUP BY prodname, EXTRACT(YEAR FROM factdate)
  ORDER BY prodname, year
),
mktexpense_growth AS (
  SELECT *
  FROM (
    SELECT product, year, mktexpense
    FROM product_expense
  )
  PIVOT (
    SUM(mktexpense) FOR year IN (2012 AS mkt2012, 2013 AS mkt2013)
  )
  ORDER BY product ASC
),
sales_growth AS (
  SELECT *
  FROM (
    SELECT product, year, sales
    FROM product_expense
  )
  PIVOT (
    SUM(sales) FOR year in (2012 AS sales2012, 2013 AS sales2013) 
  )
  ORDER BY product ASC
)
SELECT *
FROM mktexpense_growth;

SELECT mktexpense_growth.state, (mkt2013-mkt2012) AS expense_growth, (sales2013-sales2012) AS sales_growth,
        (sales2013-sales2012)/(1+(mkt2013-mkt2012)) AS correlation
FROM mktexpense_growth, sales_growth
WHERE mktexpense_growth.state = sales_growth.state
ORDER BY correlation;

SELECT product, EXTRACT(YEAR FROM factdate), SUM(actmarkcost)
FROM statecoffee, areacoffee, factcoffee
WHERE statecoffee.stateid = areacoffee.stateid
      AND areacoffee.area_code = factcoffee.areaid
GROUP BY state, EXTRACT(YEAR FROM factdate)
ORDER BY state ASC;
---------------
SELECT *
FROM (
  SELECT EXTRACT(YEAR FROM factdate) AS year, EXTRACT(MONTH FROM factdate) AS month, SUM(actsales) AS sales
  FROM factcoffee
  GROUP BY EXTRACT(YEAR FROM factdate), EXTRACT(MONTH FROM factdate)
)
PIVOT (
  SUM(sales) FOR year IN (2012, 2013)
)
ORDER BY month;

CREATE OR REPLACE VIEW season AS
  SELECT state, prodname AS product, EXTRACT(YEAR FROM factdate) AS year, EXTRACT(MONTH FROM factdate) AS month, SUM(actsales) AS sales
  FROM statecoffee, areacoffee, prodcoffee, factcoffee
  WHERE statecoffee.stateid = areacoffee.stateid
        AND areacoffee.area_code = factcoffee.areaid
        AND prodcoffee.productid = factcoffee.productid
  GROUP BY state, prodname, EXTRACT(YEAR FROM factdate), EXTRACT(MONTH FROM factdate)
  ORDER BY state ASC, prodname ASC, year ASC, month ASC;

WITH product_level AS (
  SELECT product, year, month, SUM(sales) AS sales
  FROM season
  GROUP BY product, year, month
),
product_2012 AS (
  SELECT *
  FROM (
    SELECT product, month, ROW_NUMBER() OVER (PARTITION BY product ORDER BY sales) AS rank
    FROM product_level
    WHERE year = 2012
  )
  ORDER BY product ASC, month ASC
),
product_2013 AS (
  SELECT *
  FROM (
    SELECT product, month, ROW_NUMBER() OVER (PARTITION BY product ORDER BY sales) AS rank
    FROM product_level
    WHERE year = 2013
  )
  ORDER BY product ASC, month ASC
),
product_match AS (
  SELECT product_2012.product, product_2012.month, product_2012.rank AS rank2012, product_2013.rank AS rank2013,
          (CASE WHEN product_2012.rank = product_2013.rank THEN 1 ELSE 0 END) AS match
  FROM product_2012, product_2013
  WHERE product_2012.product = product_2013.product
        AND product_2012.month = product_2013.month
  ORDER BY product ASC, month ASC
)
SELECT product, ROUND(AVG(match)*100, 0) AS percent_match 
FROM product_match
GROUP BY product
ORDER BY percent_match DESC;

WITH state_level_2012 AS (
  SELECT state, product, month, ROW_NUMBER() OVER (PARTITION BY state, product ORDER BY sales) AS rank
  FROM season
  WHERE year = 2012
),
state_level_2013 AS (
  SELECT state, product, month, ROW_NUMBER() OVER (PARTITION BY state, product ORDER BY sales) AS rank
  FROM season
  WHERE year = 2013
),
state_level_match AS (
  SELECT state_level_2012.state, state_level_2012.product, state_level_2012.month, 
          state_level_2012.rank AS rank2012, state_level_2013.rank AS rank2013,
          (CASE WHEN state_level_2012.rank = state_level_2013.rank THEN 1 ELSE 0 END) AS match
  FROM state_level_2012, state_level_2013
  WHERE state_level_2012.state = state_level_2013.state
        AND state_level_2012.product = state_level_2013.product
        AND state_level_2012.month = state_level_2013.month
  ORDER BY state ASC, product ASC, month ASC
)
SELECT state, product, ROUND(AVG(match)*100, 0) AS percent_match
FROM state_level_match
GROUP BY state, product
ORDER BY percent_match DESC;

ALTER TABLE factcoffee
  ADD quarter VARCHAR2(4);
  
UPDATE factcoffee
  SET quarter = TO_CHAR(factdate, '"Q"Q');

WITH quarter_sales AS (
  SELECT EXTRACT(YEAR FROM factdate) AS year, quarter, SUM(actsales) AS sales
  FROM factcoffee
  GROUP BY EXTRACT(YEAR FROM factdate), quarter
)
SELECT *
FROM quarter_sales
PIVOT (
 SUM(sales) FOR quarter IN ('Q1' AS Q1, 'Q2' AS Q2, 'Q3' AS Q3, 'Q4' AS Q4)
)
ORDER BY year;
----------------------------------------
WITH quarter_profit AS (
  SELECT EXTRACT(YEAR FROM factdate) AS year, quarter, SUM(actprofit) AS profit
  FROM factcoffee
  GROUP BY EXTRACT(YEAR FROM factdate), quarter
)
SELECT *
FROM quarter_profit
PIVOT (
 SUM(profit) FOR quarter IN ('Q1' AS Q1, 'Q2' AS Q2, 'Q3' AS Q3, 'Q4' AS Q4)
)
ORDER BY year;
-------------------------------------------
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE quarterly_sales';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
CREATE TABLE quarterly_sales AS (
  SELECT *
  FROM (
    SELECT state, prodname AS product, EXTRACT(YEAR FROM factdate) AS year, quarter,
            SUM(actsales) AS sales, SUM(actprofit) AS profit, SUM(actmarkcost) AS mktexpense,
            ROUND(SUM(actprofit)/SUM(actsales), 2)*100 AS percent_margin,
            ROW_NUMBER() OVER (PARTITION BY EXTRACT(YEAR FROM factdate), quarter ORDER BY SUM(actsales) DESC) AS sales_rank
    FROM statecoffee, areacoffee, prodcoffee, factcoffee
    WHERE statecoffee.stateid = areacoffee.stateid
          AND areacoffee.area_code = factcoffee.areaid
          AND prodcoffee.productid = factcoffee.productid
    GROUP BY state, prodname, EXTRACT(YEAR FROM factdate), quarter
    ORDER BY state ASC, product ASC, year ASC, quarter ASC
  )
);

SELECT *
FROM quarterly_sales;
-------------------------------------------
SELECT manager, SUM(ordsales) AS sales
FROM managers, customers, orderdet
WHERE managers.regid = customers.custreg
      AND customers.custid = orderdet.custid
GROUP BY manager
ORDER BY sales DESC;
--------------------------------------------
SELECT prodname AS product, ROUND(AVG(ordshipdate-orddate), 0) AS shipping_time
FROM products, orderdet
WHERE products.prodid = orderdet.prodid
GROUP BY prodname
ORDER BY shipping_time DESC;
---------------------------------------------
WITH total_cust AS (
  SELECT COUNT(DISTINCT custid) AS total_customers
  FROM customers
),
total_rev AS (
  SELECT SUM(ordsales) AS total_revenue
  FROM orderdet
)
SELECT ROUND(SUM(revenue)/total_revenue,2)
FROM (
  SELECT *
  FROM (
    SELECT custname AS customer, SUM(ordsales) AS revenue
    FROM customers, orderdet
    WHERE customers.custid = orderdet.custid
    GROUP BY custname
    ORDER BY revenue DESC
  ), total_cust
  WHERE ROWNUM <= total_customers*0.1
), total_rev
GROUP BY total_revenue;
-------------------------------------------------
WITH total_cust AS (
  SELECT COUNT(DISTINCT custid) AS total_customers
  FROM customers
)
SELECT customer
FROM (
  SELECT custname AS customer, COUNT(DISTINCT orderid) AS order_number
  FROM customers, orderdet
  WHERE customers.custid = orderdet.custid
  GROUP BY custname
  ORDER BY order_number DESC
), total_cust
WHERE ROWNUM <= 0.1*total_customers
INTERSECT
SELECT customer
FROM (
  SELECT custname AS customer, SUM(ordsales) AS revenue
  FROM customers, orderdet
  WHERE customers.custid = orderdet.custid
  GROUP BY custname
  ORDER BY revenue DESC
), total_cust
WHERE ROWNUM <= 0.1*total_customers
ORDER BY CUSTOMER ASC;
------------------------------------------------
SELECT EXTRACT(YEAR FROM orddate) AS year, COUNT(DISTINCT orderdet.orderid) AS order_number,
        SUM((CASE WHEN upper(status) LIKE 'RETURNED' THEN 1 ELSE 0 END)) AS total_returns,
        SUM(ordsales) AS total_sales, COUNT(DISTINCT custid) AS customers_served,
        ROUND(SUM(ordshipdate-orddate)/COUNT(DISTINCT orderdet.orderid),2) AS average_shipping_days
FROM orderdet, orders
WHERE orderdet.orderid = orders.orderid
GROUP BY EXTRACT(YEAR FROM orddate);
---------------------------------------------------
SELECT custcity AS city, prodname AS product, SUM(ordsales) AS sales,
        ROW_NUMBER() OVER (PARTITION BY custcity ORDER BY SUM(ordsales) DESC) AS rank
FROM customers, orderdet, products
WHERE customers.custid = orderdet.custid
      AND products.prodid = orderdet.prodid
GROUP BY custcity, prodname
ORDER BY city ASC, rank ASC;
----------------------------------------------------
WITH x AS (
  SELECT custname AS customer, EXTRACT(YEAR FROM orddate) AS year, SUM(ordsales) AS sales
  FROM customers, orderdet
  WHERE customers.custid = orderdet.custid
  GROUP BY custname, EXTRACT(YEAR FROM orddate)
),
by_year AS (
    SELECT *
    FROM x
    PIVOT (
      SUM(sales) FOR year in (2010 AS Y2010, 2011 AS Y2011, 2012 AS Y2012, 2013 AS Y2013)
    )
),
y2010 AS (
  SELECT customer, ROWNUM AS rn
  FROM (
    SELECT *
    FROM by_year
    WHERE Y2010 > 0
    ORDER BY Y2010 DESC
  )
  WHERE ROWNUM <= 5
),
y2011 AS (
  SELECT customer, ROWNUM AS rn
  FROM (
    SELECT *
    FROM by_year
    WHERE Y2011 > 0
    ORDER BY Y2011 DESC
  )
  WHERE ROWNUM <= 5
),
y2012 AS (
  SELECT customer, ROWNUM AS rn
  FROM (
    SELECT *
    FROM by_year
    WHERE Y2012 > 0
    ORDER BY Y2012 DESC
  )
  WHERE ROWNUM <= 5
),
y2013 AS (
  SELECT customer, ROWNUM AS rn
  FROM (
    SELECT *
    FROM by_year
    WHERE Y2013 > 0
    ORDER BY Y2013 DESC
  )
  WHERE ROWNUM <= 5
)
SELECT y2010.customer AS y2010,
        y2011.customer AS y2011,
        y2012.customer AS y2012,
        y2013.customer AS y2013
FROM y2010 JOIN  y2011 ON y2010.rn = y2011.rn
            JOIN y2012 ON y2010.rn = y2012.rn
            JOIN y2013 ON y2010.rn = y2013.rn;

WITH years AS (
  SELECT DISTINCT EXTRACT(YEAR FROM orddate) AS year
  FROM orderdet
)
SELECT *
FROM (
  SELECT custname AS customer, EXTRACT(YEAR FROM orddate) AS year, COUNT(DISTINCT orderid) AS orders, SUM(ordsales) AS sales
  FROM customers, orderdet
  WHERE customers.custid = orderdet.custid
  GROUP BY custname, EXTRACT(YEAR FROM orddate)
)
PIVOT (
  SUM(orders) FOR year IN (2010 AS Y2010, 2011 AS Y2011, 2012 AS Y2012, 2013 AS Y2013)
);

WITH x AS (
  SELECT custname AS customer, EXTRACT(YEAR FROM orddate) AS year, SUM(ordsales) AS sales
  FROM customers, orderdet
  WHERE customers.custid = orderdet.custid
  GROUP BY custname, EXTRACT(YEAR FROM orddate)
),
by_year AS (
    SELECT *
    FROM x
    PIVOT (
      SUM(sales) FOR year in (2010 AS Y2010, 2011 AS Y2011, 2012 AS Y2012, 2013 AS Y2013)
    )
),
y2010 AS (
  SELECT customer
  FROM (
    SELECT *
    FROM by_year
    WHERE Y2010 > 0
  )
),
y2011 AS (
  SELECT customer
  FROM (
    SELECT *
    FROM by_year
    WHERE Y2011 > 0
  )
),
y2012 AS (
  SELECT customer
  FROM (
    SELECT *
    FROM by_year
    WHERE Y2012 > 0
  )
),
y2013 AS (
  SELECT customer
  FROM (
    SELECT *
    FROM by_year
    WHERE Y2013 > 0
  )
),
y101112 AS (
 SELECT customer
 FROM y2010
 UNION
 SELECT customer
 FROM y2011
 UNION
 SELECT customer
 FROM y2012
),
y111213 AS (
 SELECT customer
 FROM y2011
 UNION
 SELECT customer
 FROM y2012
 UNION
 SELECT customer
 FROM y2013
),
y101213 AS (
 SELECT customer
 FROM y2011
 UNION
 SELECT customer
 FROM y2012
 UNION
 SELECT customer
 FROM y2013
),
y101113 AS (
 SELECT customer
 FROM y2011
 UNION
 SELECT customer
 FROM y2012
 UNION
 SELECT customer
 FROM y2013
)
SELECT customer
FROM y2010
MINUS
SELECT customer
FROM y111213;

WITH deal AS (
  SELECT *
  FROM (
    SELECT custname AS customer, EXTRACT(YEAR FROM orddate) AS year,
            (CASE WHEN COUNT(orderid)>0 THEN 1 ELSE 0 END) AS deal
    FROM customers, orderdet
    WHERE customers.custid = orderdet.custid
    GROUP BY custname, EXTRACT(YEAR FROM orddate)
  )
  PIVOT (
   SUM(deal) FOR year IN (2010 AS Y2010, 2011 AS Y2011, 2012 AS Y2012, 2013 AS Y2013)
  )
  ORDER BY customer ASC
)  
SELECT customer, y2010+y2011+y2012+y2013 AS deal
FROM (
  SELECT customer,
          (CASE WHEN y2010 IS NULL THEN 0 ELSE 1 END) AS y2010,
          (CASE WHEN y2011 IS NULL THEN 0 ELSE 1 END) AS y2011,
          (CASE WHEN y2012 IS NULL THEN 0 ELSE 1 END) AS y2012,
          (CASE WHEN y2013 IS NULL THEN 0 ELSE 1 END) AS y2013
  FROM deal
)
WHERE y2010+y2011+y2012+y2013 = 1
ORDER BY deal ASC;
-----------------------------------------------------
SELECT *
FROM (
  SELECT prodsubcat AS subcat, custstate AS state, COUNT (orderid) AS orders
  FROM products, customers, orderdet
  WHERE products.prodid = orderdet.prodid
        AND customers.custid = orderdet.custid
        AND upper(custstate) IN ('WASHINGTON', 'MICHIGAN')
  GROUP BY prodsubcat, custstate
)
PIVOT (
  SUM(orders) FOR state IN ('Washington' AS Washington, 'Michigan' AS Michigan)
)
ORDER BY subcat;
------------------------------------------------------
SELECT quarter, SUM(orderid) AS orders
FROM (
  SELECT TO_CHAR(orddate, '"Q"Q') AS quarter, orderid
  FROM orderdet
)
GROUP BY quarter;
-----------------------------------------------------
WITH temp AS (
  SELECT custseg, TO_CHAR(orddate, '"Q"Q') AS quarter, ordsales
  FROM customers, orderdet
  WHERE customers.custid = orderdet.custid
)
SELECT *
FROM (
  SELECT custseg AS segment, quarter, ROUND(SUM(ordsales), 0) AS sales
  FROM temp
  GROUP BY custseg, quarter
)
PIVOT (
  SUM(sales) FOR quarter IN ('Q1' AS Q1, 'Q2' AS Q2, 'Q3' AS Q3, 'Q4' AS Q4)
)
ORDER BY segment ASC;