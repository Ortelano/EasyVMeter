import usb_midi
import storage

try:
    usb_midi.set_names(
         streaming_interface_name="strEasyVMeter",
         audio_control_interface_name="EasyVMeter",
         in_jack_name="EasyVMeter In",
         out_jack_name="EasyVMeter Out"
     )
    print("Nombres MIDI establecidos en boot.py usando usb_midi.set_names")
except AttributeError:
    print("Advertencia: No se pudo usar usb_midi.set_names.")
     
try:
    storage.disable_usb_drive()
    print("Usb desactivado")
except AttributeError:
          print("Advertencia: No se pudo usar storage.disable_usb_drive.")