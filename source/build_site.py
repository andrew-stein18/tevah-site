"""Builds the Tevah page two ways from site.template.html + bg_layers.json:
   ../tevah-site.html  the claude.ai artifact (the publisher adds the document skeleton)
   ../site/            a standalone static site for tevah.io (Vercel)"""
import base64, json, pathlib, re

here = pathlib.Path(__file__).parent
root = here.parent
tpl = (here / "site.template.html").read_text()
data = json.dumps(json.loads((here / "bg_layers.json").read_text()), separators=(",", ":"))
page = tpl.replace("/*DATA*/null", data, 1)
# the artifact is one file, so the team photo rides inline there; the site serves it as a file
team = (here / "team.jpg").read_bytes()
(root / "tevah-site.html").write_text(page.replace('src="team.jpg"', 'src="data:image/jpeg;base64,' + base64.b64encode(team).decode() + '"', 1))

URL = "https://tevah.io"
TITLE = "Tevah · AI is the flood. Rise with it."
DESC = "Engineers inside your business, shipping the AI that changes how it runs. We don’t leave until you’re ahead. Bringing AI to the rest of the economy."
title, icon = re.search(r"<title>.*?</title>\n", page).group(0), re.search(r'<link rel="icon".*?>\n', page).group(0)
style = re.search(r"<style>.*?</style>\n", page, re.S).group(0)
fonts = "".join(re.findall(r'<link rel="(?:preconnect|stylesheet)".*?>\n', page))
body = page.replace(title, "").replace(icon, "").replace(style, "").replace(fonts, "").replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#0c0f14">
<link rel="canonical" href="{URL}/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Tevah">
<meta property="og:url" content="{URL}/">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{URL}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A dithered ark landing after the flood, people walking out toward the sun.">
<meta name="twitter:card" content="summary_large_image">
{fonts}{style}</head>
<body>
"""
site = root / "site"
site.mkdir(exist_ok=True)
(site / "index.html").write_text(head + body.strip() + "\n</body>\n</html>\n")
(site / "team.jpg").write_bytes(team)
(site / "favicon.svg").write_text(re.search(r"data:image/svg\+xml,(.*?)\">", icon).group(1).replace("%23", "#"))
(site / "vercel.json").write_text(json.dumps({"cleanUrls": True, "headers": [
    {"source": "/(.*)", "headers": [{"key": "X-Content-Type-Options", "value": "nosniff"},
        {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}, {"key": "X-Frame-Options", "value": "DENY"}]},
    {"source": "/(.*).(png|jpg)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]}]}, indent=2))
print("built", len(page), "bytes")
