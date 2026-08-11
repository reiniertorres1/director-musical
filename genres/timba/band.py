# Configuracion base de la banda para Timba Cubana
# La voz NO se configura aqui.
# Este archivo controla solamente el comportamiento musical de la banda.


TIMBA_BAND = {

    "identity": {
        "genre": "Modern Cuban Timba",

        "feel": (
            "Sophisticated modern Cuban dance band rooted in songo and timba. "
            "The music must feel rhythmically alive, harmonically active, "
            "funky, unpredictable and highly arranged."
        ),

        "energy": (
            "Dynamic and powerful, but never flat or continuously loud. "
            "Energy must come from groove changes, harmonic tension, "
            "rhythmic gears, bass movement, piano variations, bloques "
            "and contrasting orchestration."
        ),

        "time_signature": "4/4",

        "important": (
            "The arrangement must evolve continuously. "
            "Never build the entire song over one static harmonic loop, "
            "one repeated piano tumbao or one repeated bass pattern."
        ),
    },


    "percussion": {
        "style": (
            "Deep Cuban songo and modern timba rhythmic foundation. "
            "Interactive drum kit, congas, timbales, bongo, cowbell and guiro. "
            "The rhythm section must behave like an integrated Cuban band, "
            "not like percussion layered over a generic Latin drum loop."
        ),

        "character": (
            "Highly syncopated, tight, funky, organic and rhythmically sophisticated. "
            "Human feel with strong internal conversation between drum kit "
            "and hand percussion."
        ),

        "important": (
            "Use authentic Cuban breaks, cierres, bloques and gear changes. "
            "Change rhythmic density between sections. "
            "Use stops, pickups, short fills, displaced accents, percussion drops "
            "and sudden full-band reentries."
        ),

        "gears": (
            "The percussion must noticeably change gears during the arrangement. "
            "Verse grooves should leave space. "
            "Montuno sections should become more interlocking. "
            "Mambos should use precise rhythmic blocks. "
            "Despelote may become more open and dangerous rhythmically "
            "before the full band locks back together."
        ),
    },


    "bass": {
        "style": (
            "Virtuosic funky Cuban electric bass with deep modern timba and songo vocabulary. "
            "Highly syncopated, melodic and rhythmically active."
        ),

        "character": (
            "Warm, punchy, funky, elastic and unpredictable. "
            "The bass must feel like one of the main engines of the arrangement, "
            "not a background instrument."
        ),

        "important": (
            "The bass must NEVER simply follow root notes or repeat one basic tumbao. "
            "Use changing Cuban bass tumbaos, anticipations, syncopated pickups, "
            "ghost-note feel, octave displacement, chromatic approaches, "
            "short melodic fills and rhythmic displacement."
        ),

        "interaction": (
            "Bass must constantly converse with piano and percussion. "
            "Leave space when the piano becomes dense, then answer with fills. "
            "Lock strongly with kick drum and percussion accents during bloques "
            "and gear changes."
        ),

        "development": (
            "Create different bass identities for verses, coros, montuno, mambos "
            "and despelote. "
            "Introduce new tumbao variations when important sections return. "
            "The final third of the song should contain noticeably stronger "
            "and more adventurous bass movement."
        ),

        "avoid": (
            "No straight root-note bass, no static two-note loop, "
            "no generic salsa bass pattern repeated for the entire song, "
            "no weak low end and no passive accompaniment."
        ),
    },


    "piano": {
        "style": (
            "Virtuosic percussive Cuban piano with sophisticated modern timba vocabulary. "
            "Strong rhythmic tumbaos combined with active harmonic movement."
        ),

        "character": (
            "Syncopated, funky, harmonically sophisticated and rhythmically inventive."
        ),

        "important": (
            "Never repeat one montuno or tumbao through the entire song. "
            "Create clearly different piano figures for major sections."
        ),

        "rhythm": (
            "Use anticipations, displaced accents, syncopated chord attacks, "
            "octave movement, rhythmic gaps and variations in register. "
            "The piano should sometimes leave deliberate space for bass and percussion."
        ),

        "harmony": (
            "Use extended chord voicings, inversions, secondary dominants, "
            "altered dominants, chromatic passing harmony, diminished passing chords, "
            "temporary tonicizations and tasteful reharmonization. "
            "Harmony should create tension and release without turning into jazz fusion."
        ),

        "development": (
            "When a coro or montuno returns, the piano may reharmonize it, "
            "change inversion, move register or introduce a new tumbao. "
            "Important transitions should sometimes introduce harmonic surprises."
        ),
    },


    "brass": {
        "style": (
            "Powerful arranged Cuban brass section for mambos, responses, "
            "punches, bloques, counterlines and transitions."
        ),

        "character": (
            "Tight, sophisticated, syncopated, rhythmically complex "
            "and harmonically connected to the rhythm section."
        ),

        "mambos": (
            "Each mambo should have its own identity. "
            "Use syncopated horn blocks, chromatic movement, short counterlines, "
            "rhythmic displacement and strong interaction with bass and piano."
        ),

        "important": (
            "Do not use constant brass throughout the entire song. "
            "Reserve the strongest horn writing for mambos, bloques, transitions "
            "and climactic moments. "
            "Silence from the brass is important so that its return feels powerful."
        ),

        "avoid": (
            "Avoid gospel-like brass, church-band phrasing, generic big-band riffs, "
            "constant salsa horn stabs, excessive sustained horn chords "
            "and nonstop brass walls."
        ),
    },


    "harmony": {
        "movement": (
            "Harmonic movement is essential. "
            "The song must not remain trapped in one repetitive chord progression."
        ),

        "language": (
            "Use sophisticated but danceable Cuban harmony: extended chords, "
            "secondary dominants, altered dominants, chromatic approach chords, "
            "passing diminished harmony, inversions and temporary tonicizations."
        ),

        "modulation": (
            "Use meaningful modulations or tonal-center shifts at selected structural moments. "
            "Possible places include the bridge, first mambo, later montuno, "
            "mambo with coro or final climax."
        ),

        "important": (
            "Modulations must feel intentional and exciting, not random. "
            "Build harmonic tension before the modulation and make the new tonal center "
            "feel like a genuine lift or change of gear."
        ),

        "reharmonization": (
            "When important coros return later in the arrangement, "
            "allow tasteful reharmonization, changed bass movement or new chord inversions "
            "so repeated material does not sound identical."
        ),

        "avoid": (
            "No static four-chord loop for the whole song. "
            "No endless tonic-dominant repetition. "
            "No random jazz chords that weaken the Cuban dance groove."
        ),
    },


    "dynamics": {
        "description": (
            "The arrangement must continuously evolve through distinct musical gears. "
            "Changes should involve rhythm, harmony, bass, piano, orchestration "
            "and density, not merely louder volume."
        ),

        "gear_changes": (
            "Create unmistakable gear changes where bass tumbao, piano pattern, "
            "percussion pattern and ensemble accents change together. "
            "Some gears may feel sparse and deep; others dense, syncopated and explosive."
        ),

        "virtuosity": (
            "Use high-level ensemble musicianship. "
            "Bass, piano and percussion may become technically adventurous, "
            "especially during montuno, mambos and despelote. "
            "Virtuosity must serve groove and interaction rather than sounding like "
            "unrelated solos."
        ),

        "tension_release": (
            "Build tension with harmonic movement, rhythmic suspension, breaks, "
            "chromatic approaches and increasingly active tumbaos. "
            "Then release through a powerful coro, mambo, bloque or full-band return."
        ),

        "despelote": (
            "The despelote should feel rhythmically dangerous and exciting. "
            "Strip away parts of the orchestration, expose funky bass and percussion, "
            "allow piano and rhythm section to open up, use breaks and unexpected accents, "
            "then rebuild into an explosive but controlled full-band return."
        ),

        "final_section": (
            "The final third must introduce new musical information. "
            "Use stronger bass variation, altered piano tumbao, reharmonization, "
            "a tonal lift or modulation, new rhythmic bloques and a more intense gear. "
            "Do not simply repeat the same chorus accompaniment from the beginning."
        ),
    },


    "production": {
        "sound": (
            "Polished modern studio recording with the character of a real Cuban band. "
            "Organic, warm, punchy and rhythmically detailed."
        ),

        "mix": (
            "Bass-forward rhythm section with warm punchy low end, "
            "clearly defined percussion, present rhythmic piano "
            "and controlled brass. "
            "The bass and percussion groove must remain clearly audible."
        ),

        "important": (
            "Preserve dynamic contrast. "
            "Do not over-compress the arrangement into one constant level of energy."
        ),

        "avoid": (
            "No EDM production, no reggaeton beat, no generic Latin pop groove, "
            "no rock drums, no generic salsa arrangement, no synthetic percussion loop, "
            "no flat bass, no static harmony and no concert crowd ambience."
        ),
    },
}
