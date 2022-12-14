from csv import DictReader, reader

from django.db import migrations


def add_ingredients(apps, schema_editor):
    file = (
        '/app/foods/ingredients.csv'
    )
    ingredient = apps.get_model('foods', 'Ingredient')
    for row in reader(open(file, encoding='utf-8')):
        print(row)
        data = ingredient(name=row[0],
                          measurement_unit=row[1])
        data.save()


def remove_ingredients(apps, schema_editor):
    file = (
        '/app/foods/ingredients.csv'
    )
    ingredient = apps.get_model('foods', 'Ingredient')
    for row in DictReader(open(file, encoding='utf-8')):
        ingredient.odjects.get(name=row[0]).delete()


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
