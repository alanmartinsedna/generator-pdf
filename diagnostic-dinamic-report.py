# =========================
# IMPORTS
# =========================

from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Table, TableStyle, Spacer
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# =========================
# CONSTANTES
# =========================

MARGIN_LEFT = 20
MARGIN_RIGHT = 20
MARGIN_TOP = 56.7
MARGIN_BOTTOM = 70.9
FOOTER_Y = 42.5
HEADER_BOTTOM_PADDING = 20

# =========================
# UTILIDADES
# =========================

def px_to_pt(px):
    return px * 0.75

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return (
        int(hex_color[0:2], 16) / 255,
        int(hex_color[2:4], 16) / 255,
        int(hex_color[4:6], 16) / 255,
    )

def interpolate_color(c1, c2, t):
    return (
        c1[0] + (c2[0] - c1[0]) * t,
        c1[1] + (c2[1] - c1[1]) * t,
        c1[2] + (c2[2] - c1[2]) * t,
    )

# =========================
# BACKGROUND (GRADIENTE)
# =========================

def draw_css_gradient(canvas, width, height):
    steps = 300

    hex_colors = [
        "#c5dee9",
        "#d7e1f1",
        "#e9e5f3",
        "#f7e9f3",
        "#fafafa"
    ]

    rgb_colors = [hex_to_rgb(c) for c in hex_colors]
    segments = len(rgb_colors) - 1

    for i in range(steps):
        t_global = i / steps

        seg = min(int(t_global * segments), segments - 1)
        t_local = (t_global - seg / segments) * segments

        c1 = rgb_colors[seg]
        c2 = rgb_colors[seg + 1]

        r, g, b = interpolate_color(c1, c2, t_local)

        canvas.setFillColor(colors.Color(r, g, b))

        x = (width / steps) * i
        canvas.rect(x, 0, width / steps + 2, height, stroke=0, fill=1)

# =========================
# BACKGROUND IMAGENS
# =========================

def draw_images(canvas, width, height):
    scale_factor = 0.35

    img1_width = px_to_pt(883 * scale_factor)
    img1_height = px_to_pt(1175 * scale_factor)

    canvas.drawImage(
        "bg-img-1.png",
        409,
        540,
        width=img1_width,
        height=img1_height,
        mask='auto'
    )

    img2_width = px_to_pt(1598 * scale_factor)
    img2_height = px_to_pt(1825 * scale_factor)

    canvas.drawImage(
        "bg-img-2.png",
        -165,
        -172,
        width=img2_width,
        height=img2_height,
        mask='auto'
    )

# =========================
# LOGO
# =========================

def draw_logo(canvas):
    page_width, page_height = canvas._pagesize

    width = 100
    height = 48

    x = (page_width - width) / 2
    y = page_height - 10 - height

    canvas.drawImage(
        "logo-edna-center.png",
        x,
        y,
        width=width,
        height=height,
        mask='auto'
    )

# =========================
# BACKGROUND (ANTES DO CONTEÚDO)
# =========================

def draw_background(canvas, doc):
    canvas.saveState()

    width, height = A4

    draw_css_gradient(canvas, width, height)
    draw_images(canvas, width, height)

    canvas.restoreState()

# =========================
# HEADER + FOOTER (DEPOIS DO CONTEÚDO)
# =========================

def draw_header_footer(canvas, doc):
    canvas.saveState()

    width, height = A4

    # LOGO
    draw_logo(canvas)

    # FOOTER (agora sempre visível)
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.black)

    page_number_text = f"Página {doc.page}"

    canvas.drawRightString(
        width - MARGIN_RIGHT,
        FOOTER_Y,
        page_number_text
    )

    canvas.restoreState()

# =========================
# DOCUMENTO BASE
# =========================

doc = BaseDocTemplate(
    "./pdf-files/Diagnóstico de Riscos Psicossociais.pdf",
    pagesize=A4
)

# =========================
# FRAME (ÁREA DO CONTEÚDO)
# =========================

frame = Frame(
    x1=MARGIN_LEFT,
    y1=MARGIN_BOTTOM,
    width=A4[0] - (MARGIN_LEFT + MARGIN_RIGHT),
    height=A4[1] - (MARGIN_TOP + MARGIN_BOTTOM + HEADER_BOTTOM_PADDING),
    id="main_frame"
)

# =========================
# TEMPLATE
# =========================

template = PageTemplate(
    id="main_template",
    frames=[frame],
    onPage=draw_background,        # 🔥 fundo primeiro
    onPageEnd=draw_header_footer  # 🔥 depois footer/logo por cima
)

doc.addPageTemplates([template])

# =========================
# ESTILOS
# =========================

styles = getSampleStyleSheet()

# =========================
# CONTEÚDO DINÂMICO
# =========================

elements = []

# =======================================================================================
# "------------⬇️------ INICIO DO BLOCO PARA CONTEUDO DO RELATORIO ------⬇️------------"
style = ParagraphStyle(...)

elements.append(
    Paragraph(
        "Diagnóstico de Riscos Psicossociais",
        ParagraphStyle(
            name="Custom",
            fontName="Helvetica-Bold",  # weight 700
            fontSize=20,
            textColor=colors.HexColor('#596CFF'),
            alignment=0  # left
        )
    )
)
elements.append(Spacer(1, 20))
elements.append(
    Paragraph(
        "Grupo Agulhas Negras - Agulhas Negras",
        ParagraphStyle(
            name="Custom",
            fontName="Helvetica",  # weight 400
            fontSize=7,
            textColor=colors.HexColor('#344767'),
            alignment=0  # left
        )
    )
)
elements.append(Spacer(1, 20))




# "------------⬆️-------- FIM DO BLOCO PARA CONTEUDO DO RELATORIO -------⬆️------------"
# =======================================================================================

# =========================
# BUILD FINAL
# =========================

doc.build(elements)