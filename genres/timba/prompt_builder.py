import json

from .arrangement import TIMBA_ARRANGEMENT, TIME_SIGNATURE, TOTAL_BARS
from .band import TIMBA_BAND
from .vocals import TIMBA_VOCALS
from .lyrics import TIMBA_LYRICS


def build_timba_prompt(
    topic,
    mood="Energetic",
    extra_instructions=""
):
    """
    Construye las instrucciones completas que recibira la IA
    para componer una Timba.

    Todavia NO llama a Gemini.
    Solamente prepara correctamente toda la informacion.
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
for an original Cuban Timba production.

Your job is NOT to freely invent the musical format.

You must follow the provided arrangement, band,
vocal and lyric specifications.

==================================================
SONG REQUEST
==================================================

TOPIC:
{topic}

MOOD:
{mood}

EXTRA INSTRUCTIONS:
{extra_instructions if extra_instructions else "None"}

==================================================
MUSICAL STRUCTURE
==================================================

TIME SIGNATURE:
{TIME_SIGNATURE}

TOTAL ARRANGEMENT:
{TOTAL_BARS} bars

ARRANGEMENT BLUEPRINT:

{arrangement_data}

IMPORTANT:

The number of bars is musical duration.

Do NOT automatically interpret one written lyric
line as one musical bar.

Respect the order and function of every section.

==================================================
BAND
==================================================

{band_data}

==================================================
LEAD VOCAL
==================================================

{vocal_data}

==================================================
LYRIC COMPOSITION
==================================================

{lyrics_data}

==================================================
FINAL TASK
==================================================

Create one completely original Cuban Timba song
based on all specifications above.

You must produce FOUR clearly separated sections:

=== BAND_STYLE ===

Describe ONLY the instrumental band and production.

Do not describe the singer here.

Keep this section concise and useful for a
music-generation model.


=== VOCAL_STYLE ===

Describe ONLY the desired lead singer,
vocal character, phrasing and performance.

Do not describe the instrumental arrangement here.


=== SONG_STRUCTURE ===

Give the complete ordered musical structure.

Clearly identify:

- instrumental sections
- lead vocal sections
- coros
- soneos
- mambos
- despelote
- full-band returns
- coda

Preserve the specified number of bars.


=== LYRICS ===

Write the complete original Spanish lyrics.

Clearly label musical sections using brackets,
for example:

[Intro]
[Coro]
[Voz]
[Puente]
[Soneo]
[Mambo]
[Despelote]
[Coda]

Instrumental instructions must remain inside brackets.

Do not put production explanations inside sung lyrics.

The short coro used during the
3-bar soneo + 1-bar coro section
must remain the SAME every time.

The individual soneos must be different.

The lyrics must tell a coherent story and sound
natural when sung in Cuban Timba.

Do not imitate or reproduce any existing song.
"""

    return prompt
