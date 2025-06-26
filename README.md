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
1. Que todas las fechas tengan formato ISO (AAAA-MM-DD).
1. Que todos los valores de variación interanual tengan el formato correcto, es decir:
   1. Al inicio: signo negativo (`-`) o ausencia de signo (no se admite el signo positivo `+`).
   1. Uno o más dígitos, seguidos de un punto decimal, seguido de 4 dígitos exactos. Si es necesario deben agregarse ceros a la derecha de la parte decimal.

<table id="T_6b266">  <thead>  </thead>  <tbody>    <tr>      <th id="T_6b266_level0_row0" class="row_heading level0 row0" >1</th>      <td id="T_6b266_row0_col0" class="data row0 col0" ></td>      <td id="T_6b266_row0_col1" class="data row0 col1" >❌</td>    </tr>    <tr>      <th id="T_6b266_level0_row1" class="row_heading level0 row1" >2</th>      <td id="T_6b266_row1_col0" class="data row1 col0" >02-03-2025</td>      <td id="T_6b266_row1_col1" class="data row1 col1" >❌</td>    </tr>    <tr>      <th id="T_6b266_level0_row2" class="row_heading level0 row2" >3</th>      <td id="T_6b266_row2_col0" class="data row2 col0" >02-03-25</td>      <td id="T_6b266_row2_col1" class="data row2 col1" >❌</td>    </tr>    <tr>      <th id="T_6b266_level0_row3" class="row_heading level0 row3" >4</th>      <td id="T_6b266_row3_col0" class="data row3 col0" >2014-07-31</td>      <td id="T_6b266_row3_col1" class="data row3 col1" >✅</td>    </tr>    <tr>      <th id="T_6b266_level0_row4" class="row_heading level0 row4" >5</th>      <td id="T_6b266_row4_col0" class="data row4 col0" >2024-01-12</td>      <td id="T_6b266_row4_col1" class="data row4 col1" >✅</td>    </tr>    <tr>      <th id="T_6b266_level0_row5" class="row_heading level0 row5" >6</th>      <td id="T_6b266_row5_col0" class="data row5 col0" >2024-12-20</td>      <td id="T_6b266_row5_col1" class="data row5 col1" >✅</td>    </tr>    <tr>      <th id="T_6b266_level0_row6" class="row_heading level0 row6" >7</th>      <td id="T_6b266_row6_col0" class="data row6 col0" >2024-12-32</td>      <td id="T_6b266_row6_col1" class="data row6 col1" >❌</td>    </tr>    <tr>      <th id="T_6b266_level0_row7" class="row_heading level0 row7" >8</th>      <td id="T_6b266_row7_col0" class="data row7 col0" >2024-13-25</td>      <td id="T_6b266_row7_col1" class="data row7 col1" >❌</td>    </tr>    <tr>      <th id="T_6b266_level0_row8" class="row_heading level0 row8" >9</th>      <td id="T_6b266_row8_col0" class="data row8 col0" >24-01-12</td>      <td id="T_6b266_row8_col1" class="data row8 col1" >❌</td>    </tr>  </tbody></table>

<table id="T_98fad">  <thead>  </thead>  <tbody>    <tr>      <th id="T_98fad_level0_row0" class="row_heading level0 row0" >1</th>      <td id="T_98fad_row0_col0" class="data row0 col0" ></td>      <td id="T_98fad_row0_col1" class="data row0 col1" >✅</td>    </tr>    <tr>      <th id="T_98fad_level0_row1" class="row_heading level0 row1" >2</th>      <td id="T_98fad_row1_col0" class="data row1 col0" >-0.123</td>      <td id="T_98fad_row1_col1" class="data row1 col1" >❌</td>    </tr>    <tr>      <th id="T_98fad_level0_row2" class="row_heading level0 row2" >3</th>      <td id="T_98fad_row2_col0" class="data row2 col0" >-0.1342</td>      <td id="T_98fad_row2_col1" class="data row2 col1" >✅</td>    </tr>    <tr>      <th id="T_98fad_level0_row3" class="row_heading level0 row3" >4</th>      <td id="T_98fad_row3_col0" class="data row3 col0" >.1234</td>      <td id="T_98fad_row3_col1" class="data row3 col1" >❌</td>    </tr>    <tr>      <th id="T_98fad_level0_row4" class="row_heading level0 row4" >5</th>      <td id="T_98fad_row4_col0" class="data row4 col0" >1.2000</td>      <td id="T_98fad_row4_col1" class="data row4 col1" >✅</td>    </tr>    <tr>      <th id="T_98fad_level0_row5" class="row_heading level0 row5" >6</th>      <td id="T_98fad_row5_col0" class="data row5 col0" >1.2345</td>      <td id="T_98fad_row5_col1" class="data row5 col1" >✅</td>    </tr>    <tr>      <th id="T_98fad_level0_row6" class="row_heading level0 row6" >7</th>      <td id="T_98fad_row6_col0" class="data row6 col0" >12.345</td>      <td id="T_98fad_row6_col1" class="data row6 col1" >❌</td>    </tr>    <tr>      <th id="T_98fad_level0_row7" class="row_heading level0 row7" >8</th>      <td id="T_98fad_row7_col0" class="data row7 col0" >12.3456</td>      <td id="T_98fad_row7_col1" class="data row7 col1" >✅</td>    </tr>    <tr>      <th id="T_98fad_level0_row8" class="row_heading level0 row8" >9</th>      <td id="T_98fad_row8_col0" class="data row8 col0" >123.4567</td>      <td id="T_98fad_row8_col1" class="data row8 col1" >✅</td>    </tr>  </tbody></table>
