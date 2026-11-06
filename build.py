"""Assemble mockup pages: src/<page>.html bodies + shared header/contact/footer taken from index.html.
Each src file starts with:  <!-- title: Page title | active: About -->"""
import re, pathlib
root = pathlib.Path(__file__).parent
home = (root / 'index.html').read_text()
head = home[:home.index('<header class="site-header">')]
header = re.search(r'<header class="site-header">.*?</header>', home, re.S).group(0)
contact = re.search(r'<section class="section cta" id="contact">.*?</section>', home, re.S).group(0)
footer = re.search(r'<footer class="site-footer">.*?</footer>', home, re.S).group(0)
for src in sorted((root / 'src').glob('*.html')):
    body = src.read_text()
    m = re.match(r'<!-- title: (.*?) \| active: (.*?) -->\n', body)
    title, active = m.groups()
    body = body[m.end():]
    h = header.replace('class="active" ', '')
    h = re.sub(rf'(<a )(href="[^"]*">{re.escape(active)}</a>)', r'\1class="active" \2', h, count=1)
    page = head.replace(re.search(r'<title>.*?</title>', head).group(0), f'<title>{title} · York Traditional Acupuncture (design mockup)</title>')
    page += h + '\n' + body.replace('<!-- CONTACT -->', contact) + '\n' + footer + '\n\n</body>\n</html>\n'
    (root / src.name).write_text(page)
    print('built', src.name)
