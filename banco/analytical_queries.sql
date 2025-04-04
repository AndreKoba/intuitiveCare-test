-- Top 10 operators with highest expenses in the last quarter
SELECT 
    o.razao_social,
    e.evento_despesa,
    e.trimestre,
    e.ano
FROM operadoras o
JOIN eventos_financeiros e ON o.registro_ans = e.registro_ans
WHERE (e.ano = YEAR(CURRENT_DATE) AND e.trimestre = QUARTER(CURRENT_DATE))
    OR (e.ano = YEAR(DATE_SUB(CURRENT_DATE, INTERVAL 1 QUARTER)) 
        AND e.trimestre = QUARTER(DATE_SUB(CURRENT_DATE, INTERVAL 1 QUARTER)))
ORDER BY e.evento_despesa DESC
LIMIT 10;

-- Top 10 operators with highest expenses in the last year
SELECT 
    o.razao_social,
    SUM(e.evento_despesa) as total_despesa
FROM operadoras o
JOIN eventos_financeiros e ON o.registro_ans = e.registro_ans
WHERE e.ano = YEAR(CURRENT_DATE) - 1
GROUP BY o.razao_social
ORDER BY total_despesa DESC
LIMIT 10;