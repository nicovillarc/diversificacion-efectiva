"""Carrusel Instagram — adaptación visual de la autopsia del portafolio.

Formato: 1080×1080. Sin fórmulas. Narrativa = misma lógica del paper.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
OUT = ROOT / "instagram" / "carousel"
SIZE = 1080

# Paleta alineada al paper (navy / slate; sin púrpura ni cream genérico)
NAVY = (27, 79, 114)
SLATE = (93, 109, 126)
INK = (28, 40, 51)
MUTED = (86, 101, 115)
LINE = (213, 216, 220)
BG = (255, 255, 255)
SOFT = (247, 249, 251)
ACCENT = (146, 43, 33)  # solo énfasis puntual

FONT_REG = "/System/Library/Fonts/Supplemental/Georgia.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
FONT_ITAL = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def new_canvas(bg=BG) -> Image.Image:
    return Image.new("RGB", (SIZE, SIZE), bg)


def draw_footer(draw: ImageDraw.ImageDraw, n: int, total: int = 10) -> None:
    draw.line([(72, 1008), (SIZE - 72, 1008)], fill=LINE, width=1)
    draw.text((72, 1022), "Autopsia de un portafolio 60/40", font=font(FONT_ITAL, 22), fill=MUTED)
    draw.text((SIZE - 72, 1022), f"{n}/{total}", font=font(FONT_REG, 22), fill=MUTED, anchor="ra")


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = w if not cur else f"{cur} {w}"
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    fnt: ImageFont.FreeTypeFont,
    fill,
    max_w: int,
    line_gap: int = 10,
    align: str = "left",
) -> int:
    x, y = xy
    lines = wrap_text(draw, text, fnt, max_w)
    for line in lines:
        if align == "center":
            draw.text((SIZE // 2, y), line, font=fnt, fill=fill, anchor="ma")
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size + line_gap)
    return y


def fit_image(path: Path, max_w: int, max_h: int) -> Image.Image:
    im = Image.open(path).convert("RGB")
    im.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    return im


def paste_center(base: Image.Image, im: Image.Image, top: int) -> None:
    x = (SIZE - im.width) // 2
    base.paste(im, (x, top))


def question_badge(draw: ImageDraw.ImageDraw, text: str, y: int = 56) -> None:
    draw.text((72, y), text.upper(), font=font(FONT_BOLD, 20), fill=NAVY)


def slide_01() -> Image.Image:
    im = new_canvas()
    d = ImageDraw.Draw(im)
    # banda superior sutil
    d.rectangle([(0, 0), (SIZE, 16)], fill=NAVY)
    y = draw_wrapped(
        d,
        "¿Tu cartera realmente está diversificada?",
        (72, 320),
        font(FONT_BOLD, 54),
        INK,
        SIZE - 144,
        line_gap=14,
        align="center",
    )
    y += 28
    draw_wrapped(
        d,
        "Una autopsia cuantitativa de un portafolio 60/40.",
        (72, y),
        font(FONT_ITAL, 30),
        SLATE,
        SIZE - 144,
        line_gap=10,
        align="center",
    )
    d.text((SIZE // 2, 920), "10 slides  ·  diagnóstico, no optimización", font=font(FONT_REG, 22), fill=MUTED, anchor="ma")
    draw_footer(d, 1)
    return im


def slide_02() -> Image.Image:
    im = new_canvas(SOFT)
    d = ImageDraw.Draw(im)
    d.rectangle([(0, 0), (SIZE, 16)], fill=NAVY)
    question_badge(d, "La cartera")
    d.text((72, 100), "10 activos  ·  60% renta variable  ·  40% renta fija", font=font(FONT_BOLD, 28), fill=INK)
    y = draw_wrapped(
        d,
        "A simple vista parece una cartera bien diversificada.",
        (72, 150),
        font(FONT_ITAL, 28),
        SLATE,
        SIZE - 144,
        line_gap=8,
    )
    fig = fit_image(FIG / "fig01_portfolio_allocation_es.png", 940, 720)
    paste_center(im, fig, min(y + 20, 220))
    draw_footer(d, 2)
    return im


def slide_03() -> Image.Image:
    im = new_canvas()
    d = ImageDraw.Draw(im)
    d.rectangle([(0, 0), (SIZE, 16)], fill=NAVY)
    question_badge(d, "Primera pregunta")
    d.text((72, 100), "¿Cuántos activos tiene?", font=font(FONT_BOLD, 42), fill=INK)

    # métricas en dos bloques
    d.rounded_rectangle([(72, 180), (500, 320)], radius=8, fill=SOFT, outline=LINE)
    d.rounded_rectangle([(580, 180), (1008, 320)], radius=8, fill=SOFT, outline=LINE)
    d.text((286, 220), "10", font=font(FONT_BOLD, 56), fill=NAVY, anchor="ma")
    d.text((286, 285), "Activos nominales", font=font(FONT_REG, 22), fill=MUTED, anchor="ma")
    d.text((794, 220), "9.55", font=font(FONT_BOLD, 56), fill=NAVY, anchor="ma")
    d.text((794, 285), "Posiciones efectivas\npor capital", font=font(FONT_REG, 20), fill=MUTED, anchor="ma")

    # Fig. 2 = solo capital (no anticipar N_eff riesgo; eso llega en slide 8)
    fig = fit_image(FIG / "fig02_effective_positions_capital_es.png", 920, 480)
    paste_center(im, fig, 360)

    draw_wrapped(
        d,
        "Hasta acá, todo parece indicar que la cartera está bien distribuida.",
        (72, 880),
        font(FONT_ITAL, 26),
        SLATE,
        SIZE - 144,
        line_gap=6,
    )
    draw_footer(d, 3)
    return im


def slide_04() -> Image.Image:
    im = new_canvas()
    d = ImageDraw.Draw(im)
    d.rectangle([(0, 0), (SIZE, 16)], fill=NAVY)
    question_badge(d, "Segunda pregunta")
    d.text((72, 100), "¿Los activos realmente se comportan\nde forma independiente?", font=font(FONT_BOLD, 36), fill=INK)
    fig = fit_image(FIG / "fig03_correlation_heatmap_es.png", 900, 680)
    paste_center(im, fig, 220)
    draw_wrapped(
        d,
        "Muchos instrumentos se mueven prácticamente al mismo tiempo.",
        (72, 910),
        font(FONT_ITAL, 26),
        SLATE,
        SIZE - 144,
        line_gap=6,
    )
    draw_footer(d, 4)
    return im


def slide_05() -> Image.Image:
    im = new_canvas(SOFT)
    d = ImageDraw.Draw(im)
    d.rectangle([(0, 0), (SIZE, 16)], fill=NAVY)
    question_badge(d, "Estructura de dependencia")
    d.text((72, 100), "Clusters de riesgo", font=font(FONT_BOLD, 42), fill=INK)
    y = draw_wrapped(
        d,
        "Cuando agrupamos los activos según cómo se mueven, aparecen claramente los clusters de riesgo.",
        (72, 165),
        font(FONT_ITAL, 26),
        SLATE,
        SIZE - 144,
        line_gap=8,
    )
    fig = fit_image(FIG / "fig04_correlation_network_es.png", 920, 680)
    paste_center(im, fig, min(y + 10, 280))
    draw_footer(d, 5)
    return im


def slide_06() -> Image.Image:
    im = new_canvas()
    d = ImageDraw.Draw(im)
    d.rectangle([(0, 0), (SIZE, 16)], fill=NAVY)
    question_badge(d, "Tercera pregunta")
    d.text((72, 100), "¿Quién genera realmente el riesgo?", font=font(FONT_BOLD, 38), fill=INK)
    d.text((72, 165), "Mismo peso de capital ≠ misma contribución al riesgo.", font=font(FONT_ITAL, 24), fill=SLATE)
    d.text((72, 210), "Destacan  NVDA   ·   TSLA   ·   MU", font=font(FONT_BOLD, 26), fill=ACCENT)
    fig = fit_image(FIG / "fig05_weight_vs_prc_es.png", 980, 680)
    paste_center(im, fig, 270)
    draw_footer(d, 6)
    return im


def slide_07() -> Image.Image:
    im = new_canvas()
    d = ImageDraw.Draw(im)
    d.rectangle([(0, 0), (SIZE, 16)], fill=NAVY)
    question_badge(d, "Capital vs. riesgo")
    d.text((72, 100), "60/40 de capital\nno es 60/40 de riesgo", font=font(FONT_BOLD, 40), fill=INK)
    fig = fit_image(FIG / "fig06_capital_vs_risk_allocation_es.png", 900, 560)
    paste_center(im, fig, 240)
    draw_wrapped(
        d,
        "Aunque el 40% del capital está invertido en bonos, estos aportan apenas el 2.35% del riesgo total.",
        (72, 840),
        font(FONT_ITAL, 26),
        SLATE,
        SIZE - 144,
        line_gap=8,
    )
    draw_footer(d, 7)
    return im


def slide_08() -> Image.Image:
    im = new_canvas(SOFT)
    d = ImageDraw.Draw(im)
    d.rectangle([(0, 0), (SIZE, 16)], fill=NAVY)
    question_badge(d, "Cuarta pregunta")
    d.text((72, 100), "¿Cuántas posiciones efectivas\ntiene realmente la cartera?", font=font(FONT_BOLD, 36), fill=INK)

    d.rounded_rectangle([(72, 210), (500, 340)], radius=8, fill=BG, outline=LINE)
    d.rounded_rectangle([(580, 210), (1008, 340)], radius=8, fill=BG, outline=LINE)
    d.text((286, 250), "10", font=font(FONT_BOLD, 52), fill=SLATE, anchor="ma")
    d.text((286, 305), "Activos nominales", font=font(FONT_REG, 20), fill=MUTED, anchor="ma")
    d.text((794, 250), "6.58", font=font(FONT_BOLD, 52), fill=ACCENT, anchor="ma")
    d.text((794, 305), "Efectivas por riesgo", font=font(FONT_REG, 20), fill=MUTED, anchor="ma")

    fig = fit_image(FIG / "fig07_effective_positions_es.png", 920, 420)
    paste_center(im, fig, 370)

    draw_wrapped(
        d,
        "La cartera parece tener 10 posiciones, pero desde el punto de vista del riesgo se comporta como si tuviera poco más de seis.",
        (72, 830),
        font(FONT_ITAL, 24),
        SLATE,
        SIZE - 144,
        line_gap=6,
    )
    draw_footer(d, 8)
    return im


def slide_09() -> Image.Image:
    im = new_canvas()
    d = ImageDraw.Draw(im)
    d.rectangle([(0, 0), (SIZE, 16)], fill=NAVY)
    question_badge(d, "Última pregunta")
    d.text((72, 100), "¿Cuántas fuentes independientes\nde riesgo existen?", font=font(FONT_BOLD, 36), fill=INK)
    y = draw_wrapped(
        d,
        "El PCA permite identificar cuántos factores comunes explican el comportamiento conjunto de la cartera.",
        (72, 200),
        font(FONT_ITAL, 24),
        SLATE,
        SIZE - 144,
        line_gap=8,
    )
    # resultado clave sin fórmula
    d.rounded_rectangle([(72, y + 10), (1008, y + 110)], radius=8, fill=SOFT, outline=LINE)
    d.text((SIZE // 2, y + 45), "3 factores explican ≥ 80% de la variación conjunta", font=font(FONT_BOLD, 26), fill=NAVY, anchor="ma")
    d.text((SIZE // 2, y + 85), "5 factores explican ≥ 90%", font=font(FONT_REG, 22), fill=MUTED, anchor="ma")

    fig = fit_image(FIG / "fig08_pca_scree_es.png", 920, 480)
    paste_center(im, fig, y + 130)
    draw_footer(d, 9)
    return im


def slide_10() -> Image.Image:
    im = new_canvas()
    d = ImageDraw.Draw(im)
    d.rectangle([(0, 0), (SIZE, 16)], fill=NAVY)
    d.rectangle([(0, SIZE - 120), (SIZE, SIZE)], fill=NAVY)

    d.text((SIZE // 2, 200), "La verdadera diversificación", font=font(FONT_BOLD, 44), fill=INK, anchor="ma")
    y = 290
    paragraphs = [
        "Una cartera puede contener muchos activos y, aun así, depender de pocas fuentes de riesgo.",
        "Contar posiciones no alcanza para medir la diversificación.",
        "Para entender cómo está realmente construido un portafolio es necesario analizar su estructura de riesgo.",
    ]
    for p in paragraphs:
        y = draw_wrapped(d, p, (88, y), font(FONT_REG, 28), INK, SIZE - 176, line_gap=10, align="center")
        y += 28

    # idea única
    d.rounded_rectangle([(88, 780), (SIZE - 88, 900)], radius=10, fill=SOFT, outline=LINE)
    draw_wrapped(
        d,
        "Diversificación ≠ cantidad de activos. Diversificación = fuentes de riesgo independientes.",
        (110, 815),
        font(FONT_BOLD, 24),
        NAVY,
        SIZE - 220,
        line_gap=8,
        align="center",
    )

    d.text(
        (SIZE // 2, SIZE - 70),
        "Investigación completa disponible en LinkedIn y GitHub.",
        font=font(FONT_ITAL, 22),
        fill=(230, 235, 240),
        anchor="ma",
    )
    return im


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    builders = [
        slide_01,
        slide_02,
        slide_03,
        slide_04,
        slide_05,
        slide_06,
        slide_07,
        slide_08,
        slide_09,
        slide_10,
    ]
    print("=== Carrusel Instagram (1080×1080) ===")
    for i, fn in enumerate(builders, start=1):
        img = fn()
        path = OUT / f"slide_{i:02d}.png"
        img.save(path, "PNG", optimize=True)
        print(f"  {path.relative_to(ROOT)}")
    print(f"\nListo: {OUT}")


if __name__ == "__main__":
    main()
