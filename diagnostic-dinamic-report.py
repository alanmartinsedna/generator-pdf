from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Table, TableStyle, Spacer, Flowable
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import json

# =========================
# CARREGAR DADOS
# =========================

def load_json(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
    
data_json = load_json("data-v2.json")

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
available_doc_width = (A4[0] - (MARGIN_LEFT + MARGIN_RIGHT))
available_doc_height = (A4[1] - (MARGIN_TOP + MARGIN_BOTTOM + HEADER_BOTTOM_PADDING))
frame = Frame(
    x1=MARGIN_LEFT,
    y1=MARGIN_BOTTOM,
    width=available_doc_width,
    height=available_doc_height,
    id="main_frame",
    leftPadding=0,
    rightPadding=0,
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

# # =========================
# ESTILOS DE BADGES COM TEXTO
# =========================
class RoundedBox(Flowable):
    def __init__(
        self,
        text,
        width,
        height,
        radius=10,

        # 🎨 estilo
        background_color="#596cff",
        text_color="#FFFFFF",

        # 🔤 fonte
        font_name="Helvetica-Bold",
        font_size=10,

        # 📐 alinhamento
        align_horizontal="left",   # left | center | right
        align_vertical="middle",  # top | middle | bottom

        # 📦 padding
        padding_x=6,
        padding_y=4
    ):
        super().__init__()

        self.text = text
        self.width = width
        self.height = height
        self.radius = radius

        self.background_color = background_color
        self.text_color = text_color

        self.font_name = font_name
        self.font_size = font_size

        self.align_horizontal = align_horizontal
        self.align_vertical = align_vertical

        self.padding_x = padding_x
        self.padding_y = padding_y

    def draw(self):
        c = self.canv

        # =========================
        # BACKGROUND
        # =========================
        c.setFillColor(colors.HexColor(self.background_color))
        c.roundRect(0, 0, self.width, self.height, self.radius, fill=1, stroke=0)

        # =========================
        # TEXTO
        # =========================
        c.setFillColor(colors.HexColor(self.text_color))
        c.setFont(self.font_name, self.font_size)

        # largura do texto
        text_width = c.stringWidth(self.text, self.font_name, self.font_size)

        # -------------------------
        # ALINHAMENTO HORIZONTAL
        # -------------------------
        if self.align_horizontal == "center":
            x = ((self.width - text_width) / 2)
        elif self.align_horizontal == "right":
            x = self.width - text_width - self.padding_x
        else:  # left
            x = self.padding_x

        # -------------------------
        # ALINHAMENTO VERTICAL
        # -------------------------
        if self.align_vertical == "top":
            y = self.height - self.font_size - self.padding_y
        elif self.align_vertical == "bottom":
            y = self.padding_y
        else:  # middle
            y = (((self.height - self.font_size) / 2) + (self.font_size * 0.15))

        # -------------------------
        # DESENHO TEXTO
        # -------------------------
        c.drawString(x, y, self.text)

# =========================
# MONTA A TABELA DE PUBLICO
# =========================

def criar_tabela_publico(json_data, table_width):

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]

    # =========================
    # CONFIG DE ESTILO (BASE)
    # =========================
    HEADER_FONT_SIZE = 10
    BODY_FONT_SIZE = 8
    PADDING_TOP = 5
    PADDING_BOTTOM = 5

    # =========================
    # TRECHO 1 - ALTURA HEADER
    # =========================
    header_line_height = HEADER_FONT_SIZE + PADDING_TOP + PADDING_BOTTOM

    # =========================
    # TRECHO 2 - ALTURA BODY
    # =========================
    body_line_height = BODY_FONT_SIZE + PADDING_TOP + PADDING_BOTTOM

    # =========================
    # DADOS
    # =========================
    data = [
        [
            "Grupo",
            "Total",
            "Respondidas",
            "Não Respondidas",
            "Aderência (%)"
        ]
    ]

    for report in json_data.get("reportData", []):
        for group in report.get("public_groups", []):

            group_name = group.get("groupName", "")

            people = group.get("peopleGroup", {})
            total = people.get("totalPeople", 0)
            answered = people.get("answered", 0)
            not_answered = people.get("notAnswered", 0)

            if total > 0:
                adherence = f"{(answered / total) * 100:.2f}%"
            else:
                adherence = "0%"

            data.append([
                str(group_name),
                str(total),
                str(answered),
                str(not_answered),
                str(adherence),
            ])

    # =========================
    # LARGURA DAS COLUNAS
    # =========================
    num_cols = len(data[0])

    col_widths = [
        table_width * 0.30,
        table_width * 0.15,
        table_width * 0.15,
        table_width * 0.20,
        table_width * 0.20,
    ]

    if len(col_widths) != num_cols:
        col_widths = [table_width / num_cols] * num_cols

    # =========================
    # 🔥 ROW HEIGHTS DINÂMICO
    # =========================
    row_heights = [header_line_height] + [body_line_height] * (len(data) - 1)

    # =========================
    # CRIA TABELA
    # =========================
    table = Table(
        data,
        colWidths=col_widths,
        rowHeights=row_heights,
        repeatRows=1
    )

    # =========================
    # ESTILO
    # =========================
    '''
        ➡️ LEGENDA DE CONFIGURAÇÃO DA TABELA

        📌 COORDENADAS
            ➡️ ('COMANDO', (col_ini, row_ini), (col_fim, row_fim), valor)
            ➡️ A tabela funciona como uma matriz: (coluna, linha)
            ➡️ (0,0) = primeira célula (topo esquerdo)

        📌 ÍNDICES ESPECIAIS
            ➡️ -1 = último índice
        
        📊 EXEMPLO
            ➡️ (0, 0) → primeira coluna, primeira linha
            ➡️ (-1, 0) → última coluna, primeira linha
            ➡️ (0, -1) → primeira coluna, última linha
            ➡️ (-1, -1) → última coluna, última linha = RESULTADO ➡️ tabela inteira
    '''
    table.setStyle(TableStyle([

        # =========================
        # HEADER
        # =========================
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#596CFF")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), HEADER_FONT_SIZE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
        # =========================
        # BODY
        # =========================
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), BODY_FONT_SIZE),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#000000")),

        # =========================
        # ALINHAMENTO
        # =========================
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),

        # =========================
        # GRID
        # =========================
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor("#596CFF")),

        # =========================
        # PADDING
        # =========================
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), PADDING_TOP),
        ('BOTTOMPADDING', (0, 0), (-1, -1), PADDING_BOTTOM),

    ]))

    return table

# =========================
# CONTEÚDO DINÂMICO
# =========================

elements = []
table = criar_tabela_publico(data_json, table_width=frame._width)

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
elements.append(Spacer(1, 10))
elements.append(
    RoundedBox(
        text="Respostas entre 11/03/2026 e 19/03/2026",
        width=200,
        height=14,
        radius=7,
        background_color="#596cff",
        text_color="#FFFFFF",
        font_name="Helvetica-Bold",
        font_size=7,
        align_horizontal="left",
        align_vertical="middle",
        padding_x=20,
        padding_y=0
    )
)
elements.append(Spacer(1, 40))
elements.append(
    RoundedBox(
        text="Aderência de participação",
        width=555.27,
        height=28,
        radius=0,
        background_color="#e9ecef",
        text_color="#596CFF",
        font_name="Helvetica",
        font_size=12,
        align_horizontal="left",
        align_vertical="middle",
        padding_x=20,
        padding_y=0
    )
)
elements.append(Spacer(1, 10))
elements.append(table)



# "------------⬆️-------- FIM DO BLOCO PARA CONTEUDO DO RELATORIO -------⬆️------------"
# =======================================================================================

# =========================
# BUILD FINAL
# =========================

doc.build(elements)