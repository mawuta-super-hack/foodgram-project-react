
from django.db import migrations

INITIAL_TAGS = [
    {'name': 'Завтрак', 'color': '#006EFF', 'slug': 'breakfast'},
    {'name': 'Обед', 'color': '#FFF338', 'slug': 'lunch'},
    {'name': 'Ужин', 'color': '#FF19A7', 'slug': 'dinner'}
]


def add_tags(apps, schema_editor):
    Tag = apps.get_model('foods', 'Tag')
    for tag in INITIAL_TAGS:
        print(tag)
        data = Tag(**tag)
        data.save()


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('foods', 'Tag')
    for tag in INITIAL_TAGS:
        Tag.objects.get(name=tag['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0010_auto_20221211_1856'),
    ]

    operations = [
        migrations.RunPython(
            add_tags,
            remove_tags
        ),
    ]
