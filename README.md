# Validador de tablas finales

## 1. Objetivo y alcance

El módulo `bigdata_validator` (para Python) se implementó con el propósito de evitar que se envíen a la (nueva) web de Big Data tablas finales erróneas (es decir, no ajustadas a las políticas expresas de los indicadores). Este módulo automatiza el proceso de validación final mediante una única clase `Validator()`. El constructor de esta clase recibe como parámetro (entre otros) los datos contenidos en la tabla final que se desea validar. El proceso de validación automática se ejecuta al llamar alguno de los siguientes métodos:

* `.is_valid()`: diseñada para integrarse en el flujo de un script de Python. Devuelve `True` en caso de que los datos pasen exitosamente el proceso de validación, y `False` en caso contrario.
* `.validate()`: imprime en pantalla un breve reporte enlistando los errores encontrados, si los hay.

## 2. Documentación

### 2.1. Instalación y uso

Para instalar, ejecutar desde la línea de comandos:

```
pip install git+https://github.com/r-leo/bigdata_validator.git
```

Para importar el módulo, añadir esta línea al inicio de script .py, en una celda de Jupyter o directamente en el intérprete:

```python
from bigdata_validator import Validator
```

### 2.2. Instanciar la clase `Validator` para cada tabla final

La clase `Validator` se instancia (inicializa) pasando como parámetros:

* **`data`**: *`str` o `pandas.DataFrame`*. La tabla final que se va a validar. En caso de pasar un string, éste se interpreta como la ruta del archivo CSV correspondiente.
* **`region_isocode`**: *`str`*. El nombre de la columna que contiene los códigos ISO que identifcan a la región geográfica. Por ejemplo: `COUNTRY_ISOCODE`.
* **`region_name`**: *`str`*. El nombre de la columna que contiene el nombre de la región (no importa el idioma). Por ejemplo: `COUNTRY_SHORT_SPANISH_NAME`.
* **`name`** (`str`): el nombre de la columna empleada para categorizar los datos. Por ejemplo: en el caso de consumo de alta frecuencia, `SHORT_SPANISH_NAME`; en el caso de actividad sectorial, `SUBSECTOR_SHORT_SPA`, etc.

Ejemplo:

```python
# Crear validador para una tabla contenida en un CSV
val_investment = Validator('final_table_investment.csv', region_isocode='COUNTRY_ISOCODE',
                           region_name='COUNTRY_SHORT_SPANISH_NAME', name='SHORT_SPANISH_NAME')

# Si la tabla está en el dataframe de pandas df, entonces:
val = Validator(df...)
```

### 2.3. Validar dentro de un script: `is_valid()`

Para validar la tabla final dentro de un script, basta llamar al método `is_valid()`. Este método devuelve `True` si la tabla pasa la prueba de validación, y `False` en caso contrario.

Ejemplo:

```python
# Crear objetos Validator para una tabla válida y una inválida
table_valid = Validator('path_to_valid_table.csv'...)
table_invalid = Validator('path_to_invalid_table.csv'...)

table_valid.is_valid() # -> devuelve True
table_invalid.is_valid() # -> devuelve False
```

### 2.4. Obtener un reporte de errores: `validate()`

Si se requiere un detalle mayor de los errores encontrados, el método `.validate()` imprime en pantalla un breve reporte con la información.

Ejemplo:

```python
table_invalid = Validator('path_to_invalid_table.csv'...)
table_invalid.validate()
```

El código anterior imprime en la pantalla el reporte de los errores:

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

## 3. Pruebas internas que implementa la clase

El método `.validate()` siempre ejecuta internamente `is_valid()`. Posteriormente, si `Validator.is_valid() == False` imprime en pantalla el listado de errores encontrados. En caso contrario indica al usuario que no se encontró ningún error. Por otra parte, `.is_valid()` devuelve `True` únicamente cuando se satisfacen todas las siguientes condiciones:

1. Que el número de fechas únicas sea menor o igual a 400.
1. Que cada combinación posible de nominal/real, código ISO y categoría no tenga fechas faltantes.
1. Que cada registro real tenga su correspondiente registro nominal.
1. Que cada combinación posible de nominal/real, código ISO y categoría tenga datos para la última fecha.
1. Que todas las fechas tengan formato ISO (AAAA-MM-DD). Esto se verifica mediante la búsqueda de un match completo de cada registro de fecha contra la [expresión regular](https://regex101.com/r/0jtIVD/1) `\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])`. Como se observa, no se admiten fechas vacías.
1. Que todos los valores de variación interanual tengan el formato correcto. Esto se verifica mediante la búsqueda de un match completo de cada registro contra la [expresión regular](https://regex101.com/r/U4L5uF/1) `.{0}|(-?\d+\.\d{4})`. Como se observa, se admiten valores vacíos. El formato es como sigue:
   1. Signo: signo negativo (`-`) o ausencia de signo (no se admite el signo positivo `+`).
   1. Parte entera: uno o más dígitos.
   1. Separador decimal (obligatorio), debe ser un punto.
   1. Parte decimal: compuesta por exactamente 4 dígitos. Si es necesario deben agregarse ceros a la derecha hasta completar las cuatro cifras.

