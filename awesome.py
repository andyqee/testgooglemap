# coding=utf-8
import os																		# Load the library module
import sys		# Import the Modules
import shutil
import googlemaps
import urllib
from numpy import genfromtxt

api_key = 'AIzaSyAbiie6awXqkyQertU7gHykfPdNvQWPviw' #google api key
#

class Location:

    def __init__(self, dic = None):
        if dic != None:
            self.lat = dic['lat']
            self.lng = dic['lng']

class Bounds:

    def __init__(self, northeast = None, southwest = None):
        if northeast != None and southwest != None:
            self.northeast = Location(northeast)
            self.southwest = Location(southwest)

class City:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.loc = Location()  #位置
        self.bounds = Bounds() #边界



class Province:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.cityList = []
        self.revers = 0


def process_job(inputPath, gmaps):
    allProvinces = dict()
    allProvinces = consturctProvinceFromFiles(inputPath)
    selected_province = {k:v for k, v in allProvinces.iteritems() if len(v.cityList) > 9} # 挑选大的国家进行统计,也就是有10个城市以上的国家
    #geo fetch
    for key, value in selected_province.iteritems():
        prov = value.name

        for city in value.cityList:
            address = prov + ','+ city.name

            geo_list = gmaps.geocode(address)
            loc = geo_list[0]['geometry']
            city.loc = Location(loc['location'])
            city.bounds = Bounds(loc['bounds']['northeast'], loc['bounds']['southwest'])

    reverse_geo(selected_province)

def reverse_geo(province):
    if province:
        return

def consturctProvinceFromFiles(filePath):
    allDic = dict()
    with open(filePath, 'r') as f:
        for line in f.readlines():
            words = line.split('\t')
            provID = words[0]
            if provID in allDic:
                prov = allDic[provID]
                city = City(words[2], words[3])
                prov.cityList.append(city)
            else:
                prov = Province(provID, words[1])
                city = City(words[2], words[3])
                prov.cityList.append(city)
                allDic[provID] = prov

    return allDic

# def reverseLatLonBy(latLon, gmaps):
#
# def latiLongLookup(address, gmaps):


# def compareReversResult():

def main():

    input_file_path = './cityMeta.cvs'
    gmaps = googlemaps.Client(key=api_key)
    process_job(input_file_path, gmaps)


if __name__ == '__main__':
  main()