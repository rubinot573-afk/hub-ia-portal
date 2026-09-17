#!/usr/bin/env python3
"""
Nome do Script: post_ia_lucrativa.py
Descrição: Automação CLI unificada com a mesma engenharia de String do seu blog.
           Varre ambas as pastas (/blog e /ia-lucrativa) para gerar o sitemap.xml
           perfeito e sem conflitos de namespace.
Autor: Engenheiro de Software Sênior
"""

import os
import sys
import re
from datetime import datetime

# --- CONFIGURAÇÕES GERAIS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://frontendia-blush.vercel.app"
TXT_SOURCE = "lucrativa.txt"
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap.xml")
HOME_FILE = os.path.join(BASE_DIR, "index.html")
HUB_DIR = "ia-lucrativa"
HUB_FILE = os.path.join(BASE_DIR, HUB_DIR, "index.html")


def log_info(msg: str):
    print(f"[\033[94mINFO\033[0m] {msg}")

def log_success(msg: str):
    print(f"[\033[92mSUCESSO\033[0m] {msg}")

def log_error(msg: str):
    print(f"[\033[91mERRO CRÍTICO\033[0m] {msg}", file=sys.stderr)


def format_text_to_paragraphs(text: str) -> str:
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    html_elements = []
    current_para = []
    
    for line in lines:
        if line.startswith("##"):
            if current_para:
                html_elements.append(f"<p>{' '.join(current_para)}</p>")
                current_para = []
            clean_title = line.replace("##", "").strip()
            html_elements.append(f"<h2>{clean_title}</h2>")
        else:
            current_para.append(line)
            if len(current_para) == 3:
                html_elements.append(f"<p>{' '.join(current_para)}</p>")
                current_para = []
                
    if current_para:
        html_elements.append(f"<p>{' '.join(current_para)}</p>")
        
    return "\n        ".join(html_elements)


