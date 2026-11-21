# Генерирует страницы статей блога (blog/<slug>.html) из articles/*.txt
# Разметка исходника: @поле значение | ## Короткое | Полный заголовок | ### подзаголовок
#                     - пункт списка (**жирный**) | > вывод-цитата | [[slug|текст]] — ссылка на статью
import glob, html, re, os

SRC = os.path.dirname(os.path.abspath(__file__)) + "/articles"
OUT = "/root/projects/vk-portfolio/blog"
os.makedirs(OUT, exist_ok=True)
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17 17 7M8 7h9v9"/></svg>'

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[\[([\w-]+)\|(.+?)\]\]", r'<a href="\1.html">\2</a>', t)
    return t

def parse(path):
    meta, blocks = {}, []
    for raw in open(path, encoding="utf-8").read().split("\n\n"):
        b = raw.strip()
        if not b: continue
        if b.startswith("@"):
            for line in b.split("\n"):
                k, v = line[1:].split(" ", 1); meta[k] = v
        elif b.startswith("### "): blocks.append(("h3", b[4:]))
        elif b.startswith("## "):
            short, full = [x.strip() for x in b[3:].split("|", 1)]
            blocks.append(("h2", short, full))
        elif b.startswith("- "): blocks.append(("ul", [l[2:] for l in b.split("\n")]))
        elif b.startswith("> "): blocks.append(("quote", b[2:]))
        else: blocks.append(("p", b))
    return meta, blocks

def words(blocks):
    n = 0
    for b in blocks:
        for x in b[1:]:
            n += len(" ".join(x if isinstance(x, list) else [x]).split())
    return n

def render(meta, blocks, nxt):
    toc, body, i = [], [], 0
    for b in blocks:
        if b[0] == "h2":
            i += 1; anchor = f"s{i}"
            toc.append(f'          <li><a href="#{anchor}"><span>{i:02d}</span>{html.escape(b[1])}</a></li>')
            body.append(f'        <h2 id="{anchor}">{inline(b[2])}</h2>')
        elif b[0] == "h3": body.append(f"        <h3>{inline(b[1])}</h3>")
        elif b[0] == "p": body.append(f"        <p>{inline(b[1])}</p>")
        elif b[0] == "ul": body.append("        <ul>\n" + "\n".join(f"          <li>{inline(x)}</li>" for x in b[1]) + "\n        </ul>")
        elif b[0] == "quote": body.append(f'        <p class="article__callout">{inline(b[1])}</p>')
    mins = max(1, round(words(blocks) / 180))
    return f"""<!DOCTYPE html>
<html lang="ru" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(meta['seo_title'])}</title>
  <meta name="description" content="{html.escape(meta['seo_desc'])}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@300;400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>

  <!-- ================= ШАПКА ================= -->
  <header class="header">
    <div class="container header__inner">
      <a href="../index.html" class="logo">ВК<span>.</span></a>
      <nav class="nav">
        <a href="../index.html">Главная</a>
        <a href="../cases/index.html">Кейсы</a>
        <a href="../index.html#journal">Статьи</a>
      </nav>
      <a href="https://t.me/mofyl" target="_blank" rel="noopener" class="link-arrow">Связаться {ARROW}</a>
    </div>
  </header>

  <!-- Текст статьи генерируется из исходника; правьте текст прямо здесь или в исходнике -->
  <main class="case-wrap">
    <section class="case-hero article-hero">
      <div class="container">
        <div class="case-meta reveal"><span class="tag">{html.escape(meta['rubric'])}</span><span class="muted">Владислав Королев · {mins} мин чтения</span></div>
        <h1 class="article-hero__title reveal">{html.escape(meta['title'])}</h1>
        <p class="case-lead reveal">{html.escape(meta['lead'])}</p>
      </div>
    </section>

    <div class="container article-layout">
      <!-- Оглавление: быстрый переход к блокам (на телефоне — сверху) -->
      <aside class="toc">
        <div class="toc__title">Содержание</div>
        <ol class="toc__list">
{chr(10).join(toc)}
        </ol>
      </aside>

      <article class="article">
{chr(10).join(body)}

        <!-- Связаться -->
        <div class="dark article-cta">
          <h2>Обсудим вашу задачу?</h2>
          <p class="muted">Напишите в Telegram — отвечу в течение дня.</p>
          <a href="https://t.me/mofyl" target="_blank" rel="noopener" class="btn btn--light">Написать в Telegram</a>
        </div>

        <!-- Следующая статья -->
        <a href="{nxt['slug']}.html" class="next-article">
          <span class="muted">Следующая статья</span>
          <span class="next-article__title">{html.escape(nxt['title'])}</span>
          <span class="next-article__lead">{html.escape(nxt['lead'])}</span>
          <span class="link-arrow">Читать {ARROW}</span>
        </a>
      </article>
    </div>
  </main>

  <!-- ================= ФУТЕР ================= -->
  <footer class="dark footer">
    <div class="container">
      <h2 class="h2 reveal">Хотите обсудить роль или&nbsp;проект?</h2>
      <p class="footer__lead muted reveal">Напишите в Telegram — отвечу в течение дня.</p>
      <a href="https://t.me/mofyl" target="_blank" rel="noopener" class="btn btn--light reveal">Написать в Telegram</a>
      <div class="contacts">
        <a href="https://t.me/mofyl" target="_blank" rel="noopener">Telegram: @mofyl</a>
        <a href="tel:+375257103242">+375 (25) 710-32-42</a>
        <a href="https://www.behance.net/batbatbata7b47" target="_blank" rel="noopener">behance.net/batbatbata7b47</a>
      </div>
      <div class="copyright">© <span id="year">2026</span> Владислав Королев</div>
    </div>
  </footer>

  <script src="../js/main.js"></script>
</body>
</html>
"""

arts = [parse(f) for f in sorted(glob.glob(SRC + "/*.txt"))]
for i, (meta, blocks) in enumerate(arts):
    nxt = arts[(i + 1) % len(arts)][0]
    open(f"{OUT}/{meta['slug']}.html", "w", encoding="utf-8").write(render(meta, blocks, nxt))
    print("ok", meta["slug"], len([b for b in blocks if b[0] == "h2"]), "sections")

# Карточки для главной (печатаем — вставляются в index.html)
cards = []
for i, (m, _) in enumerate(arts):
    cards.append(f"""          <a href="blog/{m['slug']}.html" class="note reveal" data-delay="{i*100}">
            <span class="note__tag">{html.escape(m['rubric'].split(' · ')[0])}</span>
            <h3 class="h3">{html.escape(m['title'])}</h3>
            <p>{html.escape(m['card'])}</p>
            <span class="btn btn--ghost btn--sm">Читать</span>
          </a>""")
open(os.path.dirname(SRC) + "/blog_cards.html", "w").write("\n\n".join(cards))
