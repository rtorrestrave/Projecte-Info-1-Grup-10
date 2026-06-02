# ✈️ AIRPORT MANAGER - PROYECTO I1

## 👥 Integrantes del Grupo 10 (2A31)
* **Roger Torres**
* **Meritxell De Lorenzo**
* **Joan Gimeno**

---

## 📺 Demostraciones en Vídeo (Evolución del Proyecto)
Puedes ver el progreso y funcionamiento de la aplicación a lo largo de sus distintas fases de desarrollo a través de los siguientes enlaces a YouTube:

* **[Video Demostración V.1](https://youtu.be/9NLoZOT1JcQ)** ─ Primera aproximación y bases de la interfaz.
* **[Video Demostración V.2](https://youtu.be/gvJGybzJLUg)** ─ Integración de funcionalidades core y optimización de datos.
* **[Video Demostración V.3](https://youtu.be/gpKJxnHjpuI)** ─ Versión final con diseño avanzado y herramientas extra integradas.

---

## 🛠️ Descripción de Funciones Extra

La aplicación incluye un robusto conjunto de herramientas complementarias que expanden las capacidades de gestión del aeropuerto y mejoran la experiencia de usuario:

### 💾 Autosave (Guardado Automático)
El sistema cuenta con un mecanismo de persistencia automatizado. Cada vez que se realizan modificaciones críticas en los paneles o tablas de vuelos, la aplicación salva los cambios en segundo plano sin interrumpir al usuario, previniendo cualquier pérdida de datos ante cierres inesperados.

### 🌗 Modo Oscuro / Claro
Interfaz adaptativa que permite alternar visualmente entre un tema oscuro (diseñado para reducir la fatiga ocular en entornos de baja luminosidad) y un tema claro de alta visibilidad. El cambio de paleta de colores se aplica de forma fluida a todos los widgets y contenedores de la aplicación.

### 🌐 Idioma (Multilenguaje Dinámico)
Soporte completo para múltiples idiomas (Español, Catalán e Inglés). Al seleccionar una bandera o control de idioma, todo el árbol de componentes e interfaces de la aplicación se re-inyecta de manera instantánea en caliente, traduciendo etiquetas, botones y menús sin necesidad de reiniciar el software.

### 📡 Despacho ACARS
Módulo dedicado a la simulación y tratamiento de mensajes del sistema *Aircraft Communication Addressing and Reporting System* (ACARS). Permite gestionar las comunicaciones digitales operativas entre las aeronaves en ruta y la torre de control de la estación aeroportuaria.

### 🌤️ METEO (Información Meteorológica)
Sección encargada de procesar e interpretar datos del estado del tiempo actual y previsiones (informes METAR/TAF). Es crucial para la toma de decisiones respecto a las pistas activas, demoras operativas y seguridad de los despegues y aterrizajes.

### 📊 AODB (Airport Operational Database)
El corazón de los datos del sistema. Este módulo gestiona de forma centralizada la base de datos de operaciones aeroportuarias, cruzando información en tiempo real sobre asignación de slots, parkings, Gates e incidencias de los vuelos activos.

### ⏱️ Reloj en Tiempo Real
Un cronómetro persistente e integrado directamente en la barra de estado de la interfaz principal. Se actualiza segundo a segundo sincronizado con la hora del sistema (o un huso UTC aeronáutico) para mantener una referencia temporal exacta durante la gestión de las operaciones.

### 🎨 Logo Personalizado
Identidad corporativa e iconografía adaptada e integrada en la cabecera y ventanas del software. Aporta un diseño profesional y facilita la identificación visual inmediata de la marca del gestor aeroportuario.

### 🌍 Apertura Automática de Google Earth
Integración externa automatizada que enlaza las coordenadas o datos de rutas de los vuelos de la aplicación directamente con Google Earth. Al activar esta función, el sistema arranca de forma autónoma la plataforma geográfica para visualizar de manera tridimensional los mapas y trayectorias reales de aproximación.
