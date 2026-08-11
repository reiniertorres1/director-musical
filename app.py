import re
import streamlit as st
import google.generativeai as genai

APP_VERSION = "TIMBA V6 — VOZ + BANDA CONTROLADAS + JUEZ + COSTOS"

# ============================================================
# MOTOR DE TIMBA - DIRECTOR + COMPOSITOR + REVISOR + JUEZ
# ============================================================

from genres.timba.prompt_builder import (
    build_timba_band_style,
    build_timba_vocal_style,
    build_timba_director_prompt,
    build_timba_composer_prompt,
    build_timba_reviewer_prompt,
)

from genres.timba.arrangement import TOTAL_BARS

from genres.timba.quality_control import (
    validate_timba_lyrics,
    build_quality_report,
)

from genres.timba.artistic_judge import (
    build_artistic_judge_prompt,
    parse_artistic_judgment,
    evaluate_artistic_judgment,
    build_artistic_repair_report,
)


# ============================================================
# CONFIGURACION DE GEMINI
# ============================================================

MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)


# ============================================================
# PRECIOS APROXIMADOS DE GEMINI - STANDARD PAID TIER
# Actualizados: 2026-08-10
# Valores en USD por 1,000,000 de tokens.
# ============================================================

GEMINI_PRICING = {
    "gemini-2.5-flash-lite": {
        "input": 0.10,
        "output": 0.40,
    },
    "gemini-2.5-flash": {
        "input": 0.30,
        "output": 2.50,
    },
    "gemini-2.5-pro": {
        # Tarifa para prompts de hasta 200k tokens.
        "input": 1.25,
        "output": 10.00,
    },
    "gemini-2.0-flash": {
        # Modelo legado; se conserva solo como referencia.
        "input": 0.10,
        "output": 0.40,
    },
}


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

st.info(f"✅ Motor activo: {APP_VERSION}")


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
# MEDICION DE TOKENS Y COSTO
# ============================================================

def crear_contador_uso():
    return {
        "calls": 0,
        "metadata_calls": 0,
        "input_tokens": 0,
        "candidate_tokens": 0,
        "thinking_tokens": 0,
        "total_tokens": 0,
    }


def registrar_uso(response, usage):
    """Acumula los tokens reales reportados por Gemini."""

    usage["calls"] += 1

    metadata = getattr(
        response,
        "usage_metadata",
        None,
    )

    if metadata is None:
        return

    usage["metadata_calls"] += 1

    prompt_tokens = int(
        getattr(metadata, "prompt_token_count", 0) or 0
    )
    candidate_tokens = int(
        getattr(metadata, "candidates_token_count", 0) or 0
    )
    thinking_tokens = int(
        getattr(metadata, "thoughts_token_count", 0) or 0
    )
    total_tokens = int(
        getattr(metadata, "total_token_count", 0) or 0
    )

    if not total_tokens:
        total_tokens = (
            prompt_tokens
            + candidate_tokens
            + thinking_tokens
        )

    usage["input_tokens"] += prompt_tokens
    usage["candidate_tokens"] += candidate_tokens
    usage["thinking_tokens"] += thinking_tokens
    usage["total_tokens"] += total_tokens


def generar_con_uso(model, prompt, usage):
    """Genera contenido y registra automáticamente su consumo."""

    response = model.generate_content(
        prompt
    )

    registrar_uso(
        response,
        usage,
    )

    return response


def obtener_tarifa_modelo(model_name):
    nombre = model_name.lower()

    # Flash-Lite debe comprobarse antes que Flash.
    for model_key in [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
    ]:
        if model_key in nombre:
            return model_key, GEMINI_PRICING[model_key]

    return None, None


