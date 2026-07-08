import streamlit as st
import google.generativeai as genai

# Jalamos la llave secreta
MI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=MI_API_KEY)

# Configuración de la página
st.set_page_config(page_title="Director Musical - Suno AI", layout="centered")

st.title("🎵 Director Musical para Suno AI")
st.markdown("Genera prompts y letras estructuradas con variaciones dinámicas y calidad poética.")

# Diccionario de perfiles modificado para ser DINÁMICO
perfiles = {
    "Balada Romántica (Estilo Luis Miguel 90s)": {
        "base_style": "1990s adult contemporary pop ballad, symphonic bolero, smooth tenor vocals, velvety vocal tone, lush orchestral string section, acoustic grand piano, smooth fretless bass, pristine studio production, melodic phrasing",
        "reglas_dinamicas": "Construye el 'Style' de Suno usando el estilo base, pero añádele 2 o 3 tags en inglés que reflejen el 'mood' de la letra (ej. melancholic, dramatic, passionate, gentle). Además, varía el instrumento del '[Instrumental Solo]' en la letra (alterna entre saxofón alto, trompeta con sordina o piano Rhodes). REGLA ESTRICTA: NUNCA incluyas guitarras eléctricas ni acústicas en los arreglos o tags de este estilo.",
        "letra_template": """[Elegant Intro]
(Describe en una línea los instrumentos que inician según el mood, sin guitarras)

[Verse 1]
[Smooth vocals]
(4 líneas poéticas. Métrica corta de 8 sílabas)

[Pre-Chorus]
(2 líneas marcando transición con las cuerdas)

[Chorus]
[Melodic delivery]
(4 líneas de coro. Voz controlada y elegante sin gritar)

[Verse 2]
[Velvety chest voice]
(4 líneas con la misma métrica del Verse 1)

[Chorus]
[Melodic delivery]
(Repite coro)

[Instrumental Solo]
(Describe el solo con el instrumento de viento o piano que elegiste para esta variante)

[Bridge]
(2 líneas dramáticas pero controladas)

[Final Chorus]
[Smooth and Emotional]
(Último coro, cierre de la orquesta)

[Outro]
(Corte limpio final)"""
    },
    "Timba Cubana (Explosiva para el bailador)": {
        "base_style": "authentic cuban timba, pristine studio production, heavy piano tumbao, complex horn section, songo groove, bomba bassline, polyrhythmic percussion, aggressive brass mambo, clean mix",
        "reglas_dinamicas": "Construye el 'Style' usando el estilo base, pero añádele tags en inglés que reflejen la temática (ej. street style, romantic, aggressive, party).",
        "letra_template": """[Intro Tumbao y Metales]
(Arranca con fuerza, metales arriba, piano y percusión)

[Verse 1]
(Solo 4 líneas de métrica simétrica)

[Coro 1]
(Coro principal, 2 o 4 líneas)

[Soneo]
Guía: (Pregón corto con dichos cubanos)

[Mambo 1]
(Instrumental: Primer arreglo de metales)

[Coro 2]
Coro: (Coro nuevo)
Guía: (Soneo tirando pulla)
Coro: (Repite el coro 2)

[Mambo 2 - Agresivo]
(Instrumental: Cambio en los metales a reventar)

[Efecto - Bloque Rítmico]
(Corte seco)

[Bomba y Masacote]
(Piano machacando, bajo pesado)
Coro: (Coro explosivo)
Guía: (Soneo final con bomba)

[Mambo 3 - Cierre]
(Metales finales y bloque seco)"""
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
                # Buscar el mejor modelo
                modelo_valido = None
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        if 'flash' in m.name or 'pro' in m.name:
                            modelo_valido = m.name
                            break
                
                if not modelo_valido:
                    modelo_valido = 'gemini-1.5-flash'
                    
                model = genai.GenerativeModel(modelo_valido)
                
                # El Prompt Maestro Dinámico
                prompt = f"""
                Eres un director musical, arreglista y poeta experto de {seleccion}. 
                El usuario quiere una canción sobre: "{tema}".
                
                TAREA 1: GENERAR EL STYLE PROMPT PARA SUNO AI
                Estilo Base: {perfil['base_style']}
                Instrucciones de variación: {perfil['reglas_dinamicas']}
                
                TAREA 2: ESCRIBIR LA LETRA
                REGLAS LÍRICAS ESTRICTAS (ANTI-RELLENO Y DURACIÓN):
                1. CALIDAD POÉTICA: Escribe con lenguaje sofisticado y natural. QUEDA ESTRICTAMENTE PROHIBIDO usar palabras de "relleno" o que no tengan sentido solo para forzar una rima (ripios). Prioriza la rima asonante, el buen gusto y el sentimiento natural antes que una rima forzada y ridícula.
                2. MÉTRICA SIMÉTRICA: Máximo 8 sílabas por verso. Mantenlo corto para que no exceda los 4 minutos de canción.
                3. TODO ES CANTADO: Prohibido usar partes habladas o narraciones.
                4. CERO ONOMATOPEYAS: Nunca escribas ruidos, "ahhh", "zas", "pum" o instrumentos cantados.
                5. CONTROL VOCAL: Sustituye las explicaciones entre paréntesis por la letra real. Mantén intactos los tags de control de voz como [Smooth vocals] o [Velvety chest voice] para asegurar que el cantante no grite.
                
                ESTRUCTURA OBLIGATORIA (No añadas estrofas extra):
                {perfil['letra_template']}
                
                FORMATO DE RESPUESTA:
                Muestra primero el texto "**Style Prompt (Copiar en Suno):**" seguido del string de estilo generado.
                Luego deja un espacio y muestra "**Letra Final (Copiar en Suno):**" seguido de toda la letra generada. No añadas otras explicaciones.
                """
                
                response = model.generate_content(prompt)
                
                st.success("¡Arreglo y letra generados con éxito!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Hubo un problema al conectar con la API: {e}")
