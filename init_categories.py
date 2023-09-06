import os

if not os.path.exists('items.json5'):
    open('items.json5', 'x').write("""{
    'Classic Burger': {
        'direct': {
            'hanoi': [   // the name of the first store
                'HH-0189',  // entered when sold in-store or takeout.
                'HH-0216'   // entered when sold on GrabFood
            ],
            'saigon': [  // the name of the second store
                'HH-0099',  // entered when sold in-store or takeout.
                'HH-0147'   // entered when sold on GrabFood
            ]
        },
        'featured_in': {  // setup combo relationships
            'hanoi': [
                'HH-0178',  // combo lunch burger on GrabFood features 1 classic burger w/ other stuff,
                'HH-0263',  // Grab | Combo 2: Classic Burger + Mini Fries + Coca
            ],
            'saigon': []
        }
    }
}""")
    print('Generated items.json5')
else:
    print('items.json5 already exists.')


if not os.path.exists('categories.json5'):
    open('categories.json5', 'x').write("""{
    'Burgers': ['Classic Burger', "Chick'un Burger", "Pulled Shroom Burger", "Possible Burger", "Black Magic Burger"]
}""")
    print('Generated categories.json5')
else:
    print('categories.json5 already exists.')


