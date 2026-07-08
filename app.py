import streamlit as st
import google.generativeai as genai

# Jalamos la llave secreta
MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)

# Configuración de la página
st.set_page_config(page_title="Director Musical - Suno AI", layout="centered")

st.title("🎵 Director Musical para Suno AI")
st.markdown("Genera prompts y letras estructuradas con calidad profesional.")

# Diccionario de perfiles con la fórmula exacta corregida (Cero gritos, 100% elegancia)
perfiles = {
    "Balada Romántica (Estilo Luis Miguel 90s)": {
        "style": "1990s latin pop ballad, symphonic bolero, smooth male adult contemporary vocals, lush orchestral strings, warm electric piano, elegant brass section, velvety chest voice, pristine romantic studio mix, smooth vocal delivery",
        "letra_template": """[Elegant Orchestral Intro]
(Piano, cuerdas y metales suaves. Sonido de gran estudio de los 90s)

[Verse 1]
[Smooth chest voice]
(Voz suave, cálida y muy romántica. Métrica de 8 sílabas exactas)

[Pre-Chorus]
(Sutil subida musical, pero el cantante mantiene el tono aterciopelado)

[Chorus: Smooth and Melodic]
(Coro amplio y majestuoso. La voz es elegante, melódica y controlada en todo momento, cantando al oído)

[Verse 2]
[Velvety delivery]
(Baja la intensidad al piano, voz muy cercana y cálida. Misma métrica de 8 sílabas)

[Chorus: Smooth and Melodic]
(Repite el coro principal con toda la orquesta, sin perder la suavidad vocal)

[Instrumental Interlude]
(Solo de saxofón o trompeta elegante, pop 90s)

[Bridge: Emotional but restrained]
(Puente emotivo, la orquesta crece pero el cantante mantiene una técnica impecable y suave)

[Final Chorus: Melodic and Smooth]
(Cierre orquestal grandioso con la voz manteniéndose en su registro medio, elegante, sin gritar)

[Outro]
(Voz apagándose suavemente con un acorde final elegante)"""
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
                
                REGLAS MUSICALES ESTRICTAS:
                1. MÉTRICA PERFECTA (VITAL PARA LA IA): Todos los versos deben ser matemáticamente simétricos (ej. 8 sílabas exactas) para que el cantante mantenga el ritmo perfecto.
                2. ESTILO DE VOZ (CRÍTICO): El cantante debe sonar aterciopelado, elegante y romántico en todo momento. NUNCA agregues indicaciones de subir el tono, notas altas, estallidos, gritos o potencia. Usa siempre etiquetas de control como [Smooth chest voice], [Velvety delivery] o [Melodic and Smooth].
                3. TODO ES CANTADO: Prohibido usar partes habladas o explicaciones.
                4. CERO ONOMATOPEYAS: Nunca escribas "ahhh", "ohhh", "zas", "pum", porque la IA las lee como un robot y arruina la mezcla.
                5. FORMATO: Sustituye mis explicaciones entre paréntesis por la letra real. Mantén TODOS los metatags estructurales (las frases entre corchetes) exactamente como te los doy.
                
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