def calcular_costo_aproximado(model_name, usage):
    """
    Calcula una estimación para Standard Paid Tier.
    Los thinking tokens se cobran al precio de salida.
    """

    model_key, tarifa = obtener_tarifa_modelo(
        model_name
    )

    if tarifa is None:
        return None

    output_billable_tokens = (
        usage["candidate_tokens"]
        + usage["thinking_tokens"]
    )

    input_cost = (
        usage["input_tokens"]
        / 1_000_000
        * tarifa["input"]
    )

    output_cost = (
        output_billable_tokens
        / 1_000_000
        * tarifa["output"]
    )

    return {
        "model_key": model_key,
        "input_rate": tarifa["input"],
        "output_rate": tarifa["output"],
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": input_cost + output_cost,
        "output_billable_tokens": output_billable_tokens,
    }


def mostrar_costo_gemini(model_name, usage):
    """Muestra tokens consumidos y costo aproximado de la canción."""

    st.subheader(
        "💵 Uso y costo aproximado de Gemini"
    )

    costo = calcular_costo_aproximado(
        model_name,
        usage,
    )

    if costo is None:
        st.info(
            "Se registraron los tokens, pero no hay una tarifa "
            "configurada para el modelo seleccionado: "
            f"{model_name}"
        )
        return

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Costo estimado",
        f"${costo['total_cost']:.4f}",
    )

    col2.metric(
        "Llamadas a Gemini",
        usage["calls"],
    )

    col3.metric(
        "Tokens totales",
        f"{usage['total_tokens']:,}",
    )

    st.caption(
        "Estimación en USD usando Standard Paid Tier. "
        "Si tu proyecto está en Free Tier y permanece dentro "
        "de sus límites, el cobro real puede ser $0.00."
    )

    with st.expander(
        "Ver detalle de consumo"
    ):
        st.write(
            f"**Modelo usado:** {model_name}"
        )
        st.write(
            f"**Tokens de entrada:** {usage['input_tokens']:,}"
        )
        st.write(
            "**Tokens de respuesta visible:** "
            f"{usage['candidate_tokens']:,}"
        )
        st.write(
            "**Tokens de razonamiento (thinking):** "
            f"{usage['thinking_tokens']:,}"
        )
        st.write(
            "**Tokens de salida facturables estimados:** "
            f"{costo['output_billable_tokens']:,}"
        )
        st.write(
            "**Costo estimado de entrada:** "
            f"${costo['input_cost']:.6f}"
        )
        st.write(
            "**Costo estimado de salida + thinking:** "
            f"${costo['output_cost']:.6f}"
        )
        st.write(
            "**Tarifa usada:** "
            f"${costo['input_rate']}/1M input + "
            f"${costo['output_rate']}/1M output"
        )

        if usage["metadata_calls"] < usage["calls"]:
            st.warning(
                "Gemini no devolvió usage_metadata en todas "
                "las llamadas; el costo mostrado puede quedar "
                "por debajo del consumo real."
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
# AYUDANTES DE TIMBA
# ============================================================

def extraer_letra(texto, encabezado):
    """
    Extrae LYRICS o FINAL_LYRICS.
    Si Gemini omite el encabezado, utiliza el texto completo.
    """

    secciones = separar_secciones(
        texto,
        [encabezado],
    )

    letra = secciones.get(
        encabezado,
        "",
    )

    if letra:
        return letra.strip()

    return (
        texto
        .replace(
            f"=== {encabezado} ===",
            "",
        )
        .replace(
            f"{encabezado}:",
            "",
        )
        .strip()
    )


def limpiar_coro_corto(texto):
    """
    Extrae una sola línea utilizable del SHORT_CORO
    decidido por el Director.
    """

    lineas = [
        linea.strip()
        for linea in texto.splitlines()
        if linea.strip()
    ]

    if not lineas:
        return ""

    coro = lineas[0].strip()
    coro = coro.strip('"')
    coro = coro.strip("'")
    coro = coro.strip()

    return coro


def ejecutar_juez_artistico(
    model,
    topic,
    mood,
    director_plan,
    lyrics,
    usage,
    extra_instructions="",
):
    """
    Ejecuta el Juez Artístico y convierte su JSON
    en una evaluación procesada por Python.
    """

    judge_prompt = build_artistic_judge_prompt(
        topic=topic,
        mood=mood,
        director_plan=director_plan,
        final_lyrics=lyrics,
        extra_instructions=extra_instructions,
    )

    judge_response = generar_con_uso(
        model,
        judge_prompt,
        usage,
    )

    judge_text = judge_response.text

    judgment = parse_artistic_judgment(
        judge_text
    )

    evaluation = evaluate_artistic_judgment(
        judgment
    )

    return evaluation, judgment, judge_text


def mostrar_juez(
    artistic_evaluation,
    artistic_judgment,
    structural_validation,
    repair_attempts,
):
    """
    Muestra de forma visible el resultado del Control
    de Calidad y del Juez Artístico.
    """

    with st.expander(
        "⚖️ Ver Control de Calidad y Juez Artístico",
        expanded=True,
    ):

        # --------------------------------------------------------
        # CONTROL OBJETIVO
        # --------------------------------------------------------

        st.markdown("### Control estructural")

        if structural_validation["passed"]:
            st.success(
                "PASS — estructura y reglas objetivas correctas."
            )
        else:
            st.error(
                "FAIL — se detectaron problemas estructurales "
                "u objetivos."
            )

            for error in structural_validation["errors"]:
                st.write(
                    f"• ERROR: {error}"
                )

            for warning in structural_validation["warnings"]:
                st.write(
                    f"• WARNING: {warning}"
                )

        # --------------------------------------------------------
        # JUEZ ARTISTICO
        # --------------------------------------------------------

        st.markdown("### Juez Artístico")

        promedio = artistic_evaluation["average"]

        if artistic_evaluation["passed"]:
            st.success(
                f"PASS — promedio artístico: {promedio}/10"
            )
        else:
            st.error(
                f"FAIL — promedio artístico: {promedio}/10"
            )

        for categoria, puntuacion in artistic_evaluation[
            "scores"
        ].items():

            st.write(
                f"**{categoria.capitalize()}:** "
                f"{puntuacion}/10"
            )

        if artistic_evaluation["failed_categories"]:
            st.markdown(
                "#### Categorías reprobadas"
            )

            for categoria in artistic_evaluation[
                "failed_categories"
            ]:
                st.write(
                    f"• {categoria}"
                )

        problemas = artistic_judgment.get(
            "problems",
            [],
        )

        if problemas:
            st.markdown(
                "#### Problemas detectados"
            )

            for problema in problemas:
                categoria = problema.get(
                    "category",
                    "",
                )

                excerpt = problema.get(
                    "excerpt",
                    "",
                )

                reason = problema.get(
                    "reason",
                    "",
                )

                st.write(
                    f"• **{categoria}** — "
                    f"“{excerpt}” — {reason}"
                )

        fortalezas = artistic_judgment.get(
            "strengths",
            [],
        )

        if fortalezas:
            st.markdown(
                "#### Fortalezas"
            )

            for fortaleza in fortalezas:
                st.write(
                    f"• {fortaleza}"
                )

        instrucciones = artistic_judgment.get(
            "repair_instructions",
            [],
        )

        if instrucciones:
            st.markdown(
                "#### Instrucciones de reparación"
            )

            for instruccion in instrucciones:
                st.write(
                    f"• {instruccion}"
                )

        st.caption(
            f"Reparaciones automáticas realizadas: "
            f"{repair_attempts}"
        )


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
            model = genai.GenerativeModel(
                modelo_valido
            )

            usage_totals = crear_contador_uso()

            # ====================================================
            # TIMBA
            # ====================================================

            if seleccion == TIMBA:

                # ------------------------------------------------
                # ETAPA 1 - DIRECTOR MUSICAL
                # ------------------------------------------------

                with st.spinner(
                    "🎼 El Director Musical está "
                    "diseñando la canción..."
                ):

                    director_prompt = (
                        build_timba_director_prompt(
                            topic=tema,
                            mood=caracter,
                            extra_instructions=instrucciones_extra,
                        )
                    )

                    director_response = generar_con_uso(
                        model,
                        director_prompt,
                        usage_totals,
                    )

                    director_text = (
                        director_response.text
                    )


                # ------------------------------------------------
                # VOZ Y BANDA CONTROLADAS POR PYTHON
                # ------------------------------------------------
                #
                # Gemini ya NO resume ni reescribe estos estilos.
                # Se mantienen estables entre generaciones.

                banda = build_timba_band_style()
                voz = build_timba_vocal_style()


                director_sections = separar_secciones(
                    director_text,
                    [
                        "SONG_STRUCTURE",
                        "STORY_BLUEPRINT",
                        "MAIN_CORO_IDEA",
                        "SHORT_CORO",
                    ],
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

                coro_corto_esperado = limpiar_coro_corto(
                    coro_corto
                )


                # ------------------------------------------------
                # COMPROBAR DIRECTOR
                # ------------------------------------------------

                if not (
                    estructura
                    and historia
                    and coro_corto_esperado
                ):

                    st.warning(
                        "El Director Musical respondió, "
                        "pero no respetó completamente "
                        "el formato esperado."
                    )

                    st.subheader(
                        "Respuesta del Director"
                    )

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

                    composer_prompt = (
                        build_timba_composer_prompt(
                            topic=tema,
                            mood=caracter,
                            director_plan=director_text,
                            extra_instructions=instrucciones_extra,
                        )
                    )

                    composer_response = generar_con_uso(
                        model,
                        composer_prompt,
                        usage_totals,
                    )

                    composer_text = (
                        composer_response.text
                    )


                letra_borrador = extraer_letra(
                    composer_text,
                    "LYRICS",
                )

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
                # ETAPA 3 - REVISOR INICIAL
                # ------------------------------------------------

                with st.spinner(
                    "🔎 El Revisor está corrigiendo "
                    "y puliendo la letra..."
                ):

                    reviewer_prompt = (
                        build_timba_reviewer_prompt(
                            topic=tema,
                            mood=caracter,
                            director_plan=director_text,
                            draft_lyrics=letra_borrador,
                            extra_instructions=instrucciones_extra,
                        )
                    )

                    reviewer_response = generar_con_uso(
                        model,
                        reviewer_prompt,
                        usage_totals,
                    )

                    reviewer_text = (
                        reviewer_response.text
                    )


                letra_actual = extraer_letra(
                    reviewer_text,
                    "FINAL_LYRICS",
                )

                if not letra_actual:
                    st.warning(
                        "El Revisor no produjo "
                        "una letra final válida."
                    )

                    st.code(
                        reviewer_text,
                        language="text",
                    )

                    st.stop()


                # ------------------------------------------------
                # ETAPA 4 - CONTROL OBJETIVO + JUEZ ARTISTICO
                # ------------------------------------------------

                with st.spinner(
                    "⚖️ El Control de Calidad y el "
                    "Juez Artístico están evaluando la letra..."
                ):

                    structural_validation = (
                        validate_timba_lyrics(
                            letra_actual,
                            coro_corto_esperado,
                        )
                    )

                    (
                        artistic_evaluation,
                        artistic_judgment,
                        artistic_raw,
                    ) = ejecutar_juez_artistico(
                        model=model,
                        topic=tema,
                        mood=caracter,
                        director_plan=director_text,
                        lyrics=letra_actual,
                        usage=usage_totals,
                        extra_instructions=instrucciones_extra,
                    )


                # ------------------------------------------------
                # ETAPA 5 - REPARACIONES AUTOMATICAS
                # ------------------------------------------------

                MAX_REPAIR_ATTEMPTS = 2
                repair_attempts = 0

                while (
                    repair_attempts < MAX_REPAIR_ATTEMPTS
                    and (
                        not structural_validation["passed"]
                        or not artistic_evaluation["passed"]
                    )
                ):

                    repair_attempts += 1

                    reports = []

                    if not structural_validation["passed"]:
                        reports.append(
                            build_quality_report(
                                structural_validation
                            )
                        )

                    if not artistic_evaluation["passed"]:
                        reports.append(
                            build_artistic_repair_report(
                                artistic_evaluation
                            )
                        )

                    repair_report = (
                        "\n\n".join(reports)
                    )

                    repair_extra = (
                        instrucciones_extra.strip()
                    )

                    if repair_extra:
                        repair_extra += "\n\n"

                    repair_extra += (
                        "MANDATORY QUALITY REPAIR REPORT:\n\n"
                        + repair_report
                        + "\n\n"
                        + "This report has priority. "
                        + "Preserve the strong sections, "
                        + "but fix every listed problem."
                    )


                    with st.spinner(
                        f"🛠️ Reparación automática "
                        f"{repair_attempts} de "
                        f"{MAX_REPAIR_ATTEMPTS}..."
                    ):

                        repair_prompt = (
                            build_timba_reviewer_prompt(
                                topic=tema,
                                mood=caracter,
                                director_plan=director_text,
                                draft_lyrics=letra_actual,
                                extra_instructions=repair_extra,
                            )
                        )

                        repair_response = generar_con_uso(
                            model,
                            repair_prompt,
                            usage_totals,
                        )

                        repaired_text = (
                            repair_response.text
                        )

                        letra_reparada = extraer_letra(
                            repaired_text,
                            "FINAL_LYRICS",
                        )

                        if not letra_reparada:
                            break

                        letra_actual = letra_reparada

                        structural_validation = (
                            validate_timba_lyrics(
                                letra_actual,
                                coro_corto_esperado,
                            )
                        )

                        (
                            artistic_evaluation,
                            artistic_judgment,
                            artistic_raw,
                        ) = ejecutar_juez_artistico(
                            model=model,
                            topic=tema,
                            mood=caracter,
                            director_plan=director_text,
                            lyrics=letra_actual,
                            usage=usage_totals,
                            extra_instructions=instrucciones_extra,
                        )


                # ------------------------------------------------
                # RESULTADO FINAL
                # ------------------------------------------------

                aprobada = (
                    structural_validation["passed"]
                    and artistic_evaluation["passed"]
                )

                if aprobada:
                    st.success(
                        "✅ Timba aprobada por el Control "
                        "de Calidad y el Juez Artístico."
                    )
                else:
                    st.warning(
                        "⚠️ La canción terminó las reparaciones "
                        "automáticas, pero todavía NO alcanzó "
                        "todos los criterios de aprobación."
                    )


                # ============================================
                # BANDA
                # ============================================

                st.subheader(
                    "🎺 Banda"
                )

                st.caption(
                    "Style de banda fijo y controlado por Python; "
                    "Gemini no lo resume."
                )

                st.code(
                    banda,
                    language="text",
                )


                # ============================================
                # VOZ
                # ============================================

                st.subheader(
                    "🎤 Voz"
                )

                st.caption(
                    "Style vocal fijo y controlado por Python; "
                    "Gemini no lo resume."
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

                    st.markdown(
                        "### Estructura"
                    )

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

                    st.markdown(
                        "### Coro corto"
                    )

                    st.code(
                        coro_corto_esperado,
                        language="text",
                    )


                # ============================================
                # JUEZ ARTISTICO
                # ============================================

                mostrar_juez(
                    artistic_evaluation=artistic_evaluation,
                    artistic_judgment=artistic_judgment,
                    structural_validation=structural_validation,
                    repair_attempts=repair_attempts,
                )


                # ============================================
                # COSTO DE GEMINI
                # ============================================

                mostrar_costo_gemini(
                    model_name=modelo_valido,
                    usage=usage_totals,
                )


                # ============================================
                # LETRA FINAL
                # ============================================

                if aprobada:
                    st.subheader(
                        "📝 Letra Final — Copiar en Suno"
                    )
                else:
                    st.subheader(
                        "📝 Mejor versión obtenida — NO APROBADA"
                    )

                st.code(
                    letra_actual,
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

                    response = generar_con_uso(
                        model,
                        prompt,
                        usage_totals,
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

                    mostrar_costo_gemini(
                        model_name=modelo_valido,
                        usage=usage_totals,
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
