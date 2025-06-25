# Validador de tablas finales

## 1. Propósito

Para evitar que se envíen a la web de Big Data tablas que erróneas, se implementa el módulo de validación `Validator`. Este módulo recibe como entrada la ruta de un archivo CSV o bien un dataframe de `pandas` con todas las columnas de tipo `str`.

La clase `Validator` implementa dos métodos (funciones) de validación:

* `.is_valid()`: pensada para integrarse en un script de Python. Devuelve `True` o `False` como resultado de la validación.
* `.validate()`: imprime en pantalla un pequeño reporte con los errores encontrados, si los hay.

## 2. Documentación

### 2.1. Instalación y uso

Para instalar en el entorno de Python actual:

```
pip install git+https://github.com/r-leo/bigdata_validator.git
```

Para importar el módulo:

```python
from bigdata_validator import Validator
```

### 2.2. Instanciar la clase `Validator` para cada tabla final

La clase `Validator` se instancia pasando como parámetros:

* **`data`** (`str` o `pandas.DataFrame`): la tabla final que se va a validar. En caso de pasar un string, éste se interpreta como la ruta de un archivo CSV.
* **`region_isocode`** (`str`): el nombre de la columna que contiene los códigos ISO regionales.
* **`region_name`** (`str`): el nombre de una de las columnas que contiene el nombre de la región (no importa el idioma).
* **`category`** (`str`): el tipo de indicador que contiene la tabla final. Los valores posibles son: `hf` (high frequency) y `hg` (high granulatity).

Ejemplo:

```python
# Crear validador para una tabla contenida en un CSV
val_investment = Validator('final_table_investment.csv', region_isocode='country_isocode',
                           region_name='country_short_spanish_name', category='hf')

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

table_valid.is_valid() # devuelve True
table_invalid.is_valid() # devuelve False
```

### 2.4. Obtener un reporte de errores: `validate()`

Por el contrario, para imprimir en la pantalla un reporte con los errores encontrados, basta llamar al método `.validate()`.

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

## 3. Pruebas que implementa la clase

El método `Validator.is_valid()` devuelve `True` únicamente cuando se satisfacen todas las siguientes condiciones (nota: `validate()` siempre llama internamente a `is_valid()`, e imprime el reporte de errores sólo si `is_valid()` es `False`):

* Que el número de fechas únicas sea menor o igual a 400.
* Que cada combinación posible de nominal/real, código ISO y categoría no tenga fechas faltantes.
* Que cada registro real tenga su correspondiente registro nominal.
* Que cada combinación posible de nominal/real, código ISO y categoría tenga datos para la última fecha.
* Que todas las fechas tengan formato ISO (AAAA-MM-DD). Ejemplos:
  <table id="T_6b266">  <thead>  </thead>  <tbody>    <tr>      <th id="T_6b266_level0_row0" class="row_heading level0 row0" >1</th>      <td id="T_6b266_row0_col0" class="data row0 col0" ></td>      <td id="T_6b266_row0_col1" class="data row0 col1" >❌</td>    </tr>    <tr>      <th id="T_6b266_level0_row1" class="row_heading level0 row1" >2</th>      <td id="T_6b266_row1_col0" class="data row1 col0" >02-03-2025</td>      <td id="T_6b266_row1_col1" class="data row1 col1" >❌</td>    </tr>    <tr>      <th id="T_6b266_level0_row2" class="row_heading level0 row2" >3</th>      <td id="T_6b266_row2_col0" class="data row2 col0" >02-03-25</td>      <td id="T_6b266_row2_col1" class="data row2 col1" >❌</td>    </tr>    <tr>      <th id="T_6b266_level0_row3" class="row_heading level0 row3" >4</th>      <td id="T_6b266_row3_col0" class="data row3 col0" >2014-07-31</td>      <td id="T_6b266_row3_col1" class="data row3 col1" >✅</td>    </tr>    <tr>      <th id="T_6b266_level0_row4" class="row_heading level0 row4" >5</th>      <td id="T_6b266_row4_col0" class="data row4 col0" >2024-01-12</td>      <td id="T_6b266_row4_col1" class="data row4 col1" >✅</td>    </tr>    <tr>      <th id="T_6b266_level0_row5" class="row_heading level0 row5" >6</th>      <td id="T_6b266_row5_col0" class="data row5 col0" >2024-12-20</td>      <td id="T_6b266_row5_col1" class="data row5 col1" >✅</td>    </tr>    <tr>      <th id="T_6b266_level0_row6" class="row_heading level0 row6" >7</th>      <td id="T_6b266_row6_col0" class="data row6 col0" >2024-12-32</td>      <td id="T_6b266_row6_col1" class="data row6 col1" >❌</td>    </tr>    <tr>      <th id="T_6b266_level0_row7" class="row_heading level0 row7" >8</th>      <td id="T_6b266_row7_col0" class="data row7 col0" >2024-13-25</td>      <td id="T_6b266_row7_col1" class="data row7 col1" >❌</td>    </tr>    <tr>      <th id="T_6b266_level0_row8" class="row_heading level0 row8" >9</th>      <td id="T_6b266_row8_col0" class="data row8 col0" >24-01-12</td>      <td id="T_6b266_row8_col1" class="data row8 col1" >❌</td>    </tr>  </tbody></table>

