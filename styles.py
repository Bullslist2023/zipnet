def load_css():
    return """
    <style>
    body {
        background-color: #F5F5F5;
    }

    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        color: white;
        background: linear-gradient(90deg, #E53935, #C62828);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 55px;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
        border: none;
    }

    /* Botão padrão (vermelho) */
    .stButton>button {
        background-color: #E53935;
        color: white;
    }

    .stButton>button:hover {
        background-color: #C62828;
        transform: scale(1.05);
    }

    /* Verde (sucesso) */
    .btn-green button {
        background-color: #2E7D32 !important;
    }

    /* Amarelo (alerta) */
    .btn-yellow button {
        background-color: #F9A825 !important;
        color: black !important;
    }

    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        background: #E53935;
        color: white;
        border-radius: 10px;
    }
    </style>
    """