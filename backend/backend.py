import os
import time

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

load_dotenv()

app = Flask(__name__)

# Permita a origem do front-end
CORS(app, origins=["http://localhost:5173"])

# Configuração do SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")  # "*" permite qualquer origem

# Lista de URLs para verificação
urls_to_check = [
    
    {"url": "https://url.com/login"},
]


# Configurações do Selenium
firefox_options = Options()
firefox_options.add_argument("--headless")  # Executar o Firefox sem interface gráfica
gecko_driver_path = r"geckodriver.exe"


def check_site_element(url):
    with webdriver.Firefox(
        service=Service(gecko_driver_path), options=firefox_options
    ) as driver:
        try:
            driver.get(url)
            # Realiza o login
            driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(
                os.getenv("EMAIL")
            )
            driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(
                os.getenv("PASSWORD")
            )
            driver.find_element(
                By.XPATH, "/html/body/div/main/div[1]/form/button"
            ).click()
            time.sleep(1)

            # Navega até o menu desejado
            driver.find_element(
                By.XPATH, "/html/body/div/div[1]/div[1]/div/ul/div/li[1]/a/div[1]"
            ).click()
            time.sleep(1)

            # Busca pelo elemento pai com os filhos
            elemento_pai = driver.find_element(By.TAG_NAME, "tbody")

            # Busca direta pela classe desejada no SVG
            svg_elementos = elemento_pai.find_elements(By.TAG_NAME, "svg")
            for svg in svg_elementos:
                classe = svg.get_attribute("class")
                if "MuiSvgIcon-colorSecondary" in classe:
                    print(f"Achei um icone de Echat fora!")
                    return True
            print("Não encontrei um icone de Echat fora!.")
            return False
        except Exception as e:
            print(f"Erro durante a execução:\n {e}")
            return True


@app.route("/verify-site", methods=["POST"])
def verify_site():
    for site in urls_to_check:
        is_present = check_site_element(site["url"])
        # Envia o resultado ao front-end após cada verificação
        socketio.emit(
            "site_checked", {"url": site["url"], "element_present": is_present}
        )
    return jsonify({"message": "Verificação completa"})


if __name__ == "__main__":
    socketio.run(app, debug=True)
