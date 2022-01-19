from arcgis.gis import GIS
from arcgis.mapping import WebMap

from getpass import getpass
portal_url = "https://arcgis.com"
username = 'OGMGIS_utahDNR'
password = getpass() # this prompts the user to input a password without echoing, better than hard-coding and storing in the python file
gis = GIS(portal_url, username, password)

unusedList = []

def main():

    print("Logged in as {}".format(gis.properties['user']['username']))

    # creates list of items of all map image, feature, vector tile and image services (up to 10000 of each) in active portal
    services = (gis.content.search(query="owner:" + gis.users.me.username, item_type="Map Service", max_items=10000) +
                gis.content.search(query="owner:" + gis.users.me.username, item_type="Feature Service", max_items=10000) +
                gis.content.search(query="owner:" + gis.users.me.username, item_type="Vector Tile Service", max_items=10000) +
                gis.content.search(query="owner:" + gis.users.me.username, item_type="Image Service", max_items=10000) +
                gis.content.search(query="owner:" + gis.users.me.username, item_type="Feature Layer", max_items=10000))

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

main()

import pandas as pd

df = pd.DataFrame(unusedList)

df.columns = ["Name", "AGOL Link"]

df.to_csv(r"C:\Users\cschooley\Documents\Work\Personal\AGOLOrganization\notinmaps122021.csv", index = False)