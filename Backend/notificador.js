// backend/notificador.js
const twilio = require('twilio');

// Recomenda-se usar variáveis de ambiente no Render para esses dados
const accountSid = process.env.TWILIO_ACCOUNT_SID || 'SEU_ACCOUNT_SID_AQUI';
const authToken = process.env.TWILIO_AUTH_TOKEN || 'SEU_AUTH_TOKEN_AQUI';
const client = twilio(accountSid, authToken);

/**
 * Função para enviar alertas automáticos para o seu WhatsApp
 * @param {string} mensagem - O texto que será enviado
 */
async function enviarAlertaWhatsApp(mensagem) {
    try {
        const message = await client.messages.create({
            from: 'whatsapp:+14155238886', // Número de teste do Twilio
            to: 'whatsapp:+5532999999999',   // Seu número com DDD (ex: +5532...)
            body: mensagem
        });
        console.log(`[WhatsApp] Alerta enviado com sucesso. SID: ${message.sid}`);
    } catch (error) {
        console.error('[WhatsApp] Erro ao enviar notificação:', error.message);
    }
}

module.exports = { enviarAlertaWhatsApp };