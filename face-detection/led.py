import RPi.GPIO as GPIO
import time

# Configuración de los pines GPIO
LED_PIN_1 = 17  # Pin GPIO para el primer LED
LED_PIN_2 = 27  # Pin GPIO para el segundo LED

def configurar_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN_1, GPIO.OUT)
    GPIO.setup(LED_PIN_2, GPIO.OUT)

def controlar_leds(encender_primer_led):
    if encender_primer_led:
        GPIO.output(LED_PIN_1, GPIO.HIGH)
        GPIO.output(LED_PIN_2, GPIO.LOW)
    else:
        GPIO.output(LED_PIN_1, GPIO.LOW)
        GPIO.output(LED_PIN_2, GPIO.HIGH)

def limpiar_gpio():
    GPIO.cleanup()


def abrirPuerta(boolean):
    # Configurar GPIO antes de controlar los LEDs
    configurar_gpio()

    # Ejemplo de encender el primer LED
    controlar_leds(boolean)

    # Esperar unos segundos
    time.sleep(3)

    # Apagar todos los LEDs y limpiar GPIO
    controlar_leds(False)
    limpiar_gpio()


