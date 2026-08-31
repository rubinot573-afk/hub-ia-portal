const express = require('express');
const router = express.Router();
const { MongoClient } = require('mongodb');
const { z } = require('zod'); // Importação necessária para tratar os erros do Zod

// 1. Importa o validador que criamos para essa rota
const { cliqueSchema } = require('../schemas/cliqueValidator');

// Configurações do MongoDB Atlas obtidas do seu código original
const url = process.env.MONGO_URI; 
const client = new MongoClient(url);
const dbName = 'HubIA_Metrics';

// ==========================================
// ROTA POST: REGISTRAR O CLIQUE (COM ZOD)
// ==========================================
router.post('/registrar', async (req, res) => {
    try {
        // 🔥 A MÁGICA DO SEGURANÇA:
        // O Zod valida o req.body de acordo com o nosso esquema.
        // Se algo estiver errado, ele joga o código direto para o 'catch' sem abrir o banco.
        const dadosValidados = cliqueSchema.parse(req.body);

        // Conecta ao cluster do MongoDB Atlas
        await client.connect();
        const db = client.db(dbName);
        const collection = db.collection('cliques_reais');

        // Documento construído APENAS com os dados que passaram no teste do Zod
        const dadosClique = {
            productName: dadosValidados.name,
            category: dadosValidados.category,
            targetUrl: dadosValidados.affiliateLink,
            isFeatured: dadosValidados.isFeatured,
            clickedAt: new Date() // Data e hora exata do clique real
        };

        // Salva direto no banco de dados na nuvem
        const resultado = await collection.insertOne(dadosClique);

        return res.status(201).json({ 
            success: true, 
            message: "Clique real registrado e validado no MongoDB Atlas!", 
            id: resultado.insertedId 
        });

    } catch (error) {
        // Se o erro foi causado por dados inválidos enviados pelo usuário/bot
        if (error instanceof z.ZodError) {
            return res.status(400).json({
                success: false,
                error: "Dados inválidos enviados para a API de métricas.",
                detalhes: error.errors.map(err => err.message)
            });
        }

        // Se for um erro de conexão com o banco ou do servidor
        return res.status(500).json({ success: false, error: error.message });
    } finally {
        // Garante que a conexão com o banco será fechada após salvar
        await client.close();
    }
});

// ==========================================
// ROTA GET: RELATÓRIO DE MÉTRICAS (MANTIDA IGUAL)
// ==========================================
router.get('/metricas', async (req, res) => {
    try {
        await client.connect();
        const db = client.db(dbName);
        const collection = db.collection('cliques_reais');

        // Pipeline de agregação para agrupar e contar os cliques por produto
        const relatorio = await collection.aggregate([
            {
                $group: {
                    _id: "$productName", // Agrupa pelo nome do produto
                    category: { $first: "$category" }, 
                    targetUrl: { $first: "$targetUrl" }, 
                    totalCliques: { $sum: 1 } // Soma 1 para cada clique registrado
                }
            },
            {
                $sort: { totalCliques: -1 } // Ordena do mais clicado para o menos clicado
            }
        ]).toArray();

        return res.status(200).json({ success: true, dados: relatorio });
    } catch (error) {
        return res.status(500).json({ success: false, error: error.message });
    } finally {
        await client.close();
    }
});

module.exports = router;