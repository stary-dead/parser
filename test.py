def find_eu_value(table, target_size):
    eu_index = table[0].index("EU")   
    for row in table[1:]:
        if row[0] == target_size:
            return row[eu_index]  
    return None

array = [
[
            "US",
            "EU",
            "UK",
            "CHN"
        ],
        [
            "4",
            "35.5",
            "/",
            "215"
        ],
        [
            "4.5",
            "36",
            "3.5",
            "220"
        ],
        [
            "5",
            "37",
            "4",
            "225"
        ],
        [
            "5.5",
            "37.5",
            "4.5",
            "230"
        ],
        [
            "6",
            "38",
            "5",
            "235"
        ],
        [
            "6.5",
            "39",
            "5.5",
            "240"
        ],
        [
            "7",
            "39.5",
            "6",
            "245"
        ],
        [
            "7.5",
            "40",
            "6.5",
            "250"
        ],
        [
            "8",
            "41",
            "7",
            "255"
        ],
        [
            "8.5",
            "41.5",
            "7.5",
            "260"
        ],
        [
            "9",
            "42",
            "8",
            "265"
        ],
        [
            "9.5",
            "43",
            "8.5",
            "270"
        ],
        [
            "10",
            "43.5",
            "9",
            "275"
        ],
        [
            "10.5",
            "44",
            "9.5",
            "280"
        ],
        [
            "11",
            "45",
            "10",
            "285"
        ],
        [
            "11.5",
            "45.5",
            "10.5",
            "290"
        ],
        [
            "12",
            "46",
            "11",
            "295"
        ],
        [
            "12.5",
            "47",
            "11.5",
            "300"
        ],
        [
            "13",
            "47.5",
            "12",
            "305"
        ],
]

target_size = "11.5"

result = find_eu_value(array, target_size)
print("Значение из столбца EU:", result)
