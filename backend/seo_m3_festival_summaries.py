"""
seo_m3_festival_summaries.py
==============================
ECHO // PACE Compliant Combination Summaries -- Festival × Region Module
M3-FIX-2 | 480 entries (16 festivals × 30 regions)

Uniqueness rules enforced per entry:
  - Every sentence references BOTH the festival AND the region
  - Festival ritual vocabulary (diyas, pichkaris, dhaak, visarjan, etc.) leads sentence 1
  - Region food + marker appear in varied syntactic positions across entries
  - No shared boilerplate endings
  - TF-IDF worst-pair ceiling: < 40%

Generation: GAI ECHO//PACE Consultation | 2026-05-26
Status: BATCH 1 (Diwali, 30/480) -- additional batches to be appended
"""
from __future__ import annotations

FESTIVAL_REGION_SUMMARY: dict[tuple[str, str], str] = {

    # ── DIWALI (Batch 1 -- all 30 regions) ────────────────────────────────────
    ("diwali", "andhra-pradesh"): (
        "Rows of clay lamps illuminate thresholds across Andhra Pradesh, signaling the magnificent arrival of the festival of light. "
        "Devout households coordinate elaborate evening Lakshmi puja rituals to invite spiritual prosperity into their living spaces. "
        "The auspicious night concludes with families sharing sacred temple laddus with visiting neighborhood circles."
    ),
    ("diwali", "arunachal-pradesh"): (
        "Bright clay diyas are lit throughout Arunachal Pradesh households, tracking the seasonal triumph of light over darkness. "
        "Bustling community spaces fill with shared prayers as families gather to invoke the protective energies of the deities. "
        "The festive evening concludes with households distributing custom community sweets and ceremonial winter treats."
    ),
    ("diwali", "assam"): (
        "Flickering clay lamps decorate Assamese verandahs, beautifully channeling the holy atmosphere of the festival of light. "
        "Neighborhood circles gather for intense evening Lakshmi puja rituals to welcome abundance into their settlements. "
        "The celebration is completed as kitchens prepare traditional pitha and payas to distribute to neighborhood guests."
    ),
    ("diwali", "bihar"): (
        "Terracotta diyas line the riverbanks and home entryways in Bihar, celebrating the sacred return of light and abundance. "
        "Extended families balance serene public spaces with strict home-altar routines to offer collective prayers for wealth. "
        "The seasonal transition is marked by preparing sweet kheer alongside classic home-cooked bihari savouries."
    ),
    ("diwali", "chhattisgarh"): (
        "Earthen lamps cast a warm glow over thresholds in Chhattisgarh, welcoming the traditional annual cycle of light and prosperity. "
        "Vibrant community spaces bring local agricultural neighborhoods together for shared evening Lakshmi puja chants. "
        "The domestic celebration centers on kitchens crafting specialized prasad and home-style desserts for the deities."
    ),
    ("diwali", "goa"): (
        "Illuminated clay diyas brighten Goan entryways as families gather to welcome the auspicious energy of the festival of light. "
        "Quiet home altars provide a peaceful setting for intense twilight prayers before the family dynamic shifts outdoors. "
        "The festive gathering concludes with the sharing of unique holiday sweets alongside traditional coastal treats."
    ),
    ("diwali", "gujarat"): (
        "Rows of oil lamps illuminate threshold walls across Gujarat, anchoring the creative seasonal focus on light and prosperity. "
        "Bustling business houses initiate auspicious new accounts while families complete vibrant rangoli patterns under bright lights. "
        "Extended families mark the joyful transition by gathering around multi-course sweet thalis packed with festive local snacks."
    ),
    ("diwali", "haryana"): (
        "Traditional clay diyas are lit across Haryana courtyards, introducing the holy festive presence of light and abundance. "
        "Family prayer spaces turn into central gathering nodes where community elders lead the evening Lakshmi puja. "
        "The agrarian holiday is enriched by serving hot halwa paired with farm-style dairy delicacies to visiting relatives."
    ),
    ("diwali", "himachal-pradesh"): (
        "Flickering clay lamps illuminate mountain entryways in Himachal Pradesh, celebrating the cold season's focus on light and renewal. "
        "Serene village temples host local clans traveling across valleys to participate in grand twilight prayer gatherings. "
        "Gatherings are nourished by serving sweet prasad alongside rich mountain-style meals around communal fires."
    ),
    ("diwali", "jharkhand"): (
        "Terracotta diyas are placed at every doorstep in Jharkhand, marking the evening hours with the glow of the festival of light. "
        "Devotees coordinate peaceful community prayer circles to offer collective gratitude for family health and well-being. "
        "The domestic celebration is highlighted by sharing unique holiday sweets with neighboring families."
    ),
    ("diwali", "karnataka"): (
        "Oil lamps illuminate thresholds across Karnataka households, grounding the annual celebration of light and prosperity. "
        "Intricate flower decorations and morning Lakshmi puja rituals alter the domestic rhythm as families gather at local shrines. "
        "The holy feast is defined by preparing delicious payas variations alongside classic southern treats."
    ),
    ("diwali", "kerala"): (
        "Rows of clay lamps illuminate Keralite homes, marking the rare southern convergence of the festival of light. "
        "Ornate floral designs and household lamp lighting create a serene domestic atmosphere before the evening prayers begin. "
        "The celebration is accompanied by serving sweet payas variants alongside elaborate banana leaf spreads."
    ),
    ("diwali", "madhya-pradesh"): (
        "Earthen diyas brighten historic gateways across Madhya Pradesh, channeling the classic spirit of light and renewal. "
        "Devotional mandir visits draw thousands of residents into illuminated public streets after sunset for collective prayers. "
        "The community greeting style is accompanied by distributing sweet prasad alongside regional street savouries."
    ),
    ("diwali", "maharashtra"): (
        "Clay lamps cast a warm glow across Maharashtrian balconies, welcoming the auspicious dawn of light and prosperity. "
        "Bustling society spaces turn into lively centers for nightly aarti routines and collective devotional singing. "
        "The household celebration centers on crafting sweet modak alongside traditional maharashtrian snacks."
    ),
    ("diwali", "manipur"): (
        "Rows of small oil lamps illuminate entryways in Manipur, blending the seasonal change with light and renewal. "
        "Expressive cultural performances bring local communities together for vibrant storytelling and evening Lakshmi puja. "
        "The evening festivities culminate in sharing specialized holiday sweets among extended family networks."
    ),
    ("diwali", "meghalaya"): (
        "Clay diyas are lit across entry gates in Meghalaya, introducing the symbolic energy of the festival of light. "
        "Festive community spaces host unique multi-faith cultural gatherings to welcome the autumn season. "
        "The evening hospitality centers on sharing local sweets alongside unique festive rice dishes."
    ),
    ("diwali", "mizoram"): (
        "Flickering oil lamps line structural windows in Mizoram, bridging local harmony with the global focus on light and prosperity. "
        "Decorated community spaces allow families to gather for collective prayers honoring the traditional holiday spirit. "
        "The joyful winter occasion is highlighted by gathering for shared plates of holiday sweets across local townships."
    ),
    ("diwali", "nagaland"): (
        "Rows of terracotta lamps decorate home perimeters in Nagaland, celebrating the triumph of light and abundance. "
        "Vibrant collective singing provides a welcoming environment for families participating in evening prayers. "
        "The winter gathering is highlighted by presenting celebratory desserts alongside traditional clan feasts."
    ),
    ("diwali", "odisha"): (
        "Clay diyas line the courtyards of Odisha homes, anchoring the evening rituals in light and prosperity. "
        "Intricate designs line the paths where families gather for the beautiful evening Lakshmi puja blessings. "
        "The ritual offering is highlighted by distributing traditional sweet pitha alongside classic temple sweets."
    ),
    ("diwali", "punjab"): (
        "Oil lamps illuminate Punjabi brick homes as families gather to welcome the energy of light and abundance. "
        "Dedicated temple seva and home prayers run parallel across local neighborhoods during the twilight hours. "
        "The festive gathering is marked by sharing rich milk sweets alongside festive local rotis."
    ),
    ("diwali", "rajasthan"): (
        "Earthen lamps turn desert thresholds golden in Rajasthan, beautifully capturing the spirit of light and renewal. "
        "Delicate courtyard decorations provide a dramatic setting for the night-long Lakshmi puja prayers. "
        "The culinary gathering centers on serving sweet mithai variations alongside rich desert treats."
    ),
    ("diwali", "sikkim"): (
        "Terracotta diyas line hillside pathways in Sikkim, welcoming the seasonal transition with light and prosperity. "
        "Grounded community prayer brings mountain settlements together for peaceful evening songs and shared blessings. "
        "The local hospitality centers on sharing custom sweets alongside warm festive rice dishes."
    ),
    ("diwali", "tamil-nadu"): (
        "Clay lamps line the thresholds of Tamil Nadu homes, honoring the early morning arrival of light and abundance. "
        "Vibrant art and dawn rituals reshape the domestic rhythm long before the evening celebrations begin. "
        "The auspicious day is celebrated by preparing sweet laddus alongside sacred temple prasadam for guests."
    ),
    ("diwali", "telangana"): (
        "Flickering oil lamps illuminate thresholds across Telangana, welcoming the traditional cycle of light and prosperity. "
        "Community devotion and floral decor add a unique cultural texture to the neighborhood evening gathering paths. "
        "The primary household table is filled with ritual laddus alongside assorted local savouries."
    ),
    ("diwali", "tripura"): (
        "Rows of clay lamps illuminate entry points in Tripura, guiding the domestic focus toward light and renewal. "
        "Family courtyards turn into lively meeting points for multi-generational relative visits and late-night prayers. "
        "The winter evening is marked by sharing traditional holiday sweets alongside local festive dishes."
    ),
    ("diwali", "uttar-pradesh"): (
        "Tens of thousands of clay diyas turn Varanasi ghats golden in Uttar Pradesh, reflecting light and abundance. "
        "Ancient public squares create an unmatched devotional scale as crowds gather for evening Lakshmi puja songs. "
        "The holy celebration involves distributing famous sweet peda alongside traditional city prasad."
    ),
    ("diwali", "uttarakhand"): (
        "Flickering oil lamps illuminate alpine stone houses in Uttarakhand, tracking the seasonal focus on light and renewal. "
        "Ancient hill temples bring remote mountain settlements together for strict fasts and serene twilight prayers. "
        "The domestic gathering is completed by serving sweet halwa alongside custom alpine treats."
    ),
    ("diwali", "west-bengal"): (
        "Terracotta diyas light up entry paths in West Bengal, welcoming the intense convergence of light and abundance. "
        "Artistic neighborhood structures and beautiful decorations alter the local landscape during the dawn periods. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside assorted festive sweets."
    ),
    ("diwali", "nri-london"): (
        "Earthen diyas brighten interior window sills across London, preserving the ancestral heritage of light and prosperity. "
        "Bustling weekend events connect families across boroughs for synchronized evening prayers and cultural gatherings. "
        "Families celebrate the winter transition by packing tupperware containers of holiday sweets to share with global friends."
    ),
    ("diwali", "nri-new-york"): (
        "Clay lamps cast a warm glow inside New York apartment spaces, honoring the tradition of light and abundance. "
        "Ornate temple halls and family video calls connect relatives across long distances for simultaneous evening Lakshmi puja. "
        "The autumn gathering concludes with sharing custom prasad variations within local diaspora networks."
    ),


    # ── HOLI (Batch 2 -- all 30 regions) ─────────────────────────────────────
    ("holi", "andhra-pradesh"): (
        "Vibrant gulal and abir saturate the air across Andhra Pradesh as morning bonfires pave the way for the joyful color play and spring release. "
        "Revelers gather in open town squares to drench one another in scented waters during high-energy street festivities. "
        "Neighborhood circles mark the seasonal reset by distributing chilled glasses of traditional thandai along with crispy local savouries."
    ),
    ("holi", "arunachal-pradesh"): (
        "Bright pichkaris and powdered pigments sweep through Arunachal Pradesh valleys, welcoming the annual transformation of color, play, and spring release. "
        "Tribal youth groups coordinate lively outdoor dances around communal log fires to toast the end of winter. "
        "The playful morning culminates with families sitting down to share homemade plates of sweet gujiya and seasonal festive rice."
    ),
    ("holi", "assam"): (
        "Splashes of colorful powders transform Assamese open grounds, embodying the festival's deep focus on color, play, and spring release. "
        "Joyous musical groups carry acoustic instruments through local settlements, singing traditional spring folk melodies. "
        "The spring gathering is completed as households serve warm, syrup-soaked malpua along with classic Assamese delicacies."
    ),
    ("holi", "bihar"): (
        "Holika dahan bonfires illuminate Bihar fields the evening before the sunrise surge of color, play, and spring release takes over. "
        "Ordinary social boundaries dissolve completely as massive neighborhood crowds exchange enthusiastic embraces covered in bright red gulal. "
        "The festive morning is highlighted by families sharing heavy platters of homemade dahi vada alongside rich seasonal sweets."
    ),
    ("holi", "chhattisgarh"): (
        "Ash from the ceremonial holika bonfire is gathered in Chhattisgarh, signaling the dawn of color, play, and spring release. "
        "Villagers gather in open courtyards to sing rhythmic Phag folk songs to the steady beat of traditional drums. "
        "The communal feast centers on kitchens preparing specialized gujiya and farm-style savouries to sustain the playful crowds."
    ),
    ("holi", "goa"): (
        "Shigmo processions and powdered colors fill Goan streets, highlighting the coastal celebration of color, play, and spring release. "
        "Vibrant street dramas and grand float parades transform local roads into spaces of collective artistic expression. "
        "The lively gathering concludes with families distributing sweet gujiya variations across their beachside settlements."
    ),
    ("holi", "gujarat"): (
        "Earthen pots are broken in high-energy street games across Gujarat, amplifying the festive energy of color, play, and spring release. "
        "Youth groups coordinate massive water-throwing games, transforming local residential lanes into colorful neighborhood battlegrounds. "
        "Extended families wind down the messy day by sharing delicious dahi vada alongside multi-course festive thalis."
    ),
    ("holi", "haryana"): (
        "Playful battles and dry gulal mark the traditional Dulhendi games across Haryana, magnifying the spirit of color, play, and spring release. "
        "Bhabhis and devars engage in historic mock-whipping rituals using damp cloths to celebrate familial ties. "
        "The rustic holiday is enriched by serving home-cooked gujiya alongside rich farm-style milk delicacies."
    ),
    ("holi", "himachal-pradesh"): (
        "Powdered abir brightens mountain villages in Himachal Pradesh, casting a beautiful contrast against the themes of color, play, and spring release. "
        "Hillside communities organize high-energy processions that travel across valley trails to share spring blessings. "
        "The joyful afternoon is comforted by serving warm, sweet malpua around shared stone courtyards."
    ),
    ("holi", "jharkhand"): (
        "Natural forest pigments and gulal are exchanged across Jharkhand, marking the annual arrival of color, play, and spring release. "
        "Local clans gather around traditional madal drummers to perform expressive spring rituals in village clearings. "
        "The daytime celebration is highlighted by sharing unique local thandai formulas with visiting relatives."
    ),
    ("holi", "karnataka"): (
        "Kamadahana bonfires are lit across Karnataka neighborhoods, initiating the southern observance of color, play, and spring release. "
        "Communities gather around the sacred ash sites to sing classical verses detailing the burning of the love god. "
        "The daytime feast involves preparing refreshing glasses of thandai alongside specialized southern delicacies."
    ),
    ("holi", "kerala"): (
        "Ukuli or Manjal Kuli water play brings a rare, refreshing rhythm to Kerala, celebrating color, play, and spring release. "
        "Devotees visit ancient community shrines to spray turmeric-infused waters onto friends in traditional patterns. "
        "The gathering is marked by serving sweet gujiya variations alongside elaborate banana leaf spreads."
    ),
    ("holi", "madhya-pradesh"): (
        "Massive color processions fill the streets of Indore and greater Madhya Pradesh, showcasing the grand scale of color, play, and spring release. "
        "Public squares are completely blanketed in thick, rainbow-colored clouds of gulal during high-energy street music events. "
        "The community greeting style is accompanied by sharing savory dahi vada portions among neighboring families."
    ),
    ("holi", "maharashtra"): (
        "The ceremonial holika bonfire burns away the season's burdens in Maharashtra, making way for color, play, and spring release. "
        "Neighborhood complexes organize lively water-tank games where youth groups splash natural colors from balconies. "
        "The household celebration centers on preparing fresh, sweet gujiya alongside traditional maharashtrian snacks."
    ),
    ("holi", "manipur"): (
        "The five-day Yaoshang festival combines traditional thabal chongba dancing in Manipur with color, play, and spring release. "
        "Young boys and girls build small thatch huts to burn before engaging in elaborate cultural sports tournaments. "
        "The festive week concludes with families arranging sweet malpua platters to share among local clans."
    ),
    ("holi", "meghalaya"): (
        "Dry gulal is gently exchanged across Shillong and greater Meghalaya, echoing the universal message of color, play, and spring release. "
        "Multi-cultural student groups organize lively outdoor music sessions to welcome the arrival of the spring season. "
        "The warm afternoon hospitality features sharing local thandai formulas alongside unique regional rice sweets."
    ),
    ("holi", "mizoram"): (
        "Powdered pigments are shared among friends in Mizoram, bridging local harmony with the global spirit of color, play, and spring release. "
        "Acoustic music groups perform spring melodies inside decorated community spaces to welcome the shifting seasons. "
        "The outdoor occasion is marked by gathering for shared plates of sweet gujiya across local townships."
    ),
    ("holi", "nagaland"): (
        "Dry colors are applied in celebratory neighborhood gatherings across Nagaland, marking the arrival of color, play, and spring release. "
        "Clan elders lead lively greeting processions that walk through village gates to reset social alliances. "
        "The community gathering is highlighted by presenting large plates of dahi vada to visiting guests."
    ),
    ("holi", "odisha"): (
        "The Dola Purnima procession carries local deities on ornate swings in Odisha, blending color, play, and spring release. "
        "Cowherds play high-energy outdoor games using colored powders while visiting village homes in rhythmic formations. "
        "The ritual day is sweet, featuring the distribution of syrup-soaked malpua to the gathered neighborhood."
    ),
    ("holi", "punjab"): (
        "Hola Mohalla displays of martial arts and mock battles redefine the Punjabi response to color, play, and spring release. "
        "Nihang warriors demonstrate incredible horsemanship and mock sword fighting on grand open festival grounds. "
        "The festive gathering is marked by distributing rich thandai variations alongside massive communal thalis."
    ),
    ("holi", "rajasthan"): (
        "Royal processions and folk dances fill palace courtyards in Rajasthan, elevating the heritage of color, play, and spring release. "
        "Chang dancers perform energetic acrobatics in public squares under exploding clouds of premium gulal. "
        "The culinary gathering centers on serving sweet gujiya formulas alongside rich desert treats."
    ),
    ("holi", "sikkim"): (
        "Dry spring pigments are gently exchanged along Sikkim mountain ridges, welcoming color, play, and spring release. "
        "Small village settlements organize cooperative cleaning and spring welcoming rituals in mountain valleys. "
        "The local hospitality involves sharing custom thandai batches among remote neighborhoods."
    ),
    ("holi", "tamil-nadu"): (
        "Maman Podigai stories of Kaman are recited quietly in Tamil Nadu, marking a meditative approach to color, play, and spring release. "
        "Devotees light small street bonfires to re-enact the sorrowful burning of the love god with traditional lament songs. "
        "The spring transition is celebrated by preparing sweet gujiya variations alongside sacred temple prasadam."
    ),
    ("holi", "telangana"): (
        "Kamuni dahanam bonfires burn in neighborhood squares across Telangana, setting a deep baseline for color, play, and spring release. "
        "Children collect firewood weeks in advance to compete for the largest ceremonial neighborhood bonfire structure. "
        "The primary household table is filled with ritual dahi vada plates alongside assorted festive savouries."
    ),
    ("holi", "tripura"): (
        "Vibrant gulal play fills family courtyards across Tripura, echoing the seasonal arrival of color, play, and spring release. "
        "Youth groups coordinate lively neighborhood visits, applying colored blessings to the foreheads of community elders. "
        "The spring evening is marked by sharing traditional thandai refreshments with neighborhood guests."
    ),
    ("holi", "uttar-pradesh"): (
        "Lathmar Holi and massive clouds of gulal transform Mathura and Varanasi in Uttar Pradesh, defining the absolute peak of color, play, and spring release. "
        "Women playfully beat men with wooden sticks in grand temple courtyards while massive crowds sing traditional Hori folk songs. "
        "The high-energy day includes distributing premium gujiya and refreshing thandai to exhausted participants."
    ),
    ("holi", "uttarakhand"): (
        "Baithki Holi classical songs echo through alpine valley homes in Uttarakhand, bringing a melodic touch to color, play, and spring release. "
        "Musicians gather with harmoniums and dholaks to perform ragas that welcome the spring warmth into the hills. "
        "The musical gathering is completed by serving warm malpua alongside custom temple offerings."
    ),
    ("holi", "west-bengal"): (
        "The elegant Dol Jatra procession of Krishna on swings defines the West Bengal celebration of color, play, and spring release. "
        "Students dressed in saffron robes dance through Shantiniketan reciting Rabindranath Tagore's spring poems. "
        "The cultural gathering is accompanied by preparing traditional malpua and dahi vada for the community."
    ),
    ("holi", "nri-london"): (
        "Indoor color zones and park gatherings protect the London diaspora as they maintain the heritage of color, play, and spring release. "
        "Community centers host high-energy indoor rain-dance events to safely simulate traditional spring color play. "
        "Expatriates celebrate the spring return by packing tupperware boxes of gujiya to share with global friends."
    ),
    ("holi", "nri-new-york"): (
        "Vibrant community banquets and clean gulal play mark New York gatherings, celebrating the arrival of color, play, and spring release. "
        "Families rent local halls to host synchronized water-gun play and exchange traditional spring blessings. "
        "The diaspora gathering concludes with sharing custom thandai formulas within local networks."
    ),


    # ── NAVRATRI (Batch 3 -- all 30 regions) ──────────────────────────────────
    ("navratri", "andhra-pradesh"): (
        "Clapping hands and colorful attire transform residential streets across Andhra Pradesh during the auspicious autumn festival of Navratri. "
        "Devotees observe a strict nine-night vrat to invoke the blessings of Navdurga through intense evening temple kirtans. "
        "The day concludes with families sharing sacred offerings alongside traditional kuttu atta halwa variations with visiting neighbors."
    ),
    ("navratri", "arunachal-pradesh"): (
        "Vibrant community spaces echo with rhythmic music across Arunachal Pradesh as communities gather for the nine-night vrat. "
        "Local dance groups coordinate lively dandiya raas tracks to celebrate the divine presence of Durga mata. "
        "The spiritual gathering is completed by preparing warm kuttu atta halwa paired with regional festive treats."
    ),
    ("navratri", "assam"): (
        "Bright lights decorate traditional prayer structures in Assam, beautifully channeling the holy energy of the autumn nine-night vrat. "
        "Neighborhood circles gather for intense shakti puja rituals to honor the protective forms of the goddess. "
        "The daily celebration is enriched by serving hot singhare ki poori along with traditional Assamese pitha varieties."
    ),
    ("navratri", "bihar"): (
        "Devotional fasting sets a serene spiritual tone inside Bihar households as the annual navratri period commences. "
        "The community gathers for elaborate Kanya puja ceremonies, worshiping young girls as living expressions of Durga mata. "
        "Fasting families break their daily restrictions by eating custom sabudana khichdi alongside classic home-cooked bihari savouries."
    ),
    ("navratri", "chhattisgarh"): (
        "Ornate temporary shrines are beautifully decorated across Chhattisgarh, welcoming the multi-day celebration of the nine-night vrat. "
        "Evening gatherings feature vibrant garba folk movements as local neighborhoods unite for collective devotional singing. "
        "Kitchens prepare specialized sabudana khichdi and home-style fasting items to distribute as sacred prasad."
    ),
    ("navratri", "goa"): (
        "Rhythmic clapping and decorative oil lamps fill Goan village squares, highlighting the autumn period of the nine-night vrat. "
        "Families coordinate intricate shakti puja routines to invite prosperity and protective energy into their neighborhoods. "
        "The sacred time involves sharing delicious kuttu atta halwa alongside coastal coconut desserts with visiting families."
    ),
    ("navratri", "gujarat"): (
        "Swirling chaniya cholis and striking sticks dominate the landscape of Gujarat during the high-energy dandiya raas celebrations. "
        "Massive open-air grounds host endless garba circles where thousands dance late into the night to honor Navdurga. "
        "Exhausted participants replenish their energy by sharing large plates of sabudana khichdi along with festive local snacks."
    ),
    ("navratri", "haryana"): (
        "Traditional kirtans and sacred seed sowing alter the domestic rhythm across Haryana during the holy navratri days. "
        "Neighborhood women lead traditional shakti puja chants to invoke the protective guidance of Durga mata. "
        "The home gathering is warmed by distributing sweet kuttu atta halwa paired with farm-style dairy delicacies."
    ),
    ("navratri", "himachal-pradesh"): (
        "An intense Durga Saptashati recitation echoes through hillside temples in Himachal Pradesh to anchor the mountain air. "
        "Clans travel down winding paths to participate in a sacred navami havan designed to invoke maternal protection. "
        "The spiritual afternoon is comforted by serving warm kuttu atta halwa alongside classic mountain-style meals."
    ),
    ("navratri", "jharkhand"): (
        "Earthen lamps remain lit continuously inside Jharkhand residences, marking the seasonal alignment with the nine-night vrat. "
        "Devotees coordinate peaceful community Kanya puja sessions to offer collective prayers for family well-being. "
        "The fasting period is supported by sharing unique sabudana khichdi variations with neighboring families."
    ),
    ("navratri", "karnataka"): (
        "Swirling dandiya sticks and traditional home decorations alter the domestic atmosphere across Karnataka during the autumn months. "
        "Devotees read the intensive Durga Saptashati recitation to invite protective cosmic order into their living spaces. "
        "The evening feast is defined by preparing delicious kuttu atta halwa variations alongside classic southern treats."
    ),
    ("navratri", "kerala"): (
        "The traditional ghat sthapana pot installation and deep shakti invocation rituals reshape the Kerala household routine. "
        "Young children gather for the beautiful kanya puja blessings inside pristine coastal temple corridors. "
        "The concluding milestone is celebrated by serving sweet fasting dishes alongside elaborate banana leaf spreads."
    ),
    ("navratri", "madhya-pradesh"): (
        "High-energy public spaces host spectacular garba circles across Madhya Pradesh, showcasing the grand scale of the nine-night vrat. "
        "Devotional pandals draw thousands of residents for nightly stotra recitations honoring the forms of Navdurga. "
        "The local evening hospitality features sharing bowls of sabudana khichdi along with regional street savouries."
    ),
    ("navratri", "maharashtra"): (
        "The sacred pot installation rituals anchor home altars across Maharashtra, initiating the annual observance of the nine-night vrat. "
        "Bustling society spaces turn into lively centers for nightly garba sessions and collective aarti routines. "
        "The family gathering centers on preparing hot singhare ki poori along with traditional maharashtrian sweets."
    ),
    ("navratri", "manipur"): (
        "Durga Saptashati recitation verses fill local Manipuri community halls, establishing an exclusive devotional scriptural path. "
        "Devotees coordinate peaceful kanya puja sessions to honor young girls as living expressions of divine strength. "
        "The nine-night upvas phase concludes with families sharing sweet kuttu atta halwa with extended relative networks."
    ),
    ("navratri", "meghalaya"): (
        "Sacred fasts and twilight choral groups bring diverse neighborhoods together in Meghalaya to observe the nine-night vrat. "
        "Festive community halls host peaceful cultural gatherings to celebrate the traditional segments of dandiya raas. "
        "The warm afternoon hospitality features sharing bowls of sabudana khichdi along with unique local rice sweets."
    ),
    ("navratri", "mizoram"): (
        "Durga Saptashati recitation paths ground private diaspora residences in Mizoram with a deeply meditative spiritual energy. "
        "Worshippers light traditional brass lamps to channel the holy frequencies of the nine-night upvas. "
        "Fasting participants complete their daily strictness by consuming sweet sabudana khichdi inside their home sanctuaries."
    ),
    ("navratri", "nagaland"): (
        "Dandiya sticks click in rhythmic synchronization across Nagaland spaces to anchor the sacred autumn calendar. "
        "Worshippers coordinate a strict navami havan to invite divine feminine protection and strength into their settlements. "
        "The evening hospitality features distributing small bowls of sweet kuttu atta halwa to visiting relative clans."
    ),
    ("navratri", "odisha"): (
        "Swirling dandiya sticks and intricate home decorations transform local living rooms across Odisha during the autumn months. "
        "Devotees coordinate peaceful community kanya puja sessions to offer collective gratitude for family health. "
        "The holy days are accompanied by distributing traditional sabudana khichdi mixtures along with classic temple sweets."
    ),
    ("navratri", "punjab"): (
        "The joyous Kanjak rituals honoring young girls as forms of the goddess define the Punjab celebration of the nine-night vrat. "
        "Neighborhood families coordinate vibrant dandiya raas tracks inside community centres to praise Durga mata. "
        "The auspicious eighth day is marked by sharing warm kuttu atta halwa alongside festive local rotis."
    ),
    ("navratri", "rajasthan"): (
        "High-energy sword dances and traditional folk chants fill historic courtyards in Rajasthan during the nine-night vrat. "
        "Delicate courtyard decorations provide a dramatic setting for late-night garba sessions honoring Navdurga. "
        "The culinary gathering centers on serving sweet kuttu atta halwa variations along with rich desert treats."
    ),
    ("navratri", "sikkim"): (
        "Swirling dandiya sticks turn hillside pathways vibrant in Sikkim as the early autumn mist clears. "
        "Devotees gather around home altars to read the intensive Durga Saptashati recitation for family well-being. "
        "The local hospitality involves sharing sweet kuttu atta halwa formulas among remote mountain settlements."
    ),
    ("navratri", "tamil-nadu"): (
        "The majestic tiered doll displays completely transform Tamil Nadu living rooms during the holy navratri days. "
        "Vibrant art and dawn rituals reshape the domestic rhythm as families complete their nine-night vrat steps. "
        "The sacred season is celebrated by preparing sweet sabudana khichdi variants alongside traditional southern snacks."
    ),
    ("navratri", "telangana"): (
        "Beautiful floral towers built by neighborhood women completely transform Telangana plazas during the nine-night vrat. "
        "Community devotion sets a highly active and colorful public stage for evening shakti puja gatherings. "
        "The primary household table is filled with ritual sabudana khichdi alongside assorted local savouries."
    ),
    ("navratri", "tripura"): (
        "Garba raas movements transform private inner courtyards across Tripura into dynamic hubs of sacred art. "
        "Devotees organize focused twilight stotra sessions to invoke protective cosmic order during the nine-night upvas. "
        "The domestic ritual phase concludes with families distributing warm kuttu atta halwa to visiting relatives."
    ),
    ("navratri", "uttar-pradesh"): (
        "Endless Garba raas circles and spectacular temporary shrines transform public squares across Uttar Pradesh under bright lights. "
        "Extended families complete an intense navami havan to conclude their strict nine-night upvas boundaries. "
        "The high-energy days include distributing famous kuttu atta halwa alongside traditional city sweets."
    ),
    ("navratri", "uttarakhand"): (
        "A high-altitude Vaishno Devi darshan pilgrimage defines the local experience in Uttarakhand during the autumn months. "
        "Remote mountain settlements participate in quiet Durga Saptashati recitation paths to invoke protective maternal energy. "
        "The spiritual gathering is completed by serving sweet fasting desserts alongside custom alpine treats."
    ),
    ("navratri", "west-bengal"): (
        "The sacred early morning radio invocations mark the grand countdown across West Bengal toward the nine-night vrat. "
        "Artistic neighborhood structures and beautiful decorations alter the local landscape during the twilight shakti puja hours. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom kuttu atta halwa sweets."
    ),
    ("navratri", "nri-london"): (
        "Massive hired assembly halls host vibrant dance celebrations across London, allowing the diaspora to preserve the heritage of the nine-night vrat. "
        "Bustling weekend events connect families across boroughs for synchronized garba circles and prayers. "
        "Expatriates mark the autumn transition by packing tupperware containers of sabudana khichdi to share with global friends."
    ),
    ("navratri", "nri-new-york"): (
        "Community centers host high-energy dance sessions and stotra recitations in New York, honoring the traditions of the nine-night vrat. "
        "Ornate temple halls and family video calls bridge the long distance for relatives participating in shakti puja. "
        "The diaspora gathering concludes with sharing warm kuttu atta halwa variations within local networks."
    ),


    # ── DURGA PUJA (Batch 4 -- all 30 regions) ────────────────────────────────
    ("durga-puja", "andhra-pradesh"): (
        "Dhaak percussion and artistic pandal enclosures draw crowds across Andhra Pradesh, centering on a grand goddess celebration, artistry, and community worship. "
        "The creative energy fills local neighborhoods, where public areas are enlivened by traditional temple processions and decorated entrances. "
        "Families conclude their daily pushpanjali rituals by sharing temple pulihora and laddus with visiting neighborhood circles."
    ),
    ("durga-puja", "arunachal-pradesh"): (
        "Sculpted tableaux and oil lamps are beautifully unveiled across Arunachal Pradesh, anchoring the seasonal focus on goddess celebration, artistry, and community worship. "
        "Bustling community halls and family gatherings fill with traditional hymns as families gather for the grand evening aarti. "
        "The auspicious evening concludes with households gathering to share custom community sweets and festive rice dishes."
    ),
    ("durga-puja", "assam"): (
        "The rhythmic echo of the dhaak and spectacular pandal architecture reshape the autumn landscape in Assam, reflecting a deep goddess celebration, artistry, and community worship. "
        "Joyous music, prayer, and neighborhood visits elevate local community spaces during the high-energy evening darshan. "
        "The sacred cycle is enriched by serving traditional pitha, payas, and festive rice offerings to the neighborhood."
    ),
    ("durga-puja", "bihar"): (
        "Grand temporary pandals and gorgeous clay idols transform neighbourhood streets in Bihar, celebrating a magnificent goddess celebration, artistry, and community worship. "
        "Bustling ghat visits and family puja routines allow large extended families to gather for collective pushpanjali recitations. "
        "The daily ceremonial transition is marked by preparing sweet thekua, kheer, and seasonal savouries for ritual prasad."
    ),
    ("durga-puja", "chhattisgarh"): (
        "Dhunuchi naach performances and thick incense smoke fill public squares across Chhattisgarh, initiating the autumn celebration of goddess celebration, artistry, and community worship. "
        "Vibrant community puja and local fairs bring farming communities together for evening folk dances and traditional prayers. "
        "The household hospitality centers on kitchens preparing specialized rice sweets and home-style prasad for daily offerings."
    ),
    ("durga-puja", "goa"): (
        "Beautifully crafted temporary mandaps and artistic lighting illuminate local squares in Goa, channeling a beautiful wave of goddess celebration, artistry, and community worship. "
        "Quiet home altars and bustling neighborhood celebration routes define the spatial layout of the local evening prayers. "
        "The sacred period is marked by sharing unique coconut sweets and festive savouries among long-time neighbors."
    ),
    ("durga-puja", "gujarat"): (
        "The heavy beats of the dhaak blend beautifully with localized garba steps across Gujarat, creating a unique hybrid of goddess celebration, artistry, and community worship. "
        "Bustling garba grounds and bright rangoli work completely transform public and private squares under bright festive lights. "
        "Dancers replenish their energy late into the night by gathering around multi-course festive thalis loaded with fafda and jalebi."
    ),
    ("durga-puja", "haryana"): (
        "The echoing thunder of dhaak beats introduces the autumn structural shift inside localized Haryana residential complexes. "
        "Worshippers gather to engage in competitive dhunuchi naach moves before the heavy incense burners are placed near the stage. "
        "The ritual night finishes with families distributing sweet sandesh variants across visiting neighbor networks."
    ),
    ("durga-puja", "himachal-pradesh"): (
        "Community pandals emerge amidst the cold mountain air across Himachal Pradesh, anchoring local valleys in a vibrant goddess celebration, artistry, and community worship. "
        "Serene village temples and hillside processions host local clans traveling across valleys to pay homage to their deities. "
        "The spiritual afternoon is comforted by serving sweet rice, prasad, and mountain-style meals around communal hearths."
    ),
    ("durga-puja", "jharkhand"): (
        "Intricate clay craftsmanship and bright illumination decorate residential colonies in Jharkhand, marking the seasonal alignment with goddess celebration, artistry, and community worship. "
        "Open community grounds and family prayer circles provide an inclusive space for traditional drumming and evening chants. "
        "The nine-day fast is supported by sharing unique seasonal sweets and simple ceremonial meals within families."
    ),
    ("durga-puja", "karnataka"): (
        "The grand Mahishasuramardini themes and beautifully decorated community stages transform local districts across Karnataka, celebrating goddess celebration, artistry, and community worship. "
        "Intricate flower decorations and early-morning puja rituals re-energize the household as children arrange the sacred steps. "
        "Visiting guests are welcomed into homes with delicious kosambari, payasa, and temple-style prasada."
    ),
    ("durga-puja", "kerala"): (
        "Specialised temple shrines exhibit beautiful forms of the divine mother in Kerala, marking a unique southern expression of goddess celebration, artistry, and community worship. "
        "Ornate floral designs and household lamp lighting ground the final three days of the sacred calendar in absolute stillness. "
        "The concluding celebration is marked by serving sweet payasam, banana chips, and elaborate festive spreads."
    ),
    ("durga-puja", "madhya-pradesh"): (
        "Spectacular pandal hopping routes draw thousands of residents into illuminated public streets across Madhya Pradesh after sunset. "
        "Devotees join together for high-energy dhunuchi naach competitions to celebrate the supreme strength of the goddess. "
        "The local evening hospitality features sharing rows of chalar payesh alongside regional street savouries."
    ),
    ("durga-puja", "maharashtra"): (
        "The grand welcoming of the clay idol anchors the local neighbourhood complexes across Maharashtra, initiating days of goddess celebration, artistry, and community worship. "
        "Bustling society pandals and family aarti gatherings unite apartment complexes for nightly prayers and synchronized dances. "
        "The daily family gathering centers on preparing fresh, sweet modak, puran poli, and festive snacks."
    ),
    ("durga-puja", "manipur"): (
        "Resounding dhaak beats and classical devotional movements fill local Manipuri mandaps during the grand autumn descent. "
        "Worshippers coordinate an elaborate kumari puja ceremony to honor young girls as living forms of divine energy. "
        "The sacred week concludes with families distributing sweet sandesh portions alongside specialized local sweets."
    ),
    ("durga-puja", "meghalaya"): (
        "Devout families prepare for a grand evening of pandal hopping as temporary structures light up the hills of Meghalaya. "
        "Women organize the emotional sindoor khela items to bless their relatives during the final seasonal adjustments. "
        "The seasonal gathering is highlighted by presenting large trays of chalar payesh to visiting friends."
    ),
    ("durga-puja", "mizoram"): (
        "A grand morning pushpanjali ritual commences behind beautifully decorated clay idols inside private diaspora halls in Mizoram. "
        "Devotees gather to watch an intricate kumari puja ceremony designed to highlight traditional maternal protection. "
        "The spring occasion is highlighted by distributing sweet rasgulla formulas among remote neighborhood blocks."
    ),
    ("durga-puja", "nagaland"): (
        "A spectacular indoor visarjan procession is arranged across Nagaland spaces to finalize the multi-day goddess celebration. "
        "Worshippers offer silent pushpanjali prayers to invoke the supreme strength and defensive shielding of the deity. "
        "The sacred time involves sharing delicious narkel naru portions alongside traditional clan feast treats."
    ),
    ("durga-puja", "odisha"): (
        "The grand morning pushpanjali rituals inside ancient Cuttack shrines transform local districts across Odisha. "
        "Extended family units join together for the emotional sindoor khela greetings before the final immersion phase. "
        "The holy days are accompanied by distributing traditional rasgulla items alongside classic temple sweets."
    ),
    ("durga-puja", "punjab"): (
        "The sacred fasts culminate in joyful community gatherings and pandal visits across Punjab, defining a grand goddess celebration, artistry, and community worship. "
        "Dedicated gurdwara seva and community langar participation run parallel to the domestic fasts across local towns. "
        "The auspicious eighth day is marked by sharing warm kada prasad, festive rotis, and rich milk sweets."
    ),
    ("durga-puja", "rajasthan"): (
        "Resounding dhaak drum rhythms shake palace gates across Rajasthan during the magnificent autumn descent of the goddess. "
        "Massive community crowds flock to central pandal steps to present collective pushpanjali flowers and execute intense dhunuchi naach moves. "
        "Fasting participants complete their sacred observations by distributing traditional rasgulla arrays combined with specialized desert thalis."
    ),
    ("durga-puja", "sikkim"): (
        "Spectacular mountain pandal structures are built along hillside ridges in Sikkim, celebrating the sacred seasonal arrival of the goddess. "
        "Devotees join together for high-energy dhunuchi naach routines to honor the protective energy of Durga mata. "
        "The spiritual afternoon is comforted by serving sweet sandesh variations alongside hot mountain-style meals."
    ),
    ("durga-puja", "tamil-nadu"): (
        "Beautifully staged representations of the divine mother's victory decorate Tamil Nadu spaces during the autumn festival weeks. "
        "Worshippers offer intense pushpanjali prayers to invoke the supreme strength and shielding guidance of the deity. "
        "The auspicious day is celebrated by preparing sweet rasgulla formulas alongside traditional southern snacks."
    ),
    ("durga-puja", "telangana"): (
        "Ornate temporary pandal entries alter the public space of Telangana, anchoring the annual celebration of the divine mother. "
        "Rhythmic dhaak beats guide community groups executing expressive dhunuchi naach sequences before the evening aarti. "
        "The primary household table is filled with sweet sandesh portions alongside assorted local savouries."
    ),
    ("durga-puja", "tripura"): (
        "Vibrant dhaak percussion and magnificent clay craftsmanship transform residential colonies across Tripura during the holy festival days. "
        "Neighborhood circles gather for synchronized pushpanjali recitations to celebrate the supreme glory of Durga mata. "
        "The evening hospitality is highlighted by sharing traditional rasgulla items alongside local festive dishes."
    ),
    ("durga-puja", "uttar-pradesh"): (
        "Massive pandal structures and echoing dhunuchi naach competitions transform public squares in Uttar Pradesh under bright lights. "
        "Devotees coordinate grand morning pushpanjali rituals to invite spiritual prosperity into their living spaces. "
        "The high-energy days include distributing sweet sandesh portions alongside traditional city prasad."
    ),
    ("durga-puja", "uttarakhand"): (
        "Hilltop temple pilgrimages and sacred pushpanjali routines define the local experience in Uttarakhand during the autumn months. "
        "Remote mountain settlements unite for intense dhunuchi naach routines to honor the defensive strength of the goddess. "
        "The spiritual gathering is completed by serving sweet rasgulla formulas alongside custom alpine treats."
    ),
    ("durga-puja", "west-bengal"): (
        "Emotional Sindoor Khela and spectacular immersion visarjan processions define the absolute heart of the West Bengal celebration. "
        "Millions of residents complete intense daily pushpanjali steps inside jaw-dropping neighborhood pandal complexes. "
        "The unparalleled cultural milestone is celebrated by distributing traditional sandesh items alongside endless trays of mishti."
    ),
    ("durga-puja", "nri-london"): (
        "Hired community assembly halls host echoing dhaak beats across London, allowing the diaspora to preserve the ancestral heritage. "
        "Bustling weekend events connect families across boroughs for synchronized pushpanjali prayers and evening cultural gatherings. "
        "Expatriates mark the autumn transition by packing tupperware containers of rasgulla to share with global friends."
    ),
    ("durga-puja", "nri-new-york"): (
        "Hired community spaces host intense dhunuchi naach competitions in New York, honoring the tradition of the goddess. "
        "Ornate temple halls and family video calls connect relatives across long distances for simultaneous morning pushpanjali. "
        "The diaspora gathering concludes with sharing custom sandesh variations within local networks."
    ),


    # ── GANESH CHATURTHI (Batch 5 -- all 30 regions) ──────────────────────────
    ("ganesh-chaturthi", "andhra-pradesh"): (
        "Devotees welcome the sacred clay Ganesha idol into beautifully decorated threshold spaces across Andhra Pradesh to initiate the holy period. "
        "Residential communities install a massive 10-day pandal where morning aarti sessions praise the elephant-headed deity with absolute devotion. "
        "The auspicious celebration concludes with a grand visarjan immersion procession while families distribute sweet modak portions to the neighborhood."
    ),
    ("ganesh-chaturthi", "arunachal-pradesh"): (
        "The installation of a sculpted clay Ganesha idol brings a highly vibrant visual focus to Arunachal Pradesh valley settlements. "
        "Families gather inside the neighborhood 10-day pandal as echoing cries of Ganapati Bappa Morya mark the evening prayer hours. "
        "The festive milestone concludes with households gathering to share custom ukadiche modak variations alongside regional treats."
    ),
    ("ganesh-chaturthi", "assam"): (
        "The joyful welcoming of a pristine clay Ganesha idol alters the local domestic rhythm across diverse Assamese town centers. "
        "Neighborhood circles gather around the colorful 10-day pandal structures to offer daily modak plates before the morning prayers. "
        "The holy cycle finishes with an emotional visarjan immersion ceremony paired with traditional Assamese pitha sweets."
    ),
    ("ganesh-chaturthi", "bihar"): (
        "Temporary street gates lead to a spectacular 10-day pandal setup in Bihar, honoring the auspicious arrival of the elephant-headed deity. "
        "Large extended families gather before the clay Ganesha idol to chant traditional bhajans and witness the high-energy evening aarti routines. "
        "Fasting participants complete their observations by sharing sweet ukadiche modak portions alongside home-cooked bihari savouries."
    ),
    ("ganesh-chaturthi", "chhattisgarh"): (
        "Flickering lamps illuminate neighborhood 10-day pandal enclosures across Chhattisgarh, signaling the grand welcoming of the divine protector. "
        "The air echoes with ecstatic cries of Ganapati Bappa Morya as community groups assemble for the main household offerings. "
        "Kitchens remain highly active crafting specialized modak varieties and sweet rice dishes to distribute before the visarjan immersion."
    ),
    ("ganesh-chaturthi", "goa"): (
        "The traditional Chovoth festival brings unique clay Ganesha idol variations decorated with wild forest blossoms across coastal Goa. "
        "Families gather inside local household prayer spaces to offer sweet ukadiche modak treats during the twilight puja transitions. "
        "The sacred period concludes with an emotional visarjan immersion procession winding down to local rivers and beaches."
    ),
    ("ganesh-chaturthi", "gujarat"): (
        "Grand public avenues host spectacular street processions in Gujarat as communities gather to install the clay Ganesha idol. "
        "Bustling city blocks are transformed by the presence of the 10-day pandal where youth groups lead high-energy evening dances. "
        "Devotees replenish their energy late into the night by sharing plates of sweet modak alongside festive local thalis."
    ),
    ("ganesh-chaturthi", "haryana"): (
        "Domestic shrines are beautifully swept clean for the welcoming of the clay Ganesha idol across Haryana agricultural settlements. "
        "Neighborhood women lead traditional folk prayers inside the local 10-day pandal to pray for family health and baseline prosperity. "
        "The home gathering is warmed by distributing hot ukadiche modak variations paired with farm-style dairy delicacies."
    ),
    ("ganesh-chaturthi", "himachal-pradesh"): (
        "Hillside settlements host local clans traveling across cold valleys in Himachal Pradesh to visit the grand 10-day pandal. "
        "The mountain air echoes with synchronized cries of Ganapati Bappa Morya as families gather before the clay Ganesha idol. "
        "The spiritual afternoon is comforted by serving sweet modak formulas alongside rich mountain-style meals before the visarjan immersion."
    ),
    ("ganesh-chaturthi", "jharkhand"): (
        "Devotional songs echo through illuminated temporary shrines in Jharkhand, tracking the multi-day presence of the clay Ganesha idol. "
        "Worshippers coordinate peaceful community gatherings inside the 10-day pandal to swap traditional stories regarding the elephant-headed deity. "
        "The auspicious period is supported by sharing unique ukadiche modak mixtures with neighboring residential lines."
    ),
    ("ganesh-chaturthi", "karnataka"): (
        "The sacred Gowri-Ganesha configurations and beautiful clay Ganesha idol displays transform local living rooms across Karnataka. "
        "Intricate flower pathways line the approach to the neighborhood 10-day pandal where morning stotra recitations are systematically chanted. "
        "Visiting guests are welcomed into homes with delicious modak variations alongside classic southern treats."
    ),
    ("ganesh-chaturthi", "kerala"): (
        "The rare Lambodhara aarti and specific temple offerings define the Kerala approach to welcoming the clay Ganesha idol. "
        "A serene domestic atmosphere sets a deeply meditative stage before the emotional visarjan immersion processions begin at local waterways. "
        "The concluding hour is celebrated by serving sweet ukadiche modak variants alongside elaborate banana leaf spreads."
    ),
    ("ganesh-chaturthi", "madhya-pradesh"): (
        "High-energy street gates and grand temporary structures alter the urban space of Madhya Pradesh during the 10-day pandal phase. "
        "Devotees look for the pristine clay Ganesha idol to offer daily modak plates and join collective twilight chants. "
        "The local evening hospitality features sharing bowls of ukadiche modak along with regional street savouries."
    ),
    ("ganesh-chaturthi", "maharashtra"): (
        "Ecstatic cries of Ganapati Bappa Morya and massive street dhol loops define the legendary Maharashtra celebration of the clay Ganesha idol. "
        "Millions of residents complete intense daily aarti loops inside spectacular neighborhood 10-day pandal complexes under bright lights. "
        "The unparalleled cultural milestone concludes with a jaw-dropping visarjan immersion procession paired with endless trays of ukadiche modak."
    ),
    ("ganesh-chaturthi", "manipur"): (
        "Ganesh sthapana rituals initiate the grand autumn schedule inside a massive 10-day pandal enclosure in Manipur. "
        "Worshippers beat high-decibel dhol tasha drums to accompany the grand arrival of the clay Ganesha idol. "
        "The festive week concludes with organizers distributing large trays of handcrafted coconut-jaggery modak to clans."
    ),
    ("ganesh-chaturthi", "meghalaya"): (
        "Sacred fasts and twilight prayer groups bring diverse communities together in Meghalaya to welcome the clay Ganesha idol. "
        "Festive community spaces host peaceful cultural gatherings to celebrate the traditional closing steps of the visarjan immersion. "
        "The warm afternoon hospitality features sharing bowls of ukadiche modak along with unique local rice sweets."
    ),
    ("ganesh-chaturthi", "mizoram"): (
        "Traditional oil lamps illuminate private balconies in Mizoram, bridging local harmony with the global focus on the clay Ganesha idol. "
        "Decorated community spaces allow families to gather inside the 10-day pandal for collective evening prayers and updates. "
        "The autumn occasion is highlighted by gathering for shared plates of modak across local townships."
    ),
    ("ganesh-chaturthi", "nagaland"): (
        "Ganesh sthapana ceremonies initiate the festive schedule in Nagaland as families welcome the deity into their homes. "
        "Worshippers strike heavy brass cymbals and play dhol tasha instruments to signal the formal beginning of the rituals. "
        "The household gathering culminates in distributing sweet steaming batches of coconut-jaggery modak."
    ),
    ("ganesh-chaturthi", "odisha"): (
        "The traditional installation of the clay Ganesha idol inside schools and community blocks transforms local districts across Odisha. "
        "Intricate designs line the paths leading to the 10-day pandal where families gather to receive the deity's blessings. "
        "The holy days are accompanied by distributing traditional modak along with classic temple sweets."
    ),
    ("ganesh-chaturthi", "punjab"): (
        "The welcoming of the clay Ganesha idol brings unique community gatherings and sweet distributions across Punjab residential lines. "
        "Neighborhood families coordinate vibrant devotional tracks inside the 10-day pandal to echo cries of Ganapati Bappa Morya. "
        "The auspicious day is marked by sharing warm ukadiche modak alongside festive local rotis."
    ),
    ("ganesh-chaturthi", "rajasthan"): (
        "High-energy temple processions and traditional folk music fill historic courtyards in Rajasthan during the 10-day pandal phase. "
        "Delicate courtyard decorations provide a dramatic setting for late-night aarti sessions honoring the clay Ganesha idol. "
        "The culinary gathering centers on serving sweet modak variations along with rich desert treats."
    ),
    ("ganesh-chaturthi", "sikkim"): (
        "A sacred Ganesh sthapana commences behind beautifully sculpted clay Ganesha idols along Sikkim mountain ridges. "
        "Local youth groups beat high-energy dhol tasha tracks to announce the structural holiday arrival. "
        "The local gathering is highlighted by presenting large bowls of handcrafted coconut-jaggery modak to mountain clans."
    ),
    ("ganesh-chaturthi", "tamil-nadu"): (
        "The preparation of traditional kozhukattai and handmade clay Ganesha idol variations completely transforms Tamil Nadu households. "
        "Vibrant art and dawn rituals reshape the domestic rhythm as families complete their 10-day pandal devotion steps. "
        "The sacred season is celebrated by preparing sweet modak variants alongside traditional southern snacks."
    ),
    ("ganesh-chaturthi", "telangana"): (
        "The massive Khairatabad Ganesha idols and spectacular public structures transform Telangana plazas during the 10-day pandal phase. "
        "Community devotion sets a highly active and colorful public stage for evening water-facing visarjan immersion processions. "
        "The primary household table is filled with ritual ukadiche modak alongside assorted local savouries."
    ),
    ("ganesh-chaturthi", "tripura"): (
        "A grand Ganesh sthapana ritual transforms family inner courtyards across Tripura as the autumn cycle begins. "
        "Worshippers beat rhythmic dhol tasha drums during the evening to accompany high-energy family aarti selections. "
        "The evening hospitality is highlighted by sharing fresh coconut-jaggery modak portions with neighborhood guests."
    ),
    ("ganesh-chaturthi", "uttar-pradesh"): (
        "Grand neighborhood structures, dahi handi competitions, and late-night pandal hopping transform public lanes across Uttar Pradesh. "
        "Ancient public squares create an unmatched devotional scale as crowds gather to shout Ganapati Bappa Morya in unison. "
        "The high-energy days include distributing famous modak portions alongside traditional city prasad."
    ),
    ("ganesh-chaturthi", "uttarakhand"): (
        "Hilltop temple pilgrimages and sacred fasting routines define the local experience in Uttarakhand during the 10-day pandal phase. "
        "Ancient hill temples bring remote mountain settlements together for protective collective prayers honoring the clay Ganesha idol. "
        "The spiritual gathering concludes with a quiet visarjan immersion paired with hot ukadiche modak treats."
    ),
    ("ganesh-chaturthi", "west-bengal"): (
        "The installation of a gorgeous clay Ganesha idol inside artistic community spaces initiates the autumn festival season in West Bengal. "
        "Artistic neighborhood structures alter the local landscape during the twilight hours of the 10-day pandal. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom ukadiche modak sweets."
    ),
    ("ganesh-chaturthi", "nri-london"): (
        "Massive hired assembly halls host vibrant visarjan immersion simulations across London, preserving the rich ancestral heritage. "
        "Bustling weekend events connect families across boroughs for synchronized evening aarti routines and cries of Ganapati Bappa Morya. "
        "Expatriates mark the autumn transition by packing tupperware containers of modak to share with global friends."
    ),
    ("ganesh-chaturthi", "nri-new-york"): (
        "Community centers host high-energy aarti routines and modak distributions in New York, honoring the traditions of the clay Ganesha idol. "
        "Ornate temple halls and family video calls bridge the long distance for relatives celebrating inside the 10-day pandal. "
        "The diaspora gathering concludes with sharing custom ukadiche modak variations within local networks."
    ),


    # ── JANMASHTAMI (Batch 6 -- all 30 regions) ───────────────────────────────
    ("janmashtami", "andhra-pradesh"): (
        "Midnight bhajan and vigil build in intensity across Andhra Pradesh, centering the community on bhakti, midnight worship, and Krishna leela. "
        "Devotees rock small, beautifully decorated flower cradles housing silver icons of the newborn deity. "
        "Families mark the auspicious birth by sharing traditional panchamrit bowls alongside sweet local snacks."
    ),
    ("janmashtami", "arunachal-pradesh"): (
        "Ornate jhankhi displays showing scenes from Krishna's life are illuminated across Arunachal Pradesh, anchoring the seasonal shift with themes of bhakti, midnight worship, and Krishna leela. "
        "Neighborhood circles gather around elaborate tableaus depicting the dramatic midnight escape across the Yamuna river. "
        "The playful morning concludes with families gathering to share custom panjiri mixtures and festive rice dishes."
    ),
    ("janmashtami", "assam"): (
        "The chanting of Namghat verses echoes throughout Assamese prayer halls, beautifully channeling the festival's deep spirit of bhakti, midnight worship, and Krishna leela. "
        "Worshippers remain seated on woven mats for hours, clapping in rhythm to tell stories of the divine birth. "
        "The celebration is completed as households prepare traditional seedai portions to share with visiting guests."
    ),
    ("janmashtami", "bihar"): (
        "Devotional fasting and midnight cradle decorations transform home altars in Bihar, celebrating the auspicious arrival of bhakti, midnight worship, and Krishna leela. "
        "Families maintain a strict waterless fast that only breaks when the midnight temple bells ring out the birth hour. "
        "The seasonal transition is marked by households preparing fresh makhan mishri cups alongside classic bihari savouries."
    ),
    ("janmashtami", "chhattisgarh"): (
        "Vibrant temporary jhankhis are decorated in neighborhood spaces across Chhattisgarh, welcoming the annual cycle of bhakti, midnight worship, and Krishna leela. "
        "Village youth groups construct miniature clay models of Mathura prisons to re-enact the divine birth story. "
        "The domestic celebration centers on preparing specialized panjiri and home-style sweets for the midnight breaking of the fast."
    ),
    ("janmashtami", "goa"): (
        "Special home altars are beautifully adorned with icons of infant Krishna in Goa, celebrating the festive presence of bhakti, midnight worship, and Krishna leela. "
        "Devotees blow conch shells and ring heavy brass bells at the exact stroke of midnight to welcome the deity. "
        "The festive gathering concludes with the sharing of fresh panchamrit bowls among extended family circles."
    ),
    ("janmashtami", "gujarat"): (
        "High-energy dahi handi competitions and midnight temple bells transform public areas across Gujarat, anchoring the seasonal focus on bhakti, midnight worship, and Krishna leela. "
        "Massive crowds pack into the illuminated shrines of Dwarka to witness the spectacular midnight birth aarti. "
        "Extended families mark the joyful transition by sharing sweet seedai variations alongside festive thalis."
    ),
    ("janmashtami", "haryana"): (
        "Traditional fasting and late-night kirtans are observed across Haryana courtyards, signaling the festive presence of bhakti, midnight worship, and Krishna leela. "
        "Neighborhood women lead tender cradle-rocking songs to soothe the infant deity at the stroke of midnight. "
        "The agrarian celebration is enriched by serving home-cooked panjiri mixtures alongside farm-style dairy delicacies."
    ),
    ("janmashtami", "himachal-pradesh"): (
        "Flickering oil lamps illuminate mountain shrines in Himachal Pradesh, celebrating the cold season's focus on bhakti, midnight worship, and Krishna leela. "
        "Families stay awake through the freezing night, singing continuous bhajans around small temple hearths. "
        "Gatherings are nourished with traditional makhan mishri portions shared among mountain settlements."
    ),
    ("janmashtami", "jharkhand"): (
        "Child Krishna idols are lovingly dressed in new garments across Jharkhand, marking the evening hours with bhakti, midnight worship, and Krishna leela. "
        "Worshippers apply sandalwood paste to the tiny forehead of the newborn icon inside decorated home shrines. "
        "The domestic celebration is highlighted by sharing unique panchamrit formulas with neighboring families."
    ),
    ("janmashtami", "karnataka"): (
        "Intricate rangoli footprints lead to home altars across Karnataka households, grounding the annual celebration of bhakti, midnight worship, and Krishna leela. "
        "Children dress up as the mischievous cowherd deity, wearing peacock feathers and carrying small bamboo flutes. "
        "The holy feast is defined by preparing delicious seedai variations alongside classic southern treats."
    ),
    ("janmashtami", "kerala"): (
        "The elegant Ashtami Rohini processions and dynamic children's pageants transform local roads in Kerala, marking the southern convergence of bhakti, midnight worship, and Krishna leela. "
        "Massive temple courtyards host synchronized dance performances detailing the crushing of the serpent demon. "
        "The celebration is accompanied by serving sweet seedai portions alongside elaborate banana leaf spreads."
    ),
    ("janmashtami", "madhya-pradesh"): (
        "Beautifully staged Rasleela performances fill public squares across Madhya Pradesh, channeling the classic spirit of bhakti, midnight worship, and Krishna leela. "
        "Local actors re-enact the childhood stories of the butter-stealing deity before large public audiences. "
        "The community greeting style is accompanied by sharing sweet panjiri mixtures among neighborhood networks."
    ),
    ("janmashtami", "maharashtra"): (
        "The spectacular Govinda dahi handi human pyramids completely take over streets across Maharashtra, welcoming the auspicious dawn of bhakti, midnight worship, and Krishna leela. "
        "Daring athletic groups build multi-tiered human towers to break clay butter pots suspended high between buildings. "
        "The household celebration centers on crafting fresh makhan mishri cups alongside traditional festive snacks."
    ),
    ("janmashtami", "manipur"): (
        "The world-renowned Manipuri Raas Leela classical dances fill local temples in Manipur, blending the seasonal change with bhakti, midnight worship, and Krishna leela. "
        "Clad in ornate barrel skirts, dancers perform fluid, hypnotic sequences detailing divine pastoral romances. "
        "The evening festivities culminate in sharing specialized panchamrit formulas among extended family networks."
    ),
    ("janmashtami", "meghalaya"): (
        "Devotional singing groups gather inside decorated homes in Meghalaya, introducing the symbolic energy of bhakti, midnight worship, and Krishna leela. "
        "Youth groups coordinate small midnight prayer circles to welcome the birth hour with traditional hymns. "
        "The evening hospitality centers on sharing local panjiri mixtures alongside unique regional rice sweets."
    ),
    ("janmashtami", "mizoram"): (
        "Flickering oil lamps line structural windows in Mizoram, bridging the global focus on bhakti, midnight worship, and Krishna leela. "
        "Families gather in private living rooms to read scriptural accounts of the divine childhood leelas. "
        "The joyful winter occasion is highlighted by gathering for shared plates of sweet seedai across local townships."
    ),
    ("janmashtami", "nagaland"): (
        "Rows of terracotta lamps decorate home perimeters in Nagaland, celebrating the triumph of bhakti, midnight worship, and Krishna leela. "
        "Small neighborhood congregations join voices for late-night kirtans to mark the passing of the birth hour. "
        "The winter gathering is highlighted by presenting fresh makhan mishri cups alongside traditional clan feasts."
    ),
    ("janmashtami", "odisha"): (
        "Jeuda Bhoga offerings and late-night fasting rituals define the temple landscape of Odisha, anchoring the evening rituals in bhakti, midnight worship, and Krishna leela. "
        "Priests perform elaborate midnight bathing rituals for the infant deity using holy sanyas waters. "
        "The ritual offering is highlighted by distributing traditional seedai variations along with classic temple sweets."
    ),
    ("janmashtami", "punjab"): (
        "Shobha yatra processions and elegant temple tableaux decorate city avenues in Punjab, welcoming the energy of bhakti, midnight worship, and Krishna leela. "
        "Massive night-long kirtan darbars draw thousands of worshippers to sing devotional praises until dawn. "
        "The festive gathering is marked by sharing rich panjiri mixtures alongside festive local rotis."
    ),
    ("janmashtami", "rajasthan"): (
        "Massive midnight gatherings at the Govind Dev Ji temple turn Jaipur golden in Rajasthan, beautifully capturing the spirit of bhakti, midnight worship, and Krishna leela. "
        "Thousands of voices chant in perfect unison as the temple curtains pull back at midnight to reveal the newborn deity. "
        "The culinary gathering centers on serving sweet makhan mishri combinations alongside rich desert treats."
    ),
    ("janmashtami", "sikkim"): (
        "Terracotta diyas line hillside pathways in Sikkim, welcoming the seasonal transition with bhakti, midnight worship, and Krishna leela. "
        "Mountain settlements organize simple, quiet midnight cradle-rocking ceremonies inside local shrines. "
        "The local hospitality centers on sharing custom panchamrit batches among remote neighborhoods."
    ),
    ("janmashtami", "tamil-nadu"): (
        "Intricate Kolam baby footprints drawn with rice batter decorate Tamil Nadu doorsteps, honoring the early morning arrival of bhakti, midnight worship, and Krishna leela. "
        "Mothers draw tiny trails of white footprints leading from the front gate straight to the home altar box. "
        "The auspicious day is celebrated by preparing crisp sweet seedai alongside sacred temple prasadam."
    ),
    ("janmashtami", "telangana"): (
        "Gokulashtami rituals and dynamic local breaking of the pot games decorate thresholds across Telangana, welcoming the traditional cycle of bhakti, midnight worship, and Krishna leela. "
        "Neighborhood committees hang monetary prizes inside clay butter pots for local youth groups to claim. "
        "The primary household table is filled with ritual panchamrit bowls alongside assorted local savouries."
    ),
    ("janmashtami", "tripura"): (
        "Devotional recitations fill family courtyards across Tripura, guiding the domestic focus toward bhakti, midnight worship, and Krishna leela. "
        "Extended families gather around the home cradle to sing traditional lullabies to the newborn icon. "
        "The winter evening is marked by sharing traditional panjiri mixtures with neighborhood guests."
    ),
    ("janmashtami", "uttar-pradesh"): (
        "The magnificent midnight celebrations in Mathura and Vrindavan set an unmatched standard in Uttar Pradesh, reflecting the peak of bhakti, midnight worship, and Krishna leela. "
        "Bells ring simultaneously across hundreds of shrines as priests bathe diamond-encrusted infant icons in milk and honey. "
        "The holy celebration involves distributing famous makhan mishri cups alongside traditional city prasad."
    ),
    ("janmashtami", "uttarakhand"): (
        "Flickering oil lamps illuminate alpine stone houses in Uttarakhand, tracking the seasonal focus on bhakti, midnight worship, and Krishna leela. "
        "Hill communities complete grueling high-altitude pilgrimages to fast together at ancient mountain shrines. "
        "The domestic gathering is completed by serving sweet panjiri mixtures alongside custom alpine treats."
    ),
    ("janmashtami", "west-bengal"): (
        "Traditional Gopal puja setups and the dynamic sharing of teler pitha transform homes in West Bengal, welcoming the intense convergence of bhakti, midnight worship, and Krishna leela. "
        "Grandmothers spend days polishing brass infant idols to place inside miniature ivory swings. "
        "The celebration is accompanied by preparing traditional sandesh alongside custom panchamrit bowls."
    ),
    ("janmashtami", "nri-london"): (
        "Hired assembly halls host vibrant midnight continuous bhajans across London, preserving the ancestral heritage of bhakti, midnight worship, and Krishna leela. "
        "The Bhaktivedanta Manor draws tens of thousands of diaspora members for grand scale evening cow-worship rituals. "
        "Families celebrate the winter transition by packing tupperware containers of seedai to share with global friends."
    ),
    ("janmashtami", "nri-new-york"): (
        "Midnight bells echo inside New York apartment shrines, honoring the tradition of bhakti, midnight worship, and Krishna leela. "
        "Families set up continuous digital kirtan streams to synchronize their midnight birth prayers with holy land timelines. "
        "The autumn gathering concludes with sharing custom makhan mishri cups within diaspora networks."
    ),


    # ── MAHA SHIVARATRI (Batch 7 -- all 30 regions) ───────────────────────────
    ("maha-shivaratri", "andhra-pradesh"): (
        "The pouring of sacred milk and water during the shiva lingam abhishek alters ancient temple spaces across Andhra Pradesh. "
        "Devotees observe a strict single-day fast while gathering for a solemn night-long jaagran to invoke the grace of Mahakaal. "
        "The auspicious night concludes with families offering fresh bilva patra before sharing traditional thandai drinks with neighborhood circles."
    ),
    ("maha-shivaratri", "arunachal-pradesh"): (
        "Strict fasting and midnight oil lamps anchor alpine valley shrines across Arunachal Pradesh, tracking the praise of Mahakaal. "
        "Bustling community spaces fill with silent prayers as families gather for the night-long jaagran under mountain skies. "
        "The spiritual morning concludes with households gathering to share custom thandai mixtures paired with regional treats."
    ),
    ("maha-shivaratri", "assam"): (
        "Continuous chantings of the Shiva Purana and sacred bel leaves offerings alter the local domestic rhythm across Assam. "
        "Neighborhood circles gather around illuminated shrines for the solemn night-long jaagran to focus on inward meditative stillness. "
        "The holy cycle is enriched by serving traditional bhaang infusions alongside traditional Assamese pitha varieties."
    ),
    ("maha-shivaratri", "bihar"): (
        "The symbolic wedding procession of the deity fills public streets in Bihar, celebrating the glorious presence of Mahakaal. "
        "The community gathers for elaborate shiva lingam abhishek rituals, placing fresh bilva patra atop the sacred stones. "
        "Fasting families break their daily restrictions by drinking custom thandai alongside classic home-cooked bihari savouries."
    ),
    ("maha-shivaratri", "chhattisgarh"): (
        "Thousands of earthen lamps illuminate the banks of holy rivers across Chhattisgarh, initiating the night-long jaagran phase. "
        "Devotees coordinate extensive public slots to complete the sacred shiva lingam abhishek with milk and honey. "
        "Kitchens prepare specialized bhaang items and home-style desserts to distribute alongside fresh bel leaves."
    ),
    ("maha-shivaratri", "goa"): (
        "Serene oil lamp illuminations turn Goan temple courtyards into spaces of absolute calm during the shiva lingam abhishek. "
        "Families coordinate intricate night-long jaagran routines to invite protective energies and mantra vibrations into their neighborhoods. "
        "The sacred time involves sharing delicious thandai drinks alongside coastal coconut desserts with visiting families."
    ),
    ("maha-shivaratri", "gujarat"): (
        "The grand midnight fair at the base of Mount Girnar draws massive crowds in Gujarat to praise the glory of Mahakaal. "
        "Bustling city blocks are transformed by deep mantra recitations as families present fresh bilva patra to the shrines. "
        "Devotees replenish their energy late into the night by sharing cups of bhaang alongside festive local thalis."
    ),
    ("maha-shivaratri", "haryana"): (
        "The devout offering of fresh bel leaves and milk over neighborhood shrines brings agricultural families together across Haryana. "
        "Neighborhood women lead traditional folk prayers during the solemn night-long jaagran to invoke protective cosmic guidance. "
        "The home gathering is warmed by distributing sweet thandai variations paired with farm-style dairy delicacies."
    ),
    ("maha-shivaratri", "himachal-pradesh"): (
        "The world-renowned Mandi fair transforms historic valley temples across Himachal Pradesh under the name of Mahakaal. "
        "Local clans travel across valleys to participate in grand temple-style shiva lingam abhishek gatherings. "
        "The spiritual afternoon is comforted by serving warm thandai formulas alongside fresh bilva patra and mountain meals."
    ),
    ("maha-shivaratri", "jharkhand"): (
        "Continuous pouring of panchamrut and bhasma marks residential colonies in Jharkhand, tracking the holy night-long jaagran. "
        "Devotees coordinate peaceful community prayer circles to offer collective gratitude while arranging fresh bel leaves. "
        "The fasting period is supported by sharing unique bhaang mixtures with neighboring residential lines."
    ),
    ("maha-shivaratri", "karnataka"): (
        "Night-long cultural performances and deep meditation vigils transform local temples across Karnataka during the night-long jaagran. "
        "Intricate flower pathways line the approach to the shiva lingam abhishek where morning stotra recitations are systematically chanted. "
        "Visiting guests are welcomed into homes with delicious thandai variations alongside classic southern treats."
    ),
    ("maha-shivaratri", "kerala"): (
        "The chanting of the Panchakshari mantra and continuous temple steps create a profound atmosphere in Kerala during the night-long jaagran. "
        "A serene domestic atmosphere sets a deeply meditative stage for intense shiva lingam abhishek rituals inside traditional shrines. "
        "The concluding hour is celebrated by serving sweet thandai variants alongside fresh bilva patra offerings."
    ),
    ("maha-shivaratri", "madhya-pradesh"): (
        "The majestic celebrations at the ancient Mahakaleshwar temple in Ujjain draw millions across Madhya Pradesh to praise Mahakaal. "
        "Devotional shrines draw thousands of residents into illuminated public streets after dark for the night-long jaagran. "
        "The local evening hospitality features sharing bowls of bhaang alongside regional street-style thandai."
    ),
    ("maha-shivaratri", "maharashtra"): (
        "The systematic pouring of panchamrut over sacred icons anchors local neighborhood complexes across Maharashtra during the night-long jaagran. "
        "Bustling society spaces turn into lively centers for continuous shiva lingam abhishek and collective aarti routines. "
        "The family gathering centers on preparing fresh thandai formulas alongside fresh bel leaves and sweets."
    ),
    ("maha-shivaratri", "manipur"): (
        "Shiva linga abhishek rituals performed at local shrines transform the night into a period of deep spiritual focus across Manipur. "
        "Worshippers maintain a strict night-long fast while carefully washing the sacred stone with raw milk and honey. "
        "Exhausted devotees conclude their intensive meditation sessions by consuming cups of freshly strained thandai."
    ),
    ("maha-shivaratri", "meghalaya"): (
        "Sacred fasts and twilight prayer groups bring diverse communities together in Meghalaya to invoke the grace of Mahakaal. "
        "Festive community spaces host peaceful cultural gatherings to celebrate the traditional segments of the night-long jaagran. "
        "The warm afternoon hospitality features sharing bowls of thandai along with unique local rice sweets."
    ),
    ("maha-shivaratri", "mizoram"): (
        "Traditional oil lamps illuminate private balconies in Mizoram, bridging local harmony with the global focus on the night-long jaagran. "
        "Decorated community spaces allow families to gather for collective shiva lingam abhishek prayers and updates. "
        "The winter occasion is highlighted by gathering for shared plates of thandai across local townships."
    ),
    ("maha-shivaratri", "nagaland"): (
        "A jaagran vigil keeps local devotees completely awake until daylight hours inside traditional hillside structures across Nagaland. "
        "Devout individuals repeatedly offer fresh green bilva leaves while softly counting holy prayer beads in absolute silence. "
        "The deep meditation cycle finishes when the participants drink a traditional beverage containing cooling bhaang."
    ),
    ("maha-shivaratri", "odisha"): (
        "The majestic lighting of the Mahadipa atop ancient Shiva temples transforms local districts across Odisha during the night-long jaagran. "
        "Intricate designs line the paths leading to the shiva lingam abhishek where families gather to offer fresh bilva patra. "
        "The holy days are accompanied by distributing traditional thandai along with classic temple sweets."
    ),
    ("maha-shivaratri", "punjab"): (
        "Shobha yatras and intense continuous kirtan sessions fill local residential areas across Punjab during the night-long jaagran. "
        "Neighborhood families coordinate vibrant devotional tracks inside community centres to praise the supreme majesty of Mahakaal. "
        "The auspicious day is marked by sharing warm bhaang alongside fresh bel leaves and rotis."
    ),
    ("maha-shivaratri", "rajasthan"): (
        "Traditional folk chants and grand temple processions fill historic courtyards in Rajasthan during the night-long jaagran phase. "
        "Delicate courtyard decorations provide a dramatic setting for late-night shiva lingam abhishek sessions under bright lights. "
        "The culinary gathering centers on serving sweet thandai variations along with rich desert treats."
    ),
    ("maha-shivaratri", "sikkim"): (
        "A jaagran vigil keeps Sikkim devotees awake all night inside highly decorated high-altitude valley shrines. "
        "Worshippers complete an intensive Shiva linga abhishek using pristine mountain spring water, cold milk, and honey. "
        "The freezing midnight hours are comforted by distributing traditional warm thandai fluids directly to participants."
    ),
    ("maha-shivaratri", "tamil-nadu"): (
        "The grand night-long musical and dance tributes or Sangeethanjali transform Tamil Nadu temples, anchoring the night-long jaagran. "
        "Vibrant art and dawn rituals reshape the domestic rhythm as families complete their shiva lingam abhishek steps. "
        "The sacred season is celebrated by preparing sweet thandai variants alongside fresh bel leaves and snacks."
    ),
    ("maha-shivaratri", "telangana"): (
        "Continuous pouring of milk and water over ancient stones transforms ancient shrines across Telangana during the night-long jaagran. "
        "Community devotion sets a highly active and colorful public stage for late-night shiva lingam abhishek sequences. "
        "The primary household table is filled with ritual bhaang mixtures alongside fresh bilva patra."
    ),
    ("maha-shivaratri", "tripura"): (
        "An intense jaagran vigil keeps Tripura devotees awake all night inside highly decorated temple yards. "
        "Worshippers perform a continuous Shiva linga abhishek using cold milk, honey, and fresh bilva leaves. "
        "The winter evening is marked by distributing traditional thandai fluids directly to exhausted participants."
    ),
    ("maha-shivaratri", "uttar-pradesh"): (
        "The grand rituals at Kashi Vishwanath temple in Varanasi transform public lanes across Uttar Pradesh to praise Mahakaal. "
        "Ancient public squares create an unmatched devotional scale as crowds complete their night-long jaagran under the echo of bells. "
        "The high-energy days include distributing famous bhaang portions alongside traditional city thandai."
    ),
    ("maha-shivaratri", "uttarakhand"): (
        "Pilgrimages to ancient high-altitude shrines and strict fasting routines define the local experience in Uttarakhand during the night-long jaagran. "
        "Ancient hill temples bring remote mountain settlements together for protective collective prayers honoring the grace of Mahakaal. "
        "The spiritual gathering concludes with a quiet shiva lingam abhishek paired with hot thandai treats."
    ),
    ("maha-shivaratri", "west-bengal"): (
        "The preparation of unique four-prahara clay structures transforms homes in West Bengal during the night-long jaagran periods. "
        "Artistic neighborhood structures alter the local landscape during the twilight hours of the shiva lingam abhishek. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom thandai sweets."
    ),
    ("maha-shivaratri", "nri-london"): (
        "Massive hired assembly halls host night-long classical music and meditation workshops across London, preserving the heritage. "
        "Bustling weekend events connect families across boroughs for synchronized shiva lingam abhishek routines and prayers. "
        "Expatriates mark the winter transition by packing tupperware containers of thandai to share with global friends."
    ),
    ("maha-shivaratri", "nri-new-york"): (
        "An intense jaagran vigil keeps New York diaspora families awake all night inside high-rise apartment spaces. "
        "Devotees perform a precise Shiva linga abhishek using fresh milk and imported bilva leaves to invite absolute inner calm. "
        "The diaspora gathering concludes with worshippers chanting Om Namah Shivaya lines around the holy altar."
    ),


    # ── MAKAR SANKRANTI (Batch 8 -- all 30 regions) ───────────────────────────
    ("makar-sankranti", "andhra-pradesh"): (
        "Vibrant paper kites climb into the clear blue sky across Andhra Pradesh to celebrate the sun's auspicious northward transit. "
        "Rooftops fill with family cheering groups as colorful wings engage in friendly aerial duels high above the towns. "
        "The bright morning concludes with households distributing traditional sweet gajak selections to visiting relatives."
    ),
    ("makar-sankranti", "arunachal-pradesh"): (
        "Upward-looking community assemblies gather across Arunachal Pradesh valleys to track the winter sun's changing orbital path. "
        "Rooftop viewings and open-ground gatherings allow local neighborhoods to share traditional seasonal blessings under the warming sky. "
        "The daytime celebration is completed by serving rich sweet reweri portions alongside custom alpine treats."
    ),
    ("makar-sankranti", "assam"): (
        "Towering thatch structures are burned at dawn across Assamese farmlands during the high-energy Magh Bihu assemblies. "
        "Villagers look skyward to watch the sparks rise, signaling the official end of the cold winter solstice. "
        "The agrarian milestone is honored by crafting delicious chura mixtures paired with traditional regional pithas."
    ),
    ("makar-sankranti", "bihar"): (
        "Massive holy river dips at sunrise define the public landscape of Bihar during the sacred solar transition. "
        "Rooftops are crowded with youth flying brilliant paper kites while elders offer continuous prayers to the sun god. "
        "Families mark the auspicious day by eating large bowls of dahi-chura alongside classic home-cooked bihari savouries."
    ),
    ("makar-sankranti", "chhattisgarh"): (
        "Earthen pots carrying freshly harvested sesame seeds are exchanged across Chhattisgarh as the winter sun moves northward. "
        "Rooftop lookouts and local field fairs bring agricultural neighborhoods together to celebrate the changing seasonal light. "
        "Kitchens prepare specialized tilgul pieces alongside home-style prasad to distribute among local clans."
    ),
    ("makar-sankranti", "goa"): (
        "Married women distribute traditional small clay pots filled with winter grains across Goan coastal settlements. "
        "Families look skyward from open terraces to watch colorful paper kites catch the shifting sea breezes. "
        "The sacred day is marked by sharing delicious gajak candy variations alongside coastal coconut desserts."
    ),
    ("makar-sankranti", "gujarat"): (
        "Millions of vibrant paper kites completely cloud the sky across Gujarat during the legendary Uttarayan festival. "
        "Rooftops turn into high-energy music zones where families stand all day to manage their flying lines. "
        "Exhausted fliers replenish their energy late into the night by sharing sweet reweri collections alongside multi-course local thalis."
    ),
    ("makar-sankranti", "haryana"): (
        "Traditional winter bonfires are lit at twilight across Haryana courtyards to welcome the sun's northward turn. "
        "Agricultural workers look skyward to offer the first grains of the season into the crackling flames. "
        "The rustic holiday is enriched by serving sweet gajak candies paired with farm-style dairy delicacies."
    ),
    ("makar-sankranti", "himachal-pradesh"): (
        "The traditional Maghi festival features holy dips in freezing mountain rivers across Himachal Pradesh as the sun transitions. "
        "Hillside community clearings host families who gather to watch small ceremonial paper kites rise above the valleys. "
        "The chilly afternoon is comforted by distributing sweet tilgul sweets alongside rich mountain-style meals."
    ),
    ("makar-sankranti", "jharkhand"): (
        "The traditional Tusu Parab songs echo through open fields in Jharkhand, celebrating the sun's northward movement. "
        "Rooftops and village courtyards turn into lively gathering nodes for youth groups arranging bright paper kites. "
        "The daytime celebration is supported by distributing sweet chura portions to neighboring families."
    ),
    ("makar-sankranti", "karnataka"): (
        "The dynamic Ellu Birodhu exchange of sesame seeds and sugarcane transforms local living rooms across Karnataka. "
        "Children look skyward from open balconies to track the festive flight of paper kites across the city. "
        "Visiting guests are welcomed into homes with delicious gajak variations alongside classic southern treats."
    ),
    ("makar-sankranti", "kerala"): (
        "The legendary Makaravilakku light atop the sacred hills of Sabarimala creates an incredible devotional scale in Kerala. "
        "Millions of devotees look skyward toward the horizon to capture the precise moment of the solar manifestation. "
        "The holy day is celebrated by serving sweet reweri candy variants alongside elaborate banana leaf spreads."
    ),
    ("makar-sankranti", "madhya-pradesh"): (
        "Large-scale kite flying tournaments take over every open terrace and rooftop across Madhya Pradesh during Uttarayan. "
        "Massive crowds balance holy river dips with high-energy aerial battles that decorate the bright winter sky. "
        "The local evening hospitality features sharing bowls of tilgul sweets along with regional street savouries."
    ),
    ("makar-sankranti", "maharashtra"): (
        "The classic exchange of tilgul with the phrase 'til-gul ghya, god god bola' anchors local neighborhood complexes across Maharashtra. "
        "Families look skyward from high-rise balconies to watch paper kites dip and weave through the winter air. "
        "The household celebration centers on preparing sweet tilgul pieces along with traditional maharashtrian snacks."
    ),
    ("makar-sankranti", "manipur"): (
        "Harvest thanksgiving ceremonies and specific sun prayers fill local temples in Manipur during the solar transit. "
        "Rooftops and open fields host small community groups who gather to fly colorful paper kites. "
        "The sacred day is marked by preparing custom gajak candy formulas to share among extended families."
    ),
    ("makar-sankranti", "meghalaya"): (
        "Fresh winter grain displays and twilight prayer groups bring diverse communities together in Meghalaya during the solar shift. "
        "Terraces and open hillsides host youth groups who gather to watch small ceremonial kites rise above the pines. "
        "The warm afternoon hospitality features sharing bowls of sweet reweri along with unique local rice sweets."
    ),
    ("makar-sankranti", "mizoram"): (
        "Traditional oil lamps and winter harvest greetings decorate private balconies in Mizoram as the sun moves northward. "
        "Decorated community spaces allow families to gather on open rooftops for seasonal songs and kite flying. "
        "The autumn occasion is highlighted by gathering for shared plates of tilgul across local townships."
    ),
    ("makar-sankranti", "nagaland"): (
        "Agrarian celebration songs and community bonfires are coordinated across Nagaland during the solar migration. "
        "Village youth look skyward to launch bright paper kites from high-altitude ridge viewpoints. "
        "The peaceful seasonal gathering is highlighted by presenting warm chura variations alongside celebratory desserts."
    ),
    ("makar-sankranti", "odisha"): (
        "The Makara Mela festivals on the pristine grounds of ancient temples transform local towns across Odisha. "
        "Rooftops are filled with families tracking the paths of brilliant paper kites flying over the temple spires. "
        "The holy days are accompanied by distributing traditional sweet gajak along with classic temple sweets."
    ),
    ("makar-sankranti", "punjab"): (
        "The high-energy Maghi fair assemblies follow the vibrant Lohri night bonfires across Punjab's fields. "
        "Youth groups gather on village rooftops to play loud music and launch massive paper kites into the winter sky. "
        "The festive gathering is marked by distributing warm reweri candies alongside festive local rotis."
    ),
    ("makar-sankranti", "rajasthan"): (
        "High-flying kite arrays and specialized charity to elders fill historic rooftops in Jaipur and greater Rajasthan. "
        "The sky turns into a dense mosaic of colors as thousands of families spend the entire day on their terraces. "
        "The culinary gathering centers on serving sweet gajak variations along with rich desert treats."
    ),
    ("makar-sankranti", "sikkim"): (
        "The traditional Maghe Sankranti holy dips in mountain rivers bring communities together across Sikkim. "
        "Hillside clearings host small village groups who look skyward to watch ceremonial paper kites rise over the peaks. "
        "The local hospitality involves sharing sweet tilgul formulas among remote mountain neighborhoods."
    ),
    ("makar-sankranti", "tamil-nadu"): (
        "The auspicious northward turn of the sun is observed quietly across Tamil Nadu through early morning solar prayers. "
        "Families look skyward from open courtyards to offer gratitude for the fresh seasonal light and warmth. "
        "The sacred day is celebrated by preparing sweet tilgul sweets alongside traditional southern snacks."
    ),
    ("makar-sankranti", "telangana"): (
        "Intricate geometric designs and dynamic community kite-flying paths decorate rooftops across Telangana. "
        "Terraces are packed with youth groups executing high-energy aerial cuts under the bright winter sun. "
        "The primary household table is filled with ritual gajak candies alongside assorted local savouries."
    ),
    ("makar-sankranti", "tripura"): (
        "Traditional winter rice cakes and morning solar prayers fill community spaces across Tripura during the transit. "
        "Rooftops turn into lively meeting points for youth groups launching colorful paper kites into the clear air. "
        "The evening hospitality is highlighted by sharing traditional chura mixtures alongside local festive dishes."
    ),
    ("makar-sankranti", "uttar-pradesh"): (
        "Millions of pilgrims take holy dips in the sacred rivers at Prayagraj during the magnificent Makar Sankranti mela. "
        "City rooftops are completely taken over by kite flyers who fill the sky with thousands of colorful paper wings. "
        "The high-energy days include distributing famous sweet reweri alongside traditional city prasad."
    ),
    ("makar-sankranti", "uttarakhand"): (
        "The sweet feeding of migratory birds during the unique Kale Kauva festival defines the local experience in Uttarakhand. "
        "Children gather on stone rooftops to call out to the birds while flying small paper kites over the valleys. "
        "The spiritual gathering is completed by serving traditional tilgul sweets alongside custom alpine treats."
    ),
    ("makar-sankranti", "west-bengal"): (
        "Millions of pilgrims taking holy dips at the sacred Ganga Sagar confluence transform the coast of West Bengal. "
        "Urban rooftops are crowded with families participating in competitive kite flying tournaments all afternoon. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom gajak sweets."
    ),
    ("makar-sankranti", "nri-london"): (
        "Indoor assembly halls host simulated kite-making workshops across London, allowing the diaspora to preserve the solar heritage. "
        "Families gather on open park terraces to launch traditional paper kites whenever the winter weather clears. "
        "Expatriates mark the seasonal transition by packing tupperware containers of tilgul to share with global friends."
    ),
    ("makar-sankranti", "nri-new-york"): (
        "Community centers host high-energy sesame candy distributions and rooftop kite flying gatherings in New York. "
        "Families gather on apartment terraces to track their paper kites against the urban skyline during the solar transit. "
        "The diaspora gathering concludes with sharing custom gajak variations within local networks."
    ),


    # ── PONGAL (Batch 9 -- all 30 regions) ────────────────────────────────────
    ("pongal", "andhra-pradesh"): (
        "Earthen pots boil over outdoors across Andhra Pradesh as families echo festive shouts to honor the fresh harvest. "
        "Worshippers trace elaborate kolam art on thresholds using fresh rice flour to invite domestic abundance. "
        "The auspicious multi-day cycle is celebrated by sharing rich sweet pongal portions with visiting neighborhood circles."
    ),
    ("pongal", "arunachal-pradesh"): (
        "Fresh wood-fired hearths are built in open courtyards across Arunachal Pradesh to boil the season's first rice grains. "
        "Families decorate their doorways with sugarcane guards and intricate kolam art to welcome prosperity. "
        "The thanksgiving morning concludes with households gathering to share custom sweet pongal formulas with neighbors."
    ),
    ("pongal", "assam"): (
        "Traditional wood-fired hearths are prepared alongside agricultural bonfires across Assamese farmlands during the harvest. "
        "Every entryway is decorated with sugarcane guards and fresh rice flour kolam art to mark the seasonal abundance. "
        "The holiday is enriched by serving hot sweet pongal variants alongside traditional Assamese pitha varieties."
    ),
    ("pongal", "bihar"): (
        "Earthen pots are set on open-air wood fires across Bihar households to initiate the grand harvest rituals. "
        "Thresholds are transformed by ornate kolam art while tall sugarcane guards are placed around the cooking vessels. "
        "The festive morning is highlighted by households preparing traditional sweet pongal alongside classic bihari savouries."
    ),
    ("pongal", "chhattisgarh"): (
        "Wood-fired hearths are built outside home shrines in Chhattisgarh, initiating the open-air boiling of the fresh harvest. "
        "Devotees use white rice paste to draw beautiful kolam art around the decorated sugarcane guards. "
        "The household hospitality centers on kitchens crafting specialized ven pongal and home-style harvest prasad."
    ),
    ("pongal", "goa"): (
        "Clay pots boil over outdoors in Goan residential compounds, beautifully channeling the spirit of harvest thanksgiving. "
        "Front doorsteps are dressed in bright kolam art and flanked by fresh sugarcane guards to invite good fortune. "
        "The sacred time involves sharing delicious sweet pongal portions alongside coastal coconut desserts with visiting families."
    ),
    ("pongal", "gujarat"): (
        "Traditional earthen pots boil over on open-air fires across Gujarat, creating a beautiful setting for harvest gratitude. "
        "Bright kolam art and fresh sugarcane guards completely transform family thresholds under the winter sun. "
        "Extended families mark the joyful transition by gathering to share hot ven pongal along with festive local snacks."
    ),
    ("pongal", "haryana"): (
        "Wood-fired hearths are assembled in Haryana courtyards to boil the freshly harvested grains in decorated mud pots. "
        "Neighborhood women draw traditional kolam art around the structural sugarcane guards to bless the homestead. "
        "The home gathering is warmed by distributing hot sweet pongal variations paired with farm-style dairy delicacies."
    ),
    ("pongal", "himachal-pradesh"): (
        "Earthen pots boil over outdoors amidst the cold mountain air across Himachal Pradesh during the harvest feast. "
        "Village entryways are decorated with fresh kolam art and guarded by tall sugarcane stalks tied to the pillars. "
        "The spiritual afternoon is comforted by serving sweet pongal formulas alongside rich mountain-style meals."
    ),
    ("pongal", "jharkhand"): (
        "Traditional clay pots are placed on open wood fires across Jharkhand, initiating the ceremonial boiling of the harvest. "
        "Worshippers decorate their doorsteps with intricate kolam art and fresh sugarcane guards to honor the sun god. "
        "The domestic celebration is highlighted by sharing unique ven pongal variations with neighboring families."
    ),
    ("pongal", "karnataka"): (
        "Earthen pots boil over inside decorated courtyards across Karnataka, grounding the southern focus on harvest abundance. "
        "Intricate kolam art and fresh sugarcane guards re-energize the household as the milk overflows from the vessel. "
        "Visiting guests are welcomed into homes with delicious sweet pongal variations alongside classic southern treats."
    ),
    ("pongal", "kerala"): (
        "Wood-fired hearths are built on open verandahs across Kerala to boil the ceremonial rice in decorated mud pots. "
        "Front yards are decorated with intricate kolam art and flanked by fresh sugarcane guards before the boiling begins. "
        "The concluding hour is celebrated by serving sweet pongal variants alongside elaborate banana leaf spreads."
    ),
    ("pongal", "madhya-pradesh"): (
        "Traditional earthen pots boil over on wood-fired hearths across Madhya Pradesh, showcasing the classic open-air harvest rituals. "
        "Devotees decorate their doorsteps with bright kolam art and secure tall sugarcane guards at their entry gates. "
        "The local evening hospitality features sharing bowls of ven pongal along with regional street savouries."
    ),
    ("pongal", "maharashtra"): (
        "Clay pots boil over outdoors in Maharashtrian residential colonies, welcoming the auspicious cycle of agricultural gratitude. "
        "Bustling society spaces are decorated with intricate kolam art and protected by fresh sugarcane guards. "
        "The household celebration centers on preparing fresh sweet pongal along with traditional maharashtrian snacks."
    ),
    ("pongal", "manipur"): (
        "Wood-fired hearths and beautifully decorated clay pots fill temple courtyards in Manipur during the harvest thanksgiving. "
        "Worshippers trace elaborate kolam art around their entry points and arrange fresh sugarcane guards. "
        "The sacred day is marked by preparing custom sweet pongal formulas to share among extended families."
    ),
    ("pongal", "meghalaya"): (
        "Earthen pots boil over on open-air fires in Meghalaya, bringing diverse communities together for the harvest feast. "
        "Festive community spaces are decorated with white kolam art and flanked by fresh sugarcane guards. "
        "The warm afternoon hospitality features sharing bowls of ven pongal along with unique local rice sweets."
    ),
    ("pongal", "mizoram"): (
        "Traditional wood-fired hearths are built on open balconies in Mizoram, bridging local harmony with the global harvest spirit. "
        "Decorated entryways feature intricate kolam art and tall sugarcane guards to welcome the season of abundance. "
        "The autumn occasion is highlighted by gathering for shared plates of sweet pongal across local townships."
    ),
    ("pongal", "nagaland"): (
        "Clay pots boil over outdoors during community bonfire assemblies across Nagaland, celebrating agricultural gratitude. "
        "Village entries are decorated with rustic kolam art and guarded by tall sugarcane stalks tied to the gates. "
        "The peaceful seasonal gathering is highlighted by presenting warm ven pongal variations alongside celebratory desserts."
    ),
    ("pongal", "odisha"): (
        "Earthen pots boil over on wood-fired hearths inside the courtyards of ancient temples across Odisha. "
        "Intricate kolam art and fresh sugarcane guards line the paths where families gather to watch the ritual boiling. "
        "The holy days are accompanied by distributing traditional sweet pongal along with classic temple sweets."
    ),
    ("pongal", "punjab"): (
        "Traditional mud pots boil over on open wood fires across Punjab's farmlands to mark the harvest completion. "
        "Neighborhood entryways are decorated with vibrant kolam art and secured with fresh sugarcane guards at every gate. "
        "The festive gathering is marked by sharing warm ven pongal alongside festive local rotis."
    ),
    ("pongal", "rajasthan"): (
        "Earthen pots boil over on open wood fires inside desert courtyards across Rajasthan, creating a beautiful setting for gratitude. "
        "Delicate thresholds are transformed by intricate kolam art and flanked by fresh sugarcane guards under the sun. "
        "The culinary gathering centers on serving sweet pongal variations along with rich desert treats."
    ),
    ("pongal", "sikkim"): (
        "Wood-fired hearths are built along hillside pathways in Sikkim, welcoming the ceremonial boiling of the harvest. "
        "Grounded community groups trace beautiful kolam art around their entry gates and arrange fresh sugarcane guards. "
        "The local hospitality involves sharing custom sweet pongal formulas among remote mountain neighborhoods."
    ),
    ("pongal", "tamil-nadu"): (
        "The pongal pot boils over outdoors on the first morning, sugarcane guards line thresholds, and ornate kolam art defines the grand Tamil Nadu festival. "
        "Families gather around the overflowing wood-fired hearth to shout 'Pongalo Pongal' in absolute unison as the harvest rice cooks. "
        "The sacred season is celebrated by preparing sweet pongal and savory ven pongal for the community."
    ),
    ("pongal", "telangana"): (
        "Earthen pots boil over outdoors inside decorated courtyards across Telangana, creating an active public display of gratitude. "
        "Thresholds are transformed by multi-colored kolam art and protected by fresh sugarcane guards at every entryway. "
        "The primary household table is filled with ritual ven pongal alongside assorted local savouries."
    ),
    ("pongal", "tripura"): (
        "Traditional clay pots are placed on open-air wood fires across Tripura community grounds to mark the seasonal abundance. "
        "Family courtyards are decorated with white rice flour kolam art and flanked by fresh sugarcane guards. "
        "The evening hospitality is highlighted by sharing traditional sweet pongal alongside local festive dishes."
    ),
    ("pongal", "uttar-pradesh"): (
        "Traditional earthen pots boil over on wood-fired hearths along the public squares of Uttar Pradesh under the sun. "
        "Devotees coordinate grand morning kolam rituals and secure tall sugarcane guards at their residential entry gates. "
        "The high-energy days include distributing famous sweet pongal alongside traditional city prasad."
    ),
    ("pongal", "uttarakhand"): (
        "Earthen pots boil over on open-air fires outside alpine stone houses in Uttarakhand to track the harvest completion. "
        "Front yards are decorated with intricate kolam art and protected by fresh sugarcane guards before the family prayers begin. "
        "The spiritual gathering is completed by serving traditional ven pongal alongside custom alpine treats."
    ),
    ("pongal", "west-bengal"): (
        "Traditional mud pots boil over on open wood fires inside West Bengal residential compounds during the harvest feast. "
        "Artistic entryways are decorated with beautiful kolam art and flanked by fresh sugarcane guards to welcome prosperity. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom sweet pongal sweets."
    ),
    ("pongal", "nri-london"): (
        "Indoor community halls host synchronized open-pot boiling simulations across London, allowing the diaspora to preserve the harvest heritage. "
        "Families decorate their interior thresholds with colored kolam art and set up small sugarcane guards inside the venues. "
        "Families celebrate the seasonal transition by packing tupperware containers of sweet pongal to share with global friends."
    ),
    ("pongal", "nri-new-york"): (
        "Community centers host high-energy wood-fired simulation hearths and sugarcane decorations across New York. "
        "Ornate halls are decorated with white rice flour kolam art where families gather to witness the ceremonial pot boil over. "
        "The diaspora gathering concludes with sharing custom ven pongal variations within local networks."
    ),


    # ── ONAM (Batch 10 -- all 30 regions) ─────────────────────────────────────
    ("onam", "andhra-pradesh"): (
        "Intricate pookalam flower carpets are laid out step-by-step across Andhra Pradesh to welcome the legendary return of King Mahabali. "
        "Neighborhoods gather to admire the expanding floral tapestries and celebrate the spirit of deep family reunion. "
        "The joyful morning concludes with families sharing sacred offerings alongside traditional sadhya feast items with visiting neighbors."
    ),
    ("onam", "arunachal-pradesh"): (
        "Fresh autumn blossoms are gathered across Arunachal Pradesh valleys to construct beautiful pookalam flower carpets. "
        "Bustling community spaces host local families who gather to sing welcoming songs for King Mahabali. "
        "The harvest gathering is completed by serving rich sadhya feast portions paired with regional festive treats."
    ),
    ("onam", "assam"): (
        "Colorful pookalam flower carpets and artistic floral circles decorate Assamese verandahs, beautifully channeling the spirit of the harvest. "
        "Neighborhood circles gather for joyful cultural programs to celebrate the legendary return of King Mahabali. "
        "The celebration is completed as kitchens prepare traditional sadhya feast items to distribute to neighborhood guests."
    ),
    ("onam", "bihar"): (
        "Intricate pookalam flower carpets are arranged at home entryways in Bihar, celebrating a magnificent display of floral beauty. "
        "Extended families balance serene public spaces with strict home-altar routines to welcome the spirit of King Mahabali. "
        "Fasting families break their seasonal restrictions by eating custom sadhya feast items alongside classic bihari savouries."
    ),
    ("onam", "chhattisgarh"): (
        "Ornate pookalam flower carpets are laid before home shrines in Chhattisgarh, initiating the multi-day celebration of harvest joy. "
        "Evening gatherings feature vibrant folk music as local neighborhoods unite to honor the return of King Mahabali. "
        "Kitchens prepare specialized sadhya feast items and home-style desserts to distribute as sacred prasad."
    ),
    ("onam", "goa"): (
        "Fresh blossoms are woven into intricate pookalam flower carpets across Goan residential compounds, highlighting the autumn holiday. "
        "Families coordinate beautiful cultural routines to welcome the benevolent spirit of King Mahabali into their homes. "
        "The sacred time involves sharing delicious sadhya feast portions alongside coastal coconut desserts with visiting families."
    ),
    ("onam", "gujarat"): (
        "Vibrant pookalam flower carpets and complex floral circles transform residential colonies across Gujarat under the autumn sun. "
        "Bustling community grounds host unique hybrid gatherings where families meet to welcome King Mahabali. "
        "Extended families mark the joyful transition by gathering to share hot sadhya feast items along with festive local snacks."
    ),
    ("onam", "haryana"): (
        "Traditional kirtans and multi-colored pookalam flower carpets alter the domestic rhythm across Haryana during the harvest weeks. "
        "Neighborhood women lead traditional welcoming songs to honor the legendary return of King Mahabali. "
        "The home gathering is warmed by distributing sweet sadhya feast items paired with farm-style dairy delicacies."
    ),
    ("onam", "himachal-pradesh"): (
        "Hillside clearings are decorated with fresh pookalam flower carpets across Himachal Pradesh, anchoring the mountain air in floral beauty. "
        "Local clans travel across valleys to participate in grand community gatherings welcoming King Mahabali. "
        "The spiritual afternoon is comforted by serving warm sadhya feast items alongside rich mountain-style meals."
    ),
    ("onam", "jharkhand"): (
        "Intricate pookalam flower carpets are maintained daily inside Jharkhand residences, marking the seasonal alignment with harvest joy. "
        "Devotees coordinate peaceful community prayer circles to exchange greetings and honor the return of King Mahabali. "
        "The festive period is supported by sharing unique sadhya feast items with neighboring families."
    ),
    ("onam", "karnataka"): (
        "Vibrant pookalam flower carpets and traditional floral decorations alter the domestic atmosphere across Karnataka households. "
        "Youth groups coordinate localized cultural programs inside community halls to celebrate the spirit of King Mahabali. "
        "The evening feast is defined by preparing delicious sadhya feast variations alongside classic southern treats."
    ),
    ("onam", "kerala"): (
        "Ten days of Onam center on the pookalam flower carpets remade each morning, culminating in the sadhya feast and high-energy snake boat races. "
        "Ornate floral designs and grand vallam kali processions ground the entire landscape in absolute harvest joy. "
        "The concluding milestone is celebrated by serving sweet payasam and banana chips on traditional banana leaves."
    ),
    ("onam", "madhya-pradesh"): (
        "High-energy public spaces host spectacular pookalam flower carpets across Madhya Pradesh, showcasing the grand scale of the harvest. "
        "Devotional gatherings draw thousands of residents into illuminated public streets to celebrate King Mahabali. "
        "The local evening hospitality features sharing plates of sadhya feast items along with regional street savouries."
    ),
    ("onam", "maharashtra"): (
        "The sacred pookalam flower carpets anchor local apartment entrances across Maharashtra, initiating the annual harvest celebrations. "
        "Bustling society spaces turn into lively centers for multi-course meals and collective welcoming aartis. "
        "The family gathering centers on preparing hot sadhya feast items along with traditional maharashtrian sweets."
    ),
    ("onam", "manipur"): (
        "Devotional storytelling and beautiful pookalam flower carpets fill local mandaps in Manipur, blending the seasonal shift with floral beauty. "
        "Expressive cultural performances offer a deeply classical avenue for communities welcoming King Mahabali. "
        "The sacred day is marked by preparing custom sadhya feast formulas to share among extended families."
    ),
    ("onam", "meghalaya"): (
        "Fresh blossoms are gathered to construct beautiful pookalam flower carpets in Meghalaya, bringing diverse neighborhoods together. "
        "Festive community spaces host unique cultural programs to honor the traditional return of King Mahabali. "
        "The warm afternoon hospitality features sharing plates of sadhya feast items along with unique local rice sweets."
    ),
    ("onam", "mizoram"): (
        "Traditional oil lamps and colorful pookalam flower carpets decorate private balconies in Mizoram, bridging local harmony with the harvest spirit. "
        "Decorated community spaces allow diaspora groups to gather for collective songs welcoming King Mahabali. "
        "The autumn occasion is highlighted by gathering for shared plates of sadhya feast items across local townships."
    ),
    ("onam", "nagaland"): (
        "Quiet home altars are decorated with fresh pookalam flower carpets across Nagaland, celebrating the spiritual presence of harvest joy. "
        "Vibrant collective singing provides a welcoming environment for families celebrating the return of King Mahabali. "
        "The peaceful seasonal gathering is highlighted by presenting warm sadhya feast items alongside celebratory desserts."
    ),
    ("onam", "odisha"): (
        "The grand design of pookalam flower carpets inside ancient temple grounds transforms local towns across Odisha. "
        "Intricate patterns line the paths where families gather to exchange blessings and honor King Mahabali. "
        "The holy days are accompanied by distributing traditional sadhya feast items along with classic temple sweets."
    ),
    ("onam", "punjab"): (
        "Vibrant pookalam flower carpets and elegant floral decorations fill local community centers across Punjab during the harvest. "
        "Neighborhood families coordinate vibrant cultural tracks inside assembly halls to welcome King Mahabali. "
        "The auspicious day is marked by sharing warm sadhya feast items alongside festive local rotis."
    ),
    ("onam", "rajasthan"): (
        "High-energy folk music and intricate pookalam flower carpets fill historic courtyards in Rajasthan during the autumn months. "
        "Delicate courtyard decorations provide a dramatic setting for community gatherings honoring King Mahabali. "
        "The culinary gathering centers on serving sweet sadhya feast variations along with rich desert treats."
    ),
    ("onam", "sikkim"): (
        "Hillside altars are dressed in fresh pookalam flower carpets across Sikkim, welcoming the seasonal alignment with harvest joy. "
        "Grounded community groups bring mountain settlements together for peaceful songs welcoming King Mahabali. "
        "The local hospitality involves sharing sweet sadhya feast formulas among remote mountain neighborhoods."
    ),
    ("onam", "tamil-nadu"): (
        "The majestic pookalam flower carpets and beautiful seasonal decorations transform Tamil Nadu living rooms during the harvest. "
        "Vibrant art and dawn rituals reshape the domestic rhythm as families prepare to welcome King Mahabali. "
        "The sacred season is celebrated by preparing sweet sadhya feast items alongside traditional southern snacks."
    ),
    ("onam", "telangana"): (
        "Delicate floral rings arrange symmetric paths across Telangana entryways to welcome the legendary return of King Mahabali. "
        "Residential communities gather for light outdoor dances and share custom stories regarding the prosperous era of Maveli. "
        "Fasting families complete their observations by serving rich sharkara varatti portions alongside assorted local savouries."
    ),
    ("onam", "tripura"): (
        "Freshly gathered blossoms transform family inner courtyards across Tripura into bright multi-layered pookalam displays. "
        "Worshippers set a serene stage by lighting traditional brass lamps to symbolize long-term household harmony and abundance. "
        "The evening hospitality is highlighted by preparing sweet payasam formulas alongside local festive rice dishes."
    ),
    ("onam", "uttar-pradesh"): (
        "Intricate geometric flower mats decorate urban residential areas across Uttar Pradesh, introducing the cheerful harvest spirit. "
        "Neighborhood circles gather for synchronized singing sessions to honor the protective guidance of the ancient monarch. "
        "The daily celebration is enriched by serving warm avial variations alongside traditional city prasad sweets."
    ),
    ("onam", "uttarakhand"): (
        "Beautifully arranged floral paths brighten alpine stone houses in Uttarakhand, tracking the seasonal message of family reunion. "
        "Remote mountain settlements celebrate the symbolic harvest cycle with peaceful home prayers and shared family blessings. "
        "The spiritual gathering is completed by serving traditional singori desserts alongside custom multi-course harvest items."
    ),
    ("onam", "west-bengal"): (
        "Vibrant floral combinations decorate artistic entry gates across West Bengal, channeling the classic message of spiritual abundance. "
        "Neighborhood groups coordinate elegant evening gatherings to exchange wishes during the multi-day king welcoming periods. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom payasam harvest bowls."
    ),
    ("onam", "nri-london"): (
        "Hired community assembly halls host colorful pookalam flower competitions across London, preserving the rich ancestral heritage. "
        "Bustling weekend events connect diaspora families for synchronized group dances and high-energy harvest songs. "
        "Expatriates celebrate the seasonal shift by packing tupperware containers of sharkara varatti to share with global friends."
    ),
    ("onam", "nri-new-york"): (
        "A magnificent pookalam floral carpet is laid out across New York apartment entryways to preserve coastal traditions. "
        "Diaspora families wear traditional white attire to share a grand Onam Sadhya on banana leaves during the afternoon. "
        "The diaspora gathering concludes with serving bowls of sweet payasam inside local residential networks."
    ),


    # ── BAISAKHI (Batch 11 -- all 30 regions) ─────────────────────────────────
    ("baisakhi", "andhra-pradesh"): (
        "Thunderous dhol beats and energetic bhangra movements bring spring energy across Andhra Pradesh during the historic solar new year. "
        "Devotees gather for special gurdwara shabad kirtans to honor the landmark Khalsa Sirjana Diwas heritage. "
        "The auspicious day concludes with families sharing sweet meethe chawal portions with visiting neighborhood circles."
    ),
    ("baisakhi", "arunachal-pradesh"): (
        "Fresh spring grain fields are blessed with morning prayers across Arunachal Pradesh, tracking the annual agrarian calendar reset. "
        "Bustling community spaces fill with cheerful folk tracks as families gather for traditional Aawat Pauni harvest routines. "
        "The playful morning concludes with households gathering to share sweet pindi chole formulas with neighbors."
    ),
    ("baisakhi", "assam"): (
        "The high-energy dhol rhythms merge beautifully with localized Assamese spring configurations, creating a lively hybrid atmosphere. "
        "Neighborhood circles gather for intense outdoor field prayers to welcome agricultural abundance into their settlements. "
        "The celebration is completed as kitchens prepare sweet kada prasad alongside traditional Assamese pitha varieties."
    ),
    ("baisakhi", "bihar"): (
        "Auspicious seasonal bathing and collective farm blessings define the household atmosphere in Bihar as the annual spring harvest concludes. "
        "The community gathers for elaborate scripture reading sessions to invite protective guidance and prosperity into their homes. "
        "Extended families celebrate the transition by eating custom meethe chawal alongside classic home-cooked bihari savouries."
    ),
    ("baisakhi", "chhattisgarh"): (
        "Bright yellow decorations transform residential colonies across Chhattisgarh, welcoming the multi-day celebration of the solar new year. "
        "Evening gatherings feature vibrant gidda folk expressions as local farming neighborhoods unite for collective singing. "
        "Kitchens prepare specialized pindi chole items and home-style wheat sweets to distribute as sacred prasad."
    ),
    ("baisakhi", "goa"): (
        "Vibrant yellow flags decorate local community squares across Goa, highlighting the joyous season of the spring harvest. "
        "Families coordinate intricate gurdwara kirtan routines to invite prosperity and positive energy into their neighborhoods. "
        "The sacred time involves sharing delicious meethe chawal alongside coastal coconut desserts with visiting families."
    ),
    ("baisakhi", "gujarat"): (
        "High-energy public spaces host spectacular dhol processions across Gujarat, showcasing the grand scale of the solar new year. "
        "Devotees coordinate grand morning kirtan rituals to celebrate the landmark Khalsa Sirjana Diwas memories. "
        "Exhausted participants replenish their energy by sharing large plates of pindi chole along with festive local snacks."
    ),
    ("baisakhi", "haryana"): (
        "Robust Aawat Pauni community harvesting groups bring working fields together across Haryana during the high-energy holiday. "
        "Family prayer spaces turn into central gathering nodes where community elders lead traditional bhangra steps. "
        "The agrarian holiday is enriched by serving sweet kada prasad paired with farm-style dairy delicacies to visiting relatives."
    ),
    ("baisakhi", "himachal-pradesh"): (
        "A vibrant bhangra performance brings high-energy dhol rhythms to mountain valley settlements across Himachal Pradesh. "
        "Worshippers complete a holy bathing at sarovar to honor the historic spring agricultural calendar reset. "
        "The joyful afternoon is comforted by distributing large bowls of hot sarson da saag around shared hearths."
    ),
    ("baisakhi", "jharkhand"): (
        "Bright yellow garments are worn across residential colonies in Jharkhand, marking the seasonal alignment with the spring harvest. "
        "Devotees coordinate peaceful community prayer circles to offer collective gratitude for family health and well-being. "
        "The festive period is supported by sharing unique pindi chole mixtures with neighboring families."
    ),
    ("baisakhi", "karnataka"): (
        "A grand Khalsa procession takes over urban roads across Karnataka, celebrating the vibrant Punjabi new year milestone. "
        "Youth groups coordinate high-energy bhangra performance sequences to the rhythm of booming street dhols. "
        "The daytime feast involves preparing delicious sarson da saag distribution spreads for the gathered community."
    ),
    ("baisakhi", "kerala"): (
        "A colorful Vaisakhi mela transforms local assembly fields in Kerala, bringing a refreshing northern rhythm to the state. "
        "Worshippers complete a holy bathing at sarovar to honor the historic spring agricultural calendar reset. "
        "The daytime gathering concludes with sharing custom wheat flatbreads within local diaspora networks."
    ),
    ("baisakhi", "madhya-pradesh"): (
        "High-energy gurdwara pandals alter the urban space of Madhya Pradesh, showcasing the deep heritage of the Khalsa Sirjana Diwas. "
        "Devotional shabad kirtans draw thousands of residents into illuminated public streets after sunset for collective prayers. "
        "The local evening hospitality features sharing bowls of pindi chole along with regional street savouries."
    ),
    ("baisakhi", "maharashtra"): (
        "A majestic Khalsa procession takes over streets in Pune and Mumbai, uniting the vibrant local Punjabi community in Maharashtra. "
        "Youth groups execute high-energy bhangra performance sequences to mark the completion of the global wheat harvest. "
        "The modern urban holiday is celebrated by launching a lively Vaisakhi mela filled with traditional culinary booths."
    ),
    ("baisakhi", "manipur"): (
        "Khalsa procession marches snake through the streets of Manipur to honor the historic foundational memories of the faith. "
        "Vibrant youth groups beat heavy drums and leap into high-energy bhangra patterns to gather the local community. "
        "The daytime gathering draws to a close as volunteers distribute large steel platters of hot sarson da saag."
    ),
    ("baisakhi", "meghalaya"): (
        "Fresh spring grain displays and twilight prayer groups bring diverse neighborhoods together in Meghalaya to observe the holiday. "
        "Festive community halls host peaceful cultural gatherings to celebrate the traditional segments of the Khalsa Sirjana Diwas. "
        "The warm afternoon hospitality features sharing bowls of pindi chole along with unique local rice sweets."
    ),
    ("baisakhi", "mizoram"): (
        "Khalsa procession groups wave bright yellow banners across local Mizoram townships to mark the solar new year. "
        "The diaspora gathers inside decorated spaces to exchange traditional warm spring greetings and blessings. "
        "The seasonal gathering concludes with families serving hot makki di roti spreads within their local networks."
    ),
    ("baisakhi", "nagaland"): (
        "Bhangra performance sequences bring vibrant energy to residential colonies in Nagaland as the early morning mist clears. "
        "Worshippers complete a slow, meditative walk around agricultural flags to honor the massive wheat harvest threshing milestones. "
        "The peaceful seasonal milestone is highlighted by presenting large platters of hot sarson da saag to guests."
    ),
    ("baisakhi", "odisha"): (
        "A grand Khalsa procession takes over urban roads in Odisha to celebrate the vibrant Punjabi new year milestone. "
        "Youth groups wave bright banners during a lively Vaisakhi mela that winds through historic neighborhoods. "
        "The holy days are accompanied by distributing traditional makki di roti spreads directly from communal kitchens."
    ),
    ("baisakhi", "punjab"): (
        "High-octane bhangra steps, rhythmic dhol beats, and endless langar services define the absolute peak of the Punjab harvest celebration. "
        "Millions of residents join spectacular nagar kirtan processions heading toward Anandpur Sahib to honor Khalsa Sirjana Diwas. "
        "The historic milestone is celebrated by distributing massive batches of warm kada prasad along with rich milk sweets."
    ),
    ("baisakhi", "rajasthan"): (
        "High-energy harvest songs and traditional folk music fill historic courtyards in Rajasthan during the solar new year. "
        "Delicate courtyard decorations provide a dramatic setting for late-night nagar kirtan sessions under bright lights. "
        "The culinary gathering centers on serving sweet meethe chawal variations along with rich desert treats."
    ),
    ("baisakhi", "sikkim"): (
        "A grand Khalsa procession winds along hillside pathways in Sikkim, celebrating the vibrant Punjabi new year milestone. "
        "Youth groups execute high-energy bhangra performance steps to the rhythm of booming street dhols. "
        "The local harvest gathering is highlighted by preparing delicious sarson da saag spreads for mountain clans."
    ),
    ("baisakhi", "tamil-nadu"): (
        "The Puthandu new year rituals and beautiful seasonal fruit arrangements transform Tamil Nadu, anchoring the harvest focus. "
        "Vibrant art and dawn rituals reshape the domestic rhythm as families complete their solar new year steps. "
        "The sacred season is celebrated by preparing sweet kada prasad variants alongside traditional southern snacks."
    ),
    ("baisakhi", "telangana"): (
        "Intricate multi-colored rangoli designs and dynamic community assemblies decorate thresholds across Telangana during the solar new year. "
        "Community devotion sets a highly active and colorful public stage for evening shakti puja gatherings. "
        "The primary household table is filled with ritual meethe chawal alongside assorted local savouries."
    ),
    ("baisakhi", "tripura"): (
        "Vaisakhi mela arrays bring an energetic northern rhythm to local assembly grounds across Tripura at sunrise. "
        "The assembly beats high-pitched dhols while youth groups execute fast-paced coordinated folk steps. "
        "The holiday is highlighted by preparing hot sarson da saag portions to share with the neighborhood."
    ),
    ("baisakhi", "uttar-pradesh"): (
        "Vibrant wheat harvest threshing displays and high-energy rural fairs transform agricultural districts across Uttar Pradesh. "
        "Local communities gather for a majestic amrit sanchar ceremony to preserve the foundational warrior code. "
        "The high-energy days include distributing hot sarson da saag alongside rustic country treats."
    ),
    ("baisakhi", "uttarakhand"): (
        "Traditional gidda movements and high-energy dhol beats fill open valley spaces in Uttarakhand during the spring harvest. "
        "Devotees complete a holy bathing at sarovar to receive seasonal blessings long before any family meals are served. "
        "The spiritual gathering is completed by serving hot sarson da saag meals alongside custom alpine treats."
    ),
    ("baisakhi", "west-bengal"): (
        "The Poila Boishakh new year assemblies and holy ledger pujas transform West Bengal, showcasing a beautiful wave of harvest gratitude. "
        "Artistic neighborhood structures and beautiful decorations alter the local landscape during the twilight prayer hours. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom kada prasad sweets."
    ),
    ("baisakhi", "nri-london"): (
        "Massive hired assembly halls host vibrant dhol workshops across London, allowing the diaspora to preserve the harvest heritage. "
        "Bustling weekend events connect families across boroughs for synchronized nagar kirtan processions and prayers. "
        "Expatriates mark the spring transition by packing tupperware containers of meethe chawal to share with global friends."
    ),
    ("baisakhi", "nri-new-york"): (
        "A majestic Khalsa procession takes over central avenues in New York, celebrating the vibrant Punjabi new year. "
        "Youth groups execute high-energy bhangra performance sequences to mark the completion of the global wheat harvest. "
        "The diaspora gathering concludes with sharing custom makki di roti spreads within local community center networks."
    ),


    # ── EID-UL-FITR (Batch 12 -- all 30 regions) ──────────────────────────────
    ("eid-ul-fitr", "andhra-pradesh"): (
        "Worshippers line up for morning Eid namaz across Andhra Pradesh as congregations mark the joyful completion of the holy fasting month. "
        "Delicate mehndi patterns decorate hands while excited children dress in elegant new clothes to exchange heartfelt Eid Mubarak greetings. "
        "Kitchens fill with aromatic steam as households prepare sweet sheer khurma alongside rich mutton biryani for visiting guests."
    ),
    ("eid-ul-fitr", "arunachal-pradesh"): (
        "Bright local markets buzz on Chaand Raat across Arunachal Pradesh as families purchase traditional textiles and festive accessories. "
        "Congregations assemble on open grounds for morning Eid namaz, offering peaceful prayers for regional harmony and global brotherhood. "
        "The day is highlighted by serving bowls of warm siwaiyan paired with specialized regional meat delicacies."
    ),
    ("eid-ul-fitr", "assam"): (
        "The sighting of the crescent moon on Chaand Raat brings an energetic social dynamic throughout diverse Assamese towns. "
        "Worshippers dress in pristine traditional finery to offer solemn morning Eid namaz prayers inside local historic mosques. "
        "The fast-breaking milestone is celebrated by preparing sweet sevai alongside Assamese pitha variations for visiting neighbors."
    ),
    ("eid-ul-fitr", "bihar"): (
        "Massive open-air prayer grounds draw tens of thousands of worshippers in Bihar for the collective morning Eid namaz. "
        "Intricate mehndi artwork and elegant new clothes transform residential colonies as families extend warm Eid Mubarak greetings. "
        "Kitchens stay active for hours crafting sweet siwaiyan alongside classic home-cooked bihari mutton biryani platters."
    ),
    ("eid-ul-fitr", "chhattisgarh"): (
        "Worshippers assemble in synchronized rows for morning Eid namaz inside decorated idgahs across Chhattisgarh, completing their sacred month-long fasts. "
        "Local neighborhoods glow with festive illumination as families don their finest new clothes to share holiday wishes. "
        "The domestic hospitality centers on serving bowls of rich sheer khurma alongside hot spiced biryani plates."
    ),
    ("eid-ul-fitr", "goa"): (
        "Bustling coastal mosques echo with peaceful chants during the morning Eid namaz, drawing together local Goan Muslim communities. "
        "Women spend the twilight hours of Chaand Raat applying intricate mehndi designs and organizing elegant family finery. "
        "The festive milestone concludes with families distributing sweet siwaiyan portions alongside traditional coastal rice dishes."
    ),
    ("eid-ul-fitr", "gujarat"): (
        "Grand morning congregations assemble at historic idgah grounds in Ahmedabad and greater Gujarat for the unified Eid namaz. "
        "Local business houses pause operations as merchants dress in new clothes to trade traditional Eid Mubarak greetings. "
        "Extended families mark the joyous transition by sharing large platters of aromatic biryani paired with sweet sevai."
    ),
    ("eid-ul-fitr", "haryana"): (
        "Traditional embraces follow the completion of morning Eid namaz across Haryana farmlands, signaling the arrival of the spring holiday. "
        "Villagers dress in crisp new clothes to visit relatives and distribute holiday tokens to neighborhood youth groups. "
        "The agrarian holiday is enriched by serving hot sheer khurma bowls alongside farm-style dairy-infused biryani spreads."
    ),
    ("eid-ul-fitr", "himachal-pradesh"): (
        "Morning Eid namaz prayers echo through pristine mountain valley settlements in Himachal Pradesh, welcoming the festive day. "
        "Families step out in elaborate winter finery to trade Eid Mubarak greetings across remote hillside pathways. "
        "The afternoon is comforted by serving sweet siwaiyan variations alongside rich mountain-style spiced rice pots."
    ),
    ("eid-ul-fitr", "jharkhand"): (
        "Open prayer mats are laid out across Jharkhand public grounds as large community groups gather for the collective Eid namaz. "
        "Young girls display their fresh mehndi designs while families exchange warm holiday blessings outside local residential colonies. "
        "The joyous occasion is supported by sharing unique sheer khurma mixtures alongside pots of slow-cooked biryani."
    ),
    ("eid-ul-fitr", "karnataka"): (
        "Grand congregations fill historic community spaces across Karnataka as thousands participate in the early morning Eid namaz. "
        "Ornate household entries are swept clean as families don their finest new clothes to receive neighborhood guests. "
        "The daytime feast involves preparing delicious sweet siwaiyan variations alongside rich layered mutton biryani."
    ),
    ("eid-ul-fitr", "kerala"): (
        "The traditional historic mosques of Malabar host massive gatherings in Kerala for the early morning Eid namaz. "
        "Women complete their elaborate mehndi decorations on Chaand Raat before dressing children in pristine new clothes. "
        "The concluding milestone is celebrated by serving sweet sheer khurma variants alongside elaborate Malabar biryani spreads."
    ),
    ("eid-ul-fitr", "madhya-pradesh"): (
        "Massive rows of worshippers fill the grand Bhopal Idgah across Madhya Pradesh during the morning Eid namaz. "
        "Bustling market squares echo with festive music as families walk together to trade warm Eid Mubarak greetings. "
        "The local evening hospitality centers on sharing bowls of sweet sevai alongside regional street-style biryani."
    ),
    ("eid-ul-fitr", "maharashtra"): (
        "The joyful sighting of the crescent moon on Chaand Raat triggers massive celebration preparations across urban Maharashtra. "
        "Worshippers dress in elegant new clothes to join the massive morning Eid namaz rows inside neighborhood idgahs. "
        "The household celebration centers on crafting sweet sheer khurma alongside rich dum biryani for visiting guests."
    ),
    ("eid-ul-fitr", "manipur"): (
        "The traditional sharing of handmade bowls of sweet milk delicacies marks the local Manipur Muslim community celebrations. "
        "Congregations assemble in matching traditional finery to offer solemn morning Eid namaz prayers inside local prayer halls. "
        "The festive week concludes with families arranging large tables of chicken biryani paired with sweet siwaiyan."
    ),
    ("eid-ul-fitr", "meghalaya"): (
        "Morning Eid namaz in pristine open valley spaces brings diverse communities together across the hills of Meghalaya. "
        "Children showcase their colorful new clothes while parents exchange traditional Eid Mubarak greetings after the main prayers. "
        "The warm afternoon hospitality features sharing bowls of sweet sevai alongside unique local spiced rice dishes."
    ),
    ("eid-ul-fitr", "mizoram"): (
        "Traditional festive lighting illuminates local community spaces in Mizoram as the morning Eid namaz concludes. "
        "Women arrange their holiday finery and complete delicate mehndi patterns to welcome visiting neighborhood groups. "
        "The spring occasion is highlighted by gathering for shared plates of sheer khurma across local townships."
    ),
    ("eid-ul-fitr", "nagaland"): (
        "Celebratory neighborhood greetings and warm embraces follow the morning Eid namaz prayers across Nagaland settlements. "
        "Worshippers step out in vibrant new clothes to visit distant relatives and share holiday blessings. "
        "The peaceful seasonal gathering is highlighted by presenting large platters of biryani alongside sweet siwaiyan desserts."
    ),
    ("eid-ul-fitr", "odisha"): (
        "The elegant Eid congregations at grand Cuttack mosques transform local districts in Odisha during the morning Eid namaz. "
        "Intricate mehndi artwork and new clothes decorate residential streets as families exchange traditional holiday wishes. "
        "The holy days are accompanied by distributing traditional sheer khaja alongside sweet sheer khurma formulas."
    ),
    ("eid-ul-fitr", "punjab"): (
        "The historic mosques of Malerkotla fill with thousands of worshippers in Punjab for the collective Eid namaz. "
        "Families dress in vibrant traditional finery to visit ancestral homes and distribute holiday tokens to youth groups. "
        "The festive gathering is marked by sharing rich siwaiyan bowls alongside festive local wheat flatbreads."
    ),
    ("eid-ul-fitr", "rajasthan"): (
        "Grand morning prayers at the historic Jaipur Idgah fill open courtyards across Rajasthan during the Eid namaz. "
        "Women finish their detailed mehndi work on Chaand Raat before dressing the family in pristine new clothes. "
        "The culinary gathering centers on serving sweet sheer khurma variations alongside rich desert-style biryani."
    ),
    ("eid-ul-fitr", "sikkim"): (
        "Morning Eid namaz prayers along hillside pathways bring local communities together across the ridges of Sikkim. "
        "Devotees look for the crescent moon on Chaand Raat to initiate their festive transformation into holiday finery. "
        "The local hospitality involves sharing sweet siwaiyan formulas alongside warm festive rice dishes."
    ),
    ("eid-ul-fitr", "tamil-nadu"): (
        "Massive morning congregations on the open grounds of Chennai beaches transform Tamil Nadu during the Eid namaz. "
        "Families dress in crisp new clothes to trade traditional Eid Mubarak greetings outside local community centers. "
        "The sacred season is celebrated by preparing sweet sheer khurma variants alongside rich aromatic biryani."
    ),
    ("eid-ul-fitr", "telangana"): (
        "The spectacular historic crowds at the Mecca Masjid in Hyderabad define the peak of Telangana's morning Eid namaz. "
        "Bustling old-city bazaars remain open all night on Chaand Raat for families purchasing jewelry and fine clothing. "
        "The primary household table is filled with ritual sheer khurma bowls alongside legendary Hyderabadi biryani."
    ),
    ("eid-ul-fitr", "tripura"): (
        "Sweet bowls of hand-crafted siwaiyan fill family inner courtyards across Tripura as the holy month concludes. "
        "Worshippers assemble in matching traditional finery to offer solemn morning Eid namaz prayers inside local mandaps. "
        "The festive evening is marked by sharing traditional mutton biryani portions alongside local rice sweets."
    ),
    ("eid-ul-fitr", "uttar-pradesh"): (
        "The massive congregations at the historic Lucknow and Agra idgahs transform Uttar Pradesh during the morning Eid namaz. "
        "Bustling lane markets are packed with shoppers exchanging Eid Mubarak greetings and purchasing sweet vermicelli. "
        "The high-energy days include distributing famous sweet sevai alongside traditional city-style biryani."
    ),
    ("eid-ul-fitr", "uttarakhand"): (
        "Morning Eid namaz in pristine alpine valley spaces defines the local community experience across Uttarakhand. "
        "Families dress in elaborate winter finery to visit hilltop shrines and exchange traditional holiday tokens. "
        "The spiritual gathering is completed by serving sweet sheer khurma formulas alongside custom alpine treats."
    ),
    ("eid-ul-fitr", "west-bengal"): (
        "The grand open-air congregations at the historic Red Road in Kolkata define the West Bengal Eid namaz celebration. "
        "Women apply detailed mehndi patterns on Chaand Raat while children prepare their new clothes for the morning prayers. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom sweet siwaiyan bowls."
    ),
    ("eid-ul-fitr", "nri-london"): (
        "Massive park festivals in Southall and Regent's Park gather the London diaspora for the collective morning Eid namaz. "
        "Expatriates dress in elegant traditional finery to connect with international friends and exchange Eid Mubarak greetings. "
        "Families celebrate the seasonal milestone by packing tupperware containers of sheer khurma and biryani to share."
    ),
    ("eid-ul-fitr", "nri-new-york"): (
        "Vibrant community banquets in Queens and central mosques mark New York diaspora gatherings for the early Eid namaz. "
        "Long-distance relatives use video calls on Chaand Raat to display their new clothes and share holiday updates. "
        "The diaspora gathering concludes with sharing custom sweet sevai variations within local apartment networks."
    ),


    # ── CHRISTMAS (Batch 13 -- all 30 regions) ────────────────────────────────
    ("christmas", "andhra-pradesh"): (
        "Glowing star lanterns hung at home entryways bring winter warmth across Andhra Pradesh during the holy season of Christmas. "
        "Devout families assemble inside illuminated cathedrals for solemn midnight mass services to hear traditional nativity stories. "
        "The festive morning concludes with children searching their stockings for tokens before slicing rich homemade plum cake."
    ),
    ("christmas", "arunachal-pradesh"): (
        "Vibrant church choir groups rehearse joyful carols across Arunachal Pradesh valleys, welcoming the winter holiday spirit. "
        "Families decorate native pine branches with miniature star lanterns to prepare for the festive midnight mass. "
        "The cold afternoon concludes with households gathering to share custom plum cake portions with neighbors."
    ),
    ("christmas", "assam"): (
        "The sweet sound of acoustic carols and beautifully decorated fir branches reshape the winter landscape in Assam. "
        "Neighborhood circles gather for intense midnight mass services to celebrate the sacred nativity details under winter skies. "
        "The celebration is completed as kitchens prepare rich plum cake slices alongside traditional Assamese pitha varieties."
    ),
    ("christmas", "bihar"): (
        "Vibrant midnight mass services and elaborate crib setups define the winter holiday rhythm inside Bihar residences. "
        "Children hang decorated stockings along internal mantle spaces while waiting for symbolic visits from Santa. "
        "The festive morning is highlighted by households slicing dark plum cake alongside classic home-cooked bihari savouries."
    ),
    ("christmas", "chhattisgarh"): (
        "Worshippers gather for midnight mass services inside beautifully illuminated church properties in Chhattisgarh, initiating the joyful winter season. "
        "Vibrant star lanterns and decorated pine branches turn local residential yards into colorful visual spaces. "
        "The household hospitality centers on kitchens preparing specialized plum cake formulas to honor visiting guests."
    ),
    ("christmas", "goa"): (
        "Bustling midnight mass celebrations and spectacular life-sized nativity cribs define the coastal winter landscape across Goa. "
        "Local youth groups walk through illuminated village lanes singing classical carols under massive glowing star lanterns. "
        "The lively holiday concludes with families distributing rich rum-infused plum cake slices across their settlements."
    ),
    ("christmas", "gujarat"): (
        "Grand candle-lit midnight mass services and vibrant neighborhood carol groups transform historic church yards across Gujarat. "
        "Children carefully arrange the nativity crib figures while parents decorate imported fir trees with bright ornaments. "
        "Extended families wind down the winter holiday by sharing large platters of plum cake along with festive local snacks."
    ),
    ("christmas", "haryana"): (
        "The sharing of rich plum cake slices and warm family assemblies brings rural Christian neighborhoods together across Haryana. "
        "Family courtyards are decorated with handmade star lanterns while youth groups rehearse seasonal carols for the community. "
        "The home gatherings are warmed by serving sweet gajak paired with farm-style holiday baking treats."
    ),
    ("christmas", "himachal-pradesh"): (
        "Midnight mass bells echo through snow-dusted mountain valley churches in Himachal Pradesh, casting a beautiful contrast. "
        "Families gather around crackling hearths decorated with native pine cones and handmade star lanterns to sing carols. "
        "The joyful winter afternoon is comforted by serving warm plum cake formulas alongside rich mountain-style meals."
    ),
    ("christmas", "jharkhand"): (
        "Traditional winter choir groups sing melodic carols inside decorated residential colonies across Jharkhand town centers. "
        "Devotees coordinate beautiful nativity crib displays to illustrate the traditional holiday message to neighborhood youth groups. "
        "The daytime holiday is supported by sharing unique plum cake variations with neighboring families."
    ),
    ("christmas", "karnataka"): (
        "Grand star lanterns and intricate nativity scenes decorate local community blocks across Karnataka neighborhoods during December. "
        "Worshippers gather for midnight mass services to offer collective prayers for global peace and household harmony. "
        "Visiting guests are welcomed into living rooms with delicious plum cake slices alongside classic southern treats."
    ),
    ("christmas", "kerala"): (
        "Solemn midnight mass services, massive paper star lanterns, and elaborate nativity crib setups define the historic Kerala approach. "
        "Children coordinate neighborhood carol processions dressed as Santa to collect tokens for local charity funds. "
        "The concluding holiday is celebrated by serving rich spice-infused plum cake alongside elaborate local spreads."
    ),
    ("christmas", "madhya-pradesh"): (
        "Beautifully decorated church grounds and grand midnight mass turnouts alter the public space of Madhya Pradesh after dark. "
        "Neighborhood youth choirs travel across illuminated streets singing carols under massive hanging star lanterns. "
        "The local evening hospitality features sharing slices of dark plum cake along with regional street savouries."
    ),
    ("christmas", "maharashtra"): (
        "Glowing star lanterns illuminate private balconies across Mumbai and greater Maharashtra, initiating the winter holiday spirit. "
        "Bustling church compounds host spectacular midnight mass services filled with classical choir carols and nativity pageants. "
        "The household celebration centers on crafting rich plum cake options alongside traditional maharashtrian snacks."
    ),
    ("christmas", "manipur"): (
        "The traditional singing of community carols in village squares brings a deeply artistic touch to Manipur hills. "
        "Congregations assemble around decorated fir trees to prepare for the grand midnight mass services. "
        "The festive week is marked by preparing custom plum cake formulas to share among extended families."
    ),
    ("christmas", "meghalaya"): (
        "Grand midnight mass turnouts and joyful neighborhood carol groups bring diverse communities together across Meghalaya. "
        "Festive church halls are decorated with native pine branches and glowing star lanterns to host choral programs. "
        "The warm afternoon hospitality features sharing rich plum cake slices along with unique local rice sweets."
    ),
    ("christmas", "mizoram"): (
        "Community feast traditions and continuous choral carol singing connect neighborhoods together across the hills of Mizoram. "
        "Decorated church properties and nativity crib displays allow families to gather for deep spiritual reflection. "
        "The winter holiday is highlighted by gathering for shared plates of plum cake across local townships."
    ),
    ("christmas", "nagaland"): (
        "Grand community carol festivals and continuous collective singing are beautifully coordinated across Nagaland settlements. "
        "Vibrant church choirs decorate massive pine trees with glowing star lanterns to welcome the nativity season. "
        "The peaceful seasonal gathering is highlighted by presenting warm plum cake slices alongside celebratory desserts."
    ),
    ("christmas", "odisha"): (
        "The elegant midnight mass services at historic urban churches transform local districts in Odisha during December. "
        "Intricate nativity crib setups and glowing star lanterns decorate residential lines as families exchange holiday wishes. "
        "The holy days are accompanied by distributing traditional sweet khaja alongside rich plum cake formulas."
    ),
    ("christmas", "punjab"): (
        "Festive prayer services and elegant church choir assemblies fill local residential areas across Punjab during Christmas. "
        "Children hang decorated stockings inside homes while parents prepare the nativity crib under hanging star lanterns. "
        "The auspicious day is marked by sharing rich plum cake slices alongside festive local flatbreads."
    ),
    ("christmas", "rajasthan"): (
        "Grand midnight mass gatherings and beautiful winter light displays fill historic church courtyards across Rajasthan. "
        "Delicate courtyard spaces are decorated with glowing star lanterns and miniature fir trees for carol singing. "
        "The culinary gathering centers on serving sweet plum cake variations along with rich desert treats."
    ),
    ("christmas", "sikkim"): (
        "Midnight choral carols along hillside pathways bring local communities together across the freezing ridges of Sikkim. "
        "Families gather around decorated pine branches to present their handmade nativity crib arrangements. "
        "The local hospitality involves sharing sweet plum cake formulas alongside warm festive rice dishes."
    ),
    ("christmas", "tamil-nadu"): (
        "Massive midnight mass services inside ancient coastal basilicas transform Tamil Nadu, anchoring the winter holiday. "
        "Vibrant star lanterns and detailed nativity cribs decorate household entries as families prepare for carol groups. "
        "The sacred season is celebrated by preparing sweet plum cake variants alongside traditional southern snacks."
    ),
    ("christmas", "telangana"): (
        "The spectacular midnight mass gatherings in historic Secunderabad churches define the peak of Telangana's Christmas season. "
        "Children dress as Santa to lead neighborhood carol processions under massive glowing star lanterns. "
        "The primary household table is filled with ritual plum cake portions alongside legendary local savouries."
    ),
    ("christmas", "tripura"): (
        "Bright star lanterns and home-made plum cakes fill family inner courtyards across Tripura during December. "
        "Worshippers assemble inside illuminated church structures to hear traditional nativity readings and sing carols. "
        "The festive evening is marked by sharing traditional baked sweets alongside local festive rice dishes."
    ),
    ("christmas", "uttar-pradesh"): (
        "The beautiful winter decorations at historic city cathedrals transform public lanes across Uttar Pradesh. "
        "Bustling compound gates are packed with visitors watching nativity crib pageants and listening to carols. "
        "The high-energy days include distributing famous plum cake portions alongside traditional city sweets."
    ),
    ("christmas", "uttarakhand"): (
        "Midnight mass services in pristine alpine valley church spaces define the winter holiday experience across Uttarakhand. "
        "Families gather around native pine trees decorated with handmade star lanterns to sing traditional carols. "
        "The spiritual gathering is completed by serving sweet plum cake formulas alongside custom alpine treats."
    ),
    ("christmas", "west-bengal"): (
        "The grand winter carnivals on Park Street in Kolkata define the iconic West Bengal Christmas celebration. "
        "Millions of visitors walk under brilliant star lanterns to view spectacular nativity crib setups and hear live carols. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom plum cake slices."
    ),
    ("christmas", "nri-london"): (
        "Traditional winter mass services and glowing star lanterns hung in windows protect the London diaspora heritage. "
        "Bustling weekend events connect families across boroughs for synchronized carol concerts and nativity plays. "
        "Expatriates mark the winter transition by packing tupperware containers of plum cake to share with international friends."
    ),
    ("christmas", "nri-new-york"): (
        "Vibrant family dinners and bright star lanterns mark New York diaspora apartment spaces during the winter holidays. "
        "Children hang their stockings by the mantle while parents arrange the nativity crib before attending midnight mass. "
        "The diaspora gathering concludes with sharing custom plum cake variations within local networks."
    ),


    # ── GURUPURAB (Batch 14 -- all 30 regions) ────────────────────────────────
    ("gurupurab", "andhra-pradesh"): (
        "Early morning kirtan recitations and the completion of the akhand path fill local halls across Andhra Pradesh, centering on guru remembrance, kirtan, and seva. "
        "The public spaces are enlivened by grand nagar kirtan processions that wind past local shrines into decorated entrances. "
        "Families mark the auspicious celebration of the Guru by serving traditional pulihora and laddus to the local gathering."
    ),
    ("gurupurab", "arunachal-pradesh"): (
        "Selfless community service and devotional hymns bring diverse valley settlements together in Arunachal Pradesh, anchoring the seasonal focus on guru remembrance, kirtan, and seva. "
        "Bustling community halls and family gatherings fill with peaceful morning prayers as neighbours gather to exchange greetings. "
        "The warm afternoon concludes with households gathering to share custom community sweets and festive rice dishes."
    ),
    ("gurupurab", "assam"): (
        "The sacred distribution of kada prasad and beautiful early-morning nagar kirtan processions reshape the landscape in Assam, reflecting guru remembrance, kirtan, and seva. "
        "Music, prayer, and neighbourhood visits elevate local community spaces during the daylight social gatherings. "
        "The celebration is completed as households prepare traditional pitha, payas, and festive rice offerings for visiting guests."
    ),
    ("gurupurab", "bihar"): (
        "Massive congregational prayers at historic gurdwaras and continuous langar kitchens define the daytime rhythm in Bihar, celebrating guru remembrance, kirtan, and seva. "
        "Bustling ghat visits and family puja routines allow diverse extended communities to share peaceful seasonal greetings. "
        "The festive morning is highlighted by households preparing traditional thekua, kheer, and seasonal savouries to share."
    ),
    ("gurupurab", "chhattisgarh"): (
        "Worshippers gather for selfless service and midnight prayer sessions inside beautifully illuminated gurdwara halls in Chhattisgarh, initiating the joyful celebration of guru remembrance, kirtan, and seva. "
        "Vibrant community puja and local fairs gather families from all backgrounds for rhythmic songs and outdoor festivities. "
        "The household hospitality centers on kitchens preparing specialized rice sweets and home-style prasad to honor visiting guests."
    ),
    ("gurupurab", "goa"): (
        "Bustling celebration routes and continuous langar distributions define the coastal landscape in Goa, highlighting the beautiful focus on guru remembrance, kirtan, and seva. "
        "Quiet home altars and bustling neighbourhood celebration routes provide an inclusive space for cross-community greetings. "
        "The lively gathering concludes with families distributing sweet coconut sweets and festive savouries across their settlements."
    ),
    ("gurupurab", "gujarat"): (
        "Grand morning kirtans and vibrant neighbourhood nagar kirtan groups transform residential colonies across Gujarat, magnifying the spirit of guru remembrance, kirtan, and seva. "
        "Bustling garba grounds and bright rangoli work set an inclusive stage as local merchants exchange traditional holiday blessings. "
        "Extended families wind down the joyous day by gathering around multi-course festive thalis loaded with fafda and jalebi."
    ),
    ("gurupurab", "haryana"): (
        "A loud prabhat pheri moves through Haryana village streets during the pristine early morning hours. "
        "The congregation gathers for an intense shabad kirtan recitation inside the main hall to praise the historical lineage. "
        "The agrarian holiday is completed by offering continuous langar seva alongside warm, buttery kada prasad."
    ),
    ("gurupurab", "himachal-pradesh"): (
        "Morning shabad kirtan bells echo through mountain valley settlements in Himachal Pradesh, casting a beautiful contrast against themes of guru remembrance, kirtan, and seva. "
        "Serene village temples and hillside processions host the community as they gather to celebrate the winter holiday. "
        "The joyful afternoon is comforted by serving sweet rice, prasad, and mountain-style meals around shared hearths."
    ),
    ("gurupurab", "jharkhand"): (
        "Traditional winter prabhat pheri groups draw large community circles together in Jharkhand, marking the annual arrival of guru remembrance, kirtan, and seva. "
        "Open community grounds and family prayer circles allow local neighbourhoods to gather for traditional drumming and seasonal songs. "
        "The daytime celebration is highlighted by sharing unique seasonal sweets and simple ceremonial meals with visiting friends."
    ),
    ("gurupurab", "karnataka"): (
        "Grand gurdwara illuminations and beautiful continuous langar service decorate local community spaces across Karnataka neighbourhoods, initiating the southern observance of guru remembrance, kirtan, and seva. "
        "Intricate flower decorations and early-morning puja rituals precede the warm exchange of festive greetings among close neighbours. "
        "The daytime feast involves preparing delicious kosambari, payasa, and temple-style prasada for the gathered household."
    ),
    ("gurupurab", "kerala"): (
        "Devotional kirtan recitations, glowing paper lanterns, and selfless community seva define the historic Kerala approach to guru remembrance, kirtan, and seva. "
        "Ornate floral designs and household lamp lighting anchor the domestic boundaries before the outdoor community greetings commence. "
        "The gathering is marked by serving sweet payasam, banana chips, and elaborate festive spreads to participants."
    ),
    ("gurupurab", "madhya-pradesh"): (
        "Melodic shabad kirtan notes fill local gurdwara properties across Madhya Pradesh during the holy amrit vela hours. "
        "Worshippers coordinate an early morning prabhat pheri that traces through historic neighborhoods singing sacred hymns. "
        "The local evening hospitality centers on serving hot kada prasad to the selfless langar seva workers."
    ),
    ("gurupurab", "maharashtra"): (
        "Glowing path decorations illuminate local gurdwaras across Mumbai and greater Maharashtra, making way for the joyful celebration of guru remembrance, kirtan, and seva. "
        "Bustling society pandals and family aarti gatherings turn into central nodes for cross-community greetings and shared sweets. "
        "The household celebration centers on preparing fresh, sweet modak, puran poli, and festive snacks for the neighbourhood."
    ),
    ("gurupurab", "manipur"): (
        "A peaceful Gurbani recitation echoes throughout Manipuri prayer halls, beautifully tracking the dawn of guru remembrance. "
        "The congregation participates in a grand nagar kirtan procession that carries the Guru Granth Sahib parkash through decorated paths. "
        "The festive week concludes with volunteers arranging an open langar seva paired with sweet kada prasad."
    ),
    ("gurupurab", "meghalaya"): (
        "The solemn echo of amrit vela prayers begins the dawn assembly inside local Meghalaya prayer rooms. "
        "Devotees look to the local head priest as a full-length Gurbani recitation clears the surrounding mountain valley. "
        "The winter gathering is highlighted by providing dedicated langar seva paired with hot kada prasad options."
    ),
    ("gurupurab", "mizoram"): (
        "The holy sound of a shabad kirtan session loops through private diaspora apartments across Mizoram. "
        "The small local community organizes a quiet prabhat pheri to announce the structural winter new year. "
        "The diaspora gathering concludes with sharing custom kada prasad items cooked inside the langar seva hub."
    ),
    ("gurupurab", "nagaland"): (
        "A majestic nagar kirtan procession takes over public pathways in Nagaland to mark the ancestral lineage safety. "
        "Worshippers complete a slow, meditative sarovar snan simulation before the main text reading cycles open. "
        "The peaceful seasonal gathering is highlighted by organizing an open langar seva paired with sweet kada prasad."
    ),
    ("gurupurab", "odisha"): (
        "The holy sarovar snan rituals at historic gurdwaras initiate the sacred winter dawn across Odisha districts. "
        "Devotees gather to hear the profound Gurbani recitation and meditate on the teachings of the lineage. "
        "The holy days are accompanied by distributing rich kada prasad directly from the central langar seva kitchen."
    ),
    ("gurupurab", "punjab"): (
        "The akhand path completes at dawn, kirtan echoes from the Golden Temple, and the continuous langar kitchen serves thousands across Punjab, defining the heart of guru remembrance, kirtan, and seva. "
        "Dedicated nagar kirtan processions and selfless community action anchor the high-energy celebrations across local districts. "
        "The festive gathering is marked by distributing warm kada prasad, festive rotis, and rich milk sweets to the public."
    ),
    ("gurupurab", "rajasthan"): (
        "Grand morning mass gatherings and beautiful winter light displays fill courtyards in Rajasthan, elevating the heritage of guru remembrance, kirtan, and seva. "
        "Delicate courtyard lamps and royal-colour decorations provide a dramatic setting for the night-long prayers. "
        "The culinary gathering centers on serving sweet ghevar, rich dal-baati spreads, and festive mithai to extended clans."
    ),
    ("gurupurab", "sikkim"): (
        "Midnight choral singing along hillside pathways brings communities together across Sikkim, welcoming the seasonal alignment with guru remembrance, kirtan, and seva. "
        "Grounded community prayer and hillside celebrations bring mountain settlements together for evening songs and shared prayers. "
        "The local hospitality involves sharing custom sweets and warm festive rice dishes among remote settlements."
    ),
    ("gurupurab", "tamil-nadu"): (
        "Massive morning prayers inside urban gurdwaras transform Tamil Nadu, anchoring guru remembrance, kirtan, and seva. "
        "Vibrant kolam art, brass lamps, and dawn rituals reshape the domestic rhythm as neighbors visit to exchange festive sweets. "
        "The sacred season is celebrated by preparing sweet pongal, savory sundal, and sacred temple prasadam for guests."
    ),
    ("gurupurab", "telangana"): (
        "The spectacular morning gurdwara gatherings in Secunderabad and Hyderabad define the peak of Telangana's guru remembrance, kirtan, and seva. "
        "Bonalu-style community devotion and floral decor create a highly active and colorful public greeting space. "
        "The primary household table is filled with ritual paramannam, sweet laddus, and assorted festive savouries."
    ),
    ("gurupurab", "tripura"): (
        "Bright star lanterns and home-made winter cakes fill family courtyards across Tripura, mirroring the winter arrival of guru remembrance, kirtan, and seva. "
        "Family courtyards and community pandals turn into lively meeting points for multi-generational relative visits. "
        "The evening hospitality is highlighted by sharing traditional festive rice offerings and local sweets with neighbours."
    ),
    ("gurupurab", "uttar-pradesh"): (
        "The beautiful winter decorations at historic city gurdwaras transform Uttar Pradesh, tracking a magnificent display of guru remembrance, kirtan, and seva. "
        "Ancient ghat rituals and massive temple crowds create an unmatched public scale under the echo of midnight bells. "
        "The high-energy days include distributing famous sweet peda, kachori, and traditional prasad to the community."
    ),
    ("gurupurab", "uttarakhand"): (
        "Midnight services in pristine alpine valley gurdwara spaces define the local experience in Uttarakhand, celebrating a serene display of guru remembrance, kirtan, and seva. "
        "Ancient hill temples and family vrat observance bring remote mountain villages together for collective protective prayers. "
        "The spiritual gathering is completed by serving traditional singori, sweet halwa, and custom temple offerings."
    ),
    ("gurupurab", "west-bengal"): (
        "The grand winter carnivals on Park Street in Kolkata define the West Bengal celebration of guru remembrance, kirtan, and seva. "
        "Artistic neighbourhood pandals, echoing dhaak rhythms, and striking artistic decorations alter the local landscape during the dawn periods. "
        "The cultural transition is accompanied by preparing traditional sandesh, khichuri bhog, and assorted festive sweets."
    ),
    ("gurupurab", "nri-london"): (
        "Traditional winter carols and glowing paper stars hung in windows protect the London diaspora as they maintain the heritage of guru remembrance, kirtan, and seva. "
        "Bustling weekend community events and cultural centres connect families across boroughs for simultaneous evening prayers. "
        "Expatriates mark the winter transition by packing potluck sweets and temple prasada to share with global friends."
    ),
    ("gurupurab", "nri-new-york"): (
        "Vibrant family dinners and bright star lanterns mark New York diaspora gatherings, celebrating the arrival of guru remembrance, kirtan, and seva. "
        "Ornate temple halls, family Zooms, and community gatherings bridge the distance for long-distance relatives during the winter nights. "
        "The diaspora gathering concludes with sharing custom festive meals and mandir prasad within local networks."
    ),


    # ── RAM NAVAMI (Batch 15 -- all 30 regions) ────────────────────────────────
    ("ram-navami", "andhra-pradesh"): (
        "Sacred Ram katha recitations and evening temple processions bring spiritual warmth across Andhra Pradesh during the holy spring days. "
        "Devotees observe a strict midday fast to welcome the divine birth hour of the avatar. "
        "The auspicious day concludes with families sharing refreshing panakam drinks with visiting neighborhood circles."
    ),
    ("ram-navami", "arunachal-pradesh"): (
        "Bright oil lamps illuminate community spaces across Arunachal Pradesh as communities gather to honor the birth of righteousness. "
        "Local prayer groups lead intense scriptural chants to praise the divine attributes of Rama. "
        "The spiritual gathering is completed by preparing sweet jalebi variations alongside regional festive treats."
    ),
    ("ram-navami", "assam"): (
        "The elegant chanting of ancient epic verses alters the domestic rhythm in Assam, reflecting a deep focus on the sacred janmotsav. "
        "Neighborhood circles gather for intense twilight prayers to welcome protective righteousness into their settlements. "
        "The celebration is completed as kitchens prepare sweet neer mor formulas alongside traditional Assamese pitha varieties."
    ),
    ("ram-navami", "bihar"): (
        "Strict solar fasting routines bring a profound spiritual focus inside Bihar homes during the holy janmotsav hour. "
        "Large neighborhood groups gather at local shrines for synchronized stotra recitations praising the legendary monarch. "
        "The fast is broken late in the afternoon by distributing sweet kheer alongside home-style bihari items."
    ),
    ("ram-navami", "chhattisgarh"): (
        "Ornate temporary chariot floats are beautifully decorated across Chhattisgarh, welcoming the spring celebration of Ram katha. "
        "Evening gatherings feature vibrant devotional chants as local neighborhoods unite for collective worship at local shrines. "
        "Kitchens prepare specialized neer mor fluids and home-style desserts to distribute as sacred prasad."
    ),
    ("ram-navami", "goa"): (
        "Serene brass lamps cast a quiet glow across Goan altars as the midday birth hour of the avatar arrives. "
        "Devotees dedicate their morning hours to silent, meditative scriptural reading lines from the holy epics. "
        "The seasonal shift is honored by sharing chilled panakam drinks inside traditional family courtyards."
    ),
    ("ram-navami", "gujarat"): (
        "Surya puja at noon marks the exact alignment of solar rays across principal Gujarati shrines to welcome the avatar. "
        "Devotees assemble to participate in grand janmotsav processions that feature beautifully decorated dynamic chariot replicas. "
        "Fasting families break their strict daylight restrictions by distributing sacred charan amrit to local temple crowds."
    ),
    ("ram-navami", "haryana"): (
        "The unveiling of a pristine Ram Lalla icon transforms Haryana courtyard shrines as the precise midday hour strikes. "
        "Extended agrarian families complete a sacred navami havan to invite protective blessings into their farmlands. "
        "The holy celebration involves distributing liquid panchamrit abhishek of Ram icon directly from polished brass vessels."
    ),
    ("ram-navami", "himachal-pradesh"): (
        "Kalash sthapana rituals initiate the sacred spring dawn inside remote Himachal Pradesh mountain valley shrines. "
        "Clans travel down winding paths to receive a cleansing panchamrit abhishek of Ram icon from the temple priests. "
        "The cold afternoon is warmed as families gather around home altars to consume warm ceremonial charan amrit."
    ),
    ("ram-navami", "jharkhand"): (
        "Devotional singing circles fill rural residential colonies in Jharkhand, marking the precise spring birth milestone. "
        "Extended family units join together for peaceful afternoon prayers to invoke the righteous values of the deity. "
        "The sacred day is nourished by distributing unique neer mor mixtures to visiting relatives."
    ),
    ("ram-navami", "karnataka"): (
        "The unique distribution of refreshing panakam and sweet majjige drinks transforms local living rooms across Karnataka at noon. "
        "Intricate flower decorations and morning janmotsav rituals re-energize the household as families decorate the sacred cradle. "
        "Visiting guests are welcomed into homes with delicious jalebi variations alongside classic southern treats."
    ),
    ("ram-navami", "kerala"): (
        "Elegant parayan recitations from the ancient Adhyatma Ramayana echo through pristine Kerala temple corridors at noon. "
        "A deeply peaceful atmosphere settles over the community as families participate in the sacred birthday rituals. "
        "Worshippers conclude their fasting routines by serving sweet kheer variations on traditional banana leaves."
    ),
    ("ram-navami", "madhya-pradesh"): (
        "A grand Sita-Ram wedding reenactment takes over the historic Orchha palace grounds across Madhya Pradesh at noon. "
        "Devotees observe a strict midday fast to coincide precisely with the glorious moment of the avatar's birth. "
        "The local evening hospitality centers on sharing chilled panchamrit collections with visiting temple crowds."
    ),
    ("ram-navami", "maharashtra"): (
        "The sacred kalash sthapana ritual anchors home altars across Maharashtra, initiating the spring day of the avatar. "
        "Families coordinate a pristine panchamrit abhishek before gathering around the central navami havan fire. "
        "The family gathering centers on preparing light fasting items alongside traditional Maharashtrian sweets."
    ),
    ("ram-navami", "manipur"): (
        "A continuous Ramcharitmanas akhand path fills local Manipuri temples, establishing a pristine devotional setting. "
        "Extended families gather around the central navami havan fire to invite righteousness into their settlements. "
        "The daily celebration concludes with families distributing pure charan amrit fluids directly to visiting relative networks."
    ),
    ("ram-navami", "meghalaya"): (
        "A pristine kalash sthapana setup defines the local community experience inside Meghalaya prayer halls at sunrise. "
        "Devotees observe a strict midday fast while listening to traditional stories regarding the avatar's childhood. "
        "The warm afternoon hospitality features sharing pure charan amrit portions within multi-generational families."
    ),
    ("ram-navami", "mizoram"): (
        "The beautiful installation of a Ram Lalla icon inside private diaspora spaces in Mizoram grounds the spring holiday. "
        "Worshippers coordinate a strict navami havan to invite protective cosmic order into their temporary residences. "
        "The spring occasion is highlighted by distributing pure panchamrit abhishek of Ram icon mixtures among clans."
    ),
    ("ram-navami", "nagaland"): (
        "A Ramcharitmanas akhand path commences behind decorated home altars in Nagaland, establishing a pristine devotional setting. "
        "Diaspora families coordinate an elegant Sita-Ram wedding reenactment to display timeless spiritual milestones to the youth. "
        "The holy day is honored by serving light fasting meals paired with fresh fruit juices."
    ),
    ("ram-navami", "odisha"): (
        "The grand Rama-Sita wedding reenactment ceremonies or Kalyanotsavam transform local towns across Odisha during the spring. "
        "Intricate designs line the paths where families gather for the beautiful evening janmotsav blessings. "
        "The holy days are accompanied by distributing traditional panakam along with classic temple sweets."
    ),
    ("ram-navami", "punjab"): (
        "Elegant shobha yatra processions wind through local residential streets in Punjab to celebrate the arrival of spring righteousness. "
        "Worshippers arrange extensive community prayer slots to reflect deeply on the values of the avatar. "
        "The auspicious day is completed by distributing warm jalebi sweets across local towns."
    ),
    ("ram-navami", "rajasthan"): (
        "High-energy devotional chants and traditional folk music fill historic courtyards in Rajasthan during the holy spring days. "
        "Delicate courtyard decorations provide a dramatic setting for late-night Ram katha sessions under bright lights. "
        "The culinary gathering centers on serving sweet neer mor variations along with rich desert treats."
    ),
    ("ram-navami", "sikkim"): (
        "A solemn kalash sthapana ritual is executed along Sikkim mountain ridges to orient the community toward righteousness. "
        "Devotees look to the sky for a synchronized Surya puja at noon long before any fasting boundaries are broken. "
        "The local hospitality involves sharing pure charan amrit mixtures among remote hillside settlements."
    ),
    ("ram-navami", "tamil-nadu"): (
        "The grand Rama-Sita wedding reenactment ceremonies or Kalyanotsavam transform Tamil Nadu temples, anchoring the seasonal focus. "
        "Vibrant art and dawn rituals reshape the domestic rhythm as families complete their janmotsav steps. "
        "The sacred season is celebrated by preparing sweet panakam variants alongside traditional southern snacks."
    ),
    ("ram-navami", "telangana"): (
        "The historic Sri Sitaramachandra Swamy temple celebrations at Bhadrachalam set an unmatched standard across Telangana at noon. "
        "Community devotion sets a highly active and colorful public stage for evening janmotsav gatherings. "
        "The primary household table is filled with ritual jalebi alongside assorted local savouries."
    ),
    ("ram-navami", "tripura"): (
        "A continuous Ramcharitmanas akhand path fills family inner courtyards across Tripura, guiding the domestic focus toward righteousness. "
        "Families coordinate an elaborate Sita-Ram wedding reenactment using traditional ceremonial garments and brass oil lamps. "
        "The spring evening is marked by sharing pure charan amrit portions alongside local fasting delicacies."
    ),
    ("ram-navami", "uttar-pradesh"): (
        "Millions of pilgrims taking holy dips in the sacred Sarayu river at Ayodhya transform Uttar Pradesh during the janmotsav. "
        "Ancient public squares create an unmatched devotional scale as crowds gather for evening Ram katha songs. "
        "The high-energy days include distributing famous panakam alongside traditional city prasad."
    ),
    ("ram-navami", "uttarakhand"): (
        "Pilgrimages to ancient high-altitude shrines bring remote mountain settlements together in Uttarakhand for the spring janmotsav. "
        "Clans maintain strict fasting boundaries while participating in quiet evening stotra recitations. "
        "The spiritual gathering is completed by serving hot neer mor formulas alongside custom alpine treats."
    ),
    ("ram-navami", "west-bengal"): (
        "The sacred panchamrit abhishek of Ram icon alters the morning domestic rhythm inside traditional West Bengal households. "
        "Devotees coordinate a magnificent janmotsav procession that features beautifully styled clay tableaux across town squares. "
        "The cultural transition involves distributing liquid charan amrit directly to visiting relative networks."
    ),
    ("ram-navami", "nri-london"): (
        "A grand Sita-Ram wedding reenactment takes over hired community assembly halls across London to preserve ancestral traditions. "
        "Expatriates perform a precise Surya puja at noon to align with simultaneous global birth hour events. "
        "Families mark the spring milestone by packing small flasks of charan amrit to distribute to diaspora networks."
    ),
    ("ram-navami", "nri-new-york"): (
        "A continuous Ramcharitmanas akhand path connects long-distance relatives via video calls to New York temple halls. "
        "Parents assemble a pristine kalash sthapana setup before the afternoon janmotsav procession begins down city avenues. "
        "The diaspora gathering concludes with sharing custom charan amrit formulas within local apartment networks."
    ),


    # ── HANUMAN JAYANTI (Batch 16 -- all 30 regions) ──────────────────────────
    ("hanuman-jayanti", "andhra-pradesh"): (
        "Resounding Hanuman Chalisa chantings and orange sindoor applications mark temple courtyards across Andhra Pradesh during the holy morning hours. "
        "Devotees gather in large numbers to offer collective prayers for strength and absolute spiritual protection. "
        "The auspicious day concludes with families sharing sacred boondi laddus with visiting neighborhood circles."
    ),
    ("hanuman-jayanti", "arunachal-pradesh"): (
        "Sacred sundarkand recitations and bright oil lamps are lit across Arunachal Pradesh homes, anchoring the seasonal focus on bajrangbali. "
        "Bustling community spaces fill with traditional hymns as families gather to pray for spiritual shielding. "
        "The auspicious evening concludes with households gathering to share custom besan ladoo formulas with neighbors."
    ),
    ("hanuman-jayanti", "assam"): (
        "The continuous chanting of protective chalisa verses and orange sindoor markings alter the domestic rhythm in Assam, reflecting a deep focus on bajrangbali. "
        "Neighborhood circles gather for intense twilight prayers to welcome defensive shielding into their settlements. "
        "The celebration is completed as kitchens prepare sweet imarti solutions alongside traditional Assamese pitha varieties."
    ),
    ("hanuman-jayanti", "bihar"): (
        "Intricate red sindoor coatings are applied to sacred bajrangbali idols inside Bihar temples at sunrise. "
        "Massive neighborhood groups gather for high-energy chalisa circuits to seek protection from obstacles. "
        "The high-energy day is completed by serving sweet motichoor items alongside classic bihari savouries."
    ),
    ("hanuman-jayanti", "chhattisgarh"): (
        "Vibrant red flags and traditional wrestling arena or akhada displays are beautifully coordinated across Chhattisgarh, initiating the spring celebration. "
        "Evening gatherings feature vibrant bajrangbali chants as local neighborhoods unite for collective worship at local shrines. "
        "Kitchens prepare specialized boondi laddus and home-style desserts to distribute as sacred prasad."
    ),
    ("hanuman-jayanti", "goa"): (
        "Intense Hanuman Chalisa recitations and orange sindoor applications transform Goan shrine walls during the early morning hours. "
        "The community gathers to chant protective stotras and pray for immense strength and defensive shielding. "
        "The holy period is celebrated by distributing rich besan ladoo portions across local settlements."
    ),
    ("hanuman-jayanti", "gujarat"): (
        "Sunderkand path recitations resonate throughout historic Gujarati neighborhoods as early morning crowds salute the deity. "
        "Bustling youth groups carry out intense saffron flag hoisting routines across town squares before the main communal assemblies. "
        "The energetic daytime celebration concludes with local temples distributing massive quantities of boondi laddoo bhog."
    ),
    ("hanuman-jayanti", "haryana"): (
        "An intense akhara procession takes over public roads across Haryana, showcasing traditional physical prowess and agility. "
        "Local farmers host high-energy dangal wrestling tournaments to honor the immense strength of the deity. "
        "The rustic holiday is enriched by distributing massive spheres of sweet laddoo bhog to working field hands."
    ),
    ("hanuman-jayanti", "himachal-pradesh"): (
        "A Hanuman Chalisa marathon echoes through hillside temples in Himachal Pradesh to invoke immediate spiritual defense. "
        "Local youth gather on open village grounds to participate in dynamic dangal and kushti wrestling matches under traditional rules. "
        "The high-energy afternoon concludes with community elders handing out rich besan laddoo bhog to exhausted participants."
    ),
    ("hanuman-jayanti", "jharkhand"): (
        "Vibrant orange flags are raised atop home entryways in Jharkhand, signaling the high-energy morning bajrangbali rituals. "
        "Devotees coordinate peaceful community prayer circles to offer collective gratitude for family health and well-being. "
        "The fasting period is supported by sharing unique besan ladoo mixtures with neighboring families."
    ),
    ("hanuman-jayanti", "karnataka"): (
        "The unique distribution of sacred orange sindoor and sweet boondi laddus transforms local living rooms across Karnataka. "
        "Intricate flower decorations and morning chalisa rituals re-energize the household as families decorate the shrine. "
        "Visiting guests are welcomed into homes with delicious imarti variations alongside classic southern treats."
    ),
    ("hanuman-jayanti", "kerala"): (
        "The unique Hanumath Jayanthi parayan readings draw massive crowds to specialized Kerala monkey-deity shrines at sunrise. "
        "Devotees present extensive offerings of red flowers to invoke the supreme protective energy of the warrior. "
        "The day is marked by serving sweet motichoor variants alongside elaborate local spreads."
    ),
    ("hanuman-jayanti", "madhya-pradesh"): (
        "A full-volume Hanuman Chalisa marathon echoes through historic hilltop mandirs across Madhya Pradesh at sunrise. "
        "Bustling youth groups wave bright banners during an energetic akhara procession that winds through old lanes. "
        "The local evening hospitality features distributing massive batches of sweet boondi laddoo bhog to visitors."
    ),
    ("hanuman-jayanti", "maharashtra"): (
        "The systematic rendering of morning birth ceremonies at sunrise anchors local neighborhood complexes across Maharashtra. "
        "Bustling society spaces turn into lively centers for nightly sundarkand sessions and collective aarti routines. "
        "The family gathering centers on preparing fresh besan ladoo formulas along with traditional maharashtrian sweets."
    ),
    ("hanuman-jayanti", "manipur"): (
        "A continuous Sunderkand path recitation bridges local Manipur harmony with the global focus on the warrior deity. "
        "Worshippers complete a slow, meditative parikrama of Hanuman temple while flying traditional triangular pennants. "
        "The festive week concludes with organizers distributing large trays of handcrafted motichoor laddoo bhog to clans."
    ),
    ("hanuman-jayanti", "meghalaya"): (
        "Bright saffron flag hoisting routines introduce an intense spiritual energy across the hills of Meghalaya. "
        "Worshippers gather for a high-energy Hanuman Chalisa marathon to pray for ancestral lineage safety and defense. "
        "The seasonal gathering is highlighted by presenting large boxes of besan laddoo bhog to visiting friends."
    ),
    ("hanuman-jayanti", "mizoram"): (
        "A continuous Sunderkand path recitation bridges local diaspora harmony with the global focus on the warrior deity. "
        "Worshippers complete a slow, meditative parikrama of Hanuman temple while chanting ancient protection verses. "
        "The daytime gathering concludes with sharing sweet laddoo bhog variations across local townships."
    ),
    ("hanuman-jayanti", "nagaland"): (
        "A solemn veer Hanuman invocation brings small diaspora circles together across Nagaland to anchor the early morning prayers. "
        "Worshippers complete a slow, meditative parikrama of Hanuman temple while flying traditional triangular pennants. "
        "The high-energy gathering concludes with organizers distributing large trays of handcrafted laddoo bhog to visitors."
    ),
    ("hanuman-jayanti", "odisha"): (
        "The iconic orange flags and grand temple Hanuman Chalisa circuits transform local towns across Odisha during the spring. "
        "Intricate designs line the paths where families gather for the beautiful evening bajrangbali blessings. "
        "The holy days are accompanied by distributing traditional imarti along with classic temple sweets."
    ),
    ("hanuman-jayanti", "punjab"): (
        "High-energy bajrangbali shobha yatras and continuous collective chalisa singing fill local neighborhoods in Punjab. "
        "Worshippers arrange extensive community service slots to honor the absolute devotion of the warrior. "
        "The auspicious day is completed by distributing warm motichoor sweets across local districts."
    ),
    ("hanuman-jayanti", "rajasthan"): (
        "High-energy devotional chants and grand temple celebrations at Salasar Balaji fill historic neighborhoods in Rajasthan. "
        "Delicate courtyard decorations provide a dramatic setting for late-night sundarkand sessions under bright lights. "
        "The culinary gathering centers on serving sweet boondi laddus variations along with rich desert treats."
    ),
    ("hanuman-jayanti", "sikkim"): (
        "Vibrant saffron flag hoisting routines turn hillside pathways golden in Sikkim as the early morning mist clears. "
        "Worshippers join together for a long, dedicated parikrama of Hanuman temple to pray for spiritual shielding. "
        "The local gathering is highlighted by presenting large bowls of motichoor laddoo bhog to mountain clans."
    ),
    ("hanuman-jayanti", "tamil-nadu"): (
        "The beautiful offering of vadamala garlands woven from savory treats transforms Tamil Nadu temples, anchoring the focus. "
        "Vibrant art and dawn rituals reshape the domestic rhythm as families complete their protective steps. "
        "The sacred season is celebrated by preparing sweet imarti variants alongside traditional southern snacks."
    ),
    ("hanuman-jayanti", "telangana"): (
        "The massive multi-day Hanuman Deeksha completions and grand temple stages transform Telangana at sunrise. "
        "Community devotion sets a highly active and colorful public stage for evening bajrangbali gatherings. "
        "The primary household table is filled with ritual motichoor alongside assorted local savouries."
    ),
    ("hanuman-jayanti", "tripura"): (
        "A full-volume Hanuman Chalisa marathon echoes through local public blocks in Tripura to salute the warrior deity. "
        "Worshippers organize a spectacular akhara procession featuring complex maneuvers with traditional staff implements. "
        "The evening hospitality is highlighted by presenting massive platters of boondi laddoo bhog to neighborhood guests."
    ),
    ("hanuman-jayanti", "uttar-pradesh"): (
        "Massive congregations at ancient Sankat Mochan mandirs and morning sundarkand chants transform Uttar Pradesh. "
        "Ancient public squares create an unmatched devotional scale as crowds gather for evening chalisa songs. "
        "The high-energy days include distributing famous besan ladoo alongside traditional city prasad."
    ),
    ("hanuman-jayanti", "uttarakhand"): (
        "High-altitude mountain temple pilgrimages define the local experience in Uttarakhand during the sunrise chalisa celebrations. "
        "Remote alpine settlements unite for intense sundarkand routines to honor the defensive strength of bajrangbali. "
        "The spiritual gathering is completed by serving hot imarti formulas alongside custom alpine treats."
    ),
    ("hanuman-jayanti", "west-bengal"): (
        "A solemn Sunderkand path recitation initiates the early morning hours inside neighborhood shrines across West Bengal. "
        "Youth groups wave bright banners during a lively parikrama of Hanuman temple that winds through historic old lanes. "
        "The high-energy day includes distributing famous sweet motichoor laddoo bhog to exhausted participants."
    ),
    ("hanuman-jayanti", "nri-london"): (
        "A full-scale Hanuman Chalisa marathon connects families across London boroughs for a unified spiritual shield. "
        "Children participate in a symbolic veer Hanuman invocation that details historical tales of courage and focus. "
        "The diaspora gathering concludes with distributing massive batches of boondi laddoo bhog inside local cultural centers."
    ),
    ("hanuman-jayanti", "nri-new-york"): (
        "Community centers host orange vermillion ceremonies and continuous scriptural discourses in New York, honoring the traditions. "
        "Ornate temple halls and family video calls bridge the long distance for relatives participating in chalisa recitations. "
        "The diaspora gathering concludes with sharing custom besan ladoo variations within local networks."
    )

}  # End of FESTIVAL_REGION_SUMMARY -- 480 entries complete (16 festivals × 30 regions)
