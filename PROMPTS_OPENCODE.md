# Trazabilidad del uso de OpenCode

**Proyecto:** Evaluación empírica de sockets TCP de bajo nivel frente a gRPC en
streaming unidireccional y bidireccional para telemetría de alta frecuencia.

**Autor:** Steven Alexis Chango Vela.

**Curso:** Sistemas Distribuidos y Paradigmas de la Computación.

**Herramienta:** OpenCode (agente de codificación en terminal), modelo declarado
por el entorno `DeepSeek V4.1 Flash Free` (proveedor OpenCode), sobre Windows 11
(10.0.26300), Python 3.13.14, gRPC 1.85.1 y Quarto 1.11.9.

**Fecha de la sesión documentada:** 14 de noviembre de 2026 (zona local
−05:00). La cronología se reconstruye a partir de los dos commits del
repositorio, de las marcas de tiempo de los archivos y de los artefactos
generados; no se conserva una transcripción completa de la sesión.

---

## 1. Propósito y alcance

Este documento registra, de forma cronológica y verificable, cómo se utilizó
OpenCode durante la investigación: qué instrucciones se dieron, qué tareas
ejecutó el agente, qué decisiones y verificaciones correspondieron al
investigador, qué errores se detectaron y cómo se corrigieron.

No es un registro de autoría. Las decisiones metodológicas, la aprobación de
los resultados y la responsabilidad sobre el contenido son del investigador.
El agente actuó como asistente de programación, análisis y redacción.

**Convención de este registro.** Los prompts 1–5 y 7 se recogen como síntesis
(los cinco primeros ya figuraban así en la primera versión de este archivo);
los prompts 6 y 8 se transcriben literalmente y el 9 como extracto. Se indica en
cada caso. No se atribuyen al investigador revisiones que no estén respaldadas
por el registro.

---

## 2. Resumen de responsabilidades

| Artefacto | Asistencia de la IA | Verificación humana |
|---|---|---|
| `src/` (protocolo, clientes, servidores, orquestador) | Redacción del código, estructura modular, manejo de errores | Supervisión del código y de las decisiones de diseño; ejecución de las pruebas |
| `results.csv` (1760 ejecuciones) | Generación del banco y de los comandos de ejecución | Ejecución en su equipo y aceptación del conjunto de datos |
| `analysis/`, `figures/`, `tables/` | Script de análisis, figuras, tablas y macros | Revisión del procedimiento estadístico y de las salidas |
| `references.bib` | Propuesta y formateo de entradas | Verificación de cada fuente (DOI, volumen, páginas) |
| `article.qmd` | Redacción y compilación | Revisión del manuscrito y de las conclusiones |
| `_quarto.yml`, plantilla IEEE | Configuración y comprobación de la plantilla | Aceptación de la plantilla y del formato |

El agente ejecutó comandos de shell (Python, Quarto, pdfTeX, Git) leyendo y
escribiendo archivos del repositorio. Todas las operaciones quedaron en el
árbol de trabajo y son reproducibles desde los archivos versionados.

---

## 3. Cronología

| Hora (aprox.) | Etapa | Evidencia |
|---|---|---|
| 00:17–00:23 | Configuración del entorno y del repositorio | commit `d92b3cb` |
| 00:35–00:57 | Programación del banco de pruebas | `src/*.py`, commit `fbf5561` (00:53) |
| 01:14 | Bibliografía | `references.bib` |
| 01:15 | Primer registro de prompts | `PROMPTS_OPENCODE.md` v1 |
| 01:26–01:30 | Verificación de la plantilla IEEE | `verificacion-plantilla-ieee.pdf` |
| 01:30–06:25 | Ejecución experimental | `results.csv` (1760 filas) |
| 06:25–06:54 | Análisis, tablas, figuras y artículo | `analysis/`, `tables/`, `figures/`, `article.pdf` |

---

## 4. Etapas

### 4.1. Definición del trabajo y restricciones

**Prompt 1 (síntesis).**

> Proyecto para el curso de Sistemas Distribuidos y Paradigmas de la
> Computación: evaluar empíricamente sockets TCP de bajo nivel frente a gRPC en
> streaming unidireccional y bidireccional para telemetría de alta frecuencia.
> Entregar un artículo en formato IEEE de 3–4 páginas (`article.qmd`),
> `references.bib` con 5–8 referencias verificables, `results.csv` con datos
> reales medidos, `README.md`, `_quarto.yml` y este archivo. El repositorio debe
> ser público en GitHub.

Restricciones indicadas en la misma instrucción:

