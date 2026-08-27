const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const mongoSanitize = require('express-mongo-sanitize');
require('dotenv').config();

const app = express();

app.use(cors({ origin: '*', methods: ['GET', 'POST'] }));
app.use(helmet({ contentSecurityPolicy: false, crossOriginResourcePolicy: false }));
app.use(express.json({ limit: '10kb' }));
app.use(mongoSanitize());

mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/portal-ia-banco')
  .then(() => console.log('✅ MongoDB sincronizado com sucesso!'))
  .catch(() => console.log('⚠️ Rodando API em modo offline local estável.'));

const toolRoutes = require('./routes/toolRoutes'); 
app.use('/api', toolRoutes);

app.get('/', (req, res) => res.send('API HubIA ativa.'));

const PORT = 5000;
app.listen(PORT, '0.0.0.0', () => console.log('🚀 Motor ativo na porta 5000'));