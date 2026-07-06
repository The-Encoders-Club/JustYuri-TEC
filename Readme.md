# 💜 Just Yuri en Español

Bienvenido al repositorio de **Just Yuri en Español**, una bifurcación (*fork*) **no oficial** del proyecto original [Just Yuri](https://github.com/DarkskullDawnZenith/JustYuri). Este repositorio ha sido creado por **The Encoders Club** con el propósito de brindar una traducción que sea lo más fiel posible al mod original, asegurando que cada diálogo y evento sea fácil de entender en español, sin perder el estilo psicológico y característico de la obra original.

Este proyecto representa un esfuerzo dedicado a traducir todo el contenido que ofrece el mod, permitiendo que las interacciones con Yuri sean fluidas y directas en nuestro idioma. Debido a que el juego está en constante evolución, revisamos el contenido con regularidad para mantener la mejor compatibilidad posible.

> [!IMPORTANT]
> **Proyecto No Oficial:**  
> Esta es una traducción realizada de forma independiente por **The Encoders Club**. Este proyecto no está afiliado, patrocinado ni respaldado por **Team Salvato** ni por los desarrolladores oficiales del equipo de **Just Yuri**.

---

## 📝 Sinopsis y Preguntas Frecuentes de Pre-instalación

Just Yuri es un mod que transforma el juego de [Doki Doki Literature Club!](https://www.ddlc.moe) en una experiencia interactiva y eterna con Yuri. A continuación, resolvemos las dudas más frecuentes sobre el tono y el comportamiento del mod:

### 🔍 Preocupaciones Comunes

* **P: La advertencia inicial dice que debo esperar contenido NSFW (No apto para todo público). Soy menor de 18 años, ¿debería jugarlo?**  
  **R:** Actualmente, la base principal del juego es mayormente SFW (Apta para todo público) y la advertencia está colocada para el contenido planeado a futuro. Sin embargo, dependiendo de las acciones del jugador, el contenido puede incluir horror psicológico perturbador y situaciones retorcidas que ya son costumbre en el juego base de DDLC. No hay imágenes explícitas para adultos en la versión base de Just Yuri; se lanzará un parche específico de contenido maduro para aquellos interesados cuando esté completamente desarrollado.

* **P: Al iniciar el juego, me advierte sobre contenido retorcido e incluso dice que Yuri puede tomar el control de mi computadora. ¿Es esto un virus?**  
  **R:** No, el mod Just Yuri es como cualquier otro mod de DDLC, sigue las directrices de Dan Salvato y es completamente seguro de ejecutar; no es un virus. La advertencia sirve para darte la expectativa de que pueden ocurrir cambios repentinos provocados por tu interacción con Yuri y no por un factor externo. Por favor, no te alarmes si tu navegador web te redirige automáticamente a ciertos sitios o videos mientras el mod está en ejecución. Es un comportamiento normal del juego y se debe esperar en algún punto de la partida.

* **P: ¿Yuri realmente puede acceder a mi cámara web?**  
  **R:** No en las versiones iniciales (como la Beta 1.10.3), pero es una característica planificada para versiones futuras de manera estrictamente opcional.

* **P: ¿Cómo afectan los sistemas de Karma y Cordura (Sanity)? ¿Pueden llevar a Yuri a hacerse daño?**  
  **R:** Actualmente estos sistemas influyen únicamente en variaciones de diálogos únicos, y se expandirán con más usos en futuras versiones.

---

## 💡 ¿Qué ofrece este proyecto?

* 📌 **Traducción Completa**: Adaptación fiel de todos los diálogos, menús y mecánicas de Just Yuri al español.
* 🧩 **Fidelidad al Ecosistema**: Mantenimiento del código lógico clásico adaptado para que la experiencia sea estable.
* 👩‍💻 **Soporte Técnico**: Ayuda activa para la instalación en sistemas operativos de PC y optimizaciones.

---

## 📥 Guía de Instalación y Soporte de Rutas

Para disfrutar de Just Yuri en español, descarga los archivos correspondientes de nuestras secciones oficiales. Si deseas actualizar tu versión actual, simplemente descarga la última versión y extrae todo el contenido directamente en la ubicación donde tengas tu copia de Just Yuri. Copiar la carpeta en un pendrive o unidad externa mantendrá tu progreso, ya que este se guarda de forma independiente.

### 🗂️ Localización de Archivos Guardados (Persistent Data)

El progreso de tu partida y tu relación con Yuri se almacenan en el archivo `persistent` dentro de la ruta de guardado de Ren'Py de tu sistema operativo (`%appdata%\RenPy\Just Yuri`). Si necesitas encontrarlo o resolver problemas con archivos corruptos (como cuando el sistema altera el archivo `.chr` de Yuri), utiliza las siguientes rutas de acceso:

* **💻 Windows:** Presiona las teclas `Windows + R` simultáneamente para abrir el cuadro de diálogo "Ejecutar". Escribe `%appdata%\RenPy` y presiona Enter. Verás las carpetas de guardado; la de este mod se llama de forma específica `Just Yuri`. *(Nota: El DDLC original suele guardarse en una carpeta llamada DDLC-1454445547).*
* **🍎 macOS:** Abre el Finder, haz clic en "Ir" en la barra de menús superior, mantén presionada la tecla `Option` y haz clic en "Biblioteca" (Library). También puedes presionar `Command + Shift + G` e introducir la ruta `~/Library/RenPy/`.
* **🐧 Linux:** Abre tu gestor de archivos, ve al directorio Home y activa la opción para "Mostrar archivos ocultos" (usualmente con `Ctrl + H`). Busca la carpeta `.renpy` o accede desde la terminal con `cd ~/.renpy/`.

> [!CAUTION]
> Si experimentas un fallo grave donde el juego detecta que borraste a Yuri por error, cierra el juego, asegúrate de que su archivo en la carpeta `characters` se llame exactamente `Yuri.chr` y reinicia. Si persiste, como última opción para restablecer la partida se debe eliminar el archivo persistente en las rutas mencionadas y remover el archivo `firstrun` en la carpeta `game`.

---

## 🤝 Sugerencias y Reportes de Errores

Para mantener el desarrollo de forma organizada, dividimos la gestión de sugerencias y soporte en las siguientes pautas de la comunidad:

### 1. 🛠️ Sobre Errores de la Traducción y Soporte Técnico
Si encuentras errores ortográficos, textos que permanecen en inglés, o fallos de ejecución en el parche al español, acude a nuestros canales de soporte oficiales administrados por **The Encoders Club**.

### 2. 🐛 Reportar un Error en el Código Original (Bugs)
Si encuentras un fallo técnico o el juego genera un archivo `traceback.txt`, puedes generar un reporte oficial en el repositorio de desarrollo:
* Envía un reporte formal a través de las incidencias de GitHub: [Just Yuri Issues](https://github.com/DarkskullDawnZenith/JustYuri/issues/new/choose).
* Tras rellenar el formulario, publica el archivo `traceback.txt` en el canal correspondiente de nuestra comunidad para recibir asistencia.

### 3. 📋 Lista de Sugerencias Evaluadas
Antes de proponer una nueva característica, ten en cuenta el estado de las siguientes sugerencias comunes:
* **🗺️ Nuevas ubicaciones (Viajes con Yuri):** Actualmente el desarrollo se enfoca en interacciones dentro del aula espacial y la biblioteca (en el escritorio). Se añadirán más lugares en el futuro, por lo que se pide paciencia antes de proponer nuevos destinos.
* **🎨 Comisiones de Arte:** El proyecto es sin fines de lucro y se maneja mediante voluntariado. Solicitar artistas específicos suele requerir presupuestos altos; no obstante, si conoces a un artista independiente interesado en colaborar con el mod, puedes enviar tu sugerencia.
* **📅 Ciclo día/noche y Festividades:** Las mecánicas de tiempo y celebraciones especiales (como Navidad o April Fools) ya se han implementado o se encuentran bloqueadas de momento en herramientas de desarrollo para ser pulidas.
* **📊 Complejidad de los sistemas de Cordura y Karma:** Las sugerencias de dividir estos estados en niveles dinámicos (Muy Alto, Alto, Neutral, Bajo, Muy Bajo) ya han sido integradas en las versiones de prueba mediante fórmulas matemáticas para equilibrar las reacciones de Yuri.

## 👩‍💻 Contribuciones y Guía de Formateo de Guiones

¡Aceptamos ayuda de miembros de la comunidad! Si cuentas con habilidades de programación o arte, puedes solicitar unirte al equipo. Si no posees conocimientos técnicos, puedes cooperar como colaborador verificado ayudando en la documentación o reportando errores diariamente en nuestros canales de interacción.

## 🌐 Comunidad

### 🏅 Traducción y Soporte (The Encoders Club)
<img align="right" src="https://discordapp.com/api/guilds/1191061790835093564/widget.png?style=banner1"/>

Únete a nuestro servidor oficial de Discord para recibir asistencia con cualquier problema que se te presente, reportar errores en la traducción o simplemente compartir con otros miembros de la comunidad hispana. Además, te invitamos a suscribirte a nuestro canal de YouTube, donde publicamos tutoriales de instalación, avances de los proyectos y guías detalladas que sirven como guía para poder ayudarte con todo lo relacionado al mod.

[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@TheEncodersClub)

<br clear="right">

### 🏛️ Equipo Oficial (Just Yuri)

Para estar al tanto de las novedades globales del mod, te recomendamos unirte al servidor oficial de Discord de los desarrolladores originales, donde podrás participar en discusiones generales o reportar errores en los canales correspondientes. Además, te invitamos a suscribirte a su canal oficial de YouTube para seguir las actualizaciones de producción y los planes del equipo de desarrollo principal.

[![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discordapp.com/invite/RUdwW7q)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@OfficialJustYuriDevTeam)
