from reportlab.platypus import BaseDocTemplate, Frame, Indenter, PageTemplate, Paragraph, Table, TableStyle, Spacer, Flowable, ListFlowable, ListItem
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
    
# data_json = load_json("data-v2.json")
data_json = load_json("data-cenario-01.json")

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
# FUNÇÃO CALCULO MEDIA GERAL DE ADERENCIA
# =========================

def calc_global_adherence_average(json_data):
    total_people_sum = 0
    total_answered_sum = 0

    for report in json_data.get("reportData", []):
        public_groups = report.get("public_groups", [])
        for group in public_groups:
            people = group.get("peopleGroup", {})
            total = people.get("totalPeople", 0)
            answered = people.get("answered", 0)
            total_people_sum += total
            total_answered_sum += answered

    if total_people_sum == 0:
        raise Exception("Erro: total de pessoas é zero.")

    global_adherence = (total_answered_sum / total_people_sum) * 100
    formated_adherence = f"Média geral da aderência de participação {global_adherence:.2f}%"
    return formated_adherence

# =========================
# FUNÇÃO CALCULO MEDIA GERAL DO DIAGNOSTICO
# =========================

def calc_global_diagnostic_average(json_data):
    total_avarage_sum = 0

    for report in json_data.get("reportData", []):
        public_groups = report.get("public_groups", [])
        quantity_groups = len(public_groups)
        for group in public_groups:
            people = group.get("peopleGroup", {})
            total_avarage_group = people.get("avarageGroup", 0)
            total_avarage_sum += total_avarage_group

    if quantity_groups < 0:
        raise Exception("Erro: total de GRUPOS é MENOR OU IGUAL a zero.")
    
    total_avarage_result = ((total_avarage_sum / quantity_groups) * 100)

    formated_total_avarage_result = f'{total_avarage_result:.1f}%'

    return total_avarage_result, formated_total_avarage_result

# =============================================
# FUNÇÃO QUE MONTA O CARD FINAL DO DIAGNOSTICO
# =============================================
class ScoreCard(Flowable):
    def __init__(self, value, value_str, width=130, height=80):
        super().__init__()

        self.value = value
        self.value_str = value_str
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        # 🔥 ISSO AQUI É O SEGREDO
        return self.width, self.height

    def draw(self):
        c = self.canv

        # =========================
        # LÓGICA DE COR
        # =========================
        if self.value > 100:
            raise Exception("Erro: percentual acima de 100%")
        elif 0 <= self.value <= 20:
            bg = "#2f6e2d"
            label = "Excelente"
        elif self.value <= 40:
            bg = "#c3dfa5"
            label = "Bom"
        elif self.value <= 60:
            bg = "#ffd656"
            label = "Razoável"
        elif self.value <= 80:
            bg = "#f4b184"
            label = "Ruim"
        elif self.value <= 100:
            bg = "#ee3650"
            label = "Muito Ruim"
        else:
            bg = "#adadad"
            label = "n/d"

        bg_color = colors.HexColor(bg)

        # =========================
        # FUNDO
        # =========================
        c.setFillColor(bg_color)
        c.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)

        # =========================
        # CENTRO
        # =========================
        cx = self.width / 2
        cy = self.height / 2

        # círculo
        c.setFillColor(colors.white)

        circle_radius = 20
        circle_x_position = cx
        circle_y_position = cy + 8

        c.circle(circle_x_position, circle_y_position, circle_radius, stroke=0, fill=1)

        # =========================
        # TEXTO VALOR
        # =========================
        c.setFillColor(bg_color)
        c.setFont("Helvetica-Bold", 11)
        text_width = c.stringWidth(self.value_str, "Helvetica-Bold", 11)

        text_value_x_position = cx - (text_width / 2)
        text_value_y_position = cy + 4

        c.drawString(text_value_x_position, text_value_y_position, self.value_str)

        # =========================
        # TEXTO LABEL
        # =========================
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11)
        label_width = c.stringWidth(label, "Helvetica-Bold", 11)

        text_label_x_position = cx - label_width / 2
        text_label_y_position = cy - 27

        c.drawString(text_label_x_position, text_label_y_position, label)

