# Evaluación Empírica de Sockets TCP de Bajo Nivel vs. gRPC en Streaming Unidireccional y Bidireccional para Telemetría de Alta Frecuencia

**Autor:** Steven Alexis Chango Vela
**Asignatura:** Sistemas Distribuidos y Paradigmas de la Computación
**Fecha:** noviembre de 2026
**Estado:** completo — experimento ejecutado, análisis realizado y artículo compilado
**Licencia:** MIT (ver `LICENSE`)

---

## Resumen

La telemetría de alta frecuencia exige transportar mensajes pequeños con latencia
acotada y bajo coste por mensaje. gRPC aporta contrato tipado y streaming sobre
HTTP/2, pero interpone serialización, *framing* y *runtime* entre la aplicación
y el socket. Este trabajo cuantifica ese coste frente a un socket TCP con
*framing* binario mínimo en cuatro escenarios (TCP y gRPC, streaming
unidireccional y bidireccional), con 1760 ejecuciones, 30 réplicas por celda,
*cargas útiles* de 64 a 4096 B y ritmos de 100 a 1000 Hz. La latencia de un solo
sentido (OWD) se mide con un reloj monotónico compartido entre cliente y
servidor; el RTT se reporta solo como RTT, nunca como OWD. Las 144 comparaciones
principales fueron significativas tras la corrección de Holm. En unidireccional,
gRPC incrementó la OWD p50 un 64.1 % a 1024 B y 1000 Hz; en bidireccional el
cambio de mediana fue −29.4 % y la cola p99 un 60.2 % mayor. gRPC consumió más
CPU y memoria por mensaje y su *throughput* fue un orden de magnitud menor,
aunque esa familia no alcanzó significancia tras Holm. El coste reside en la pila
de abstracción, no en los bytes de cabecera.

---

## Objetivos

**General.** Cuantificar el coste de la pila de abstracción de gRPC frente a
sockets TCP de bajo nivel en streaming unidireccional y bidireccional, en un
entorno controlado de un solo host, para telemetría de alta frecuencia.

**Específicos.**

1. Medir OWD real (no RTT/2), RTT, tiempo de procesamiento, *lateness*,
   *throughput*, CPU y memoria en los cuatro escenarios.
2. Separar la significancia estadística de la relevancia práctica.
3. Descomponer el coste en serialización, comunicación (*framing*) y abstracción.
4. Dejar el experimento y el análisis reproducibles desde un entorno limpio.
5. Documentar las amenazas a la validez y las limitaciones del diseño.

---

## Metodología

### Escenarios

| ID | Escenario | Transporte | Semántica |
|---|---|---|---|
| `T-U` | TCP unidireccional | socket TCP, *framing* propio | cliente → servidor, sin respuesta |
| `T-B` | TCP bidireccional | socket TCP *full-duplex* | mensaje → `ACK` por mensaje |
| `G-U` | gRPC unidireccional | HTTP/2 | `Upload` (*client streaming*) |
| `G-B` | gRPC bidireccional | HTTP/2 | `Exchange` (*bidirectional streaming*) |

Los cuatro escenarios transportan la misma carga lógica (`seq`, `t_send_ns`,
`payload`), con el mismo tamaño, número de mensajes, ritmo, calentamiento y
planificador. La carga útil se genera con semilla fija: los bytes son idénticos
en todas las pilas. En `T-B`/`G-B` el lector de ACK corre en una tarea
independiente del escritor, para no convertir el escenario en
petición-respuesta.

### Diseño experimental

- *Payloads*: 64, 256, 1024 y 4096 B.
- Ritmos agregados: 100, 500 y 1000 Hz.
- Concurrencia: `C = 1` en el bloque principal; `C ∈ {4, 16}` a 1024 B y 500 Hz.
- *Throughput*: régimen no limitado (`unpaced`), 5 s por ejecución.
- 2000 mensajes medidos por ejecución; calentamiento `max(500 mensajes, 2 s)`.
- 30 réplicas por celda (5 en *throughput*); una celda = procesos nuevos, sin
  reutilizar conexiones ni intérpretes.
- Afinidad: servidor en CPU 0–1, cliente en CPU 2–3. Orden de ejecución
  barajado (`shuffled`), registrado en `order_index`.
- Matriz congelada en `configs/design.yaml`; el *hash* de la configuración y el
  *commit* de Git quedan en cada fila de `results.csv`.

### Métricas

