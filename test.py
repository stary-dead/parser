def convert_to_european_size(info):
    us_women_to_eu = {
        "5.5": "35.5",
        "6": "36",
        "6.5": "37",
        "7": "37.5",
        "7.5": "38.5",
        "8": "39",
        "8.5": "40",
        "9": "40.5",
        "9.5": "41",
        "10": "42",
        "10.5": "42.5",
        "11": "43.5",
        "11.5": "44",
        "12": "44.5",
        "12.5": "45",
        "13": "45.5",
        "13.5": "46",
        "14": "47",
        "14.5": "47.5",
        "15": "48",
        "15.5": "49",
        "16": "49.5",
        "16.5": "50"
    }

    us_men_to_eu = {
        "4": "35.5",
        "4.5": "36",
        "5": "37",
        "5.5": "37.5",
        "6": "38",
        "6.5": "39",
        "7": "39.5",
        "7.5": "40",
        "8": "41",
        "8.5": "41.5",
        "9": "42",
        "9.5": "43",
        "10": "43.5",
        "10.5": "44",
        "11": "45",
        "11.5": "45.5",
        "12": "46",
        "12.5": "46.5",
        "13": "47",
        "13.5": "47.5",
        "14": "48",
        "14.5": "48.5",
        "15": "49",
        "15.5": "49.5"
    }

    uk_to_eu = {
        "3.5": "36",
        "4": "36.5",
        "4.5": "37.5",
        "5": "38",
        "5.5": "38.5",
        "6": "39",
        "6.5": "40",
        "7": "40.5",
        "7.5": "41",
        "8": "42",
        "8.5": "42.5",
        "9": "43",
        "9.5": "44",
        "10": "44.5",
        "10.5": "45",
        "11": "45.5",
        "11.5": "46",
        "12": "46.5",
        "12.5": "47",
        "13": "47.5",
        "14": "48",
        "14.5": "48.5"
    }

    has_price = False
    for item in info:
        size = item["size"]
        price = item["price"]
        if(price !="$--") and (price!=None) and (price!=""):
            has_price = True
        else:
            item["price"] = ""
        if size.startswith("US W"):
            us_size = size.split()[2]
            if us_size in us_women_to_eu:
                item["size"] =  us_women_to_eu[us_size]
        elif size.startswith("US M"):
            us_size = size.split()[2]
            if us_size in us_men_to_eu:
                item["size"] = us_men_to_eu[us_size]
        elif size.startswith("UK"):
            uk_size = size.split()[1]
            if uk_size in uk_to_eu:
                item["size"] = uk_to_eu[uk_size]
    
    return info, has_price

print(convert_to_european_size([
        {
            "size": "US M 4",
            "price": "$--"
        },
        {
            "size": "US M 4.5",
            "price": "$143"
        },
        {
            "size": "US M 5",
            "price": "$--"
        },
        {
            "size": "US M 5.5",
            "price": "$--"
        },
        {
            "size": "US M 6",
            "price": "$--"
        },
        {
            "size": "US M 6.5",
            "price": "$--"
        },
        {
            "size": "US M 7",
            "price": "$--"
        },
        {
            "size": "US M 7.5",
            "price": "$--"
        },
        {
            "size": "US M 8",
            "price": "$--"
        },
        {
            "size": "US M 8.5",
            "price": "$--"
        },
        {
            "size": "US M 9",
            "price": "$--"
        },
        {
            "size": "US M 9.5",
            "price": "$--"
        },
        {
            "size": "US M 10",
            "price": "$--"
        },
        {
            "size": "US M 10.5",
            "price": "$--"
        },
        {
            "size": "US M 11",
            "price": "$--"
        },
        {
            "size": "US M 11.5",
            "price": "$--"
        },
        {
            "size": "US M 12",
            "price": "$--"
        },
        {
            "size": "US M 12.5",
            "price": "$--"
        },
        {
            "size": "US M 13",
            "price": "$--"
        },
        {
            "size": "US M 14",
            "price": "$--"
        }
    ]))