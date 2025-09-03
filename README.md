# TP1 – Conciencia en el código (Green Software)

![Foto Utn](./imgs/FRC.png)

## Portada
- **Autor:** Gino
- **Legajo:** 95345  
- **Asignatura:** Green Software 4k4 2025 — Trabajo Práctico Nº1 (segunda alternativa)
- **Profesor:** Ingeniero Franco Mana  
- **Fecha:** 2025-09-03

---

## Objetivo
Medir potencia, energía y emisiones de CO₂e asociadas a la ejecución de un algoritmo en Python utilizando la librería CodeCarbon en modo *offline*, y comparar el cálculo de emisiones con un factor de emisión (FE) fijo provisto por la consigna.

**Metodología.**
1. Se armó el script con `OfflineEmissionsTracker` de CodeCarbon (intervalo de muestreo: 1 s).  
2. Se ejecutó el algoritmo **Criba de Eratóstenes** para `N = 50,000,000`.  
3. Se tomaron del CSV de CodeCarbon las métricas clave: `cpu_power`, `gpu_power`, `ram_power`, `energy_consumed`, `duration`, `emissions`.  
4. Se calculó además:  
   - Potencia promedio derivada de energía: P = Energía (Wh)/ Duración (h).  
   - Emisiones con FE fijo: Emisiones [tCO₂e] = Energía [MWh] * FE [tCO₂e/MWh].

**Entorno de ejecución.**
- SO: Windows 11 (10.0.26100)  
- Python: 3.12.3  
- CodeCarbon: 3.0.4  
- CPU: AMD Ryzen 7 5700U with Radeon Graphics — *modo constante (fallback)*  
- RAM disponible: 23.326 GB  
- GPU: no  
- Archivo de salida: `cc_logs/emissions.csv`

**Dependencias.**
```bash
pip install "codecarbon>=3.0.4"
```

---

## Código fuente

El script principal es **`tp1_green_software.py`**. Contiene:

- Implementación de la *Criba de Eratóstenes* (O(n log log n) tiempo, O(n) memoria).
- Estructuras para leer el CSV de CodeCarbon y consolidar métricas.
- Un reporte formateado en consola con tiempos, potencias, energía y emisiones (CodeCarbon vs. FE fijo).

**Ejecución (ejemplos).**
```bash
# Valores por defecto equivalentes a la corrida reportada
python tp1_green_software.py --n 50000000 --fe 0.26 --country ARG --interval 1 --reps 1

# Variar parámetros
python tp1_green_software.py --n 10000000 --fe 0.26 --country ARG --interval 2 --reps 3
```

**Parámetros principales.**
- `--n`: cota superior para la criba (por defecto: 50,000,000).  
- `--fe`: factor de emisión en tCO₂e/MWh (por defecto: 0.26).  
- `--country`: ISO-3 del país para CodeCarbon offline (por defecto: ARG).  
- `--interval`: intervalo de muestreo de potencia en segundos (≥1).  
- `--reps`: repeticiones del algoritmo (para aumentar la carga).

**Salidas.**
- Consola: reporte con *duración, energía, potencias* y *emisiones* (CodeCarbon y FE fijo).  
- CSV: `cc_logs/emissions.csv` con columnas estándar de CodeCarbon.

---

## Resultados
**Imagenes de la consola cuando se corrio**
![Imagen1](./imgs/image.png)
![Imagen2](./imgs/image%20copy.png)
![Imagen3](./imgs/image%20copy%202.png)
![Imagen4](./imgs/image%20copy%203.png)

**Contexto de la corrida reportada.**
- Algoritmo: Criba de Eratóstenes  
- Parámetros: `N = 50,000,000`, `country = ARG`, `FE = 0.26 tCO₂e/MWh`, `interval = 1 s`, `reps = 1`  
- Primos encontrados: **3,001,134**

**Métricas principales (según tracker).**
- **Duración:** 7.616 s  
- **Energía total:** 0.000263 kWh (≈ **946.8 J**)  
- **Potencias (promedio CodeCarbon):** CPU **120.00 W**, GPU **0.00 W**, RAM **10.00 W**, **Total 130.00 W**  
- **Potencia promedio derivada de energía:** **124.37 W**

**Cálculo de emisiones.**
- Con **FE fijo Argentina** (0.26 tCO₂e/MWh): **0.000068 kgCO₂e** (**0.068 g**)  
- **Estimación CodeCarbon** (ARG offline): **0.000093 kgCO₂e** (**0.093 g**)

> Diferencia aproximada: 0.025 g CO₂e por corrida (CodeCarbon > FE fijo), esperable por los modelos y factores propios de la librería en modo offline.


---

## Conclusión

La medición muestra un **consumo energético muy pequeño** para una corrida aislada (≈0.000263 kWh), que se traduce en emisiones del orden de **centésimas de gramo de CO₂e** (0.068–0.093 g), convergentes entre el cálculo con **FE fijo** y la **estimación de CodeCarbon**. La ligera diferencia se explica por el **modelo de potencia de fallback** en CPU y por los **factores regionales internos** de la librería en modo offline.


## Licencias y referencias

- Criba de Eratóstenes (implementación base, MIT): <https://github.com/aditya5558/Sieve-of-Eratosthenes>  
- CodeCarbon — parámetros, salida y metodología:  
  - <https://mlco2.github.io/codecarbon/parameters.html>  
  - <https://mlco2.github.io/codecarbon/output.html>  
  - <https://mlco2.github.io/codecarbon/methodology.html>
