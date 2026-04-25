from pathlib import Path
from jinja2 import Template

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = BASE_DIR / "public"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Commodity Flow</title>
  <link rel="stylesheet" href="static/css/style.css">
</head>
<body>

<header class="header">
  <div class="logo">Commodity Flow</div>
  <nav>
    <a href="index.html">Home</a>
    <a href="insights.html">Insights</a>
    <a href="signals.html">Signals</a>
    <a href="interviews.html">Interviews</a>
    <a href="framework.html">Framework</a>
    <a href="contact.html">Contact</a>
  </nav>
</header>

<section class="hero">
  <h1>Understanding global trade through<br><span>flows, markets, and structures.</span></h1>
  <p>Commodity Flow connects market signals, shipping flows, and industrial structures to explain how global systems actually change.</p>
  <a class="button" href="contact.html">Request a Discussion</a>
</section>

<section class="section">
  <h2>Latest Insights</h2>
  <div class="cards">
    {% for article in articles %}
    <div class="card">
      <p class="category">{{ article.category }}</p>
      <h3>{{ article.title }}</h3>
      <p>{{ article.description }}</p>
      <div>
        {% for tag in article.tags %}
        <span class="tag">{{ tag }}</span>
        {% endfor %}
      </div>
    </div>
    {% endfor %}
  </div>
</section>

<section class="section light">
  <h2>Signals</h2>
  <p>Selected indicators and structural proxies derived from public data, trade statistics, and flow observations.</p>
  <div class="signal-grid">
    <div class="signal">Market Signals<br><small>CIF–FOB freight proxies</small></div>
    <div class="signal">Flow Signals<br><small>Routes, ports, vessel movement</small></div>
    <div class="signal">Network Signals<br><small>Connectivity and centrality</small></div>
    <div class="signal">Infrastructure Signals<br><small>Capacity, queues, terminals</small></div>
  </div>
</section>

<footer class="footer">
  <p>© Commodity Flow. Structural intelligence for global trade.</p>
</footer>

</body>
</html>
"""

articles = [
    {
        "category": "Commodities",
        "title": "From LNG to Oil: How Substitution Actually Happens",
        "description": "Price shocks do not move markets alone. Substitution depends on infrastructure, logistics, and industrial constraints.",
        "tags": ["LNG", "Oil", "Substitution"],
    },
    {
        "category": "Shipping",
        "title": "Container Hubs as Networks",
        "description": "Port competitiveness depends not only on facilities, but on position inside evolving trade networks.",
        "tags": ["Containers", "Ports", "Network"],
    },
    {
        "category": "Passenger Flow",
        "title": "Cruise Terminals as Flow Systems",
        "description": "Passenger flows, queues, and CIQ capacity can be analyzed as constrained infrastructure systems.",
        "tags": ["Cruise", "Queueing", "CIQ"],
    },
]

def write_page(filename: str, title: str = ""):
    template = Template(HTML_TEMPLATE)
    html = template.render(articles=articles)
    output_path = PUBLIC_DIR / filename
    output_path.write_text(html, encoding="utf-8")

def main():
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    write_page("index.html")
    print("Built public/index.html")

if __name__ == "__main__":
    main()