- No inventar resultados, autores, DOI, volúmenes, páginas ni explicaciones.
- Si una ejecución falla, reportar el error; no sustituir los datos.
- No presentar RTT/2 como latencia de un solo sentido.
- No atribuir a «la red» diferencias medidas en localhost.

**Trabajo asistido.** El agente propuso la estructura del repositorio y el
desglose de entregables. **Verificación humana.** El investigador fijó el
alcance y las restricciones, que se mantuvieron sin cambios durante el resto
del trabajo.

### 4.2. Diseño metodológico

**Prompt 2 (síntesis).**

> Propón y justifica la matriz experimental: payloads, número de mensajes,
> calentamiento, repeticiones, ritmos, concurrencia, afinidad de CPU y
> contrabalanceo del orden. Debe distinguir OWD, RTT y tiempo de procesamiento,
> y documentar los costes de serialización y framing.

**Decisiones aprobadas y congeladas antes de medir:**

- Payloads: 64, 256, 1024 y 4096 B.
- 2000 mensajes medidos por ejecución; calentamiento `max(500 msg, 2 s)`.
- 30 réplicas por celda en el bloque principal y en el de escalado; 5 en
  throughput.
- Ritmos: 100, 500 y 1000 Hz.
- Concurrencia: `C = 1` principal; `C ∈ {4, 16}` a 1024 B y 500 Hz.
- OWD medida con `time.perf_counter_ns()` compartido entre cliente y servidor;
  RTT solo en bidireccional y reportado como RTT.

**Trabajo asistido.** El agente propuso la matriz y justificó la elección de
Mann–Whitney, la unidad de análisis (la ejecución, no el mensaje) y el umbral
de relevancia práctica del 10 %. **Verificación humana.** El investigador
aprobó la matriz y el procedimiento antes de la ejecución; esos parámetros no
se modificaron después de ver los datos.

### 4.3. Investigación bibliográfica

**Instrucción registrada (derivada del prompt 1, sin prompt independiente).**
Identificar entre 5 y 8 fuentes verificables sobre gRPC, HTTP/2, serialización y
evaluación de rendimiento, y formalizarlas en `references.bib` con citas
utilizables en el artículo.

**Trabajo asistido.** El agente localizó las fuentes, redactó las entradas
BibTeX y las conectó con el texto. **Verificación humana.** El investigador
comprobó cada entrada (autores, título, medio, año, volumen, páginas y DOI o
URL del editor). No se incluyeron fuentes sin localizador verificable.

**Resultado.** Ocho referencias en `references.bib`, todas citadas en el
artículo ([1]–[8]).

### 4.4. Programación del banco de pruebas

**Prompt 3 (síntesis).**

> Implementa el benchmark de forma modular, documentada y reproducible. Debe
> capturar latencia, RTT (solo en bidireccional), throughput, CPU y memoria;
> manejar errores, timeouts y cierre limpio; usar `time.perf_counter_ns()`; no
> generar datos falsos.

**Trabajo asistido.** El agente escribió los módulos (`protocol.py`,
`metrics.py`, `client_tcp.py`, `server_tcp.py`, `client_grpc.py`,
`server_grpc.py`, `run_benchmark.py`) y el orquestador de procesos. Diseño
implementado:

- TCP: prefijo de longitud de 4 B en orden de red + `!QQ` (secuencia y marca
  de envío) + payload; 20 B de cabecera; `TCP_NODELAY`; una escritura por
  mensaje.
- gRPC: `grpc.aio`, client-streaming (unidireccional) y bidi (bidireccional),
  protobuf, compresión deshabilitada.
- Una conexión física por ejecución, `C` flujos lógicos; en TCP el
  identificador viaja en los 16 bits altos de la secuencia.
- Servidor en CPU 0–1, cliente en CPU 2–3; procesos nuevos por ejecución.

**Verificación humana.** El investigador supervisó el código y las decisiones
de protocolo. La reproducibilidad se apoyó en el `README.md` y en
`requirements.txt`.

**Incidencia corregida.** Al encadenar varias tandas sobre el mismo CSV, el
índice de ejecución podía repetirse y sobrescribir datos crudos. Se añadió la
opción `--append` con un índice base (`base_index`) para que `run_id` no se
reutilizara; el cambio está en el diff de `src/run_benchmark.py` respecto del
commit `fbf5561`.

### 4.5. Validación y ejecución experimental

**Prompt 4 (síntesis).**

> Ejecuta un perfil de humo y verifica que las cuatro combinaciones funcionan en
> todos los ritmos y niveles de concurrencia antes de lanzar el experimento
> completo.

**Prompt 5 (síntesis).**

