from machine import Pin
from time import sleep_ms

DT_PIN = 19
SCK_PIN = 18

LIMITE_VAZIO = 150
LIMITE_CHEIO = 4900

dt = Pin(DT_PIN, Pin.IN)
sck = Pin(SCK_PIN, Pin.OUT)
sck.value(0)


def ler_hx711():
    if dt.value() == 1:
        return None

    valor = 0

    for _ in range(24):
        sck.value(1)
        valor = (valor << 1) | dt.value()
        sck.value(0)

    # Pulso extra para finalizar a leitura
    sck.value(1)
    sck.value(0)

    if valor & 0x800000:
        valor -= 1 << 24

    return valor


def converter_para_gramas(valor_bruto):
    peso = round(valor_bruto / 420.0)

    if peso < 0:
        peso = 0

    return peso


reposicao_pendente = False
sensor_ativo = False

estado = "inicio"
ultimo_peso = None

print("Sistema Kanban Inicializado")


while True:
    leitura = ler_hx711()

    if leitura is None:
        sleep_ms(10)
        continue

    peso = converter_para_gramas(leitura)

    if peso > 0:
        sensor_ativo = True

    if sensor_ativo:

        if peso == 0:
            if estado != "erro":
                print(
                    "ALERTA: Caixa ausente ou erro de calibração no sensor HX711!"
                )

            estado = "erro"

        elif peso <= LIMITE_VAZIO:
            if not reposicao_pendente:
                print(
                    "Evento de reposição disparado! Caixa vazia detectada."
                )
                reposicao_pendente = True

            estado = "vazio"

        elif peso >= LIMITE_CHEIO:
            if reposicao_pendente:
                print("Abastecimento concluído. Caixa cheia.")
                reposicao_pendente = False

            estado = "cheio"

        else:
            if estado != "regular" or peso != ultimo_peso:
                print("Status: Estoque Regular ({}g)".format(peso))

            estado = "regular"

    ultimo_peso = peso

    sleep_ms(50)
