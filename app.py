import streamlit as st
import google.generativeai as genai

# Jalamos la llave secreta y se la asignamos a la variable que tu código ya conoce
MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)

# Configuración de la página para móviles
st.set_page_config(page_title="Director Musical - Suno AI", layout="centered")

st.title("🎵 Director Musical para Suno AI")
st.markdown("Genera prompts y letras estructuradas con calidad profesional.")

# Diccionario de perfiles definitivo purgado de ruidos en vivo
perfiles = {
    "Balada Romántica (Estilo Luis Miguel)": {
        "style": "bolero, romantic latin pop, pristine studio recording, lush orchestral strings, soft acoustic guitar, jazz chords, slow tempo, elegant, acoustic drum kit, soft crooner, natural studio vocals, melodic phrasing, intimate, gentle whisper, no belting, NO crowd, NO audience, NO live performance, NO cheering",
        "letra_template": """[Intro Orquestal]
(Cuerdas románticas y piano suave. Atmósfera íntima)

[Verse 1 - Soft Vocals]
(Canta con voz aterciopelada y casi susurrada. Escribe 4 versos íntimos)

[Pre-Chorus - Gentle]
(Sube la emoción de la orquesta, pero la voz se mantiene controlada y romántica. Escribe 2 versos)

[Chorus - No Belting]
(Coro amplio, instrumentación rica, voz con mucho sentimiento pero SIN gritar. Escribe 4 versos con la melodía principal)

[Verse 2 - Intimate]
(Vuelve a la intimidad, voz suave y cercana contando el resto de la historia. Escribe 4 versos)

[Chorus - No Belting]
(Repite el coro con más instrumentación, cuerdas majestuosas, voz cálida)

[Bridge]
(Puente musical y lírico con cambio de acordes. Voz expresiva pero contenida)

[Guitar Solo]

[Chorus - Emotional but smooth]
(Último coro con toda la emoción, modulación hacia arriba, pero manteniendo el control vocal)

[Outro]
(Voz susurrada finalizando el tema, cuerdas desvaneciéndose lentamente, terminar en seco)"""
    },
    "Timba Cubana (Explosiva para el bailador)": {
        "style": "authentic cuban timba, pristine studio production, heavy piano tumbao, complex horn section, songo groove, bomba bassline, polyrhythmic percussion, aggressive brass mambo, clean mix, NO crowd, NO audience, NO live performance, NO cheering",
        "letra_template": """[Intro Tumbao y Metales]
(Arranca con fuerza, metales arriba, piano y percusión)

[Verse 1]
(Cuerpo del tema: Solo 4 líneas contando la historia directo al grano)

[Coro 1]
(Coro principal, pegadizo y claro)

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
tema = st.text_input("¿De qué trata la canción? (Tema principal):", placeholder="Ej. Un malentendido en el barrio...")

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
                Eres un arreglista y sonero experto de {seleccion}. Escribe una canción sobre: "{tema}".
                
                REGLAS MUSICALES ESTRICTAS:
                1. TODO ES CANTADO: Queda TOTALMENTE PROHIBIDO usar partes habladas o narraciones secas.
                2. NUNCA menciones nombres de orquestas reales en la letra.
                3. ARMONÍA: Presta especial atención a la sección [Bridge: Key Change]. Crea una letra distinta ahí que invite al cantante a subir de tono o cambiar la armonía drásticamente.
                4. EL SONEO Y REGLA DE ONOMATOPEYAS: Los soneos deben ser melódicos y con sabor cubano. NUNCA uses onomatopeyas literales como "zas", "pum" o similares, ya que los cantantes virtuales las vocalizan de forma literal arruinando el tumbao.
                5. FORMATO: Sustituye mis explicaciones entre paréntesis por la letra real. Mantén TODOS los metatags intactos (incluyendo [Drum Break], [Moña], etc.). No escribas introducciones explicativas.
                
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
