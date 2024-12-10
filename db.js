const odbc = require('odbc');

// String de conexão ODBC
const connectionString = "Driver={ODBC Driver 17 for SQL Server};Server=DESKTOP-QUVHV6B;Database=operacional;Trusted_Connection=Yes;";

// Função para conectar ao banco
async function getDbConnection() {
    try {
        const connection = await odbc.connect(connectionString);
        console.log('Conexão bem-sucedida com SQL Server via ODBC!');
        return connection;
    } catch (err) {
        console.error('Erro ao conectar ao SQL Server via ODBC:', err.message);
        throw err;
    }
}

module.exports = { getDbConnection };
