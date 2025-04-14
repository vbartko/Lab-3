#******************************************************************************
# Author:           Vee Bartko
# Lab:              Lab 3
# Date:             5 July 2024
# Description:      This program finds the neutron flux of a gold foil sample,
#                   and averages fluxes upon user request.
# Input:            float mass, float irradiationTime,
#                   float delayBeforeCountTime, float activity
# Output:           float flux and float average flux
# Sources:          Lab 3 specifications, python documentation, and
#                   the Department of Energy Handbook (for flux equation)
#******************************************************************************
import math

def main():
    mass = 0.0
    irradiationTime = 0.0
    countingTime = 0.0
    activity = 0.0
    flux = 0.0
    avg = True
    average = 0.0
    n = 0
    repeat = True

    while repeat:
        mass, irradiationTime, countingTime = getSampleInfo()
        activity = getActivity()
        flux = getFlux(mass, irradiationTime, countingTime, activity)

        print("The flux is ", round(flux,0), " neutrons per square centimeter seconds.")

        if avg == True:
            average, n = getAverage()
            average += flux
            average = average / n
            print("The average flux is ", round(average,0), " neutrons per square centimeter seconds.")

        ask = input("Do you want to start over and find the flux of other samples? (y/n) ")
        if ask == "n":
            repeat = False
        elif ask == "y":
            repeat = True
        else:
            print("Please enter y or n!")

#Get the sample information
def getSampleInfo():
    mass = float(input("Enter mass of sample in grams: "))
    irradiationTime = float(input("Enter irradiation time in seconds: "))
    countingTime = float(input("Enter the time between the end of the "
                               "irradiation \nand the start of the count"
                               " in seconds: "))
    return mass, irradiationTime, countingTime

#Get the activity of the sample using the branching ratio of gold (Au-197)
def getActivity():
    branch412 = 0.9562
    branch676 = 0.00805
    branch1088 = 0.001589
    activity412 = float(input(
        "Enter the activity (in Bq) at the 412 keV peak: "))
    activity676 = float(input(
        "Enter the activity (in Bq) at the 676 keV peak: "))
    activity1088 = float(input(
        "Enter the activity (in Bq) at the 1088 keV peak: "))

    activity = ((activity412*branch412) + (activity676*branch676) + (activity1088*branch1088))
    return activity

#Use the flux equation from the DoE handbook
def getFlux(mass, irradiationTime, countingTime, activity):
#    mole = 6.022*(10**23)
    decayConst = math.log(2)/232770
    atomNum = ((6.022*(10**23))/197.96)*mass
    crossSection = 98.8

    flux = ((10**24) *
            (activity*(math.e**(decayConst*countingTime))) /
            (atomNum*crossSection*(1-(math.e**(-1*decayConst*irradiationTime)))))
    return flux

#Get the flux of other samples and add them together, keeping track of the number of samples
def getAverage():
    n = 1
    question = 'y'
    otherMass = 0.0
    otherIrTime = 0.0
    otherCountingTime = 0.0
    otherActivity = 0.0
    average = 0.0

    question = input("Do you want to average the flux with another sample? (y/n): ")
    while question.lower() == 'y':
        otherMass = float(input("Enter the mass of another sample (grams): "))
        otherIrTime = float(input("Enter the irradiation time of another sample (seconds): "))
        otherCountingTime = float(input("Enter the time delay before counting another sample (seconds): "))
        otherActivity = float(input("Enter the activity of another sample: "))
        otherFlux = getFlux(otherMass, otherIrTime, otherCountingTime,otherActivity)
        average += otherFlux
        n += 1
        question = input("Do you want to average the flux with another sample? (y/n): ")
    if question.lower() == "n":
        avg = False
    else:
        print("Please enter y or n!")
        question = 'y'
    return average, n

main()