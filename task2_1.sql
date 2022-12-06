SELECT
    ID
       , ISNULL([A], 0) AS A
       , ISNULL([B], 0) AS B
       , ISNULL([C], 0) AS C
FROM (
    SELECT ID, Name, Val
    FROM A) as SourceT
PIVOT (
    SUM(Val)
    FOR Name in ([A], [B], [C])
) as PivotT
