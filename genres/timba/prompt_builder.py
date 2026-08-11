import json

from .arrangement import TIMBA_ARRANGEMENT, TIME_SIGNATURE, TOTAL_BARS
from .band import TIMBA_BAND
from .vocals import TIMBA_VOCALS
from .lyrics import TIMBA_LYRICS


def build_timba_prompt(
    topic,
    mood="Bailable y sabrosa",
    extra_instructions=""
):
    """
    Construye el prompt maestro para generar una Timba.

    La IA debe:
    1. Respetar la estructura musical.
    2. Mantener banda y voz separadas.
    3. Crear un style compacto para Suno.
    4. Escribir una letra limpia, natural y utilizable.
    """

    arrangement_data = json.dumps(
        TIMBA_ARRANGEMENT,
        ensure_ascii=False,
        indent=2
    )

    band_data = json.dumps(
        TIMBA_BAND,
        ensure_ascii=False,
        indent=2
    )

    vocal_data = json.dumps(
        TIMBA_VOCALS,
        ensure_ascii=False,
        indent=2
    )

    lyrics_data = json.dumps(
        TIMBA_LYRICS,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
You are the musical director, arranger and songwriter
for an ORIGINAL modern Cuban Timba production.

Your job is to follow the musical system provided below.

Do NOT imitate or reproduce any existing song,
melody, hook, lyric or signature arrangement.

The musical references contained in the configuration
describe general Cuban Timba characteristics only.

==================================================
SONG REQUEST
==================================================

TOPIC:
{topic}

CHARACTER:
{mood}

EXTRA INSTRUCTIONS:
{extra_instructions if extra_instructions else "None"}

==================================================
ARRANGEMENT
==================================================

TIME SIGNATURE:
{TIME_SIGNATURE}

TOTAL:
{TOTAL_BARS} bars

ARRANGEMENT BLUEPRINT:

{arrangement_data}

CRITICAL ARRANGEMENT RULES:

- Follow the sections in the exact requested order.
- Preserve the intended bar lengths.
- Bars represent musical duration, NOT number of lyric lines.
- Do not assume one line of lyrics equals one bar.
- Leave realistic breathing and instrumental space.
- Instrumental sections must remain instrumental.
- The arrangement must progressively build in energy.
- Do not turn every section into full-band playing.
- Respect reductions, breakdowns, mambos and full-band returns.

==================================================
BAND CONFIGURATION
==================================================

{band_data}

==================================================
VOCAL CONFIGURATION
==================================================

{vocal_data}

==================================================
LYRIC WRITING RULES
==================================================

{lyrics_data}

==================================================
IMPORTANT SUNO OUTPUT RULES
==================================================

Your output will later be copied into Suno.

Therefore:

1. BAND_STYLE must be SHORT.
   Maximum approximately 55 words.

2. VOCAL_STYLE must also be SHORT.
   Maximum approximately 40 words.

3. Do NOT write essays.

4. Do NOT explain why an instrument is being used.

5. Do NOT write phrases such as:
   "The band embodies..."
   "The percussion provides..."
   "The singer showcases..."
   "The arrangement features..."

6. Instead use concise musical descriptors.

Example of the desired BAND_STYLE density:

Modern Cuban timba, deep songo groove, syncopated electric bass,
changing piano tumbaos, tight congas and timbales, funky drum kit,
strategic brass mambos, rhythmic bloques, dynamic gear changes,
controlled breakdowns, explosive full-band returns, polished studio sound.

This example demonstrates FORMAT and DENSITY only.
Do not simply copy it.

==================================================
LYRIC QUALITY - CRITICAL
==================================================

The Spanish lyrics must sound like something a skilled
Cuban popular-music songwriter could naturally write and sing.

The lyrics must NOT sound like generic AI-generated Latin music.

STRICTLY AVOID generic filler expressions unless the story
genuinely requires them.

Avoid overusing expressions such as:

- puro sabor
- que se prenda la fiesta
- mi destino es bailar
- que suenen los tambores
- fuego
- candela
- con mi swing
- la vida sigue
- mi corazón en paz
- la verdad siempre sale
- yo sigo mi camino

Do not insert generic dance-party phrases merely because
the genre is Timba.

Every line should relate to the actual story.

==================================================
CUBAN LANGUAGE
==================================================

Use natural Cuban conversational Spanish when appropriate.

The language may contain:

- humor
- irony
- double meaning
- street intelligence
- teasing
- confidence
- conversational expressions

But do NOT fill every sentence with Cuban slang.

Do NOT create a caricature of Cuban speech.

The strongest Cuban flavor should come from:
rhythm, attitude, phrasing, wit and call-and-response.

==================================================
COROS
==================================================

Coros are extremely important.

Each coro must have:

- a clear rhythmic identity
- simple words
- strong repetition value
- direct connection to the story
- enough space for the lead singer to interact

Do not make every coro identical.

The song may develop new coros as the arrangement advances.

EXCEPTION:

During the section:

3 bars lead singer
+
1 bar short coro
x 7

the SAME short coro response must be used every time.

That response should be extremely concise and memorable.

==================================================
SONEOS
==================================================

Soneos must sound spontaneous.

Every soneo must contribute something new.

Possible functions include:

- answering the coro
- teasing the other person
- revealing another detail
- making a joke
- challenging someone
- changing perspective
- using clever everyday imagery
- increasing dramatic tension

Do NOT simply paraphrase the previous soneo.

For the seven short soneos:

- create exactly 7 different lead improvisations
- use the exact same short coro after each one
- each improvisation must fit the idea of 3 musical bars
- finish the thought before the coro enters

==================================================
INSTRUMENTAL LABELS
==================================================

This rule is CRITICAL.

Inside LYRICS:

NEVER write explanatory prose such as:

(Instrumental intro with piano and brass)
(Full band returns with maximum energy)
(Band thins out)
(Lead vocalist improvises)

Do NOT use parentheses for production explanations.

Instead, all non-sung musical instructions must be
short bracket labels.

GOOD:

[Intro - 16 bars - Songo instrumental]

[Mambo 1 - 16 bars]

[Despelote - 8 bars]

[Full Band Return - 8 bars]

[Coda - 4 bars]

BAD:

[Intro]
(Instrumental intro with strong Songo groove...)

==================================================
LYRIC FORMATTING
==================================================

Every sung phrase must appear on its own line.

Do not create paragraphs.

Do not write explanations inside the lyrics.

Do not write "Guide:" before lead-vocal lines.

Do not write commentary for the user.

Section labels must remain inside brackets.

The actual sung lyrics must be in Spanish.

Musical section labels may use short standard music terminology.

==================================================
FINAL OUTPUT FORMAT
==================================================

Return EXACTLY these four sections
and NOTHING ELSE.

Do not use Markdown bold.

Do not place triple backticks around the response.


=== BAND_STYLE ===

Write ONE compact Suno-ready description of ONLY the band.

Maximum approximately 55 words.

Include the essential:

- Cuban Timba identity
- songo/timba rhythmic foundation
- percussion
- bass
- piano
- strategic brass
- dynamic gear changes
- studio character

Do NOT describe the singer.


=== VOCAL_STYLE ===

Write ONE compact Suno-ready description of ONLY the singer.

Maximum approximately 40 words.

Describe:

- male voice
- register
- timbre
- melodic delivery
- Cuban rhythmic phrasing
- soneo character
- controlled progression of energy

Do NOT describe the band.


=== SONG_STRUCTURE ===

Give a concise ordered map of the arrangement.

Use one line per section.

Include the number of bars.

Do not add explanations or prose paragraphs.


=== LYRICS ===

Write the complete original song.

Follow the complete arrangement.

Use clean bracket labels.

Instrumental sections contain ONLY their bracket label.

Do not put prose underneath instrumental sections.

Do not use production explanations in parentheses.

Do not write bar counts as spoken lyrics.

Do not reproduce existing lyrics or recognizable hooks.

Most importantly:

Write a coherent song about the requested topic,
not a collection of generic Timba phrases.
"""

    return prompt
