#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP1 - Conciencia en el código (Green Software)
Mide potencia y CO₂eq emitidos por la ejecución de un algoritmo en Python usando CodeCarbon.

Autor: Gino
Legajo: 95345
Asignatura: Green Software — Trabajo Práctico Nº1 Segunda alternativa
País: Argentina (factor de emisión por consigna FE = 0.26 tCO₂/MWh)

Metodología:
- Medimos energía, potencias y tiempo con CodeCarbon (OfflineEmissionsTracker).
- Ejecutamos un algoritmo, en este caso se eligio Criba de Eratóstenes (algoritmo inventado por Eratostenes para encontrar numeros primos)
 y reportamos resultados.
- Calculamos emisiones con: Emisiones [tCO₂e] = Energía [MWh] × FE [tCO₂e/MWh].
  Nota dimensional: FE dado en la consigna es por unidad de ENERGÍA
  Por claridad: 0.26 tCO₂/MWh = 0.26 kgCO₂/kWh.

Código base del algoritmo:
- Criba de Eratóstenes en Python, basada en una implementación pública bajo licencia MIT.
  Referencia: https://github.com/aditya5558/Sieve-of-Eratosthenes (MIT)

Documentación de CodeCarbon:
- Parámetros y modo offline (country_iso_code): https://mlco2.github.io/codecarbon/parameters.html
- Campos de salida (CSV: cpu_power, gpu_power, ram_power, energy_consumed, duration, emissions): https://mlco2.github.io/codecarbon/output.html
- Metodología y modelo/fallback de potencia: https://mlco2.github.io/codecarbon/methodology.html
"""
import argparse
import csv
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

# Intentamos importar CodeCarbon.
try:
    from codecarbon import OfflineEmissionsTracker  # type: ignore
except Exception as e:
    sys.stderr.write(
        "⚠️  No se pudo importar 'codecarbon'.\n"
        "Instala la dependencia con:\n"
        "    pip install 'codecarbon>=3.0.4'\n"
        f"Detalle del error: {e}\n"
    )
    sys.exit(1)


# ----------------------------
# Algoritmo: Criba de Eratóstenes
# ----------------------------
def criba_de_eratostenes(n: int) -> List[int]:
    """
    Devuelve todos los primos ≤ n usando la criba de Eratóstenes.
    Implementación propia (basada en el enfoque clásico, ver referencia MIT mas arriba).
    Complejidad: O(n log log n) tiempo, O(n) memoria.

    :param n: cota superior
    :return: lista de números primos ≤ n
    """
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)  # bytearray para menor overhead que list[bool]
    sieve[0:2] = b"\x00\x00"
    limit = int(math.isqrt(n))
    for p in range(2, limit + 1):
        if sieve[p]:
            start = p * p
            sieve[start:n + 1:p] = b"\x00" * (((n - start) // p) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]


# ----------------------------
# Métricas / estructura
# ----------------------------
@dataclass
class RunMetrics:
    duracion_s: float
    poder_CPU_W: float
    poder_GPU_W: float
    poder_RAM_W: float
    energia_kWh: float
    emisiones_kg_codecarbon: float

    @property
    def poder_total_W(self) -> float:
        return self.poder_CPU_W + self.poder_GPU_W + self.poder_RAM_W

    @property
    def poder_promedio_desde_energia_W(self) -> float:
        # P_prom = Energía / Tiempo
        # energia_kWh * 1000 => Wh ; duracion_s/3600 => h ; => W
        if self.duracion_s <= 0:
            return float("nan")
        return (self.energia_kWh * 1000.0) / (self.duracion_s / 3600.0)


def leer_ultima_fila_de_emision(csv_path: Path) -> Dict[str, Any]:
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe el CSV de CodeCarbon en: {csv_path}")
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise RuntimeError("El CSV de CodeCarbon está vacío.")
    return rows[-1]


# ----------------------------
# Reporte
# ----------------------------
def mostrar_reporte(n: int, contador_primos: int, fe_t_por_MWh: float, country_iso: str, m: RunMetrics) -> None:
    # FE 0.26 tCO2/MWh == 0.26 kgCO2/kWh
    fe_kg_por_kWh = fe_t_por_MWh  # ya que 1 t/MWh == 1 kg/kWh
    energia_MWh = m.energia_kWh / 1000.0
    emisiones_t = energia_MWh * fe_t_por_MWh
    emisiones_kg = emisiones_t * 1000.0

    # Texto con fórmula (para el docente)
    formula = "Emisiones [tCO₂e] = Energía [MWh] × FE [tCO₂e/MWh]"

    print("\n" + "=" * 78)
    print("TP1 - CONCIENCIA EN EL CÓDIGO  |  Medición con CodeCarbon".center(78))
    print("=" * 78)
    print(f"Algoritmo: Criba de Eratóstenes  |  N = {n:,}  |  Primos encontrados: {contador_primos:,}")
    print(f"País (ISO-3): {country_iso}  |  FE usado: {fe_t_por_MWh:.3f} tCO₂e/MWh  (= {fe_kg_por_kWh:.3f} kgCO₂e/kWh)")
    print("-" * 78)
    print(f"Duración medida por tracker: {m.duracion_s:.3f} s")
    print(f"Energía total: {m.energia_kWh:.6f} kWh  ({energia_MWh:.9f} MWh)")
    print(f"Potencia promedio (CodeCarbon): CPU {m.poder_CPU_W:.2f} W | GPU {m.poder_GPU_W:.2f} W | RAM {m.poder_RAM_W:.2f} W | Total {m.poder_total_W:.2f} W")
    print(f"Potencia promedio derivada de energía: {m.poder_promedio_desde_energia_W:.2f} W")
    print("-" * 78)
    print(f"FÓRMULA: {formula}")
    print(f"Emisiones con FE fijo Argentina: {emisiones_kg:.6f} kgCO₂e")
    print(f"Emisiones estimadas por CodeCarbon (para {country_iso}): {m.emisiones_kg_codecarbon:.6f} kgCO₂e")
    print("-" * 78)
    print("Notas:")
    print("• FE de la consigna (0.26 tCO₂/MWh) equivale a 0.26 kgCO₂/kWh; se aplica a la ENERGÍA.")
    print("• CodeCarbon estima potencias (CPU/GPU/RAM) y energía; si no hay sensores, usa modelos de fallback.")
    print("• Diferencias entre 'CodeCarbon' y 'FE fijo' se deben a factores/regiones que usa la librería.")
    print("=" * 78 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="TP1 - Medición de potencia y CO₂eq con CodeCarbon sobre la Criba de Eratóstenes."
    )
    parser.add_argument("--n", type=int, default=50000000, help="Cota superior para la criba (por defecto: 50000000).")
    parser.add_argument("--fe", type=float, default=0.26, help="Factor de emisión en tCO₂/MWh (por defecto: 0.26).")
    parser.add_argument("--country", type=str, default="ARG", help="Código ISO-3 del país para CodeCarbon Offline.")
    parser.add_argument("--outdir", type=Path, default=Path("cc_logs"), help="Directorio de salida (CSV de CodeCarbon).")
    parser.add_argument("--interval", type=int, default=1, help="Intervalo de muestreo de potencia en segundos (>=1).")
    parser.add_argument("--reps", type=int, default=1, help="Repeticiones del algoritmo para cargarlo un poco más.")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)

    tracker = OfflineEmissionsTracker(
        project_name="TP1-GreenSoftware",
        measure_power_secs=max(1, int(args.interval)),
        tracking_mode="process",       # aísla el/los procesos medidos
        country_iso_code=args.country, # obligatorio en offline
        output_dir=str(args.outdir),
        save_to_file=True,
        log_level="info",
    )

    tracker.start()
    # Ejecutamos el algoritmo las veces que se pidió
    primos_totales = 0
    for _ in range(max(1, args.reps)):
        primes = criba_de_eratostenes(args.n)
        primos_totales = len(primes)
    emissions_kg = tracker.stop()

    # Leemos el CSV para obtener todos los campos requeridos por la consigna
    csv_path = args.outdir / "emissions.csv"
    row = leer_ultima_fila_de_emision(csv_path)

    # Campos que vamos a reportar (ver docs de CodeCarbon)
    duration_s = float(row["duration"])
    cpu_power_W = float(row.get("cpu_power") or 0.0)
    gpu_power_W = float(row.get("gpu_power") or 0.0)
    ram_power_W = float(row.get("ram_power") or 0.0)
    energy_kWh = float(row["energy_consumed"])

    metrics = RunMetrics(
        duracion_s=duration_s,
        poder_CPU_W=cpu_power_W,
        poder_GPU_W=gpu_power_W,
        poder_RAM_W=ram_power_W,
        energia_kWh=energy_kWh,
        emisiones_kg_codecarbon=float(emissions_kg),
    )

    mostrar_reporte(
        n=args.n,
        contador_primos=primos_totales,
        fe_t_por_MWh=float(args.fe),
        country_iso=str(args.country),
        m=metrics,
    )


if __name__ == "__main__":
    main()
