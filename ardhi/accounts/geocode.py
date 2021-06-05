# import geoip
# import geoip2.database as gdb
# import os
#
# from django.contrib.gis import geoip2
#
# def walk(geoip):
#     for name in os.listdir(geoip):
#         path = os.path.join(geoip, name)
#         if os.path.isfile(path):
#             print(path)
#         else:
#             walk(path)
#
# with gdb.Reader(os.path.join(geoip, 'GeoLite2-City/GeoLite2-City.mmdb')) as reader:
#     response = reader.enterprise('128.101.101.101')
#
#     print()
#
#
#
