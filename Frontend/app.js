// REPOSITÓRIO CENTRAL DIVERSIFICADO (Sincronizado por Abas e CTAs Inteligentes de Alta Conversão)
const bancoDeDadosIA = [
    {
        name: "ChatGPT 4o",
        description: "A IA de conversação líder de mercado. Ideal para otimizar redação publicitária, criar copys de vendas e acelerar o desenvolvimento de códigos.",
        category: "Produtividade (IA)",
        affiliateLink: "https://openai.com",
        logoUrl: "imagens/chatgpt.png",
        isFeatured: true,
        ctaText: "Testar Ferramenta ➔"
    },
    {
        name: "Midjourney v6",
        description: "Geração de artes digitais e imagens publicitárias ultra-realistas de altíssima fidelidade através de comandos simples de texto.",
        category: "Design (IA)",
        affiliateLink: "https://midjourney.com",
        logoUrl: "imagens/midjourney.png",
        isFeatured: false,
        ctaText: "Testar Ferramenta ➔"
    },
    {
        name: "Masterclass: Engenharia de Prompt",
        description: "Formação completa do básico ao avançado para dominar os comandos ocultos do ChatGPT e criar automações de marketing digital de alto nível.",
        category: "Cursos & E-books",
        affiliateLink: "https://hotmart.com", 
        logoUrl: "imagens/copyai.png", 
        isFeatured: true,
        ctaText: "Garantir Minha Vaga 🎓"
    },
    {
    name: "IA na Sua Rotina: 20h de Aplicação Prática",
    description: "Aprenda a usar ferramentas como ChatGPT, Gemini, Claude, SORA e FLUX para otimizar suas tarefas diárias e economizar tempo no dia a dia.",
    category: "Cursos & E-books",
    affiliateLink: "https://go.hotmart.com/C107368635C", 
    logoUrl: "imagens/hotmart.png", // Altere para o caminho da sua imagem da Hotmart se tiver
    isFeatured: false,
    ctaText: "Garantir Minha Vaga 🎓" // Mantendo seu sistema de CTA personalizado
},
    
    {
        name: "Microfone Condensador RGB com Braço Articulado",
        description: "[EQUIPAMENTO] Kit completo ideal para podcasts, streaming e gravação de vídeos de alta performance. Possui cancelamento de ruído inteligente, conexão USB plug-and-play e controle de eco integrado.",
        category: "Eletrônicos & Hardware",
        affiliateLink: "https://amzn.to", // URL de exemplo da Amazon
        logoUrl: "imagens/midjourney.png", 
        isFeatured: true,
        ctaText: "Ver Preço na Amazon 🛒"
    },
    {
        name: "Copy.ai",
        description: "Automação total de copywriting. Gera legendas persuasivas para Instagram, TikTok e e-mails de vendas em alta escala.",
        category: "Marketing (IA)",
        affiliateLink: "https://copy.ai",
        logoUrl: "imagens/copyai.png",
        isFeatured: false,
        ctaText: "Testar Ferramenta ➔"
    },
    {
        name: "ElevenLabs v2",
        description: "A clonagem de voz e conversão de texto em áudio mais perfeita do mercado. Excelente para vídeos virais de Reels e canais de nicho sem aparecer.",
        category: "Marketing (IA)",
        affiliateLink: "https://elevenlabs.io",
        logoUrl: "imagens/chatgpt.png", 
        isFeatured: true,
        ctaText: "Testar Ferramenta ➔"
    }
];
// 1. RENDERIZADOR DE CARDS PREMIUM (INTEGRADO COM RASTREAMENTO REAL)
function renderizarPlataforma(ferramentas) {
    const grid = document.getElementById('tools-grid');
    if (!grid) return;

    grid.innerHTML = "";

    if (ferramentas.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 4rem 1rem;">
                <p style="color: #64748b; font-size: 1.2rem; margin-bottom: 1rem;">Nenhum produto ou Inteligência Artificial encontrada...</p>
                <button onclick="document.getElementById('search-input').value=''; renderizarPlataforma(bancoDeDadosIA);" style="background: #111827; color: #6366f1; border: 1px solid #1e293b; padding: 0.6rem 1.4rem; border-radius: 20px; cursor: pointer; font-weight: 600;">Limpar Filtros</button>
            </div>`;
        return;
    }

      // Código original que gera os seus cards na tela
    ferramentas.forEach(produto => {
        const card = document.createElement('div');
        card.className = produto.isFeatured ? 'tool-card featured' : 'tool-card';
        
        card.innerHTML = `
            <img src="${produto.logoUrl || 'imagens/default.png'}" alt="${produto.name || 'Produto'}" class="tool-logo">
            <h3 class="tool-name">${produto.name || 'Sem nome'}</h3>
            <p class="tool-desc">${produto.description || 'Sem descrição'}</p>
            <button class="cta-btn">${produto.ctaText || 'Acessar ➔'}</button>
        `;

        const botaoCta = card.querySelector('.cta-btn');
        if (botaoCta) {
            botaoCta.addEventListener('click', async () => {
                try {
                    await registrarCliqueReal(produto);
                } catch (err) {
                    console.error("Falha ao registrar estatística, mas redirecionando usuário...", err);
                }
                
                if (produto.affiliateLink) {
                    window.open(produto.affiliateLink, '_blank');
                }
            });
        }

        // CORREÇÃO: Esta linha DEVE ficar antes de fechar o ferramentas.forEach
        grid.appendChild(card); 
    }); // Fecha o ferramentas.forEach
} // Fecha a função renderizarPlataforma

// 2. FUNÇÃO DE RASTREAMENTO REAL (CORRIGIDA COM A ROTA DA SUA API NO RENDER)
async function registrarCliqueReal(produto) {
    try {
        // ATENÇÃO: Substitua o 'seu-subdominio' pelo nome real do seu app no Render
        // Exemplo: https://onrender.com
        await fetch('https://hub-ia-portal-1.onrender.com/api/cliques/registrar', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: produto.name,
                category: produto.category,
                affiliateLink: produto.affiliateLink,
                isFeatured: produto.isFeatured
            })
        });
    } catch (error) {
        console.error("Erro no rastreamento do portfólio:", error);
        // Lança o erro para ser capturado pela trava de segurança do addEventListener
        throw error;
    }
}

    grid.innerHTML = ferramentas.map(tool => {
        const seloDestaque = tool.isFeatured ? `<span style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #0b0f19; font-weight: 700; font-size: 0.7rem; padding: 0.25rem 0.6rem; border-radius: 6px; margin-left: auto; letter-spacing: 0.5px;">DESTAQUE</span>` : '';
        const demandaVisual = (tool.name.length * 22) + 145; 
        const textoBotao = tool.ctaText ? tool.ctaText : "Testar Ferramenta ➔";

        return `
            <div class="tool-card" style="animation: fadeIn 0.35s cubic-bezier(0.4, 0, 0.2, 1) both;">
                <div class="tool-header">
                    <img src="${tool.logoUrl}" alt="Logo ${tool.name}" class="tool-logo" width="55" height="55" style="object-fit: cover;" onerror="this.src='https://placehold.co'">
                    <h3>${tool.name}</h3>
                    ${seloDestaque}
                </div>
                <p class="tool-desc">${tool.description}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.4rem; border-top: 1px solid #1e293b; padding-top: 1rem;">
                    <span class="category-tag">${tool.category}</span>
                    <span style="font-size: 0.8rem; color: #475569; font-weight: 500;">🔥 ${demandaVisual} Cliques</span>
                </div>
                <a href="${tool.affiliateLink}" target="_blank" rel="noopener sponsored" class="btn-affiliate" onclick="capturarConversao('${tool.name}')">${textoBotao}</a>
            </div>
        `;
    }).join('');


