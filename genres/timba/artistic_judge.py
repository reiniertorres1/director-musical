import json
import re


# ============================================================
# CONFIGURACION DEL JUEZ
# ============================================================

MINIMUM_SCORE = 7
MINIMUM_AVERAGE = 7.5

CRITICAL_CATEGORIES = [
    "naturalidad",
    "historia",
    "coros",
    "soneos",
    "cubania",
    "rimas",
    "originalidad",
    "final",
]


# ============================================================
# PROMPT DEL JUEZ ARTISTICO
# ============================================================

def build_artistic_judge_prompt(
    topic,
    mood,
    director_plan,
    final_lyrics,
    extra_instructions=""
):
    """
    El Juez NO escribe ni reescribe la canción.

    Solamente analiza la letra final y entrega
    un diagnóstico artístico estructurado.
    """

    prompt = f"""
You are the ARTISTIC QUALITY JUDGE for an original
modern Cuban Timba song.

You are NOT the songwriter.

You are NOT the arranger.

You are NOT allowed to rewrite the song.

Your only job is to judge the artistic quality
of the finished lyrics with demanding professional
standards.

==================================================
ORIGINAL REQUEST
==================================================

TOPIC:
{topic}

CHARACTER:
{mood}

EXTRA INSTRUCTIONS:
{extra_instructions if extra_instructions else "None"}

==================================================
DIRECTOR'S PLAN
==================================================

{director_plan}

==================================================
FINAL LYRICS TO JUDGE
==================================================

{final_lyrics}

==================================================
IMPORTANT
==================================================

Do not give a high score merely because the song
has the correct musical structure.

Structure is checked separately by software.

You are judging the WRITING.

A technically complete lyric can still deserve
a low artistic score.

==================================================
1. NATURALIDAD
==================================================

Judge whether the Spanish sounds like believable
spoken and sung language.

Penalize:

- AI-sounding sentences
- strange word combinations
- unnatural grammar
- phrases no real person would say
- poetry inserted only to sound lyrical
- motivational/self-help language
- sentences created mainly for rhyme

Examples of weak writing logic:

"mi cerebro procesa, mi calma es de hierro"

"la vida es una siesta"

"mis oídos ya tienen sus canciones"

"mi paciencia cambió de dirección"

Do not judge only those exact phrases.

Detect the same TYPE of artificial writing.

==================================================
2. HISTORIA
==================================================

Judge whether the lyric actually develops the
specific situation established by the Director.

Look for:

- concrete details
- progression
- cause and reaction
- consistency
- believable development

Penalize when the song abandons its story and
turns into generic declarations.

==================================================
3. COROS
==================================================

Judge whether the main coros are:

- conversational
- memorable
- rhythmically useful
- easy to repeat
- connected to the story
- suitable for call-and-response

Penalize coros that sound written only to rhyme.

Penalize generic Latin-pop slogans.

==================================================
4. SONEOS
==================================================

Judge the improvisations as Cuban Timba soneos.

They should feel spontaneous and conversational.

They should:

- interact with the story
- introduce new angles
- tease
- answer
- expose contradictions
- create humor or irony
- escalate naturally

Penalize seven variations of essentially
the same thought.

Penalize poetic filler.

==================================================
5. CUBANIA
==================================================

Judge whether the Cuban character feels natural.

Cubania should come from:

- cadence
- attitude
- picardia
- wit
- conversational rhythm
- call-and-response
- believable expressions

Do NOT reward a lyric simply for inserting:

rumba
timba
sabor
candela
Habana
clave
tumbao
gozar

In fact, penalize those words when they are used
as generic decoration instead of serving the story.

==================================================
6. RIMAS
==================================================

Judge whether rhyme sounds natural.

Penalize:

- obvious rhyme hunting
- awkward syntax for rhyme
- weak lines preserved only because they rhyme
- predictable rhyme pairs
- excessive end rhyme

A good Timba lyric does NOT need every line to rhyme.

==================================================
7. ORIGINALIDAD
==================================================

Judge whether the lyric has its own personality.

Penalize:

- generic Latin song language
- generic breakup language
- generic AI poetry
- stock phrases
- cliché metaphor families

Especially detect when one metaphor is stretched
through the entire song, such as repeatedly using:

movie
script
show
theater
novel
curtain
performance

One metaphor can be effective.

A whole song built from the same easy metaphor
becomes predictable.

==================================================
8. FINAL
==================================================

Judge the final third of the song separately.

Many AI-written lyrics begin reasonably well and
collapse near the end into generic filler.

Penalize endings that suddenly become:

- "a gozar"
- "puro sabor"
- "mi rumba"
- "la timba me llama"
- "la calle me espera"
- "la vida es bella"
- "sigo mi camino"
- generic freedom declarations
- unrelated party language

The final section should continue exploiting
the actual story and character.

==================================================
SCORING
==================================================

Give an integer score from 1 to 10 for:

naturalidad
historia
coros
soneos
cubania
rimas
originalidad
final

Use demanding standards.

5 = mediocre / clearly needs rewriting

6 = usable but noticeably weak

7 = good

8 = very good

9 = excellent

10 = exceptional and rare

Do NOT give 8-10 casually.

==================================================
PROBLEM DETECTION
==================================================

Identify the most important weak lines or sections.

For each problem include:

- category
- exact lyric excerpt
- concise explanation

Do not list trivial issues.

Focus on problems that materially reduce quality.

==================================================
REPAIR INSTRUCTIONS
==================================================

Give specific instructions for a lyric editor.

For example:

"Rewrite Soneos 4-7 because they abandon the
restaurant/concert discovery and become generic
freedom language."

NOT:

"Make the song better."

The instructions must tell the editor exactly
what needs correction while preserving strong
material.

==================================================
OUTPUT FORMAT - STRICT JSON
==================================================

Return ONLY valid JSON.

Do not use Markdown.

Do not use ```json fences.

Use exactly this structure:

{{
    "scores": {{
        "naturalidad": 1,
        "historia": 1,
        "coros": 1,
        "soneos": 1,
        "cubania": 1,
        "rimas": 1,
        "originalidad": 1,
        "final": 1
    }},
    "problems": [
        {{
            "category": "naturalidad",
            "excerpt": "exact lyric excerpt",
            "reason": "brief explanation"
        }}
    ],
    "strengths": [
        "specific strong aspect"
    ],
    "repair_instructions": [
        "specific correction instruction"
    ]
}}

Nothing else.
"""

    return prompt


