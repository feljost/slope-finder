ski_resorts = [
    # Major International Resorts
    {
        "id": "zermatt",
        "name": "Zermatt",
        "location": {"lat": 46.0207, "lng": 7.7491},
        "elevation": "1620m - 3883m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/zermatt-breuil-cervinia-valtournenche-matterhorn/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Zermatt_summerski.jpg"
    },
    {
        "id": "st-moritz",
        "name": "St. Moritz - Corviglia",
        "location": {"lat": 46.48356, "lng": 9.832565},
        "elevation": "1772m - 3057m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/st-moritz-corviglia/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Corviglia_Skigebiet.jpg"
    },
    {
        "id": "st-moritz-corvatsch", # ID corrected to be unique
        "name": "St. Moritz - Corvatsch",
        "location": {"lat": 46.4436, "lng": 9.8053}, # Coordinates adjusted for Corvatsch base
        "elevation": "1797m - 3303m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/corvatsch-furtschellas/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Corvatsch_Bergstation.jpg"
    },
    {
        "id": "verbier",
        "name": "Verbier (4 Vallées)",
        "location": {"lat": 46.0961, "lng": 7.2286},
        "elevation": "1350m - 3330m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/4-vallees-verbier-la-tzoumaz-nendaz-veysonnaz-thyon/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Ski_slope_Verbier_Valais_027.JPG"
    },
    {
        "id": "parsenn",
        "name": "Davos Parsenn",
        "location": {"lat": 46.808398133928996, "lng": 9.838391279762277},
        "snowreport_url": "https://www.skiresort.info/ski-resort/parsenn-davos-klosters/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Davos-Parsenn-01.jpg"
    },
    {
        "id": "grindelwald",
        "name": "Grindelwald-Wengen",
        "location": {"lat": 46.598319, "lng": 7.908181},
        "elevation": "1034m - 2970m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/kleine-scheidegg-maennlichen-grindelwald-wengen/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Grindelwaldgletscher.jpg"
    },
    {
        "id": "laax",
        "name": "Laax",
        "location": {"lat": 46.820113, "lng": 9.263288},
        "elevation": "1100m - 3018m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/laax-flims-falera/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Laax,_Switzerland_(Unsplash_fkFf2iwq5O0).jpg"
    },
    {
        "id": "saas-fee",
        "name": "Saas-Fee",
        "location": {"lat": 46.11118294192689, "lng": 7.932982627802498},
        "elevation": "1800m - 3573m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/saas-fee/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Saas-Fee_Dorf_Winter.jpg"
    },
    {
        "id": "engelberg",
        "name": "Engelberg-Titlis",
        "location": {"lat": 46.816200, "lng": 8.396476},
        "elevation": "1003m - 3020m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/engelberg-titlis/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Titlis_Cliff_Walk.jpg"
    },
    {
        "id": "arosa",
        "name": "Arosa",
        "location": {"lat": 46.78324, "lng": 9.67886},
        "elevation": "1229m - 2865m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/arosa-lenzerheide/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Arosa2007_12_15_001.JPG"
    },
    {
        "id": "lenzerheide",
        "name": "Lenzerheide",
        "location": {"lat": 46.740294, "lng": 9.556845},
        "elevation": "1229m - 2865m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/arosa-lenzerheide/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Gondola_lift_system_-Lenzerheide,_Graubunden,_Switzerland-19Dec2009-2cr.jpg"
    },
    {
        "id": "crans-montana",
        "name": "Crans-Montana",
        "location": {"lat": 46.3117, "lng": 7.4764},
        "elevation": "1510m - 2927m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/crans-montana/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Crans-Montana_vu_du_ciel.jpg"
    },
    {
        "id": "adelboden",
        "name": "Adelboden-Lenk",
        "location": {"lat": 46.4913, "lng": 7.5583},
        "elevation": "1068m - 2362m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/adelboden-lenk/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Skiweltcup_Slalom_in_Adelboden.jpg"
    },
    {
        "id": "andermatt",
        "name": "Andermatt-Sedrun",
        "location": {"lat": 46.6350, "lng": 8.5946},
        "elevation": "1444m - 2961m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/andermatt-oberalp-sedrun/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/00_0339_Ski-Gebiet_Gurschen_%E2%80%93_Gemsstock_-_Andermatt.jpg"
    },
    {
        "id": "gstaad",
        "name": "Gstaad",
        "location": {"lat": 46.4740, "lng": 7.2866},
        "elevation": "1000m - 3000m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/egglila-videmanette-gstaadsaanenrougemont/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Gstaad-01.jpg"
    },
    {
        "id": "jungfrau",
        "name": "Mürren-Schilthorn",
        "location": {"lat": 46.5594, "lng": 7.8927},
        "elevation": "796m - 2970m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/schilthorn-muerrenlauterbrunnen/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Mürren_im_Winter.jpg"
    },
    {
        "id": "samnaun",
        "name": "Samnaun/Ischgl",
        "location": {"lat": 46.9416, "lng": 10.3605},
        "elevation": "1400m - 2872m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/ischglsamnaun-silvretta-arena/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Ischgl_Idalp.jpg"
    },
    {
        "id": "villars",
        "name": "Villars-Gryon",
        "location": {"lat": 46.2996, "lng": 7.0569},
        "elevation": "1300m - 2200m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/villarsgryonles-diablerets/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Ski_Lift_Villars.jpg"
    },
    {
        "id": "scuol",
        "name": "Scuol",
        "location": {"lat": 46.7967, "lng": 10.2988},
        "elevation": "1250m - 2785m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/scuol-motta-naluns/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Scuol_Motta_Naluns.jpg"
    },
    {
        "id": "flims",
        "name": "Flims",
        "location": {"lat": 46.8361, "lng": 9.2847},
        "elevation": "1100m - 3018m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/laax-flims-falera/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Caumasee.jpg"
    },
    {
        "id": "leukerbad",
        "name": "Leukerbad",
        "location": {"lat": 46.3833, "lng": 7.6333},
        "elevation": "1411m - 2610m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/leukerbad/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Leukerbad_view_2.jpg"
    },
    {
        "id": "flumserberg",
        "name": "Flumserberg",
        "location": {"lat": 47.0906, "lng": 9.2828},
        "elevation": "1220m - 2222m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/flumserberg/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Skiing_lesson_at_Flumserberg.jpg"
    },
    # Portes du Soleil
    {
        "id": "champery",
        "name": "Champéry (Portes du Soleil)",
        "location": {"lat": 46.1748, "lng": 6.8703},
        "elevation": "1050m - 2277m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/les-portes-du-soleil-morzineavoriazles-getschatelmorginschampery/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Champery_Village.jpg"
    },
    {
        "id": "morgins",
        "name": "Morgins (Portes du Soleil)",
        "location": {"lat": 46.2366, "lng": 6.8525},
        "elevation": "1350m - 2000m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/les-portes-du-soleil-morzineavoriazles-getschatelmorginschampery/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Morgins.jpg"
    },
    # 4 Vallées (Specific Sectors)
    {
        "id": "nendaz",
        "name": "Nendaz (4 Vallées)",
        "location": {"lat": 46.1837, "lng": 7.2931},
        "elevation": "1400m - 3330m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/4-vallees-verbier-la-tzoumaz-nendaz-veysonnaz-thyon/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Haute-Nendaz_Village_2011.jpg"
    },
    {
        "id": "veysonnaz",
        "name": "Veysonnaz (4 Vallées)",
        "location": {"lat": 46.2078, "lng": 7.3372},
        "elevation": "1350m - 2450m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/4-vallees-verbier-la-tzoumaz-nendaz-veysonnaz-thyon/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Piste_de_l'Ours.jpg"
    },
    {
        "id": "thyon",
        "name": "Thyon (4 Vallées)",
        "location": {"lat": 46.1961, "lng": 7.3828},
        "elevation": "1500m - 2450m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/4-vallees-verbier-la-tzoumaz-nendaz-veysonnaz-thyon/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Thyon_2000.jpg"
    },
    # Valais - Anniviers
    {
        "id": "grimentz-zinal",
        "name": "Grimentz-Zinal",
        "location": {"lat": 46.1764, "lng": 7.5706},
        "elevation": "1570m - 2900m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/grimentz-zinal/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Grimentz_Village.jpg"
    },
    {
        "id": "st-luc-chandolin",
        "name": "St-Luc / Chandolin",
        "location": {"lat": 46.2192, "lng": 7.6042},
        "elevation": "1650m - 3000m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/saint-lucchandolin-anniviers/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/St-Luc.jpg"
    },
    # Valais - Aletsch & Others
    {
        "id": "aletsch-arena",
        "name": "Aletsch Arena",
        "location": {"lat": 46.3908, "lng": 8.0433},
        "elevation": "1845m - 2869m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/aletsch-arena-riederalp-bettmeralp-fiesch-eggishorn/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Aletschgletscher_mit_Konkordiaplatz.jpg"
    },
    {
        "id": "belalp",
        "name": "Belalp",
        "location": {"lat": 46.3575, "lng": 7.9458},
        "elevation": "1322m - 3112m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/belalp-blatten/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Belalp.jpg"
    },
    {
        "id": "lauchernalp",
        "name": "Lauchernalp (Lötschental)",
        "location": {"lat": 46.4025, "lng": 7.7719},
        "elevation": "1968m - 3111m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/lauchernalp-loetschental/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Lauchernalp_im_Winter.jpg"
    },
    {
        "id": "saas-grund",
        "name": "Saas-Grund",
        "location": {"lat": 46.1219, "lng": 7.9406},
        "elevation": "1559m - 3200m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/hohsaas-saas-grund/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Saas-Grund_Kreuzboden.jpg"
    },
    {
        "id": "anzere",
        "name": "Anzère",
        "location": {"lat": 46.2961, "lng": 7.3969},
        "elevation": "1500m - 2500m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/anzere/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Anzere_Village.jpg"
    },
    {
        "id": "ovronnaz",
        "name": "Ovronnaz",
        "location": {"lat": 46.2131, "lng": 7.1714},
        "elevation": "1350m - 2427m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/ovronnaz/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Ovronnaz.jpg"
    },
    # Vaud & Bern
    {
        "id": "glacier-3000",
        "name": "Glacier 3000",
        "location": {"lat": 46.3333, "lng": 7.2167},
        "elevation": "1350m - 3000m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/glacier-3000/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Glacier3000.jpg"
    },
    {
        "id": "leysin",
        "name": "Leysin - Les Mosses",
        "location": {"lat": 46.3428, "lng": 7.0117},
        "elevation": "1250m - 2331m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/leysin-les-mosses/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Leysin_village.jpg"
    },
    {
        "id": "meiringen-hasliberg",
        "name": "Meiringen-Hasliberg",
        "location": {"lat": 46.7333, "lng": 8.1833},
        "elevation": "1055m - 2433m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/meiringen-hasliberg/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Hasliberg_Reuti.jpg"
    },
    {
        "id": "lenk",
        "name": "Lenk",
        "location": {"lat": 46.4550, "lng": 7.4431},
        "elevation": "1068m - 2362m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/adelboden-lenk/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Lenk_im_Simmental.jpg"
    },
    # Central Switzerland
    {
        "id": "stoos",
        "name": "Stoos",
        "location": {"lat": 46.9744, "lng": 8.6508},
        "elevation": "1305m - 1935m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/stoos-fronalpstockklingenstock/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Stoos_Fronalpstock.jpg"
    },
    {
        "id": "hoch-ybrig",
        "name": "Hoch-Ybrig",
        "location": {"lat": 47.0167, "lng": 8.8167},
        "elevation": "1050m - 1831m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/hoch-ybrig-unteribergoberiberg/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Hoch-Ybrig_Spirstock.jpg"
    },
    {
        "id": "melchsee-frutt",
        "name": "Melchsee-Frutt",
        "location": {"lat": 46.7761, "lng": 8.2711},
        "elevation": "1080m - 2255m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/melchsee-frutt/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Melchsee-Frutt_Dorf.jpg"
    },
    {
        "id": "sorenberg",
        "name": "Sörenberg",
        "location": {"lat": 46.8167, "lng": 8.0333},
        "elevation": "1166m - 2350m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/soerenberg-rothorndorf/snow-report/",
        "image_url": "https://www.soerenberg.ch/fileadmin/_processed_/0/a/csm_skigebiet-eisee-brienzer-rothorn-soerenberg-yorick-leusink-4_f68693f231.jpg"
    },
    # Eastern Switzerland
    {
        "id": "pizol",
        "name": "Pizol",
        "location": {"lat": 47.0086, "lng": 9.4239},
        "elevation": "1047m - 2227m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/pizol-bad-ragaz-wangs/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Pizol_Wangs.jpg"
    },
    {
        "id": "chaeserrugg",
        "name": "Chäserrugg (Toggenburg)",
        "location": {"lat": 47.1681, "lng": 9.2961},
        "elevation": "900m - 2262m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/chaeserrugg-unterwasser-alt-st-johann-toggenburg/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Chaeserrugg.jpg"
    },
    {
        "id": "braunwald",
        "name": "Braunwald",
        "location": {"lat": 46.9406, "lng": 9.0017},
        "elevation": "1256m - 1904m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/braunwald/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Braunwald_Glarus_Sued.jpg"
    },
    {
        "id": "elm",
        "name": "Elm",
        "location": {"lat": 46.9189, "lng": 9.1728},
        "elevation": "1020m - 2105m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/elm-im-sernftal/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Elm_Martinsloch.jpg"
    },
    # Graubünden (Misc)
    {
        "id": "diavolezza",
        "name": "Diavolezza / Lagalb",
        "location": {"lat": 46.4103, "lng": 9.9822},
        "elevation": "2093m - 3066m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/diavolezza-lagalb/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Diavolezza.jpg"
    },
    {
        "id": "obersaxen",
        "name": "Obersaxen Mundaun",
        "location": {"lat": 46.7444, "lng": 9.1217},
        "elevation": "1201m - 2310m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/obersaxen-mundaun-val-lumnezia/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Obersaxen_Mundaun.jpg"
    },
    {
        "id": "brigels",
        "name": "Brigels",
        "location": {"lat": 46.7533, "lng": 9.0622},
        "elevation": "1110m - 2418m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/brigels-waltensburg-andiast/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Brigels.jpg"
    },
    {
        "id": "savognin",
        "name": "Savognin",
        "location": {"lat": 46.5983, "lng": 9.5936},
        "elevation": "1200m - 2713m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/savognin/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Savognin_Julia.jpg"
    },
    {
        "id": "bivio",
        "name": "Bivio",
        "location": {"lat": 46.4678, "lng": 9.6506},
        "elevation": "1769m - 2560m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/bivio/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Bivio_Village.jpg"
    },
    {
        "id": "spluegen",
        "name": "Splügen-Tambo",
        "location": {"lat": 46.5531, "lng": 9.3242},
        "elevation": "1480m - 2215m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/spluegen-tambo/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Spluegen.jpg"
    },
    {
        "id": "tschiertschen",
        "name": "Tschiertschen",
        "location": {"lat": 46.8167, "lng": 9.6000},
        "elevation": "1350m - 2400m",
        "snowreport_url": "https://www.skiresort.info/ski-holiday-in/tschiertschen-praden-2062/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Tschiertschen.jpg"
    },
    # Ticino
    {
        "id": "airolo",
        "name": "Airolo",
        "location": {"lat": 46.5269, "lng": 8.6083},
        "elevation": "1175m - 2250m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/pesciuem-airolo/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Airolo.jpg"
    },
    {
        "id": "bosco-gurin",
        "name": "Bosco Gurin",
        "location": {"lat": 46.3167, "lng": 8.5000},
        "elevation": "1506m - 2400m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/bosco-gurin-grossalp/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Bosco_Gurin_Walser.jpg"
    },
    {
        "id": "nara",
        "name": "Nara",
        "location": {"lat": 46.4667, "lng": 8.9167},
        "elevation": "1400m - 2123m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/nara-leontica/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Leontica_Nara.jpg"
    },
    {
        "id": "cari",
        "name": "Carì",
        "location": {"lat": 46.4883, "lng": 8.8167},
        "elevation": "1650m - 2293m",
        "snowreport_url": "https://www.skiresort.info/ski-resort/cari/snow-report/",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Cari_Leventina.jpg"
    },
]