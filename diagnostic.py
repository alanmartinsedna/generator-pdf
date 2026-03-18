from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


# Converte HEX → RGB (0 a 1)
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return (
        int(hex_color[0:2], 16) / 255,
        int(hex_color[2:4], 16) / 255,
        int(hex_color[4:6], 16) / 255,
    )


# Interpolação entre duas cores
def interpolate_color(c1, c2, t):
    return (
        c1[0] + (c2[0] - c1[0]) * t,
        c1[1] + (c2[1] - c1[1]) * t,
        c1[2] + (c2[2] - c1[2]) * t,
    )


# Gradiente baseado no CSS (diagonal)
def draw_css_gradient(pdf, width, height):
    steps = 300  # quanto maior, mais suave

    # cores do CSS
    hex_colors = [
        "#c5dee9",
        "#d7e1f1",
        "#e9e5f3",
        "#f7e9f3",
        "#fafafa"
    ]

    # converter para RGB
    rgb_colors = [hex_to_rgb(c) for c in hex_colors]

    segments = len(rgb_colors) - 1

    for i in range(steps):
        t_global = i / steps

        # qual segmento estamos
        seg = min(int(t_global * segments), segments - 1)

        t_local = (t_global - seg / segments) * segments

        c1 = rgb_colors[seg]
        c2 = rgb_colors[seg + 1]

        r, g, b = interpolate_color(c1, c2, t_local)

        pdf.setFillColor(colors.Color(r, g, b))

        # efeito diagonal (to right bottom)
        x = (width / steps) * i
        y = (height / steps) * i

        pdf.rect(x, 0, width / steps + 2, height, stroke=0, fill=1)


# =========================
# EXECUÇÃO
# =========================

pdf = canvas.Canvas("Relatorio-Diagnostico.pdf", pagesize=A4)

width, height = A4

draw_css_gradient(pdf, width, height)

pdf.save()