import os

def obter_dados_do_usuario():
    """Captura os dados do artigo direto pelo terminal do VS Code."""
    print("✏️ --- PAINEL DE CRIAÇÃO DE ARTIGOS (HUBIA) ---")
    
    titulo = input("Digite o TÍTULO do artigo: ").strip()
    # Gera um slug amigável limpando caracteres especiais comuns
    slug = titulo.lower().replace(" ", "-").replace(":", "").replace("?", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ã", "a").replace("ç", "c")
    
    categoria = input("Digite a CATEGORIA (ex: Produtividade (IA), Cursos & E-books, Eletrônicos & Hardware): ").strip()
    
    print("\n[DICA] Digite ou cole o texto do artigo. Pressione Enter em uma linha vazia para finalizar:")
    linhas_texto = []
    while True:
        linha = input()
        if linha == "":
            break
        linhas_texto.append(f"<p>{linha}</p>")
    
    conteudo_corpo = "\n        ".join(linhas_texto)
    
    print("\n🔗 --- CONFIGURAÇÃO DO FUNIL DUPLO ---")
    url_partnerstack = input("Link de Afiliado (PartnerStack/Amazon): ").strip()
    nome_ferramenta = input("Nome exato do item (ex: ElevenLabs): ").strip()
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
    """Gera o código HTML completo alinhado com a rota cliques.js do Render."""
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
                   data-track="true" 
                   data-name="{post['nome_item']}" 
                   data-category="{post['categoria']}" 
                   data-featured="false"
                   target="_blank" 
                   class="cta-btn">Testar {post['nome_item']} Agora</a>
            </div>

            <!-- FUNIL 2: Upsell de Infoproduto (E-book) -->
            <div class="cta-container" style="border-color: var(--accent-glow);">
                <h3>Quer acelerar seus resultados com IA?</h3>
                <p>Baixe nosso Guia Estratégico com mais de 500 prompts e templates prontos.</p>
                <a href="{post['url_checkout']}" 
                   data-track="true" 
                   data-name="Ebook - {post['nome_item']}" 
                   data-category="Cursos & E-books" 
                   data-featured="false"
                   target="_blank" 
                   class="cta-btn" 
                   style="background: var(--accent-purple); color: #fff;">Garantir E-book com Desconto</a>
            </div>
        </div>
    </article>

     <!-- SCRIPT DO MENSAGEIRO: ADAPTADO PARA O SEU CLIQUES.JS DO RENDER -->
    <script>
        document.getElementById('post-content').addEventListener('click', function(e) {{
            const link = e.target.closest('[data-track]');
            if (link) {{
                const name = link.getAttribute('data-name');
                const category = link.getAttribute('data-category');
                const affiliateLink = link.getAttribute('href');
                const isFeatured = link.getAttribute('data-featured') === 'true';
                
                if (typeof gtag !== 'undefined') {{
                    gtag('event', 'click_cta_blog', {{ 'product_name': name, 'category': category }});
                }}
                
                if (navigator.sendBeacon) {{
                    const headers = {{ type: 'application/json' }};
                    const payload = new Blob([JSON.stringify({{
                        name: name,
                        category: category,
                        affiliateLink: affiliateLink,
                        isFeatured: isFeatured
                    }})], headers);
                    
                    // Dispara nativamente para a rota registrada do seu back-end
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
    """Grava o arquivo físico do artigo dentro da subpasta blog."""
    pasta_destino = "blog"
    os.makedirs(pasta_destino, exist_ok=True)
        
    caminho_arquivo = os.path.join(pasta_destino, f"{slug}.html")
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n🚀 [SUCESSO] Artigo físico gerado: {caminho_arquivo}")
    return slug

def injetar_card_na_listagem(post):
    """Abre a listagem de cards do blog e insere o post novo no topo automaticamente."""
    caminho_index = os.path.join("blog", "index.html")
    if not os.path.exists(caminho_index):
        return

    with open(caminho_index, "r", encoding="utf-8") as f:
        conteudo_index = f.read()

    novo_card = f"""
            <!-- CARD AUTOMÁTICO: {post['titulo']} -->
            <a href="/blog/{post['slug']}" class="blog-card">
                <div>
                    <span class="category-badge">{post['categoria']}</span>
                    <h3>{post['titulo']}</h3>
                    <p>Aprenda o passo a passo definitivo para dominar essa solução e aplicar no seu ecossistema digital.</p>
                </div>
            </a>"""

    if novo_card not in conteudo_index:
        conteudo_index = conteudo_index.replace('<section class="blog-grid">', f'<section class="blog-grid">\n{novo_card}')
        with open(caminho_index, "w", encoding="utf-8") as f:
            f.write(conteudo_index)
        print(f"🎴 Card visual de '{post['titulo']}' injetado em blog/index.html!")

def gerar_sitemap_xml():
    """Varre as subpastas e atualiza o sitemap.xml para indexação imediata do Google."""
    print("🗺️ Reconstruindo sitemap.xml...")
    dom_base = "https://vercel.app"
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://sitemaps.org">\n'
    xml += f"  <url>\n    <loc>{dom_base}/</loc>\n    <priority>1.0</priority>\n  </url>\n"
    xml += f"  <url>\n    <loc>{dom_base}/blog</loc>\n    <priority>0.8</priority>\n  </url>\n"
    
    if os.path.exists("blog"):
        for arquivo in os.listdir("blog"):
            if arquivo.endswith(".html") and arquivo != "index.html":
                slug_limpo = arquivo.replace(".html", "")
                xml += f"  <url>\n    <loc>{dom_base}/blog/{slug_limpo}</loc>\n    <priority>0.6</priority>\n  </url>\n"
                
    xml += "</urlset>"
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)
    print("🚀 [SUCESSO] sitemap.xml atualizado na raiz do seu Frontend!")

# Fluxo de Execução Principal do Terminal
if __name__ == "__main__":
    # Garante a casca limpa da listagem de cards caso ela não exista
    caminho_listagem = os.path.join("blog", "index.html")
    os.makedirs("blog", exist_ok=True)
    
    if not os.path.exists(caminho_listagem):
        casca_limpa = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog & Tutoriais IA | HubIA</title>
    <style>
        :root { --bg-dark: #0B0F19; --card-dark: #1E293B; --text-main: #F8FAFC; --text-muted: #94A3B8; --accent-glow: #38BDF8; }
        body { background-color: var(--bg-dark); color: var(--text-main); font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 40px 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { font-size: 2.5rem; margin-bottom: 10px; color: #FFF; }
        p.subtitle { color: var(--text-muted); font-size: 1.1rem; margin-bottom: 40px; }
        .blog-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }
        .blog-card { background-color: var(--card-dark); border: 1px solid #334155; border-radius: 12px; padding: 25px; text-decoration: none; color: inherit; transition: transform 0.2s, border-color 0.2s; display: flex; flex-direction: column; justify-content: space-between; }
        .blog-card:hover { transform: translateY(-4px); border-color: var(--accent-glow); }
        .category-badge { background: rgba(56, 189, 248, 0.1); color: var(--accent-glow); padding: 4px 10px; border-radius: 50px; font-size: 0.8rem; font-weight: bold; align-self: flex-start; margin-bottom: 15px; }
        .blog-card h3 { margin: 0 0 10px 0; font-size: 1.3rem; color: #FFF; }
        .blog-card p { margin: 0; color: var(--text-muted); font-size: 0.95rem; line-height: 1.5; }
    </style>
</head>
<body>
    <main class="container">
        <h1>Central de Tutoriais HubIA</h1>
        <p class="subtitle">Aprenda a dominar ferramentas de IA e impulsione seus resultados orgânicos.</p>
        <section class="blog-grid">
            <!-- Os cards automáticos do Python serão injetados logo aqui embaixo -->
        </section>
    </main>
</body>
</html>"""
        with open(caminho_listagem, "w", encoding="utf-8") as f:
            f.write(casca_limpa)
        print("📁 Arquivo de índice blog/index.html gerado!")

    dados = obter_dados_do_usuario()
    html_final = construir_html_premium(dados)
    salvar_html(dados['slug'], html_final)
    injetar_card_na_listagem(dados)
    gerar_sitemap_xml()