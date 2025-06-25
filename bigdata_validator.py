import pandas as pd

from datetime import datetime
from typing import TypeAlias, Union

pandasSeries: TypeAlias = pd.Series
pandasDataFrame: TypeAlias = pd.DataFrame
data: TypeAlias = Union[str, pd.DataFrame]


class Validator:
    def __init__(self, data: data = None, *, region_isocode: str = None,
                 region_name: str = None, category: str = None) -> None:
        if type(data) == str:
            self.df = pd.read_csv(filename, dtype=str, skip_blank_lines=False)
            self.df = self.df.fillna('')
        elif type(data) == pandasDataFrame:
            self.df = dataframe.copy()
        self.df = self.df.rename(columns={
            'NOMINAL_REAL_TYPE': 'type',
            'INTERANUAL_VARIATION_DATE': 'date',
            'INTERANUAL_VARIATION': 'value',
            region_isocode: 'iso',
            region_name: 'name'})
        self.category = category
        self.date_min = self.df.query('date != ""')['date'].min()
        self.date_max = self.df.query('date != ""')['date'].max()
        self.days = (datetime.fromisoformat(self.date_max)
                     - datetime.fromisoformat(self.date_min)).days + 1
        self.errors = []

    def _test_regex(self, series: pandasSeries, regex: str) -> dict:
        series = series.copy()
        results = series.str.fullmatch(regex)
        match_true = series[results]
        match_false = series[results == False]
        return {
            'results': results,
            'matchs': match_true,
            'nomatchs': match_false,
            'rows_match': list(map(str, match_true.index + 2)),
            'rows_nomatch': list(map(str, match_false.index + 2))}
    
    def _test_date_number(self) -> None:
        unique_dates = self.df['date'].unique()
        if len(unique_dates) > 400:
            self.errors.append('El número de fechas es mayor a 400.')

    def _test_date_continuity(self) -> None:
        fails = (self.df
                 .query('iso != "Total"')
                 [['type', 'iso', 'name', 'date']].drop_duplicates()
                 .groupby(['type', 'iso', 'name'])
                 .agg({'date': 'count'}).reset_index()
                 .query(f'date != {self.days}')
                 .drop(columns='date')).values
        for f in fails:
            self.errors.append(f'La combinación {f} tiene fechas faltantes.')

    def _test_nr_correspondence(self) -> None:
        df_n = self.df.query('type == "N" and value != ""')
        df_r = self.df.query('type == "R" and value != ""')
        if len(df_n) < len (df_r):
            self.errors.append('Existen datos reales sin su correspondiente '
                               'valor nominal.')

    def _test_dates(self) -> None:
        dates = self.df['date']
        regex = r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])'
        test = self._test_regex(dates, regex)
        if len(test['rows_nomatch']) > 0:
            self.errors.append(f'Fechas erróneas en la(s) fila(s): '
                               f'{",".join(test["rows_nomatch"])}')

    def _test_values(self) -> None:
        values = self.df['value']
        regex = r'.{0}|(-?\d+\.\d{4})'
        test = self._test_regex(values, regex)
        if len(test['rows_nomatch']) > 0:
            self.errors.append(f'Valores erróneas en la(s) fila(s): '
                               f'{",".join(test["rows_nomatch"])}')
    
    def _test_last_observation(self) -> None:
        missing = (self.df
                   .query(f'date == "{self.date_max}" and value == ""')
                   [['type', 'iso', 'name']]).values
        for m in missing:
            self.errors.append(f'El registro {m} no tiene datos para la '
                               'última fecha.')
    
    def is_valid(self) -> bool:
        self._test_date_number()
        self._test_date_continuity()
        self._test_nr_correspondence()
        self._test_dates()
        self._test_values()
        self._test_last_observation()
        return True if len(self.errors) == 0 else False
    
    def validate(self) -> None:
        if self.is_valid():
            print('No se encontraron errores.')
        else:
            print(f'Errores encontrados ({len(self.errors)}):\n')
            for e in enumerate(self.errors, start=1):
                print(f'{e[0]}\t{e[1]}')
