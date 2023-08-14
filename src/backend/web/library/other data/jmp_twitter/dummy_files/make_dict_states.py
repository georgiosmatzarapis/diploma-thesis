import json


states = ['ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'de', 'fl', 'ga', 'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la',
          'ma', 'md', 'me', 'mi', 'mn', 'mo', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 'ny', 'oh', 'ok',
          'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy']

dictStates = [{'AK': 'AK'}, {'Alaska': 'AK'},  {'AL': 'AL'}, {'Alabama': 'AL'}, {'AR': 'AR'}, {'Arkansas': 'AR'},
              {'AZ': 'AZ'}, {'Arizona': 'AZ'}, {'CA': 'CA'}, {'California': 'CA'}, {'CO': 'CO'}, {'Colorado': 'CO'},
              {'CT': 'CT'}, {'Connecticut': 'CT'}, {'DE': 'DE'}, {'Delaware': 'DE'}, {'FL': 'FL'}, {'Florida': 'FL'},
              {'GA': 'GA'}, {'Georgia': 'GA'}, {'HI': 'HI'},
              {'Hawaii': 'HI'}, {'IA': 'IA'}, {'Iowa': 'IA'}, {'ID': 'ID'}, {'Idaho': 'ID'}, {'IL': 'IL'},
              {'Illinois': 'IL'}, {'IN': 'IN'}, {'Indiana': 'IN'}, {'KS': 'KS'}, {'Kansas': 'KS'}, {'KY': 'KY'},
              {'Kentucky': 'KY'}, {'LA': 'LA'}, {'Louisiana': 'LA'}, {'MA': 'MA'}, {'Massachusetts': 'MA'},
              {'MD': 'MD'}, {'Maryland': 'MD'}, {'DC': 'MD'}, {'Washington, DC': 'MD'}, {'ME': 'ME'}, {'Maine': 'ME'},
              {'MI': 'MI'}, {'Michigan': 'MI'},
              {'MN': 'MN'}, {'Minnesota': 'MN'}, {'MO': 'MO'}, {'Missouri': 'MO'}, {'MS': 'MS'}, {'Mississippi': 'MS'},
              {'MT': 'MT'}, {'Montana': 'MT'}, {'NC': 'NC'}, {'North Carolina': 'MT'}, {'ND': 'ND'},
              {'North Dakota': 'ND'}, {'NE': 'NE'}, {'Nebraska': 'NE'}, {'NH': 'NH'}, {'New Hampshire': 'NH'},
              {'NJ': 'NJ'}, {'New Jersey': 'NJ'}, {'NM': 'NM'}, {'New Mexico': 'NM'}, {'NV': 'NV'},
              {'Nevada': 'NV'}, {'NY': 'NY'}, {'New York': 'NY'}, {'OH': 'OH'}, {'Ohio': 'OH'}, {'OK': 'OK'},
              {'Oklahoma': 'OK'}, {'OR': 'OR'}, {'Oregon': 'OR'}, {'PA': 'PA'}, {'Pennsylvania': 'PA'}, {'RI': 'RI'},
              {'Rhode Island': 'RI'}, {'SC': 'SC'}, {'South Carolina': 'SC'}, {'SD': 'SD'}, {'South Dakota': 'SD'},
              {'TN': 'TN'}, {'Tennessee': 'TN'}, {'TX': 'TX'}, {'Texas': 'TX'}, {'UT': 'UT'}, {'Utah': 'UT'},
              {'VA': 'VA'}, {'Virginia': 'VA'}, {'VT': 'VT'}, {'Vermont': 'VT'}, {'WA': 'WA'}, {'Washington': 'WA'},
              {'WI': 'WI'}, {'Wisconsin': 'WI'}, {'WV': 'WV'}, {'West Virginia': 'WV'}, {'WY': 'WY'}, {'Wyoming': 'WY'}]


dictStates2 = [{'AK': ['AK', 'Alaska']},
{'AL': ['AL', 'Alabama']},
{'AR': ['AR', 'Arkansas']},
{'AZ': ['AZ', 'Arizona']},
{'CA': ['CA', 'California']},
{'CO': ['CO', 'Colorado']},
{'CT': ['CT', 'Connecticut']},
{'DE': ['DE', 'Delaware']},
{'FL': ['FL', 'Florida']},
{'GA': ['GA', 'Georgia']},
{'HI': ['HI', 'Hawaii']},
{'IA': ['IA', 'Iowa']},
{'ID': ['ID', 'Idaho']},
{'IL': ['IL', 'Illinois']},
{'IN': ['IN', 'Indiana']},
{'KS': ['KS', 'Kansas']},
{'KY': ['KY', 'Kentucky']},
{'LA': ['LA', 'Louisiana']},
{'MA': ['MA', 'Massachusetts']},
{'MD': ['MD', 'Maryland', 'DC', 'Washington, DC', 'Washington, D.C.']},
{'ME': ['ME', 'Maine']},
{'MI': ['MI', 'Michigan']},
{'MN': ['MN', 'Minnesota']},
{'MO': ['MO', 'Missouri']},
{'MS': ['MS', 'Mississippi']},
{'MT': ['MT', 'Montana']},
{'NC': ['NC', 'North Carolina']},
{'ND': ['ND', 'North Dakota']},
{'NE': ['NE', 'Nebraska']},
{'NH': ['NH', 'New Hampshire']},
{'NJ': ['NJ', 'New Jersey']},
{'NM': ['NM', 'New Mexico']},
{'NV': ['NV', 'Nevada']},
{'NY': ['NY', 'New York']},
{'OH': ['OH', 'Ohio']},
{'OK': ['OK', 'Oklahoma']},
{'OR': ['OR', 'Oregon']},
{'PA': ['PA', 'Pennsylvania']},
{'RI': ['RI', 'Rhode Island']},
{'SC': ['SC', 'South Carolina']},
{'SD': ['SD', 'South Dakota']},
{'TN': ['TN', 'Tennessee']},
{'TX': ['TX', 'Texas']},
{'UT': ['UT', 'Utah']},
{'VA': ['VA', 'Virginia']},
{'VT': ['VT', 'Vermont']},
{'WA': ['WA', 'Washington']},
{'WI': ['WI', 'Wisconsin']},
{'WV': ['WV', 'West Virginia']},
{'WY': ['WY', 'Wyoming']}
               ]

# print(len(states))
#
print(len(dictStates2))

for x in dictStates2:
    print(x.values())

with open('states1.json', 'w') as file:
    json.dump(dictStates2, file, indent=4)

print('File written successfully!')

