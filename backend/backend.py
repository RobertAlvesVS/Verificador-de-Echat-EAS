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
    {"url": "https://laboclin.eassystems.com.br/login"},
    {"url": "https://cardioprev.eassystems.com.br/login"},
    {"url": "https://navarro.eassystems.com.br/login"},
    {"url": "https://oftalmovilas.eassystems.com.br/login"},
    {"url": "https://carvillas.eassystems.com.br/login"},
    {"url": "https://amoedo.eassystems.com.br/login"},
    {"url": "https://icb.eassystems.com.br/login"},
    {"url": "https://odccajaz.eassystems.com.br/login"},
    {"url": "https://cfisio.eassystems.com.br/login"},
    {"url": "https://hospitalsea.eassystems.com.br/login"},
    {"url": "https://hospolhosantbarbosa.eassystems.com.br/login"},
    {"url": "https://angiclin.eassystems.com.br/login"},
    {"url": "https://fazendafelicita.eassystems.com.br/login"},
    {"url": "https://guirra.eassystems.com.br/login"},
    {"url": "https://holhos.eassystems.com.br/login"},
    {"url": "https://otorhinus.eassystems.com.br/login"},
    {"url": "https://rcs.eassystems.com.br/login"},
    {"url": "https://wisetech.eassystems.com.br/login"},
    {"url": "https://agnusdei.eassystems.com.br/login"},
    {"url": "https://biomol.eassystems.com.br/login"},
    {"url": "https://maxbe.eassystems.com.br/login"},
    {"url": "https://hsaomatheuscirurgia.eassystems.com.br/login"},
    {"url": "https://clinday.eassystems.com.br/login"},
    {"url": "https://erasmo.eassystems.com.br/login"},
    {"url": "https://espacoabsolut.eassystems.com.br/login"},
    {"url": "https://otorhinusfilial.eassystems.com.br/login"},
    {"url": "https://prover.eassystems.com.br/login"},
    {"url": "https://salvador.eassystems.com.br/login"},
    {"url": "https://seta.eassystems.com.br/login"},
    {"url": "https://sst.eassystems.com.br/login"},
    {"url": "https://wfg.eassystems.com.br/login"},
    {"url": "https://dnmaster.eassystems.com.br/login"},
    {"url": "https://echat.eassystems.com.br/login"},
    {"url": "https://alianca.eassystems.com.br/login"},
    {"url": "https://echat2.eassystems.com.br/login"},
    {"url": "https://apg.eassystems.com.br/login"},
    {"url": "https://qockpit.eassystems.com.br/login"},
    {"url": "https://rodoclinica.eassystems.com.br/login"},
    {"url": "https://vocetotal.eassystems.com.br/login"},
    {"url": "https://bns.eassystems.com.br/login"},
    {"url": "https://diagnoplus.eassystems.com.br/login"},
    {"url": "https://ivaclinica.eassystems.com.br/login"},
    {"url": "https://laboclinpernambues.eassystems.com.br/login"},
    {"url": "https://cardiovascular.eassystems.com.br/login"},
    {"url": "https://silvestre.eassystems.com.br/login"},
    {"url": "https://bb.eassystems.com.br/login"},
    {"url": "https://pitapoan.eassystems.com.br/login"},
    {"url": "https://climego.eassystems.com.br/login"},
    {"url": "https://itapoanmed.eassystems.com.br/login"},
    {"url": "https://priovermelho.eassystems.com.br/login"},
    {"url": "https://clioc.eassystems.com.br/login"},
    {"url": "https://vita.eassystems.com.br/login"},
    {"url": "https://laboclingrupo.eassystems.com.br/login"},
    {"url": "https://odontosim.eassystems.com.br/login"},
    {"url": "https://klingo.eassystems.com.br/login"},
    {"url": "https://antbarbosa.eassystems.com.br/login"},
    {"url": "https://laboclincanela.eassystems.com.br/login"},
    {"url": "https://exame.eassystems.com.br/login"},
    {"url": "https://vida.eassystems.com.br/login"},
    {"url": "https://iel.eassystems.com.br/login"},
    {"url": "https://aa.eassystems.com.br/login"},
    {"url": "https://modernasany.eassystems.com.br/login"},
    {"url": "https://colp.eassystems.com.br/login"},
    {"url": "https://cmulher.eassystems.com.br/login"},
    {"url": "https://coracaodovale.eassystems.com.br/login"},
    {"url": "https://qualivida.eassystems.com.br/login"},
    {"url": "https://laboclinfeira.eassystems.com.br/login"},
    {"url": "https://medpless.eassystems.com.br/login"},
    {"url": "https://centromedicoantbarbosa.eassystems.com.br/login"},
    {"url": "https://laboclinqualidade.eassystems.com.br/login"},
    {"url": "https://laboclinareatecnica.eassystems.com.br/login"},
    {"url": "https://irba.eassystems.com.br/login"},
    {"url": "https://laboclinrh.eassystems.com.br/login"},
    {"url": "https://perfinor.eassystems.com.br/login"},
    {"url": "https://medjan.eassystems.com.br/login"},
    {"url": "https://uros.eassystems.com.br/login"},
    {"url": "https://hsaomatheus.eassystems.com.br/login"},
    {"url": "https://procardiaco.eassystems.com.br/login"},
    {"url": "https://cotefi.eassystems.com.br/login"},
    {"url": "https://nutriclin.eassystems.com.br/login"},
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
