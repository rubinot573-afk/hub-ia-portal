const express = require('express');
const router = express.Router();
const Tool = require('../models/tool');

// Rota para listar todas as ferramentas
router.get('/tools', async (req, res) => {
    try {
        const { category } = req.query;
        let query = {};
        if (category) query.category = category;
        const tools = await Tool.find(query);
        res.status(200).json(tools);
    } catch (error) {
        res.status(500).json({ message: "Erro ao buscar ferramentas.", error });
    }
});

// Rota para cadastrar uma nova ferramenta
router.post('/admin/tools', async (req, res) => {
    try {
        const newTool = new Tool(req.body);
        const savedTool = await newTool.save();
        res.status(201).json(savedTool);
    } catch (error) {
        res.status(400).json({ message: "Erro ao cadastrar ferramenta.", error });
    }
});

module.exports = router;