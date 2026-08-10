# Estructura oficial de la Timba
# Compás: 4/4
# Total: 200 compases

TIME_SIGNATURE = "4/4"

TIMBA_ARRANGEMENT = [
    {
        "section": "Introduccion",
        "bars": 16,
        "description": "Introduccion instrumental de la banda."
    },

    {
        "section": "Coro inicial",
        "bars": 16,
        "pattern": "4 compases x 4 repeticiones",
        "description": "Coro de 4 compases repetido cuatro veces."
    },

    {
        "section": "Voz 1",
        "bars": 8,
        "description": "Primera seccion del cantante."
    },

    {
        "section": "Coro 2",
        "bars": 8,
        "description": "Coro de ocho compases."
    },

    {
        "section": "Voz 2",
        "bars": 8,
        "description": "Segunda seccion del cantante."
    },

    {
        "section": "Puente",
        "bars": 8,
        "description": "Puente inmediatamente despues de Voz 2."
    },

    {
        "section": "Coro 3",
        "bars": 8,
        "description": "Coro antes de comenzar la zona de improvisacion."
    },

    {
        "section": "Improvisacion y coro",
        "bars": 32,
        "pattern": "(8 compases improvisacion + 8 compases coro) x 2",
        "description": "El cantante improvisa durante 8 compases y responde el coro durante 8. El ciclo se repite dos veces."
    },

    {
        "section": "Mambo 1",
        "bars": 16,
        "description": "Mambo instrumental fuerte de la banda."
    },

    {
        "section": "Soneo corto",
        "bars": 28,
        "pattern": "(3 compases cantante + 1 compas coro) x 7",
        "description": "Improvisaciones diferentes del cantante sobre el mismo coro corto."
    },

    {
        "section": "Mambo con coro",
        "bars": 16,
        "description": "Mambo con participacion del coro y banda completa."
    },

    {
        "section": "Despelote",
        "bars": 8,
        "description": "La banda se tumba y deja espacio para el cantante y la seccion ritmica."
    },

    {
        "section": "Regreso de la banda",
        "bars": 8,
        "description": "Regresa toda la banda con maxima energia."
    },

    {
        "section": "Coro largo final",
        "bars": 16,
        "pattern": "Coro de 4 compases repetido durante 16 compases",
        "description": "El cantante improvisa por encima del coro."
    },

    {
        "section": "Coda",
        "bars": 4,
        "description": "Cierre final de la cancion."
    },
]


TOTAL_BARS = sum(section["bars"] for section in TIMBA_ARRANGEMENT)