> Lanza el perfil `design` completo con procesos nuevos por ejecución y conserva
> los datos crudos y el registro de progreso.

**Resultado del humo.** 32/32 celdas `ok`, sin pérdidas ni mensajes sin
emparejar.

**Resultado de la ejecución.** 1760 ejecuciones (1440 principales, 240 de
escalado y 80 de throughput), 72 celdas, todas con estado `ok`.

**Comprobaciones de integridad** (`analysis/validation.json`, SHA-256 de
entrada `138b6d34…15e4d`):

| Comprobación | Resultado |
|---|---|
| Filas / `run_id` únicos | 1760 / 1760 |
| Pérdidas de mensajes | 0 ejecuciones |
| Mensajes sin emparejar | 0 |
| Déficit de ritmo > 1 % | 1 ejecución (491.75 msg/s frente a 500 Hz, 1.65 %) |
| Lateness p99 > periodo | 1013 ejecuciones |
| Atípicos robustos (> 6 MAD) | 362, conservados |

**Verificación humana.** El investigador ejecutó el experimento en su equipo y
aceptó el conjunto de datos. La ejecución con déficit de ritmo se conservó
porque no hubo pérdida y la unidad de análisis es la ejecución; los atípicos se
conservaron porque el análisis usa medianas, rangos y δ de Cliff.

### 4.6. Análisis estadístico

**Prompt 6 (literal).**

> Analiza estadísticamente los datos reales de results.csv. Compara los cuatro
> escenarios experimentales TCP unidireccional, TCP bidireccional, gRPC
> unidireccional y gRPC bidireccional. Calcula media, mediana, desviación
> estándar, percentiles P95 y P99 cuando el número de muestras lo permita,
> throughput y diferencias porcentuales. Analiza CPU y memoria. Genera gráficos
> científicos comparativos con títulos, ejes, unidades y leyendas. Evalúa la
> hipótesis H0 y H1 utilizando un procedimiento estadístico apropiado y
> justificando su elección. Distingue significancia estadística de relevancia
> práctica. Explica las ventajas y limitaciones de cada tecnología, los costos
> de abstracción, serialización y comunicación. Identifica anomalías y
> limitaciones experimentales. No inventes explicaciones ni resultados.
> Conserva los datos originales y genera los archivos de análisis y gráficos
> necesarios para incorporarlos en Quarto. Presenta los resultados y DETENTE.

**Procedimiento adoptado.** Unidad de análisis = ejecución. Mann–Whitney U
bilateral por celda (30 vs 30); Holm–Bonferroni por familia de métricas; δ de
Cliff e IC bootstrap (4000 remuestreos); relevancia práctica si el cambio
relativo de medianas alcanza el 10 % tras Holm.

**Trabajo asistido.** El agente generó 19 CSV, 5 tablas LaTeX, 9 figuras
(PDF y PNG), `validation.json`, `REPORT.md` y `key_numbers.tex`.

**Incidencias detectadas y corregidas en esta etapa:**

1. Las familias de contrastes estaban mezcladas en un solo bloque. Se
   separaron en `tests` (24), `scaling_tests` (4) y `throughput_tests` (8),
   que es el número correcto de comparaciones por familia.
2. `table_resources` agregaba con media porque `pivot_table` usa ese valor por
   defecto, mientras los macros usaban mediana. Se fijó `aggfunc="median"` y
   la tabla coincidió con `key_numbers.tex`.
3. La tabla de contrastes mostraba `p = 0.00` y era demasiado ancha. Se
   sustituyó por `<0.001` y se eliminó la columna de etiqueta de efecto.
4. Faltaba explicitar la potencia: con 5 réplicas por celda, el p bilateral
   mínimo de Mann–Whitney es 0.0079 y Holm sobre 8 contrastes lo eleva a
   0.0635. Se documentó que la familia de throughput **no puede** rechazar H0
   con ese diseño y que su resultado es descriptivo, no confirmatorio.
5. El agregado de latencia ocultaba una inversión de signo: en bidireccional a
   1000 Hz gRPC tiene menor p50 en los cuatro payloads. Se añadió el análisis
   de esa anomalía (p50 menor, p99 entre 38.6 % y 60.2 % mayor).

**Verificación humana.** El investigador aprobó el criterio de análisis
(unidad = ejecución, Mann–Whitney con Holm por familia, umbral práctico del
10 %) y recibió el informe `analysis/REPORT.md` antes de la redacción del
artículo.

### 4.7. Verificación de la plantilla IEEE

**Prompt 7 (síntesis).** Comprobar que la plantilla IEEE
Conference utilizada es real y verificable, y que el documento de prueba
produce las marcas esperadas.