# =============================================
# FUNÇÃO CALCULA MÉDIA DOS GRUPOS DE PERGUNTAS
# =============================================

def calc_global_average_question_group(json_data):

    # Dicionário acumulador dinâmico
    # Estrutura:
    # {
    #     "Nome do Grupo 1": soma_total,
    #     "Nome do Grupo 2": soma_total,
    # }
    group_totals = {}

    quantity_public_groups = 0

    # =========================
    # PERCORRE REPORTS
    # =========================
    for report in json_data.get("reportData", []):

        public_groups = report.get("public_groups", [])

        # Conta total de grupos de público
        quantity_public_groups += len(public_groups)

        # =========================
        # PERCORRE GRUPOS DE PÚBLICO
        # =========================
        for public_group_item in public_groups:

            answers_group_list = public_group_item.get("answersGroupName", [])

            # =========================
            # PERCORRE GRUPOS DE PERGUNTAS (DINÂMICO)
            # =========================
            for question_group in answers_group_list:
                group_name = question_group.get("groupNameAnswer", "Sem Nome")
                final_average = question_group.get("finalAverage", 0)

                # Soma acumulada por nome do grupo
                if group_name not in group_totals:
                    group_totals[group_name] = 0

                group_totals[group_name] += final_average

    # =========================
    # VALIDAÇÃO
    # =========================
    if quantity_public_groups <= 0:
        raise Exception(
            "Erro: Não existem grupos de público para calcular a média."
        )

    # =========================
    # CALCULA MÉDIA FINAL
    # =========================
    result_list = []

    for group_name, total_sum in group_totals.items():
        average = total_sum / quantity_public_groups
        formated_average = ( average * 100 )
        result_list.append({
            "groupNameAnswer": group_name,
            "totalValueAverage": formated_average
        })

    return result_list

# ===============================================
# CONFIGURAÇÃO DE ESTILO DE TEXTO BASEADO NO HTML
# ===============================================
# =========================
# TAGS DE BLOCO
# =========================
settings_style_map = {

    # =========================
    # HEADINGS
    # =========================

    "h1": ParagraphStyle(
        name="H1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28.8,
        spaceAfter=12,
        spaceBefore=6,
    ),
    "h2": ParagraphStyle(
        name="H2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=21.6,
        spaceAfter=9,
        spaceBefore=6,
    ),
    "h3": ParagraphStyle(
        name="H3",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16.8,
        spaceAfter=7,
        spaceBefore=5,
    ),
    "h4": ParagraphStyle(
        name="H4",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=14.4,
        spaceAfter=6,
        spaceBefore=4,
    ),
    "h5": ParagraphStyle(
        name="H5",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        spaceAfter=5,
        spaceBefore=4,
    ),
    "h6": ParagraphStyle(
        name="H6",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=10.8,
        spaceAfter=4,
        spaceBefore=3,
    ),
    "p": ParagraphStyle(
        name="P",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=14.4,
        spaceAfter=6,
    ),
    "blockquote": ParagraphStyle(
        name="BLOCKQUOTE",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=12,
        leading=14.4,
        leftIndent=20,
        textColor=colors.grey,
        spaceAfter=6,
        spaceBefore=6,
    ),
    "address": ParagraphStyle(
        name="ADDRESS",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=12,
        leading=14.4,
        spaceAfter=6,
    )
}

# =========================
# TAGS PARA LISTAS
# =========================

