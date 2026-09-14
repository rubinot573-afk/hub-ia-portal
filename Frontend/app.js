// REPOSITÓRIO CENTRAL DIVERSIFICADO (Sincronizado por Abas e CTAs Inteligentes de Alta Conversão)
const bancoDeDadosIA = [
    {
        name: "ChatGPT 4o",
        description: "A IA de conversação líder de mercado. Ideal para otimizar redação publicitária, criar copys de vendas e acelerar o desenvolvimento de códigos.",
        category: "Produtividade (IA)",
        affiliateLink: "https://openai.com",
        logoUrl: "imagens/chatGPT.jpg",
        isFeatured: false,
        ctaText: "Testar Ferramenta ➔"
    },
    {
        name: "Midjourney v6",
        description: "Geração de artes digitais e imagens publicitárias ultra-realistas de altíssima fidelidade através de comandos simples de texto.",
        category: "Design (IA)",
        affiliateLink: "https://midjourney.com",
        logoUrl: "imagens/midjourney.jpg",
        isFeatured: false,
        ctaText: "Testar Ferramenta ➔"
    },
    {
        name: "O Guia Prático de Inteligência Artificial para Iniciantes",
        description: "Um guia prático para quem quer utilizar IA no dia a dia, mesmo sem experiência com tecnologia.",
        category: "Cursos & E-books",
        affiliateLink: "https://go.hotmart.com/O107562882J", 
        logoUrl: "", 
        isFeatured: true,
        ctaText: "Garantir Minha Vaga 🎓"
    },
    {
    name: "IA na Sua Rotina: 20h de Aplicação Prática",
    description: "Aprenda a usar ferramentas como ChatGPT, Gemini, Claude, SORA e FLUX para otimizar suas tarefas diárias e economizar tempo no dia a dia.",
    category: "Cursos & E-books",
    affiliateLink: "https://go.hotmart.com/C107368635C", 
    logoUrl: "", // Altere para o caminho da sua imagem da Hotmart se tiver
    isFeatured: true,
    ctaText: "Garantir Minha Vaga 🎓" // Mantendo seu sistema de CTA personalizado
},
    
    {
        name: "Microfone Condensador RGB com Braço Articulado",
        description: "[EQUIPAMENTO] Kit completo ideal para podcasts, streaming e gravação de vídeos de alta performance. Possui cancelamento de ruído inteligente, conexão USB plug-and-play e controle de eco integrado.",
        category: "Eletrônicos & Hardware",
        affiliateLink: "https://link.amazon/B0do2TKsA",
        logoUrl:"", 
        isFeatured: true,
        ctaText: "Ver Preço na Amazon 🛒"
    },

    {
  name: "Mouse Sem Fio Logitech M170",
  description: "Conexão sem fio 2.4GHz Plug-and-Play com alcance de até 10 metros. Design ambidestro confortável, rolagem linha por linha e bateria com duração de até 12 meses. Compatível com Windows, Mac e Linux.",
  category: "Eletrônicos & Hardware",
  affiliateLink: "https://link.amazon/B00OnuFcL",
  logoUrl:"",
  isFeatured: true,
  ctaText:"Ver preço na Amazon 🛒"
},
    {
        name: "Copy.ai",
        description: "Automação total de copywriting. Gera legendas persuasivas para Instagram, TikTok e e-mails de vendas em alta escala.",
        category: "Marketing (IA)",
        affiliateLink: "https://copy.ai",
        logoUrl: "imagens/copyai.jpg",
        isFeatured: false,
        ctaText: "Testar Ferramenta ➔"
    },
    {
        name: "ElevenLabs v2",
        description: "A clonagem de voz e conversão de texto em áudio mais perfeita do mercado. Excelente para vídeos virais de Reels e canais de nicho sem aparecer.",
        category: "Marketing (IA)",
        affiliateLink: "https://elevenlabs.io",
        logoUrl: "imagens/elevenlabs.jpg", 
        isFeatured: true,
        ctaText: "Testar Ferramenta ➔"
    }
];
// =========================================================================
// 1. RENDERIZADOR DE CARDS PREMIUM (MANTENDO ESTRUTURA ORIGINAL DE .MAP)
// =========================================================================
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

    // 1. Aplica a ordenação: true (1) fica em primeiro, false (0) fica em segundo
    const ferramentasOrdenadas = ferramentas.sort((a, b) => {
        return (b.isFeatured === true ? 1 : 0) - (a.isFeatured === true ? 1 : 0);
    });

    // 2. Alimenta o innerHTML usando o novo array ordenado
    grid.innerHTML = ferramentasOrdenadas.map(tool => {
        const seloDestaque = tool.isFeatured ? `<span style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #0b0f19; font-weight: 700; font-size: 0.7rem; padding: 0.25rem 0.6rem; border-radius: 6px; margin-left: auto; letter-spacing: 0.5px;">DESTAQUE</span>` : '';
        const textoBotao = tool.ctaText ? tool.ctaText : "Testar Ferramenta ➔";
        const temImagem = tool.logoUrl && tool.logoUrl.trim() !== "";

        return `
            <div class="tool-card" style="animation: fadeIn 0.35s cubic-bezier(0.4, 0, 0.2, 1) both;">
                <div class="tool-header ${temImagem ? '' : 'sem-logo'}" style="display: flex; align-items: center; gap: 1rem; width: 100%;">
                    ${temImagem ? `<img src="${tool.logoUrl}" alt="Logo ${tool.name}" class="tool-logo" width="55" height="55" style="object-fit: cover; border-radius: 8px; flex-shrink: 0;">` : ''}
                    <h3 style="margin: 0; font-size: 1.3rem; line-height: 1.4;">${tool.name}</h3>
                    ${seloDestaque}
                </div>
                <p class="tool-desc">${tool.description}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.4rem; border-top: 1px solid #1e293b; padding-top: 1rem;">
                    <span class="category-tag">${tool.category}</span>
                </div>
                <a href="${tool.affiliateLink}" target="_blank" rel="noopener sponsored" class="btn-affiliate" onclick="capturarConversao('${tool.name.replace(/'/g, "\\'")}', '${tool.category.replace(/'/g, "\\'")}', '${tool.affiliateLink.replace(/'/g, "\\'")}', ${Boolean(tool.isFeatured)})">${textoBotao}</a>
            </div>
        `;
    }).join('');
} // 👈 CHAVE CORRIGIDA AQUI! Fechando a função renderizarPlataforma antes de começar as outras.

