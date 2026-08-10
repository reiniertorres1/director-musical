# Configuracion base de la banda para Timba Cubana
# La voz NO se configura aqui.
# Este archivo controla solamente el comportamiento musical de la banda.


TIMBA_BAND = {

    "identity": {
        "genre": "Cuban Timba",
        "feel": "Modern Cuban dance band with strong songo and timba vocabulary",
        "energy": "Dynamic, powerful, danceable and sophisticated",
        "time_signature": "4/4",
    },


    "percussion": {
        "style": (
            "Deep Cuban songo and modern timba rhythmic foundation. "
            "Strong interaction between drum kit, congas, timbales, "
            "bongo, cowbell and guiro. "
            "The percussion must evolve throughout the arrangement instead "
            "of playing the same pattern continuously."
        ),

        "character": (
            "Highly syncopated, tight, funky, aggressive when necessary, "
            "but always musical and danceable."
        ),

        "important": (
            "Use authentic Cuban rhythmic breaks, bloques, gear changes, "
            "contrasting sections and controlled moments where the percussion "
            "drops or reduces intensity before the full band returns."
        ),
    },


    "bass": {
        "style": (
            "Electric bass with deep Cuban timba and songo tumbaos. "
            "Syncopated and melodic, strongly interacting with the percussion."
        ),

        "character": (
            "Funky, powerful and unpredictable without becoming excessively busy."
        ),

        "important": (
            "The bass should change tumbao patterns between important sections "
            "and help create the different gears of the arrangement."
        ),
    },


    "piano": {
        "style": (
            "Percussive Cuban piano tumbaos with modern timba vocabulary."
        ),

        "character": (
            "Syncopated, rhythmic, funky and harmonically rich."
        ),

        "important": (
            "Do not repeat one piano montuno through the entire song. "
            "Use different tumbao figures and rhythmic variations as "
            "the arrangement develops."
        ),
    },


    "brass": {
        "style": (
            "Powerful arranged Cuban brass section used for mambos, "
            "responses, punches and rhythmic accents."
        ),

        "character": (
            "Tight, sophisticated, syncopated and energetic."
        ),

        "important": (
            "Do not use constant brass throughout the entire song. "
            "Reserve the strongest horn writing for mambos, bloques, "
            "transitions and climactic sections."
        ),

        "avoid": (
            "Avoid gospel-like brass, church-band phrasing, "
            "generic big-band riffs and excessive sustained horn chords."
        ),
    },


    "dynamics": {
        "description": (
            "The arrangement must continuously evolve through musical gears. "
            "Alternate full-band passages with reduced textures, rhythmic breaks, "
            "mambos, percussion-driven sections and explosive returns of the band."
        ),

        "despelote": (
            "During despelote sections reduce the orchestration dramatically, "
            "leaving rhythmic space before rebuilding into the full band."
        ),
    },


    "production": {
        "sound": (
            "Polished modern studio recording with acoustic Cuban band character."
        ),

        "mix": (
            "Punchy rhythm section, clear bass, defined percussion, "
            "present piano and controlled brass."
        ),

        "avoid": (
            "No EDM production, no reggaeton beat, no generic Latin pop groove, "
            "no rock drums, no concert crowd ambience."
        ),
    },
}
