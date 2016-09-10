/*Part A*/
/*A*/
CREATE VIEW TEMP1 AS (
  SELECT STATE, AREA_CODE, SUM(ACTSALES) AS SALES
  FROM STATECOFFEE, AREACOFFEE, FACTCOFFEE
  WHERE STATECOFFEE.STATEID=AREACOFFEE.STATEID AND
        AREACOFFEE.AREA_CODE=FACTCOFFEE.AREAID AND
        EXTRACT(YEAR FROM FACTDATE) = 2013
  GROUP BY STATE, AREA_CODE
);

CREATE VIEW TEMP2 AS (
  SELECT STATE, AVG(SALES) AS AVGSALES
  FROM TEMP1
  GROUP BY STATE
);

SELECT TEMP1.STATE, AREA_CODE, SALES
FROM TEMP1, TEMP2
WHERE TEMP1.STATE = TEMP2.STATE AND
      TEMP1.SALES > 0.1*TEMP2.AVGSALES
ORDER BY SALES DESC
)

SELECT PRODNAME, TOTALSALES, ROUND(TOTALPROFIT/TOTALSALES,2) AS GROSSMARGIN
FROM (
SELECT PRODNAME, SUM(ACTSALES) AS TOTALSALES, SUM(ACTPROFIT) TOTALPROFIT
FROM PRODCOFFEE, FACTCOFFEE
WHERE PRODCOFFEE.PRODUCTID=FACTCOFFEE.PRODUCTID
GROUP BY PRODNAME
)
ORDER BY TOTALSALES DESC;

SELECT *
FROM (
SELECT AREAID, PRODLINE, SUM(ACTPROFIT) AS TOTALPROFIT
FROM FACTCOFFEE, PRODCOFFEE
WHERE FACTCOFFEE.PRODUCTID=PRODCOFFEE.PRODUCTID AND
      EXTRACT(YEAR FROM FACTDATE) = 2012
GROUP BY AREAID, PRODLINE
)
PIVOT (
  COUNT(PRODLINE)
  FOR PRODLINE IN ('Beans', 'Leaves')
)
ORDER BY AREAID;

CREATE VIEW TEMP_LEAVES AS
SELECT AREAID, SUM(ACTPROFIT) AS SUBTOTAL
FROM FACTCOFFEE, PRODCOFFEE
WHERE FACTCOFFEE.PRODUCTID=PRODCOFFEE.PRODUCTID AND
      PRODCOFFEE.PRODLINE='Leaves'
GROUP BY AREAID;

CREATE VIEW TEMP_BEANS AS
SELECT AREAID, SUM(ACTPROFIT) AS SUBTOTAL
FROM FACTCOFFEE, PRODCOFFEE
WHERE FACTCOFFEE.PRODUCTID=PRODCOFFEE.PRODUCTID AND
      PRODCOFFEE.PRODLINE='Beans'
GROUP BY AREAID;

SELECT TEMP_LEAVES.AREAID AS AREAID,
        TEMP_LEAVES.SUBTOTAL AS LEAVESPROFIT,
        TEMP_BEANS.SUBTOTAL AS BEANSPROFIT
FROM TEMP_LEAVES, TEMP_BEANS
WHERE TEMP_LEAVES.AREAID=TEMP_BEANS.AREAID AND
      TEMP_LEAVES.SUBTOTAL > 2*TEMP_BEANS.SUBTOTAL AND
      TEMP_BEANS.SUBTOTAL > 0
ORDER BY LEAVESPROFIT;

SELECT AREAID, SUM(ACTPROFIT)
FROM FACTCOFFEE, PRODCOFFEE
WHERE FACTCOFFEE.PRODUCTID=PRODCOFFEE.PRODUCTID AND
      PRODLINE='Beans'
GROUP BY AREAID;

/*B*/
SELECT * FROM (
SELECT AREAID, EXTRACT(YEAR FROM FACTDATE) AS YEAR, SUM(ACTPROFIT) AS TOTALPROFIT
FROM FACTCOFFEE
GROUP BY AREAID, EXTRACT(YEAR FROM FACTDATE)
)
PIVOT (
SUM(TOTALPROFIT) FOR (YEAR) IN ('2012' AS FY2012, '2013' AS FY2013)
)
ORDER BY AREAID;