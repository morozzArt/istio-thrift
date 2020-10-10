namespace py country

struct Country {
    1: string name,
    2: i32 id = 0,
    3: string currency,
    4: string capital
}

service CountryManager {
    Country get_country(1: string name)
}