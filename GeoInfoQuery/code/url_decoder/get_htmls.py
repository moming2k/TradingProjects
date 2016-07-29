#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_htmls
# Author: Mark Wang
# Date: 27/7/2016

import re
import urllib2


def get(cid):
    url = 'https://maps.google.com/?cid={}'.format(cid)
    req = urllib2.urlopen(url)
    return req.read()


def get_html_file():
    cid_list = ["9207955936104980714",
                "16573829435820636979"]

    index = 0
    for cid in cid_list:
        file_name = "file{}.html".format(index)
        html = get(cid)
        with open(file_name, 'w') as f:
            f.write(html)
        index += 1


if __name__ == '__main__':
    # get_html_file()
    html = ""
    with open('file6.html') as f:
        html = f.read()

    result = re.findall(r'cacheResponse\((.*)\)', html)
    # print result[0]

    left_brace = 0
    # s = list(result[0])
    s = list('[[[3595.471367846551,-80.39067620000002,25.6888094],[0,0,0],[1024,768],13.10000038146973],"/maps-lite/js/2/ml_20160726_0",107,"!1b0!3s!7s!10b0!11b0!13b0!14smap,common!17b0!18b1!19b0!22s1!23s2!24s!25s!26b1!27b0",null,["en",""],["/maps/lite/ApplicationService.GetEntityDetails","/maps/lite/ApplicationService.UpdateStarring","/maps/lite/ApplicationService.Search",null,"/maps/lite/suggest","/maps/lite/directions","/maps/lite/MapsLiteService.GetHotelAvailability",null,"https://www.google.com/maps/api/js/reviews?key=AIzaSyCNWEtGyeVduDK_k5UOq8iBk-qP8G4TJL0\u0026language=en","/maps/lite/reviews","/maps/timeline/_rpc/mas","/maps/timeline/_rpc/pc","//maps.gstatic.com","//www.gstatic.com"],[[[2,"spotlight",null,null,null,null,null,[[null,null,null,null,null,null,null,null,null,null,null,[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,1]],["0x0:0xe602120f5a007b33","",null,[null,null,25.6888094,-80.3906762],0],null,null,null,null,null,null,null,null,10,null,[null,null,null,null,null,null,null,null,null,null,null,null,null,1],null,null,null,null,null,[14]]]],[[52,[["entity_class","0"]]]]],[["0x88d9c0e8865aae7b:0xe602120f5a007b33","The Prestige Institute for Aesthetic Surgery \u0026 Med Spa, 8501 SW 124th Ave #102a, Miami, FL 33183",[25.6888094,-80.3906762],"16573829435820636979"],"The Prestige Institute for Aesthetic Surgery \u0026 Med Spa",["8501 SW 124th Ave #102a","Miami, FL 33183"],null,null,null,null,"+1 305-595-2244",null,null,null,["/url?q=http://www.theprestigeinstitute.com/\u0026sa=U\u0026ved=0ahUKEwiZwNSc4JjOAhUIKpQKHbV3Dm0Q61gIBigDMAA\u0026usg=AFQjCNGmsvmNlgrbnCgdSXM9oH7sZ1h4WA","theprestigeinstitute.com",null,"0ahUKEwiZwNSc4JjOAhUIKpQKHbV3Dm0Q61gIBigDMAA"],"Spa","8501 SW 124th Ave #102a, Miami, FL 33183",null,null,null,null,null,[null,null,null,null,1,null,null,1],null,null,null,1,null,null,null,"ChIJe65ahujA2YgRM3sAWg8SAuY",["/url?q=https://locu.com/places/the-prestige-institute-for-aesthetic-surgery-med-spa-miami-us/%23menu\u0026sa=U\u0026ved=0ahUKEwiZwNSc4JjOAhUIKpQKHbV3Dm0QqRkIBygEMAA\u0026usg=AFQjCNGLy7Zez-FUAYZzJ97g9YDWwzG1jg","locu.com",null,"0ahUKEwiZwNSc4JjOAhUIKpQKHbV3Dm0QqRkIBygEMAA"]],null,null,null,null,null,null,null,"/maps/api/js?client=google-maps-lite\u0026paint_origin=\u0026libraries=common,geometry,map,search\u0026v=3.25.9\u0026language=en\u0026region=\u0026callback=v3loaded","/maps-lite/js/2/ml_20160726_0/main.js",0,"Scrapy/1.1.0 (+http://scrapy.org),gzip(gfe),gzip(gfe)",null,null,0,0,null,"https://www.google.com/maps/place//data=!4m2!3m1!1s0x0:0xe602120f5a007b33?dg=dbrw\u0026newdg=1",0,null,0,null,null,"blabV6SxEoOO0gSWoo7QDw",null,null,["dbrw",1],null,null,null,1,0,null,null,null,null,null,null,"blabV5nRFIjU0AS177noBg",null,null,null,null,"//consent.google.com","2.ml_20160726_0",null,null,1]')
    new_s = []
    index = 0
    for c in s[1:-1]:
        if c == '[':
            left_brace += 1
        if c == ']':
            left_brace -= 1

        if left_brace == 0 and c == ',':
            index += 1
        elif index > 9:
            break
        elif index == 9:
            new_s.append(c)

    s = ''.join(new_s)
    print s
    import json
    b = json.loads(s)
    print b
    print b[-16]