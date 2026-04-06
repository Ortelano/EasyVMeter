import usb_midi  # Importa la librería para configurar el dispositivo USB como MIDI.
import storage    # Importa la librería para controlar el almacenamiento USB.

# --- Configuración de Nombres del Dispositivo MIDI USB ---
# Este bloque 'try...except' intenta establecer nombres descriptivos para los interfaces MIDI USB.
# Esto ayuda a identificar el dispositivo más fácilmente en DAWs (Digital Audio Workstations)
# y otros programas que listan dispositivos MIDI.
try:
    # usb_midi.set_names() permite personalizar los nombres que aparecen en el sistema operativo.
    # 'streaming_interface_name': Nombre del interfaz de flujo principal (a menudo la "tarjeta de sonido" virtual).
    # 'audio_control_interface_name': Nombre del interfaz de control de audio.
    # 'in_jack_name': Nombre del puerto MIDI de entrada visible en el software.
    # 'out_jack_name': Nombre del puerto MIDI de salida visible en el software.
    usb_midi.set_names(
        streaming_interface_name="strEasyVMeter",
        audio_control_interface_name="EasyVMeter",
        in_jack_name="EasyVMeter In",
        out_jack_name="EasyVMeter Out"
    )
    # Mensaje de confirmación en la consola serial si la operación fue exitosa.
    print("Nombres MIDI establecidos en boot.py usando usb_midi.set_names")
except AttributeError:
    # Si la función usb_midi.set_names no existe en esta versión de CircuitPython,
    # o si los parámetros son incorrectos, se capturará un AttributeError.
    # Esto es una advertencia, ya que el dispositivo seguirá funcionando, pero con nombres por defecto.
    print("Advertencia: No se pudo usar usb_midi.set_names. Es posible que esta función no exista en la versión de CircuitPython.")

# --- Desactivación del Acceso al Disco USB ---
# Este bloque 'try...except' intenta deshabilitar el acceso al almacenamiento USB (como una unidad de disco).
# Esto es útil en dispositivos que no necesitan ser vistos como un disco para el usuario final,
# liberando recursos y evitando problemas de corrupción si el usuario intenta escribir en él.
try:
    # storage.disable_usb_drive() desactiva la función de unidad de disco USB del dispositivo.
    storage.disable_usb_drive()
    # Mensaje de confirmación en la consola serial si la operación fue exitosa.
    print("Usb desactivado")
except AttributeError:
    # Si la función storage.disable_usb_drive no existe en esta versión de CircuitPython,
    # se capturará un AttributeError. El dispositivo podría seguir mostrando el disco USB.
    print("Advertencia: No se pudo usar storage.disable_usb_drive. Es posible que esta función no exista en la versión de CircuitPython.")