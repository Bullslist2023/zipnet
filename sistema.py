import streamlit as st
import streamlit.components.v1 as components


def user_info_html():

    return """
    <html>
    <body style="font-family:Arial;">

    <h3>📊 Informações do seu dispositivo</h3>

    <p id="os"></p>
    <p id="browser"></p>
    <p id="screen"></p>
    <p id="lang"></p>
    <p id="tz"></p>

    <script>

        document.getElementById("os").innerHTML =
            "🖥 Sistema: " + navigator.platform;

        document.getElementById("browser").innerHTML =
            "🌐 Navegador: " + navigator.userAgent;

        document.getElementById("screen").innerHTML =
            "📺 Resolução: " + screen.width + "x" + screen.height;

        document.getElementById("lang").innerHTML =
            "🌍 Idioma: " + navigator.language;

        document.getElementById("tz").innerHTML =
            "⏰ Fuso: " + Intl.DateTimeFormat().resolvedOptions().timeZone;

    </script>

    </body>
    </html>
    """


st.title("Diagnóstico do Usuário")

components.html(user_info_html(), height=300)
