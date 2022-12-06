from django.db import migrations
from csv import DictReader, reader


def add_ingredients(apps, schema_editor):
    file = (
        'D:/Dev/foodgram-project-react/backend/foodgram/foods/ingredients.csv'
    )
    Ingredient = apps.get_model('foods', 'Ingredient')
    for row in reader(open(file, encoding='utf-8')):
        print(row)
        data = Ingredient(name=row[0],
                          measurement_unit=row[1])
        data.save()


def remove_ingredients(apps, schema_editor):
    file = (
        'D:/Dev/foodgram-project-react/backend/foodgram/foods/ingredients.csv'
    )
    Ingredient = apps.get_model('foods', 'Ingredient')
    for row in DictReader(open(file, encoding='utf-8')):
        Ingredient.odjects.get(name=row[0]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0008_auto_20221206_2108'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredients,
            remove_ingredients
        ),
    ]