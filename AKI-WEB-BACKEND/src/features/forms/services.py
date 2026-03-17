from datetime import datetime
from io import BytesIO
from itertools import groupby
from operator import itemgetter
from typing import Sequence

import pandas as pd
from faker import Faker

from . import schemas
from .config import column_key_mapping, column_value_mapping
from .constants import STATUS, TypeCode
from .mappings import map_forms_to_tree
from .repositories import FormRepository, FormPeriodRepository, SceneryRepository, LocationStructureRepository, \
    MeasureRepository
from .schemas import Form, FormColumnDefinition, FormHistory, FormData, CreateFormData, UserFormsSummary, \
    FormRowDefinition, FormColumnGroupDefinition, FormHistoryBase
from .utils import filter_dataframe, get_valid_column
from ...shared.schemas import TreeNode


class FormService:
    def __init__(self, form_repository: FormRepository):
        self.form_repository = form_repository
        self.fake = Faker()

    async def get_form_by_id(self, form_id):
        item = await self.form_repository.get(form_id=form_id, status=STATUS.ACTIVE)
        return schemas.FormBase.model_validate(item) if item else None

    async def get_all_form(self) -> Sequence[Form]:
        result = []
        for _ in range(self.fake.random_int(min=1, max=10)):
            result.append(
                Form(id=self.fake.uuid4(cast_to=None),
                     title=self.fake.company()))
        return result

    async def get_forms_by_group_id(self, group_id):
        return await self.get_all_form()

    async def get_form_columns_by_id(self,
                                     form_id: int,
                                     period_id:  str | int,
                                     user_id: str | None = None,
                                     language_id: int | None = None):
        """
        Retrieves form columns by form ID and period ID.

        Args:
            form_id (int): The ID of the form
            period_id (int): The ID of the period
            user_id (str, optional): The user ID. Defaults to None.
            language_id (int, optional): The language ID. Defaults to None.

        Returns:
            list[FormColumnDefinition]: List of column definitions for the form
        """
        period_id = await self._get_latest_period_id(period_id, form_id)

        histories = await self.form_repository.get_form_history_by_id(form_id=form_id)

        is_new_period = False
        # Check if period_id exists in histories
        if not any(str(history['periodId']).lower() == str(period_id).lower() for history in histories):
            is_new_period = True
            last_period = max(history['periodId'] for history in histories)
            entities = await self.form_repository.get_form_data_by_id(form_id=form_id, period_id=last_period, user_id=user_id, language_id=language_id)
        else:
            entities = await self.form_repository.get_form_data_by_id(form_id=form_id, period_id=period_id, user_id=user_id, language_id=language_id)

        form = await self.form_repository.get(form_id=form_id)
        column_key = 'rowNumber' if form.trasposed else 'colNumber'
        label_1_key = 'rowLabel01' if form.trasposed else 'colLabel01'
        label_2_key = 'rowLabel02' if form.trasposed else 'colLabel02'

        entities.sort(key=itemgetter('formId', column_key))
        grouped_data = {
            key: list(group)
            for key, group in groupby(entities, key=itemgetter('formId', column_key))
        }
        all_uom_empty = all(entity.get('uom', '').strip() == '' for entity in entities)

        result = [
            FormColumnDefinition(col_id='scenarioCode', field='scenarioCode', header_name='Escenario',
                                 filter='agTextColumnFilter', cell_class="mark-pinned-row", pinned="left",
                                 suppress_movable=True, editable=False, hide=True),
            FormColumnDefinition(col_id='locationCode', field='locationCode', header_name='Locación',
                                 filter='agTextColumnFilter', cell_class="mark-pinned-row", pinned="left",
                                 suppress_movable=True, editable=False, hide=True),
            FormColumnDefinition(col_id='measureCode', field='measureCode', header_name='Item',
                                 filter='agTextColumnFilter', cell_class="mark-pinned-row", pinned="left",
                                 suppress_movable=True, editable=False, hide=True),
            FormColumnDefinition(col_id='label', field='label', header_name='Item', resizable=False,
                                 cell_class="mark-pinned-row", pinned="left",
                                 suppress_movable=True, editable=False),
            FormColumnDefinition(col_id='uom', field='uom', header_name='', resizable=False, width=85,
                                 cell_class="mark-pinned-row", pinned="left", suppress_movable=True, editable=False,
                                 hide=all_uom_empty)
        ]

        # TODO: Cambiar columna de periodo
        if is_new_period:
            new_period = await self.form_repository.get_next_period_by_id(form_id=form_id)

        for key, group in grouped_data.items():
            item = group[0]

            label_2 = item.get(label_2_key, '').strip()
            if label_2:
                column = FormColumnGroupDefinition(
                    group_id=str(item[column_key]),
                    header_name=item.get(label_1_key, '').strip(),
                    children=[
                        FormColumnDefinition(
                            col_id=str(item[column_key]),
                            header_name=label_2,
                            field=str(item[column_key]),
                            filter='agNumberColumnFilter',
                            cell_editor='agNumberCellEditor' if any(
                                obj['dataTypeCode'] == 'DEC' for obj in group) else None,
                            editable=any(obj['canEdit'] == 'Y' for obj in group),
                            single_click_edit=any(obj['canEdit'] == 'Y' for obj in group),
                        )
                    ]
                )
            else:
                column = FormColumnDefinition(
                    col_id=str(item[column_key]),
                    header_name=item.get(label_1_key, '').strip(),
                    field=str(item[column_key]), 
                    filter='agNumberColumnFilter',
                    cell_editor='agNumberCellEditor' if any(
                        obj['dataTypeCode'] == 'DEC' for obj in group) else None,
                    editable=any(obj['canEdit'] == 'Y' for obj in group),
                    single_click_edit=any(obj['canEdit'] == 'Y' for obj in group),
                )
            result.append(column)

        return result
    
    async def _get_latest_period_id(self, period_id: str | int, form_id: int) -> int:
        """Gets the latest period ID if 'latest' is specified, otherwise returns the original period_id"""
        if period_id == 'latest':
            histories = await self.form_repository.get_form_history_by_id(form_id=form_id)
            return max(histories, key=lambda x: x['periodCode'])['periodId']
        return period_id

    async def get_form_rows_by_id(self,
                                  form_id: int,
                                  period_id: str | int,
                                  user_id: str | None = None,
                                  language_id: int | None = None):
        """
        Retrieves form rows by form ID and period ID.

        Args:
            form_id (int): The ID of the form to retrieve rows for
            period_id (int): The period ID to retrieve rows for
            user_id (str | None, optional): Optional user ID filter. Defaults to None.
            language_id (int | None, optional): Optional language ID filter. Defaults to None.

        Returns:
            list[FormRowDefinition]: List of form row definitions with their associated data
        """
        period_id = await self._get_latest_period_id(period_id, form_id)

        entities = await self.form_repository.get_form_data_by_id(form_id=form_id,
                                                                  period_id=period_id,
                                                                  user_id=user_id,
                                                                  language_id=language_id)
                
        form = await self.form_repository.get(form_id=form_id)
        column_key = 'rowNumber' if form.trasposed else 'colNumber'
        row_key = 'colNumber' if form.trasposed else 'rowNumber'
        label_1_key = 'colLabel01' if form.trasposed else 'rowLabel01'
        label_2_key = 'colLabel02' if form.trasposed else 'rowLabel02'

        entities.sort(key=itemgetter('formId', row_key, column_key))
        grouped_data = {
            key: list(group)
            for key, group in groupby(entities, key=itemgetter('formId', row_key))
        }

        result = []

        for key, group in grouped_data.items():
            row_base = dict(group[0])
            row_id = row_base.get(row_key, 0)
            row = FormRowDefinition.model_validate(row_base, strict=False)
            row.row_id = row_id

            extra = {}
            for item in group:
                value = None
                if item['dataTypeCode'] == TypeCode.DECIMAL:
                    value = float(item['valueDec']) if item['valueDec'] else None
                extra['isFiller'] = item['isFiller']
                extra['label'] = item[label_1_key]
                extra['uom'] = item[label_2_key]
                period_point = item.get('periodPoint', None)
                if isinstance(period_point, datetime):
                    period_point = str(period_point)
                extra[str(item[column_key])] = value
                extra['cellGroup'] = True if item.get('isFiller', None) == 'Y' and item.get('canEdit', None) == 'N' else False

            row.__pydantic_extra__ = extra

            result.append(row)

        return result

    async def process_form_data(self, form_id: int,
                                period_id: str | int,
                                user_id: str | None = None,
                                language_id: int | None = None, data: pd.DataFrame = None):
        """
        Processes form data based on the provided form_id, period_id, and DataFrame data.

        :param form_id: The ID of the form to process.
        :param period_id: The period ID for the data processing.
        :param user_id: The user ID performing the data processing (optional).
        :param language_id: The language ID for the data processing (optional).
        :param data: DataFrame containing the data to process the form rows.
        :return: List of processed form rows.
        """
        period_id = await self._get_latest_period_id(period_id, form_id)

        histories = await self.form_repository.get_form_history_by_id(form_id=form_id)

        is_new_period = False
        # Check if period_id exists in histories
        if not any(str(history['periodId']) == str(period_id) for history in histories):
            is_new_period = True
            last_period = max(history['periodId'] for history in histories)
            entities = await self.form_repository.get_form_data_by_id(form_id=form_id, period_id=last_period, user_id=user_id, language_id=language_id)
        else:
            entities = await self.form_repository.get_form_data_by_id(form_id=form_id, period_id=period_id, user_id=user_id, language_id=language_id)

        # Ordenar las entidades por formId, rowNumber y colNumber
        entities.sort(key=itemgetter('formId', 'rowNumber', 'colNumber'))
        grouped_data = {
            key: list(group)
            for key, group in groupby(entities, key=itemgetter('formId', 'rowNumber'))
        }

        result = []

        last_group_index = -1
        for key, group in grouped_data.items():
            base_row = dict(group[0])
            row = FormRowDefinition.model_validate(base_row, strict=False)

            extra = {}
            for item in group:
                value_to_set = None

                # TODO: Agregar trim, doble espacio y lowercase
                combined_data = filter_dataframe(data, item, column_key_mapping)

                if item['isFiller'] == 'Y' and not combined_data.empty:
                    last_group_index = int(combined_data.index.max())

                if item['canEdit'] == 'Y':
                    column = get_valid_column(item, list(data.columns), column_value_mapping)
                    if column:
                        filtered_data = combined_data.loc[combined_data.index > last_group_index]
                        if not filtered_data.empty:
                            value_to_set = filtered_data[column].iloc[0]
                            if item['dataTypeCode'] == TypeCode.DECIMAL:
                                value_to_set = float(value_to_set) if value_to_set else None

                extra['isFiller'] = item['isFiller']
                extra['label'] = item['rowLabel01']
                extra['uom'] = item['rowLabel02']
                extra[str(item['colNumber'])] = value_to_set
                extra['cellGroup'] = True if item['isFiller'] == 'Y' and item['canEdit'] == 'N' else False

            row.__pydantic_extra__ = extra

            result.append(row)

        return result

    async def get_form_raw_by_id(self,
                                 form_id: int,
                                 period_id: str | int,
                                 user_id: str | None = None,
                                 language_id: int | None = None) -> Sequence[FormData]:
        period_id = await self._get_latest_period_id(period_id, form_id)

        entities = await self.form_repository.get_form_data_by_id(form_id=form_id,
                                                                  period_id=period_id,
                                                                  user_id=user_id,
                                                                  language_id=language_id)

        return [FormData.model_validate(entity) for entity in entities]

    async def get_form_history_by_id(self, form_id: int):
        entities = await self.form_repository.get_form_history_by_id(form_id=form_id)

        return [FormHistory.model_validate(entity) for entity in entities]

    async def get_next_period_by_id(self, form_id: int):
        item = await self.form_repository.get_next_period_by_id(form_id=form_id)

        return FormHistoryBase.model_validate(item) if item else None

    async def save_form_data(self, items: Sequence[CreateFormData]):
        results = []
        for item in items:
            try:
                await self.form_repository.save_form_data(form_id=item.form_id,
                                                      period_id=item.period_id,
                                                      period_point=item.period_point,
                                                      scenario_id=item.scenario_id,
                                                      location_id=item.location_id,
                                                      measure_id=item.measure_id,
                                                      form_code=item.form_code,
                                                      period_code=item.period_code,
                                                      scenario_code=item.scenario_code,
                                                      location_code=item.location_code,
                                                      measure_code=item.measure_code,
                                                      value_int=item.value_int,
                                                      value_dec=item.value_dec,
                                                      value_float=item.value_float,
                                                      value_text=item.value_text,
                                                      value_boolean=item.value_boolean,
                                                      value_datetime=item.value_datetime,
                                                      user_id=item.user_id)
            except Exception as e:  
                results.append({"success": False, "item": item, "error": str(e)})
            # Compilar reporte
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        
        return {
            "saved": len(successful),
            "errors": len(failed),
            "details": {
                "successful": successful,
                "failed": failed
            }
        }

    async def get_forms_by_user_id(self, user_id: str, language_id: int) -> list[UserFormsSummary]:
        entities = await self.form_repository.get_forms_by_user_id(user_id=user_id, language_id=language_id)

        return [UserFormsSummary.model_validate(entity) for entity in entities]

    async def get_forms_in_tree(self, user_id: str, language_id: int) -> list[TreeNode]:
        entities = await self.get_forms_by_user_id(user_id=user_id, language_id=language_id)

        return map_forms_to_tree(entities)

    async def add_period(self, form_id: int, user_id: str):
        return await self.form_repository.add_period(form_id=form_id, user_id=user_id)

    async def export_form_data_to_excel(self, form_id: int, period_id: int, user_id: str | None = None,
                                        language_id: int | None = None) -> BytesIO:
        """
        Asynchronously exports form data to an Excel file.

        Parameters:
            form_id (int): ID of the form to export data from.
            period_id (int): ID of the period to filter the data.
            user_id (str | None): Optional user ID to filter the data.
            language_id (int | None): Optional language ID to filter the data.

        Returns:
            BytesIO: In-memory Excel file with the exported data.
        """

        # Obtener datos del formulario desde el repositorio
        form_data = await self.form_repository.get_form_data_by_id(
            form_id=form_id,
            period_id=period_id,
            user_id=user_id,
            language_id=language_id
        )

        # Crear un DataFrame a partir de los datos obtenidos
        df = pd.DataFrame.from_dict(form_data, orient='columns')

        value_column = self._select_value_column(df)

        df = self._convert_column_types(df)

        # Pivotar el DataFrame
        df_pivoted = df.pivot(index=['rowNumber', 'rowLabel01', 'rowLabel02'],
                              columns=['colLabel01', 'colLabel02'],
                              values=value_column)

        # Limpiar los nombres de las columnas del DataFrame pivotado
        df_pivoted.columns = [' '.join(col).strip() for col in df_pivoted.columns.values]

        # Restablecer el índice para hacer las columnas accesibles
        df_pivoted_reset = df_pivoted.reset_index()

        # Eliminar la columna 'rowNumber'
        df_pivoted_cleaned = df_pivoted_reset.drop(['rowNumber'], axis=1)

        # Renombrar las columnas para mayor claridad
        df_pivoted_cleaned = df_pivoted_cleaned.rename(columns={
            'rowLabel01': 'Item',
            'rowLabel02': ''
        })

        # Escribir el DataFrame limpio en un archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_pivoted_cleaned.to_excel(writer, index=False)

        output.seek(0)  # Rewind para leer desde el inicio

        return output

    @staticmethod
    def _convert_column_types(df) -> pd.DataFrame:
        """
        Converts DataFrame columns to appropriate types.

        Parameters:
            df (pd.DataFrame): The DataFrame whose columns need type conversion.

        Returns:
            pd.DataFrame: The DataFrame with columns converted to appropriate types.
        """
        df['valueInt'] = pd.to_numeric(df['valueInt'], errors='coerce')
        df['valueDec'] = pd.to_numeric(df['valueDec'], errors='coerce')
        df['valueFloat'] = pd.to_numeric(df['valueFloat'], errors='coerce')
        df['valueBoolean'] = df['valueBoolean'].astype(bool, errors='ignore')
        df['valueDateTime'] = pd.to_datetime(df['valueDateTime'], errors='coerce')

        return df

    @staticmethod
    def _select_value_column(df) -> str:
        """
        Selects the appropriate value column based on data type.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the form data.

        Returns:
            str: The name of the selected value column.
        """
        # Determinar la columna de valor adecuada según el tipo de datos
        data_types = df[df['isFiller'] == 'N']['dataTypeCode'].unique()
        value_columns = {
            TypeCode.INTEGER: 'valueInt',
            TypeCode.DECIMAL: 'valueDec',
            TypeCode.FLOAT: 'valueFloat',
            TypeCode.TEXT: 'valueText',
            TypeCode.BOOLEAN: 'valueBoolean',
            TypeCode.DATETIME: 'valueDateTime'
        }
        for dtype, column in value_columns.items():
            if dtype in data_types:
                return column
        return 'valueText'

    async def save_form_data_from_dataframe(self,
                                            form_id: str | int,
                                            period_id: str | int,
                                            user_id: str | None = None,
                                            language_id: int | None = None,
                                            data: pd.DataFrame = None):

        items = await self.get_create_form_data(form_id=form_id,
                                                period_id=period_id,
                                                user_id=user_id,
                                                language_id=language_id, data=data)

        return await self.save_form_data(items=items)

    async def get_create_form_data(self,
                                   form_id: str | int,
                                   period_id: str | int,
                                   user_id: str | None = None,
                                   language_id: int | None = None,
                                   data: pd.DataFrame = None) -> list[CreateFormData]:

        # Obtener los datos del formulario por form_id y period_id
        entities = await self.form_repository.get_form_data_by_id(form_id=form_id,
                                                                  period_id=period_id,
                                                                  user_id=user_id,
                                                                  language_id=language_id)
        # Ordenar las entidades por formId, rowNumber y colNumber
        entities.sort(key=itemgetter('formId', 'rowNumber', 'colNumber'))
        grouped_data = {
            key: list(group)
            for key, group in groupby(entities, key=itemgetter('formId', 'rowNumber'))
        }

        result = []

        last_group_index = -1
        for key, group in grouped_data.items():

            for item in group:
                value_to_set = None

                # TODO: Agregar trim, doble espacio y lowercase
                combined_data = filter_dataframe(data, item, column_key_mapping)

                if item['isFiller'] == 'Y' and not combined_data.empty:
                    last_group_index = int(combined_data.index.max())
                    continue

                if item['canEdit'] == 'Y':
                    column = get_valid_column(item, list(data.columns), column_value_mapping)
                    if column:
                        filtered_data = combined_data.loc[combined_data.index > last_group_index]
                        if not filtered_data.empty:
                            value_to_set = filtered_data[column].iloc[0]
                            if item['dataTypeCode'] == TypeCode.DECIMAL:
                                value_to_set = float(value_to_set) if value_to_set else None

                    row = CreateFormData.model_validate(item, strict=False)
                    row.user_id = user_id
                    row.value_dec = value_to_set
                    result.append(row)

        return result


