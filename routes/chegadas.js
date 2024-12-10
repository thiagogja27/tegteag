const express = require("express");
const router = express.Router();
const { getDbConnection } = require("../db");
const moment = require("moment");

// Rota para listar todas as chegadas (GET /chegadas)
router.get("/", async (req, res) => {
    try {
        console.log("Iniciando GET em /chegadas...");
        const connection = await getDbConnection();

        const query = "SELECT * FROM Chegadas";
        const result = await connection.query(query);

        console.log("Resultado do banco:", result);
        res.status(200).json(result);
    } catch (err) {
        console.error("Erro ao buscar chegadas:", err);
        res.status(500).json({ message: "Erro ao buscar dados.", error: err.message });
    }
});

// Rota para editar uma chegada existente (PUT /chegadas/:id)
router.put("/:id", async (req, res) => {
    const { id } = req.params; // ID da chegada a ser editada
    const { dataHora, quantidade, produto, ferrovia, empresa } = req.body;

    console.log("Dados recebidos no PUT /chegadas:", { id, dataHora, quantidade, produto, ferrovia, empresa });

    // Verifica se todos os campos obrigatórios foram enviados
    if (!dataHora || !quantidade || !produto || !ferrovia || !empresa) {
        console.warn("Erro: Campos obrigatórios ausentes.");
        return res.status(400).json({ message: "Todos os campos são obrigatórios." });
    }

    const formattedDataHora = moment(dataHora).format("YYYY-MM-DD HH:mm:ss");

    try {
        const connection = await getDbConnection();

        // Query de atualização
        const query = `
            UPDATE Chegadas
            SET DataHora = ?, Quantidade = ?, Produto = ?, Ferrovia = ?, Empresa = ?
            WHERE ID = ?;
        `;

        const result = await connection.query(query, [
            formattedDataHora,
            quantidade,
            produto,
            ferrovia,
            empresa,
            id,
        ]);

        // Verifica se algum registro foi alterado
        if (result.affectedRows === 0) {
            console.warn(`Nenhuma chegada encontrada para o ID: ${id}`);
            return res.status(404).json({ message: "Chegada não encontrada." });
        }

        console.log("Chegada atualizada com sucesso:", result);
        res.status(200).json({ message: "Chegada atualizada com sucesso!" });
    } catch (err) {
        console.error("Erro ao atualizar chegada:", err);
        res.status(500).json({ message: "Erro ao atualizar chegada.", error: err.message });
    }
});

// Rota para inserir uma nova chegada (POST /chegadas)
router.post("/", async (req, res) => {
    const { dataHora, quantidade, produto, ferrovia, empresa } = req.body;

    console.log("Dados recebidos no POST /chegadas:", { dataHora, quantidade, produto, ferrovia, empresa });

    if (!dataHora || !quantidade || !produto || !ferrovia || !empresa) {
        console.warn("Erro: Campos obrigatórios ausentes.");
        return res.status(400).json({ message: "Todos os campos são obrigatórios." });
    }

    const formattedDataHora = moment(dataHora).format("YYYY-MM-DD HH:mm:ss");

    try {
        console.log("Conectando ao banco de dados...");
        const connection = await getDbConnection();

        const query = `
            INSERT INTO Chegadas (DataHora, Quantidade, Produto, Ferrovia, Empresa)
            VALUES (?, ?, ?, ?, ?);
        `;
        const result = await connection.query(query, [
            formattedDataHora,
            quantidade,
            produto,
            ferrovia,
            empresa,
        ]);

        console.log("Resultado da inserção no banco:", result);
        res.status(201).json({ message: "Chegada salva com sucesso!" });
    } catch (err) {
        console.error("Erro ao salvar chegada:", err);
        res.status(500).json({ message: "Erro ao salvar chegada.", error: err.message });
    }
});

// Rota para excluir uma chegada (DELETE /chegadas/:id)
router.delete("/:id", async (req, res) => {
    const { id } = req.params;

    console.log(`Recebendo DELETE para ID: ${id}`);
    if (!id) {
        return res.status(400).json({ message: "ID não fornecido." });
    }

    try {
        const connection = await getDbConnection();

        const query = "DELETE FROM Chegadas WHERE ID = ?";
        const result = await connection.query(query, [id]);

        if (result.affectedRows === 0) {
            console.warn(`Nenhuma chegada encontrada para o ID: ${id}`);
            return res.status(404).json({ message: "Chegada não encontrada." });
        }

        console.log("Chegada excluída com sucesso:", result);
        res.status(200).json({ message: "Chegada excluída com sucesso!" });
    } catch (err) {
        console.error("Erro ao excluir chegada:", err);
        res.status(500).json({ message: "Erro ao excluir chegada.", error: err.message });
    }
});

module.exports = router;