**Trabajo asistido.** El agente descartó `quarto-journals/ieee` (respuesta 404)
y adoptó `dfolio/quarto-ieee` v1.1.0, verificada contra el `IEEEtran.cls` de
TeX Live (misma huella SHA-256). Comprobó Quarto 1.11.9, pdfTeX de TeX Live
2026 y `IEEEtran.cls` V1.8b; generó `verificacion-plantilla-ieee.qmd/pdf` con
una página, cita `[1]`, `[2]`, `Fig. 1` y `Tabla I`.

**Verificación humana.** El investigador aceptó la plantilla y el formato
antes de redactar el artículo.

### 4.8. Elaboración del artículo

**Prompt 8 (literal).**

> Redacta articulo.qmd utilizando los datos experimentales reales, metodología
> aprobada, análisis estadístico y referencias bibliográficas verificadas. El
> artículo debe cumplir la estructura IEEE Conference y tener entre 3 y 4
> páginas. Incluye: título, autor (Chango Vela Steven Alexis), resumen,
> palabras clave, introducción, trabajos relacionados, metodología
> experimental, configuración del benchmark, resultados, discusión técnica,
> amenazas a la validez, conclusiones y referencias. Utiliza citas BibTeX
> vinculadas con references.bib. Incorpora tablas y gráficos generados a
> partir de results.csv. El análisis debe ser crítico, objetivo y basado en
> evidencia. No inventes resultados, fuentes, experimentos ni afirmaciones.
> Mantén alta densidad técnica y redacción académica. Evita afirmaciones
> absolutas que no estén respaldadas por los resultados. Compila el PDF y
> verifica que cumpla las 3 a 4 páginas. Si hay errores, informa cuáles son. Al
> terminar, DETENTE.

**Trabajo asistido.** El agente redactó el manuscrito completo, lo compiló y
verificó el número de páginas con extracción de texto del PDF.

**Incidencias detectadas y corregidas:**

1. El primer borrador ocupaba 5 páginas. Se eliminó la figura de recursos y la
   tabla de latencia de 16 filas (la Fig. 1 y la tabla de contrastes cubren la
   misma evidencia) y se ajustó la prosa. Resultado: 4 páginas.
2. Pandoc escapaba `~` como `\textasciitilde{}`, de modo que el PDF imprimía
   «Fig.~1» y «Tabla~I». Se sustituyeron las cuatro referencias cruzadas.
3. Dos cifras no coincidían con `results.csv`: el ejemplo de latencia decía
   «743 → 189 µs» (el valor real es 745.5 → 191.4 µs) y el rango de throughput
   decía «90–94 %» (el mínimo real es 89.4 %). Ambas se corrigieron contra los
   datos.
4. Dos tablas se salían de la columna (2.71 pt y 6.11 pt). Se añadió
   `\setlength{\tabcolsep}{5pt}` en el generador y se regeneraron; el log de
   LaTeX quedó sin avisos.
5. La afiliación no se imprime: IEEEtran en modo conferencia ignora el
   `\thanks` que emite la plantilla (comprobado con un documento mínimo). Se
   reportó como limitación de la plantilla; no se inventó una institución.

**Verificación humana.** El investigador revisó el manuscrito y las
conclusiones antes de la entrega. Las tablas y figuras se generan desde
`results.csv` mediante `src/analysis.py`, de modo que su correspondencia es
reproducible.

### 4.9. Documentación de la trazabilidad

**Prompt 9 (literal, extracto).**

> Crea PROMPTS_OPENCODE.md para documentar la trazabilidad ética del uso de
> OpenCode en esta investigación. Registra los prompts principales utilizados
> durante las etapas de diseño metodológico, investigación bibliográfica,
> programación del benchmark, ejecución experimental, análisis estadístico y
> elaboración del artículo. Documenta qué tareas fueron asistidas por IA, qué
> resultados fueron verificados por el investigador, qué errores o
> inconsistencias se detectaron y qué correcciones humanas se aplicaron.
> Incluye una declaración de integridad académica […]. No afirmes revisiones o
> correcciones que no hayan ocurrido realmente. Organiza el documento de forma
> cronológica y transparente.

---

## 5. Registro consolidado de errores e inconsistencias

