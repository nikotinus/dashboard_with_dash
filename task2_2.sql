SELECT 
    t.ID
    , IFNULL(A.Val, 0) as 'A'
    , IFNULL(B.Val, 0) as 'B'
    , IFNULL(C.Val, 0) as 'C'
FROM
    (SELECT DISTINCT ID
    FROM A) AS t
    LEFT JOIN (
        SELECT ID, SUM(Val) as Val
        FROM A
        GROUP BY ID, Name
        HAVING Name = "A") as A
    on A.ID = t.ID
    LEFT JOIN (
        SELECT ID, SUM(Val) as Val
        FROM A
        GROUP BY ID, Name
        HAVING Name = "B") as B
    on B.ID = t.ID
    LEFT JOIN (
        SELECT ID, SUM(Val) as Val
        FROM A
        GROUP BY ID, Name
        HAVING Name = "C") as C
    on C.ID = t.ID
