self.addEventListener('message', function (e) {
    if (e.data.cmd == 'start') {
        options = e.data.options;
        parseData(e.data.data);
    } else if (e.data.cmd == 'startRefresh') {
        options = e.data.options;
        refreshData(e.data.data, e.data.prevData, e.data.vars);
    }
}, false);

var mapping = {};
var duplicateMonMap = {};
var options;

mapping.allSubStatsMin = {
    "SPD": { "g5": 15, "g6": 20 },
    "ATK%": { "g5": 20, "g6": 25 },
    "ATK flat": { "g5": 40, "g6": 50 },
    "HP%": { "g5": 20, "g6": 25 },
    "HP flat": { "g5": 450, "g6": 675 },
    "DEF%": { "g5": 20, "g6": 25 },
    "DEF flat": { "g5": 40, "g6": 50 },
    "CRate": { "g5": 15, "g6": 20 },
    "CDmg": { "g5": 15, "g6": 20 },
    "RES": { "g5": 15, "g6": 20 },
    "ACC": { "g5": 15, "g6": 20 }
};

mapping.allSubStatsMax = {
    "SPD": { "g1": 5, "g2": 10, "g3": 15, "g4": 20, "g5": 25, "g6": 30 },
    "ATK%": { "g1": 10, "g2": 15, "g3": 25, "g4": 30, "g5": 35, "g6": 40 },
    "ATK flat": { "g1": 20, "g2": 25, "g3": 40, "g4": 50, "g5": 75, "g6": 100 },
    "HP%": { "g1": 10, "g2": 15, "g3": 25, "g4": 30, "g5": 35, "g6": 40 },
    "HP flat": { "g1": 300, "g2": 525, "g3": 825, "g4": 1125, "g5": 1500, "g6": 1875 },
    "DEF%": { "g1": 10, "g2": 15, "g3": 25, "g4": 30, "g5": 35, "g6": 40 },
    "DEF flat": { "g1": 20, "g2": 25, "g3": 40, "g4": 50, "g5": 75, "g6": 100 },
    "CRate": { "g1": 5, "g2": 10, "g3": 15, "g4": 20, "g5": 25, "g6": 30 },
    "CDmg": { "g1": 10, "g2": 15, "g3": 20, "g4": 25, "g5": 25, "g6": 35 },
    "RES": { "g1": 10, "g2": 15, "g3": 20, "g4": 25, "g5": 35, "g6": 40 },
    "ACC": { "g1": 10, "g2": 15, "g3": 20, "g4": 25, "g5": 35, "g6": 40 }
};

mapping.monster_attribute = {
    1: "Water",
    2: "Fire",
    3: "Wind",
    4: "Light",
    5: "Dark"
};

mapping.effect_types = {
    0: '',
    1: 'HP flat',
    2: 'HP%',
    3: 'ATK flat',
    4: 'ATK%',
    5: 'DEF flat',
    6: 'DEF%',
    8: 'SPD',
    9: 'CRate',
    10: 'CDmg',
    11: 'RES',
    12: 'ACC'
};

mapping.rune_sets = {
    1: "Energy",
    2: "Guard",
    3: "Swift",
    4: "Blade",
    5: "Rage",
    6: "Focus",
    7: "Endure",
    8: "Fatal",
    10: "Despair",
    11: "Vampire",
    13: "Violent",
    14: "Nemesis",
    15: "Will",
    16: "Shield",
    17: "Revenge",
    18: "Destroy",
    19: "Fight",
    20: "Determination",
    21: "Enhance",
    22: "Accuracy",
    23: "Tolerance",
    99: "Immemorial"
};

mapping.rune_quality = {
    1: "Common",
    2: "Magic",
    3: "Rare",
    4: "Hero",
    5: "Legend"
};

mapping.levelToUpgrades = {
    0: { 0: 'Common', 1: 'Magic', 2: 'Rare', 3: 'Hero', 4: 'Legend' },
    3: { 1: 'Common', 2: 'Magic', 3: 'Rare', 4: 'Hero', 5: 'Legend' },
    6: { 2: 'Common', 3: 'Magic', 4: 'Rare', 5: 'Hero', 6: 'Legend' },
    9: { 2: 'Common', 4: 'Magic', 5: 'Rare', 6: 'Hero', 7: 'Legend' },
    12: { 3: 'Common', 5: 'Magic', 6: 'Rare', 7: 'Hero', 8: 'Legend' }
};

