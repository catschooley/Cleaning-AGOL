from arcgis.gis import GIS
from arcgis.mapping import WebMap
import pandas as pd

from getpass import getpass

print("The default portal to search all of AGOL is 'https://arcgis.com'. If you want to search only your organization's portal it might look something more like 'https://utahdnr.maps.arcgis.com/'.")
portal_url = input("Enter portal to search: ")
username = input("Enter AGOL username: ")
print("Enter password: ")
password = getpass() # this prompts the user to input a password without echoing, better than hard-coding and storing in the python file
gis = GIS(portal_url, username, password)
ownerUsername = input("Please enter username of contents you wish to search: ")
folderPath = input("Enter file path for csv: ")
csvName = input("Enter the name for the csv file. DO NOT INCLUDE FILE EXTENSION: ")
maxItemNumber = int(input("Enter the maximum number of feature service you would like to search. Choose a number less than 10,000: "))

saveLocation = folderPath + csvName + "\\.csv"
unusedList = []

def main():

    print("Logged in as {}".format(gis.properties['user']['username']))

    # creates list of items of all map image, feature, vector tile and image services (up to 10000 of each) in active portal
    services = (gis.content.search(query="owner:" + ownerUsername, item_type="Map Service", max_items=maxItemNumber) +
                gis.content.search(query="owner:" + ownerUsername, item_type="Feature Service", max_items=maxItemNumber) +
                gis.content.search(query="owner:" + ownerUsername, item_type="Vector Tile Service", max_items=maxItemNumber) +
                gis.content.search(query="owner:" + ownerUsername, item_type="Image Service", max_items=maxItemNumber) +
                gis.content.search(query="owner:" + ownerUsername, item_type="Feature Layer", max_items=maxItemNumber))

    print(f'Searching webmaps in {portal_url}')

    # creates list of items of all webmaps in active portal
    web_maps = gis.content.search(query="", item_type="Web Map", max_items = 10000)
    # loops through list of webmap items
    for item in web_maps:
        # creates a WebMap object from input webmap item
        print(item.title)
        web_map = WebMap(item)
        # accesses layers in WebMap object
        layers = web_map.layers
        # loops through layers
        for layer in layers:
            # tests whether the layer has a styleUrl(VTS) or url (everything else)
             if hasattr(layer, 'styleUrl'):
                 for service in services:
                    if service.url in layer.styleUrl:
                        services.remove(service)
             elif hasattr(layer, 'url'):
                 for service in services:
                    if service.url in layer.url:
                        services.remove(service)
    print(f'The following services are not used in any webmaps in {portal_url}')
    # as we have removed all services being used in active portal, print list of remaining unused services
    for service in services:
        print("{} | {}".format(service.title ,portal_url + r'/home/item.html?id=' + service.id))
        unusedList.append([service.title, portal_url + r'/home/item.html?id=' + service.id])
    print("There are a total of {} unused services in your portal".format(str(len(services))))
    
    df = pd.DataFrame(unusedList)

    df.columns = ["Name", "AGOL Link"]

    df.to_csv(saveLocation, index = False)

main()
