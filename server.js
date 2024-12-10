const express = require('express');
const app = express();
const port = 3000;
const path = require('path');

// Middleware para JSON
app.use(express.json());

// Importação de rotas
const movimentacoesRoutes = require('./routes/movimentacoes');
const usuariosRoutes = require('./routes/usuarios');
const naviosRoutes = require('./routes/navios');
const capacidadesRoutes = require('./routes/capacidades');
const indicadoresRoutes = require('./routes/indicadores');
const authRoutes = require('./routes/auth');
const posicoesRoutes = require('./routes/posicoes');
const chegadasRouter = require('./routes/chegadas');

// Servir arquivos estáticos
app.use(express.static(path.join(__dirname, 'public')));

// Rotas da API
app.use('/movimentacoes', movimentacoesRoutes);
app.use('/usuarios', usuariosRoutes);
app.use('/navios', naviosRoutes);
app.use('/capacidades', capacidadesRoutes);
app.use('/indicadores', indicadoresRoutes);
app.use('/auth', authRoutes);
app.use('/posicoes', posicoesRoutes);
app.use('/chegadas', chegadasRouter);

// Rotas principais para servir páginas HTML
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/insert', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'insert.html'));
});

app.get('/dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

// Iniciar o servidor
app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});
