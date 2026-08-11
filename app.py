import re
import streamlit as st
import google.generativeai as genai

# ============================================================
# MOTOR DE TIMBA - TRES ETAPAS
# ============================================================

from genres.timba.prompt_builder import (
    build_timba_director_prompt,
    build_timba_composer_prompt,
    build_timba_reviewer_prompt,
)
from genres.timba.arrangement import TOTAL_BARS


# ============================================================
# CONFIGURACION DE GEMINI
# ============================================================

MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)


# ============================================================
# CONFIGURACION DE PAGINA
# ============================================================

st.set_page_config(
    page_title="Director Musical - Suno AI",
    layout="centered",
)

st.title("🎵 Director Musical para Suno AI")
st.markdown(
    "Genera arreglos, estilos vocales y letras estructuradas "
    "para crear música en Suno."
)


# ============================================================
# PERFILES
# ============================================================

TIMBA = "Timba Cubana"
BALADA = "Balada Romántica"

perfiles_disponibles = [
    TIMBA,
    BALADA,
]


# ============================================================
# BALADA - SISTEMA TEMPORAL
# ============================================================

BALADA_CONFIG = {
    "base_style": (
        "1990s romantic latin pop ballad, symphonic bolero, "
        "lush orchestral strings, 90s synth pad, vintage electric piano, "
        "jazz chords, smooth fretless bass, elegant acoustic drum kit, "
        "rich male crooner, velvety chest voice, pristine studio mix, "
        "NO crowd"
    ),
    "reglas_dinamicas": (
        "Añade 2 o 3 tags en inglés que reflejen el mood de la letra. "
        "Mantén el sonido de sintetizadores de los 90s y piano eléctrico. "
        "NUNCA incluyas guitarras eléctricas ni acústicas."
    ),
    "reglas_letras": (
        "Escribe una letra romántica elegante y natural. "
        "Evita ripios, frases artificiales y rimas forzadas. "
        "No uses jerga callejera."
    ),
    "letra_template": """
[Elegant Orchestral Intro]

[Verse 1]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Pre-Chorus]
(Verso 1)
(Verso 2)

[Chorus]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Verse 2]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Chorus]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Instrumental Solo]

[Bridge]
(Verso 1)
(Verso 2)

[Final Chorus]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Outro]
""",
}


# ============================================================
# BUSCAR MODELO GEMINI
# ============================================================

def obtener_modelo():
    modelos = []

    for modelo in genai.list_models():
        if "generateContent" in modelo.supported_generation_methods:
            modelos.append(modelo.name)

    preferencias = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "flash",
        "pro",
    ]

    for preferencia in preferencias:
        for nombre in modelos:
            if preferencia in nombre.lower():
                return nombre

    if modelos:
        return modelos[0]

    raise RuntimeError(
        "No se encontró ningún modelo de Gemini compatible."
    )


# ============================================================
# SEPARADOR GENERICO DE SECCIONES
# ============================================================

def separar_secciones(texto, nombres):
    texto = texto.replace("**", "").strip()

    nombres_regex = "|".join(
        re.escape(nombre)
        for nombre in nombres
    )

    patron = (
        rf"(?m)^\s*"
        rf"(?:===\s*)?"
        rf"({nombres_regex})"
        rf"(?:\s*===)?"
        rf"\s*:?\s*$"
    )

    partes = re.split(
        patron,
        texto,
    )

    resultado = {}

    if len(partes) >= 3:
        for i in range(1, len(partes), 2):
            nombre = partes[i].strip()
            contenido = ""

            if i + 1 < len(partes):
                contenido = partes[i + 1].strip()

            resultado[nombre] = contenido

    return resultado


# ============================================================
# INTERFAZ
# ============================================================

st.subheader("Configura tu canción")

seleccion = st.selectbox(
    "Selecciona el Perfil Musical:",
    perfiles_disponibles,
)


# ============================================================
# CONTROLES DE TIMBA
# ============================================================

if seleccion == TIMBA:
    st.caption(
        f"Estructura completa de Timba: "
        f"{TOTAL_BARS} compases en 4/4"
    )

    tema = st.text_input(
        "¿De qué trata la canción?",
        placeholder=(
            "Ej. Se cansó de que su pareja "
            "le siga mintiendo..."
        ),
    )

    caracter = st.selectbox(
        "Carácter de la canción:",
        [
            "Bailable y sabrosa",
            "Callejera y agresiva",
            "Romántica pero bailable",
            "Picante y divertida",
            "Dramática",
            "Despelote total",
        ],
    )

    instrucciones_extra = st.text_area(
        "Instrucciones adicionales (opcional):",
        placeholder=(
            "Ej. Quiero un coro muy pegajoso, "
            "menos metales al principio, "
            "más energía después del primer mambo..."
        ),
    )


