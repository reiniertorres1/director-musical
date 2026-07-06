import streamlit as st
import google.generativeai as genai

# Jalamos la llave secreta
MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)

# Configuración de la página
st.set_page_config(page_title="Director Musical - Suno AI", layout="centered")

st.title("🎵 Director Musical para Suno AI")
st.markdown("Genera prompts y letras estructuradas con calidad profesional.")

# Diccionario de perfiles con la fórmula exacta de Suno para Pop Orquestal 90s
perfiles = {
    "Balada Romántica (Estilo Luis Miguel)": {
        "style": "90s orchestral latin pop, symphonic bolero, powerful tenor vocals, grand piano, lush string section, smooth fretless bass, brass accents, dramatic romantic ballad, pristine studio polish, emotional crescendo, clear vibrato, clean belting, NO acoustic guitar, NO lo-fi, NO crowd",
        "letra_template": """[Majestic Intro]
(Piano de cola y gran sección de cuerdas. Sonido de estudio de Los Ángeles, años 90)

[Verse 1]
(Voz de tenor clara, potente y elegante. Métrica estricta de 8 sílabas para no perder el ritmo)

[Pre-Chorus]
(Sube la tensión musical, entran los platillos suavemente)

[Big Chorus]
(Estalla la orquesta completa. Voz llena, apasionada y con vibrato limpio, sin desafinar. Métrica exacta)

[Verse 2]
(Baja la intensidad al piano y bajo fretless. Misma métrica estricta del Verse 1)

[Big Chorus]
(Coro expansivo y majestuoso)

[Instrumental Interlude]
(Solo de saxofón alto o trompeta brillante, muy estilo pop de los 90s)

[Bridge]
(Puente dramático. Acordes de paso. La voz entrega la máxima emoción con técnica de estudio impecable)

[Climactic Final Chorus]
(Cierre majestuoso. Toda la potencia orquestal y vocal al límite, pero controlada)

[Outro]
(Vocal sostenida final, cerrando con un acorde orquestal grandioso y corte en seco)"""
    },
    "Timba Cubana (Explosiva para el bailador)": {
        "style": "authentic cuban timba, pristine studio production, heavy piano tumbao, complex horn section, songo groove, bomba bassline, polyrhythmic percussion, aggressive brass mambo, clean mix, NO crowd, NO audience, NO live performance, NO cheering",
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
tema = st.text_input("¿De qué trata la canción? (Tema principal):", placeholder="Ej. Un amor de 25 años...")

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
                
                REGLAS MUSICALES ESTRICTAS:
                1. MÉTRICA PERFECTA (VITAL PARA LA IA): Para que el cantante no cante fuera de tiempo, TODOS los versos deben ser matemáticamente simétricos. Si el Verse 1 tiene versos de 8 sílabas, el Verse 2 debe tener versos de 8 sílabas. 
                2. TODO ES CANTADO: Queda TOTALMENTE PROHIBIDO usar partes habladas o narraciones secas.
                3. NUNCA menciones nombres de orquestas o cantantes en la letra.
                4. EL SONEO Y REGLA DE ONOMATOPEYAS: NUNCA uses onomatopeyas literales (no escribas "zas", "pum", "ahhh", "ohhh"), ya que los cantantes de IA las vocalizan como robots y arruinan la pista.
                5. FORMATO: Sustituye mis explicaciones entre paréntesis por la letra real. Mantén TODOS los metatags intactos (como [Big Chorus], [Bridge], etc.). No escribas introducciones.
                
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
