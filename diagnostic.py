from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# =========================
# UTILIDADES
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
# FUNÇÃO DE TEXTO COM (CORREÇÃO TOP-LEFT)
# =========================
def draw_text(
        pdf,
        x,
        y,
        text,
        size=12,
        font="Helvetica",
        weight=400,
        color=colors.black,
        align="left"
    ):
    pdf.saveState()

    pdf.translate(x, y)
    pdf.scale(1, -1)

    # =========================
    # 🎨 COR
    # =========================
    def parse_color(c):
        if isinstance(c, str) and c.startswith("#"):
            c = c.lstrip("#")
            r = int(c[0:2], 16) / 255
            g = int(c[2:4], 16) / 255
            b = int(c[4:6], 16) / 255
            return colors.Color(r, g, b)

        if isinstance(c, str):
            return getattr(colors, c, colors.black)

        if isinstance(c, tuple):
            if len(c) == 4:
                r, g, b, a = c
            else:
                r, g, b = c
                a = 1

            if max(r, g, b) > 1:
                r /= 255
                g /= 255
                b /= 255

            return colors.Color(r, g, b, alpha=a)

        return c

    pdf.setFillColor(parse_color(color))

    # =========================
    # 🔠 FONTE DINÂMICA
    # =========================
    def resolve_font(font_name, weight):
        """
        Tenta encontrar variações da fonte automaticamente:
        Ex:
        MinhaFonte → MinhaFonte-Bold
        """

        if weight >= 600:
            bold_name = f"{font_name}-Bold"

            if bold_name in pdfmetrics.getRegisteredFontNames():
                return bold_name

        return font_name

    font_name = resolve_font(font, weight)

    # valida se fonte existe
    if font_name not in pdfmetrics.getRegisteredFontNames():
        raise ValueError(f"Fonte '{font_name}' não registrada no ReportLab.")

    pdf.setFont(font_name, size)

    # =========================
    # 📐 ALINHAMENTO
    # =========================
    text_width = pdf.stringWidth(text, font_name, size)

    if align == "center":
        x_offset = -text_width / 2
    elif align == "right":
        x_offset = -text_width
    else:
        x_offset = 0

    # =========================
    # 🖊️ DESENHO
    # =========================
    pdf.drawString(x_offset, -size, text)

    pdf.restoreState()

'''
    # 👇 USO DO HELPER (CORRETO) - DA FUNÇÃO def draw_text()
    draw_text(pdf, 50, 80, "Texto padrão")
    draw_text(pdf, 50, 120, "Texto azul", color="#596CFF")
    draw_text(pdf, 50, 160, "Texto vermelho", color="red")
    draw_text(pdf, 50, 200, "RGB 255", color=(255, 0, 0))
    draw_text(pdf, 50, 240, "RGBA", color=(0, 0, 255, 0.5))
    draw_text(pdf, 50, 280, "Grande", size=22)
    draw_text(pdf, 50, 320, "Pequeno", size=8)
    draw_text(pdf, 50, 360, "Normal", weight=400)
    draw_text(pdf, 50, 400, "Negrito", weight=700)
    draw_text(pdf, 50, 360, "Normal", weight=400)
    draw_text(pdf, 50, 400, "Negrito", weight=700)
    draw_text(pdf, 300, 520, "Esquerda", align="left")
    draw_text(pdf, 300, 560, "Centralizado", align="center")
    draw_text(pdf,x=300,y=650,text="Diagnóstico de Riscos 1",size=20,font="Helvetica",weight=700,color="#596CFF",align="center")
    draw_text(pdf,x=300,y=675,text="Diagnóstico de Riscos 2",size=20,font="Helvetica",weight=700,color="#596CFF",align="center")
    draw_text(pdf,50,700,"Título Principal",size=24,weight=700,color="#1A1A1A")
    draw_text(pdf,50,740,"Subtítulo explicativo",size=14,color=(120, 120, 120))
    draw_text(pdf,x=400,y=780,text="Texto avançado RGBA + alinhado",size=16,font="Helvetica",weight=700,color=(255, 100, 50, 0.7),align="right")
'''

# =========================
# LOGO COMPANY
# =========================

def draw_logo_image(
        pdf,
        image_path,
        x=None,
        y=0,
        width=100,
        height=50,
        page_width=None,
        align="left"
    ):
    pdf.saveState()

    # =========================
    # SISTEMA TOP-LEFT (corrigir imagem)
    # =========================
    pdf.translate(0, 0)
    pdf.scale(1, -1)

    # =========================
    # LARGURA DA PÁGINA
    # =========================
    if page_width is None:
        page_width = pdf._pagesize[0]

    # =========================
    # 📐 LÓGICA DE ALINHAMENTO
    # =========================
    if x is None:
        if align == "center":
            x = (page_width - width) / 2
        elif align == "right":
            x = page_width - width
        else:  # left
            x = 0

    # =========================
    # 🖼️ DESENHO DA IMAGEM
    # =========================
    pdf.drawImage(
        image_path,
        x,
        -y - height,   # 👈 correção top-left
        width=width,
        height=height,
        mask='auto'
    )

    pdf.restoreState()

    '''
         # 👇 USO DO HELPER (CORRETO) - DA FUNÇÃO def draw_logo_image()
        draw_logo_image(pdf,"logo-edna-center.png",x=50,y=50,width=100,height=48)
        draw_logo_image(pdf,"logo-edna-center.png",x=None,y=150,width=100,height=48,align="left")
        draw_logo_image(pdf,"logo-edna-center.png",y=200,width=100,height=48,align="center")
        draw_logo_image(pdf,"logo-edna-center.png",y=250,width=100,height=48,align="right")
    '''


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
# IMAGENS (AJUSTADAS PARA TOP-LEFT)
# =========================

def draw_images(pdf, width, height):
    scale_factor = 0.35

    # -------------------------
    # IMG 1 (top-right)
    # -------------------------
    img1_width = px_to_pt(883 * scale_factor)
    img1_height = px_to_pt(1175 * scale_factor)

    x1 = width - img1_width + px_to_pt(62)
    y1 = -px_to_pt(260)

    pdf.drawImage(
        "bg-img-1.png",
        x1,
        y1,
        width=img1_width,
        height=img1_height,
        mask='auto'
    )

    # -------------------------
    # IMG 2 (bottom-left)
    # -------------------------
    img2_width = px_to_pt(1598 * scale_factor)
    img2_height = px_to_pt(1825 * scale_factor)

    x2 = -px_to_pt(290)
    y2 = height - img2_height + px_to_pt(380)

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

# 🔥 SISTEMA GLOBAL TOP-LEFT
pdf.translate(0, height)
pdf.scale(1, -1)

# =========================
# FUNDO
# =========================

draw_css_gradient(pdf, width, height)
draw_images(pdf, width, height)

# =======================================================================================
# "------------⬇️------ INICIO DO BLOCO PARA CONTEUDO DO RELATORIO ------⬇️------------"

'''
👉 Agora você trabalha como se fosse CSS:

(0,0) = topo esquerdo
X → direita
Y → baixo
'''

draw_logo_image(pdf,"logo-edna-center.png",y=20,width=100,height=48,align="center")

# "------------⬆️-------- FIM DO BLOCO PARA CONTEUDO DO RELATORIO -------⬆️------------"
# =======================================================================================

pdf.save()