import streamlit as st
import google.generativeai as genai

# Jalamos la llave secreta
MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)

# Configuración de la página
st.set_page_config(page_title="Director Musical - Suno AI", layout="centered")

st.title("🎵 Director Musical para Suno AI")
st.markdown("Genera prompts y letras estructuradas con calidad profesional.")

# Diccionario de perfiles optimizado para duración de 4 min y control vocal absoluto
perfiles = {
    "Balada Romántica (Estilo Luis Miguel 90s)": {
        "style": "1990s adult contemporary pop ballad, symphonic bolero, smooth tenor vocals, velvety vocal tone, lush orchestral string section, acoustic grand piano, rhodes electric piano, smooth fretless bass, subtle saxophone solo, pristine studio production, melodic phrasing",
        "letra_template": """[Majestic Intro]
(Piano de cola elegante y sección de cuerdas majestuosa. Sonido limpio de estudio)

[Verse 1]
[Smooth vocals]
(Escribe solo 4 líneas. Métrica corta de 8 sílabas por línea. Voz suave y melódica)

[Pre-Chorus]
(Sutil subida de las cuerdas. Solo 2 líneas cortas para marcar la transición)

[Chorus]
[Melodic delivery]
(Coro principal. 4 líneas con rima perfecta. Voz clara, elegante y contenida, sin gritar)

[Verse 2]
[Velvety chest voice]
(Baja la intensidad al piano y bajo. 4 líneas cortas con la misma métrica exacta del Verse 1)

[Chorus]
[Melodic delivery]
(Repite el coro principal con toda la orquesta de cuerdas brillando)

[Instrumental Sax Solo]
(Solo de saxofón alto melódico, muy elegante, estilo pop de los 90s)

[Bridge]
(Puente emotivo. Solo 2 líneas líricas. La voz se mantiene controlada y técnica)

[Final Chorus]
[Smooth and Emotional]
(Último coro, cierre con toda la instrumentación pero el cantante mantiene su registro sin modular hacia arriba)

[Outro]
(Acorde orquestal final grandioso con corte limpio en seco)"""
    },
    "Timba Cubana (Explosiva para el bailador)": {
        "style": "authentic cuban timba, pristine studio production, heavy piano tumbao, complex horn section, songo groove, bomba bassline, polyrhythmic percussion, aggressive brass mambo, clean mix",
        "letra_template": """[Intro Tumbao y Metales]
(Arranca con fuerza, metales arriba, piano y percusión)

[Verse 1]
(Cuerpo del tema: Solo 4 líneas de métrica simétrica contando la historia)

[Coro 1]
(Coro principal, pegadizo y claro. 2 o 4 líneas rítmicas)

[Soneo]
Guía: (Pregón corto con buenos dicharachos de la calle)

[Mambo 1]
(Instrumental: Primer arreglo de metales, bailable y sabroso)

[Coro 2]
Coro: (Un coro nuevo, más picante y corto)
Guía: (Soneo tirando pulla al ritmo del bajo)
Coro: (Repite el coro 2)

[Mambo 2 - Agresivo]
(Instrumental: Cambio en los metales, trompetas altas y trombones a reventar)

[Efecto - Bloque Rítmico]
(Corte seco de la banda entera)

[Bomba y Masacote]
(Cae el piano machacando, bajo pesado, energía al máximo)
Coro: (Coro explosivo de 2 líneas)
Guía: (Soneo final con toda la bomba)

[Mambo 3 - Cierre]
(Metales finales a fuego y cierre con bloque seco)"""
    }
}

# Interfaz de usuario
st.subheader("Configura tu canción")
seleccion = st.selectbox("Selecciona el Perfil Musical:", list(perfiles.keys()))
tema = st.text_input("¿De qué trata la canción? (Tema principal):", placeholder="Ej. Un amor incondicional...")

# Botón de generación
if st.button("Escribir Letra con IA", type="primary"):
    if not MI_API_KEY:
        st.error("⚠️ No has puesto la API Key en el código. Pégala en la variable MI_API_KEY.")
    elif not tema:
        st.warning("⚠️ Por favor ingresa un tema para la canción.")
    else:
        with st.spinner("Afinando la orquesta de estudio..."):
            perfil = perfiles[seleccion]
            molde = perfil["letra_template"]
            estilo = perfil["style"]
            
            try:
                # Sistema Anti Error 404
                modelo_valido = None
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        if 'flash' in m.name or 'pro' in m.name:
                            modelo_valido = m.name
                            break
                
                if not modelo_valido:
                    modelo_valido = 'gemini-1.5-flash'
                    
                model = genai.GenerativeModel(modelo_valido)
                
                prompt = f"""
                Eres un arreglista, compositor y letrista experto de {seleccion}. Escribe una canción sobre: "{tema}".
                
                REGLAS MUSICALES ULTRA ESTRICTAS PARA QUE LA CANCIÓN DURE MÁXIMO 4 MINUTOS Y LA IA NO GRITE:
                1. MÉTRICA CORTA Y EXACTA: Cada línea de los versos y coros debe tener un máximo de 8 sílabas. Frases cortas y elegantes. Esto es VITAL para que la IA no se atropelle ni cante fuera de métrica.
                2. CONTROL VOCAL ABSOLUTO: El cantante debe mantener un registro de tenor suave, melódico y aterciopelado. Usa estrictamente las etiquetas entre corchetes como [Smooth vocals] o [Melodic delivery] y jamás pongas textos que inciten a gritar, estallar o subir tonos descontrolados.
                3. DURACIÓN BAJO CONTROL: No extiendas las estrofas. Respeta el límite exacto de líneas indicado en la estructura para que la canción no rebase jamás los 4 minutos.
                4. TODO ES CANTADO: Prohibido usar partes habladas o explicaciones.
                5. CERO ONOMATOPEYAS: Nunca escribas "ahhh", "ohhh", "zas", "pum", porque la IA las lee literalmente y arruina la mezcla.
                6. FORMATO: Sustituye mis explicaciones entre paréntesis por la letra real. Mantén TODOS los metatags estructurales exactamente como te los doy.
                
                Estructura obligatoria a rellenar:
                {molde}
                """
                
                response = model.generate_content(prompt)
                texto_final = response.text
                
                st.success("¡Estructura generada con éxito!")
                
                st.subheader("Style Prompt (Copiar en Suno)")
                st.code(estilo, language="text")
                
                st.subheader("Letra Final (Copiar en Suno)")
                st.code(texto_final, language="text")
                
            except Exception as e:
                st.error(f"Hubo un problema al conectar con la API: {e}")
