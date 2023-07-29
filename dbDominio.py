import pypyodbc as pypyodbc

# Conexão com BD Domínio
conn = pypyodbc.connect(
    "Driver={SQL Server};"
    "Server=srv4;"
    "Database=AutomateLog;"
    "Trusted_Connection=yes;"
)
RodarQuery = conn.cursor()

def consulta(ccm):
    dSQLEmpresa = (f"""
    
        IF NOT (
        SELECT COUNT(*) FROM (
        SELECT CAST(CODI_EMP AS VARCHAR)+'-'+APELIDO APELIDO
        FROM (SELECT codclt FROM Confirp..gectclt 
        WHERE SUBSTRING(RTRIM(LTRIM(REPLACE(REPLACE(REPLACE(insmun,'.',''),'-',''),'/',''))),1,8) = '{ccm}') AS A LEFT JOIN (SELECT CODI_EMP, APELIDO 
        FROM OPENQUERY(SRVDOMINIOPRD,'SELECT CODI_EMP, APEL_EMP AS "Apelido" FROM BETHADBA.GEEMPRE') AS A) AS B ON A.codclt=B.CODI_EMP WHERE APELIDO IS NOT NULL
        ) AS A
        ) > 0
        BEGIN SELECT 0 APELIDO END
        ELSE
        BEGIN  
        SELECT CAST(CODI_EMP AS VARCHAR)+'-'+APELIDO APELIDO
        FROM (SELECT codclt FROM Confirp..gectclt 
        WHERE SUBSTRING(RTRIM(LTRIM(REPLACE(REPLACE(REPLACE(insmun,'.',''),'-',''),'/',''))),1,8) = '{ccm}') AS A LEFT JOIN (SELECT CODI_EMP, APELIDO 
        FROM OPENQUERY(SRVDOMINIOPRD,'SELECT CODI_EMP, APEL_EMP AS "Apelido" FROM BETHADBA.GEEMPRE') AS A) AS B ON A.codclt=B.CODI_EMP
        WHERE APELIDO IS NOT NULL END
           
        """)

    RodarQuery.execute(dSQLEmpresa)  # execute serve para rodar a query
    dEmp = RodarQuery.fetchall()  # Fetchall serve para verificar os valores retornados
    return dEmp[0][0]
print('Teste de versionamento 29/07/2023')
print("Vou  colocar mais um print pra teste")