// =========================================================================
// 2. FUNÇÃO DE RASTREAMENTO REAL (CHAMADA PELO ONCLICK DO LINK)
// =========================================================================
async function capturarConversao(nome, category = '', affiliateLink = '', isFeatured = false) {
    const nomeFormatado = String(nome || 'Clique');
    const categoriaFormatada = String(category || '');
    const linkFormatado = String(affiliateLink || '');

    let relatorio = JSON.parse(localStorage.getItem('hubia_analytics')) || {};
    relatorio[nomeFormatado] = (relatorio[nomeFormatado] || 0) + 1;
    localStorage.setItem('hubia_analytics', JSON.stringify(relatorio));
    console.log(`📊 [CONVERSÃO LOCAL] Clique para: ${nomeFormatado}`);

    try {
        await fetch('https://onrender.com', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: nomeFormatado,
                category: categoriaFormatada,
                affiliateLink: linkFormatado,
                isFeatured: !!isFeatured,
                action: 'click'
            })
        });
    } catch (error) {
        console.log('⚠️ Sincronização em segundo plano arquivada localmente.');
    }
}

// =========================================================================
// 3. FILTRAGEM POR CATEGORIA SINCRO (INTEGRADINHA E SEM QUEBRAS)
// =========================================================================
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

// 4. ENGENHARIA DE BUSCA DINÂMICA
function activarBusca() {
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
function initApp() {
    renderizarPlataforma(bancoDeDadosIA);
    verificarFiltros();
    activarBusca();
    gerenciarCookies();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}