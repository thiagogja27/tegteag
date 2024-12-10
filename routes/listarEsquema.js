const { getDbConnection } = require('../db');

async function consultarEsquemaBanco() {
    try {
        const connection = await getDbConnection();

        // Consultar todas as tabelas no banco
        const tabelasQuery = `
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE';
        `;
        const tabelas = await connection.query(tabelasQuery);

        // Para cada tabela, buscar suas colunas
        for (const tabela of tabelas) {
            console.log(`Tabela: ${tabela.TABLE_NAME}`);

            const colunasQuery = `
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '${tabela.TABLE_NAME}';
            `;
            const colunas = await connection.query(colunasQuery);

            console.log(`Colunas da tabela ${tabela.TABLE_NAME}:`);
            colunas.forEach((coluna) => {
                console.log(
                    `  - ${coluna.COLUMN_NAME} (${coluna.DATA_TYPE}${
                        coluna.CHARACTER_MAXIMUM_LENGTH ? `, MaxLength: ${coluna.CHARACTER_MAXIMUM_LENGTH}` : ''
                    })`
                );
            });
        }

        await connection.close();
    } catch (err) {
        console.error('Erro ao consultar o esquema do banco:', err.message);
    }
}

consultarEsquemaBanco();
