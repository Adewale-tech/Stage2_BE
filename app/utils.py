from app.models import Country

def save_countries_to_db(db, countries_data):
    saved_list = []

    for country in countries_data:
        exists = db.query(Country).filter_by(name=country.get("name")).first()
        if exists:
            saved_list.append(exists)
            continue

        new_country = Country(
            name=country.get("name"),
            capital=country.get("capital"),
            region=country.get("region"),
            population=country.get("population"),
            flag=country.get("flag"),
            currency=country["currencies"][0]["code"] if country.get("currencies") else None,
        )
        db.add(new_country)
        db.commit()
        db.refresh(new_country)
        saved_list.append(new_country)

    return saved_list
