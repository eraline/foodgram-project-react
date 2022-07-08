import pandas as pd
from recipes.models import Ingredient


def load_ingredients(path_to_file):
    df = pd.read_csv(path_to_file)
    df.columns = ['name', 'measurement_unit']
    count = 0
    for row in df.to_dict('records'):
        Ingredient.objects.create(
            name=row['name'],
            measurement_unit=row['measurement_unit'])
        count += 1
    print(f'Loaded {count} ingredients')
