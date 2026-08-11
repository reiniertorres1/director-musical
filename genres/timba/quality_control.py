import re
import unicodedata


# ============================================================
# SECCIONES OBLIGATORIAS
# ============================================================

REQUIRED_SECTIONS = [
    ("Introduccion", 16),
    ("Coro inicial", 16),
    ("Voz 1", 8),
    ("Coro 2", 8),
    ("Voz 2", 8),
    ("Puente", 8),
    ("Coro 3", 8),
    ("Improvisacion y coro", 32),
    ("Mambo 1", 16),
    ("Soneo corto", 28),
    ("Mambo con coro", 16),
    ("Despelote", 8),
    ("Regreso de la banda", 8),
    ("Coro largo final", 16),
    ("Coda", 4),
]


# ============================================================
# FRASES GENERICAS QUE QUEREMOS DETECTAR
# ============================================================

GENERIC_FILLER = [
    "puro sabor",
    "mi rumba me llama",
    "me pongo a gozar",
    "a gozar",
    "la vida es pa gozar",
    "la vida es para gozar",
    "mi calle me espera",
    "mi vida sigue en ritmo",
    "mi corazon es timba",
    "el sol de la habana",
    "que suene la clave",
    "que suenen los tambores",
    "candela",
    "fuego",
    "mi alma vuela",
    "mi destino",
    "mi nueva libertad",
    "brindo por mi sosiego",
    "me bajo de este barco",
]


# ============================================================
# NORMALIZACION
# ============================================================

def normalize_text(text):
    """
    Convierte texto a una forma simple para comparaciones.
    Quita acentos y pasa todo a minusculas.
    """

    text = text.lower().strip()

    text = unicodedata.normalize(
        "NFD",
        text
    )

    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    return text


# ============================================================
# EXTRAER ETIQUETAS
# ============================================================

def extract_labels(lyrics):
    """
    Extrae todas las etiquetas entre corchetes.
    """

    return re.findall(
        r"\[([^\]]+)\]",
        lyrics
    )


# ============================================================
# COMPROBAR ESTRUCTURA
# ============================================================

def check_required_sections(lyrics):
    errors = []

    labels = [
        normalize_text(label)
        for label in extract_labels(lyrics)
    ]

    for section_name, bars in REQUIRED_SECTIONS:

        expected_name = normalize_text(
            section_name
        )

        matching_labels = [
            label
            for label in labels
            if expected_name in label
        ]

        if not matching_labels:

            errors.append(
                f"Falta la sección obligatoria: "
                f"{section_name} ({bars} bars)."
            )

            continue

        # Comprobar que al menos una etiqueta
        # tenga el número correcto de compases.

        correct_bar_count = any(
            re.search(
                rf"\b{bars}\s*bars?\b",
                label
            )
            for label in matching_labels
        )

        if not correct_bar_count:

            errors.append(
                f"La sección '{section_name}' "
                f"debe indicar {bars} bars."
            )

    return errors


# ============================================================
# COMPROBAR 7 SONEOS CORTOS
# ============================================================

def check_short_soneos(lyrics):
    errors = []

    normalized = normalize_text(
        lyrics
    )

    for number in range(1, 8):

        pattern = (
            rf"\[soneo\s*{number}"
            rf"\s*-\s*3\s*bars?\]"
        )

        if not re.search(
            pattern,
            normalized
        ):

            errors.append(
                f"Falta [Soneo {number} - 3 bars]."
            )

    return errors


# ============================================================
# EXTRAER RESPUESTAS DE CORO CORTO
# ============================================================

def extract_short_coro_responses(lyrics):
    """
    Busca cada:

    [Coro Corto - 1 bar]
    respuesta

    y devuelve las respuestas encontradas.
    """

    pattern = (
        r"\[Coro\s+Corto\s*-\s*1\s*bar\]"
        r"\s*\n+"
        r"([^\n\[]+)"
    )

    matches = re.findall(
        pattern,
        lyrics,
        flags=re.IGNORECASE
    )

    return [
        match.strip()
        for match in matches
    ]


# ============================================================
# COMPROBAR CORO CORTO
# ============================================================

def check_short_coro(
    lyrics,
    expected_short_coro
):
    errors = []

    responses = (
        extract_short_coro_responses(
            lyrics
        )
    )

    if len(responses) != 7:

        errors.append(
            "La sección de soneos cortos debe "
            f"tener exactamente 7 respuestas de "
            f"Coro Corto. Se encontraron {len(responses)}."
        )

        return errors

    expected = normalize_text(
        expected_short_coro
    )

    for index, response in enumerate(
        responses,
        start=1
    ):

        actual = normalize_text(
            response
        )

        if actual != expected:

            errors.append(
                f"Coro Corto #{index} incorrecto. "
                f"Esperado: '{expected_short_coro}' | "
                f"Encontrado: '{response}'"
            )

    return errors


# ============================================================
# DETECTAR RELLENO GENERICO
# ============================================================

def check_generic_filler(lyrics):
    warnings = []

    normalized = normalize_text(
        lyrics
    )

    for phrase in GENERIC_FILLER:

        normalized_phrase = (
            normalize_text(
                phrase
            )
        )

        if normalized_phrase in normalized:

            warnings.append(
                f"Frase genérica detectada: "
                f"'{phrase}'"
            )

    return warnings


# ============================================================
# COMPROBAR FORMATO PROHIBIDO
# ============================================================

def check_bad_formatting(lyrics):
    errors = []

    forbidden_patterns = [
        r"\(cantante",
        r"\(coro",
        r"\(guia",
        r"\(instrumental",
        r"\(full band",
        r"\(band ",
    ]

    normalized = normalize_text(
        lyrics
    )

    for pattern in forbidden_patterns:

        if re.search(
            pattern,
            normalized
        ):

            errors.append(
                "Se detectaron instrucciones "
                "musicales en paréntesis."
            )

            break

    return errors


# ============================================================
# CONTROL COMPLETO
# ============================================================

def validate_timba_lyrics(
    lyrics,
    expected_short_coro
):
    """
    Ejecuta todas las comprobaciones objetivas.

    Devuelve un diccionario:

    {
        "passed": True/False,
        "errors": [...],
        "warnings": [...]
    }
    """

    errors = []
    warnings = []

    errors.extend(
        check_required_sections(
            lyrics
        )
    )

    errors.extend(
        check_short_soneos(
            lyrics
        )
    )

    errors.extend(
        check_short_coro(
            lyrics,
            expected_short_coro
        )
    )

    errors.extend(
        check_bad_formatting(
            lyrics
        )
    )

    warnings.extend(
        check_generic_filler(
            lyrics
        )
    )

    passed = (
        len(errors) == 0
        and len(warnings) == 0
    )

    return {
        "passed": passed,
        "errors": errors,
        "warnings": warnings,
    }


# ============================================================
# CREAR REPORTE PARA EL REVISOR
# ============================================================

def build_quality_report(
    validation_result
):
    """
    Convierte los errores encontrados en instrucciones
    claras para que el Revisor pueda corregirlos.
    """

    if validation_result["passed"]:

        return "PASS"

    lines = [
        "QUALITY CONTROL: FAIL",
        "",
        "The following problems must be corrected:",
        ""
    ]

    for error in validation_result["errors"]:

        lines.append(
            f"- ERROR: {error}"
        )

    for warning in validation_result["warnings"]:

        lines.append(
            f"- WARNING: {warning}"
        )

    lines.extend(
        [
            "",
            "Correct these problems without "
            "rewriting parts that are already strong."
        ]
    )

    return "\n".join(
        lines
    )
