import os

def obter_dados_do_usuario():
    """Captura os dados do artigo direto pelo terminal do VS Code."""
    print("✏️ --- PAINEL DE CRIAÇÃO DE ARTIGOS (HUBIA) ---")
    
    titulo = input("Digite o TÍTULO do artigo: ").strip()
    # Gera um slug simples substituindo espaços por hífens e deixando em minúsculo
    slug = titulo.lower().replace(" ", "-").replace(":", "").replace("?", "")
    
    categoria = input("Digite a CATEGORIA (ex: Áudio, Hardware, Ebooks): ").strip()
    
    print("\n[DICA] Digite ou cole o texto do artigo. Pressione Enter em uma linha vazia para finalizar:")
    linhas_texto = []
    while True:
        linha = input()
        if linha == "":
            break
        linhas_texto.append(f"<p>{linha}</p>")
    
    conteudo_corpo = "\n        ".join(linhas_texto)
    
    # Links de Afiliados personalizados para este post
    print("\n🔗 --- CONFIGURAÇÃO DO FUNIL DUPLO ---")
    url_partnerstack = input("Link de Afiliado (PartnerStack/Ferramenta): ").strip()
    nome_ferramenta = input("Nome da ferramenta (ex: elevenlabs): ").strip()
    url_hotmart = input("Link de Checkout do E-book (Hotmart/Kiwify): ").strip()

    return {
        "titulo": titulo,
        "slug": slug,
        "categoria": categoria,
        "conteudo": conteudo_corpo,
        "url_afiliado": url_partnerstack,
        "nome_item": nome_ferramenta,
        "url_checkout": url_hotmart
    }

def construir_html_premium(post):
    """Gera o código HTML completo com o CSS Dark Mode e scripts do GA4 inclusos."""
    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post['titulo']} | HubIA</title>
    <style>
        :root {{
            --bg-dark: #0B0F19;
            --card-dark: #1E293B;
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            --accent-glow: #38BDF8;
            --accent-purple: #A855F7;
        }}
        body {{
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 40px 20px;
            line-height: 1.8;
        }}
        .container {{
            max-width: 720px;
            margin: 0 auto;
        }}
        h1 {{ font-size: 2.5rem; color: #FFF; margin-bottom: 5px; }}
        .meta-info {{ color: var(--text-muted); font-size: 0.95rem; margin-bottom: 40px; }}
        .content {{ font-size: 1.15rem; color: #E2E8F0; }}
        
        /* CTAs de Alta Conversão */
        .cta-container {{
            background: linear-gradient(135deg, #1E1B4B 0%, #311042 100%);
            border: 1px solid var(--accent-purple);
            padding: 30px;
            border-radius: 12px;
            margin: 40px 0;
            text-align: center;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.15);
        }}
        .cta-btn {{
            display: inline-block;
            background: var(--accent-glow);
            color: #000;
            font-weight: bold;
            padding: 14px 32px;
            border-radius: 6px;
            text-decoration: none;
            margin-top: 20px;
            font-size: 1rem;
            transition: transform 0.2s, filter 0.2s;
        }}
        .cta-btn:hover {{ 
            transform: scale(1.02);
            filter: brightness(1.1);
        }}
    </style>
</head>
<body>

    <article class="container">
        <h1>{post['titulo']}</h1>
        <div class="meta-info">
            <span>Categoria: <strong>{post['categoria']}</strong></span>
        </div>
        
        <div id="post-content" class="content">
            {post['conteudo']}
            
            <!-- FUNIL 1: CTA de Afiliado (Ferramenta) -->
            <div class="cta-container">
                <h3>Pronto para dominar essa tecnologia?</h3>
                <p>Crie sua conta na ferramenta agora mesmo e comece a aplicar o que aprendeu.</p>
                <a href="{post['url_afiliado']}" 
                   data-track="partnerstack" 
                   data-name="{post['nome_item']}" 
                   target="_blank" 
                   class="cta-btn">Testar {post['nome_item'].capitalize()} Agora</a>
            </div>

            <!-- FUNIL 2: Upsell de Infoproduto (E-book) -->
            <div class="cta-container" style="border-color: var(--accent-glow);">
                <h3>Quer acelerar seus resultados com IA?</h3>
                <p>Baixe nosso Guia Estratégico com mais de 500 prompts e templates prontos.</p>
                <a href="{post['url_checkout']}" 
                   data-track="hotmart" 
                   data-name="ebook-premium" 
                   target="_blank" 
                   class="cta-btn" 
                   style="background: var(--accent-purple); color: #fff;">Garantir E-book com Desconto</a>
            </div>
        </div>
    </article>

    <script>
        // Rastreamento inteligente acionado no clique dos CTAs
        document.getElementById('post-content').addEventListener('click', function(e) {{
            const link = e.target.closest('[data-track]');
            if (link) {{
                const tipo = link.getAttribute('data-track');
                const nome = link.getAttribute('data-name');
                
                // Dispara o evento para o seu GA4 se ele já estiver carregado globalmente
                if (typeof gtag !== 'undefined') {{
                    gtag('event', 'click_cta_blog', {{ 'cta_type': tipo, 'cta_name': nome }});
                }}
                
                // Envia para o seu back-end no Render em segundo plano
                if (navigator.sendBeacon) {{
                    const payload = JSON.stringify({{ tipo: tipo, item: nome, data: new Date() }});
                    navigator.sendBeacon('https://seu-backend-render.com', payload);
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    return html_template

def salvar_html(slug, html_content):
    """Cria a pasta e salva o arquivo HTML fisicamente."""
    pasta_destino = "blog"
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        
    caminho_arquivo = os.path.join(pasta_destino, f"{slug}.html")
    
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n🚀 [SUCESSO] Artigo gerado com sucesso!")
    print(f"📂 Arquivo criado em: {caminho_arquivo}")
    print(f"🔗 URL futura na Vercel: ://hubia.com{slug}.html")

# Fluxo de Execução
if __name__ == "__main__":
    dados = obter_dados_do_usuario()
    html_final = construir_html_premium(dados)
    salvar_html(dados['slug'], html_final)