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
from bigdata_validator import Validator
```

### 3.2. Crear un objeto `Validator` para cada tabla final

La clase `Validator` se crea pasando los siguientes parámetros:

* **`data`**: `str` o `pandas.DataFrame`</br>
La tabla final que se va a validar. Puede ser un objeto `pandas.DataFrame` o un string que contenga la ruta al archivo CSV que contiene los datos.
* **`region_isocode`**: `str`</br>
El nombre de la columna que contiene los códigos ISO que identifcan a la región geográfica. Por ejemplo: `COUNTRY_ISOCODE`.
* **`region_name`**: `str`</br>
El nombre de la columna que contiene el nombre de la región (no importa el idioma). Por ejemplo: `COUNTRY_SHORT_SPANISH_NAME`.
* **`name`**: `str`</br>
El nombre de la columna empleada para categorizar los datos. Por ejemplo: en el caso de consumo de alta frecuencia, `SHORT_SPANISH_NAME`; en el caso de actividad sectorial, `SUBSECTOR_SHORT_SPA`, etc.

Ejemplo:

```python
# Si los datos están contenidos en un CSV:
val_investment = Validator('final_table_investment.csv', region_isocode='COUNTRY_ISOCODE',
                           region_name='COUNTRY_SHORT_SPANISH_NAME', name='SHORT_SPANISH_NAME')

# Si los datos están ya en un dataframe de pandas:
val_investment = Validator(df_investment, region_isocode='COUNTRY_ISOCODE',
                           region_name='COUNTRY_SHORT_SPANISH_NAME', name='SHORT_SPANISH_NAME')
```


### 3.3. Ejecutar el proceso de validación

Hay ds formas de ejecutar el proceso de validación:

#### Opción A: usando `is_valid()`

El método `is_valid()` simplemente devuelve `True` si la tabla pasa la prueba de validación, y `False` en caso contrario. No proporciona ningún detalle adicional en caso de que la tabla no pase la prueba. Ejemplo:

```python
val_investment.is_valid() # -> devuelve True (pasó la prueba) o False (no pasó la prueba)
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

1. El número de fechas únicas es menor o igual a 400.
1. Cada combinación posible de nominal/real, código ISO y categoría no tiene fechas faltantes.
1. Cada registro real tiene su correspondiente registro nominal.
1. Cada combinación posible de nominal/real, código ISO y categoría tiene datos para la última fecha.
1. Todas las fechas tienen formato ISO (AAAA-MM-DD). Esto se verifica mediante la búsqueda de un match completo de cada registro de fecha contra la [expresión regular](https://regex101.com/r/0jtIVD/1) `\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])`. Como se observa, no se admiten fechas vacías.
1. Todos los valores de variación interanual tienen el formato correcto. Esto se verifica mediante la búsqueda de un match completo de cada registro contra la [expresión regular](https://regex101.com/r/U4L5uF/1) `.{0}|(-?\d+\.\d{4})`. Sí se admiten valores vacíos. El formato es como sigue:
   1. *Signo*, ya sea negativo (`-`) o ausencia de signo (no se admite el signo positivo `+`).
   1. *Parte entera*, consistente en uno o más dígitos.
   1. *Separador decimal*, es obligatorio y debe ser un punto.
   1. *Parte decimal*, compuesta por exactamente 4 dígitos (de acuerdo con las políticas, si es necesario deben agregarse ceros a la derecha hasta completar las cuatro cifras de la parte decimal).