# ============================================================
# LIMPIAR RESPUESTA JSON
# ============================================================

def clean_json_response(text):
    """
    Limpia posibles code fences aunque el modelo
    haya ignorado la instruccion.
    """

    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


# ============================================================
# LEER RESPUESTA DEL JUEZ
# ============================================================

def parse_artistic_judgment(text):
    """
    Convierte la respuesta JSON del Juez
    en un diccionario Python.
    """

    cleaned = clean_json_response(
        text
    )

    try:

        data = json.loads(
            cleaned
        )

    except json.JSONDecodeError as exc:

        raise ValueError(
            "El Juez Artístico no devolvió "
            "un JSON válido."
        ) from exc

    return data


# ============================================================
# VALIDAR PUNTUACIONES
# ============================================================

def evaluate_artistic_judgment(judgment):
    """
    Python decide si la letra pasa.

    No dejamos que Gemini decida por sí solo
    si su propia evaluación constituye PASS.
    """

    scores = judgment.get(
        "scores",
        {}
    )

    normalized_scores = {}

    for category in CRITICAL_CATEGORIES:

        value = scores.get(
            category
        )

        try:
            value = int(
                value
            )

        except (TypeError, ValueError):

            value = 0

        value = max(
            0,
            min(
                value,
                10
            )
        )

        normalized_scores[
            category
        ] = value


    average = (
        sum(
            normalized_scores.values()
        )
        / len(CRITICAL_CATEGORIES)
    )


    failed_categories = [
        category
        for category, score
        in normalized_scores.items()
        if score < MINIMUM_SCORE
    ]


    passed = (
        not failed_categories
        and average >= MINIMUM_AVERAGE
    )


    return {
        "passed": passed,
        "average": round(
            average,
            2
        ),
        "scores": normalized_scores,
        "failed_categories": failed_categories,
        "problems": judgment.get(
            "problems",
            []
        ),
        "strengths": judgment.get(
            "strengths",
            []
        ),
        "repair_instructions": judgment.get(
            "repair_instructions",
            []
        ),
    }


# ============================================================
# REPORTE PARA EL REVISOR
# ============================================================

def build_artistic_repair_report(
    evaluation
):
    """
    Convierte el diagnóstico del Juez en instrucciones
    que pueden ser enviadas nuevamente al Revisor.
    """

    if evaluation["passed"]:

        return "ARTISTIC QUALITY: PASS"

    lines = [
        "ARTISTIC QUALITY: FAIL",
        "",
        f"Average score: {evaluation['average']}/10",
        "",
        "SCORES:"
    ]


    for category, score in evaluation[
        "scores"
    ].items():

        lines.append(
            f"- {category}: {score}/10"
        )


    if evaluation[
        "failed_categories"
    ]:

        lines.append("")
        lines.append(
            "FAILED CATEGORIES:"
        )

        for category in evaluation[
            "failed_categories"
        ]:

            lines.append(
                f"- {category}"
            )


    if evaluation[
        "problems"
    ]:

        lines.append("")
        lines.append(
            "SPECIFIC PROBLEMS:"
        )

        for problem in evaluation[
            "problems"
        ]:

            category = problem.get(
                "category",
                "unknown"
            )

            excerpt = problem.get(
                "excerpt",
                ""
            )

            reason = problem.get(
                "reason",
                ""
            )

            lines.append(
                f"- [{category}] "
                f"'{excerpt}' -> {reason}"
            )


    if evaluation[
        "repair_instructions"
    ]:

        lines.append("")
        lines.append(
            "REQUIRED REPAIRS:"
        )

        for instruction in evaluation[
            "repair_instructions"
        ]:

            lines.append(
                f"- {instruction}"
            )


    lines.extend(
        [
            "",
            "Preserve sections that are already strong.",
            "Do not redesign the entire song unnecessarily.",
            "Correct the specific artistic weaknesses above."
        ]
    )


    return "\n".join(
        lines
    )
