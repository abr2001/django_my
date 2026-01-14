import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def _load_models():
    from main.models import Country, Wine

    return Country, Wine


Country, Wine = _load_models()

wines_data = [
    {
        'name': 'Château Margaux',
        'wine_type': 'red',
        'country': 'Франция',
        'region': 'Бордо',
        'year': 2015,
        'price': 45000,
        'volume': 750,
        'alcohol': 13.5,
        'description': 'Легендарное вино из региона Бордо. Элегантное и сложное, с нотами черной смородины, фиалки и кедра.',
        'grape_variety': 'Каберне Совиньон, Мерло',
        'in_stock': True,
    },
    {
        'name': 'Barolo Riserva',
        'wine_type': 'red',
        'country': 'Италия',
        'region': 'Пьемонт',
        'year': 2016,
        'price': 12500,
        'volume': 750,
        'alcohol': 14.0,
        'description': 'Король итальянских вин. Мощное и структурированное вино с ароматами розы, вишни и трюфеля.',
        'grape_variety': 'Неббиоло',
        'in_stock': True,
    },
    {
        'name': 'Rioja Gran Reserva',
        'wine_type': 'red',
        'country': 'Испания',
        'region': 'Риоха',
        'year': 2014,
        'price': 8900,
        'volume': 750,
        'alcohol': 13.8,
        'description': 'Выдержанное испанское вино с богатым вкусом ванили, кожи и спелых фруктов.',
        'grape_variety': 'Темпранильо',
        'in_stock': True,
    },
    {
        'name': 'Chablis Grand Cru',
        'wine_type': 'white',
        'country': 'Франция',
        'region': 'Бургундия',
        'year': 2019,
        'price': 15000,
        'volume': 750,
        'alcohol': 12.5,
        'description': 'Минеральное белое вино с нотами зеленого яблока, цитрусов и морской соли.',
        'grape_variety': 'Шардоне',
        'in_stock': True,
    },
    {
        'name': 'Riesling Spätlese',
        'wine_type': 'white',
        'country': 'Германия',
        'region': 'Мозель',
        'year': 2020,
        'price': 4500,
        'volume': 750,
        'alcohol': 8.5,
        'description': 'Полусладкое немецкое вино с ароматами персика, абрикоса и медовых нот.',
        'grape_variety': 'Рислинг',
        'in_stock': True,
    },
    {
        'name': 'Sancerre',
        'wine_type': 'white',
        'country': 'Франция',
        'region': 'Луара',
        'year': 2021,
        'price': 3200,
        'volume': 750,
        'alcohol': 12.0,
        'description': 'Свежее и ароматное вино с нотами крыжовника, лайма и минералов.',
        'grape_variety': 'Совиньон Блан',
        'in_stock': True,
    },
    {
        'name': 'Provence Rosé',
        'wine_type': 'rose',
        'country': 'Франция',
        'region': 'Прованс',
        'year': 2022,
        'price': 2800,
        'volume': 750,
        'alcohol': 12.5,
        'description': 'Легкое розовое вино с ароматами клубники, персика и цветов. Идеально для летнего вечера.',
        'grape_variety': 'Гренаш, Сира',
        'in_stock': True,
    },
    {
        'name': 'Bandol Rosé',
        'wine_type': 'rose',
        'country': 'Франция',
        'region': 'Прованс',
        'year': 2021,
        'price': 4200,
        'volume': 750,
        'alcohol': 13.0,
        'description': 'Элегантное розовое вино с насыщенным вкусом красных ягод и пряностей.',
        'grape_variety': 'Мурведр, Гренаш',
        'in_stock': True,
    },
    {
        'name': 'Dom Pérignon',
        'wine_type': 'sparkling',
        'country': 'Франция',
        'region': 'Шампань',
        'year': 2012,
        'price': 28000,
        'volume': 750,
        'alcohol': 12.5,
        'description': 'Престижное шампанское с тонкими пузырьками и ароматами белых цветов, миндаля и бриоши.',
        'grape_variety': 'Шардоне, Пино Нуар',
        'in_stock': True,
    },
    {
        'name': 'Prosecco Superiore',
        'wine_type': 'sparkling',
        'country': 'Италия',
        'region': 'Венето',
        'year': 2022,
        'price': 1800,
        'volume': 750,
        'alcohol': 11.0,
        'description': 'Свежее игристое вино с ароматами зеленого яблока, груши и белых цветов.',
        'grape_variety': 'Глера',
        'in_stock': True,
    },
    {
        'name': 'Cava Reserva',
        'wine_type': 'sparkling',
        'country': 'Испания',
        'region': 'Каталония',
        'year': 2019,
        'price': 2400,
        'volume': 750,
        'alcohol': 11.5,
        'description': 'Испанское игристое вино с нотами цитрусов, белого хлеба и миндаля.',
        'grape_variety': 'Макабео, Парельяда',
        'in_stock': True,
    },
    {
        'name': 'Amarone della Valpolicella',
        'wine_type': 'red',
        'country': 'Италия',
        'region': 'Венето',
        'year': 2015,
        'price': 9800,
        'volume': 750,
        'alcohol': 15.5,
        'description': 'Мощное итальянское вино из подвяленного винограда с ароматами вишни, шоколада и специй.',
        'grape_variety': 'Корвина, Рондинелла',
        'in_stock': True,
    },
]

def populate():
    Wine.objects.all().delete()
    print("Удалены старые записи...")
    
    for wine_data in wines_data:
        country_name = wine_data.pop('country')
        country = Country.objects.get(name=country_name)
        wine = Wine.objects.create(country=country, **wine_data)
        print(f"Добавлено: {wine.name} ({country.name})")
    
    print(f"\nВсего добавлено вин: {Wine.objects.count()}")

if __name__ == '__main__':
    populate()