mapping.monster_names = {
    "101": "Fairy",
    "10111": "Elucia",
    "10112": "Iselia",
    "10113": "Aeilene",
    "10114": "Neal",
    "10115": "Sorin",

    "102": "Imp",
    "10211": "Fynn",
    "10212": "Cogma",
    "10213": "Ralph",
    "10214": "Taru",
    "10215": "Garok",

    "103": "Pixie",
    "10311": "Kacey",
    "10312": "Tatu",
    "10313": "Shannon",
    "10314": "Cheryl",
    "10315": "Camaryn",

    "104": "Yeti",
    "10411": "Kunda",
    "10412": "Tantra",
    "10413": "Rakaja",
    "10414": "Arkajan",
    "10415": "Kumae",

    "105": "Harpy",
    "10511": "Ramira",
    "10512": "Lucasha",
    "10513": "Prilea",
    "10514": "Kabilla",
    "10515": "Hellea",

    "106": "Hellhound",
    "10611": "Tarq",
    "10612": "Sieq",
    "10613": "Gamir",
    "10614": "Shamar",
    "10615": "Shumar",

    "107": "Warbear",
    "10711": "Dagora",
    "10712": "Ursha",
    "10713": "Ramagos",
    "10714": "Lusha",
    "10715": "Gorgo",

    "108": "Elemental",
    "10811": "Daharenos",
    "10812": "Bremis",
    "10813": "Taharus",
    "10814": "Priz",
    "10815": "Camules",

    "109": "Garuda",
    "10911": "Konamiya",
    "10912": "Cahule",
    "10913": "Lindermen",
    "10914": "Teon",
    "10915": "Rizak",

    "110": "Inugami",
    "11011": "Icaru",
    "11012": "Raoq",
    "11013": "Ramahan",
    "11014": "Belladeon",
    "11015": "Kro",

    "111": "Salamander",
    "11111": "Kaimann",
    "11112": "Krakdon",
    "11113": "Lukan",
    "11114": "Sharman",
    "11115": "Decamaron",

    "112": "Nine-tailed Fox",
    "11211": "Soha",
    "11212": "Shihwa",
    "11213": "Arang",
    "11214": "Chamie",
    "11215": "Kamiya",

    "113": "Serpent",
    "11311": "Shailoq",
    "11312": "Fao",
    "11313": "Ermeda",
    "11314": "Elpuria",
    "11315": "Mantura",

    "114": "Golem",
    "11411": "Kuhn",
    "11412": "Kugo",
    "11413": "Ragion",
    "11414": "Groggo",
    "11415": "Maggi",

    "115": "Griffon",
    "11511": "Kahn",
    "11512": "Spectra",
    "11513": "Bernard",
    "11514": "Shamann",
    "11515": "Varus",

    "116": "Undine",
    "11611": "Mikene",
    "11612": "Atenai",
    "11613": "Delphoi",
    "11614": "Icasha",
    "11615": "Tilasha",

    "117": "Inferno",
    "11711": "Purian",
    "11712": "Tagaros",
    "11713": "Anduril",
    "11714": "Eludain",
    "11715": "Drogan",

    "118": "Sylph",
    "11811": "Tyron",
    "11812": "Baretta",
    "11813": "Shimitae",
    "11814": "Eredas",
    "11815": "Aschubel",

    "119": "Sylphid",
    "11911": "Lumirecia",
    "11912": "Fria",
    "11913": "Acasis",
    "11914": "Mihael",
    "11915": "Icares",

    "120": "High Elemental",
    "12011": "Ellena",
    "12012": "Kahli",
    "12013": "Moria",
    "12014": "Shren",
    "12015": "Jumaline",

    "121": "Harpu",
    "12111": "Sisroo",
    "12112": "Colleen",
    "12113": "Seal",
    "12114": "Sia",
    "12115": "Seren",

    "122": "Slime",
    "12211": "",
    "12212": "",
    "12213": "",
    "12214": "",
    "12215": "",

    "123": "Forest Keeper",
    "12311": "",
    "12312": "",
    "12313": "",
    "12314": "",
    "12315": "",

    "124": "Mushroom",
    "12411": "",
    "12412": "",
    "12413": "",
    "12414": "",
    "12415": "",

    "125": "Maned Boar",
    "12511": "",
    "12512": "",
    "12513": "",
    "12514": "",
    "12515": "",

    "126": "Monster Flower",
    "12611": "",
    "12612": "",
    "12613": "",
    "12614": "",
    "12615": "",

    "127": "Ghost",
    "12711": "",
    "12712": "",
    "12713": "",
    "12714": "",
    "12715": "",

    "128": "Low Elemental",
    "12811": "Tigresse",
    "12812": "Lamor",
    "12813": "Samour",
    "12814": "Varis",
    "12815": "Havana",

    "129": "Mimick",
    "12911": "",
    "12912": "",
    "12913": "",
    "12914": "",
    "12915": "",

    "130": "Horned Frog",
    "13011": "",
    "13012": "",
    "13013": "",
    "13014": "",
    "13015": "",

    "131": "Sandman",
    "13111": "",
    "13112": "",
    "13113": "",
    "13114": "",
    "13115": "",

    "132": "Howl",
    "13211": "Lulu",
    "13212": "Lala",
    "13213": "Chichi",
    "13214": "Shushu",
    "13215": "Chacha",

    "133": "Succubus",
    "13311": "Izaria",
    "13312": "Akia",
    "13313": "Selena",
    "13314": "Aria",
    "13315": "Isael",

    "134": "Joker",
    "13411": "Sian",
    "13412": "Jojo",
    "13413": "Lushen",
    "13414": "Figaro",
    "13415": "Liebli",

    "135": "Ninja",
    "13511": "Susano",
    "13512": "Garo",
    "13513": "Orochi",
    "13514": "Gin",
    "13515": "Han",

    "136": "Surprise Box",
    "13611": "",
    "13612": "",
    "13613": "",
    "13614": "",
    "13615": "",

    "137": "Bearman",
    "13711": "Gruda",
    "13712": "Kungen",
    "13713": "Dagorr",
    "13714": "Ahman",
    "13715": "Haken",

    "138": "Valkyrja",
    "13811": "Camilla",
    "13812": "Vanessa",
    "13813": "Katarina",
    "13814": "Akroma",
    "13815": "Trinity",

    "139": "Pierret",
    "13911": "Julie",
    "13912": "Clara",
    "13913": "Sophia",
    "13914": "Eva",
    "13915": "Luna",

    "140": "Werewolf",
    "14011": "Vigor",
    "14012": "Garoche",
    "14013": "Shakan",
    "14014": "Eshir",
    "14015": "Jultan",

    "141": "Phantom Thief",
    "14111": "Luer",
    "14112": "Jean",
    "14113": "Julien",
    "14114": "Louis",
    "14115": "Guillaume",

    "142": "Angelmon",
    "14211": "Blue Angelmon",
    "14212": "Red Angelmon",
    "14213": "Gold Angelmon",
    "14214": "White Angelmon",
    "14215": "Dark Angelmon",

    "144": "Dragon",
    "14411": "Verad",
    "14412": "Zaiross",
    "14413": "Jamire",
    "14414": "Zerath",
    "14415": "Grogen",

    "145": "Phoenix",
    "14511": "Sigmarus",
    "14512": "Perna",
    "14513": "Teshar",
    "14514": "Eludia",
    "14515": "Jaara",

    "146": "Chimera",
    "14611": "Taor",
    "14612": "Rakan",
    "14613": "Lagmaron",
    "14614": "Shan",
    "14615": "Zeratu",

    "147": "Vampire",
    "14711": "Liesel",
    "14712": "Verdehile",
    "14713": "Argen",
    "14714": "Julianne",
    "14715": "Cadiz",

    "148": "Viking",
    "14811": "Huga",
    "14812": "Geoffrey",
    "14813": "Walter",
    "14814": "Jansson",
    "14815": "Janssen",

    "149": "Amazon",
    "14911": "Ellin",
    "14912": "Ceres",
    "14913": "Hina",
    "14914": "Lyn",
    "14915": "Mara",

    "150": "Martial Cat",
    "15011": "Mina",
    "15012": "Mei",
    "15013": "Naomi",
    "15014": "Xiao Ling",
    "15015": "Miho",

    "152": "Vagabond",
    "15211": "Allen",
    "15212": "Kai'en",
    "15213": "Roid",
    "15214": "Darion",
    "15215": "Jubelle",

    "153": "Epikion Priest",
    "15311": "Rina",
    "15312": "Chloe",
    "15313": "Michelle",
    "15314": "Iona",
    "15315": "Rasheed",

    "154": "Magical Archer",
    "15411": "Sharron",
    "15412": "Cassandra",
    "15413": "Ardella",
    "15414": "Chris",
    "15415": "Bethony",

    "155": "Rakshasa",
    "15511": "Su",
    "15512": "Hwa",
    "15513": "Yen",
    "15514": "Pang",
    "15515": "Ran",

    "156": "Bounty Hunter",
    "15611": "Wayne",
    "15612": "Randy",
    "15613": "Roger",
    "15614": "Walkers",
    "15615": "Jamie",

    "157": "Oracle",
    "15711": "Praha",
    "15712": "Juno",
    "15713": "Seara",
    "15714": "Laima",
    "15715": "Giana",

    "158": "Imp Champion",
    "15811": "Yaku",
    "15812": "Fairo",
    "15813": "Pigma",
    "15814": "Shaffron",
    "15815": "Loque",

    "159": "Mystic Witch",
    "15911": "Megan",
    "15912": "Rebecca",
    "15913": "Silia",
    "15914": "Linda",
    "15915": "Gina",

    "160": "Grim Reaper",
    "16011": "Hemos",
    "16012": "Sath",
    "16013": "Hiva",
    "16014": "Prom",
    "16015": "Thrain",

    "161": "Occult Girl",
    "16111": "Anavel",
    "16112": "Rica",
    "16113": "Charlotte",
    "16114": "Lora",
    "16115": "Nicki",

    "162": "Death Knight",
    "16211": "Fedora",
    "16212": "Arnold",
    "16213": "Briand",
    "16214": "Conrad",
    "16215": "Dias",

    "163": "Lich",
    "16311": "Rigel",
    "16312": "Antares",
    "16313": "Fuco",
    "16314": "Halphas",
    "16315": "Grego",

    "164": "Skull Soldier",
    "16411": "",
    "16412": "",
    "16413": "",
    "16414": "",
    "16415": "",

    "165": "Living Armor",
    "16511": "Nickel",
    "16512": "Iron",
    "16513": "Copper",
    "16514": "Silver",
    "16515": "Zinc",

    "166": "Dragon Knight",
    "16611": "Chow",
    "16612": "Laika",
    "16613": "Leo",
    "16614": "Jager",
    "16615": "Ragdoll",

    "167": "Magical Archer Promo",
    "16711": "",
    "16712": "",
    "16713": "",
    "16714": "Fami",
    "16715": "",

    "168": "Monkey King",
    "16811": "Shi Hou",
    "16812": "Mei Hou Wang",
    "16813": "Xing Zhe",
    "16814": "Qitian Dasheng",
    "16815": "Son Zhang Lao",

    "169": "Samurai",
    "16911": "Kaz",
    "16912": "Jun",
    "16913": "Kaito",
    "16914": "Tosi",
    "16915": "Sige",

    "170": "Archangel",
    "17011": "Ariel",
    "17012": "Velajuel",
    "17013": "Eladriel",
    "17014": "Artamiel",
    "17015": "Fermion",

    "172": "Drunken Master",
    "17211": "Mao",
    "17212": "Xiao Chun",
    "17213": "Huan",
    "17214": "Tien Qin",
    "17215": "Wei Shin",

    "173": "Kung Fu Girl",
    "17311": "Xiao Lin",
    "17312": "Hong Hua",
    "17313": "Ling Ling",
    "17314": "Liu Mei",
    "17315": "Fei",

    "174": "Beast Monk",
    "17411": "Chandra",
    "17412": "Kumar",
    "17413": "Ritesh",
    "17414": "Shazam",
    "17415": "Rahul",

    "175": "Mischievous Bat",
    "17511": "",
    "17512": "",
    "17513": "",
    "17514": "",
    "17515": "",

    "176": "Battle Scorpion",
    "17611": "",
    "17612": "",
    "17613": "",
    "17614": "",
    "17615": "",

    "177": "Minotauros",
    "17711": "Urtau",
    "17712": "Burentau",
    "17713": "Eintau",
    "17714": "Grotau",
    "17715": "Kamatau",

    "178": "Lizardman",
    "17811": "Kernodon",
    "17812": "Igmanodon",
    "17813": "Velfinodon",
    "17814": "Glinodon",
    "17815": "Devinodon",

    "179": "Hell Lady",
    "17911": "Beth",
    "17912": "Raki",
    "17913": "Ethna",
    "17914": "Asima",
    "17915": "Craka",

    "180": "Brownie Magician",
    "18011": "Orion",
    "18012": "Draco",
    "18013": "Aquila",
    "18014": "Gemini",
    "18015": "Korona",

    "181": "Kobold Bomber",
    "18111": "Malaka",
    "18112": "Zibrolta",
    "18113": "Taurus",
    "18114": "Dover",
    "18115": "Bering",

    "182": "King Angelmon",
    "18211": "Blue King Angelmon",
    "18212": "Red King Angelmon",
    "18213": "Gold King Angelmon",
    "18214": "White King Angelmon",
    "18215": "Dark King Angelmon",

    "183": "Sky Dancer",
    "18311": "Mihyang",
    "18312": "Hwahee",
    "18313": "Chasun",
    "18314": "Yeonhong",
    "18315": "Wolyung",

    "184": "Taoist",
    "18411": "Gildong",
    "18412": "Gunpyeong",
    "18413": "Woochi",
    "18414": "Hwadam",
    "18415": "Woonhak",

    "185": "Beast Hunter",
    "18511": "Gangchun",
    "18512": "Nangrim",
    "18513": "Suri",
    "18514": "Baekdu",
    "18515": "Hannam",

    "186": "Pioneer",
    "18611": "Woosa",
    "18612": "Chiwu",
    "18613": "Pungbaek",
    "18614": "Nigong",
    "18615": "Woonsa",

    "187": "Penguin Knight",
    "18711": "Toma",
    "18712": "Naki",
    "18713": "Mav",
    "18714": "Dona",
    "18715": "Kuna",

    "188": "Barbaric King",
    "18811": "Aegir",
    "18812": "Surtr",
    "18813": "Hraesvelg",
    "18814": "Mimirr",
    "18815": "Hrungnir",

    "189": "Polar Queen",
    "18911": "Alicia",
    "18912": "Brandia",
    "18913": "Tiana",
    "18914": "Elenoa",
    "18915": "Lydia",

    "190": "Battle Mammoth",
    "19011": "Talc",
    "19012": "Granite",
    "19013": "Olivine",
    "19014": "Marble",
    "19015": "Basalt",

    "191": "Fairy Queen",
    "19111": "",
    "19112": "",
    "19113": "",
    "19114": "Fran",
    "19115": "",

    "192": "Ifrit",
    "19211": "Theomars",
    "19212": "Tesarion",
    "19213": "Akhamamir",
    "19214": "Elsharion",
    "19215": "Veromos",

    "193": "Cow Girl",
    "19311": "Sera",
    "19312": "Anne",
    "19313": "Hannah",
    "19314": "Loren",
    "19315": "Cassie",

    "194": "Pirate Captain",
    "19411": "Galleon",
    "19412": "Carrack",
    "19413": "Barque",
    "19414": "Brig",
    "19415": "Frigate",

    "195": "Charger Shark",
    "19511": "Aqcus",
    "19512": "Ignicus",
    "19513": "Zephicus",
    "19514": "Rumicus",
    "19515": "Calicus",

    "196": "Mermaid",
    "19611": "Tetra",
    "19612": "Platy",
    "19613": "Cichlid",
    "19614": "Molly",
    "19615": "Betta",

    "197": "Sea Emperor",
    "19711": "Poseidon",
    "19712": "Okeanos",
    "19713": "Triton",
    "19714": "Pontos",
    "19715": "Manannan",

    "198": "Magic Knight",
    "19811": "Lapis",
    "19812": "Astar",
    "19813": "Lupinus",
    "19814": "Iris",
    "19815": "Lanett",

    "199": "Assassin",
    "19911": "Stella",
    "19912": "Lexy",
    "19913": "Tanya",
    "19914": "Natalie",
    "19915": "Isabelle",

    "200": "Neostone Fighter",
    "20011": "Ryan",
    "20012": "Trevor",
    "20013": "Logan",
    "20014": "Lucas",
    "20015": "Karl",

    "201": "Neostone Agent",
    "20111": "Emma",
    "20112": "Lisa",
    "20113": "Olivia",
    "20114": "Illiana",
    "20115": "Sylvia",

    "202": "Martial Artist",
    "20211": "Luan",
    "20212": "Sin",
    "20213": "Lo",
    "20214": "Hiro",
    "20215": "Jackie",

    "203": "Mummy",
    "20311": "Nubia",
    "20312": "Sonora",
    "20313": "Namib",
    "20314": "Sahara",
    "20315": "Karakum",

    "204": "Anubis",
    "20411": "Avaris",
    "20412": "Khmun",
    "20413": "Iunu",
    "20414": "Amarna",
    "20415": "Thebae",

    "205": "Desert Queen",
    "20511": "Bastet",
    "20512": "Sekhmet",
    "20513": "Hathor",
    "20514": "Isis",
    "20515": "Nephthys",

    "206": "Horus",
    "20611": "Qebehsenuef",
    "20612": "Duamutef",
    "20613": "Imesety",
    "20614": "Wedjat",
    "20615": "Amduat",

    "207": "Jack-o'-lantern",
    "20711": "Chilling",
    "20712": "Smokey",
    "20713": "Windy",
    "20714": "Misty",
    "20715": "Dusky",

    "208": "Frankenstein",
    "20811": "Tractor",
    "20812": "Bulldozer",
    "20813": "Crane",
    "20814": "Driller",
    "20815": "Crawler",

    "209": "Elven Ranger",
    "20911": "Eluin",
    "20912": "Adrian",
    "20913": "Erwin",
    "20914": "Lucien",
    "20915": "Isillen",

    "210": "Harg",
    "21011": "Remy",
    "21012": "Racuni",
    "21013": "Raviti",
    "21014": "Dova",
    "21015": "Kroa",

    "211": "Fairy King",
    "21111": "Psamathe",
    "21112": "Daphnis",
    "21113": "Ganymede",
    "21114": "Oberon",
    "21115": "Nyx",

    "212": "Panda Warrior",
    "21211": "Mo Long",
    "21212": "Xiong Fei",
    "21213": "Feng Yan",
    "21214": "Tian Lang",
    "21215": "Mi Ying",

    "213": "Dice Magician",
    "21311": "Reno",
    "21312": "Ludo",
    "21313": "Morris",
    "21314": "Tablo",
    "21315": "Monte",

    "214": "Harp Magician",
    "21411": "Sonnet",
    "21412": "Harmonia",
    "21413": "Triana",
    "21414": "Celia",
    "21415": "Vivachel",

    "215": "Unicorn",
    "21511": "Amelia",
    "21512": "Helena",
    "21513": "Diana",
    "21514": "Eleanor",
    "21515": "Alexandra",
    "21611": "Amelia",
    "21612": "Helena",
    "21613": "Diana",
    "21614": "Eleanor",
    "21615": "Alexandra",

    "218": "Paladin",
    "21811": "Josephine",
    "21812": "Ophilia",
    "21813": "Louise",
    "21814": "Jeanne",
    "21815": "Leona",

    "219": "Chakram Dancer",
    "21911": "Talia",
    "21912": "Shaina",
    "21913": "Melissa",
    "21914": "Deva",
    "21915": "Belita",

    "220": "Boomerang Warrior",
    "22011": "Sabrina",
    "22012": "Maruna",
    "22013": "Zenobia",
    "22014": "Bailey",
    "22015": "Martina",

    "15105": "Devilmon",
    "14314": "Rainbowmon",

    "1000111": "Homunculus - Attack (Water)",
    "1000112": "Homunculus - Attack (Fire)",
    "1000113": "Homunculus - Attack (Wind)",

    "1000214": "Homunculus - Support (Light)",
    "1000215": "Homunculus - Support (Dark)"
};