class FormPeriodService:
    def __init__(self, period_repository: FormPeriodRepository):
        self.period_repository = period_repository

    async def get_periods_by_form(self, form_id: str | int):
        entities = await self.period_repository.list(form_id=form_id, status=STATUS.ACTIVE)
        return [schemas.FormPeriodBase.model_validate(item) for item in entities]

    async def get_period_by_id(self, period_id: str | int):
        item = await self.period_repository.get(period_id=period_id, status=STATUS.ACTIVE)
        return schemas.FormPeriodBase.model_validate(item) if item else None


class SceneryService:
    def __init__(self, scenery_repository: SceneryRepository):
        self.scenery_repository = scenery_repository

    async def get_all_scenarios(self):
        entities = await self.scenery_repository.list(status=STATUS.ACTIVE)
        return [schemas.SceneryBase.model_validate(item) for item in entities]

    async def get_scenery_by_id(self, scenery_id: str | int):
        item = await self.scenery_repository.get(scenery_id=scenery_id, status=STATUS.ACTIVE)
        return schemas.SceneryBase.model_validate(item) if item else None


class LocationStructureService:
    def __init__(self, location_structure_repository: LocationStructureRepository):
        self.location_structure_repository = location_structure_repository

    async def get_all_locations(self):
        entities = await self.location_structure_repository.list(status=STATUS.ACTIVE)
        return [schemas.LocationStructureBase.model_validate(item) for item in entities]

    async def get_location_by_id(self, location_id: str | int):
        item = await self.location_structure_repository.get(location_id=location_id, status=STATUS.ACTIVE)
        return schemas.LocationStructureBase.model_validate(item) if item else None


class MeasureService:
    def __init__(self, measure_repository: MeasureRepository):
        self.measure_repository = measure_repository

    async def get_all_measures(self):
        entities = await self.measure_repository.list(status=STATUS.ACTIVE)
        return [schemas.MeasureBase.model_validate(item) for item in entities]

    async def get_measure_by_id(self, measure_id: str | int):
        item = await self.measure_repository.get(measure_id=measure_id, status=STATUS.ACTIVE)
        return schemas.MeasureBase.model_validate(item) if item else None
