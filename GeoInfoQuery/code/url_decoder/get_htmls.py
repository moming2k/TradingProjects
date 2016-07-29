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
    cid_list = ["9207955936104980714"]

    index = 6
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
    s = list('[[[2698.507191764814,-122.3228416,47.44105039999999],[0,0,0],[1024,768],13.10000038146973],"/maps-lite/js/2/ml_20160719_1",107,"!1b0!3s!7s!10b0!11b0!13b0!14smap,common!17b0!18b1!19b0!22s1!23s2!24s!25s!26b1!27b0",null,["en",""],["/maps/lite/ApplicationService.GetEntityDetails","/maps/lite/ApplicationService.UpdateStarring","/maps/lite/ApplicationService.Search",null,"/maps/lite/suggest","/maps/lite/directions","/maps/lite/MapsLiteService.GetHotelAvailability",null,"https://www.google.com/maps/api/js/reviews?key=AIzaSyCNWEtGyeVduDK_k5UOq8iBk-qP8G4TJL0\u0026language=en","/maps/lite/reviews","/maps/timeline/_rpc/mas","/maps/timeline/_rpc/pc","//maps.gstatic.com","//www.gstatic.com"],[[[2,"spotlight",null,null,null,null,null,[[null,null,null,null,null,null,null,null,null,null,null,[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,1]],["0x0:0x7fc93b2356fca0ea","",null,[null,null,47.44105039999999,-122.3228416],0],null,null,null,null,null,null,null,null,10,null,[null,null,null,null,null,null,null,null,null,null,null,null,null,1],null,null,null,null,null,[14]]]],[[52,[["entity_class","0"]]]]],[["0x54905b4d2e72c295:0x7fc93b2356fca0ea","Occupational Skills Center, 18010 8th Ave S, Burien, WA 98148",[47.44105039999999,-122.3228416],"9207955936104980714"],"Occupational Skills Center",["18010 8th Ave S","Burien, WA 98148"],null,"4 reviews","http://www.google.com/search?q=Occupational+Skills+Center,+18010+8th+Ave+S,+Burien,+WA+98148\u0026ludocid=9207955936104980714#lrd=0x54905b4d2e72c295:0x7fc93b2356fca0ea,1",null,"+1 206-631-7300",null,null,null,["/url?q=http://www.pugetsoundsc.org/\u0026sa=U\u0026ved=0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ61gICCgEMAA\u0026usg=AFQjCNHcLVQRMdhjLFtSCSRRcdKLC-cHSg","pugetsoundsc.org",null,"0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ61gICCgEMAA"],"Technical School","18010 8th Ave S, Burien, WA 98148",null,null,null,null,null,["http://www.google.com/search?q=Occupational+Skills+Center,+18010+8th+Ave+S,+Burien,+WA+98148\u0026ludocid=9207955936104980714#lrd=0x54905b4d2e72c295:0x7fc93b2356fca0ea,1","4 reviews",null,null,1,null,[[["/url?q=https://www.google.com/maps/contrib/100814299535949426328/reviews\u0026sa=U\u0026ved=0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4h4IDigAMAA\u0026usg=AFQjCNGGhh8F3RTJumedl6y2c1r-ONDsLw","J Gutierrez","//lh5.googleusercontent.com/-pDkYNs_SWsM/AAAAAAAAAAI/AAAAAAAAAA8/hlXNm3-wnUk/photo.jpg","0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4h4IDigAMAA"],"a month ago",null,"Love this school!!!! The people are awesome and very genuine!!! Keep it Real Class of 2015!!!!!",5,"http://maps.google.com/?q=Puget+Sound+Skills+Center+loc:+18010+8th+Ave+S,+Burien,+WA+98148\u0026gl=US\u0026sll=47.44105,-122.322841","100814299535949426328",["https://www.google.com/support/contact/bin/request.py?entity=%7B%22author%22:%22AIe9_BE_-CToNTHJp0bHZZnBB-FdaftGalOn4LtYNrVZu7Z7q9VKf-f75prowvPCIndRTnR6Bvp5%22,%22groups%22:%5B%22maps%22%5D,%22id%22:%22http://maps.google.com/?q%3DPuget%2BSound%2BSkills%2BCenter%2Bloc:%2B18010%2B8th%2BAve%2BS,%2BBurien,%2BWA%2B98148%26gl%3DUS%26sll%3D47.44105,-122.322841%22%7D\u0026client=13\u0026contact-type=anno","Flag as inappropriate",null,"0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQoykIDygBMAA"],null,null,"AIe9_BFmECx2BnMcFI6fy6g2iEPEwjmQuWYyqrIBo9RnRfa8F62c70Dc22-UxUhptSMu7oqYEVkI57jpj2txwrLQ0Ek46wwzeVdtRURnASq_J2sCo2xYGEv4zrRxIs8qIdgcc9tXvWVxV8hyFPb77M0RBZX1rd4T0ljjFP6xiS8JhgyKzck5y1aEJetS8RxVBTlg3CT0R5wnhUXytx4_0g2tX4sQNskwFJIWqEtaTaLkFqLdmNwt8impwcejnN0yBuycrbdSgouS","0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4R4IDSgAMAA"],[["/url?q=https://www.google.com/maps/contrib/107425097449434949477/reviews\u0026sa=U\u0026ved=0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4h4IESgAMAA\u0026usg=AFQjCNHsitXsc6iDRc-cQWp8as3wXCkfYg","Skyy uchiha","//lh5.googleusercontent.com/-WgQpVcmfCTQ/AAAAAAAAAAI/AAAAAAAALsg/vHS5QBDG41E/photo.jpg","0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4h4IESgAMAA"],"6 months ago",null,"I went here for two years and I to this day go back and visit I love this school!!!!!!! :) ",5,"http://maps.google.com/?q=Puget+Sound+Skills+Center+loc:+18010+8th+Ave+S,+Burien,+WA+98148\u0026gl=US\u0026sll=47.44105,-122.322841","107425097449434949477",["https://www.google.com/support/contact/bin/request.py?entity=%7B%22author%22:%22AIe9_BGJcTmQOebM6NbazRkEiMmvMBK0930waPisAl2p3UHmbwyw7oQVc_edcNPESZJV3ydl-IC6%22,%22groups%22:%5B%22maps%22%5D,%22id%22:%22http://maps.google.com/?q%3DPuget%2BSound%2BSkills%2BCenter%2Bloc:%2B18010%2B8th%2BAve%2BS,%2BBurien,%2BWA%2B98148%26gl%3DUS%26sll%3D47.44105,-122.322841%22%7D\u0026client=13\u0026contact-type=anno","Flag as inappropriate",null,"0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQoykIEigBMAA"],null,null,"AIe9_BHLxzKAtdTMgw4EwM8CJF1WD7wziTQHblw589AZixDtskfl0yLV0b_7Il92iAqGsoRNl4aS7gRvDL3Z0pDetkIm2mgTWq894-pHzGsic5f4rU6zmBctXtLfNFJRxNHmfLxzzvP8Cbk1IXo32c2z_b5OO98pFVWl9qBnlK606st1ZX4ag_ww-TWJD80eRe_9h_4ewapvi5QU3GCxy3P5hrvnADN9AxAqVjhMYtRydJuPa5LBmixHLBpsbxuNwsqoEuNTWFmj","0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4R4IECgBMAA"],[["/url?q=https://www.google.com/maps/contrib/100599958755981767173/reviews\u0026sa=U\u0026ved=0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4h4IFCgAMAA\u0026usg=AFQjCNHdbrO3SFMmgi5uIU2zQ9JX1fecCA","jaden coleman","//lh4.googleusercontent.com/-KJUqZjcJ6Z8/AAAAAAAAAAI/AAAAAAAAATw/t6Va0KT6wmg/photo.jpg","0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4h4IFCgAMAA"],"6 months ago",null,"Great school",5,"http://maps.google.com/?q=Puget+Sound+Skills+Center+loc:+18010+8th+Ave+S,+Burien,+WA+98148\u0026gl=US\u0026sll=47.44105,-122.322841","100599958755981767173",["https://www.google.com/support/contact/bin/request.py?entity=%7B%22author%22:%22AIe9_BEwek_R4BFH34Gwx9F-bUC904puea9v-Vhn9ptMS4z1JdWayI2dlR0fjvu-i0gboOYKKGiM%22,%22groups%22:%5B%22maps%22%5D,%22id%22:%22http://maps.google.com/?q%3DPuget%2BSound%2BSkills%2BCenter%2Bloc:%2B18010%2B8th%2BAve%2BS,%2BBurien,%2BWA%2B98148%26gl%3DUS%26sll%3D47.44105,-122.322841%22%7D\u0026client=13\u0026contact-type=anno","Flag as inappropriate",null,"0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQoykIFSgBMAA"],null,null,"AIe9_BGr8ws4rxcebphqBfEm4i_Rki9t1votbX9PntQjSZri4wNCpbi2kOIqa2lb39fxx0fmY4TiTpnfd3JMxnL6Yz222Zn311mQ84PvTw56YzaFt5V_x1ROqemlGliY9UpX9WlPy3xwglkfea09pnZRYTg0KA5ihQt4SePjERremNI5ksowcNPalNq7csLJe4xLgCPNz67iVcKc4djsl0_EUwr6kJCZsh6bmnzgx0cH596ASI5n3EPh4dz7A_PGfmwa4UYNSA8X","0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4R4IEygCMAA"],[["/url?q=https://www.google.com/maps/contrib/108842668045173528663/reviews\u0026sa=U\u0026ved=0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4h4IFygAMAA\u0026usg=AFQjCNHnFfoKhV28M44cqvcA7Ga_vciLuA","benjamin padrow-silva","https://lh6.googleusercontent.com/-W2x66uScG8A/AAAAAAAAAAI/AAAAAAAAAAA/rTvI1uQtpd8/s40-c-k-mo/photo.jpg","0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4h4IFygAMAA"],"9 months ago",null,null,4,"http://maps.google.com/?q=Puget+Sound+Skills+Center+loc:+18010+8th+Ave+S,+Burien,+WA+98148\u0026gl=US\u0026sll=47.44105,-122.322841","108842668045173528663",["https://www.google.com/support/contact/bin/request.py?entity=%7B%22author%22:%22AIe9_BEG_jpn34IqhsUClWrxA3u1WPKnQnTYLPufsfYavZYP7GnnaKx9MSWDB77Pzfv0oJxAec9d%22,%22groups%22:%5B%22maps%22%5D,%22id%22:%22http://maps.google.com/?q%3DPuget%2BSound%2BSkills%2BCenter%2Bloc:%2B18010%2B8th%2BAve%2BS,%2BBurien,%2BWA%2B98148%26gl%3DUS%26sll%3D47.44105,-122.322841%22%7D\u0026client=13\u0026contact-type=anno","Flag as inappropriate",null,"0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQoykIGCgBMAA"],null,null,"AIe9_BGLn6wJL96ul5PXRSu0mdL7NtLDbeBIuQfHtgx3UZvbOJ7SeLt3B8HM5vdlhLk0MOqWey8uNgzU8uqBZnS22pM7WNH7xjKmNX2xB1Pii4J1itY_SCr8Lmi-K2VH-qKXf_7dpOqSaYNKss2S0K_Q2sthHpT1ZPTg02qkoS9j_DQ-2iEvuFc30D8flxdRxtYkFF6BH9Vk6hmczunDfLpiQRxKtwpgZON1Ghw0WNja1SWcfmyMUleqLasfvB-vd3fM6Ui5Kihp","0ahUKEwig7Zaf9ZPOAhUFE5QKHXSpBWoQ4R4IFigDMAA"]],1],null,null,null,1,null,null,null,"ChIJlcJyLk1bkFQR6qD8ViM7yX8"],null,null,null,null,null,null,null,"/maps/api/js?client=google-maps-lite\u0026paint_origin=\u0026libraries=common,geometry,map,search\u0026v=3.25.8\u0026language=en\u0026region=\u0026callback=v3loaded","/maps-lite/js/2/ml_20160719_1/main.js",0,"Python-urllib/2.7,gzip(gfe),gzip(gfe)",null,null,0,0,null,"https://www.google.com/maps/place//data=!4m2!3m1!1s0x0:0x7fc93b2356fca0ea?dg=dbrw\u0026newdg=1",0,null,0,null,null,"Ys2YV-TnApKK0gShtYGIBw",null,null,["dbrw",1],null,null,null,1,0,null,null,null,null,null,null,"Ys2YV6C0BIWm0AT00pbQBg",null,null,null,null,"//consent.google.com","2.ml_20160719_1",null,null,1]')
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
    print b[-16]