import os
import datetime
import json
import re
import unicodedata
from html import escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def obter_dados_do_usuario():
    """Captura os dados do artigo tratando automaticamente palavras-chave textuais simples."""
    print(" --- PAINEL DE CRIAÇÃO DE ARTIGOS (HUBIA) ---")
    
    titulo = input("Digite o TÍTULO do artigo: ").strip()
    
    # 1. Remove todos os acentos e cedilhas de forma mágica (transforma 'ç' em 'c', 'ã' em 'a', etc.)
    slug_limpo = unicodedata.normalize('NFKD', titulo).encode('ascii', 'ignore').decode('utf-8')
    
    # 2. Transforma em minúsculo e troca os espaços por hífens
    slug_limpo = slug_limpo.lower().replace(" ", "-")
    
    # 3. Remove QUALQUER caractere que não seja letra, número ou hífen (limpa de vez :, ?, !, @, etc.)
    slug = re.sub(r'[^a-z0-9-]+', '-', slug_limpo).strip('-')
    if not slug:
        slug = "artigo"
    categoria = input("Digite a CATEGORIA (ex: Produtividade (IA), Cursos & E-books): ").strip()
    descricao_seo = input("Digite uma descrição curta (1 frase para o LinkedIn/Google): ").strip()
    
    caminho_txt = os.path.join(BASE_DIR, "artigo.txt")
    print(f"\n Lendo o conteúdo de '{caminho_txt}'...")
    
    if not os.path.exists(caminho_txt):
        print(f" [ERRO] O arquivo '{caminho_txt}' não foi encontrado!")
        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write("Cole o texto aqui.")
            
    with open(caminho_txt, "r", encoding="utf-8") as f:
        conteudo_completo = f.read().strip()
    
    
    conteudo_normalizado = conteudo_completo
    for marcador in ["PRIMEIRA FERRAMENTA:", "SEGUNDA FERRAMENTA:", "TERCEIRA FERRAMENTA:", "PROMPT EXATO:", "Create a high-converting", "[Tone:", "Act as a"]:
        conteudo_normalizado = conteudo_normalizado.replace(marcador, f"\n\n{marcador}")

    paragrafos = [p.strip() for p in conteudo_normalizado.split('\n') if p.strip()]
    
    linhas_texto = []
    for p in paragrafos:
        # Formatação inteligente para os blocos de comando em inglês
        if p.startswith('"') or p.startswith('"[Tone:') or p.startswith('Create a') or p.startswith('Act as a'):
            prompt_limpo = p.strip('"')
            linhas_texto.append(f'<pre><code>{escape(prompt_limpo, quote=False)}</code></pre>')
        # Formatação inteligente para os títulos textuais
        elif p.startswith('PRIMEIRA') or p.startswith('SEGUNDA') or p.startswith('TERCEIRA') or p.startswith('PROMPT'):
            linhas_texto.append(f'<h3>{escape(p)}</h3>')
        else:
            linhas_texto.append(f'<p>{escape(p)}</p>')
            
    conteudo_corpo = "\n        ".join(linhas_texto)
    
    print("\n🔗 --- CONFIGURAÇÃO DE AFILIAÇÃO (Opcionais: Pressione ENTER para pular) ---")
    url_partnerstack = input("Link de Afiliado (PartnerStack/Amazon) [ENTER para pular]: ").strip()
    
    nome_ferramenta = ""
    if url_partnerstack:
        nome_ferramenta = input("Nome exato do item (ex: ElevenLabs): ").strip()
        
    url_hotmart = input("Link de Checkout do E-book (Hotmart/Kiwify) [ENTER para pular]: ").strip()

    return {
        "titulo": titulo,
        "slug": slug,
        "categoria": categoria,
        "descricao": descricao_seo,
        "conteudo": conteudo_corpo,
        "url_afiliado": url_partnerstack,
        "nome_item": nome_ferramenta,
        "url_checkout": url_hotmart
    }

