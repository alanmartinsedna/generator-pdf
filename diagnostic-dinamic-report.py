from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Table, TableStyle, Spacer
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# =========================
# UTILIDADES DEFAULT
# =========================

# Converte pixel para pontos
def px_to_pt(px):
    return px * 0.75

# 👉 Converte cor HEX (CSS) → RGB (0 a 1)
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return (
        int(hex_color[0:2], 16) / 255,
        int(hex_color[2:4], 16) / 255,
        int(hex_color[4:6], 16) / 255,
    )

'''
👉 Faz transição suave entre duas cores
c1 = cor inicial
c2 = cor final
t = valor entre 0 e 1
'''
def interpolate_color(c1, c2, t):
    return (
        c1[0] + (c2[0] - c1[0]) * t,
        c1[1] + (c2[1] - c1[1]) * t,
        c1[2] + (c2[2] - c1[2]) * t,
    )

# =========================
# GRADIENTE
# =========================

def draw_css_gradient(pdf, width, height):
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

        pdf.setFillColor(colors.Color(r, g, b))

        horizontal_position = (width / steps) * i
        pdf.rect(horizontal_position, 0, width / steps + 2, height, stroke=0, fill=1)
        
# =========================
# IMAGENS DO BACKGROUND DO DOCUMENTO
# =========================

def draw_images(pdf, width, height):
    scale_factor = 0.35

    # -------------------------Q
    # IMG 1 bg-img-1.png
    # -------------------------
    img1_width = px_to_pt(883 * scale_factor)
    img1_height = px_to_pt(1175 * scale_factor)

    x1 = 409
    y1 = 540
    
    pdf.drawImage(
        "bg-img-1.png",
        x1,
        y1,
        width=img1_width,
        height=img1_height,
        mask='auto'
    )

    # -------------------------
    # IMG 2 bg-img-2.png
    # -------------------------
    img2_width = px_to_pt(1598 * scale_factor)
    img2_height = px_to_pt(1825 * scale_factor)

    x2 = -165
    y2 = -172

    pdf.drawImage(
        "bg-img-2.png",
        x2,
        y2,
        width=img2_width,
        height=img2_height,
        mask='auto'
    )

# =========================
# EXECUÇÃO DO BACKGROUND DO ARQUIVO
# =========================

pdf = canvas.Canvas("Relatorio-Diagnostico.pdf", pagesize=A4)
width, height = A4
draw_css_gradient(pdf, width, height)
draw_images(pdf, width, height)


# =======================================================================================
# "------------⬇️------ INICIO DO BLOCO PARA CONTEUDO DO RELATORIO ------⬇️------------"











# "------------⬆️-------- FIM DO BLOCO PARA CONTEUDO DO RELATORIO -------⬆️------------"
# =======================================================================================

pdf.save()