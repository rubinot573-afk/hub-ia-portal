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

module.exports = router;