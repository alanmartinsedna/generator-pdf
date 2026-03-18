from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


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

        x = (width / steps) * i
        pdf.rect(x, 0, width / steps + 2, height, stroke=0, fill=1)


# =========================
# IMAGENS
# =========================

def draw_images(pdf, width, height):
    # -------------------------
    # IMG 1 (top-right)
    # -------------------------
    scale_factor = 0.3
    img1_width = px_to_pt(883 * scale_factor)
    img1_height = px_to_pt(1175 * scale_factor)

    x1 = width - img1_width + px_to_pt(62)
    y1 = height - img1_height + px_to_pt(140)

    pdf.drawImage(
        "bg-img-1.png",
        x1,
        y1,
        width=img1_width,
        height=img1_height,
        mask='auto'
    )

    # -------------------------
    # IMG 2 (bottom-left) ✅ CORRIGIDO
    # -------------------------
    img2_width = px_to_pt(1598 * scale_factor)
    img2_height = px_to_pt(1825 * scale_factor)

    x2 = -px_to_pt(290)

    # 👇 AJUSTE PRINCIPAL AQUI
    y2 = -img2_height + px_to_pt(300)

    pdf.drawImage(
        "bg-img-2.png",
        x2,
        y2,
        width=img2_width,
        height=img2_height,
        mask='auto'
    )


# =========================
# EXECUÇÃO
# =========================

pdf = canvas.Canvas("Relatorio-Diagnostico.pdf", pagesize=A4)

width, height = A4

draw_css_gradient(pdf, width, height)

draw_images(pdf, width, height)

pdf.save()