settings_list_map = {

    "ul": {
        "bulletType": "bullet",
        "leftIndent": 10,
        "bulletFontName": "Helvetica",
        "bulletFontSize": 12,
    },
    "ol": {
        "bulletType": "1",  # numerada
        "leftIndent": 10,
        "bulletFontName": "Helvetica",
        "bulletFontSize": 12,
    },
    "li_style": ParagraphStyle(
        name="LI",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=14.4,
        spaceAfter=3,
    )
}

# =========================
# FUNCAO BUSCA RECOMENDAÇÃO
# =========================
def get_recommendation_by_score(data_json, average_questions_groups_list):

    result_recommendation_list = []
    data_recommendation_list = data_json.get("dataRecommendation", [])

    for average_group_item in average_questions_groups_list:

        group_name_answer = average_group_item.get("groupNameAnswer")
        group_average = average_group_item.get("totalValueAverage")

        if group_name_answer is None or group_average is None:
            continue

        for recommendation_group in data_recommendation_list:

            label_group = recommendation_group.get("label")

            # Verifica se o label corresponde ao nome do grupo
            if not label_group:
                continue

            if label_group.strip().upper() == group_name_answer.strip().upper():

                meta = recommendation_group.get("meta", {})
                recommendations_list = meta.get("recommendations", [])

                for recommendation_item in recommendations_list:

                    start_value = recommendation_item.get("start")
                    end_value = recommendation_item.get("end")

                    if start_value is None or end_value is None:
                        continue

                    if start_value <= group_average <= end_value:

                        result_recommendation_list.append({
                            "label": label_group,
                            "concept": recommendation_item.get("concept"),
                            "recommendations": recommendation_item.get("recommendations")
                        })

                        break  # encontrou a recomendação correta

                break  # encontrou o agrupador correto

    return result_recommendation_list

# =========================
# FUNÇÃO DE LIMPEZA DE HTML E FORMATAÇÃO DE TEXTO
# =========================

def build_flowables_from_html(html_content, settings_style_map, settings_list_map):

    from reportlab.platypus import Paragraph, Spacer, ListFlowable, ListItem
    from reportlab.lib.units import cm
    import html as html_lib
    import re

    flowables = []

    if not html_content:
        return flowables

    # =====================================================
    # 1️⃣ Decode entidades HTML (&Aacute; etc)
    # =====================================================
    html_content = html_lib.unescape(html_content)

    # =====================================================
    # 2️⃣ Remove quebras de linha desnecessárias
    # =====================================================
    html_content = html_content.replace("\n", "")

    # =====================================================
    # 3️⃣ Remove TODOS atributos de QUALQUER tag
    # =====================================================
    html_content = re.sub(r'<(\w+)(\s+[^>]+)>', r'<\1>', html_content)

    # =====================================================
    # 4️⃣ Converte strong → b (mais seguro no ReportLab)
    # =====================================================
    html_content = re.sub(r'<strong>', '<b>', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'</strong>', '</b>', html_content, flags=re.IGNORECASE)

    # =====================================================
    # 5️⃣ Remove COMPLETAMENTE spans (não servem no ReportLab)
    # =====================================================
    html_content = re.sub(r'</?span>', '', html_content, flags=re.IGNORECASE)

    # =====================================================
    # 6️⃣ Remove <p> aninhado
    # =====================================================
    html_content = re.sub(r'<p>\s*<p>', '<p>', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'</p>\s*</p>', '</p>', html_content, flags=re.IGNORECASE)

    # =====================================================
    # 7️⃣ Regex para blocos principais
    # =====================================================
    block_pattern = re.compile(
        r'<(p|h1|h2|h3|h4|h5|h6|ul|ol|blockquote|address)>(.*?)</\1>',
        re.IGNORECASE | re.DOTALL
    )

    blocks = block_pattern.findall(html_content)

    for tag_name, inner_html in blocks:

        tag_name = tag_name.lower().strip()
        inner_html = inner_html.strip()

        if not inner_html:
            continue

        # =====================================================
        # LISTAS
        # =====================================================
        if tag_name in ["ul", "ol"]:

            li_pattern = re.compile(
                r'<li>(.*?)</li>',
                re.IGNORECASE | re.DOTALL
            )

            li_items = li_pattern.findall(inner_html)
            list_items = []

            for li_html in li_items:

                li_html = li_html.strip()

                if not li_html:
                    continue

                li_paragraph = Paragraph(
                    li_html,
                    settings_list_map["li_style"]
                )

                list_items.append(ListItem(li_paragraph))

            if list_items:

                list_config = settings_list_map.get(tag_name, {})

                LIST_MARGIM_LEFT = 15

                flowables.append(
                    Indenter(left=LIST_MARGIM_LEFT)   # empurra todo o bloco da lista, inclusive bullets
                )

                flowables.append(
                    ListFlowable(
                        list_items,
                        bulletType=list_config.get("bulletType", "bullet"),
                        leftIndent=list_config.get("leftIndent", 10),
                        bulletFontName=list_config.get("bulletFontName", "Helvetica"),
                        bulletFontSize=list_config.get("bulletFontSize", 12),
                    )
                )

                flowables.append(
                    Indenter(left= -LIST_MARGIM_LEFT)  # volta o contexto após a lista
                )

                flowables.append(Spacer(1, 0.3 * cm))

        # =====================================================
        # BLOCOS NORMAIS
        # =====================================================
        else:

            style = settings_style_map.get(tag_name, settings_style_map["p"])

            flowables.append(
                Paragraph(inner_html, style)
            )

            flowables.append(Spacer(1, 0.2 * cm))

    return flowables


