const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const mongoSanitize = require('express-mongo-sanitize');
require('dotenv').config();

const app = express();

// ==========================================
// 1. CONFIGURAÇÃO DE INFRAESTRUTURA (RENDER)
// ==========================================
// O Render trabalha com proxies reversos. Sem essa linha, o Rate Limit vai
// enxergar o IP do próprio Render, bloqueando todos os usuários legítimos juntos.
app.set('trust proxy', 1);

// ==========================================
// 2. CONFIGURAÇÃO DE CORS RESTRITO
// ==========================================
// REMOVIDO: origin: '*' (Isso permitia que qualquer site roubasse dados da sua API).
// Correção: Permitir apenas o seu front-end hospedado na Vercel.
const corsOptions = {
  origin: 'https://frontendia-blush.vercel.app', // Substitua pela sua URL real da Vercel
  methods: ['GET', 'POST'],
  optionsSuccessStatus: 200
};
app.use(cors(corsOptions));

// ==========================================
// 3. SEGURANÇA DE CABEÇALHOS (HELMET)
// ==========================================
// Mantive as desativações de CSP e CORP que você definiu (úteis caso sua API sirva imagens externas),
// mas o Helmet continua removendo cabeçalhos que revelam que você usa Express e Node.js.
app.use(helmet({ 
  contentSecurityPolicy: false, 
  crossOriginResourcePolicy: false 
}));

// ==========================================
// 4. LIMITAÇÃO DE PAYLOAD E INPUTS
// ==========================================
// Perfeito! Protege contra ataques de negação de serviço (DoS) por envio de JSONs gigantes.
app.use(express.json({ limit: '10kb' }));

// Remove chaves maliciosas (como $ e .) enviadas no body ou query para evitar injeção NoSQL no Atlas.
app.use(mongoSanitize());

// ==========================================
// 5. MITIGAÇÃO DE ROBÔS E CLIQUES FALSOS
// ==========================================
// Cria um limitador de requisições para impedir cliques automatizados na sua API.
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // Janela de 15 minutos
  max: 100, // Limita cada IP real a no máximo 100 requisições por janela
  message: {
    status: 429,
    error: 'Muitos cliques ou requisições detectadas. Tente novamente em 15 minutos.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});
// Aplica o limitador estritamente nas rotas de ferramentas do HubIA
app.use('/api', apiLimiter);

// ==========================================
// 6. CONEXÃO COM O BANCO DE DADOS (MONGODB)
// ==========================================
mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/portal-ia-banco')
  .then(() => console.log('✅ MongoDB sincronizado com sucesso!'))
  .catch(() => console.log('⚠️ Rodando API em modo offline local estável.'));

// ==========================================
// 7. ROTAS DA APLICAÇÃO
// ==========================================
const toolRoutes = require('./routes/toolRoutes'); 
app.use('/api', toolRoutes);

app.get('/', (req, res) => res.send('API HubIA ativa.'));

// ==========================================
// 8. INICIALIZAÇÃO DO MOTOR
// ==========================================
// Mantive a porta 5000 e o bind '0.0.0.0' que é obrigatório para o Render escutar o tráfego externo.
const PORT = process.env.PORT || 5000;
app.listen(PORT, '0.0.0.0', () => console.log(`🚀 Motor ativo na porta ${PORT}`));