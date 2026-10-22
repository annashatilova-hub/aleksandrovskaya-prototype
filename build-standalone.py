#!/usr/bin/env python3
"""Сборка standalone-прототипа в один HTML без внешних зависимостей."""
import base64
import mimetypes
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
SRC = ROOT / "index.html"
OUT = ROOT / "prototip-aleksandrovskaya.html"
ASSETS = ROOT / "assets"


def svg_data(svg: str) -> str:
    return "data:image/svg+xml;charset=utf-8," + quote(svg, safe="")


def photo(title: str, subtitle: str = "Заглушка — фото от заказчика", w: int = 800, h: int = 480) -> str:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="#e8f2f2"/>
  <rect x="{w*0.28:.0f}" y="{h*0.22:.0f}" width="{w*0.44:.0f}" height="{h*0.38:.0f}" rx="10" fill="#c5dede"/>
  <circle cx="{w*0.38:.0f}" cy="{h*0.35:.0f}" r="22" fill="#2b6b6b" opacity="0.3"/>
  <path d="M{w*0.31:.0f} {h*0.52:.0f} L{w*0.5:.0f} {h*0.38:.0f} L{w*0.69:.0f} {h*0.52:.0f} L{w*0.69:.0f} {h*0.58:.0f} L{w*0.31:.0f} {h*0.58:.0f} Z" fill="#2b6b6b" opacity="0.3"/>
  <text x="{w/2:.0f}" y="{h*0.72:.0f}" text-anchor="middle" fill="#2b6b6b" font-family="Arial,sans-serif" font-size="22" font-weight="600">{title}</text>
  <text x="{w/2:.0f}" y="{h*0.78:.0f}" text-anchor="middle" fill="#666666" font-family="Arial,sans-serif" font-size="15">{subtitle}</text>
</svg>"""
    return svg_data(svg)


def logo() -> str:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="220" height="64" viewBox="0 0 220 64">
  <text x="110" y="22" text-anchor="middle" fill="#2b6b6b" font-family="Georgia,serif" font-size="11" letter-spacing="2">БАЗА ОТДЫХА</text>
  <text x="110" y="48" text-anchor="middle" fill="#2b6b6b" font-family="Georgia,serif" font-size="24" font-style="italic">Александровская</text>
</svg>"""
    return svg_data(svg)


def hero_bg() -> str:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a3340"/>
      <stop offset="100%" stop-color="#2a4a55"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="70%" r="40%">
      <stop offset="0%" stop-color="#ffb347" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#ffb347" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1600" height="900" fill="url(#sky)"/>
  <rect width="1600" height="900" fill="url(#glow)"/>
  <ellipse cx="800" cy="700" rx="950" ry="160" fill="#0f2830" opacity="0.8"/>
  <rect x="120" y="520" width="520" height="12" rx="6" fill="#c49a6c" opacity="0.7"/>
  <circle cx="180" cy="526" r="18" fill="#ffd27a" opacity="0.8"/>
  <circle cx="240" cy="526" r="18" fill="#ffd27a" opacity="0.75"/>
  <circle cx="300" cy="526" r="18" fill="#ffd27a" opacity="0.7"/>
  <circle cx="360" cy="526" r="18" fill="#ffd27a" opacity="0.65"/>
</svg>"""
    return svg_data(svg)


def file_data_uri(path: Path) -> str | None:
    if not path.is_file():
        return None
    mime, _ = mimetypes.guess_type(path.name)
    if not mime:
        mime = "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def get_hero_uri() -> str:
    return (
        file_data_uri(ASSETS / "hero-bg.jpg")
        or file_data_uri(ASSETS / "for main block.jpg")
        or hero_bg()
    )


def main() -> None:
    html = SRC.read_text(encoding="utf-8")

    # Убрать внешние шрифты
    html = html.replace(
        "  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
        "  <link href=\"https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Marck+Script&display=swap\" rel=\"stylesheet\">\n",
        "",
    )
    html = html.replace(
        "font-family: 'Montserrat', sans-serif;",
        "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;",
    )
    html = html.replace(
        "font-family: 'Marck Script', cursive;",
        "font-family: Georgia, 'Times New Roman', serif;",
    )
    html = html.replace(
        "font-family: 'Montserrat', sans-serif",
        "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif",
    )

    hero = hero_bg()
    html = html.replace(
        "url('https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=1600&q=80') center/cover no-repeat;",
        f"url('{hero}') center/cover no-repeat;",
    )
    html = html.replace(
        "url('https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=900&q=80') center/cover no-repeat;",
        f"url('{hero}') center/cover no-repeat;",
    )

    asset_paths = sorted(
        [p for p in ASSETS.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}],
        key=lambda p: len(p.name),
        reverse=True,
    )
    for path in asset_paths:
        uri = file_data_uri(path)
        if not uri:
            if path.name == "logo.png":
                uri = logo()
            else:
                continue
        html = html.replace(f"assets/{path.name}", uri)

    html = html.replace(
        "<title>База отдыха «Александровская» — прототип</title>",
        "<title>База отдыха «Александровская» — прототип (standalone)</title>",
    )
    html = html.replace(
        "Прототип структуры сайта для согласования. Фото — временные заглушки, тексты — из материалов заказчика. Финальная версия собирается на Tilda.",
        "Standalone-прототип: один файл, всё внутри. Открыть двойным щелчком в браузере. Финальная версия собирается на Tilda.",
    )
    html = html.replace(
        "© 2026 База отдыха «Александровская». Прототип для согласования структуры сайта.",
        "© 2026 База отдыха «Александровская». Standalone-прототип для согласования структуры сайта.",
    )

    OUT.write_text(html, encoding="utf-8")
    size_kb = OUT.stat().st_size / 1024
    print(f"OK: {OUT.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
