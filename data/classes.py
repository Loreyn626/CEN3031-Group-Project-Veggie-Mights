'''
Creating a class obj for Country. 
Since there are multiple rows of data for the same countries from years 2017-2024, certain variables are added as arrays.
Skimming the data, there are no years & countries where cost categories have changed and ALL data points have "Estimated Value" for dataQuality.
'''

import math

class Country:
    def __init__(self, code, name, region): 
        # Only created ONCE
        self.code = code
        self.name = name
        self.region = region
        self.dataQuality = "Estimated value"

        # Additonal data provided per yearly values
        self.costCategory = []
        self.years = []
        self.costPPPs = []
        self.annualCosts =[]
        self.vegetablesPPPs = []
        self.fruitsPPPs = []
        self.totalFoodCosts = []

        # Calculated data from above datasets
        self.averagePPP = 0
        self.averageAnnualCost = 0
        self.averageVegetablesPPP = 0
        self.averageFruitsPPP = 0
        self.averageTotalFoodCost = 0
        self.averageCostCategory = ''

    # Using if-else statement to filter object creation on parsing csv, we can use this to add data values to the obj arrays
    def appendAnnualData(self, year, costPPP, annualCost, vegetablesPPP, fruitsPPP, totalFoodCost):
        self.years.append(year)
        self.costPPPs.append(costPPP)
        self.annualCosts.append(annualCost)
        self.vegetablesPPPs.append(vegetablesPPP)
        self.fruitsPPPs.append(fruitsPPP)
        self.totalFoodCosts.append(totalFoodCost)

        # The original dataset did not have any data rows with 'Low Cost' so this is to manually calculate affordability using PPP (purchasing power parity)
        # The numbers can be tweaked
        if float(costPPP) <= 2.5:
            self.costCategory.append('Low Cost')
        elif 2.5 < float(costPPP) <= 3.5:
            self.costCategory.append('Medium Cost')
        else:
            self.costCategory.append('High Cost')

    # Calculates averages for the country from the arrays --> costPPP, annualCost, veggiePPP, totalFoodCost
    def calcAverages(self):
        arrays = [self.costPPPs, self.annualCosts, self.vegetablesPPPs, self.fruitsPPPs, self.totalFoodCosts]
        for index, array in enumerate(arrays):
            valid = [float(i) for i in array if i is not '']
            if len(valid) > 0:
                average = round(sum(valid)/len(valid), 2)
            else:
                average = 'N/A'

            if index == 0:
                self.averagePPP = average
                # Calculates average cost category based on average PPP
                if average <= 2.5:
                    self.averageCostCategory = 'Low Cost'
                elif 2.5 < average <= 3.5:
                    self.averageCostCategory = 'Medium Cost'
                else:
                    self.averageCostCategory = 'High Cost'
            elif index == 1:
                self.averageAnnualCost = average
            elif index == 2:
                self.averageVegetablesPPP = average
            elif index == 3:
                self.averageFruitsPPP = average
            else:
                self.averageTotalFoodCost = average