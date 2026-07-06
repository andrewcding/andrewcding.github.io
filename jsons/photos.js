// Photo album data — one entry per photo, in display order.
// img: file in imgs/photo/   thumb: file in imgs/photo/thumbnails/
// caption: HTML allowed (<br>)   long: true = smaller caption font (long text)
window.PHOTOS = [
  {
    "img": "IMG_8665.JPEG",
    "caption": "A sand dune under blue skies in the vastness of the Sahara desert.<br><br> Winner of the 2022 Waterloo Exchange Photo Contest",
    "credit": "Erg Chebbi, Morocco · 2022",
    "long": true,
    "thumb": "dune.jpg"
  },
  {
    "img": "IMG_7629.JPEG",
    "caption": "A breathtaking view of Mount Fuji, rising above the tranquil waters of Lake Kawaguchi.",
    "credit": "Lake Kawaguchi, Japan · 2022",
    "long": false,
    "thumb": "fuji.jpg"
  },
  {
    "img": "IMG_3635.JPEG",
    "caption": "A lone fishing boat among the towerering karst formations.",
    "credit": "Ha Long Bay, Vietnam · 2022",
    "long": false,
    "thumb": "boat.jpg"
  },
  {
    "img": "IMG_6581.JPEG",
    "caption": "The bright colourful lights of Spaceship Earth illuminates the night.",
    "credit": "Epcot, United States · 2022",
    "long": false,
    "thumb": "epcot.jpg"
  },
  {
    "img": "IMG_3287.jpg",
    "caption": "A crowd of eager whale watchers witness a thrilling moment as a whale comes into view.",
    "credit": "Off the Coast of Akureyri, Iceland · 2018",
    "long": false,
    "thumb": "whale.jpg"
  },
  {
    "img": "IMG_4198.JPEG",
    "caption": "A vintage coin-operated viewfinder directs attention towards the iconic Empire State Building.",
    "credit": "New York, United States · 2019",
    "long": false,
    "thumb": "empirestate.jpg"
  },
  {
    "img": "IMG_1177.JPEG",
    "caption": "Pink blossoms in focus, set in front of a bridge in a traditional Chinese garden.",
    "credit": "Xi'an, China · 2018",
    "long": false,
    "thumb": "flowers.jpg"
  },
  {
    "img": "IMG_0313.JPEG",
    "caption": "Crystal blue lake nestled in mountains with Mont Blanc in the distance, captured after a rewarding hike.",
    "credit": "Mont Blanc, France · 2022",
    "long": true,
    "thumb": "montblanc.jpg"
  },
  {
    "img": "IMG_0561.JPEG",
    "caption": "Silhouetted figures traverse a lantern-lit tunnel, creating a captivating contrast of light and shadow.",
    "credit": "Xi'an, China · 2018",
    "long": false,
    "thumb": "lanterns.jpg"
  },
  {
    "img": "IMG_0342.JPEG",
    "caption": "A powerful display of Icelandic nature, a view of Skógafoss up close.",
    "credit": "Skógafoss, Iceland · 2018",
    "long": false,
    "thumb": "waterfall.jpg"
  },
  {
    "img": "IMG_0350.JPEG",
    "caption": "Skógafoss towers over a romantic couple standing at its base.",
    "credit": "Skógafoss, Iceland · 2018",
    "long": false,
    "thumb": "waterfall2.jpg"
  },
  {
    "img": "IMG_0165.JPEG",
    "caption": "An idyllic Swiss town overlooking Lac de Joux, captured during a scenic hike.",
    "credit": "Le Pont, Switzerland · 2022",
    "long": false,
    "thumb": "trail.jpg"
  },
  {
    "img": "IMG_0033.JPEG",
    "caption": "A serene view of a distant lighthouse and sailboats over the calm waters of Lake Ontario.",
    "credit": "Mississauga, Canada · 2018",
    "long": false,
    "thumb": "sail.jpg"
  },
  {
    "img": "IMG_0748.JPEG",
    "caption": "A moody and captivating view of mountains and water while off the coast of Akureyri.",
    "credit": "Off the Coast of Akureyri, Iceland · 2018",
    "long": false,
    "thumb": "icelandmountains.jpg"
  },
  {
    "img": "IMG_0768.JPEG",
    "caption": "A scarlet vessel teeming with eager observers pause to admire a surfacing whale.",
    "credit": "Off the Coast of Akureyri, Iceland · 2018",
    "long": false,
    "thumb": "whale2.jpg"
  },
  {
    "img": "IMG_0616.JPEG",
    "caption": "As the sun sets over the horizon, a row of people sit serenely along the waterfront, basking in the tranquility of the moment.",
    "credit": "West Coast Park, Singapore · 2022",
    "long": true,
    "thumb": "westcoast.jpg"
  },
  {
    "img": "IMG_0449.JPEG",
    "caption": "This view showcases Lake Geneva and the French Alps, framed by a cozy table for two adorned with vibrant red flowers. <br><br> Runner Up of the 2022 Where in the world?! Co-op Photo Contest.",
    "credit": "Yvoire, France · 2022",
    "long": true,
    "thumb": "yvoire.jpg"
  },
  {
    "img": "IMG_0392.JPEG",
    "caption": "Château de Sion standing tall amidst the picturesque mountain valley.",
    "credit": "Sion, Switzerland · 2022",
    "long": false,
    "thumb": "sion.jpg"
  },
  {
    "img": "IMG_0692.JPEG",
    "caption": "The CN Tower rising above the misty fog, behind the CBC building.",
    "credit": "Toronto, Canada · 2018",
    "long": false,
    "thumb": "toronto.jpg"
  },
  {
    "img": "IMG_2214.JPEG",
    "caption": "A bridge nestled amidst lush greenery in a tranquil forest.",
    "credit": "Capilano, Canada · 2019",
    "long": false,
    "thumb": "bridge.jpg"
  },
  {
    "img": "IMG_2277.JPEG",
    "caption": "Seaplane touches down amidst mountain backdrop.",
    "credit": "Vancouver, Canada · 2019",
    "long": false,
    "thumb": "plane.jpg"
  },
  {
    "img": "IMG_2309.JPEG",
    "caption": "Crystal clear turquoise waters cascade down in a multi-tiered waterfall, a natural masterpiece in motion.",
    "credit": "Kuang Si, Laos · 2022",
    "long": false,
    "thumb": "kuangsi.jpg"
  },
  {
    "img": "IMG_2397.JPEG",
    "caption": "A vibrant orange jellyfish gliding effortlessly in the water.",
    "credit": "Vancouver, Canada · 2019",
    "long": false,
    "thumb": "jellyfish.jpg"
  },
  {
    "img": "IMG_2441.JPEG",
    "caption": "A view of Vancouver's Stanley Park, framed by soaring towers in the distance and lush forest to the left.",
    "credit": "Vancouver, Canada · 2019",
    "long": false,
    "thumb": "stanley1.jpg"
  },
  {
    "img": "IMG_2444.JPEG",
    "caption": "A view of Stanley Park in Vancouver with the iconic seawall in the foreground.",
    "credit": "Vancouver, Canada · 2019",
    "long": false,
    "thumb": "stanley2.jpg"
  },
  {
    "img": "IMG_2466.JPEG",
    "caption": "A stunning vista of the Vancouver skyline from Stanley Park.",
    "credit": "Vancouver, Canada · 2019",
    "long": false,
    "thumb": "vancouver1.jpg"
  },
  {
    "img": "IMG_3121.JPEG",
    "caption": "A detailed close-up of the intricate statues adorning the façade of Milan's iconic Duomo.",
    "credit": "Milan, Italy · 2019",
    "long": false,
    "thumb": "rome.jpg"
  },
  {
    "img": "IMG_3316.JPEG",
    "caption": "A picturesque view of Bern, featuring the turquoise-green waters of the Aare River and charming medieval buildings lining its banks.",
    "credit": "Bern, Switzerland · 2019",
    "long": true,
    "thumb": "bern.jpg"
  },
  {
    "img": "IMG_3358.JPEG",
    "caption": "A stunning golden hour view of the Swiss countryside, captured along a scenic path flanked by verdant fields and majestic mountains",
    "credit": "Buchholterberg, Switzerland · 2019",
    "long": true,
    "thumb": "goldenhour.jpg"
  },
  {
    "img": "IMG_3449.JPEG",
    "caption": "A view of Swiss train tracks cutting through the majestic Swiss Alps.",
    "credit": "Kleine Scheidegg, Switzerland · 2019",
    "long": false,
    "thumb": "train1.jpg"
  },
  {
    "img": "IMG_3484.JPEG",
    "caption": "A solitary black house stands amidst the expansive Swiss Alps, nestled in a valley and overlooking the breathtaking landscape below.",
    "credit": "Wengen, Switzerland · 2019",
    "long": true,
    "thumb": "mountainhouse.jpg"
  },
  {
    "img": "IMG_3577.JPEG",
    "caption": "A striking red train makes its grand entrance into the breathtaking Swiss Alps.",
    "credit": "Kleine Scheidegg, Switzerland · 2019",
    "long": false,
    "thumb": "train2.jpg"
  },
  {
    "img": "IMG_3704.JPEG",
    "caption": "A cloudy day in Zurich as seen from the terrace of ETH with the cityscape stretching out below.",
    "credit": "Zürich, Switzerland · 2019",
    "long": false,
    "thumb": "zurich.jpg"
  },
  {
    "img": "IMG_7293.JPEG",
    "caption": "A burst of pink flowers takes center stage against the backdrop of a charming yellow house.",
    "credit": "Nice, France · 2022",
    "long": false,
    "thumb": "flower1.jpg"
  },
  {
    "img": "IMG_7360.JPEG",
    "caption": "A pristine view of Calanques de Sugiton, with its azure waters and rugged coastline.",
    "credit": "Marseille, France · 2022",
    "long": false,
    "thumb": "calanques.jpg"
  },
  {
    "img": "IMG_7589.JPEG",
    "caption": "A charming Italian town nestled on the shores of Lake Como.",
    "credit": "Lake Como, Italy · 2022",
    "long": false,
    "thumb": "como.jpg"
  },
  {
    "img": "IMG_7717.JPEG",
    "caption": "From the tranquil waters of Lake Como, Menaggio stands proud with the mountains as its backdrop.",
    "credit": "Menaggio, Italy · 2022",
    "long": false,
    "thumb": "como2.jpg"
  },
  {
    "img": "IMG_8115.JPEG",
    "caption": "A view of Dubrovnik from a rooftop perch, with Mount Srd looming in the distance.",
    "credit": "Dubrovnik, Croatia · 2022",
    "long": false,
    "thumb": "dubrovnik1.jpg"
  },
  {
    "img": "IMG_9924.JPEG",
    "caption": "A view of the Matterhorn rising behind a calm lake, its summit crowned with a halo of clouds.",
    "credit": "Matterhorn, Switzerland · 2022",
    "long": false,
    "thumb": "matterhorn1.jpg"
  },
  {
    "img": "IMG_9945.JPEG",
    "caption": "A peaceful forest scene with the Matterhorn peeking over the treetops in the distance.",
    "credit": "Matterhorn, Switzerland · 2022",
    "long": false,
    "thumb": "matterhorn2.jpg"
  },
  {
    "img": "IMG_7135.JPEG",
    "caption": "Overlooking Lake Geneva and Swiss Riviera from the historic Chateau Chillon.",
    "credit": "Montreux, Switzerland · 2022",
    "long": false,
    "thumb": "montreux.jpg"
  },
  {
    "img": "IMG_9425.JPEG",
    "caption": "Through a natural opening in the rock, witness the awe-inspiring beauty of Bryce Canyon National Park in all its grandeur.",
    "credit": "Bryce Canyon National Park, United States · 2023",
    "long": false,
    "thumb": "holeinwall.jpg"
  },
  {
    "img": "IMG_9002.JPEG",
    "caption": "Amidst the hustle and bustle of the Moroccan souk, vendors display their wares for sale, with a towering minaret in the background.",
    "credit": "Fes, Morocco · 2022",
    "long": true,
    "thumb": "souk.jpg"
  },
  {
    "img": "IMG_1060.JPEG",
    "caption": "The spring bloom graces the path to a Chinese temple.",
    "credit": "Xi'an China · 2022",
    "long": false,
    "thumb": "templ2.jpg"
  },
  {
    "img": "IMG_1307.JPEG",
    "caption": "Xi'an's Bell Tower glows in the darkness, a beacon of the city's rich history.",
    "credit": "Xi'an China · 2022",
    "long": false,
    "thumb": "temple.jpg"
  },
  {
    "img": "IMG_1470.JPEG",
    "caption": "A lone airplane flies through a sea of gray.",
    "credit": "Mississauga, Canada · 2018",
    "long": false,
    "thumb": "plane2.jpg"
  },
  {
    "img": "IMG_1848.JPEG",
    "caption": "A carefully balanced stack of rocks takes center stage against the urban backdrop.",
    "credit": "Vancouver, Canada · 2019",
    "long": false,
    "thumb": "vancouver3.jpg"
  },
  {
    "img": "IMG_9576.JPEG",
    "caption": "A mesmerizing display of light and shadow in the depths of Antelope Canyon.",
    "credit": "Antelope Canyon, United States · 2023",
    "long": false,
    "thumb": "antelopecanyon.jpg"
  },
  {
    "img": "IMG_9965.JPEG",
    "caption": "A road immersed in the captivating landscapes of Valley of Fire State Park.",
    "credit": "Valley of Fire State Park, United States · 2023",
    "long": false,
    "thumb": "valleyoffire.jpg"
  },
  {
    "img": "IMG_3637.JPEG",
    "caption": "A moment of transit: a train stops at a Swiss alpine station amidst stunning mountain scenery.",
    "credit": "Kleine Scheidegg, Switzerland · 2019",
    "long": false,
    "thumb": "train3.jpg"
  },
  {
    "img": "IMG_0825.JPEG",
    "caption": "The vibrant glow of Singapore's Garden by the Bay comes alive at night, illuminating the futuristic supertrees and captivating visitors.",
    "credit": "Singapore · 2022",
    "long": true,
    "thumb": "gardensbythebay.jpg"
  },
  {
    "img": "IMG_3726.JPEG",
    "caption": "A tranquil path towards a charming home.",
    "credit": "Vaduz, Liechtenstein · 2019",
    "long": false,
    "thumb": "vaduz.jpg"
  },
  {
    "img": "IMG_3830.JPEG",
    "caption": "The beauty of Vienna's historic city center, basking in the glow of a setting sun.",
    "credit": "Vienna, Austria · 2019",
    "long": false,
    "thumb": "vienna.jpg"
  },
  {
    "img": "IMG_3888.JPEG",
    "caption": "The dark and moody hues of Humber Bay from high up in the sky.",
    "credit": "Toronto, Canada · 2019",
    "long": false,
    "thumb": "toronto2.jpg"
  },
  {
    "img": "IMG_4317.JPEG",
    "caption": "Looking up at the towering skyscrapers of New York City, featuring One World Trade Center standing tall in the centre.",
    "credit": "New York, United States · 2019",
    "long": true,
    "thumb": "newyork.jpg"
  },
  {
    "img": "IMG_4367.JPEG",
    "caption": "The sun sets over Lady Liberty, casting her silhouette in golden light.",
    "credit": "New York, United States · 2019",
    "long": false,
    "thumb": "liberty.jpg"
  },
  {
    "img": "IMG_4636.JPEG",
    "caption": "Nature's canvas painted in shades of autumn at Columbia Lake.",
    "credit": "Waterloo, Canada · 2019",
    "long": false,
    "thumb": "waterloo.jpg"
  },
  {
    "img": "IMG_6054.JPEG",
    "caption": "The sunny shores of Boracay, where the tranquil ocean meets the rugged coastline.",
    "credit": "Boracay, Philippines · 2022",
    "long": false,
    "thumb": "boracay.jpg"
  },
  {
    "img": "IMG_6953.JPEG",
    "caption": "La Passerelle de l'Utopie extends into Lake Neuchatel, inviting visitors to walk and enjoy the view.",
    "credit": "Neuchâtel, Switzerland · 2022",
    "long": false,
    "thumb": "neuchatel.jpg"
  },
  {
    "img": "IMG_6991.JPEG",
    "caption": "A picturesque view of Swiss wine country, punctuated by the Swiss flag waving strong.",
    "credit": "Lavaux, Switzerland · 2022",
    "long": false,
    "thumb": "lavaux.jpg"
  },
  {
    "img": "IMG_7042.JPEG",
    "caption": "A view of Lake Geneva from above.",
    "credit": "Glion, Switzerland · 2022",
    "long": false,
    "thumb": "lavaux2.jpg"
  },
  {
    "img": "IMG_7189.JPEG",
    "caption": "Reflections of beauty and wonder at Fontaine Miroir d'Eau.",
    "credit": "Nice, France · 2022",
    "long": false,
    "thumb": "nice.jpg"
  },
  {
    "img": "IMG_7261.JPEG",
    "caption": "Capturing the essence of Japan at Kiyomizu-dera Sanjunoto.",
    "credit": "Kyoto, Japan · 2022",
    "long": false,
    "thumb": "kyoto1.jpg"
  },
  {
    "img": "IMG_7652.JPEG",
    "caption": "As the day fades away, the majesty of Mount Fuji takes center stage.",
    "credit": "Fujikawaguchiko, Japan · 2022",
    "long": false,
    "thumb": "fuji2.jpg"
  },
  {
    "img": "IMG_7837.JPEG",
    "caption": "A picturesque vista of Lake Lugano and its surrounding landscape from the vantage point of Monte Bre, the crown jewel of Lugano.",
    "credit": "Lugano, Switzerland · 2022",
    "long": true,
    "thumb": "lugano.jpg"
  },
  {
    "img": "IMG_8167.JPEG",
    "caption": "A moment of tranquility and reflection at Hassan II Mosque captured after a rainstorm.",
    "credit": "Casablanca, Morocco · 2022",
    "long": false,
    "thumb": "casa.jpg"
  },
  {
    "img": "IMG_8171.JPEG",
    "caption": "Peeking through time: a glimpse of Dubrovnik's old town through a weathered window.",
    "credit": "Dubrovnik, Croatia · 2022",
    "long": false,
    "thumb": "porthole.jpg"
  },
  {
    "img": "IMG_8297.JPEG",
    "caption": "Palm trees against blue sky in Marrakesh's medina.",
    "credit": "Marrakesh, Morocco · 2022",
    "long": false,
    "thumb": "palmtree.jpg"
  },
  {
    "img": "IMG_1019.jpeg",
    "caption": "Pacific waves crashing into Mile Rock Beach.",
    "credit": "San Francisco, United States · 2023",
    "long": false,
    "thumb": "sf.jpg"
  },
  {
    "img": "IMG_8345.JPEG",
    "caption": "The red and white of the Croatian flag stands out against the historic architecture of Dubrovnik's old town.",
    "credit": "Dubrovnik, Croatia · 2022",
    "long": true,
    "thumb": "dubrovnik3.jpg"
  },
  {
    "img": "IMG_8533.JPEG",
    "caption": "Nature's respite: a tranquil grove of palm trees amid the stark beauty of Morocco's rocky landscape.",
    "credit": "Tinghir, Morocco · 2022",
    "long": true,
    "thumb": "morocco.jpg"
  },
  {
    "img": "IMG_8818.JPEG",
    "caption": "Amsterdam's charming canals framed by vibrant flowers in full bloom.",
    "credit": "Amsterdam, Netherlands · 2022",
    "long": false,
    "thumb": "amsterdam.jpg"
  },
  {
    "img": "IMG_0171.JPEG",
    "caption": "The historic architecture of a Swiss town is perfectly reflected on the calm waters.",
    "credit": "Vallorbe, Switzerland · 2022",
    "long": false,
    "thumb": "vallorbe.jpg"
  },
  {
    "img": "IMG_0242.JPEG",
    "caption": "Nature's perfection captured in this photo of Mont Blanc, a river, and vibrant greenery.",
    "credit": "Mont Blanc, France · 2022",
    "long": false,
    "thumb": "montblanc2.jpg"
  },
  {
    "img": "IMG_0657.JPEG",
    "caption": "A vibrant night scene in Singapore's Chinatown, with neon lights illuminating the busy streets.",
    "credit": "Chinatown, Singapore · 2022",
    "long": true,
    "thumb": "chinatown.jpg"
  },
  {
    "img": "IMG_9910.JPEG",
    "caption": "Embarking on an unforgettable journey through the dramatic canyons of Zion National Park.",
    "credit": "Zion National Park, United States · 2023",
    "long": true,
    "thumb": "zion.jpg"
  },
  {
    "img": "IMG_9858.JPEG",
    "caption": "Ascend to new heights and conquer the legendary Angels Landing in Zion National Park, where an exhilarating hike rewards you with breathtaking views of the surrounding canyons.",
    "credit": "Zion National Park, United States · 2023",
    "long": true,
    "thumb": "angelslanding.jpg"
  },
  {
    "img": "IMG_3155.JPEG",
    "caption": "A picturesque view of Phi Phi islands' harbor, with boats bobbing in the turquoise waters.",
    "credit": "Phi Phi Islands, Thailand · 2022",
    "long": true,
    "thumb": "phiphi.jpg"
  },
  {
    "img": "IMG_7296.JPEG",
    "caption": "The captivating architecture of Gare de Sud in Nice, France, blending timeless elegance with a touch of Mediterranean charm.",
    "credit": "Nice, France · 2022",
    "long": true,
    "thumb": "gare.jpg"
  },
  {
    "img": "IMG_8161.JPEG",
    "caption": "Amidst the cobblestone streets, the prominent church tower in Dubrovnik's Old Town commands attention with its grandeur.",
    "credit": "Dubrovnik, Croatia · 2022",
    "long": true,
    "thumb": "dubrovnik4.jpg"
  },
  {
    "img": "IMG_8813.JPEG",
    "caption": "Tranquil moments abound along Amsterdam's iconic canals.",
    "credit": "Amsterdam, Netherlands · 2022",
    "long": false,
    "thumb": "amsterdam2.jpg"
  },
  {
    "img": "IMG_9413.JPEG",
    "caption": "The emerald-hued mountains of the Alps rise magnificently, inviting exploration and adventure.",
    "credit": "Switzerland · 2022",
    "long": true,
    "thumb": "mountains2.jpg"
  },
  {
    "img": "IMG_9564.JPEG",
    "caption": "A peaceful retreat: Castle Hill Garden in Budapest.",
    "credit": "Budapest, Hungary · 2022",
    "long": false,
    "thumb": "budapest.jpg"
  },
  {
    "img": "IMG_0598.JPEG",
    "caption": "Towering Art Deco buildings on Wall Street.",
    "credit": "New York City, United States · 2023",
    "long": false,
    "thumb": "newyork2.jpg"
  }
];
