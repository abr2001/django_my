import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def _load_models():
    from main.models import Country, Wine

    return Country, Wine


Country, Wine = _load_models()

countries_data = [
    {'name': 'Франция', 'code': 'FR'},
    {'name': 'Италия', 'code': 'IT'},
    {'name': 'Испания', 'code': 'ES'},
    {'name': 'Германия', 'code': 'DE'},
]

def migrate_countries():
    print("Создание стран...")
    for country_data in countries_data:
        country, created = Country.objects.get_or_create(
            name=country_data['name'],
            defaults={'code': country_data['code']}
        )
        if created:
            print(f"✓ Создана страна: {country.name}")
        else:
            print(f"- Страна уже существует: {country.name}")
    
    print("\nМиграция данных вин...")
    wines = Wine.objects.all()
    
    for wine in wines:
        if wine.country_old and not wine.country:
            try:
                country = Country.objects.get(name=wine.country_old)
                wine.country = country
                wine.save()
                print(f"✓ Обновлено вино: {wine.name} -> {country.name}")
            except Country.DoesNotExist:
                print(f"✗ Страна не найдена для вина: {wine.name} ({wine.country_old})")
    
    print(f"\nВсего вин: {Wine.objects.count()}")
    print(f"Вин с новым полем country: {Wine.objects.filter(country__isnull=False).count()}")
    print(f"Вин без country: {Wine.objects.filter(country__isnull=True).count()}")

if __name__ == '__main__':
    migrate_countries()
