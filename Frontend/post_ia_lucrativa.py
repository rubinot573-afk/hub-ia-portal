#!/usr/bin/env python3
"""
Nome do Script: post_ia_lucrativa.py
Descrição: Automação CLI que espelha exatamente a arquitetura da sua pasta /blog/.
           Gera arquivos .html soltos diretamente dentro do diretório /ia-lucrativa/.
Autor: Engenheiro de Software Sênior
"""

import os
import sys
import re
from datetime import datetime
import xml.etree.ElementTree as ET

# --- CONFIGURAÇÕES GERAIS ---
BASE_URL = "https://frontendia-blush.vercel.app"  # Substitua pelo seu domínio de produção
TXT_SOURCE = "lucrativa.txt"
SITEMAP_FILE = "sitemap.xml"
HOME_FILE = "index.html"  # Home principal da raiz
HUB_DIR = "ia-lucrativa"   # Pasta central dos Infoprodutos
HUB_FILE = os.path.join(HUB_DIR, "index.html") # Vitrine da aba


def log_info(msg: str):
    print(f"[\033[94mINFO\033[0m] {msg}")

def log_success(msg: str):
    print(f"[\033[92mSUCESSO\033[0m] {msg}")

def log_error(msg: str):
    print(f"[\033[91mERRO CRÍTICO\033[0m] {msg}", file=sys.stderr)


def format_text_to_paragraphs(text: str) -> str:
    """Processa o texto bruto do TXT convertendo '##' em <h2> e gerando parágrafos curtos."""
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
    """Retorna o HTML mobile-first limpo com botão neon para a página do e-book."""
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


def update_sitemap(sitemap_path: str, new_url: str):
    """Atualiza o sitemap.xml."""
    if not os.path.exists(sitemap_path):
        raise FileNotFoundError(f"Sitemap não encontrado em: {sitemap_path}")

    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns_uri = root.tag[1:].split("}")[0] if root.tag.startswith("{") else ""
    loc_path = f".//{{{ns_uri}}}loc" if ns_uri else ".//loc"
    url_path = f"{{{ns_uri}}}url" if ns_uri else "url"

    for loc in root.findall(loc_path):
        if loc.text and loc.text.strip() == new_url:
            return

    url_element = ET.Element(url_path)
    ET.SubElement(url_element, f"{{{ns_uri}}}loc" if ns_uri else "loc").text = new_url
    ET.SubElement(url_element, f"{{{ns_uri}}}lastmod" if ns_uri else "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(url_element, f"{{{ns_uri}}}priority" if ns_uri else "priority").text = "0.8"
    root.append(url_element)
    ET.indent(tree, space="  ", level=0)
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
    log_success("Sitemap.xml atualizado.")


def update_main_home_nav(home_path: str, hub_slug: str):
    """Garante que o botão do menu principal aponte estático para a aba /ia-lucrativa/."""
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
            <a href="/{hub_slug}" style="background: linear-gradient(135deg, rgba(0, 255, 102, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%); color: #00ff66; font-weight: 600; text-decoration: none; font-size: 0.95rem; padding: 6px 14px; border-radius: 6px; border: 1px solid rgba(0, 255, 102, 0.2); transition: all 0.2s;" onmouseover="this.style.color='#FFF'; this.style.borderColor='#A855F7';" onmouseout="this.style.color='#00ff66'; this.style.borderColor='rgba(0, 255, 102, 0.2)';" style="margin-right: 8px;">
                🚀 IA Lucrativa
            </a>"""

    pattern = f"{start_tag}(.*?){end_tag}"
    replacement = f"{start_tag}\\1{hub_button_html}\n{end_tag}"
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(home_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    log_success("Botão da aba central 'IA Lucrativa' verificado no menu principal.")


def update_hub_showcase(hub_path: str, book_slug: str, title: str):
    """Injeta o link do novo e-book (.html) dentro da página vitrine da aba /ia-lucrativa/index.html."""
    if not os.path.exists(hub_path):
        log_info(f"Página de vitrine do hub ({hub_path}) não encontrada. Pulei listagem interna.")
        return

    with open(hub_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- INJECT_PRODUCT_BUTTONS_START -->"
    end_tag = "<!-- INJECT_PRODUCT_BUTTONS_END -->"

    if start_tag not in content or end_tag not in content:
        log_error(f"Tags de ancoragem não encontradas em {hub_path} para listar o e-book.")
        return

    if f"{book_slug}.html" in content:
        log_info(f"O e-book {book_slug}.html já está listado na vitrine do Hub.")
        return

    # IMPORTANTE: Agora aponta para o arquivo .html solto na pasta, igual ao blog!
    new_book_link = f"""
        <div class="book-card" style="margin-bottom: 15px; padding: 15px; background: #161b22; border-radius: 8px; border: 1px solid #21262d;">
            <h3 style="color: #fff; margin-bottom: 5px;">{title}</h3>
            <a href="/{HUB_DIR}/{book_slug}.html" style="color: #00ff66; font-weight: 600; text-decoration: none; font-size: 0.9rem;">Ver detalhes do e-book →</a>
        </div>
    """

    pattern = f"{start_tag}(.*?){end_tag}"
    replacement = f"{start_tag}\1{new_book_link}\n{end_tag}"
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    log_success(f"E-book '{title}' listado na vitrine do seu Hub como {book_slug}.html")


def main():
    print("\n🚀 \033[1;95mGERENCIADOR DE ECOSSISTEMA - ESTILO BLOG\033[0m 🚀\n")

    if not os.path.exists(TXT_SOURCE):
        log_error(f"Arquivo '{TXT_SOURCE}' não encontrado.")
        sys.exit(1)

    with open(TXT_SOURCE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    book_slug = input("👉 Digite o SLUG DO E-BOOK (ex: menos-teoria-mais-sistema): ").strip().lower()
    book_slug = re.sub(r'[^a-z0-9-]', '', book_slug)
    if not book_slug:
        log_error("Slug inválido.")
        sys.exit(1)

    title = input("👉 Digite o TÍTULO COMPLETO do e-book: ").strip()
    headline = input("👉 Digite a FRASE DE EFEITO (Headline): ").strip()
    checkout_url = input("👉 Digite o LINK DE CHECKOUT da Hotmart: ").strip()

    if not all([title, headline, checkout_url]):
        log_error("Todos os campos são obrigatórios.")
        sys.exit(1)

    # NOVO DESTINO: Gera ia-lucrativa/menos-teoria-mais-sistema.html (Estilo o seu Blog!)
    target_html = os.path.join(os.getcwd(), HUB_DIR, f"{book_slug}.html")
    new_page_url = f"{BASE_URL}/{HUB_DIR}/{book_slug}.html"

    try:
        paragraphs_html = format_text_to_paragraphs(raw_text)
        final_html = generate_html_content(book_slug, title, headline, checkout_url, paragraphs_html)

        # 1. Ajusta Navegação Inicial
        update_main_home_nav(HOME_FILE, HUB_DIR)

        # 2. Injeta link com extensão .html no Hub Central
        update_hub_showcase(HUB_FILE, book_slug, title)

        # 3. Salva no Sitemap com a extensão .html
        update_sitemap(SITEMAP_FILE, new_page_url)

        # 4. Garante que a pasta ia-lucrativa existe e escreve o arquivo .html solto
        os.makedirs(HUB_DIR, exist_ok=True)
        with open(target_html, "w", encoding="utf-8") as f:
            f.write(final_html)

        log_success(f"SUCESSO! Página gerada exatamente no padrão do seu blog em: /{HUB_DIR}/{book_slug}.html")
    except Exception as e:
        log_error(f"Erro ao processar: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()