| Magnitud | Definición | Dónde se mide |
|---|---|---|
| OWD (c→s) | `t_recv − t_send` | servidor |
| OWD (s→c) | `t_ack_recv − t_srv_send` | cliente |
| RTT | `t_ack_recv − t_send` | cliente |
| T_proc | `t_handler_end − t_recv` | servidor |
| *lateness* | `t_send − deadline` | cliente |
| CPU | `cpu_*_us_msg` (normalizada por mensaje) | por proceso |
| Memoria | RSS mediana y pico por proceso | por proceso |

Cliente y servidor son procesos separados en el **mismo host**, por lo que
comparten el dominio de `time.perf_counter_ns()`: eso permite medir OWD real,
pero no se extrapola a una red física. El *throughput* en las celdas con ritmo
es, por construcción, igual a la tasa ofrecida y no se interpreta como
hallazgo. La CPU se normaliza por mensaje porque es la métrica comparable
entre protocolos.

### Análisis estadístico

Unidad de análisis = **ejecución** (cada fila de `results.csv` ya contiene los
percentiles de 2000 mensajes; agregar por ejecución evita tratar 60 000
mensajes como independientes). Se usa Mann–Whitney U bilateral por celda,
corrección de Holm–Bonferroni por familia de métricas, δ de Cliff e intervalos
bootstrap. Se distingue significancia estadística (Holm) de relevancia práctica
(cambio relativo de medianas ≥ 10 %). El script `src/analysis.py` es de solo
lectura y registra el SHA-256 de la entrada.

### Limitaciones declaradas

- Un solo host (loopback): la OWD no incluye propagación, pérdida ni congestión.
- Una implementación en Python y cuatro *payloads*; no se extrapola a otros
  lenguajes ni a redes de área amplia.
- La granularidad del temporizador de Windows y la ausencia de espera activa
  agrupan envíos; la *lateness* p99 supera un periodo en 1013 ejecuciones.
- No se controló la frecuencia ni la energía de la CPU.
- La familia de *throughput* tiene 5 réplicas por celda y 8 contrastes: con
  Holm, el p mínimo ajustado es 0.063, de modo que no puede rechazar H0 con este
  diseño. Se reporta como evidencia descriptiva, no confirmatoria.

---

## Tecnologías utilizadas

| Componente | Versión |
|---|---|
| Windows 11 | build 26300 |
| Python | 3.13.14 (64 bits) |
| gRPC / grpcio-tools | 1.85.1 |
| protobuf | 7.36.2 |
| pandas / numpy / scipy | 3.1.1 / 2.5.4 / 1.18.1 |
| matplotlib / psutil / PyYAML | 3.11.2 / 7.2.2 / 6.0.3 |
| Quarto | 1.11.9 |
| Extensión IEEE | `dfolio/quarto-ieee` v1.1.0 (`ieee-pdf`, `IEEEtran.cls` V1.8b) |
| Motor LaTeX | pdfTeX, TeX Live 2026 |
| Git | 2.56.1 |

Las dependencias Python están fijadas en `requirements.txt`.

---

## Estructura del repositorio

```
.
├── articulo.qmd                 # artículo (fuente Quarto)
├── articulo.pdf                 # artículo compilado (4 páginas, IEEE Conference)
├── references.bib               # 8 referencias verificables
├── _quarto.yml                  # configuración del proyecto (IEEE, español)
├── benchmark.py                 # punto de entrada del benchmark (envoltorio)
├── results.csv                  # 1760 ejecuciones (una fila por ejecución)
├── README.md                    # este archivo
├── PROMPTS_OPENCODE.md          # trazabilidad del uso de OpenCode
├── requirements.txt             # dependencias Python fijadas
├── LICENSE                      # MIT
├── configs/
│   └── design.yaml              # matriz experimental congelada (smoke y design)
├── src/
│   ├── run_benchmark.py         # orquestador: matriz, procesos, cruce, results.csv
│   ├── analysis.py              # análisis estadístico, tablas, figuras y macros
│   ├── protocol.py              # tramado TCP y ACK
│   ├── common.py                # eventos, planificador, carga, afinidad
│   ├── metrics.py               # percentiles, jitter, CPU/RSS
│   ├── bootstrap.py             # generación de los stubs de gRPC
│   ├── client_tcp.py / server_tcp.py
│   └── client_grpc.py / server_grpc.py
├── proto/telemetry.proto        # contrato gRPC
├── analysis/
│   ├── REPORT.md                # informe del análisis
│   ├── validation.json          # comprobaciones de integridad y SHA-256
│   └── key_numbers.tex          # macros usadas por el artículo
├── tables/                      # 24 tablas (.tex y .csv) generadas
├── figures/                     # 18 figuras (PDF y PNG) generadas
├── _extensions/dfolio/ieee/     # plantilla IEEE incluida (reproducibilidad offline)
├── verificacion-plantilla-ieee.qmd / .pdf   # comprobación de la plantilla
└── data/                        # raw y smoke NO se versionan (.gitignore)
```

