from countries.models import Country, Region, Domain


def create_region(obj, row):
    region, region_created = Region.objects.get_or_create(
        name=row.get("region")
    )
    if region_created:
        obj.stdout.write(
            obj.style.SUCCESS("Region: {} - Created".format(region))
        )

    return region


def create_country(obj, row, region):
    country, country_created = Country.objects.get_or_create(
        name=row.get("name"),
        defaults={
            "alpha2Code": row.get("alpha2Code"),
            "alpha3Code": row.get("alpha3Code"),
            "population": row.get("population"),
            "capital": row.get('capital', ' '),
            "region": region,
        },
    )

    obj.stdout.write(
        obj.style.SUCCESS(
            "{} - {}".format(
                country, "Created" if country_created else "Updated"
            )
        )
    )

    return country


def create_domain(obj, country, domains):
    for item in domains:
        domain, domain_created = Domain.objects.get_or_create(name=item)

        if domain_created:
            obj.stdout.write(
                obj.style.SUCCESS("Domain: {} - Created".format(domain))
            )

        country.top_level_domain.add(domain)