// 2. FILTRAGEM POR CATEGORIA SINCRO (Nome corrigido sem o "c")
function verificarFiltros() {
    const badges = document.querySelectorAll('.badge');
    badges.forEach(badge => {
        badge.addEventListener('click', () => {
            badges.forEach(b => b.classList.remove('active'));
            badge.classList.add('active');

            const input = document.getElementById('search-input');
            if (input) input.value = "";

            const categoria = badge.textContent.trim();
            if (categoria === "Todas") {
                renderizarPlataforma(bancoDeDadosIA);
            } else {
                const filtradas = bancoDeDadosIA.filter(t => t.category.toLowerCase() === categoria.toLowerCase());
                renderizarPlataforma(filtradas);
            }
        });
    });
}

// 3. ENGENHARIA DE BUSCA DINÂMICA
function ativarBusca() {
    const input = document.getElementById('search-input');
    if (!input) return;

    input.addEventListener('input', (e) => {
        const termo = e.target.value.toLowerCase().trim();
        const filtradas = bancoDeDadosIA.filter(t => 
            t.name.toLowerCase().includes(termo) || 
            t.description.toLowerCase().includes(termo)
        );
        
        if (termo !== "") {
            document.querySelectorAll('.badge').forEach(b => b.classList.remove('active'));
        } else {
            const badgeTodas = Array.from(document.querySelectorAll('.badge')).find(b => b.textContent.trim() === "Todas");
            if (badgeTodas) badgeTodas.classList.add('active');
        }
        renderizarPlataforma(filtradas);
    });
}

