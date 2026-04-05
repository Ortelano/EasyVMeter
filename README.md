# EasyVMeter
Haptic Input Gain Monitoring System

Easy Vmeter: Monitorización háptica para una producción accesible

Este proyecto nace de una experiencia personal en mis clases de sonido. Durante varios años, he trabajado con un alumno invidente utilizando Reaper y herramientas como OSARA. Aunque hemos logrado avanzar muchísimo en composición y mezcla, nos encontramos con un obstáculo crítico: la gestión de la ganancia de entrada. Las soluciones actuales solo avisan cuando la señal ya ha clipado, lo cual es insuficiente para realizar una grabación profesional de forma autónoma.
Ante este reto, decidí diseñar una herramienta que tradujera los niveles de señal en vibraciones físicas. Easy Vmeter es un dispositivo basado en el procesador RP2040 que emula una superficie de control MIDI. Al utilizar el protocolo Mackie Control, el dispositivo es capaz de capturar la información de nivel del DAW (por defecto, el canal 1) y convertirla en una respuesta háptica en tiempo real. Al ser un protocolo estándar, el dispositivo es compatible con la gran mayoría de los DAW del mercado.
Mi objetivo es que esta herramienta sea accesible para todos. Por ello, comparto este proyecto de forma Open Source, incluyendo el código, los diseños de FreeCAD para la carcasa 3D y toda la documentación necesaria para que cualquier persona pueda construirlo y mejorar su flujo de trabajo.