var rune_id = 1;
var monster_id = 1;
var craft_id = 1;

var storage_id = 0;

var structure = {
    runes: [],
    mons: [],
    crafts: [],
    savedBuilds: [],
    buildings: [],
    uniqueToId: { gridRunes: {}, gridMons: {}, gridCrafts: {} },
    wizard_id: 0,
    tvalue: 0
};

function getMonsterName(monster_uid) {
    if (monster_uid) {
        if (mapping.monster_names[monster_uid]) {
            return mapping.monster_names[monster_uid];
        } else {
            var family = Number(monster_uid.toString().substr(0, 3));

            if (mapping.monster_names[family]) {
                var attribute = Number(monster_uid.toString().slice(-1));
                return mapping.monster_names[family] + ' (' + mapping.monster_attribute[attribute] + ')';
            } else {
                return 'Unknown Monster';
            }
            return 'Unknown Monster';
        }
    } else {
        return false;
    }
}

function filterMonster(monster) {
    //filter useless monster
    if (options.filterUselessMons && (monster['unit_master_id'] === 15105 || monster['unit_master_id'] === 14314))
        return true;

    //filter grades
    if (options.filterGradesMons && options.filterGradesMonsInput > 0 && monster['class'] < options.filterGradesMonsInput)
        return true;

    return false;
}

