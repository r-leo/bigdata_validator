# Validador de tablas finales

Para evitar que se envíen a la web de Big Data tablas que erróneas, se implementa el módulo de validación `Validator`. Este módulo recibe como entrada la ruta de un archivo CSV o bien un dataframe de `pandas` con todas las columnas de tipo `str`.

La clase `Validator` implementa dos métodos (funciones) de validación: una pensada para integrarse en un script de Python (`.is_valid()`, que devuelve un `True` o `False` como resultado de la validación) y otra para imprimir en la pantalla un pequeño reporte con los errores encontrados, si los hay (`.validate()`).

## 2. Documentación

### 2.1. Instanciar la clase `Validator` para cada tabla final

La clase `Validator` se instancia pasando como parámetros:

* `data` (`str` o `pandas.DataFrame`): la tabla final que se va a validar. En caso de pasar un string, éste se interpreta como la ruta de un archivo CSV.
* `region_isocode` (`str`): el nombre de la columna que contiene los códigos ISO regionales.
* `region_name` (`str`): el nombre de una de las columnas que contiene el nombre de la región (no importa el idioma).
* `category` (`str`): el tipo de indicador que contiene la tabla final. Los valores posibles son: `hf` (high frequency) y `hg` (high granulatity).

Ejemplo:

```python
# Crear validador para una tabla contenida en un CSV
val_investment = Validator('final_table_investment.csv', region_isocode='country_isocode',
                           region_name='country_short_spanish_name', category='hf')

# Si la tabla está en el dataframe de pandas df, entonces:
val = Validator(df...)
```

### 2.2. Si la validación se hace dentro de un script, usar `is_valid()`

### 2.3. Si la validación se hace en un entorno donde se espera un reporte de los errores, usar `validate()`
