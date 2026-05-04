import requests


#api_address=" https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=58e9339d63c845cdaa37e34f911e9cd8 "
api_address=" https://newsapi.org/v2/top-headlines?country=in&apiKey=1dc02f081103421e99fd810fa6b6da3a "


json_data = requests.get(api_address).json()

ar=[]
def news():
    num_articles = len(json_data["articles"])
    for i in range(min(num_articles, 3)):  # Limit loop to the number of articles
        ar.append("Number " + str(i + 1) + " , " + json_data["articles"][i]["title"] + ".")
    return ar

#def news():
#    for i in range(3):
#        ar.append("Number " + str(i+1) +" , "+ json_data["articles"][i]["title"]+".")
#        
#        return ar