function refreshData(data, prevData, vars) {
    //get storage_id
    for (id in data['building_list']) {
        if (data['building_list'][id]['building_master_id'] === 25) {
            storage_id = data['building_list'][id]['building_id'];
            break;
        }
    }

    // index new data
    var indexNew = { runes: {}, monsters: {}, crafts: {} };
    data.runes.forEach(rune => {
        indexNew.runes[rune.rune_id] = true;
    });

    data.unit_list.forEach(monster => {
        indexNew.monsters[monster.unit_id] = true;

        monster.runes.forEach(rune => {
            indexNew.runes[rune.rune_id] = true;
        });
    });

    data.rune_craft_item_list.forEach(craft => {
        indexNew.crafts[craft.craft_item_id] = true;
    });

    // remove all data without unique ids (self-created) and delete entries and index data for better performance
    var indexes = { runes: {}, monsters: {}, crafts: {} };
    var indexHelper = 0;
    prevData.runes = prevData.runes.filter(rune => {
        if (prevData.uniqueToId.gridRunes[rune[vars.tableMetaData.gridRunes.unique_field]] && indexNew.runes[rune[vars.tableMetaData.gridRunes.unique_field]]) {
            indexes.runes[rune[vars.tableMetaData.gridRunes.unique_field]] = indexHelper;
            indexHelper++;
            return true;
        } else {
            if (prevData.uniqueToId.gridRunes[rune[vars.tableMetaData.gridRunes.unique_field]])
                delete prevData.uniqueToId.gridRunes[rune[vars.tableMetaData.gridRunes.unique_field]];

            return false;
        }
    });

    indexHelper = 0;
    prevData.mons = prevData.mons.filter(monster => {
        if (prevData.uniqueToId.gridMons[monster[vars.tableMetaData.gridMons.unique_field]] && indexNew.monsters[monster[vars.tableMetaData.gridMons.unique_field]]) {
            indexes.monsters[monster[vars.tableMetaData.gridMons.unique_field]] = indexHelper;
            indexHelper++;
            return true;
        } else {
            if (prevData.uniqueToId.gridMons[monster[vars.tableMetaData.gridMons.unique_field]])
                delete prevData.uniqueToId.gridMons[monster[vars.tableMetaData.gridMons.unique_field]];

            return false;
        }
    });

    indexHelper = 0;
    prevData.crafts = prevData.crafts.filter(craft => {
        if (prevData.uniqueToId.gridCrafts[craft[vars.tableMetaData.gridCrafts.unique_field]] && indexNew.crafts[craft[vars.tableMetaData.gridCrafts.unique_field]]) {
            indexes.crafts[craft[vars.tableMetaData.gridCrafts.unique_field]] = indexHelper;
            indexHelper++;
            return true;
        } else {
            if (prevData.uniqueToId.gridCrafts[craft[vars.tableMetaData.gridCrafts.unique_field]])
                delete prevData.uniqueToId.gridCrafts[craft[vars.tableMetaData.gridCrafts.unique_field]];

            return false;
        }
    });

    data.runes.forEach(rune => {
        if (prevData.uniqueToId.gridRunes[rune.rune_id] && prevData.runes[indexes.runes[rune.rune_id]]) {
            // remember properties of this rune
            var locked = prevData.runes[indexes.runes[rune.rune_id]].locked;
            var originName = prevData.runes[indexes.runes[rune.rune_id]].originName;
            prevData.runes[indexes.runes[rune.rune_id]] = mapRune(rune, prevData.uniqueToId.gridRunes[rune.rune_id]);
            prevData.runes[indexes.runes[rune.rune_id]].locked = locked;
            if (!options.refreshData_overrideLocation) {
                prevData.runes[indexes.runes[rune.rune_id]].originName = originName;
            }
        } else {
            // new rune
            vars.nextRuneId++;
            prevData.runes.push(mapRune(rune, vars.nextRuneId));
            prevData.uniqueToId.gridRunes[rune.rune_id] = vars.nextRuneId;
        }
    });

    data.unit_list.forEach(monster => {
        // filter
        var filtered = false;
        if (!monster.runes || monster.runes.length === 0) {
            if (options.filterNorunesMons)
                filtered = true;
            if (filterMonster(monster))
                filtered = true;
        }

        if (!filtered) {
            if (prevData.uniqueToId.gridMons[monster.unit_id] && prevData.mons[indexes.monsters[monster.unit_id]]) {
                var mon = mapMonster(monster, prevData.uniqueToId.gridMons[monster.unit_id]);
                prevData.mons[indexes.monsters[monster.unit_id]] = mon;
            } else {
                // new monster
                vars.nextMonsId++;
                var mon = mapMonster(monster, vars.nextMonsId);
                prevData.mons.push(mon);
                prevData.uniqueToId.gridMons[monster.unit_id] = vars.nextMonsId;
            }

            monster.runes.forEach(rune => {
                if (prevData.uniqueToId.gridRunes[rune.rune_id] && prevData.runes[indexes.runes[rune.rune_id]]) {
                    // remember properties of this rune
                    var locked = prevData.runes[indexes.runes[rune.rune_id]].locked;
                    var originName = prevData.runes[indexes.runes[rune.rune_id]].originName;
                    prevData.runes[indexes.runes[rune.rune_id]] = mapRune(rune, prevData.uniqueToId.gridRunes[rune.rune_id], monster, mon.id);
                    prevData.runes[indexes.runes[rune.rune_id]].locked = locked;
                    if (!options.refreshData_overrideLocation) {
                        prevData.runes[indexes.runes[rune.rune_id]].originName = originName;
                    }
                } else {
                    // new rune
                    vars.nextRuneId++;
                    prevData.runes.push(mapRune(rune, vars.nextRuneId, monster, mon.id));
                    prevData.uniqueToId.gridRunes[rune.rune_id] = vars.nextRuneId;
                }
            });
        }
    });

    data.rune_craft_item_list.forEach(craft => {
        if (prevData.uniqueToId.gridCrafts[craft.craft_item_id] && prevData.crafts[indexes.crafts[craft.craft_item_id]]) {
            prevData.crafts[indexes.crafts[craft.craft_item_id]] = mapCraft(craft, prevData.uniqueToId.gridCrafts[craft.craft_item_id]);
        } else {
            // new craft
            vars.nextCraftId++;
            prevData.crafts.push(mapCraft(craft, vars.nextCraftId));
            prevData.uniqueToId.gridCrafts[craft.craft_item_id] = vars.nextCraftId;
        }
    });

    prevData.buildings = [];
    data.deco_list.forEach(building => {
        var buildingObj = {};
        buildingObj.master_id = building.master_id;
        buildingObj.level = building.level;
        prevData.buildings.push(buildingObj);
    });

    prevData.tvalue = data.tvalue;

    self.postMessage({ cmd: 'done', structure: prevData });
}

