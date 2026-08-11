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
    # ============================================================
# NUEVO SISTEMA DE DOS ETAPAS
# ============================================================


def build_timba_director_prompt(
    topic,
    mood="Bailable y sabrosa",
    extra_instructions=""
):
    """
    ETAPA 1:
    El Director Musical diseña la canción.

    No escribe todavía la letra completa.
    Decide banda, voz, estructura narrativa,
    coros y estrategia musical.
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

    prompt = f"""
You are the MUSICAL DIRECTOR and ARRANGER
of an original modern Cuban Timba production.

You are NOT writing the complete lyrics yet.

Your job is to design the song so that another
specialized songwriter can write the lyrics afterward.

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

{arrangement_data}

==================================================
BAND
==================================================

{band_data}

==================================================
VOICE
==================================================

{vocal_data}

==================================================
YOUR JOB
==================================================

Create the musical and lyrical BLUEPRINT.

Do NOT write the full song.

The blueprint must solve these things BEFORE
the songwriter starts writing:

1. What is the exact dramatic idea of the song?

2. How does the story progress from beginning
   to end?

3. What should Verse 1 accomplish?

4. What should Verse 2 accomplish?

5. What is the function of the bridge?

6. What happens emotionally when the montuno begins?

7. What should the singer talk about during
   the soneos?

8. What should happen during the final coro?

9. Create the MAIN CORO concept.

10. Create the SHORT CORO used during:
    3 bars singer + 1 bar coro x 7.

The short coro must be extremely concise.

==================================================
IMPORTANT LYRIC STRATEGY
==================================================

Before creating any coro or hook, first turn the
user's topic into a SPECIFIC HUMAN SITUATION.

Do not work only with abstract ideas such as:
"betrayal", "lies", "moving on" or "jealousy".

Create believable concrete circumstances that give
the songwriter something real to talk about.

For example, depending on the user's topic:

- something the other person said
- an excuse that does not add up
- a message, call or detail that exposed the truth
- a repeated behavior the singer finally recognizes
- a contradiction in the other person's story
- a specific everyday moment
- a funny or ironic reaction to what happened

Do NOT make the situation melodramatic unless the
user specifically requests drama.

The song should feel as if something actually
happened between real people.

==================================================
CHARACTER POINT OF VIEW
==================================================

Define clearly how the main character reacts.

Possible attitudes include:

- amused
- sarcastic
- confident
- annoyed
- teasing
- indifferent
- surprised
- provocative
- calmly dismissive

Do not automatically make the singer heartbroken.

For a playful or danceable Timba, prefer confidence,
wit and picardia over suffering.

==================================================
CONVERSATIONAL WRITING
==================================================

The central hooks should sound like phrases that
a real person could actually SAY to another person.

Prefer spoken, direct expressions over poetic lines.

GOOD TYPE OF THINKING:

"Ahora cuentame otra"
"Esa ya me la se"
"Conmigo ese cuento no"
"Eso no te lo crees ni tu"
"Te cogieron fuera de base"

These are examples of NATURAL DIRECTION only.
Do not automatically reuse them.

BAD TYPE OF THINKING:

"Tu verdad se desarmo, mi sonrisa florecio"
"Mis ojos despertaron al jardin de tu mentira"
"Mi destino renacio cuando tu amor termino"

Do not write poetic sentences merely to create rhyme.

==================================================
RHYME RULE
==================================================

NEVER choose a weaker phrase just because it rhymes.

Natural speech, rhythm, attitude and memorability
are more important than perfect rhyme.

A coro does NOT need every line to rhyme.

Avoid obvious paired rhymes created only for effect.

==================================================
CUBAN CHARACTER
==================================================

The Cuban personality should come primarily from:

- conversational rhythm
- wit
- irony
- picardia
- double meaning
- everyday observations
- clever answers
- believable reactions
- call-and-response potential

Do not force Cuban slang into every sentence.

Do not turn the singer into a caricature.

Avoid generic Latin-music filler such as:

- puro sabor
- que se prenda la fiesta
- mi destino es bailar
- fuego
- candela
- sigue tu camino
- la vida sigue
- que suenen los tambores
- mi corazon es timba
- este sabor cubano

==================================================
CORO CREATION PROCESS
==================================================

Do NOT start by trying to rhyme.

First ask:

"What is the strongest thing this character could
say directly to the other person?"

Then convert that thought into a short,
rhythmically memorable coro.

The MAIN CORO should feel like a phrase people
could remember after hearing it once.

The SHORT CORO should be even simpler.

For the 1-bar response section, favor approximately
2 to 6 spoken words whenever musically possible.

==================================================
DIRECTOR LANGUAGE
==================================================

Write the following sections entirely in SPANISH:

STORY_BLUEPRINT
MAIN_CORO_IDEA
SHORT_CORO

The songwriter will later compose the complete
Spanish lyric from this material.

