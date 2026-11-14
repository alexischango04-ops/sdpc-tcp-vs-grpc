# Informe de análisis

## Integridad de los datos

- Fichero analizado: `C:\Users\Steve\Documents\sdpc-tcp-vs-grpc\results.csv`
- SHA-256: `138b6d3407eafcd8dcbd503aa5a8262d0edc931727139a3be67ba7aaf4615e4d`
- Ejecuciones analizadas: **1760**
- Celdas con datos: **72**
- Estados: `{'ok': 1760}`
- Filas con `loss_pct > 0`: **0**
- Filas con `join_missing > 0`: **0**
- Filas con latencia p50 ausente: **0**
- Ejecuciones con déficit de ritmo > 1 %: **1**
- Ejecuciones con lateness p99 > periodo (diagnóstico de ráfagas): **1013**
- Atípicos robustos (|x − mediana| > 6·MAD por celda): **362**

## Hipótesis y procedimiento

La unidad de análisis es la **ejecución** (n = 30 réplicas independientes por celda). Para cada celda (modalidad × payload × ritmo × concurrencia) se contrasta:

- **H0**: la distribución de la métrica por ejecución es idéntica en TCP y en gRPC.
- **H1**: las distribuciones difieren (bilateral).

Se usa **Mann–Whitney U** bilateral porque las métricas son acotadas, asimétricas y no se puede suponer normalidad ni homocedasticidad; con n = 30 por grupo la aproximación normal es adecuada. El error de tipo I se controla por familia de métricas con **Holm–Bonferroni**. El tamaño del efecto se cuantifica con **δ de Cliff** y la relevancia práctica se declara a priori como |Δ| ≥ 10 % en la mediana.

## Resumen por escenario (mediana de celdas)

|    | scenario   |   lat_p50_us |   lat_p99_us |   cpu_client_us_msg |   cpu_server_us_msg |   rss_client_med_mb |   rss_server_med_mb |
|---:|:-----------|-------------:|-------------:|--------------------:|--------------------:|--------------------:|--------------------:|
|  0 | G-B        |       524.72 |       821.72 |              951.17 |              464.84 |               37.32 |               36.75 |
|  1 | G-U        |       527.51 |       855.85 |              656.25 |              312.5  |               37.01 |               36.62 |
|  2 | T-B        |       330.98 |       422.19 |              513.67 |              228.52 |               28.64 |               28.36 |
|  3 | T-U        |       383.24 |       472.96 |              455.08 |              183.59 |               28.14 |               28.29 |

## Potencia y resolución de los contrastes

Con Mann–Whitney exacto, el p bilateral mínimo alcanzable depende del tamaño de grupo. La última columna aplica la corrección de Holm de la familia: si supera 0,05, esa familia **no puede declarar significancia** aunque el efecto sea máximo.

| Familia | Contrastes | n TCP/gRPC | p mínimo | p mínimo tras Holm |
|---|---:|---|---:|---:|
| principal (C = 1) | 24 | 30/30 | 1.69e-17 | 4.06e-16 |
| escalado por concurrencia | 4 | 30/30 | 1.69e-17 | 6.76e-17 |
| throughput | 8 | 5/5 | 0.00794 | 0.0635 |

## Latencia p50 (mediana entre réplicas, C=1)

| scenario   |   100.0 |   500.0 |   1000.0 |
|:-----------|--------:|--------:|---------:|
| G-B        |   762.2 |   527.0 |    187.1 |
| G-U        |   749.4 |   528.6 |    435.7 |
| T-B        |   431.2 |   331.6 |    268.1 |
| T-U        |   470.6 |   383.3 |    274.9 |

## Contraste lat_p50_us (principal, C = 1)

- Comparaciones: **24**; significativas tras Holm: **24**
- Δ% mediano en las significativas: **57.9 %**
- Efectos: {'grande': 24}
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **24**

## Contraste lat_p99_us (principal, C = 1)

- Comparaciones: **24**; significativas tras Holm: **24**
- Δ% mediano en las significativas: **87.1 %**
- Efectos: {'grande': 24}
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **24**

## Contraste cpu_client_us_msg (principal, C = 1)

- Comparaciones: **24**; significativas tras Holm: **24**
- Δ% mediano en las significativas: **71.5 %**
- Efectos: {'grande': 24}
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **24**

## Contraste cpu_server_us_msg (principal, C = 1)

- Comparaciones: **24**; significativas tras Holm: **24**
- Δ% mediano en las significativas: **93.9 %**
- Efectos: {'grande': 24}
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **24**

## Contraste rss_client_med_mb (principal, C = 1)

- Comparaciones: **24**; significativas tras Holm: **24**
- Δ% mediano en las significativas: **30.4 %**
- Efectos: {'grande': 24}
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **24**

