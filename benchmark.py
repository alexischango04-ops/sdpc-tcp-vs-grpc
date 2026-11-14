"""Punto de entrada del benchmark TCP vs gRPC.

Este modulo es un envoltorio delgado alrededor de ``src.run_benchmark`` para
que el repositorio exponga ``benchmark.py`` en la raiz, como pide la rúbrica.
La implementacion real (matriz experimental, procesos, cruce de datos y
generacion de ``results.csv``) esta en ``src/run_benchmark.py``.

Uso::

    python benchmark.py --profile design --dry-run
    python benchmark.py --config configs/design.yaml --profile design --out results.csv
"""

from src.run_benchmark import main

if __name__ == "__main__":
    raise SystemExit(main())