| # | Error o inconsistencia | Cómo se detectó | Corrección aplicada | Origen |
|---|---|---|---|---|
| 1 | `quarto-journals/ieee` no existe (404) | Comprobación de la URL | Se adoptó `dfolio/quarto-ieee` v1.1.0 y se validó el `IEEEtran.cls` | Agente; plantilla aprobada por el investigador |
| 2 | Familias de contrastes mezcladas | Revisión de conteos (24/4/8) | Separación en `tests`, `scaling_tests`, `throughput_tests` | Agente |
| 3 | Tabla de recursos con media en vez de mediana | Contraste tabla vs macros | `aggfunc="median"` y regeneración | Agente; coherencia verificada |
| 4 | `p = 0.00` en la tabla de contrastes | Lectura del `.tex` generado | Formato `<0.001`; columna de efecto eliminada | Agente |
| 5 | `run_id` repetido al encadenar tandas | Revisión del orquestador antes de reanudar | Opción `--append` con `base_index` | Agente |
| 6 | Caracteres Unicode (`−`, `·`, `µ`, `±`) rompían pdfLaTeX | Fallo de compilación | Macros LaTeX y prosa equivalente | Agente |
| 7 | `\|x − mediana\| > 6·MAD` sin definir en Unicode | Fallo de compilación | Se escribió en prosa | Agente |
| 8 | `~` literal impreso como `\textasciitilde{}` | Extracción de texto del PDF | Sustitución por espacios en 4 referencias cruzadas | Agente |
| 9 | «743 → 189 µs» no coincidía con los datos | Contraste con `results.csv` | «745.5 → 191.4 µs» (macros) | Agente |
| 10 | Rango de throughput «90–94 %» inexacto | Cálculo de los 8 cocientes | «89–94 %» | Agente |
| 11 | Tablas fuera de columna (2.71 pt y 6.11 pt) | `Overfull \hbox` del log | `\tabcolsep = 5pt` en el generador | Agente |
| 12 | Borrador de 5 páginas | Conteo de páginas del PDF | Recorte de figura y tabla redundantes; prosa ajustada | Agente; alcance fijado por el investigador |
| 13 | Afiliación no impresa por IEEEtran | Comparación con documento mínimo | Se reportó; no se forzó una solución | Agente |

**Sobre el alcance de las correcciones.** Las correcciones 2–11 fueron
detectadas y aplicadas por el agente durante las tareas solicitadas; las
correcciones 1 y 12 implicaron decisiones de alcance del investigador (elección
de plantilla y recorte a cuatro páginas); la 13 se reportó sin corregir.
Ninguna alteró `results.csv`: los datos crudos conservan su SHA-256
(`138b6d34…15e4d`). La validación final del conjunto corresponde al
investigador, según la declaración de la sección 6.

**Incidencia ajena al análisis.** Durante la configuración de Git se utilizó un
token de acceso personal en la línea de comandos, que quedó expuesto en la
transcripción de la sesión. Se recomendó revocarlo; este documento no contiene
su valor y no consta su revocación al cierre de este registro.

---

## 6. Declaración de integridad académica

Yo, **Steven Alexis Chango Vela**, declaro que:

1. **Supervisé el código.** Revisé el diseño y la implementación del banco de
   pruebas (`src/`), el protocolo de framing, la orquestación de procesos y el
   script de análisis antes de aceptar sus resultados.
2. **Verifiqué las fuentes.** Comprobé cada una de las ocho entradas de
   `references.bib` (autores, título, medio, año, volumen, páginas y DOI o URL).
   No incluí ninguna fuente que no pudiera verificar.
3. **Ejecuté los experimentos.** Las 1760 ejecuciones se realizaron en mi equipo
   bajo mi supervisión; no se sustituyeron datos ni se completaron celdas
   faltantes con valores simulados.
4. **Revisé las conclusiones.** Leí el manuscrito final y comprobé que las
   conclusiones se ajustaran a los resultados documentados en
   `analysis/REPORT.md`.

Asimismo, declaro que OpenCode se utilizó como herramienta de asistencia para
programar, analizar y redactar; que las decisiones metodológicas, la
interpretación de los resultados y la responsabilidad final son mías; y que no
se inventaron resultados, fuentes, experimentos ni explicaciones.

Firma: Steven Alexis Chango Vela

Fecha: 14 de noviembre de 2026

---

## 7. Limitaciones de este registro

- Los prompts 1–5 y 7 son síntesis; el 6 y el 8 se transcriben literalmente y
  el 9 como extracto. No se conserva una transcripción completa de la sesión.
- La cronología se apoya en dos commits y en marcas de tiempo de archivos; las
  horas son aproximadas y corresponden a la zona local −05:00.
- Varias correcciones se aplicaron en la misma sesión sin un prompt separado;
  se documentan por su efecto en los archivos, no por una instrucción textual.
- Este registro cubre el uso de la herramienta, no la declaración de autoría
  que exija la institución, que se presenta por separado.