# ============================================================
# CONTROLES DE BALADA
# ============================================================

else:
    tema = st.text_input(
        "¿De qué trata la canción?",
        placeholder=(
            "Ej. Una relación que terminó "
            "demasiado tarde..."
        ),
    )

    caracter = "Romantic, elegant and emotional"
    instrucciones_extra = ""


# ============================================================
# BOTON DE GENERACION
# ============================================================

if st.button(
    "Crear Canción con IA",
    type="primary",
):
    if not tema:
        st.warning(
            "⚠️ Escribe primero de qué quieres "
            "que trate la canción."
        )

    else:
        try:
            modelo_valido = obtener_modelo()
            model = genai.GenerativeModel(modelo_valido)

            # ====================================================
            # TIMBA - SISTEMA DE TRES ETAPAS
            # ====================================================

            if seleccion == TIMBA:

                # ------------------------------------------------
                # ETAPA 1 - DIRECTOR MUSICAL
                # ------------------------------------------------

                with st.spinner(
                    "🎼 El Director Musical está "
                    "diseñando la canción..."
                ):
                    director_prompt = build_timba_director_prompt(
                        topic=tema,
                        mood=caracter,
                        extra_instructions=instrucciones_extra,
                    )

                    director_response = model.generate_content(
                        director_prompt
                    )

                    director_text = director_response.text

                director_sections = separar_secciones(
                    director_text,
                    [
                        "BAND_STYLE",
                        "VOCAL_STYLE",
                        "SONG_STRUCTURE",
                        "STORY_BLUEPRINT",
                        "MAIN_CORO_IDEA",
                        "SHORT_CORO",
                    ],
                )

                banda = director_sections.get(
                    "BAND_STYLE",
                    "",
                )
                voz = director_sections.get(
                    "VOCAL_STYLE",
                    "",
                )
                estructura = director_sections.get(
                    "SONG_STRUCTURE",
                    "",
                )
                historia = director_sections.get(
                    "STORY_BLUEPRINT",
                    "",
                )
                coro_principal = director_sections.get(
                    "MAIN_CORO_IDEA",
                    "",
                )
                coro_corto = director_sections.get(
                    "SHORT_CORO",
                    "",
                )

                # ------------------------------------------------
                # COMPROBAR DIRECTOR
                # ------------------------------------------------

                if not (
                    banda
                    and voz
                    and estructura
                    and historia
                    and coro_corto
                ):
                    st.warning(
                        "El Director Musical respondió, "
                        "pero no respetó completamente "
                        "el formato esperado."
                    )

                    st.subheader("Respuesta del Director")
                    st.code(
                        director_text,
                        language="text",
                    )
                    st.stop()

                # ------------------------------------------------
                # ETAPA 2 - COMPOSITOR
                # ------------------------------------------------

                with st.spinner(
                    "✍️ El Compositor está escribiendo "
                    "la letra..."
                ):
                    composer_prompt = build_timba_composer_prompt(
                        topic=tema,
                        mood=caracter,
                        director_plan=director_text,
                        extra_instructions=instrucciones_extra,
                    )

                    composer_response = model.generate_content(
                        composer_prompt
                    )

                    composer_text = composer_response.text

                composer_sections = separar_secciones(
                    composer_text,
                    [
                        "LYRICS",
                    ],
                )

                letra_borrador = composer_sections.get(
                    "LYRICS",
                    "",
                )

                # Fallback por si Gemini omite el encabezado LYRICS.
                if not letra_borrador:
                    letra_borrador = (
                        composer_text
                        .replace(
                            "=== LYRICS ===",
                            "",
                        )
                        .replace(
                            "LYRICS:",
                            "",
                        )
                        .strip()
                    )

                # ------------------------------------------------
                # COMPROBAR BORRADOR
                # ------------------------------------------------

                if not letra_borrador:
                    st.warning(
                        "El Compositor no produjo "
                        "una letra válida."
                    )
                    st.code(
                        composer_text,
                        language="text",
                    )
                    st.stop()

                # ------------------------------------------------
                # ETAPA 3 - REVISOR FINAL
                # ------------------------------------------------

                with st.spinner(
                    "🔎 El Revisor está corrigiendo "
                    "y puliendo la letra..."
                ):
                    reviewer_prompt = build_timba_reviewer_prompt(
                        topic=tema,
                        mood=caracter,
                        director_plan=director_text,
                        draft_lyrics=letra_borrador,
                        extra_instructions=instrucciones_extra,
                    )

                    reviewer_response = model.generate_content(
                        reviewer_prompt
                    )

                    reviewer_text = reviewer_response.text

                reviewer_sections = separar_secciones(
                    reviewer_text,
                    [
                        "FINAL_LYRICS",
                    ],
                )

                letra = reviewer_sections.get(
                    "FINAL_LYRICS",
                    "",
                )

                # Fallback por si Gemini omite el encabezado FINAL_LYRICS.
                if not letra:
                    letra = (
                        reviewer_text
                        .replace(
                            "=== FINAL_LYRICS ===",
                            "",
                        )
                        .replace(
                            "FINAL_LYRICS:",
                            "",
                        )
                        .strip()
                    )

                # ------------------------------------------------
                # RESULTADO
                # ------------------------------------------------

                if letra:
                    st.success(
                        "¡Timba creada correctamente!"
                    )

                    # ============================================
                    # BANDA
                    # ============================================

                    st.subheader("🎺 Banda")
                    st.caption(
                        "Solamente el sonido de la orquesta."
                    )
                    st.code(
                        banda,
                        language="text",
                    )

                    # ============================================
                    # VOZ
                    # ============================================

                    st.subheader("🎤 Voz")
                    st.caption(
                        "Solamente el cantante y "
                        "su manera de interpretar."
                    )
                    st.code(
                        voz,
                        language="text",
                    )

                    # ============================================
                    # STYLE FINAL
                    # ============================================

                    style_final = (
                        banda.rstrip(" .")
                        + ". "
                        + voz.lstrip()
                    )

                    st.subheader(
                        "🎼 Style Final — Copiar en Suno"
                    )
                    st.code(
                        style_final,
                        language="text",
                    )

                    # ============================================
                    # PLAN DEL DIRECTOR
                    # ============================================

                    with st.expander(
                        "🧠 Ver decisiones del Director Musical"
                    ):
                        st.markdown("### Estructura")
                        st.code(
                            estructura,
                            language="text",
                        )

                        st.markdown(
                            "### Plan de la historia"
                        )
                        st.code(
                            historia,
                            language="text",
                        )

                        if coro_principal:
                            st.markdown(
                                "### Idea del coro principal"
                            )
                            st.code(
                                coro_principal,
                                language="text",
                            )

                        st.markdown("### Coro corto")
                        st.code(
                            coro_corto,
                            language="text",
                        )

                    # ============================================
                    # LETRA FINAL
                    # ============================================

                    st.subheader(
                        "📝 Letra Final — Copiar en Suno"
                    )
                    st.caption(
                        "Esta es la versión revisada por "
                        "el tercer paso del motor."
                    )
                    st.code(
                        letra,
                        language="text",
                    )

                else:
                    st.warning(
                        "El Revisor no produjo "
                        "una letra final válida."
                    )
                    st.code(
                        reviewer_text,
                        language="text",
                    )

            # ====================================================
            # BALADA - SISTEMA ANTERIOR
            # ====================================================

            else:
                perfil = BALADA_CONFIG

                with st.spinner(
                    "Creando la balada..."
                ):
                    prompt = f"""
Eres un director musical, arreglista y compositor
especializado en balada romántica latina.

El usuario quiere una canción sobre:

"{tema}"

==================================================
STYLE PARA SUNO
==================================================

Estilo base:

{perfil["base_style"]}

Variaciones:

{perfil["reglas_dinamicas"]}

==================================================
LETRA
==================================================

{perfil["reglas_letras"]}

La letra debe sonar natural al cantarse.

No fuerces todas las líneas a tener exactamente
la misma cantidad de sílabas.

Cada verso debe ir en una línea independiente.

Los espacios instrumentales deben quedar solos.

No uses onomatopeyas innecesarias.

ESTRUCTURA:

{perfil["letra_template"]}

==================================================
RESPUESTA
==================================================

Devuelve solamente:

STYLE_PROMPT:

(style)

LETRA_FINAL:

(letra)
"""

                    response = model.generate_content(
                        prompt
                    )

                    texto_respuesta = response.text

                if "LETRA_FINAL:" in texto_respuesta:
                    partes = texto_respuesta.split(
                        "LETRA_FINAL:",
                        1,
                    )

                    style_part = (
                        partes[0]
                        .replace(
                            "STYLE_PROMPT:",
                            "",
                        )
                        .strip()
                    )

                    letra_part = (
                        partes[1]
                        .strip()
                    )

                    st.success(
                        "¡Balada creada correctamente!"
                    )

                    st.subheader(
                        "🎼 Style Prompt — Copiar en Suno"
                    )
                    st.code(
                        style_part,
                        language="text",
                    )

                    st.subheader(
                        "📝 Letra — Copiar en Suno"
                    )
                    st.code(
                        letra_part,
                        language="text",
                    )

                else:
                    st.warning(
                        "Gemini no devolvió "
                        "el formato esperado."
                    )
                    st.code(
                        texto_respuesta,
                        language="text",
                    )

        except Exception as e:
            st.error(
                f"Hubo un problema al conectar "
                f"con Gemini: {e}"
            )