## Contraste rss_server_med_mb (principal, C = 1)

- Comparaciones: **24**; significativas tras Holm: **24**
- Δ% mediano en las significativas: **29.5 %**
- Efectos: {'grande': 24}
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **24**

## Contraste lat_p50_us (escalado por concurrencia, 1024 B y 500 Hz)

- Comparaciones: **4**; significativas tras Holm: **4**
- Δ% mediano en las significativas: **158.2 %**
- Efectos: {'grande': 4}
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **4**

## Contraste lat_p99_us (escalado por concurrencia, 1024 B y 500 Hz)

- Comparaciones: **4**; significativas tras Holm: **4**
- Δ% mediano en las significativas: **180.8 %**
- Efectos: {'grande': 4}
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **4**

## Contraste cpu_client_us_msg (escalado por concurrencia, 1024 B y 500 Hz)

- Comparaciones: **4**; significativas tras Holm: **4**
- Δ% mediano en las significativas: **250.1 %**
- Efectos: {'grande': 4}
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **4**

## Contraste cpu_server_us_msg (escalado por concurrencia, 1024 B y 500 Hz)

- Comparaciones: **4**; significativas tras Holm: **4**
- Δ% mediano en las significativas: **253.1 %**
- Efectos: {'grande': 4}
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **4**

## Contraste thr_msg_s (throughput sin limitación de ritmo)

- Comparaciones: **8**; significativas tras Holm: **0**
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **0**

## Contraste thr_payload_mbps (throughput sin limitación de ritmo)

- Comparaciones: **8**; significativas tras Holm: **0**
- Significativas y prácticamente relevantes (|Δ| ≥ 10 %): **0**

## Anomalías observadas

- En **4 de 24** celdas principales la OWD p50 es **menor en gRPC** (B/64 B/1000 Hz, B/256 B/1000 Hz, B/1024 B/1000 Hz, B/4096 B/1000 Hz); Δ% entre -32.9 % y -27.9 %. En esas mismas celdas el p99 de gRPC es mayor (Δ% entre +38.6 % y +60.2 %): la ventaja afecta a la mediana, no a la cola.
- La mediana agregada por escenario oculta esa inversión; por eso el artículo debe reportar celda por celda y no solo el promedio de escenario.
- Déficit de ritmo > 1 % en `01165-G-U-p256-r500-c1-n07` (1.65 %).
- Atípicos robustos por métrica: lat_p50_us 197, lat_p99_us 115, lateness_p99_us 50 (sobre 1760 ejecuciones evaluadas por métrica).

## Limitaciones metodológicas

- Cliente y servidor comparten host; el OWD se mide con el mismo reloj (`perf_counter_ns()`), de modo que no incluye el tránsito por una red real.
- Windows no ofrece temporizadores de alta resolución sin espera activa; con `spin_us = 0` el emisor puede agrupar envíos (lateness > periodo) sin perder mensajes, lo que añade ráfagas al patrón de llegada.
- La contabilidad de CPU de Windows tiene granularidad de 15,625 ms; con 2000 mensajes por ejecución la resolución es de ~7,8 µs por mensaje.
- La familia de throughput usa 5 réplicas por celda y 8 contrastes: con Mann–Whitney exacto el p bilateral mínimo es 0,0079 y, ajustado por Holm, 0,063. Esa familia no puede rechazar H0 al 5 % con el diseño actual aunque las diferencias observadas ronden el 90 %; se reporta el tamaño del efecto y se trata como evidencia descriptiva, no confirmatoria.
- El sobre de bytes compara cabeceras de aplicación (TCP: 4 B de longitud + 16 B de seq/t_send; gRPC: prefijo de 5 B + codificación protobuf); no incluye cabeceras HTTP/2 ni TCP/IP.
- Los percentiles P95/P99 entre réplicas requieren al menos 2 ejecuciones por celda; las celdas con menos réplicas se reportan con su n real.

## Figuras generadas

- `figures/fig01_latency_p50.pdf` / `figures/fig01_latency_p50.png`
- `figures/fig02_latency_p99.pdf` / `figures/fig02_latency_p99.png`
- `figures/fig03_throughput.pdf` / `figures/fig03_throughput.png`
- `figures/fig04_resources.pdf` / `figures/fig04_resources.png`
- `figures/fig05_rtt.pdf` / `figures/fig05_rtt.png`
- `figures/fig06_lateness.pdf` / `figures/fig06_lateness.png`
- `figures/fig07_overhead.pdf` / `figures/fig07_overhead.png`
- `figures/fig08_rate.pdf` / `figures/fig08_rate.png`
- `figures/fig09_scaling.pdf` / `figures/fig09_scaling.png`
