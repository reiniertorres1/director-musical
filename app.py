import streamlit as st
import google.generativeai as genai

# Jalamos la llave secreta
MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)

# Configuración de la página
st.set_page_config(page_title="Director Musical - Suno AI", layout="centered")

st.title("🎵 Director Musical para Suno AI")
st.markdown("Genera prompts y letras estructuradas con calidad profesional.")

# Diccionario de perfiles con Reglas de Letra INDEPENDIENTES
perfiles = {
    "Timba Cubana (Callejera - Estilo Pupy / Van Van / Maykel Blanco)": {
        "base_style": "modern havana timba, heavy songo groove, deep male baritone vocals, conversational sonero, laid-back vocal delivery, fat bassline, syncopated piano tumbao, modern brass blocks, street timba, NO high pitch, NO belting, NO screaming, NO traditional salsa",
        "reglas_dinamicas": "Añade tags en inglés que reflejen la temática (ej. street party, neighborhood drama, aggressive groove).",
        "reglas_letras": "REGLA VITAL: Escribe con pura calle y jerga cubana actual. Usa dicharachos, picardía y temática de barrio (el día a día, la rumba, personajes de la calle). Estilo Juan Formell o Pupy y los que Son Son. NADA de poesía romántica ni palabras formales. Lenguaje directo, bailador y sabroso.",
        "letra_template": """[Intro Songo Instrumental]

[Chorus 1]
(Verso 1 del coro - pegajoso y callejero)
(Verso 2 del coro)
(Verso 3 del coro)
(Verso 4 del coro)
(Repite Verso 1 del coro)
(Repite Verso 2 del coro)
(Repite Verso 3 del coro)
(Repite Verso 4 del coro)

[Verse 1]
[Deep baritone vocals]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Chorus 2]
(Verso 1 del coro)
(Verso 2 del coro)
(Verso 3 del coro)
(Verso 4 del coro)

[Verse 2]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Bridge]
(Verso 1)
(Verso 2)
(Verso 3)
(Verso 4)

[Chorus 3]
(Verso 1 del coro)
(Verso 2 del coro)
(Verso 3 del coro)
(Verso 4 del coro)

[Tight Percussion Block]

[Soneo 1 y Coro]
[Conversational delivery]
Guía: (Verso de improvisación 1 - puro dicho cubano)
Guía: (Verso de improvisación 2)
Guía: (Verso de improvisación 3)
Guía: (Verso de improvisación 4)
Coro: (Verso del coro)
Coro: (Verso del coro)
Coro: (Verso del coro)
Coro: (Verso del coro)
Guía: (Verso de improvisación 5)
Guía: (Verso de improvisación 6)
Guía: (Verso de improvisación 7)
Guía: (Verso de improvisación 8)
Coro: (Verso del coro)
Coro: (Verso del coro)
Coro: (Verso del coro)
Coro: (Verso del coro)

[Mambo Instrumental 1]

[Montuno - Llamada y Respuesta]
Guía: (Línea larga 1)
Coro: (Respuesta corta y picante)
Guía: (Línea larga 2)
Coro: (Misma respuesta corta)
Guía: (Línea larga 3)
Coro: (Misma respuesta corta)
Guía: (Línea larga 4)
Coro: (Misma respuesta corta)
Guía: (Línea larga 5)
Coro: (Misma respuesta corta)
Guía: (Línea larga 6)
Coro: (Misma respuesta corta)
Guía: (Línea larga 7)
Coro: (Misma respuesta corta)

[Mambo con Coro]
(Verso 1 del coro)
(Verso 2 del coro)

[Breakdown - Funky Bass and Congas only]

[Full Band Entrance - Aggressive Mambo]

[Final Chorus with Melodic Ad-libs]
(Verso 1 del coro largo)
(Verso 2 del coro largo)
(Verso 3 del coro largo)
(Verso 4 del coro largo)

[Outro con Bloque Seco]"""
    },
    "Balada Romántica (Estilo Luis Miguel 90s)": {
        "base_style": "1990s romantic latin pop ballad, symphonic bolero, lush orchestral strings, 90s synth pad, vintage electric piano, jazz chords, smooth fretless bass, elegant acoustic drum kit, rich male crooner, velvety chest voice, pristine studio mix, NO crowd",
        "reglas_dinamicas": "Añade 2 o 3 tags en inglés que reflejen el 'mood' de la letra (ej. melancholic, dramatic, passionate). Mantén siempre el sonido de los sintetizadores de los 90s y el piano eléctrico. REGLA ESTRICTA: NUNCA incluyas guitarras eléctricas ni acústicas.",
        "reglas_letras": "REGLA VITAL: Calidad poética y cero ripios. Usa vocabulario romántico, elegante y sofisticado. NADA de jerga ni lenguaje callejero.",
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
    }
}

# Interfaz de usuario
st.subheader("Configura tu canción")
seleccion = st.selectbox("Selecciona el Perfil Musical:", list(perfiles.keys()))
tema = st.text_input("¿De qué trata la canción? (Tema principal):", placeholder="Ej. Un chisme en el barrio...")

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
                Eres un director musical, arreglista y compositor experto de {seleccion}. 
                El usuario quiere una canción sobre: "{tema}".
                
                TAREA 1: GENERAR EL STYLE PROMPT PARA SUNO AI
                Estilo Base: {perfil['base_style']}
                Instrucciones de variación: {perfil['reglas_dinamicas']}
                
                TAREA 2: ESCRIBIR LA LETRA
                {perfil['reglas_letras']}
                
                REGLAS ESTRICTAS DE FORMATO:
                1. FORMATO VISUAL OBLIGATORIO (CRÍTICO): Tienes que presionar ENTER después de cada verso. NO agrupes los versos en párrafos continuos.
                2. PROHIBIDO ESCRIBIR ACOTACIONES: Los espacios instrumentales (como [Tight Percussion Block], [Breakdown - Funky Bass and Congas only]) se dejan completamente solos, sin texto debajo.
                3. MÉTRICA: Máximo 8 sílabas por verso.
                4. CERO ONOMATOPEYAS. NUNCA uses "ahhh", "zas", "pum".
                
                ESTRUCTURA OBLIGATORIA A RELLENAR (COMPLETA TODA LA PLANTILLA SIN SALTARTE NADA):
                {perfil['letra_template']}
                
                FORMATO DE RESPUESTA OBLIGATORIO:
                Escribe exactamente las palabras "STYLE_PROMPT:" y "LETRA_FINAL:" para separar tu respuesta. No añadas nada más.
                
                STYLE_PROMPT:
                (aquí va el style generado)
                
                LETRA_FINAL:
                (aquí va la letra generada respetando los saltos de línea y la estructura larga)
                """
                
                response = model.generate_content(prompt)
                texto_respuesta = response.text
                
                st.success("¡Arreglo y letra generados con éxito!")
                
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
