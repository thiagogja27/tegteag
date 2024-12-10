const express = require('express');
const router = express.Router();
const { getDbConnection } = require('../db');
const moment = require("moment");

// Rota para calcular percentuais de capacidade utilizada por empresa
router.get('/percentuais', async (req, res) => {
    try {
        console.log("Iniciando consulta de percentuais...");
        const connection = await getDbConnection();

        // Consulta ajustada para refletir a nova estrutura da tabela
        const query = `
            SELECT 
                m.empresa,
                SUM(m.toneladas_vagao + m.toneladas_caminhao) AS total_utilizado,
                MAX(c.capacidade_total) AS capacidade_total,
                CASE 
                    WHEN MAX(c.capacidade_total) > 0 THEN 
                        (SUM(m.toneladas_vagao + m.toneladas_caminhao) / MAX(c.capacidade_total)) * 100
                    ELSE 0
                END AS percentual_utilizado
            FROM 
                movimentacoes m
            LEFT JOIN 
                capacidades c ON c.terminal = 'Geral'
            WHERE 
                m.tipo = 'Entrada'
            GROUP BY 
                m.empresa;
        `;
        console.log('Consulta SQL executada:', query);

        const result = await connection.query(query);
        console.log('Resultado da consulta:', result);

        if (!result || result.length === 0) {
            console.error('Nenhum dado encontrado.');
            return res.status(404).json({ message: 'Nenhum dado encontrado.' });
        }

        const percentuais = result.map(row => ({
            empresa: row.empresa,
            total_utilizado: row.total_utilizado || 0,
            capacidade_total: row.capacidade_total || 0,
            percentual_utilizado: (row.percentual_utilizado || 0).toFixed(2)
        }));

        console.log('Percentuais calculados:', percentuais);
        res.json(percentuais);
    } catch (err) {
        console.error('Erro ao calcular percentuais:', err.message);
        res.status(500).send('Erro ao calcular percentuais');
    }
});

// Inserir capacidade
router.post("/", async (req, res) => {
    const { terminal, capacidade_total } = req.body;

    // Verifique se os campos necessários estão presentes
    if (!terminal || !capacidade_total) {
        return res.status(400).json({ message: "Terminal e capacidade total são obrigatórios." });
    }

    // Verifique se capacidade_total é um número válido
    if (isNaN(capacidade_total) || capacidade_total <= 0) {
        return res.status(400).json({ message: "A capacidade total deve ser um número válido maior que 0." });
    }

    // Usando moment para garantir o formato de data adequado
    const formattedDate = moment().format("YYYY-MM-DD HH:mm:ss");

    console.log('Valores recebidos para inserção:');
    console.log('Terminal:', terminal);
    console.log('Capacidade Total:', capacidade_total);
    console.log('Data de Atualização:', formattedDate); // Exibe a data formatada

    try {
        const connection = await getDbConnection();

        // Query de inserção
        const query = `
            INSERT INTO capacidades (terminal, capacidade_total, data_atualizacao)
            VALUES (?, ?, ?);
        `;
        
        // Passando os parâmetros corretamente para a consulta
        console.log('Consulta SQL:', query);
        console.log('Valores passados para query:', [terminal, capacidade_total, formattedDate]);

        const result = await connection.query(query, [terminal, capacidade_total, formattedDate]);

        console.log('Resultado da inserção no banco:', result);

        // Fechar a conexão ODBC
        await connection.close();

        res.status(201).json({ message: "Capacidade salva com sucesso!" });
    } catch (err) {
        console.error("Erro ao salvar capacidade:", err.message);
        console.error("Detalhes do erro:", err.stack);  // Log detalhado do erro
        res.status(500).json({ message: "Erro ao salvar capacidade.", error: err.message });
    }
});

// Atualizar a capacidade total
router.put('/', async (req, res) => {
    const { capacidade_total } = req.body;

    console.log('Dados recebidos para atualização de capacidade total:', { capacidade_total });

    if (!capacidade_total || capacidade_total <= 0) {
        return res.status(400).send('Capacidade total inválida');
    }

    try {
        const connection = await getDbConnection();
        const query = 'UPDATE capacidades SET capacidade_total = ? WHERE terminal = "Geral"';

        console.log('Executando consulta SQL para atualização:', query);
        const result = await connection.query(query, [capacidade_total]);

        console.log('Resultado da atualização no banco:', result);

        await connection.close();

        res.status(200).send('Capacidade total atualizada com sucesso');
    } catch (err) {
        console.error('Erro ao atualizar capacidade total:', err.message);
        res.status(500).send('Erro ao atualizar capacidade total');
    }
});

module.exports = router;
