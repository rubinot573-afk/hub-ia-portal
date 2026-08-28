const express = require('express');
const router = express.Router();
const { MongoClient } = require('mongodb');

// Pega a URL de conexão do MongoDB Atlas das variáveis de ambiente do Render
const url = process.env.MONGO_URI; 
const client = new MongoClient(url);
const dbName = 'HubIA_Metrics'; // Nome do banco que será criado automaticamente

router.post('/registrar', async (req, res) => {
    try {
        const { name, category, affiliateLink, isFeatured } = req.body;

        // Conecta ao cluster do MongoDB Atlas
        await client.connect();
        const db = client.db(dbName);
        const collection = db.collection('cliques_reais');

        // Documento com os dados exatos do clique que vieram do front-end
        const dadosClique = {
            productName: name,
            category: category,
            targetUrl: affiliateLink,
            isFeatured: isFeatured,
            clickedAt: new Date() // Data e hora exata do clique real
        };

        // Salva direto no banco de dados na nuvem
        const resultado = await collection.insertOne(dadosClique);

        res.status(201).json({ 
            success: true, 
            message: "Clique real registrado no MongoDB Atlas!", 
            id: resultado.insertedId 
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    } finally {
        // Garante que a conexão com o banco será fechada após salvar
        await client.close();
    }
});
// Adicione esta rota GET logo abaixo da sua rota POST e antes do module.exports

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
                    category: { $first: "$category" }, // Pega a categoria do primeiro que encontrar
                    targetUrl: { $first: "$targetUrl" }, // Pega o link de afiliado
                    totalCliques: { $sum: 1 } // Soma 1 para cada clique registrado
                }
            },
            {
                $sort: { totalCliques: -1 } // Ordena do mais clicado para o menos clicado
            }
        ]).toArray();

        res.status(200).json({ success: true, dados: relatorio });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    } finally {
        await client.close();
    }
});
module.exports = router;