// 4. ANALYTICS DE CLIQUES (Métricas de CRO)
async function capturarConversao(nome) {
    let relatorio = JSON.parse(localStorage.getItem('hubia_analytics')) || {};
    relatorio[nome] = (relatorio[nome] || 0) + 1;
    localStorage.setItem('hubia_analytics', JSON.stringify(relatorio));
    console.log(`📊 [CONVERSÃO LOCAL] Clique para: ${nome}`);

    try {
        const API_URL = 'https://onrender.com';
        await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: nome, action: 'click' })
        });
    } catch (error) {
        console.log('⚠️ Sincronização em segundo plano arquivada localmente.');
    }
}

// 5. GERENCIADOR DE COOKIES E PREFERÊNCIAS (LGPD Avançado)
function gerenciarCookies() {
    const cookieBar = document.getElementById('cookie-bar');
    const cookieOptions = document.getElementById('cookie-options');
    const btnConfig = document.getElementById('btn-config-cookies');
    const btnAccept = document.getElementById('btn-cookies');
    const checkAnalytics = document.getElementById('check-analytics');

    if (!cookieBar || !btnAccept || !btnConfig || !cookieOptions) return;

    if (localStorage.getItem('hubia_cookies_aceito') === 'true') {
        cookieBar.style.display = 'none';
    }

    btnConfig.addEventListener('click', () => {
        if (cookieOptions.style.display === 'none') {
            cookieOptions.style.display = 'flex';
            btnConfig.textContent = '✖️ Fechar';
        } else {
            cookieOptions.style.display = 'none';
            btnConfig.textContent = '⚙️ Configurar';
        }
    });

    btnAccept.addEventListener('click', () => {
        localStorage.setItem('hubia_cookies_aceito', 'true');
        const aceitouAnalytics = checkAnalytics ? checkAnalytics.checked : true;
        localStorage.setItem('hubia_permitir_analytics', aceitouAnalytics);

        cookieBar.style.transition = 'all 0.3s ease';
        cookieBar.style.opacity = '0';
        setTimeout(() => cookieBar.style.display = 'none', 300);
    });
}

// INICIALIZAÇÃO DO ECOSSISTEMA (Sincronizado perfeitamente)
document.addEventListener("DOMContentLoaded", () => {
    renderizarPlataforma(bancoDeDadosIA);
    verificarFiltros();
    ativarBusca();
    gerenciarCookies();
});