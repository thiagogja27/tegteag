const express = require('express');
const router = express.Router();
const { getDbConnection } = require('../db');

// Rota para listar movimentações
router.get('/', async (req, res) => {
    try {
        const connection = await getDbConnection();

        const queryAll = `
            SELECT 
                id, -- Incluído para edição e exclusão
                data,
                produto, 
                empresa, 
                CAST(toneladas_vagao AS FLOAT) AS toneladas_vagao,
                CAST(toneladas_caminhao AS FLOAT) AS toneladas_caminhao,
                quantidade_vagoes,
                quantidade_caminhoes,
                tipo
            FROM movimentacoes;
        `;

        const queryGrouped = `
            SELECT 
                produto, 
                SUM(CAST(toneladas_vagao AS FLOAT) + CAST(toneladas_caminhao AS FLOAT)) AS total_toneladas
            FROM movimentacoes
            GROUP BY produto;
        `;

        const allDataResult = await connection.query(queryAll);
        const groupedDataResult = await connection.query(queryGrouped);

        await connection.close();

        console.log("Movimentações carregadas com sucesso.");

        res.json({
            allData: allDataResult,
            groupedData: groupedDataResult
        });
    } catch (err) {
        console.error('Erro ao buscar movimentações:', err.message);
        res.status(500).send('Erro ao buscar movimentações');
    }
});

// Rota para inserir movimentações
router.post('/', async (req, res) => {
    const {
        data,
        produto,
        empresa,
        toneladas_vagao,
        toneladas_caminhao,
        quantidade_vagoes,
        quantidade_caminhoes,
        tipo
    } = req.body;

    console.log("Recebendo dados para inserção:", {
        data,
        produto,
        empresa,
        toneladas_vagao,
        toneladas_caminhao,
        quantidade_vagoes,
        quantidade_caminhoes,
        tipo
    });

    // Validação básica
    if (!data || !produto || !empresa || !tipo || 
        (!toneladas_vagao && !toneladas_caminhao)) {
        console.warn("Campos obrigatórios ausentes.");
        return res.status(400).json({ message: "Todos os campos obrigatórios devem ser preenchidos." });
    }

    try {
        console.log("Tentando conectar ao banco de dados...");
        const connection = await getDbConnection();

        const query = `
            INSERT INTO movimentacoes (
                data, 
                produto, 
                empresa, 
                toneladas_vagao, 
                toneladas_caminhao, 
                quantidade_vagoes, 
                quantidade_caminhoes, 
                tipo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        `;

        console.log("Executando query:", query);
        console.log("Parâmetros:", [
            data,
            produto,
            empresa,
            toneladas_vagao || 0,
            toneladas_caminhao || 0,
            quantidade_vagoes || 0,
            quantidade_caminhoes || 0,
            tipo
        ]);

        const result = await connection.query(query, [
            data,
            produto,
            empresa,
            toneladas_vagao || 0,
            toneladas_caminhao || 0,
            quantidade_vagoes || 0,
            quantidade_caminhoes || 0,
            tipo
        ]);

        console.log("Query executada com sucesso:", result);

        await connection.close();
        console.log("Conexão ao banco de dados encerrada.");

        res.status(201).json({ message: 'Movimentação salva com sucesso!' });
    } catch (err) {
        console.error("Erro ao salvar movimentação:", err.message);
        res.status(500).json({ message: 'Erro ao salvar movimentação.', error: err.message });
    }
});

// Rota para editar movimentações
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const {
        data,
        produto,
        empresa,
        toneladas_vagao,
        toneladas_caminhao,
        quantidade_vagoes,
        quantidade_caminhoes,
        tipo
    } = req.body;

    console.log("Recebendo dados para edição:", {
        id,
        data,
        produto,
        empresa,
        toneladas_vagao,
        toneladas_caminhao,
        quantidade_vagoes,
        quantidade_caminhoes,
        tipo
    });

    if (!data || !produto || !empresa || !tipo ||
        (!toneladas_vagao && !toneladas_caminhao)) {
        return res.status(400).json({ message: "Todos os campos obrigatórios devem ser preenchidos." });
    }

    try {
        const connection = await getDbConnection();

        const query = `
            UPDATE movimentacoes
            SET 
                data = ?, 
                produto = ?, 
                empresa = ?, 
                toneladas_vagao = ?, 
                toneladas_caminhao = ?, 
                quantidade_vagoes = ?, 
                quantidade_caminhoes = ?, 
                tipo = ?
            WHERE id = ?;
        `;

        await connection.query(query, [
            data,
            produto,
            empresa,
            toneladas_vagao || 0,
            toneladas_caminhao || 0,
            quantidade_vagoes || 0,
            quantidade_caminhoes || 0,
            tipo,
            id
        ]);

        console.log("Movimentação atualizada com sucesso.");

        await connection.close();

        res.status(200).json({ message: 'Movimentação atualizada com sucesso!' });
    } catch (err) {
        console.error('Erro ao editar movimentação:', err.message);
        res.status(500).json({ message: 'Erro ao editar movimentação.', error: err.message });
    }
});

// Rota para excluir movimentações
router.delete('/:id', async (req, res) => {
    const { id } = req.params;

    console.log("Recebendo solicitação para exclusão:", { id });

    try {
        const connection = await getDbConnection();

        const query = `
            DELETE FROM movimentacoes WHERE id = ?;
        `;

        await connection.query(query, [id]);

        console.log("Movimentação excluída com sucesso.");

        await connection.close();

        res.status(200).json({ message: 'Movimentação excluída com sucesso!' });
    } catch (err) {
        console.error('Erro ao excluir movimentação:', err.message);
        res.status(500).json({ message: 'Erro ao excluir movimentação.', error: err.message });
    }
});

module.exports = router;