* Que todos los valores de variación interanual tengan el formato correcto. Ejemplos:
  <table id="T_98fad">  <thead>  </thead>  <tbody>    <tr>      <th id="T_98fad_level0_row0" class="row_heading level0 row0" >1</th>      <td id="T_98fad_row0_col0" class="data row0 col0" ></td>      <td id="T_98fad_row0_col1" class="data row0 col1" >✅</td>    </tr>    <tr>      <th id="T_98fad_level0_row1" class="row_heading level0 row1" >2</th>      <td id="T_98fad_row1_col0" class="data row1 col0" >-0.123</td>      <td id="T_98fad_row1_col1" class="data row1 col1" >❌</td>    </tr>    <tr>      <th id="T_98fad_level0_row2" class="row_heading level0 row2" >3</th>      <td id="T_98fad_row2_col0" class="data row2 col0" >-0.1342</td>      <td id="T_98fad_row2_col1" class="data row2 col1" >✅</td>    </tr>    <tr>      <th id="T_98fad_level0_row3" class="row_heading level0 row3" >4</th>      <td id="T_98fad_row3_col0" class="data row3 col0" >.1234</td>      <td id="T_98fad_row3_col1" class="data row3 col1" >❌</td>    </tr>    <tr>      <th id="T_98fad_level0_row4" class="row_heading level0 row4" >5</th>      <td id="T_98fad_row4_col0" class="data row4 col0" >1.2000</td>      <td id="T_98fad_row4_col1" class="data row4 col1" >✅</td>    </tr>    <tr>      <th id="T_98fad_level0_row5" class="row_heading level0 row5" >6</th>      <td id="T_98fad_row5_col0" class="data row5 col0" >1.2345</td>      <td id="T_98fad_row5_col1" class="data row5 col1" >✅</td>    </tr>    <tr>      <th id="T_98fad_level0_row6" class="row_heading level0 row6" >7</th>      <td id="T_98fad_row6_col0" class="data row6 col0" >12.345</td>      <td id="T_98fad_row6_col1" class="data row6 col1" >❌</td>    </tr>    <tr>      <th id="T_98fad_level0_row7" class="row_heading level0 row7" >8</th>      <td id="T_98fad_row7_col0" class="data row7 col0" >12.3456</td>      <td id="T_98fad_row7_col1" class="data row7 col1" >✅</td>    </tr>    <tr>      <th id="T_98fad_level0_row8" class="row_heading level0 row8" >9</th>      <td id="T_98fad_row8_col0" class="data row8 col0" >123.4567</td>      <td id="T_98fad_row8_col1" class="data row8 col1" >✅</td>    </tr>  </tbody></table>
