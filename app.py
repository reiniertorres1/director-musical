import streamlit as st
import google.generativeai as genai

# Jalamos la llave secreta
MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)

# Configuración de la página
st.set_page_config(page_title="Director Musical - Suno AI", layout="centered")

st.title("🎵 Director Musical para Suno AI")
st.markdown("Genera prompts y letras estructuradas con variaciones dinámicas y calidad poética.")

# Diccionario de perfiles con formato estricto para Suno (Cero acotaciones cantadas)
perfiles = {
    "Balada Romántica (Estilo Luis Miguel 90s)": {
        "base_style": "1990s adult contemporary pop ballad, symphonic bolero, smooth tenor vocals, velvety vocal tone, lush orchestral string section, acoustic grand piano, smooth fretless bass, pristine studio production, melodic phrasing",
        "reglas_dinamicas": "Construye el 'Style' de Suno usando el estilo base, pero añádele 2 o 3 tags en inglés que reflejen el 'mood' de la letra (ej. melancholic, dramatic, passionate, gentle). REGLA ESTRICTA: NUNCA incluyas guitarras eléctricas ni acústicas.",
        "letra_template": """[Elegant Orchestral Intro]

[Verse 1]
[Smooth vocals]
(Línea 1 octosílaba)
(Línea 2 octosílaba)
(Línea 3 octosílaba)
(Línea 4 octosílaba)

[Pre-Chorus]
(Línea 1 corta)
(Línea 2 corta)

[Chorus]
[Melodic delivery]
(Línea 1 del coro)
(Línea 2 del coro)
(Línea 3 del coro)
(Línea 4 del coro)

[Verse 2]
[Velvety chest voice]
(Línea 1 octosílaba)
(Línea 2 octosílaba)
(Línea 3 octosílaba)
(Línea 4 octosílaba)

[Chorus]
[Melodic delivery]
(Línea 1 del coro)
(Línea 2 del coro)
(Línea 3 del coro)
(Línea 4 del coro)

[Instrumental Saxophone Solo]

[Bridge]
(Línea 1 dramática)
(Línea 2 dramática)

[Final Chorus]
[Smooth and Emotional]
(Línea 1 del coro)
(Línea 2 del coro)
(Línea 3 del coro)
(Línea 4 del coro)

[Outro]"""
    },
    "Timba Cubana (Explosiva para el bailador)": {
        "base_style": "authentic cuban timba, pristine studio production, heavy piano tumbao, complex horn section, songo groove, bomba bassline, polyrhythmic percussion, aggressive brass mambo, clean mix",
        "reglas_dinamicas": "Construye el 'Style' usando el estilo base, pero añádele tags en inglés que reflejen la temática (ej. street style, romantic, aggressive, party).",
        "letra_template": """[Intro Tumbao y Metales]

[Verse 1]
(Línea 1)
(Línea 2)
(Línea 3)
(Línea 4)

[Coro 1]
(Línea 1)
(Línea 2)

[Soneo]
Guía: (Pregón corto 1)
Guía: (Pregón corto 2)

[Mambo 1]

[Coro 2]
Coro: (Línea 1)
Coro: (Línea 2)
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
                1. FORMATO VISUAL OBLIGATORIO: Cada línea de la canción TIENE que ir en un renglón nuevo (usa la tecla Enter). NUNCA agrupes los versos en un solo párrafo de corrido, porque el cantante se quedará sin aire y cantará fuera de ritmo.
                2. PROHIBIDO ESCRIBIR ACOTACIONES: NUNCA escribas texto explicativo fuera de los corchetes. No escribas "Un piano melancólico entra" ni "Solo de saxofón". Suno es una IA y cantará esas instrucciones con la voz del artista. Los espacios instrumentales (como [Intro] o [Solo]) se dejan vacíos debajo.
                3. CALIDAD POÉTICA: Cero ripios. Usa lenguaje elegante y rima natural.
                4. MÉTRICA SIMÉTRICA: Máximo 8 sílabas por verso. 
                5. CERO ONOMATOPEYAS.
                
                ESTRUCTURA OBLIGATORIA A RELLENAR (Sustituye lo que está entre paréntesis por la letra real con saltos de línea):
                {perfil['letra_template']}
                
                FORMATO DE RESPUESTA:
                Muestra primero el texto "**Style Prompt (Copiar en Suno):**" seguido del string de estilo generado.
                Luego deja un espacio y muestra "**Letra Final (Copiar en Suno):**" seguido de toda la letra generada.
                """
                
                response = model.generate_content(prompt)
                
                st.success("¡Arreglo y letra generados con éxito!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Hubo un problema al conectar con la API: {e}")
