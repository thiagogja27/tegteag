const express = require('express');
const router = express.Router();
const { getDbConnection } = require('../db');

// Rota para login
router.post('/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        const connection = await getDbConnection();
        const query = `
            SELECT id, username, role
            FROM usuarios
            WHERE username = '${username}' AND password = '${password}';
        `;
        const result = await connection.query(query);
        await connection.close();

        if (result.length > 0) {
            // Login bem-sucedido
            res.json({
                success: true,
                message: 'Login realizado com sucesso',
                user: result[0],
            });
        } else {
            // Credenciais inválidas
            res.status(401).json({
                success: false,
                message: 'Usuário ou senha incorretos',
            });
        }
    } catch (err) {
        console.error('Erro ao realizar login:', err.message);
        res.status(500).send('Erro ao realizar login');
    }
});

module.exports = router;
