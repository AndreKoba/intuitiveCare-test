-- Import Operadoras data
LOAD DATA INFILE 'c:/Users/kobay/OneDrive/Documentos/Teste-CareIntuitive/Banco/Relatorio_cadop.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- For the financial data (you'll need to adjust the file path for each quarter's file)
LOAD DATA INFILE 'c:/Users/kobay/OneDrive/Documentos/Teste-CareIntuitive/Banco/financial_data.csv'
INTO TABLE eventos_financeiros
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;