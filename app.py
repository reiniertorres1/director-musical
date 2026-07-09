import streamlit as st
import google.generativeai as genai

# Jalamos la llave secreta
MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)

# Configuración de la página
st.set_page_config(page_title="Director Musical - Suno AI", layout="centered")

st.title("🎵 Director Musical para Suno AI")
st.markdown("Genera prompts y letras estructuradas con variaciones dinámicas y calidad poética.")

# Diccionario de perfiles
perfiles = {
    "Balada Romántica (Estilo Luis Miguel 90s)": {
        "base_style": "1990s romantic latin pop ballad, symphonic bolero, lush orchestral strings, 90s synth pad, vintage electric piano, jazz chords, smooth fretless bass, elegant acoustic drum kit, rich male crooner, velvety chest voice, pristine studio mix, NO crowd",
        "reglas_dinamicas": "Añade 2 o 3 tags en inglés que reflejen el 'mood' de la letra (ej. melancholic, dramatic, passionate). Mantén siempre el sonido de los sintetizadores de los 90s y el piano eléctrico.",
        "letra_template": """[Elegant Orchestral Intro]

[Verse 1]
[Smooth vocals]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Pre-Chorus]
(Verso 1)
(Verso 2)

[Chorus]
[Melodic delivery]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Verse 2]
[Velvety chest voice]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Chorus]
[Melodic delivery]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Instrumental Solo]

[Bridge]
(Verso 1)
(Verso 2)

[Final Chorus]
[Smooth and Emotional]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Outro]"""
    },
    "Timba Cubana (Explosiva para el bailador)": {
        "base_style": "authentic cuban timba, pristine studio production, heavy piano tumbao, complex horn section, songo groove, bomba bassline, polyrhythmic percussion, aggressive brass mambo, clean mix",
        "reglas_dinamicas": "Añade tags en inglés que reflejen la temática (ej. street style, romantic, aggressive, party).",
        "letra_template": """[Intro Tumbao y Metales]

[Verse 1]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Coro 1]
(Verso 1)
(Verso 2)

[Soneo]
Guía: (Pregón corto 1)
Guía: (Pregón corto 2)

[Mambo 1]

[Coro 2]
Coro: (Verso 1)
Coro: (Verso 2)
Guía: (Soneo tirando pulla)

[Mambo 2 - Agresivo]

[Efecto - Bloque Rítmico]

[Bomba y Masacote]
Coro: (Coro explosivo)
Guía: (Soneo final con bomba)

[Mambo 3 - Cierre]"""
    }
}

# Interfaz de usuario
st.subheader("Configura tu canción")
seleccion = st.selectbox("Selecciona el Perfil Musical:", list(perfiles.keys()))
tema = st.text_input("¿De qué trata la canción? (Tema principal):", placeholder="Ej. Una despedida inevitable en el aeropuerto...")

# Botón de generación
if st.button("Escribir Letra con IA", type="primary"):
    if not MI_API_KEY:
        st.error("⚠️ No has puesto la API Key en el código.")
    elif not tema:
        st.warning("⚠️ Por favor ingresa un tema para la canción.")
    else:
        with st.spinner("Creando arreglo dinámico y escribiendo letra..."):
            perfil = perfiles[seleccion]
            
            try:
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
                Eres un director musical, arreglista y poeta experto de {seleccion}. 
                El usuario quiere una canción sobre: "{tema}".
                
                TAREA 1: GENERAR EL STYLE PROMPT PARA SUNO AI
                Estilo Base: {perfil['base_style']}
                Instrucciones de variación: {perfil['reglas_dinamicas']}
                
                TAREA 2: ESCRIBIR LA LETRA
                REGLAS ESTRICTAS PARA QUE SUNO CANTE BIEN:
                1. CALIDAD POÉTICA Y CERO RIPIOS: Queda ESTRICTAMENTE PROHIBIDO usar palabras antimusicales o de relleno. Usa vocabulario romántico. Si no encuentras una rima consonante, usa rima asonante. NO sacrifiques la elegancia por rimar a la fuerza.
                2. PROHIBIDO ESCRIBIR ACOTACIONES: Los espacios instrumentales (como [Intro] o [Instrumental Solo]) se dejan completamente solos.
                3. MÉTRICA SIMÉTRICA: Máximo 8 sílabas por verso para no perder la métrica de 4 minutos.
                4. CERO ONOMATOPEYAS. NUNCA uses "ahhh", "zas", "pum".
                
                ESTRUCTURA OBLIGATORIA A RELLENAR:
                {perfil['letra_template']}
                
                FORMATO DE RESPUESTA OBLIGATORIO:
                Escribe exactamente las palabras "STYLE_PROMPT:" y "LETRA_FINAL:" para separar tu respuesta. No añadas nada más.
                
                STYLE_PROMPT:
                (aquí va el style generado)
                
                LETRA_FINAL:
                (aquí va la letra generada respetando los saltos de línea de la estructura)
                """
                
                response = model.generate_content(prompt)
                texto_respuesta = response.text
                
                st.success("¡Arreglo y letra generados con éxito!")
                
                # Sistema para forzar la separación visual en cajas de código en Streamlit
                if "LETRA_FINAL:" in texto_respuesta:
                    partes = texto_respuesta.split("LETRA_FINAL:")
                    style_part = partes[0].replace("STYLE_PROMPT:", "").strip()
                    letra_part = partes[1].strip()
                    
                    st.subheader("Style Prompt (Copiar en Suno)")
                    st.code(style_part, language="text")
                    
                    st.subheader("Letra Final (Copiar en Suno)")
                    st.code(letra_part, language="text")
                else:
                    st.text(texto_respuesta)
                
            except Exception as e:
                st.error(f"Hubo un problema al conectar con la API: {e}")
