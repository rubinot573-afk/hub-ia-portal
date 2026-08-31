const { z } = require('zod');

// Criamos o manual de regras com os campos exatos que você usa no corpo do POST
const cliqueSchema = z.object({
  name: z.string({
    required_error: "O nome do produto é obrigatório."
  }).min(2, "Nome do produto muito curto."),

  category: z.string({
    required_error: "A categoria é obrigatória."
  }).min(2, "Categoria inválida."),

  affiliateLink: z.string({
    required_error: "O link de afiliado é obrigatório."
  }).url("O link de afiliado precisa ser uma URL válida (https://...)."),

  isFeatured: z.boolean({
    invalid_type_error: "O campo isFeatured precisa ser verdadeiro ou falso (boolean)."
  }).default(false) // Se o front não mandar, ele assume falso automaticamente
});

module.exports = { cliqueSchema };