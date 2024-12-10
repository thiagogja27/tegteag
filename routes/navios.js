const express = require('express');
const router = express.Router();
const { getDbConnection } = require('../db');
const moment = require('moment');

// Rota para listar todos os navios (GET /navios)
router.get('/', async (req, res) => {
    try {
        const connection = await getDbConnection();
        const query = 'SELECT * FROM Navios';
        const result = await connection.query(query);
        res.status(200).json(result);
    } catch (err) {
        res.status(500).json({ message: 'Erro ao buscar navios.', error: err.message });
    }
});

// Rota para buscar detalhes de um navio específico (GET /navios/:id)
router.get('/:id', async (req, res) => {
    const { id } = req.params;
    try {
        const connection = await getDbConnection();
        const query = 'SELECT * FROM Navios WHERE Id = ?';
        const result = await connection.query(query, [id]);
        if (result.length === 0) {
            return res.status(404).json({ message: 'Navio não encontrado.' });
        }
        res.status(200).json(result[0]);
    } catch (err) {
        res.status(500).json({ message: 'Erro ao buscar navio.', error: err.message });
    }
});

// Rota para salvar dados de navios (POST /navios)
router.post('/', async (req, res) => {
    const { data, nome_navio, atracacao, inicio, talhe, saida, status } = req.body;
    if (!data || !nome_navio || !atracacao || !inicio || !talhe || !saida || !status) {
        return res.status(400).json({ message: 'Todos os campos são obrigatórios.' });
    }

    const formattedData = moment(data).format('YYYY-MM-DD HH:mm:ss');
    const formattedAtracacao = moment(atracacao).format('YYYY-MM-DD HH:mm:ss');
    const formattedInicio = moment(inicio).format('YYYY-MM-DD HH:mm:ss');
    const formattedTalhe = moment(talhe).format('YYYY-MM-DD HH:mm:ss');
    const formattedSaida = moment(saida).format('YYYY-MM-DD HH:mm:ss');

    let connection;

    try {
        connection = await getDbConnection();
        const query = `
            INSERT INTO Navios (Data, NomeNavio, Atracacao, Inicio, Talhe, Saida, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        `;
        const result = await connection.query(query, [
            formattedData,
            nome_navio,
            formattedAtracacao,
            formattedInicio,
            formattedTalhe,
            formattedSaida,
            status,
        ]);
        res.status(201).json({ message: 'Navio salvo com sucesso!' });
    } catch (err) {
        res.status(500).json({ message: 'Erro ao salvar navio.', error: err.message });
    } finally {
        if (connection) {
            connection.close();
        }
    }
});

// Rota para atualizar um navio (PUT /navios/:id)
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { data, nome_navio, atracacao, inicio, talhe, saida, status } = req.body;

    console.log("Recebido para atualização:", { id, data, nome_navio, atracacao, inicio, talhe, saida, status });

    if (!data || !nome_navio || !atracacao || !inicio || !talhe || !saida || !status) {
        console.warn("Campos obrigatórios ausentes");
        return res.status(400).json({ message: 'Todos os campos são obrigatórios.' });
    }

    const formattedData = moment(data).format('YYYY-MM-DD HH:mm:ss');
    const formattedAtracacao = moment(atracacao).format('YYYY-MM-DD HH:mm:ss');
    const formattedInicio = moment(inicio).format('YYYY-MM-DD HH:mm:ss');
    const formattedTalhe = moment(talhe).format('YYYY-MM-DD HH:mm:ss');
    const formattedSaida = moment(saida).format('YYYY-MM-DD HH:mm:ss');

    try {
        const connection = await getDbConnection();
        const query = `
            UPDATE Navios
            SET Data = ?, NomeNavio = ?, Atracacao = ?, Inicio = ?, Talhe = ?, Saida = ?, Status = ?
            WHERE Id = ?;
        `;
        const result = await connection.query(query, [
            formattedData,
            nome_navio,
            formattedAtracacao,
            formattedInicio,
            formattedTalhe,
            formattedSaida,
            status,
            id,
        ]);

        console.log("Resultado da atualização:", result);

        if (result.affectedRows === 0) {
            return res.status(404).json({ message: 'Navio não encontrado.' });
        }
        res.status(200).json({ message: 'Navio atualizado com sucesso!' });
    } catch (err) {
        console.error("Erro ao atualizar navio:", err);
        res.status(500).json({ message: 'Erro ao atualizar navio.', error: err.message });
    }
});

// Rota para excluir um navio (DELETE /navios/:id)
router.delete('/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const connection = await getDbConnection();
        const query = 'DELETE FROM Navios WHERE Id = ?';
        const result = await connection.query(query, [id]);
        if (result.affectedRows === 0) {
            return res.status(404).json({ message: 'Navio não encontrado.' });
        }
        res.status(200).json({ message: 'Navio excluído com sucesso!' });
    } catch (err) {
        res.status(500).json({ message: 'Erro ao excluir navio.', error: err.message });
    }
});

module.exports = router;