`data/raw/` y `data/smoke/` contienen los CSV por mensaje y los registros de las
ejecuciones; están excluidos del repositorio por su volumen (≈118 MB). Se
regeneran al ejecutar el benchmark.

---

## Reproducción desde un entorno limpio

### 1. Prerrequisitos

- Git y Python 3.13 (64 bits).
- 4 núcleos disponibles (la afinidad del experimento usa CPU 0–3).
- pdfTeX para compilar el artículo. Si no está instalado:
  `quarto install tinytex`. La clase `IEEEtran` está incluida en
  `_extensions/dfolio/ieee/`, por lo que no hace falta instalarla aparte.

### 2. Clonar y preparar el entorno

```powershell
git clone https://github.com/chstevensiu7/sdpc-tcp-vs-grpc.git
cd sdpc-tcp-vs-grpc
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Los *stubs* de gRPC (`proto/*_pb2*.py`) se generan automáticamente al importar
los módulos; no hay que ejecutar `protoc` a mano.

### 3. Inspeccionar la matriz sin ejecutar

```powershell
python benchmark.py --profile design --dry-run
# o equivalente: python -m src.run_benchmark --profile design --dry-run
# salida esperada: perfil=design celdas=1760 ...
```

### 4. Validación del arnés (humo)

```powershell
python benchmark.py --config configs/design.yaml --profile smoke --out data/smoke/results.csv
```

32 ejecuciones cortas (24 de ritmo + 4 concurrentes + 4 de *throughput*), sin
valor estadístico. Debe terminar con 32/32 celdas en estado `ok` y sin pérdidas.

### 5. Batería completa del artículo

```powershell
python benchmark.py --config configs/design.yaml --profile design --out results.csv
```

**1760 ejecuciones** (1440 principales, 240 de escalado y 80 de *throughput*),
con procesos nuevos en cada una. Requiere **varias horas** y una máquina
dedicada; no se recomienda ejecutarla en un equipo compartido. El progreso queda
en `data/run_design.log` y los CSV por mensaje en `data/raw/`.

Opciones útiles: `--only T-U,G-B` (filtra escenarios), `--limit N` (primeras N
celdas), `--order sequential|shuffled` (cambia el orden; el efectivo queda en
`order_index`).

### 6. Análisis estadístico

```powershell
python -m src.analysis --results results.csv --out-dir .
```

Regenera `analysis/`, `tables/` y `figures/` sin modificar `results.csv`, y
escribe el SHA-256 de la entrada en `analysis/validation.json`.

### 7. Compilar el artículo

```powershell
quarto render articulo.qmd --to ieee-pdf
```

Genera `articulo.pdf`. Si se ejecuta `quarto render` sin argumento, el proyecto
compila también `verificacion-plantilla-ieee.qmd`.

### 8. Verificación rápida

- `articulo.pdf`: 4 páginas, con Fig. 1 y Tablas I–III, sin referencias
  colgantes (`??`).
- `results.csv`: 1760 filas, 72 celdas, 1760 ejeciones con estado `ok`.
- SHA-256 de `results.csv` (medido en este equipo):
  `138b6d3407eafcd8dcbd503aa5a8262d0edc931727139a3be67ba7aaf4615e4d`.
- `python -m src.run_benchmark --profile design --dry-run` → 1760 celdas.

---

## Datos y reproducibilidad

- `results.csv`: 1760 filas × 69 columnas; una fila por ejecución. Incluye
  identificación, entorno, configuración, conteos, latencia, RTT, *throughput*,
  CPU y memoria.
- `analysis/validation.json`: 0 pérdidas, 0 mensajes sin emparejar, 1 ejecución
  con déficit de ritmo del 1.65 % y 362 valores atípicos conservados (el análisis
  usa medianas y rangos).
- Los percentiles de `results.csv` se calcularon en el orquestador a partir de
  los CSV por mensaje; por eso `data/raw/` no se versiona, pero puede
  regenerarse.

---

## Uso de OpenCode

`PROMPTS_OPENCODE.md` documenta, de forma cronológica, los prompts utilizados,
las tareas asistidas por IA, las verificaciones humanas, los 13 errores
detectados y la declaración de integridad académica.

---

## Licencia

MIT — ver `LICENSE`.