# =========================
# CONTEÚDO DINÂMICO
# =========================

elements = []
table = criar_tabela_publico(data_json, table_width=frame._width)
total_global_avarage_diagnostic_main = calc_global_diagnostic_average(data_json)
total_global_avarage_diagnostic_number = total_global_avarage_diagnostic_main[0]
total_global_avarage_diagnostic_str = total_global_avarage_diagnostic_main[1]

# calc_global_average_question_group(data_json)

# get_recommendation_by_score(data_json, calc_global_average_question_group(data_json))
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
elements.append(Spacer(1, 20))
elements.append(
    Paragraph(
        calc_global_adherence_average(data_json),
        ParagraphStyle(
            name="Custom",
            fontName="Helvetica-Bold",  # weight 400
            fontSize=16,
            textColor=colors.HexColor('#596CFF'),
            alignment=0  # left
        )
    )
)
elements.append(Spacer(1, 20))
elements.append(
    Table(
        [[ScoreCard(total_global_avarage_diagnostic_number, total_global_avarage_diagnostic_str)]],
        colWidths=[A4[0] - (MARGIN_LEFT + MARGIN_RIGHT)],
        style=[
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]
    )
)
elements.append(Spacer(1, 20))
result_recommendation_list = get_recommendation_by_score(
    data_json,
    calc_global_average_question_group(data_json)
)

for item in result_recommendation_list:

    # 1️⃣ Nome do grupo (label)
    elements.append(
        Paragraph(item["label"], settings_style_map["h2"])
    )
    elements.append(Spacer(1, 10))

    # 2️⃣ Título da recomendação (concept)
    elements.append(
        Paragraph(item["concept"], settings_style_map["h3"])
    )
    elements.append(Spacer(1, 10))

    # 3️⃣ Texto HTML da recomendação
    html_content = item["recommendations"]

    # Aqui você chama SUA FUNÇÃO que limpa e converte HTML
    flowables = build_flowables_from_html(
        html_content,
        settings_style_map,
        settings_list_map
    )

    for flowable in flowables:
        elements.append(flowable)

    elements.append(Spacer(1, 10))

elements.append(Spacer(1, 40))


# "------------⬆️-------- FIM DO BLOCO PARA CONTEUDO DO RELATORIO -------⬆️------------"
# =======================================================================================

# =========================
# BUILD FINAL
# =========================

doc.build(elements)