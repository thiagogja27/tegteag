const { getDbConnection } = require('./db');

async function testConnection() {
    try {
        const connection = await getDbConnection();
        const result = await connection.query("SELECT name FROM sys.tables");
        console.log('Tabelas no banco de dados:', result);
        await connection.close(); // Fechar conexão após o uso
    } catch (err) {
        console.error('Erro ao testar a conexão:', err.message);
    }
}

testConnection();
