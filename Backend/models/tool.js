const mongoose = require('mongoose');

const ToolSchema = new mongoose.Schema({
  name: { type: String, required: true, unique: true, trim: true },
  slug: { type: String, unique: true, lowercase: true, trim: true },
  description: { type: String, required: true },
  metaDescription: { type: String, maxLength: 160 },
  category: { type: String, required: true, index: true },
  affiliateLink: { type: String, required: true },
  logoUrl: { type: String, required: true },
  isFeatured: { type: Boolean, default: false },
  clicksCount: { type: Number, default: 0 }, // Métricas para o seu laboratório de marketing
  createdAt: { type: Date, default: Date.now }
});

// FUNÇÃO AUTOMÁTICA (Middleware do Mongoose)
// Antes de salvar no banco, transforma o nome da IA em uma URL amigável para SEO
ToolSchema.pre('save', function(next) {
  if (!this.isModified('name')) return next();
  
  this.slug = this.name
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')       // Substitui espaços por traços
    .replace(/[^\w\-]+/g, '')   // Remove caracteres especiais
    .replace(/\-\-+/g, '-');    // Remove traços duplicados
  next();
});

module.exports = mongoose.model('Tool', ToolSchema);