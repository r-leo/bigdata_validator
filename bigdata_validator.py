#
# -----------------------------------------------------------------------------
# bigdata_validator
# Rodrigo Leo
# -----------------------------------------------------------------------------
#


# Module version
__version__ = '3.0.0'


# Import dependencies
import pandas as pd
from datetime import datetime
from enum import Enum, auto
from typing import Union
from textwrap import dedent


# High frequency indicators
class HF(Enum):
    CONSUMPTION = auto()
    EXTERNAL = auto()
    INVESTMENT = auto()
    SECTORAL = auto()

# High granularity indicators
class HGC(Enum):
    COUNTRY = auto()
    REGIONS = auto()
    STATES = auto()
    CITIES = auto()


# Main class
class Validator:
    version = __version__

    def __init__(self, data: str,
                 indicator: Union[HF, HGC],
                 file_separator: str = ',',
                 decimal_separator: str = '.',
                 is_global: bool = False):
        
        self.indicator = indicator
        self.decimal_separator = decimal_separator
        self.valid_decimal_separator = True
        self.invalid_decimal_message = ""

        self.requires_total = False
        self.order = []

        if isinstance(self.indicator, HGC) or self.indicator in (HF.CONSUMPTION, HF.INVESTMENT):
        #if indicator.name.lower().startswith('hg_') or indicator.name.lower() in ('hf_investment', hf):
            self.requires_total = True
        elif self.indicator == HF.EXTERNAL:
            self.order = ['Exports', 'Imports']
        
        if self.decimal_separator not in ('.', ','):
            self.valid_decimal_separator = False
            self.invalid_decimal_message = f'ERROR: El separador decimal "{self.decimal_separator}" no es válido. Sólo se admite punto (".") o coma (",").'
            print(self.invalid_decimal_message)
            return
        
        df = pd.read_csv(data, sep=file_separator, dtype=str, skip_blank_lines=False).fillna('')
        
        blank_cols = len([c for c in df.columns[1:] if 'Unnamed:' in c]) + 1

        for i in range(blank_cols):
            column_name = [v.strip().lower() for v in df.iloc[:,i].values if v.strip() != ''][0]
            df = df.rename(columns={df.columns[i]: column_name})
        
        blank_rows = len([v for v in df['date'].values if v.strip() == '']) + 1
        df = df.rename(columns={col: col.lower() for col in df.columns})
        df = df.iloc[blank_rows:,:].rename(columns={'type %': 'type', 'isocode': 'iso'})
        df = df.drop(columns='graph', errors='ignore')

        df['type'] = df['type'].apply(lambda x: x.strip()[0].upper())
        
        self.df = df
        self.date_min = self.df['date'].min()
        self.date_max = self.df['date'].max()
        self.days = (datetime.fromisoformat(self.date_max) - datetime.fromisoformat(self.date_min)).days + 1
        self.errors = []

    def _test_regex(self, series: pd.Series, regex: str) -> dict:
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
        fails = (self.df[['type', 'iso', 'date']]
                 .drop_duplicates()
                 .groupby(['type', 'iso'])
                 .agg({'date': 'count'}).reset_index()
                 .query(f'date != {self.days}')
                 .drop(columns='date')).values
        # fails = (self.df
        #          .query('iso != "Total"')
        #          [['type', 'iso', 'date']].drop_duplicates()
        #          .groupby(['type', 'iso'])
        #          .agg({'date': 'count'}).reset_index()
        #          .query(f'date != {self.days}')
        #          .drop(columns='date')).values
        for f in fails:
            self.errors.append(f'La combinación {f} tiene fechas faltantes.')

    def _test_nr_correspondence(self) -> None:
        df_n = self.df.query('type == "N"')
        df_r = self.df.query('type == "R"')
        # df_n = self.df.query('type == "Nominal" and value != ""')
        # df_r = self.df.query('type == "R" and value != ""')
        if len(df_n) < len (df_r):
            self.errors.append('Existen datos reales sin su correspondiente '
                               'valor nominal.')

    def _test_dates(self) -> None:
        dates = self.df['date']
        regex = r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])'
        test = self._test_regex(dates, regex)
        if len(test['rows_nomatch']) > 0:
            self.errors.append(f'Fechas erróneas en la(s) fila(s): '
                               f'{", ".join(test["rows_nomatch"])}')

    def _test_values(self) -> None:
        if self.decimal_separator == '.':
            regex = r'.{0}|(-?\d+\.\d{4})'
        else:
            regex = r'.{0}|(-?\d+,\d{4})'
        values = self.df.iloc[:,5:]
        for col in values.columns:
            test = self._test_regex(values[col], regex)
            if len(test['rows_nomatch']) > 0:
                self.errors.append(f'Valores erróneos en la(s) fila(s): '
                                f'{", ".join(test["rows_nomatch"])}')
    
    def _test_last_observation(self) -> None:
        value_columns = self.df.columns[5:]
        for col in value_columns:
            missing = self.df.query(f'date == "{self.date_max}" and `{col}` == ""')[['type', 'iso']].values
        for m in missing:
            self.errors.append(f'El registro {m} no tiene datos para la '
                               'última fecha.')
    
    def _test_total(self) -> None:
        if self.requires_total and 'total' not in self.df.columns[-1]:
            self.errors.append('Falta la columna de total.')
    
    def _test_order(self) -> None:
        if len(self.order) > 0:
            #actual_order = list(self.df['name'].unique())
            if False:#if self.order != actual_order:
                self.errors.append(f'El orden correcto es: {self.order}.')

    def is_valid(self) -> bool:
        if not self. valid_decimal_separator:
            return False
        self._test_date_number()
        self._test_date_continuity()
        self._test_nr_correspondence()
        self._test_dates()
        self._test_values()
        self._test_last_observation()
        self._test_total()
        self._test_order()
        return True if len(self.errors) == 0 else False
    
    def validate(self) -> None:
        if not self.valid_decimal_separator:
            print(self.invalid_decimal_message)
            return
        if self.is_valid():
            print('No se encontraron errores.')
        else:
            print(f'{len(self.errors)} tipo(s) de error(es) encontrado(s):\n')
            for e in enumerate(self.errors, start=1):
                print(f'{e[0]}\t{e[1]}')
