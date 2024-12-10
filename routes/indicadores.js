const express = require('express');
const router = express.Router();
const { getDbConnection } = require('../db');

// Listar indicadores
router.get('/', async (req, res) => {
    try {
        const connection = await getDbConnection();
        const result = await connection.query('SELECT * FROM indicadores');
        await connection.close();
        res.json(result);
    } catch (err) {
        console.error('Erro ao buscar indicadores:', err.message);
        res.status(500).send('Erro ao buscar indicadores');
    }
});

// Inserir indicador
router.post('/', async (req, res) => {
    const { data, terminal, tipo, valor } = req.body;
    try {
        const connection = await getDbConnection();
        const query = `
            INSERT INTO indicadores (data, terminal, tipo, valor)
            VALUES ('${data}', '${terminal}', '${tipo}', ${valor});
        `;
        await connection.query(query);
        await connection.close();
        res.status(201).send('Indicador adicionado com sucesso');
    } catch (err) {
        console.error('Erro ao adicionar indicador:', err.message);
        res.status(500).send('Erro ao adicionar indicador');
    }
});

module.exports = router;