function parseData(data) {
    //get storage_id
    for (id in data['building_list']) {
        if (data['building_list'][id]['building_master_id'] === 25) {
            storage_id = data['building_list'][id]['building_id'];
            break;
        }
    }

    //inventory runes
    var inv_runes_length = data['runes'].length;
    for (var i = 0; i < inv_runes_length; i++) {
        structure.uniqueToId.gridRunes[data['runes'][i]['rune_id']] = rune_id;
        structure.runes.push(mapRune(data['runes'][i], rune_id));

        rune_id++;
    }

    //monster and rune on monsters
    var unit_list_length = data['unit_list'].length;
    for (var i = 0; i < unit_list_length; i++) {

        //filter (only monster without runes)
        if (!data['unit_list'][i].runes || data['unit_list'][i].runes.length === 0) {
            if (options.filterNorunesMons)
                continue;
            if (filterMonster(data['unit_list'][i]))
                continue;
        }

        structure.uniqueToId.gridMons[data['unit_list'][i]['unit_id']] = monster_id;
        structure.mons.push(mapMonster(data['unit_list'][i], monster_id));

        //runes equiped on monster
        for (j in data['unit_list'][i].runes) {
            structure.uniqueToId.gridRunes[data['unit_list'][i].runes[j]['rune_id']] = rune_id;
            structure.runes.push(mapRune(data['unit_list'][i].runes[j], rune_id, data['unit_list'][i], monster_id));
            rune_id++;
        }

        monster_id++;
    }

    //crafts
    var crafts_list_length = data['rune_craft_item_list'].length;
    for (var i = 0; i < crafts_list_length; i++) {
        structure.uniqueToId.gridCrafts[data['rune_craft_item_list'][i]['craft_item_id']] = craft_id;
        structure.crafts.push(mapCraft(data['rune_craft_item_list'][i], craft_id));

        craft_id++;
    }

    //buildings
    for (var i = 0; i < data['deco_list'].length; i++) {
        var building = {};
        building.master_id = data['deco_list'][i].master_id;
        building.level = data['deco_list'][i].level;
        structure.buildings.push(building);
    }

    //general
    structure.wizard_id = data['wizard_id'];
    structure.tvalue = data['tvalue'];

    self.postMessage({ cmd: 'done', structure: structure });
}

