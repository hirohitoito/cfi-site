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
  <p>Selected indicators and structural proxies derived from trade, market, and vessel-side operational data.</p>

  <div class="signal-grid">
    <div class="signal">Market Signals<br><small>CIF–FOB proxies</small></div>
    <div class="signal">Flow Signals<br><small>Vessel-side operational signals</small></div>
    <div class="signal">Network Signals<br><small>Under development</small></div>
    <div class="signal">Infrastructure Signals<br><small>Under development</small></div>
  </div>

  <div class="chart-card">
    <h3>Freight Proxy: LNG vs Oil</h3>
    <p>Derived signal estimating logistics cost pressure embedded in commodity trade values.</p>
    <img src="static/charts/freight_proxy.png" style="width:100%; max-width:850px;">
  </div>

  <div class="chart-card">
    <h3>LNG Freight Proxy and Vessel Dwell Time</h3>
    <p>Connecting market-side freight pressure with vessel-side operational signals.</p>
    <img src="static/charts/lng_freight_vessel_signal.png" style="width:100%; max-width:850px;">
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
        "title": "From LNG to Oil: Substitution Dynamics",
        "description": "Price changes propagate through constrained industrial systems.",
        "tags": ["LNG", "Oil", "Substitution"],
    },
    {
        "category": "Shipping",
        "title": "Ports as Network Positions",
        "description": "Ports compete as nodes in networks, not isolated assets.",
        "tags": ["Ports", "Network"],
    },
]

def main():
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    template = Template(HTML_TEMPLATE)
    html = template.render(articles=articles)
    (PUBLIC_DIR / "index.html").write_text(html, encoding="utf-8")
    print("Built index.html")

if __name__ == "__main__":
    main()
