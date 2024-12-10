const express = require('express');
const router = express.Router();
const { getDbConnection } = require('../db');

// Listar todos os usuários
router.get('/', async (req, res) => {
    try {
        const connection = await getDbConnection();
        const result = await connection.query('SELECT * FROM usuarios');
        await connection.close();
        res.json(result);
    } catch (err) {
        console.error('Erro ao buscar usuários:', err.message);
        res.status(500).send('Erro ao buscar usuários');
    }
});

// Adicionar um novo usuário
router.post('/', async (req, res) => {
    const { username, password, role } = req.body;
    try {
        const connection = await getDbConnection();
        const query = `
            INSERT INTO usuarios (username, password, role)
            VALUES ('${username}', '${password}', '${role}');
        `;
        await connection.query(query);
        await connection.close();
        res.status(201).send('Usuário adicionado com sucesso');
    } catch (err) {
        console.error('Erro ao adicionar usuário:', err.message);
        res.status(500).send('Erro ao adicionar usuário');
    }
});

// Atualizar um usuário
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { username, password, role } = req.body;
    try {
        const connection = await getDbConnection();
        const query = `
            UPDATE usuarios
            SET username = '${username}', password = '${password}', role = '${role}'
            WHERE id = ${id};
        `;
        await connection.query(query);
        await connection.close();
        res.send('Usuário atualizado com sucesso');
    } catch (err) {
        console.error('Erro ao atualizar usuário:', err.message);
        res.status(500).send('Erro ao atualizar usuário');
    }
});

// Remover um usuário
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    try {
        const connection = await getDbConnection();
        const query = `DELETE FROM usuarios WHERE id = ${id};`;
        await connection.query(query);
        await connection.close();
        res.send('Usuário removido com sucesso');
    } catch (err) {
        console.error('Erro ao remover usuário:', err.message);
        res.status(500).send('Erro ao remover usuário');
    }
});

module.exports = router;