function mapCraft(craft, craft_id) {
    var map = {};
    var type_str = craft['craft_type_id'].toString();

    map.DT_RowId = 'row_' + craft_id;
    map.id = craft_id;
    map.item_id = craft['craft_item_id'];
    map.type = (craft['craft_type'] == 1 || craft['craft_type'] == 3) ? 'E' : 'G';
    map.set = mapping.rune_sets[Number(type_str.slice(0, -4))];
    map.stat = mapping.effect_types[Number(type_str.slice(-4, -2))];
    map.grade = Number(type_str.slice(-1));

    return map;
}

function mapMonster(monster, monster_id) {
    var map = {};

    map.DT_RowId = 'row_' + monster_id;
    map.id = monster_id;

    var storage_string = '';
    if (monster['building_id'] === storage_id)
        storage_string = (options.shortenStorage) ? ' *' : ' (In Storage)';

    var duplicate_string = '';
    if (monster['unit_master_id']) {
        if (duplicateMonMap[monster['unit_master_id']]) {
            duplicateMonMap[monster['unit_master_id']]++;
            duplicate_string = (duplicateMonMap[monster['unit_master_id']] > 1) ? ' ' + duplicateMonMap[monster['unit_master_id']] : '';
        } else {
            duplicateMonMap[monster['unit_master_id']] = 1;
        }
    }

    var monsterName = getMonsterName(monster['unit_master_id']);
    if (monster.homunculus) {
        var name = monsterName.split(' ');
        map.name = name[0] + ' - ' + monster.homunculus_name + duplicate_string + storage_string;
    } else {
        map.name = monsterName + duplicate_string + storage_string;
    }

    map.level = monster['unit_level'];
    map.unit_id = monster['unit_id'];
    map.master_id = monster['unit_master_id'];
    map.stars = monster['class'];
    map.attribute = mapping.monster_attribute[monster['attribute']];
    map.location = (storage_string == '') ? 'inventory' : 'storage';
    map.b_hp = monster['con'] * 15;
    map.b_atk = monster['atk'];
    map.b_def = monster['def'];
    map.b_spd = monster['spd'];
    map.b_crate = monster['critical_rate'];
    map.b_cdmg = monster['critical_damage'];
    map.b_res = monster['resist'];
    map.b_acc = monster['accuracy'];

    return map;
}

