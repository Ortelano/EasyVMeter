# Easy Vmeter: Monitorización Háptica Accesible

**Easy Vmeter** es un dispositivo de código abierto diseñado para facilitar la producción musical a personas con discapacidad visual. Permite monitorizar la ganancia de entrada y los niveles de audio mediante una respuesta vibratoria (háptica) en tiempo real.

## ✨ Características Principales
* **Protocolo Mackie Control:** Compatible de forma nativa con la mayoría de DAWs (Reaper, Pro Tools, etc.).
* **Feedback Táctil:** Traduce niveles de volumen (0 a 11) en diferentes intensidades de vibración.
* **Modo Solo:** Filtrado inteligente para centrarse únicamente en las partes más fuertes de la señal.
* **Seguridad Avanzada:** * Sistema de enfriamiento (cooldown) para evitar saturación del motor en eventos de clip.
  * Timeout automático de 0.5s si se pierde la señal MIDI para proteger el hardware.

## 🛠️ Hardware
* **Cerebro:** Waveshare RP2040-Zero.
* **Actuador:** Motor de vibración controlado por PWM (GP29).
* **Carcasa:** Archivos de diseño para impresión 3D incluidos (FreeCAD).

## 🚀 Instalación
1. Descarga el firmware de CircuitPython y cárgalo en tu RP2040-Zero.
2. Copia los archivos `boot.py`, `code.py` y la carpeta de librerías en la raíz del dispositivo.
3. Configura el dispositivo en tu DAW como una superficie de control Mackie Control (usa el puerto "EasyVMeter In/Out").

## 📂 Estructura del Repositorio
* `/Software`: Código fuente en CircuitPython y librerías necesarias.
* `/3D_Design`: Archivos FreeCAD y STLs para la carcasa.
* `/Docs`: Manual completo de usuario y montaje.

## 📺 Tutoriales en Vídeo
- [Introducción y Propósito](https://youtu.be/ggoi_HVR03I)
- [Hardware y Electrónica](https://youtu.be/q_lWQ2pnNio)
- [Diseño 3D (FreeCAD)](https://youtu.be/SDiyq6ZNVbk)
- [Análisis del Código](https://youtu.be/Rb0bXWAjWm8)
- [Demo e Integración DAW](https://youtu.be/bEbQwglQXCA)

---
*Desarrollado con el objetivo de hacer la producción musical accesible para todos.*
