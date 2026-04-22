import csv
from data.classes import Country

countries = []
current_index = -1

with open('data/price_of_healthy_diet_clean.csv', 'r') as csvFile:
    csvReader = csv.DictReader(csvFile)

    for line in csvReader:
        code = line['country_code']
        name = line['country']
        region = line['region']
        
        # If country is NOT in countries array, create and append country
        if not any(country.name == name for country in countries):
            countryObj = Country(code, name, region)
            countries.append(countryObj)
            current_index += 1

        # Append these no matter, the values go from 2017-2024 for each country with no repeats
        year = line['year']
        costPPP = line['cost_healthy_diet_ppp_usd']
        annualCost = line['annual_cost_healthy_diet_usd']
        vegetablesPPP = line['cost_vegetables_ppp_usd']
        fruitsPPP = line['cost_fruits_ppp_usd']
        totalFoodCosts = line['total_food_components_cost']
        countries[current_index].appendAnnualData(year, costPPP, annualCost, vegetablesPPP, fruitsPPP, totalFoodCosts)

# Goes back in list and calculates averages (float type to 2 dec)
for country in countries: 
    country.calcAverages()

# -- Additional thoughts --
# Could try to go back and find a way to calc averages in 1 loop above, but would need to include catches to identify countries with missing annual datas like Zimbabwe, Nicaragua, Taiwan, etc. 
# There are portions of the dataset that are wrong. Viet Nam and USA for example is in the region of Europe. Region has been parsed and added to obj data but might need to removed or not used depending on how much is wrong.