function getRuneQuality(rune) {
    if (rune.grade < 3)
        return 'Unknown';

    var legend = false;
    var upgrades = 0;
    for (var i = 1; i < 5; i++) {
        if (rune['s' + i + '_t'] === '')
            break;

        var maxIncrement = (mapping.allSubStatsMax[rune['s' + i + '_t']]['g' + rune.grade] / 5);
        var realValue = (rune['s' + i + '_data'].gvalue) ? (rune['s' + i + '_v'] - rune['s' + i + '_data'].gvalue - maxIncrement) : rune['s' + i + '_v'] - maxIncrement;
        var temp = 0;
        while (temp < realValue) {
            temp += maxIncrement;
            upgrades++;
        }
        if (i === 4 && realValue > maxIncrement)
            legend = true;
    }

    return (upgrades >= 4 || legend) ? 'Legend' : 'Unknown';
}

function mapRune(rune, rune_id, monster, monster_id) {
    var map = {};
    var monster = monster || {};

    var subs = {
        'ATK flat': '-',
        'ATK%': '-',
        'HP flat': '-',
        'HP%': '-',
        'DEF flat': '-',
        'DEF%': '-',
        'RES': '-',
        'ACC': '-',
        'SPD': '-',
        'CDmg': '-',
        'CRate': '-',
    };

    for (var i = 0; i < 4; i++) {
        if (rune.sec_eff[i]) {
            map['s' + (i + 1) + '_t'] = mapping.effect_types[rune.sec_eff[i][0]];
            map['s' + (i + 1) + '_v'] = (rune.sec_eff[i][1] + rune.sec_eff[i][3]);

            map['s' + (i + 1) + '_data'] = {
                enchanted: (rune.sec_eff[i][2] == 1),
                gvalue: rune.sec_eff[i][3]
            };

            subs[mapping.effect_types[rune.sec_eff[i][0]]] = (subs[mapping.effect_types[rune.sec_eff[i][0]]] > 0) ? (subs[mapping.effect_types[rune.sec_eff[i][0]]] + rune.sec_eff[i][1] + rune.sec_eff[i][3]) : (rune.sec_eff[i][1] + rune.sec_eff[i][3]);

        } else {
            map['s' + (i + 1) + '_t'] = "";
            map['s' + (i + 1) + '_v'] = 0;
            map['s' + (i + 1) + '_data'] = {};
        }
    }

    map.DT_RowId = 'row_' + rune_id;
    map.id = rune_id;
    map.unique_id = rune['rune_id'];
    map.monster = monster_id || 0;
    map.originID = monster_id || 0;

    var storage_string = '';
    if (monster['building_id'] === storage_id)
        storage_string = (options.shortenStorage) ? ' *' : ' (In Storage)';

    var duplicate_string = '';
    if (monster['unit_master_id']) {
        if (duplicateMonMap[monster['unit_master_id']]) {
            duplicate_string = (duplicateMonMap[monster['unit_master_id']] > 1) ? ' ' + duplicateMonMap[monster['unit_master_id']] : '';
        }
    }

    var monsterName = getMonsterName(monster['unit_master_id']) ? getMonsterName(monster['unit_master_id']) : "Inventory";
    if (monster.homunculus && monsterName !== 'Inventory') {
        var name = monsterName.split(' ');
        map.monster_n = name[0] + ' - ' + monster.homunculus_name + duplicate_string + storage_string;
        map.originName = name[0] + ' - ' + monster.homunculus_name + duplicate_string + storage_string;
    } else {
        map.monster_n = monsterName + duplicate_string + storage_string;
        map.originName = monsterName + duplicate_string + storage_string;
    }

    map.efficiency = 0;
    map.set = mapping.rune_sets[rune['set_id']] || rune['set_id'];
    map.slot = rune['slot_no'];
    map.grade = rune['class'];
    map.level = rune['upgrade_curr'];
    map.m_t = mapping.effect_types[rune['pri_eff'][0]];
    map.m_v = rune['pri_eff'][1];
    map.i_t = mapping.effect_types[rune['prefix_eff'][0]];
    map.i_v = rune['prefix_eff'][1];
    map.locked = 0;
    map.sub_res = subs['RES'];
    map.sub_cdmg = subs['CDmg'];
    map.sub_atkf = subs['ATK flat'];
    map.sub_acc = subs['ACC'];
    map.sub_atkp = subs['ATK%'];
    map.sub_defp = subs['DEF%'];
    map.sub_deff = subs['DEF flat'];
    map.sub_hpp = subs['HP%'];
    map.sub_hpf = subs['HP flat'];
    map.sub_spd = subs['SPD'];
    map.sub_crate = subs['CRate'];

    var quality = rune['extra'];
    map.quality = quality == 0 ? getRuneQuality(map) : mapping.rune_quality[quality];

    return map;
}