def construir_html_premium(post):
    """Gera o código HTML com suporte a blocos de código e Meta Tags do LinkedIn."""
    data_atual = datetime.date.today().strftime("%d/%m/%Y")
    dom_base = "https://frontendia-blush.vercel.app"
    url_completa_post = f"{dom_base}/blog/{post['slug']}"

    titulo = escape(post['titulo'])
    categoria = escape(post['categoria'])
    descricao = escape(post['descricao'], quote=True)
    url_afiliado = escape(post['url_afiliado'], quote=True)
    nome_item = escape(post['nome_item'])
    url_checkout = escape(post['url_checkout'], quote=True)
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["titulo"],
        "description": post["descricao"],
        "datePublished": datetime.date.today().isoformat(),
        "url": url_completa_post,
        "author": {"@type": "Person", "name": "Rafael"},
        "publisher": {"@type": "Organization", "name": "HubIA",
                      "logo": {"@type": "ImageObject", "url": f"{dom_base}/assets/logo.png"}}
    }, ensure_ascii=False)

    cta_afiliado_html = ""
    if post['url_afiliado'] and post['nome_item']:
        cta_afiliado_html = f"""
            <div class="cta-container">
                <h3>Pronto para dominar essa tecnologia?</h3>
                <p>Crie sua conta na ferramenta agora mesmo e comece a aplicar o que aprendeu.</p>
                <a href="{url_afiliado}" data-track="true" data-name="{nome_item}" data-category="{categoria}" data-featured="false" target="_blank" rel="noopener noreferrer" class="cta-btn">Conferir {nome_item} Agora</a>
            </div>
        """

    cta_checkout_html = ""
    if post['url_checkout']:
        nome_rastreio = post['nome_item'] if post['nome_item'] else "Guia HubIA"
        cta_checkout_html = f"""
            <div class="cta-container" style="border-color: var(--accent-glow);">
                <h3>Quer acelerar seus resultados com IA?</h3>
                <p>Baixe nosso Guia Estratégico com mais de 500 prompts e templates prontos.</p>
                <a href="{url_checkout}" data-track="true" data-name="Ebook - {nome_rastreio}" data-category="Cursos &amp; E-books" data-featured="false" target="_blank" rel="noopener noreferrer" class="cta-btn" style="background: var(--accent-purple); color: #fff;">Garantir E-book com Desconto</a>
            </div>
        """

    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo} | HubIA</title>
    <meta name="description" content="{descricao}">

    <!-- META TAGS DE COMPARTILHAMENTO (LINKEDIN / OPEN GRAPH) -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url_completa_post}">
    <meta property="og:title" content="{titulo} | HubIA">
    <meta property="og:description" content="{descricao}">
    <meta property="og:image" content="{dom_base}/assets/og-image-default.jpg">

    <!--  SCHEMA MARKUP INJETADO VIA PYTHON (Google lê isso instantaneamente) -->
    <script type="application/ld+json">
    {schema}
    </script>

    <style>
        :root {{
            --bg-dark: #0B0F19;
            --card-dark: #1E293B;
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            --accent-glow: #38BDF8;
            --accent-purple: #A855F7;
        }}
        body {{ background-color: var(--bg-dark); color: var(--text-main); font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 40px 20px; line-height: 1.8; }}
        .container {{ max-width: 720px; margin: 0 auto; }}
        h1 {{ font-size: 2rem; color: #FFF; margin-bottom: 5px; line-height: 1.3; }}
        @media (max-width: 480px) {{ h1 {{ font-size: 1.5rem; }} }}
        .meta-info {{ color: var(--text-muted); font-size: 0.95rem; margin-bottom: 40px; }}
        .content {{ font-size: 1.15rem; color: #E2E8F0; }}
        
        pre {{
            background-color: #1E293B;
            border-left: 4px solid var(--accent-glow);
            padding: 18px;
            border-radius: 8px;
            overflow-x: auto;
            white-space: pre-wrap;
            font-family: monospace;
            color: #38BDF8;
            font-size: 0.95rem;
            margin: 20px 0;
            line-height: 1.5;
        }}
        h3 {{
            color: #FFF;
            margin-top: 35px;
            font-size: 1.35rem;
        }}
        
        .cta-container {{ background: linear-gradient(135deg, #1E1B4B 0%, #311042 100%); border: 1px solid var(--accent-purple); padding: 30px; border-radius: 12px; margin: 40px 0; text-align: center; box-shadow: 0 0 20px rgba(168, 85, 247, 0.15); }}
        .cta-btn {{ display: inline-block; background: var(--accent-glow); color: #000; font-weight: bold; padding: 14px 32px; border-radius: 6px; text-decoration: none; margin-top: 20px; font-size: 1rem; transition: transform 0.2s, filter 0.2s; }}
        .cta-btn:hover {{ transform: scale(1.02); filter: brightness(1.1); }}
    </style>
</head>
<body>

    <article class="container">
        <h1>{titulo}</h1>
        <div class="meta-info">
            <span>Categoria: <strong>{categoria}</strong></span> | <span>Publicado em: {data_atual}</span>
        </div>
        
        <div id="post-content" class="content">
            {post['conteudo']}
            
            {cta_afiliado_html}
            {cta_checkout_html}
        </div>
    </article>

    <script>
        document.getElementById('post-content').addEventListener('click', function(e) {{
            const link = e.target.closest('[data-track]');
            if (link) {{
                const name = link.getAttribute('data-name');
                const category = link.getAttribute('data-category');
                const affiliateLink = link.getAttribute('href');
                const isFeatured = link.getAttribute('data-featured') === 'true';
                
                if (!affiliateLink || affiliateLink === "#" || affiliateLink.trim() === "") return;

                if (typeof gtag !== 'undefined') {{
                    gtag('event', 'click_cta_blog', {{ 'product_name': name, 'category': category }});
                }}
                
                if (navigator.sendBeacon) {{
                    const headers = {{ type: 'application/json' }};
                    const payload = new Blob([JSON.stringify({{ name: name, category: category, affiliateLink: affiliateLink, isFeatured: isFeatured }})], headers);
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
    pasta_destino = os.path.join(BASE_DIR, "blog")
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_destino, f"{slug}.html")
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"🚀 [SUCESSO] Artigo físico gerado: {caminho_arquivo}")
    return slug

def injetar_card_na_listagem(post):
    caminho_index = os.path.join(BASE_DIR, "blog", "index.html")
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
                    <p>{post['descricao']}</p>
                </div>
            </a>"""

    if novo_card not in conteudo_index:
        conteudo_index = conteudo_index.replace('<section class="blog-grid">', f'<section class="blog-grid">\n{novo_card}')
        with open(caminho_index, "w", encoding="utf-8") as f:
            f.write(conteudo_index)
        print(f"🎴 Card visual injetado em blog/index.html!")


def gerar_sitemap_xml():
    """Varre as subpastas e atualiza o sitemap.xml para indexação imediata do Google."""
    print("🗺️ Reconstruindo sitemap.xml...")
    # Correção 1: Inserção do domínio real completo do HubIA
    dom_base = "https://frontendia-blush.vercel.app"
    
    # Correção 2: Adicionada a declaração correta de namespace (xmlns) exigida pelo Google
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # URL da Home
    xml += f"  <url>\n    <loc>{dom_base}/</loc>\n    <priority>1.0</priority>\n  </url>\n"
    # URL da Listagem do Blog
    xml += f"  <url>\n    <loc>{dom_base}/blog</loc>\n    <priority>0.8</priority>\n  </url>\n"
    
    # Varre a pasta blog e adiciona dinamicamente TODOS os posts que existirem lá dentro
    blog_dir = os.path.join(BASE_DIR, "blog")
    if os.path.exists(blog_dir):
        for arquivo in os.listdir(blog_dir):
            if arquivo.endswith(".html") and arquivo != "index.html":
                slug_limpo = arquivo.replace(".html", "")
                xml += f"  <url>\n    <loc>{dom_base}/blog/{slug_limpo}</loc>\n    <priority>0.6</priority>\n  </url>\n"
                
    xml += "</urlset>"
    with open(os.path.join(BASE_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("🚀 [SUCESSO] sitemap.xml atualizado na raiz do seu Frontend com Namespace correto!")


if __name__ == "__main__":
    dados = obter_dados_do_usuario()
    html_final = construir_html_premium(dados)
    salvar_html(dados['slug'], html_final)
    injetar_card_na_listagem(dados)
    gerar_sitemap_xml()