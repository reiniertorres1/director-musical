import re
import streamlit as st
import google.generativeai as genai

# ============================================================
# MOTOR NUEVO DE TIMBA
# ============================================================

from genres.timba.prompt_builder import build_timba_prompt
from genres.timba.arrangement import TOTAL_BARS


# ============================================================
# CONFIGURACION DE GEMINI
# ============================================================

MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)


# ============================================================
# CONFIGURACION DE LA PAGINA
# ============================================================

st.set_page_config(
    page_title="Director Musical - Suno AI",
    layout="centered"
)

st.title("🎵 Director Musical para Suno AI")

st.markdown(
    "Genera arreglos, estilos vocales y letras estructuradas "
    "para crear música en Suno."
)


# ============================================================
# PERFILES DISPONIBLES
# ============================================================

TIMBA = "Timba Cubana"
BALADA = "Balada Romántica"

perfiles_disponibles = [
    TIMBA,
    BALADA
]


# ============================================================
# PERFIL DE BALADA
#
# Lo conservamos por ahora separado del nuevo motor de Timba.
# Más adelante construiremos su propia carpeta.
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
"""
}


# ============================================================
# BUSCAR UN MODELO DISPONIBLE DE GEMINI
# ============================================================

def obtener_modelo():
    modelos = []

    for modelo in genai.list_models():

        if "generateContent" in modelo.supported_generation_methods:
            modelos.append(modelo.name)

    # Preferimos modelos Flash cuando estén disponibles.
    preferencias = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "flash",
        "pro"
    ]

    for preferencia in preferencias:

        for nombre in modelos:

            if preferencia in nombre.lower():
                return nombre

    if modelos:
        return modelos[0]

    raise RuntimeError(
        "No se encontró ningún modelo de Gemini "
        "compatible con generateContent."
    )


# ============================================================
# SEPARAR LAS PARTES PRODUCIDAS POR GEMINI
# ============================================================

def separar_secciones_timba(texto):
    """
    Busca las cuatro secciones que debe producir
    nuestro nuevo Director Musical de Timba.
    """

    texto = texto.replace("**", "")

    patron = (
        r"(?m)^\s*"
        r"(?:===\s*)?"
        r"(BAND_STYLE|VOCAL_STYLE|SONG_STRUCTURE|LYRICS)"
        r"(?:\s*===)?"
        r"\s*:?\s*$"
    )

    partes = re.split(patron, texto)

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
    perfiles_disponibles
)


# ============================================================
# CONTROLES ESPECIFICOS DE TIMBA
# ============================================================

if seleccion == TIMBA:

    st.caption(
        f"Estructura completa de Timba: "
        f"{TOTAL_BARS} compases en 4/4"
    )

    tema = st.text_input(
        "¿De qué trata la canción?",
        placeholder="Ej. Se cansó de que su pareja le siga mintiendo..."
    )

    caracter = st.selectbox(
        "Carácter de la canción:",
        [
            "Bailable y sabrosa",
            "Callejera y agresiva",
            "Romántica pero bailable",
            "Picante y divertida",
            "Dramática",
            "Despelote total"
        ]
    )

    instrucciones_extra = st.text_area(
        "Instrucciones adicionales (opcional):",
        placeholder=(
            "Ej. Quiero un coro muy pegajoso, "
            "menos metales al principio, "
            "más energía después del primer mambo..."
        )
    )


# ============================================================
# CONTROLES DE BALADA
# ============================================================

else:

    tema = st.text_input(
        "¿De qué trata la canción?",
        placeholder="Ej. Una relación que terminó demasiado tarde..."
    )

    caracter = "Romantic, elegant and emotional"

    instrucciones_extra = ""


# ============================================================
# BOTON DE GENERACION
# ============================================================

if st.button(
    "Crear Canción con IA",
    type="primary"
):

    if not tema:

        st.warning(
            "⚠️ Escribe primero de qué quieres que trate la canción."
        )

    else:

        with st.spinner(
            "El Director Musical está preparando la canción..."
        ):

            try:

                modelo_valido = obtener_modelo()

                model = genai.GenerativeModel(
                    modelo_valido
                )


                # ====================================================
                # NUEVO MOTOR DE TIMBA
                # ====================================================

                if seleccion == TIMBA:

                    prompt = build_timba_prompt(
                        topic=tema,
                        mood=caracter,
                        extra_instructions=instrucciones_extra
                    )

                    response = model.generate_content(
                        prompt
                    )

                    texto_respuesta = response.text

                    secciones = separar_secciones_timba(
                        texto_respuesta
                    )


                    # ----------------------------------------------
                    # COMPROBAR RESPUESTA
                    # ----------------------------------------------

                    banda = secciones.get(
                        "BAND_STYLE",
                        ""
                    )

                    voz = secciones.get(
                        "VOCAL_STYLE",
                        ""
                    )

                    estructura = secciones.get(
                        "SONG_STRUCTURE",
                        ""
                    )

                    letra = secciones.get(
                        "LYRICS",
                        ""
                    )


                    if banda and voz and letra:

                        st.success(
                            "¡Timba creada correctamente!"
                        )


                        # ==========================================
                        # BANDA
                        # ==========================================

                        st.subheader(
                            "🎺 Banda"
                        )

                        st.caption(
                            "Aquí aparece solamente el sonido "
                            "de la orquesta."
                        )

                        st.code(
                            banda,
                            language="text"
                        )


                        # ==========================================
                        # VOZ
                        # ==========================================

                        st.subheader(
                            "🎤 Voz"
                        )

                        st.caption(
                            "Aquí aparece solamente el cantante "
                            "y su manera de interpretar."
                        )

                        st.code(
                            voz,
                            language="text"
                        )


                        # ==========================================
                        # STYLE FINAL PARA SUNO
                        # ==========================================

                        style_final = (
                            banda.rstrip(" .")
                            + ". "
                            + voz.lstrip()
                        )

                        st.subheader(
                            "🎼 Style Final — Copiar en Suno"
                        )

                        st.caption(
                            "Este combina la banda y la voz."
                        )

                        st.code(
                            style_final,
                            language="text"
                        )


                        # ==========================================
                        # ESTRUCTURA
                        # ==========================================

                        if estructura:

                            with st.expander(
                                "📐 Ver estructura musical"
                            ):

                                st.code(
                                    estructura,
                                    language="text"
                                )


                        # ==========================================
                        # LETRA
                        # ==========================================

                        st.subheader(
                            "📝 Letra — Copiar en Suno"
                        )

                        st.code(
                            letra,
                            language="text"
                        )


                    else:

                        st.warning(
                            "Gemini respondió, pero no respetó "
                            "completamente el formato solicitado."
                        )

                        st.subheader(
                            "Respuesta completa de Gemini"
                        )

                        st.code(
                            texto_respuesta,
                            language="text"
                        )


                # ====================================================
                # BALADA - SISTEMA ANTERIOR
                # ====================================================

                else:

                    perfil = BALADA_CONFIG

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
                            1
                        )

                        style_part = partes[0].replace(
                            "STYLE_PROMPT:",
                            ""
                        ).strip()

                        letra_part = partes[1].strip()

                        st.success(
                            "¡Balada creada correctamente!"
                        )

                        st.subheader(
                            "🎼 Style Prompt — Copiar en Suno"
                        )

                        st.code(
                            style_part,
                            language="text"
                        )

                        st.subheader(
                            "📝 Letra — Copiar en Suno"
                        )

                        st.code(
                            letra_part,
                            language="text"
                        )

                    else:

                        st.warning(
                            "Gemini no devolvió el formato esperado."
                        )

                        st.code(
                            texto_respuesta,
                            language="text"
                        )


            except Exception as e:

                st.error(
                    f"Hubo un problema al conectar "
                    f"con Gemini: {e}"
                )