def generate_html_content(slug: str, title: str, headline: str, checkout_url: str, paragraphs_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{headline}">
    <style>
        :root {{
            --bg-color: #0d1117;
            --text-color: #c9d1d9;
            --accent-color: #00ff66;
            --accent-glow: rgba(0, 255, 102, 0.4);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
            display: flex;
            justify-content: center;
        }}
        main {{ max-width: 480px; width: 100%; padding-bottom: 60px; }}
        header {{ text-align: center; margin-bottom: 30px; }}
        h1 {{ font-size: 1.8rem; color: #fff; margin-bottom: 15px; line-height: 1.3; }}
        h2 {{ font-size: 1.3rem; color: #fff; margin-top: 35px; margin-bottom: 15px; border-bottom: 1px solid #21262d; padding-bottom: 8px; }}
        .headline {{ font-size: 1.1rem; color: var(--accent-color); font-weight: 500; margin-bottom: 20px; }}
        .capa-container {{ text-align: center; margin-bottom: 30px; }}
        .capa {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }}
        .content {{ font-size: 1rem; margin-bottom: 40px; }}
        .content p {{ margin-bottom: 20px; text-align: left; color: #e6edf3; }}
        .btn-container {{ position: sticky; bottom: 20px; width: 100%; text-align: center; z-index: 100; }}
        .btn-checkout {{
            display: block;
            padding: 16px 24px;
            background: var(--bg-color);
            color: var(--accent-color);
            text-decoration: none;
            font-weight: bold;
            font-size: 1.2rem;
            border: 2px solid var(--accent-color);
            border-radius: 50px;
            box-shadow: 0 0 15px var(--accent-glow);
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .faq {{ margin-top: 50px; border-top: 1px solid #21262d; padding-top: 30px; }}
        .faq h2 {{ font-size: 1.4rem; color: #fff; margin-bottom: 20px; text-align: center; border: none; padding: 0; }}
        .faq-item {{ margin-bottom: 20px; background: #161b22; padding: 15px; border-radius: 6px; }}
        .faq-item h3 {{ font-size: 1rem; color: #fff; margin-bottom: 8px; }}
        .faq-item p {{ font-size: 0.9rem; color: #8b949e; }}
    </style>
</head>
<body>
    <main>
        <header>
            <h1>{title}</h1>
            <p class="headline">“{headline}”</p>
        </header>

        <section class="capa-container">
            <img src="/img/{slug}.png" alt="Capa do e-book {title}" class="capa" loading="eager">
        </section>

        <section class="content">
            {paragraphs_html}
        </section>

        <div class="btn-container">
            <a href="{checkout_url}" class="btn-checkout" target="_blank" rel="noopener noreferrer">Garantir Acesso Imediato</a>
        </div>

        <section class="faq">
            <h2>Dúvidas Frequentes (FAQ)</h2>
            <div class="faq-item">
                <h3>Como recebo o conteúdo?</h3>
                <p>Imediatamente após a aprovação do pagamento, você receberá os dados de acesso direto no seu e-mail.</p>
            </div>
            <div class="faq-item">
                <h3>O formato é amigável para leitura?</h3>
                <p>Sim, o e-book foi totalmente diagramado e otimizado para leitura confortável em smartphones, tablets e computadores.</p>
            </div>
            <div class="faq-item">
                <h3>Possui garantia?</h3>
                <p>Sim, você tem garantia incondicional de 7 dias assegurada pela Hotmart.</p>
            </div>
        </section>
    </main>
</body>
</html>
"""


def reconstruir_sitemap_completo():
    """Gera o sitemap.xml do zero, lendo o Blog E a pasta IA Lucrativa juntos (Sem conflito)."""
    print("🗺️ Reconstruindo sitemap.xml com Engenharia Unificada...")
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # URLs Base Estáticas
    xml += f"  <url>\n    <loc>{BASE_URL}/</loc>\n    <priority>1.0</priority>\n  </url>\n"
    xml += f"  <url>\n    <loc>{BASE_URL}/blog</loc>\n    <priority>0.8</priority>\n  </url>\n"
    xml += f"  <url>\n    <loc>{BASE_URL}/{HUB_DIR}</loc>\n    <priority>0.8</priority>\n  </url>\n"
    
    # 1. Varre e adiciona posts do Blog
    blog_dir = os.path.join(BASE_DIR, "blog")
    if os.path.exists(blog_dir):
        for arquivo in os.listdir(blog_dir):
            if arquivo.endswith(".html") and arquivo != "index.html":
                slug_limpo = arquivo.replace(".html", "")
                xml += f"  <url>\n    <loc>{BASE_URL}/blog/{slug_limpo}</loc>\n    <priority>0.6</priority>\n  </url>\n"

    # 2. Varre e adiciona e-books da IA Lucrativa
    ia_dir = os.path.join(BASE_DIR, HUB_DIR)
    if os.path.exists(ia_dir):
        for arquivo in os.listdir(ia_dir):
            if arquivo.endswith(".html") and arquivo != "index.html":
                slug_limpo = arquivo.replace(".html", "")
                xml += f"  <url>\n    <loc>{BASE_URL}/{HUB_DIR}/{slug_limpo}</loc>\n    <priority>0.6</priority>\n  </url>\n"
                
    xml += "</urlset>"
    
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(xml)
    log_success("Sitemap.xml reconstruído e unificado com sucesso total!")


def update_main_home_nav(home_path: str, hub_slug: str):
    if not os.path.exists(home_path):
        return
    with open(home_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- INJECT_PRODUCT_BUTTONS_START -->"
    end_tag = "<!-- INJECT_PRODUCT_BUTTONS_END -->"

    if start_tag not in content or end_tag not in content:
        return

    if f"href='/{hub_slug}'" in content or f'href="/{hub_slug}"' in content or f"/{hub_slug}/" in content:
        return

        hub_button_html = f"""
            <a href="/{hub_slug}" style="background: linear-gradient(135deg, rgba(0, 255, 102, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%); color: #00ff66; font-weight: 600; text-decoration: none; font-size: 0.95rem; padding: 6px 14px; margin-right: 8px; border-radius: 6px; border: 1px solid rgba(0, 255, 102, 0.2); transition: all 0.2s;" onmouseover="this.style.color='#FFF'; this.style.borderColor='#A855F7';" onmouseout="this.style.color='#00ff66'; this.style.borderColor='rgba(0, 255, 102, 0.2)';">
                🚀 IA Lucrativa
            </a>"""

    pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
    updated_content = re.sub(
        pattern,
        lambda match: f"{start_tag}{match.group(1)}{hub_button_html}\n{end_tag}",
        content,
        count=1,
        flags=re.DOTALL,
    )

    with open(home_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    log_success("Botão da barra de navegação principal configurado.")


def update_hub_showcase(hub_path: str, book_slug: str, title: str, headline: str):
    if not os.path.exists(hub_path):
        return

    with open(hub_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- INJECT_PRODUCT_BUTTONS_START -->"
    end_tag = "<!-- INJECT_PRODUCT_BUTTONS_END -->"

    if start_tag not in content or end_tag not in content:
        return

    if f"{book_slug}.html" in content:
        return

    new_card_html = f"""
            <!-- CARD AUTOMÁTICO: {title} -->
            <a href="/{HUB_DIR}/{book_slug}.html" class="blog-card">
                <div>
                    <span class="category-badge">E-book (IA)</span>
                    <h3>{title}</h3>
                    <p>{headline}</p>
                </div>
            </a>"""

    pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
    updated_content = re.sub(
        pattern,
        lambda match: f"{start_tag}{match.group(1)}{new_card_html}\n{end_tag}",
        content,
        count=1,
        flags=re.DOTALL,
    )

    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    log_success("Card do e-book criado com sucesso na vitrine!")


def main():
    print("\n🚀 \033[1;95mGERENCIADOR DE ECOSSISTEMA UNIFICADO\033[0m 🚀\n")

    caminho_txt = os.path.join(BASE_DIR, TXT_SOURCE)
    if not os.path.exists(caminho_txt):
        log_error(f"Arquivo '{caminho_txt}' não encontrado.")
        sys.exit(1)

    with open(caminho_txt, "r", encoding="utf-8") as f:
        raw_text = f.read()

    book_slug = input("👉 Digite o SLUG DO E-BOOK (ex: menos-teoria-mais-sistema): ").strip().lower()
    book_slug = re.sub(r"[^a-z0-9-]", "", book_slug)
    if not book_slug:
        sys.exit(1)

    title = input("👉 Digite o TÍTULO COMPLETO do e-book: ").strip()
    headline = input("👉 Digite a FRASE DE EFEITO (Headline): ").strip()
    checkout_url = input("👉 Digite o LINK DE CHECKOUT da Hotmart: ").strip()
    target_html = os.path.join(BASE_DIR, HUB_DIR, f"{book_slug}.html")

    try:
        paragraphs_html = format_text_to_paragraphs(raw_text)
        final_html = generate_html_content(
            book_slug, title, headline, checkout_url, paragraphs_html
        )
        update_main_home_nav(HOME_FILE, HUB_DIR)
        update_hub_showcase(HUB_FILE, book_slug, title, headline)

        os.makedirs(os.path.join(BASE_DIR, HUB_DIR), exist_ok=True)
        with open(target_html, "w", encoding="utf-8") as f:
            f.write(final_html)

        reconstruir_sitemap_completo()
        log_success(
            f"Lançamento concluído com sucesso total! Arquivo: /{HUB_DIR}/{book_slug}.html"
        )
    except Exception as e:
        log_error(f"Erro ao processar: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()