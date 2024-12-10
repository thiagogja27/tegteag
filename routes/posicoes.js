const express = require("express");
const router = express.Router();
const { getDbConnection } = require("../db");
const moment = require("moment"); // Biblioteca para manipulação de datas (npm install moment)

// Rota para listar todas as posições (GET /posicoes)
router.get("/", async (req, res) => {
  try {
    console.log("Requisição recebida em GET /posicoes para listar todas as posições.");
    const connection = await getDbConnection();

    const query = "SELECT * FROM Posições";
    const result = await connection.query(query);

    console.log("Lista de posições carregada com sucesso:", result);
    res.status(200).json(result);
  } catch (err) {
    console.error("Erro ao buscar posições:", err);
    res.status(500).json({ message: "Erro ao buscar dados.", error: err.message });
  }
});

// Rota para buscar detalhes de uma posição específica (GET /posicoes/:id)
router.get("/:id", async (req, res) => {
  const { id } = req.params;

  try {
    console.log(`Requisição recebida em GET /posicoes/${id} para buscar detalhes da posição.`);
    const connection = await getDbConnection();

    const query = "SELECT * FROM Posições WHERE ID = ?";
    const result = await connection.query(query, [id]);

    if (result.length === 0) {
      console.warn(`Nenhuma posição encontrada com o ID: ${id}`);
      return res.status(404).json({ message: "Posição não encontrada." });
    }

    console.log("Detalhes da posição encontrados:", result[0]);
    res.status(200).json(result[0]);
  } catch (err) {
    console.error(`Erro ao buscar detalhes da posição com ID ${id}:`, err);
    res.status(500).json({ message: "Erro ao buscar dados.", error: err.message });
  }
});

// Rota para salvar dados de posições (POST /posicoes)
router.post("/", async (req, res) => {
  const { dataHora, ramal, ferrovia, quantidade, tipo, terminal } = req.body;

  console.log("Requisição recebida em POST /posicoes");
  console.log("Dados recebidos:", { dataHora, ramal, ferrovia, quantidade, tipo, terminal });

  // Validação de campos obrigatórios
  if (!dataHora || !ramal || !ferrovia || !quantidade || !tipo || !terminal) {
      console.warn("Erro: Campos obrigatórios ausentes");
      return res.status(400).json({ message: "Todos os campos são obrigatórios." });
  }

  // Converter a data/hora para o formato esperado pelo SQL Server
  const formattedDataHora = moment(dataHora).format("YYYY-MM-DD HH:mm:ss");

  console.log("Data/Hora formatada:", formattedDataHora);

  let connection;

  try {
      console.log("Conectando ao banco de dados...");
      connection = await getDbConnection();

      console.log("Conexão estabelecida. Preparando a consulta SQL.");
      const query = `
          INSERT INTO Posições (DataHora, Ramal, Ferrovia, Quantidade, Tipo, Terminal)
          VALUES (?, ?, ?, ?, ?, ?);
      `;

      console.log("Executando a consulta SQL...");
      const result = await connection.query(query, [
          formattedDataHora,
          ramal,
          ferrovia,
          quantidade,
          tipo,
          terminal,
      ]);

      console.log("Consulta executada com sucesso:", result);

      res.status(201).json({ message: "Dados de posição salvos com sucesso!" });
  } catch (err) {
      console.error("Erro ao salvar dados de posição:", err);
      res.status(500).json({
          message: "Erro ao salvar dados de posição.",
          error: err.message,
      });
  } finally {
      if (connection) {
          console.log("Fechando a conexão...");
          await connection.close();
          console.log("Conexão fechada.");
      }
  }
});


// Rota para atualizar uma posição (PUT /posicoes/:id)
router.put("/:id", async (req, res) => {
  const { id } = req.params;
  const { dataHora, ramal, ferrovia, quantidade, tipo, terminal } = req.body;

  console.log("Requisição recebida em PUT /posicoes");
  console.log("Dados recebidos para atualização:", { dataHora, ramal, ferrovia, quantidade, tipo, terminal });

  // Validação de campos obrigatórios
  if (!dataHora || !ramal || !ferrovia || !quantidade || !tipo || !terminal) {
    console.warn("Erro: Campos obrigatórios ausentes");
    return res.status(400).json({ message: "Todos os campos são obrigatórios." });
  }

  // Converter a data/hora para o formato esperado pelo SQL Server
  const formattedDataHora = moment(dataHora).format("YYYY-MM-DD HH:mm:ss");

  console.log("Data/Hora formatada:", formattedDataHora);

  let connection;

  try {
    console.log("Conectando ao banco de dados...");
    connection = await getDbConnection();

    console.log("Conexão estabelecida. Preparando a consulta SQL.");
    const query = `
      UPDATE Posições
      SET DataHora = ?, Ramal = ?, Ferrovia = ?, Quantidade = ?, Tipo = ?, Terminal = ?
      WHERE ID = ?;
    `;

    console.log("Executando a consulta SQL...");
    const result = await connection.query(query, [
      formattedDataHora,
      ramal,
      ferrovia,
      quantidade,
      tipo,
      terminal,
      id,
    ]);

    console.log("Consulta executada com sucesso:", result);

    if (result.affectedRows === 0) {
      console.warn(`Nenhuma posição encontrada para o ID: ${id}`);
      return res.status(404).json({ message: "Posição não encontrada." });
    }

    res.status(200).json({ message: "Posição atualizada com sucesso!" });
  } catch (err) {
    console.error("Erro ao atualizar posição:", err);
    res.status(500).json({
      message: "Erro ao atualizar posição.",
      error: err.message,
      stack: process.env.NODE_ENV === "development" ? err.stack : undefined,
    });
  } finally {
    if (connection) {
      console.log("Fechando a conexão...");
      await connection.close();
      console.log("Conexão fechada.");
    }
  }
});

// Rota para excluir uma posição (DELETE /posicoes/:id)
router.delete("/:id", async (req, res) => {
    const { id } = req.params;
  
    console.log(`Requisição recebida em DELETE /posicoes/${id}`);
  
    let connection;
  
    try {
      console.log("Conectando ao banco de dados...");
      connection = await getDbConnection();
  
      console.log("Conexão estabelecida. Preparando a consulta SQL.");
      const query = "DELETE FROM Posições WHERE ID = ?";
  
      console.log("Executando a consulta SQL...");
      const result = await connection.query(query, [id]);
  
      console.log("Consulta executada com sucesso:", result);
  
      if (result.affectedRows === 0) {
        console.warn(`Nenhuma posição encontrada para o ID: ${id}`);
        return res.status(404).json({ message: "Posição não encontrada." });
      }
  
      res.status(200).json({ message: "Posição excluída com sucesso!" });
    } catch (err) {
      console.error("Erro ao excluir posição:", err);
      res.status(500).json({
        message: "Erro ao excluir posição.",
        error: err.message,
      });
    } finally {
      if (connection) {
        console.log("Fechando a conexão...");
        await connection.close();
        console.log("Conexão fechada.");
      }
    }
  });
  

module.exports = router;

