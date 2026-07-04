import streamlit as st
import google.generativeai as genai

# =========================================================
# 1. PEGA TU API KEY AQUÍ ADENTRO (ENTRE LAS COMILLAS)
# =========================================================
MI_API_KEY = "AQ.Ab8RN6LlU-5d_oicAjFd1EHKxCYuNAHuW1NOPiaB1TuRuOYbvg"

# Configuración de la página para móviles
st.set_page_config(page_title="Director Musical - Suno AI", layout="centered")

st.title("🎵 Director Musical para Suno AI")
st.markdown("Genera prompts y letras estructuradas con calidad profesional.")

# Diccionario de perfiles definitivo: Calidad de estudio, modulación y soneos melódicos.
perfiles = {
    "Balada Romántica (Estilo Luis Miguel)": {
        "style": "bolero, romantic latin pop, pristine studio recording, lush orchestral strings, soft acoustic guitar, jazz chords, slow tempo, elegant, acoustic drum kit, soft crooner, natural studio vocals, melodic phrasing, intimate, no belting, NO robotic voice, NO crowd, NO audience",
        "letra_template": "[Verse 1]\n(Escribe 4 versos íntimos)\n\n[Pre-Chorus]\n(Escribe 2 versos subiendo la emoción)\n\n[Chorus]\n(Escribe 4 versos con la melodía principal)\n\n[Verse 2]\n(Escribe 4 versos continuando la historia)\n\n[Chorus]\n(Repite el coro principal)\n\n[Bridge]\n(Puente musical y lírico con cambio de acordes)\n\n[Guitar Solo]\n\n[Chorus]\n(Último coro con toda la emoción, modulación hacia arriba)\n\n[End]\n(Terminar en seco, corte limpio)"
    },
    "Timba Cubana (Estilo Mandy Cantero)": {
        "style": "authentic cuban timba, pristine studio production, organic songo groove, studio acoustic drum kit, real brass section, acoustic trumpets, progressive harmony, harmonic modulation, baby bass tumbao, natural studio vocals, expressive melodic sonero, NO synth brass, NO midi horns, NO robotic voice, NO crowd, NO audience, NO live performance",
        "letra_template": "[Intro]\n(Arreglo musical de metales reales, sin voz)\n\n[Verse 1]\n(CANTADO: Historia clara, estilo crónica urbana)\n\n[Pre-Chorus]\n(CANTADO: Subiendo la intensidad armónica)\n\n[Chorus 1]\n(CANTADO: Coro principal, melódico y con peso)\n\n[Drum Break]\n(Corte de batería estilo songo para preparar los metales)\n\n[Mambo]\n(Instrumental: sección de metales agresiva y real)\n\n[Verse 2]\n(CANTADO: Continúa la historia)\n\n[Chorus 1]\n(Repite el coro melódico)\n\n[Soneo]\n(CANTADO: Improvisación melódica y afinada)\n\n[Bridge: Key Change]\n(CANTADO: Puente lírico forzando una modulación armónica, cambia la melodía por completo)\n\n[Chorus 2]\n(CANTADO: Un coro más corto y directo)\n\n[Soneo]\n(CANTADO: Diálogo directo respondiendo al coro)\n\n[Micro-Chorus]\n(CANTADO: Coro de una sola frase cortísima que se repite rítmicamente)\n\n[Moña]\n(Contrapunto intenso de trompetas acústicas)\n\n[Soneo]\n(CANTADO: Remate final melódico)\n\n[End]\n(Corte musical limpio y contundente)"
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
                genai.configure(api_key=MI_API_KEY)
                
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
                4. EL SONEO: Los soneos deben ser melódicos. Tienen que tener sabor, pero con palabras bien dichas que inviten a una interpretación de estudio natural, no a gritos robotizados.
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