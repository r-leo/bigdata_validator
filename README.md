# Validador de tablas finales


## 1. Objetivo y alcance

**`bigdata_validator`** es un módulo de Python diseñado con el propósito de evitar que se envíen a la nueva web de Big Data tablas finales que no se ajusten a las políticas explícitas establecidas. El módulo automatiza el proceso de validación final implementando un objeto `Validator` que lleva a cabo el proceso de verificación que de otra forma tendría que hacerse manualmente. Tiene la flexibilidad necesaria para integrarse dentro de un script de Python, o bien ejecutarse de forma interactiva en el intérprete o la celda de un notebook (de Jupyter por ejemplo).


## 2. Instalación / descarga

### 2.1. Opción A: instalación local con pip

Para instalar usando pip, ejecutar la siguiente línea en la terminal:

```bash
pip install git+https://github.com/r-leo/bigdata_validator.git
```

### 2.2. Opción B: descarga directa (sin instalación)

Para usar el módulo sin instalarlo, descargar el archivo [bigdata_validator.py](./bigdata_validator.py) y guardarlo en el mismo directorio donde se encuentre el script de Python o el notebook donde se desee utilizar.


## 3. Uso

### 3.1. Importar el módulo

Para importar el módulo:

```python
import bigdata_validator
from bigdata_validator import Validator
```

Para verificar que esté instalada la versión más reciente (`2.1.0`):

```python
print(bigdata_validator.__version__)
```

> [!NOTE]
> Si la versión instalada no es la más reciente, actualizar usando pip en la terminal:
> ```bash
> pip install --upgrade git+https://github.com/r-leo/bigdata_validator.git
> ```

### 3.2. Crear un objeto `Validator` para cada tabla final

La clase `Validator` se crea pasando los siguientes parámetros:

* **`data`**: `str` o `pandas.DataFrame` (requerido). La tabla final que se va a validar. Puede ser un objeto `pandas.DataFrame` o un string que contenga la ruta al archivo CSV que contiene los datos.
* **`indicator`**: `str` (requerido). El nombre del indicador. Debe tomar uno de los siguientes posibles valores:
   * Indicadores de *alta frecuencia*:
     * `"hf_consumption"` = consumo.
     * `"hf_investment"` = inversión.
     * `"hf_external"` = sector exterior.
     * `"hf_sectoral"` = actividad sectorial.
   * Indicadores de *alta granularidad*:
     * `"hg_national"` =  consumo agregado (nacional).
     * `"hg_regions"` = consumo por regiones.
     * `"hg_states"` = consumo por estados.
     * `"hg_cities"` = consumo por ciudades.
* **`file_separator`**: `str` (opcional, por defecto: `","`). El separador de campos en caso de que los datos provengan de un archivo CSV.
* **`decimal_separator`**: `str` (opcional, por defecto: `"."`). El separador decimal de la variable `INTERANUAL_VARIATION_DATE`. Este separador se emplea independientemente de si los datos proporcionados son un archivo CSV o un DataFrame de pandas. Sólo se admiten como valores el punto (`"."`) y la coma (`","`).

Ejemplo:

```python
# Si los datos están contenidos en un CSV:
val_investment = Validator('final_table_investment.csv', 'hf_investment')

# Si los datos están ya en un dataframe de pandas:
val_investment = Validator(df_investment, 'hf_investment')
```


### 3.3. Ejecutar el proceso de validación

Hay ds formas de ejecutar el proceso de validación:

#### Opción A: usando `is_valid()`

El método `is_valid()` simplemente devuelve `True` si la tabla pasa la prueba de validación, y `False` en caso contrario. No proporciona ningún detalle adicional en caso de que la tabla no pase la prueba. Ejemplo:

```python
val_investment.is_valid()
# -> devuelve True (pasó la prueba) o False (no pasó la prueba)
```

#### Opción B: usando `validate()`

El método `.validate()` lleva a cabo el proceso de validación de la tabla, y en caso de que no lo pase satisfactoriamente, imprime en pantalla los criterios donde falló. Ejemplo:

```python
val_investment.validate()
```

El código anterior imprime en la pantalla un mensaje indicando si la tabla pasó o no la prueba. En caso de que no la pase, muestra un reporte de los errores encontrados. Un ejemplo de reporte de errores es:

```
Errores encontrados (26):

1	El registro ['N' 'MX-CAM' 'Aerolíneas'] no tiene datos para la última fecha.
2	El registro ['N' 'MX-COL' 'Aerolíneas'] no tiene datos para la última fecha.
3	El registro ['N' 'MX-GUA' 'Aerolíneas'] no tiene datos para la última fecha.
4	El registro ['N' 'MX-HID' 'Aerolíneas'] no tiene datos para la última fecha.
5	El registro ['N' 'MX-MOR' 'Aerolíneas'] no tiene datos para la última fecha.
6	El registro ['N' 'MX-NAY' 'Aerolíneas'] no tiene datos para la última fecha.
...
```


## 4. Notas importantes

1. En caso de leer archivos CSV, es obligatorio que estén codificados con UTF-8.
1. **Importante**: por el momento, el módulo sólo acepta como separador decimal el punto.


## 5. Anexo: estructura del proceso de validación

> **Nota**. No es necesario leer esta sección para usar el módulo. Únicamente describe las pruebas que se llevan a cabo sobre los datos para determinar si son válidos o no.

El método `validate()` siempre ejecuta internamente `is_valid()`. Si el resultado es `False`, recopila los errores encontrados junto con su descripción y los imprime línea por línea en la pantalla. En caso contrario indica al usuario que no se encontró ningún error.

Por otra parte, `is_valid()` devuelve `True` únicamente cuando se satisfacen todas las siguientes condiciones:

### Condiciones generales (aplican a todos los indicadores)
1. El número de valores únicos del campo de fecha debe ser menor o igual a 400.
1. Ninguna combinación de nominal/real, región geográfica y categoría debe tener fechas faltantes.
1. Para cada registro real debe existir el correspondiente registro nominal.
1. Todas las combinaciones de nominal/real, región geográfica y categoría debe tener datos no nulos en el registro correspondiente a la fecha más reciente de la tabla.
1. La variable de fecha debe estar expresada como AAAA-MM-DD, lo que equivale a la siguiente [expresión regular](https://regex101.com/r/0jtIVD/1): `\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])`. No se admiten fechas vacías.
1. La variable de variación interanual debe tener el formato definido por la [expresión regular](https://regex101.com/r/U4L5uF/1) `.{0}|(-?\d+\.\d{4})`. Sí se admiten valores vacíos. El formato consta de la concatenación de: **signo**, ya sea negativo (`-`) o sin signo; **parte entera**, consistente en uno o más dígitos; **separador decimal**, que es obligatorio y debe ser un punto (`.`); y **parte decimal**, compuesta por exactamente 4 dígitos (de acuerdo con las políticas, si es necesario deben agregarse ceros a la derecha hasta completar cuatro dígitos en la parte decimal).

### Condiciones específicas (sólo aplican a algunos indicadores)
1. Deben existir datos agregados (es decir, la categoría `Total`) para los indicadores de consumo (`hf_consumption`), inversión (`hf_investment`) y todos los de alta granularidad (`hg_*`).
1. El orden de las categorías del  indicador de sector exterior debe ser (exportaciones, importaciones).