Do not mentally translate English poetic ideas
into Spanish afterward.

Think about the story and hooks directly in Spanish.

==================================================
STORY SPECIFICITY
==================================================

STORY_BLUEPRINT must include:

SITUACION CONCRETA:
What specifically happened.

ACTITUD DEL PERSONAJE:
How the singer reacts.

VOZ 1:
What new information is revealed.

VOZ 2:
How the situation develops.

PUENTE:
What changes emotionally or narratively.

MONTUNO / IMPROVISACION:
What material the singer can play with.

SONEOS CORTOS:
At least 7 different conversational angles or
details that can later inspire the seven soneos.

FINAL:
What attitude or conclusion closes the story.

Give the songwriter concrete material.

Do not write the complete lyrics yet.

==================================================
BAND STYLE
==================================================

Write one compact Suno-ready BAND description.

Maximum about 55 words.

No singer description.

No essays.

==================================================
VOCAL STYLE
==================================================

Write one compact Suno-ready VOCAL description.

Maximum about 40 words.

No band description.

==================================================
OUTPUT FORMAT
==================================================

Return EXACTLY these sections:

=== BAND_STYLE ===

=== VOCAL_STYLE ===

=== SONG_STRUCTURE ===

=== STORY_BLUEPRINT ===

=== MAIN_CORO_IDEA ===

=== SHORT_CORO ===

Nothing else.


SONG_STRUCTURE:

Use one line for every arrangement section
and include the number of bars.


STORY_BLUEPRINT:

Explain concisely what lyrical job each major
vocal section must accomplish.

Do not write full verses.


MAIN_CORO_IDEA:

Give the central hook idea and optionally
2 or 3 candidate hook phrases.

Do NOT write an entire song.


SHORT_CORO:

Write exactly ONE short Spanish coro response.

It must be suitable for the recurring
1-bar coro section.

Keep it concise, rhythmic and memorable.
"""

    return prompt



def build_timba_composer_prompt(
    topic,
    mood,
    director_plan,
    extra_instructions=""
):
    """
    ETAPA 2:
    El Compositor recibe las decisiones
    del Director Musical y escribe la letra.
    """

    arrangement_data = json.dumps(
        TIMBA_ARRANGEMENT,
        ensure_ascii=False,
        indent=2
    )

    lyrics_data = json.dumps(
        TIMBA_LYRICS,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
You are now the SONGWRITER.

A separate musical director has already designed
the song.

Your job is NOT to redesign it.

Your job is to write an excellent original
Spanish lyric that follows the director's plan.

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
DIRECTOR'S BLUEPRINT
==================================================

{director_plan}

==================================================
ARRANGEMENT
==================================================

{arrangement_data}

==================================================
LYRIC RULES
==================================================

{lyrics_data}

==================================================
CRITICAL RULE
==================================================

Follow the Director's dramatic plan.

Do not replace the central idea with generic
Timba or party lyrics.

Every sung line must have a reason to exist.

==================================================
NATURAL CUBAN WRITING
==================================================

Write natural contemporary Cuban Spanish.

The lyric should sound conversational and musical.

Use wit, irony, picardía and everyday language
when appropriate.

Do NOT exaggerate Cuban slang.

Do NOT write a caricature.

Avoid generic AI poetry.

Avoid decorative metaphors unless they are
genuinely clever and natural.

==================================================
COROS
==================================================

Use the director's MAIN CORO concept.

You may refine its wording to improve rhythm.

The main coro must be memorable and easy to repeat.

For the:

3 bars singer
+
1 bar coro
x 7

use EXACTLY the SHORT CORO selected by the director.

Do not change that short response between soneos.

==================================================
SEVEN SHORT SONEOS
==================================================

Create exactly 7 different short soneos.

Each must:

- introduce a different thought
- relate directly to the story
- sound spontaneous
- finish cleanly before the coro
- avoid repeating the previous idea

Possible functions:

- expose another lie
- make fun of an excuse
- answer the coro
- reveal a detail
- challenge the other person
- make an ironic observation
- escalate the situation

Do not simply change synonyms.

==================================================
FORMATTING
==================================================

Use bracket labels.

GOOD:

[Introduccion - 16 bars - Songo instrumental]

[Coro Inicial - 16 bars]

[Voz 1 - 8 bars]

[Mambo 1 - 16 bars]

[Soneo Corto - 28 bars]

[Coda - 4 bars]

Instrumental sections contain ONLY
their bracket label.

Never write:

(Instrumental...)
(Band enters...)
(Brass builds...)

Do not use production explanations in parentheses.

Do not write:

Cantante:
Coro:
Guía:

Instead use clean section labels.

Every sung phrase must appear on its own line.

==================================================
FINAL OUTPUT
==================================================

Return ONLY:

=== LYRICS ===

followed by the complete original lyric.

No explanations.

No Markdown code fences.

No commentary before or after the lyrics.
"""

    return prompt
