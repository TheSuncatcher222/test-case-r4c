from datetime import datetime
import os

from django.test import TestCase
from freezegun import freeze_time
import pandas

from ..models import Robot
from ..views import create_robots_data


class ExcelTestCase(TestCase):
    """
    Производит тестирование создания excel файла.
    """
    def setUp(self):
        self.TEST_EXCEL = 'robots/tests/test_summary_for_week_robots.xlsx'
        self.TARGET_EXCEL = 'robots/summary_for_week_robots.xlsx'
        self.CSV_DATA = 'robots/tests/test_data.csv'
        data = pandas.read_csv(
            self.CSV_DATA,
            # Поле Mark сделано для визуального отображения в CSV файле
            # какие модели не должны попасть в выборку при mock даты
            # на 2022-01-17 20:20:20
            delimiter=';',
        )
        print(data)
        objects: list = []
        for _, row in data.iterrows():
            created_date = datetime.strptime(
                row['created'], '%Y-%m-%d %H:%M:%S'
            )
            objects.append(
                Robot(
                    model=row['model'],
                    version=row['version'],
                    created=created_date,
                )
            )
        Robot.objects.bulk_create(objects)

    @freeze_time('2022-01-17 20:20:20')
    def test_create_excel(self):
        assert Robot.objects.all().count() == 13
        create_robots_data()
        df1 = pandas.read_excel(self.TEST_EXCEL)
        df2 = pandas.read_excel(self.TARGET_EXCEL)
        assert df1.equals(df2)
        return

    def tearDown(self):
        """
        Удаляет сгенерированный в тестах файл summary_for_week_robots.xlsx.
        """
        try:
            os.remove(self.TARGET_EXCEL)
        except FileNotFoundError:
            pass
        return
