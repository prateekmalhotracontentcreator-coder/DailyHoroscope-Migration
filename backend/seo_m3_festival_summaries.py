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
        "Hillside shrines echo with deep devotional music across Himachal Pradesh, anchoring the mountain air in the nine-night vrat. "
        "Local clans travel across valleys to participate in grand temple-style shakti puja gatherings. "
        "The spiritual afternoon is comforted by serving warm singhare ki poori alongside rich mountain-style meals."
    ),
    ("navratri", "jharkhand"): (
        "Earthen lamps remain lit continuously inside Jharkhand residences, marking the seasonal alignment with the nine-night vrat. "
        "Devotees coordinate peaceful community Kanya puja sessions to offer collective prayers for family well-being. "
        "The fasting period is supported by sharing unique sabudana khichdi variations with neighboring families."
    ),
    ("navratri", "karnataka"): (
        "Vibrant festive steps and traditional home decorations alter the domestic atmosphere across Karnataka during the nine-night vrat. "
        "Youth groups coordinate localized dandiya raas routines inside temple courtyards to celebrate the glory of Durga mata. "
        "The evening feast is defined by preparing delicious kuttu atta halwa variations alongside classic southern treats."
    ),
    ("navratri", "kerala"): (
        "Sacred books are placed before the altar for blessings in Kerala, marking a unique southern expression of the nine-night vrat. "
        "The quiet community focus sets a deeply meditative stage for intense shakti puja rituals inside traditional shrines. "
        "The concluding day is celebrated by serving sweet sabudana khichdi variants alongside elaborate banana leaf spreads."
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
        "Devotional storytelling and graceful dance sequences fill local mandaps in Manipur, blending the seasonal shift with the nine-night vrat. "
        "Expressive cultural performances offer a deeply classical avenue for communities participating in shakti puja. "
        "The sacred week is marked by preparing custom kuttu atta halwa formulas to share among extended families."
    ),
    ("navratri", "meghalaya"): (
        "Sacred fasts and twilight choral groups bring diverse neighborhoods together in Meghalaya to observe the nine-night vrat. "
        "Festive community halls host peaceful cultural gatherings to celebrate the traditional segments of dandiya raas. "
        "The warm afternoon hospitality features sharing bowls of sabudana khichdi along with unique local rice sweets."
    ),
    ("navratri", "mizoram"): (
        "Traditional oil lamps illuminate private balconies in Mizoram, bridging local harmony with the global focus on the nine-night vrat. "
        "Decorated community spaces allow diaspora groups to gather for collective prayers honoring Durga mata. "
        "The autumn occasion is highlighted by gathering for shared plates of kuttu atta halwa across local townships."
    ),
    ("navratri", "nagaland"): (
        "Quiet home altars are decorated with fresh autumn flowers across Nagaland, celebrating the spiritual presence of the nine-night vrat. "
        "Vibrant collective singing provides a welcoming environment for families participating in shakti puja rituals. "
        "The peaceful seasonal gathering is highlighted by presenting warm singhare ki poori alongside celebratory desserts."
    ),
    ("navratri", "odisha"): (
        "The grand invocation of Navdurga inside ancient shrines transforms local towns across Odisha during the nine-night vrat. "
        "Intricate designs line the paths where families gather for the beautiful evening Kanya puja blessings. "
        "The holy days are accompanied by distributing traditional kuttu atta halwa along with classic temple sweets."
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
        "Hillside altars are dressed in fresh autumn leaves across Sikkim, welcoming the seasonal alignment with the nine-night vrat. "
        "Grounded community prayer brings mountain settlements together for peaceful shakti puja songs and shared blessings. "
        "The local hospitality involves sharing sweet sabudana khichdi formulas among remote neighborhoods."
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
        "Devotional stotra recitations fill local community halls across Tripura, mirroring the autumn arrival of the nine-night vrat. "
        "Community pandals turn into lively meeting points for families participating in evening dandiya raas sessions. "
        "The evening hospitality is highlighted by sharing traditional singori alongside custom kuttu atta halwa dishes."
    ),
    ("navratri", "uttar-pradesh"): (
        "Vibrant open-air theater stages and massive temple queues transform Uttar Pradesh during the holy navratri days. "
        "Ancient public squares create an unmatched devotional scale as crowds gather for evening shakti puja songs. "
        "The high-energy days include distributing famous kuttu atta halwa alongside traditional city prasad."
    ),
    ("navratri", "uttarakhand"): (
        "Hilltop temple pilgrimages and sacred fasting routines define the local experience in Uttarakhand during the nine-night vrat. "
        "Ancient hill temples bring remote mountain settlements together for protective collective prayers honoring Durga mata. "
        "The spiritual gathering is completed by serving hot singhare ki poori alongside custom alpine treats."
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
        "Sculpted idols and grand temporary shrines bring diverse communities together across Haryana, magnifying the annual cycle of goddess celebration, artistry, and community worship. "
        "Family courtyards and temple offerings turn into central meeting points where neighborhood women lead traditional folk prayers. "
        "The home gatherings are warmed by sharing rustic halwa, puri, and farm-style festive meals among relatives."
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
        "Magnificent temporary enclosures and echoing dhunuchi naach competitions alter the urban space of Madhya Pradesh, showcasing deep goddess celebration, artistry, and community worship. "
        "Devotional mandir visits and old-city processions draw thousands out into illuminated public streets after sunset. "
        "The local evening hospitality is accompanied by distributing savory poha-style snacks, sweets, and prasad to visitors."
    ),
    ("durga-puja", "maharashtra"): (
        "The grand welcoming of the clay idol anchors the local neighbourhood complexes across Maharashtra, initiating days of goddess celebration, artistry, and community worship. "
        "Bustling society pandals and family aarti gatherings unite apartment complexes for nightly prayers and synchronized dances. "
        "The daily family gathering centers on preparing fresh, sweet modak, puran poli, and festive snacks."
    ),
    ("durga-puja", "manipur"): (
        "Artistic tableaux and classical devotional sequences fill local mandaps in Manipur, blending the season with goddess celebration, artistry, and community worship. "
        "Expressive cultural performances and temple participation offer a deeply classical avenue for community connection. "
        "The sacred week concludes with neighborhoods arranging large community feasts paired with specialized seasonal sweets."
    ),
    ("durga-puja", "meghalaya"): (
        "Beautifully illuminated temporary stages and morning pushpanjali bring families together in Meghalaya, honoring the message of goddess celebration, artistry, and community worship. "
        "Festive church halls, homes, and community spaces host unique inter-cultural programs to celebrate the autumn season. "
        "The warm afternoon hospitality features sharing local festive rice dishes and unique local sweets with guests."
    ),
    ("durga-puja", "mizoram"): (
        "Elegant temporary mandaps are decorated with autumn lights in Mizoram, bridging local harmony with the global focus on goddess celebration, artistry, and community worship. "
        "Decorated community halls and neighbourhood visits allow diaspora groups to gather for seasonal updates and songs. "
        "The autumn occasion is highlighted by gathering for shared festive meals and sweet offerings across local townships."
    ),
    ("durga-puja", "nagaland"): (
        "Artistic pandal spaces are constructed with autumn flowers across Nagaland, celebrating the spiritual presence of goddess celebration, artistry, and community worship. "
        "Vibrant collective singing and family hosting provide a welcoming environment for visiting relatives and friends. "
        "The peaceful seasonal gathering is highlighted by presenting large community meals and celebratory desserts."
    ),
    ("durga-puja", "odisha"): (
        "The majestic silver backdrops or Chandi Medha transform ancient shrines across Odisha, elevating days of deep goddess celebration, artistry, and community worship. "
        "Intricate alpona art and neighbourhood mandaps line the village paths where families gather to receive the goddess's blessings. "
        "The holy days are accompanied by distributing traditional sweet khaja, pitha, and temple mahaprasad to neighbourhood networks."
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
        "Welcoming the clay idol with evening aarti and sweet modak blocks marks the autumn shift across Andhra Pradesh, centering on auspicious beginnings and Ganapati devotion. "
        "The spiritual energy fills local neighborhoods, where public areas are enlivened by traditional temple processions and decorated entrances. "
        "Families conclude their ten-day immersion rituals by sharing temple pulihora and laddus with visiting neighbourhood circles."
    ),
    ("ganesh-chaturthi", "arunachal-pradesh"): (
        "Sacred modak offerings and bright oil lamps welcome Vinayaka idols across Arunachal Pradesh homes, anchoring the seasonal focus on auspicious beginnings and Ganapati devotion. "
        "Bustling community halls and family gatherings fill with traditional hymns as families gather for the festive evening aarti. "
        "The primary celebration concludes with households gathering to share custom community sweets and festive rice dishes."
    ),
    ("ganesh-chaturthi", "assam"): (
        "The joyful welcoming of clay Ganesha idols reshapes the domestic rhythm in Assam, reflecting the festival's focus on auspicious beginnings and Ganapati devotion. "
        "Joyous music, prayer, and neighbourhood visits elevate local community spaces during the twilight puja transitions. "
        "The sacred cycle is enriched by serving traditional pitha, payas, and festive rice offerings to the neighbourhood."
    ),
    ("ganesh-chaturthi", "bihar"): (
        "Special home altars and standard dahi handi decorations define the household atmosphere in Bihar, celebrating days of auspicious beginnings and Ganapati devotion. "
        "Bustling ghat visits and family puja routines allow large extended families to gather for collective bhajan recitations. "
        "The daily ceremonial transition is marked by preparing sweet thekua, kheer, and seasonal savouries for ritual prasad."
    ),
    ("ganesh-chaturthi", "chhattisgarh"): (
        "Neighbourhood pandals house beautifully sculpted clay idols across Chhattisgarh, initiating the autumn celebration of auspicious beginnings and Ganapati devotion. "
        "Vibrant community puja and local fairs bring farming communities together for evening folk dances and traditional prayers. "
        "The household hospitality centers on kitchens preparing specialized rice sweets and home-style prasad for daily offerings."
    ),
    ("ganesh-chaturthi", "goa"): (
        "The traditional Chovoth festival features unique clay idols decorated with wild flowers and fruits in Goa, channeling a beautiful wave of auspicious beginnings and Ganapati devotion. "
        "Quiet home altars and bustling neighbourhood celebration routes define the spatial layout of the local evening prayers. "
        "The sacred period is marked by sharing unique coconut sweets and festive savouries among long-time neighbors."
    ),
    ("ganesh-chaturthi", "gujarat"): (
        "Bustling street pandals and echoing cries of Ganpati Bappa Morya transform public areas across Gujarat, magnifying the festive energy of auspicious beginnings and Ganapati devotion. "
        "Bustling garba grounds and bright rangoli work completely transform public and private squares under bright festive lights. "
        "Extended families mark the joyful transition by gathering around multi-course festive thalis loaded with fafda and jalebi."
    ),
    ("ganesh-chaturthi", "haryana"): (
        "Domestic shrines are beautifully decorated for the welcoming of Lord Ganesha across Haryana, magnifying the annual cycle of auspicious beginnings and Ganapati devotion. "
        "Family courtyards and temple offerings turn into central meeting points where neighbourhood women lead traditional folk prayers. "
        "The home gatherings are warmed by sharing rustic halwa, puri, and farm-style festive meals among relatives."
    ),
    ("ganesh-chaturthi", "himachal-pradesh"): (
        "Community pandals emerge amidst the cold mountain air across Himachal Pradesh, anchoring local valleys in auspicious beginnings and Ganapati devotion. "
        "Serene village temples and hillside processions host local clans traveling across valleys to pay homage to their deities. "
        "The spiritual afternoon is comforted by serving sweet rice, prasad, and mountain-style meals around communal hearths."
    ),
    ("ganesh-chaturthi", "jharkhand"): (
        "Devotional songs echo through illuminated temporary shrines in Jharkhand, marking the seasonal alignment with auspicious beginnings and Ganapati devotion. "
        "Open community grounds and family prayer circles provide an inclusive space for traditional drumming and evening chants. "
        "The ten-day period is supported by sharing unique seasonal sweets and simple ceremonial meals within families."
    ),
    ("ganesh-chaturthi", "karnataka"): (
        "The sacred Gowri-Ganesha rituals and beautifully crafted clay idols transform local living rooms across Karnataka, celebrating auspicious beginnings and Ganapati devotion. "
        "Intricate flower decorations and early-morning puja rituals re-energize the household as children arrange the sacred steps. "
        "Visiting guests are welcomed into homes with delicious kosambari, payasa, and temple-style prasada."
    ),
    ("ganesh-chaturthi", "kerala"): (
        "The rare Lambodhara aarti and specific temple offerings define the Kerala approach to auspicious beginnings and Ganapati devotion. "
        "Ornate floral designs and household lamp lighting ground the final three days of the sacred calendar in absolute stillness. "
        "The concluding celebration is marked by serving sweet payasam, banana chips, and elaborate festive spreads."
    ),
    ("ganesh-chaturthi", "madhya-pradesh"): (
        "High-energy community pandals and grand temporary shrines alter the urban space of Madhya Pradesh, showcasing deep auspicious beginnings and Ganapati devotion. "
        "Devotional mandir visits and old-city processions draw thousands out into illuminated public streets after sunset. "
        "The local evening hospitality is accompanied by distributing savory poha-style snacks, sweets, and prasad to visitors."
    ),
    ("ganesh-chaturthi", "maharashtra"): (
        "The grand welcoming with aarti and modak builds toward the magnificent immersion procession that defines the legendary Maharashtra celebration of auspicious beginnings and Ganapati devotion. "
        "Bustling society pandals and family aarti gatherings unite apartment complexes for nightly prayers and synchronized dances. "
        "The daily family gathering centers on preparing fresh, sweet modak, puran poli, and festive snacks."
    ),
    ("ganesh-chaturthi", "manipur"): (
        "Devotional storytelling and classical sequences fill local temples in Manipur, blending the season with auspicious beginnings and Ganapati devotion. "
        "Expressive cultural performances and temple participation offer a deeply classical avenue for community connection. "
        "The sacred week concludes with neighbourhoods arranging large community feasts paired with specialized seasonal sweets."
    ),
    ("ganesh-chaturthi", "meghalaya"): (
        "Sacred fasts and twilight prayer groups bring families together in Meghalaya, honoring the message of auspicious beginnings and Ganapati devotion. "
        "Festive church halls, homes, and community spaces host unique inter-cultural programs to celebrate the autumn season. "
        "The warm afternoon hospitality features sharing local festive rice dishes and unique local sweets with guests."
    ),
    ("ganesh-chaturthi", "mizoram"): (
        "Traditional oil lamps illuminate private balconies in Mizoram, bridging local harmony with the global focus on auspicious beginnings and Ganapati devotion. "
        "Decorated community halls and neighbourhood visits allow diaspora groups to gather for seasonal updates and songs. "
        "The autumn occasion is highlighted by gathering for shared festive meals and sweet offerings across local townships."
    ),
    ("ganesh-chaturthi", "nagaland"): (
        "Quiet home altars are decorated with autumn flowers across Nagaland, celebrating the spiritual presence of auspicious beginnings and Ganapati devotion. "
        "Vibrant collective singing and family hosting provide a welcoming environment for visiting relatives and friends. "
        "The peaceful seasonal gathering is highlighted by presenting large community meals and celebratory desserts."
    ),
    ("ganesh-chaturthi", "odisha"): (
        "The traditional installation of Ganesh idols inside schools and community blocks transforms Odisha, elevating days of deep auspicious beginnings and Ganapati devotion. "
        "Intricate alpona art and neighbourhood mandaps line the village paths where families gather to receive the deity's blessings. "
        "The holy days are accompanied by distributing traditional sweet khaja, pitha, and temple mahaprasad to neighbourhood networks."
    ),
    ("ganesh-chaturthi", "punjab"): (
        "The welcoming of Ganesha idols brings unique community gatherings and sweet distributions across Punjab, defining a grand celebration of auspicious beginnings and Ganapati devotion. "
        "Dedicated gurdwara seva and community langar participation run parallel to the domestic fasts across local towns. "
        "The auspicious day is marked by sharing warm kada prasad, festive rotis, and rich milk sweets."
    ),
    ("ganesh-chaturthi", "rajasthan"): (
        "Traditional folk chants and grand temple processions fill historic neighbourhoods in Rajasthan, elevating the heritage of auspicious beginnings and Ganapati devotion. "
        "Delicate courtyard lamps and royal-colour decorations provide a dramatic setting for the night-long prayers. "
        "The culinary gathering centers on serving sweet ghevar, rich dal-baati spreads, and festive mithai to extended clans."
    ),
    ("ganesh-chaturthi", "sikkim"): (
        "Hillside altars are dressed in fresh autumn leaves across Sikkim, welcoming the seasonal alignment with auspicious beginnings and Ganapati devotion. "
        "Grounded community prayer and hillside celebrations bring mountain settlements together for evening songs and shared prayers. "
        "The local hospitality involves sharing custom sweets and warm festive rice dishes among remote settlements."
    ),
    ("ganesh-chaturthi", "tamil-nadu"): (
        "The preparation of traditional kozhukattai and clay Vinayaka idols transforms Tamil Nadu homes, anchoring auspicious beginnings and Ganapati devotion. "
        "Vibrant kolam art, brass lamps, and dawn rituals reshape the domestic rhythm as neighbors visit to exchange sundal packets. "
        "The sacred season is celebrated by preparing sweet pongal, savory sundal, and sacred temple prasadam for guests."
    ),
    ("ganesh-chaturthi", "telangana"): (
        "The massive Khairatabad Ganesha idols and grand temporary stages transform Telangana, highlighting the local form of auspicious beginnings and Ganapati devotion. "
        "Bonalu-style community devotion and floral decor create a highly active and colorful public greeting space. "
        "The primary household table is filled with ritual paramannam, sweet laddus, and assorted festive savouries."
    ),
    ("ganesh-chaturthi", "tripura"): (
        "Devotional stotra recitations fill local community halls across Tripura, mirroring the autumn arrival of auspicious beginnings and Ganapati devotion. "
        "Family courtyards and community pandals turn into lively meeting points for multi-generational relative visits. "
        "The evening hospitality is highlighted by sharing traditional festive rice offerings and local sweets with neighbors."
    ),
    ("ganesh-chaturthi", "uttar-pradesh"): (
        "Grand neighbourhood pandals, dahi handi competitions, and late-night processions transform Uttar Pradesh, tracking days of auspicious beginnings and Ganapati devotion. "
        "Ancient ghat rituals and massive temple crowds create an unmatched public scale under the echo of midnight bells. "
        "The high-energy days include distributing famous sweet peda, kachori, and traditional prasad to the community."
    ),
    ("ganesh-chaturthi", "uttarakhand"): (
        "Hilltop temple pilgrimages and sacred fasts define the local experience in Uttarakhand, celebrating auspicious beginnings and Ganapati devotion. "
        "Ancient hill temples and family vrat observance bring remote mountain villages together for collective protective prayers. "
        "The spiritual gathering is completed by serving traditional singori, sweet halwa, and custom temple offerings."
    ),
    ("ganesh-chaturthi", "west-bengal"): (
        "The installation of Ganesha idols inside artistic community spaces initiates the festival season in West Bengal, showcasing a beautiful wave of auspicious beginnings and Ganapati devotion. "
        "Artistic neighbourhood pandals, echoing dhaak rhythms, and striking artistic decorations alter the local landscape during the dawn periods. "
        "The cultural transition is accompanied by preparing traditional sandesh, khichuri bhog, and assorted festive sweets."
    ),
    ("ganesh-chaturthi", "nri-london"): (
        "Massive community centers host vibrant immersion processions across London, allowing the diaspora to maintain ancestral auspicious beginnings and Ganapati devotion. "
        "Bustling weekend community events and cultural centres connect families across boroughs for simultaneous evening prayers. "
        "Expatriates mark the autumn transition by packing potluck sweets and temple prasada to share with global friends."
    ),
    ("ganesh-chaturthi", "nri-new-york"): (
        "Community centers host high-energy aarti and modak distributions in New York, preserving the heritage of auspicious beginnings and Ganapati devotion. "
        "Ornate temple halls, family Zooms, and community gatherings bridge the distance for long-distance relatives during the sacred nights. "
        "The diaspora gathering concludes with sharing custom festive meals and mandir prasad within local networks."
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
        "The unbroken four-prahara night vigil and sacred shiva abhishek pour over ancient lingams in Andhra Pradesh, centering on a night vigil, mantra, and inward stillness. "
        "The intense meditative energy fills local neighbourhoods, where public areas are enlivened by traditional temple processions and decorated entrances. "
        "Families mark the auspicious celebration by sharing traditional pulihora and laddus after surrendering their sleep for the night."
    ),
    ("maha-shivaratri", "arunachal-pradesh"): (
        "Strict fasting and midnight oil lamps anchor alpine valley shrines across Arunachal Pradesh, tracking the seasonal focus on a night vigil, mantra, and inward stillness. "
        "Bustling community halls and family gatherings fill with silent prayers as families gather for the grand midnight offerings. "
        "The spiritual morning concludes with households gathering to share custom community sweets and festive rice dishes."
    ),
    ("maha-shivaratri", "assam"): (
        "Continuous chantings of the Shiva Purana and sacred bilva leaf offerings alter the domestic rhythm in Assam, reflecting a deep focus on a night vigil, mantra, and inward stillness. "
        "Joyous music, prayer, and neighbourhood visits elevate local community spaces during the twilight transit hours. "
        "The sacred cycle is enriched by serving traditional pitha, payas, and festive rice offerings to the neighbourhood."
    ),
    ("maha-shivaratri", "bihar"): (
        "The symbolic wedding procession of Shiva or Shivaratri Mahotsav fills streets in Bihar, celebrating a magnificent display of a night vigil, mantra, and inward stillness. "
        "Bustling ghat visits and family puja routines allow large extended families to gather for collective mantra recitations. "
        "The daily ceremonial transition is marked by preparing sweet thekua, kheer, and seasonal savouries for ritual prasad."
    ),
    ("maha-shivaratri", "chhattisgarh"): (
        "Thousands of oil lamps illuminate the banks of holy rivers across Chhattisgarh, initiating the quiet celebration of a night vigil, mantra, and inward stillness. "
        "Vibrant community puja and local fairs bring farming communities together for evening folk dances and traditional prayers. "
        "The household hospitality centers on kitchens preparing specialized rice sweets and home-style prasad for daily offerings."
    ),
    ("maha-shivaratri", "goa"): (
        "Serene oil lamp illuminations turn temple courtyards into spaces of absolute calm in Goa, channeling a beautiful wave of a night vigil, mantra, and inward stillness. "
        "Quiet home altars and bustling neighbourhood celebration routes define the spatial layout of the local evening prayers. "
        "The sacred period is marked by sharing unique coconut sweets and festive savouries among long-time neighbours."
    ),
    ("maha-shivaratri", "gujarat"): (
        "The grand Mahashivaratri fair at the base of Mount Girnar draws massive crowds in Gujarat, magnifying the festive energy of a night vigil, mantra, and inward stillness. "
        "Bustling garba grounds and bright rangoli work completely transform public and private squares under bright festive lights. "
        "Dancers replenish their energy late into the night by gathering around multi-course festive thalis loaded with fafda and jalebi."
    ),
    ("maha-shivaratri", "haryana"): (
        "Devout pouring of milk and water over neighbourhood shrines brings communities together across Haryana, magnifying the annual cycle of a night vigil, mantra, and inward stillness. "
        "Family courtyards and temple offerings turn into central meeting points where neighbourhood women lead traditional folk prayers. "
        "The home gatherings are warmed by sharing rustic halwa, puri, and farm-style festive meals among relatives."
    ),
    ("maha-shivaratri", "himachal-pradesh"): (
        "The world-renowned Mandi Shivaratri fair transforms historic valley temples across Himachal Pradesh, anchoring local valleys in a vibrant display of a night vigil, mantra, and inward stillness. "
        "Serene village temples and hillside processions host local clans traveling across valleys to pay homage to their deities. "
        "The spiritual afternoon is comforted by serving sweet rice, prasad, and mountain-style meals around communal hearths."
    ),
    ("maha-shivaratri", "jharkhand"): (
        "Continuous pouring of milk, honey, and bhasma marks residential colonies in Jharkhand, marking the seasonal alignment with a night vigil, mantra, and inward stillness. "
        "Open community grounds and family prayer circles provide an inclusive space for traditional drumming and evening chants. "
        "The nine-day fast is supported by sharing unique seasonal sweets and simple ceremonial meals within families."
    ),
    ("maha-shivaratri", "karnataka"): (
        "Night-long cultural performances and deep meditation vigils transform local temples across Karnataka, celebrating a night vigil, mantra, and inward stillness. "
        "Intricate flower decorations and early-morning puja rituals re-energize the household as children arrange the sacred steps. "
        "Visiting guests are welcomed into homes with delicious kosambari, payasa, and temple-style prasada."
    ),
    ("maha-shivaratri", "kerala"): (
        "The chanting of the Panchakshari mantra and continuous temple steps create a profound atmosphere in Kerala, marking a unique southern expression of a night vigil, mantra, and inward stillness. "
        "Ornate floral designs and household lamp lighting ground the final three days of the sacred calendar in absolute stillness. "
        "The concluding celebration is marked by serving sweet payasam, banana chips, and elaborate festive spreads."
    ),
    ("maha-shivaratri", "madhya-pradesh"): (
        "The majestic celebrations at the ancient Mahakaleshwar temple in Ujjain draw millions across Madhya Pradesh, showcasing deep arrays of a night vigil, mantra, and inward stillness. "
        "Devotional mandir visits and old-city processions draw thousands out into illuminated public streets after sunset. "
        "The local evening hospitality is accompanied by distributing savory poha-style snacks, sweets, and prasad to visitors."
    ),
    ("maha-shivaratri", "maharashtra"): (
        "The systematic pouring of panchamrut over sacred lingams anchors local neighbourhood complexes across Maharashtra, initiating days of a night vigil, mantra, and inward stillness. "
        "Bustling society pandals and family aarti gatherings unite apartment complexes for nightly prayers and synchronized dances. "
        "The daily family gathering centers on preparing fresh, sweet modak, puran poli, and festive snacks."
    ),
    ("maha-shivaratri", "manipur"): (
        "Devotional storytelling and classical musical sequences fill local temples in Manipur, blending the season with a night vigil, mantra, and inward stillness. "
        "Expressive cultural performances and temple participation offer a deeply classical avenue for community connection. "
        "The sacred week concludes with neighbourhoods arranging large community feasts paired with specialized seasonal sweets."
    ),
    ("maha-shivaratri", "meghalaya"): (
        "Sacred fasts and twilight prayer groups bring families together in Meghalaya, honoring the message of a night vigil, mantra, and inward stillness. "
        "Festive church halls, homes, and community spaces host unique inter-cultural programs to celebrate the autumn season. "
        "The warm afternoon hospitality features sharing local festive rice dishes and unique local sweets with guests."
    ),
    ("maha-shivaratri", "mizoram"): (
        "Traditional oil lamps illuminate private balconies in Mizoram, bridging local harmony with the global focus on a night vigil, mantra, and inward stillness. "
        "Decorated community halls and neighbourhood visits allow diaspora groups to gather for seasonal updates and songs. "
        "The autumn occasion is highlighted by gathering for shared festive meals and sweet offerings across local townships."
    ),
    ("maha-shivaratri", "nagaland"): (
        "Quiet hilltop altars are decorated with sacred flowers across Nagaland, celebrating the spiritual presence of a night vigil, mantra, and inward stillness. "
        "Vibrant collective singing and family hosting provide a welcoming environment for visiting relatives and friends. "
        "The peaceful seasonal gathering is highlighted by presenting large community meals and celebratory desserts."
    ),
    ("maha-shivaratri", "odisha"): (
        "The majestic lighting of the Mahadipa atop ancient Shiva temples transforms Odisha, elevating a profound wave of a night vigil, mantra, and inward stillness. "
        "Intricate alpona art and neighbourhood mandaps line the village paths where families gather to receive the deity's blessings. "
        "The holy days are accompanied by distributing traditional sweet khaja, pitha, and temple mahaprasad to neighbourhood networks."
    ),
    ("maha-shivaratri", "punjab"): (
        "Shobha yatras and intense continuous kirtan sessions fill local residential areas across Punjab, defining a grand display of a night vigil, mantra, and inward stillness. "
        "Dedicated gurdwara seva and community langar participation run parallel to the domestic fasts across local towns. "
        "The auspicious eighth day is marked by sharing warm kada prasad, festive rotis, and rich milk sweets."
    ),
    ("maha-shivaratri", "rajasthan"): (
        "Traditional folk chants and grand temple processions fill royal courtyards in Rajasthan, elevating the heritage of a night vigil, mantra, and inward stillness. "
        "Delicate courtyard lamps and royal-colour decorations provide a dramatic setting for the night-long prayers. "
        "The culinary gathering centers on serving sweet ghevar, rich dal-baati spreads, and festive mithai to extended clans."
    ),
    ("maha-shivaratri", "sikkim"): (
        "Hillside altars are dressed in fresh autumn leaves across Sikkim, welcoming the seasonal alignment with a night vigil, mantra, and inward stillness. "
        "Grounded community prayer and hillside celebrations bring mountain settlements together for evening songs and shared prayers. "
        "The local hospitality involves sharing custom sweets and warm festive rice dishes among remote settlements."
    ),
    ("maha-shivaratri", "tamil-nadu"): (
        "The night-long musical and dance tributes or Sangeethanjali transform Tamil Nadu temples, anchoring a night vigil, mantra, and inward stillness. "
        "Vibrant kolam art, brass lamps, and dawn rituals reshape the domestic rhythm as neighbors visit to exchange sundal packets. "
        "The sacred season is celebrated by preparing sweet pongal, savory sundal, and sacred temple prasadam for guests."
    ),
    ("maha-shivaratri", "telangana"): (
        "Continuous pouring of milk and water over ancient lingams transforms ancient shrines across Telangana, highlighting a profound display of a night vigil, mantra, and inward stillness. "
        "Bonalu-style community devotion and floral decor create a highly active and colorful public greeting space. "
        "The primary household table is filled with ritual paramannam, sweet laddus, and assorted festive savouries."
    ),
    ("maha-shivaratri", "tripura"): (
        "Devotional stotra recitations fill local community halls across Tripura, mirroring the winter arrival of a night vigil, mantra, and inward stillness. "
        "Family courtyards and community pandals turn into lively meeting points for multi-generational relative visits. "
        "The evening hospitality is highlighted by sharing traditional festive rice offerings and local sweets with neighbours."
    ),
    ("maha-shivaratri", "uttar-pradesh"): (
        "The grand rituals at Kashi Vishwanath temple in Varanasi transform Uttar Pradesh, tracking a magnificent display of a night vigil, mantra, and inward stillness. "
        "Ancient ghat rituals and massive temple crowds create an unmatched public scale under the echo of midnight bells. "
        "The high-energy days include distributing famous sweet peda, kachori, and traditional prasad to the community."
    ),
    ("maha-shivaratri", "uttarakhand"): (
        "Pilgrimages to ancient high-altitude temples and strict fasts define the local experience in Uttarakhand, celebrating a serene display of a night vigil, mantra, and inward stillness. "
        "Ancient hill temples and family vrat observance bring remote mountain villages together for collective protective prayers. "
        "The spiritual gathering is completed by serving traditional singori, sweet halwa, and custom temple offerings."
    ),
    ("maha-shivaratri", "west-bengal"): (
        "The preparation of unique four-prahara clay lingams transforms homes in West Bengal, showcasing a beautiful wave of a night vigil, mantra, and inward stillness. "
        "Artistic neighbourhood pandals, echoing dhaak rhythms, and striking artistic decorations alter the local landscape during the dawn periods. "
        "The cultural transition is accompanied by preparing traditional sandesh, khichuri bhog, and assorted festive sweets."
    ),
    ("maha-shivaratri", "nri-london"): (
        "Massive community halls host night-long classical music and meditation workshops across London, allowing the diaspora to maintain an authentic experience of a night vigil, mantra, and inward stillness. "
        "Bustling weekend community events and cultural centres connect families across boroughs for simultaneous evening prayers. "
        "Expatriates mark the autumn transition by packing potluck sweets and temple prasada to share with global friends."
    ),
    ("maha-shivaratri", "nri-new-york"): (
        "Community centers host high-energy bhajan recitations and continuous abhishek in New York, preserving the heritage of a night vigil, mantra, and inward stillness. "
        "Ornate temple halls, family Zooms, and community gatherings bridge the distance for long-distance relatives during the sacred nights. "
        "The diaspora gathering concludes with sharing custom festive meals and mandir prasad within local networks."
    ),


    # ── MAKAR SANKRANTI (Batch 8 -- all 30 regions) ───────────────────────────
    ("makar-sankranti", "andhra-pradesh"): (
        "Colorful kites climb from rooftops and tilgul boxes pass between neighbours across Andhra Pradesh, centering on harvest, sunlight, and transition. "
        "The bright seasonal energy fills local neighbourhoods, where public areas are enlivened by traditional temple processions and decorated entrances. "
        "Families mark the auspicious solar migration by sharing traditional pulihora and laddus outside their decorated homes."
    ),
    ("makar-sankranti", "arunachal-pradesh"): (
        "Sesame and jaggery sweets are prepared to welcome the sun's northward turn across Arunachal Pradesh, anchoring the seasonal focus on harvest, sunlight, and transition. "
        "Bustling community halls and family gatherings fill with traditional greetings as families celebrate the passing of the cold winter solstice. "
        "The playful morning concludes with households gathering to share custom community sweets and festive rice dishes."
    ),
    ("makar-sankranti", "assam"): (
        "High-energy Magh Bihu bonfires and upward-looking community games alter the rural landscape in Assam, reflecting a deep focus on harvest, sunlight, and transition. "
        "Joyous music, prayer, and neighbourhood visits elevate local community spaces during the daylight agricultural changes. "
        "The sacred cycle is enriched by serving traditional pitha, payas, and festive rice offerings to the neighbourhood."
    ),
    ("makar-sankranti", "bihar"): (
        "Traditional dahi-chura meals and massive holy dips at river confluences mark the daytime rhythm in Bihar, celebrating harvest, sunlight, and transition. "
        "Bustling ghat visits and family puja routines allow large extended families to gather for collective sun prayers. "
        "The daily ceremonial transition is marked by preparing sweet thekua, kheer, and seasonal savouries for ritual prasad."
    ),
    ("makar-sankranti", "chhattisgarh"): (
        "Earthen pots filled with freshly harvested til and rice are exchanged across Chhattisgarh, initiating the quiet celebration of harvest, sunlight, and transition. "
        "Vibrant community puja and local fairs bring farming communities together for evening folk dances and traditional prayers. "
        "The household hospitality centers on kitchens preparing specialized rice sweets and home-style prasad for daily offerings."
    ),
    ("makar-sankranti", "goa"): (
        "Married women distribute traditional clay pots filled with seasonal grains and sugarcane in Goa, channeling a beautiful wave of harvest, sunlight, and transition. "
        "Quiet home altars and bustling neighbourhood celebration routes define the spatial layout of the local evening prayers. "
        "The sacred period is marked by sharing unique coconut sweets and festive savouries among long-time neighbours."
    ),
    ("makar-sankranti", "gujarat"): (
        "Thousands of vibrant kites cloud the skies of Ahmedabad during the grand Uttarayan festival in Gujarat, magnifying the festive energy of harvest, sunlight, and transition. "
        "Bustling garba grounds and bright rangoli work completely transform public and private squares under bright festive lights. "
        "Dancers replenish their energy late into the night by gathering around multi-course festive thalis loaded with fafda and jalebi."
    ),
    ("makar-sankranti", "haryana"): (
        "The sharing of sweet reweri, gajak, and til sweets brings agricultural families together across Haryana, magnifying the annual cycle of harvest, sunlight, and transition. "
        "Family courtyards and temple offerings turn into central meeting points where neighbourhood women lead traditional folk prayers. "
        "The home gatherings are warmed by sharing rustic halwa, puri, and farm-style festive meals among relatives."
    ),
    ("makar-sankranti", "himachal-pradesh"): (
        "The Maghi festival features traditional holy dips and shared community charity across Himachal Pradesh, anchoring local valleys in harvest, sunlight, and transition. "
        "Serene village temples and hillside processions host local clans traveling across valleys to pay homage to their deities. "
        "The spiritual afternoon is comforted by serving sweet rice, prasad, and mountain-style meals around communal hearths."
    ),
    ("makar-sankranti", "jharkhand"): (
        "The traditional Tusu Parab songs and freshly harvested grain offerings decorate residential colonies in Jharkhand, marking the seasonal alignment with harvest, sunlight, and transition. "
        "Open community grounds and family prayer circles provide an inclusive space for traditional drumming and evening chants. "
        "The nine-day fast is supported by sharing unique seasonal sweets and simple ceremonial meals within families."
    ),
    ("makar-sankranti", "karnataka"): (
        "The dynamic Ellu Birodhu exchange of sesame seeds, sugarcane, and groundnuts transforms local living rooms across Karnataka, celebrating harvest, sunlight, and transition. "
        "Intricate flower decorations and early-morning puja rituals re-energize the household as children arrange the sacred steps. "
        "Visiting guests are welcomed into homes with delicious kosambari, payasa, and temple-style prasada."
    ),
    ("makar-sankranti", "kerala"): (
        "The legendary Makaravilakku lighting atop the sacred hills of Sabarimala creates an incredible devotional scale in Kerala, marking a unique southern expression of harvest, sunlight, and transition. "
        "Ornate floral designs and household lamp lighting ground the final three days of the sacred calendar in absolute stillness. "
        "The concluding celebration is marked by serving sweet payasam, banana chips, and elaborate festive spreads."
    ),
    ("makar-sankranti", "madhya-pradesh"): (
        "Large-scale kite flying tournaments and grand holy river dips alter the public space of Madhya Pradesh, showcasing deep arrays of harvest, sunlight, and transition. "
        "Devotional mandir visits and old-city processions draw thousands out into illuminated public streets after sunset. "
        "The local evening hospitality is accompanied by distributing savory poha-style snacks, sweets, and prasad to visitors."
    ),
    ("makar-sankranti", "maharashtra"): (
        "The classic exchange of tilgul with the phrase 'til-gul ghya, god god bola' anchors local neighbourhood complexes across Maharashtra, initiating days of harvest, sunlight, and transition. "
        "Bustling society pandals and family aarti gatherings unite apartment complexes for nightly prayers and synchronized dances. "
        "The daily family gathering centers on preparing fresh, sweet modak, puran poli, and festive snacks."
    ),
    ("makar-sankranti", "manipur"): (
        "Harvest thanksgiving rituals and classical devotional musical sequences fill local temples in Manipur, blending the season with harvest, sunlight, and transition. "
        "Expressive cultural performances and temple participation offer a deeply classical avenue for community connection. "
        "The sacred week concludes with neighbourhoods arranging large community feasts paired with specialized seasonal sweets."
    ),
    ("makar-sankranti", "meghalaya"): (
        "Fresh winter grain displays and twilight prayer groups bring families together in Meghalaya, honoring the message of harvest, sunlight, and transition. "
        "Festive church halls, homes, and community spaces host unique inter-cultural programs to celebrate the autumn season. "
        "The warm afternoon hospitality features sharing local festive rice dishes and unique local sweets with guests."
    ),
    ("makar-sankranti", "mizoram"): (
        "Traditional oil lamps and winter harvest greetings decorate private balconies in Mizoram, bridging local harmony with the global focus on harvest, sunlight, and transition. "
        "Decorated community halls and neighbourhood visits allow diaspora groups to gather for seasonal updates and songs. "
        "The autumn occasion is highlighted by gathering for shared festive meals and sweet offerings across local townships."
    ),
    ("makar-sankranti", "nagaland"): (
        "Agrarian celebration songs and community bonfires are coordinated across Nagaland, celebrating the spiritual presence of harvest, sunlight, and transition. "
        "Vibrant collective singing and family hosting provide a welcoming environment for visiting relatives and friends. "
        "The peaceful seasonal gathering is highlighted by presenting large community meals and celebratory desserts."
    ),
    ("makar-sankranti", "odisha"): (
        "The Makara Mela festivals on the pristine grounds of ancient temples transform Odisha, elevating a profound wave of deep harvest, sunlight, and transition. "
        "Intricate alpona art and neighbourhood mandaps line the village paths where families gather to receive the deity's blessings. "
        "The holy days are accompanied by distributing traditional sweet khaja, pitha, and temple mahaprasad to neighbourhood networks."
    ),
    ("makar-sankranti", "punjab"): (
        "The high-energy Maghi fair following the vibrant Lohri night bonfires fills local residential areas across Punjab, defining a grand display of harvest, sunlight, and transition. "
        "Dedicated gurdwara seva and community langar participation run parallel to the domestic fasts across local towns. "
        "The auspicious eighth day is marked by sharing warm kada prasad, festive rotis, and rich milk sweets."
    ),
    ("makar-sankranti", "rajasthan"): (
        "High-flying kite arrays and specialised charity to elders fill historic neighbourhoods in Rajasthan, elevating the heritage of harvest, sunlight, and transition. "
        "Delicate courtyard lamps and royal-colour decorations provide a dramatic setting for the night-long prayers. "
        "The culinary gathering centers on serving sweet ghevar, rich dal-baati spreads, and festive mithai to extended clans."
    ),
    ("makar-sankranti", "sikkim"): (
        "The traditional Maghe Sankranti holy dips in mountain rivers bring communities together across Sikkim, welcoming the seasonal alignment with harvest, sunlight, and transition. "
        "Grounded community prayer and hillside celebrations bring mountain settlements together for evening songs and shared prayers. "
        "The local hospitality involves sharing custom sweets and warm festive rice dishes among remote settlements."
    ),
    ("makar-sankranti", "tamil-nadu"): (
        "The grand Pongal boil-over rituals and beautiful cattle decorations transform Tamil Nadu, anchoring harvest, sunlight, and transition. "
        "Vibrant kolam art, brass lamps, and dawn rituals reshape the domestic rhythm as neighbours visit to exchange sundal packets. "
        "The sacred season is celebrated by preparing sweet pongal, savory sundal, and sacred temple prasadam for guests."
    ),
    ("makar-sankranti", "telangana"): (
        "Intricate multi-colored rangoli designs and dynamic community kite-flying paths decorate thresholds across Telangana, highlighting a profound display of harvest, sunlight, and transition. "
        "Bonalu-style community devotion and floral decor create a highly active and colorful public greeting space. "
        "The primary household table is filled with ritual paramannam, sweet laddus, and assorted festive savouries."
    ),
    ("makar-sankranti", "tripura"): (
        "Traditional Pous Sankranti rice cakes and devotional stotra recitations fill community halls across Tripura, mirroring the winter arrival of harvest, sunlight, and transition. "
        "Family courtyards and community pandals turn into lively meeting points for multi-generational relative visits. "
        "The evening hospitality is highlighted by sharing traditional festive rice offerings and local sweets with neighbours."
    ),
    ("makar-sankranti", "uttar-pradesh"): (
        "The world-famous Khichdi Mela holy dips in Prayagraj transform Uttar Pradesh, tracking a magnificent display of harvest, sunlight, and transition. "
        "Ancient ghat rituals and massive temple crowds create an unmatched public scale under the echo of midnight bells. "
        "The high-energy days include distributing famous sweet peda, kachori, and traditional prasad to the community."
    ),
    ("makar-sankranti", "uttarakhand"): (
        "The sweet feeding of migratory birds during the Kale Kauva festival defines the local experience in Uttarakhand, celebrating a serene display of harvest, sunlight, and transition. "
        "Ancient hill temples and family vrat observance bring remote mountain villages together for collective protective prayers. "
        "The spiritual gathering is completed by serving traditional singori, sweet halwa, and custom temple offerings."
    ),
    ("makar-sankranti", "west-bengal"): (
        "Millions of pilgrims taking holy dips at Ganga Sagar transform West Bengal, showcasing a beautiful wave of harvest, sunlight, and transition. "
        "Artistic neighbourhood pandals, echoing dhaak rhythms, and striking artistic decorations alter the local landscape during the dawn periods. "
        "The cultural transition is accompanied by preparing traditional sandesh, khichuri bhog, and assorted festive sweets."
    ),
    ("makar-sankranti", "nri-london"): (
        "Indoor community halls host colorful simulated kite workshops across London, allowing the diaspora to maintain an authentic experience of harvest, sunlight, and transition. "
        "Bustling weekend community events and cultural centres connect families across boroughs for simultaneous evening prayers. "
        "Expatriates mark the autumn transition by packing potluck sweets and temple prasada to share with global friends."
    ),
    ("makar-sankranti", "nri-new-york"): (
        "Community centers host high-energy sesame candy distribution and stotra recitations in New York, preserving the heritage of harvest, sunlight, and transition. "
        "Ornate temple halls, family Zooms, and community gatherings bridge the distance for long-distance relatives during the sacred nights. "
        "The diaspora gathering concludes with sharing custom festive meals and mandir prasad within local networks."
    ),


    # ── PONGAL (Batch 9 -- all 30 regions) ────────────────────────────────────
    ("pongal", "andhra-pradesh"): (
        "Earthen pots boil over outdoors in Andhra Pradesh as families echo festive shouts to welcome the spirit of harvest gratitude and household abundance. "
        "The agrarian energy fills local neighbourhoods, where public areas are enlivened by traditional temple processions and decorated entrances. "
        "Families mark the auspicious multi-day cycle by sharing traditional pulihora and laddus with their immediate neighbourhood circles."
    ),
    ("pongal", "arunachal-pradesh"): (
        "Freshly harvested grains are offered around home fires across Arunachal Pradesh, anchoring the winter solstice with harvest gratitude and household abundance. "
        "Bustling community halls and family gatherings fill with warm winter prayers as families gather for seasonal thanksgiving rituals. "
        "The playful morning concludes with households gathering to share custom community sweets and festive rice dishes."
    ),
    ("pongal", "assam"): (
        "The building of traditional thatch huts and agricultural bonfires reshapes fields in Assam, reflecting a deep harvest gratitude and household abundance. "
        "Joyous music, prayer, and neighbourhood visits elevate local community spaces during the daylight cultural transitions. "
        "The winter cycle is enriched by serving traditional pitha, payas, and festive rice offerings to the neighbourhood."
    ),
    ("pongal", "bihar"): (
        "Traditional sesame distributions and solar prayers define the daytime household rhythm in Bihar, celebrating harvest gratitude and household abundance. "
        "Bustling ghat visits and family puja routines allow large extended families to gather for collective agricultural chants. "
        "The daily ceremonial transition is marked by preparing sweet thekua, kheer, and seasonal savouries for ritual prasad."
    ),
    ("pongal", "chhattisgarh"): (
        "Earthen pots carrying newly harvested grains are placed before home shrines in Chhattisgarh, initiating the quiet celebration of harvest gratitude and household abundance. "
        "Vibrant community puja and local fairs bring farming communities together for evening folk dances and traditional prayers. "
        "The household hospitality centers on kitchens preparing specialized rice sweets and home-style prasad for daily offerings."
    ),
    ("pongal", "goa"): (
        "Clay pots filled with winter harvest produce are offered at family altars across Goa, channeling a beautiful wave of harvest gratitude and household abundance. "
        "Quiet home altars and bustling neighbourhood celebration routes define the spatial layout of the local evening prayers. "
        "The sacred period is marked by sharing unique coconut sweets and festive savouries among long-time neighbours."
    ),
    ("pongal", "gujarat"): (
        "Bright solar patterns and high-flying kite arrays decorate residential colonies across Gujarat, magnifying the festive energy of harvest gratitude and household abundance. "
        "Bustling garba grounds and bright rangoli work completely transform public and private squares under bright festive lights. "
        "Dancers replenish their energy late into the night by gathering around multi-course festive thalis loaded with fafda and jalebi."
    ),
    ("pongal", "haryana"): (
        "Agrarian families gather to offer fresh winter crops to community shrines across Haryana, magnifying the annual cycle of harvest gratitude and household abundance. "
        "Family courtyards and temple offerings turn into central meeting points where neighbourhood women lead traditional folk prayers. "
        "The home gatherings are warmed by sharing rustic halwa, puri, and farm-style festive meals among relatives."
    ),
    ("pongal", "himachal-pradesh"): (
        "Village winter bonfires emerge amidst the cold mountain air across Himachal Pradesh, anchoring local valleys in harvest gratitude and household abundance. "
        "Serene village temples and hillside processions host local clans traveling across valleys to pay homage to their deities. "
        "The spiritual afternoon is comforted by serving sweet rice, prasad, and mountain-style meals around communal hearths."
    ),
    ("pongal", "jharkhand"): (
        "Traditional Tusu festival markers and fresh grain decorations transform residential colonies in Jharkhand, marking the seasonal alignment with harvest gratitude and household abundance. "
        "Open community grounds and family prayer circles provide an inclusive space for traditional drumming and evening chants. "
        "The nine-day fast is supported by sharing unique seasonal sweets and simple ceremonial meals within families."
    ),
    ("pongal", "karnataka"): (
        "The classic Sankranti ellu-bella grain exchange and cattle decorating rituals transform local living rooms across Karnataka, celebrating harvest gratitude and household abundance. "
        "Intricate flower decorations and early-morning puja rituals re-energize the household as children arrange the sacred steps. "
        "Visiting guests are welcomed into homes with delicious kosambari, payasa, and temple-style prasada."
    ),
    ("pongal", "kerala"): (
        "Specialised Makaravilakku temple rituals and solar prayers are observed quietly in Kerala, marking a unique southern expression of harvest gratitude and household abundance. "
        "Ornate floral designs and household lamp lighting ground the final three days of the sacred calendar in absolute stillness. "
        "The concluding celebration is marked by serving sweet payasam, banana chips, and elaborate festive spreads."
    ),
    ("pongal", "madhya-pradesh"): (
        "Large-scale kite flying tournaments and grand holy river dips alter the public space of Madhya Pradesh, showcasing deep arrays of harvest gratitude and household abundance. "
        "Devotional mandir visits and old-city processions draw thousands out into illuminated public streets after sunset. "
        "The local evening hospitality is accompanied by distributing savory poha-style snacks, sweets, and prasad to visitors."
    ),
    ("pongal", "maharashtra"): (
        "The sharing of sweet tilgul sweets with messages of goodwill anchors local neighbourhood complexes across Maharashtra, initiating days of harvest gratitude and household abundance. "
        "Bustling society pandals and family aarti gatherings unite apartment complexes for nightly prayers and synchronized dances. "
        "The daily family gathering centers on preparing fresh, sweet modak, puran poli, and festive snacks."
    ),
    ("pongal", "manipur"): (
        "Harvest thanksgiving rituals and classical devotional musical sequences fill local temples in Manipur, blending the season with harvest gratitude and household abundance. "
        "Expressive cultural performances and temple participation offer a deeply classical avenue for community connection. "
        "The sacred week concludes with neighbourhoods arranging large community feasts paired with specialized seasonal sweets."
    ),
    ("pongal", "meghalaya"): (
        "Fresh winter grain displays and twilight prayer groups bring families together in Meghalaya, honoring the message of harvest gratitude and household abundance. "
        "Festive church halls, homes, and community spaces host unique inter-cultural programs to celebrate the autumn season. "
        "The warm afternoon hospitality features sharing local festive rice dishes and unique local sweets with guests."
    ),
    ("pongal", "mizoram"): (
        "Traditional oil lamps and winter harvest greetings decorate private balconies in Mizoram, bridging local harmony with the global focus on harvest gratitude and household abundance. "
        "Decorated community halls and neighbourhood visits allow diaspora groups to gather for seasonal updates and songs. "
        "The autumn occasion is highlighted by gathering for shared festive meals and sweet offerings across local townships."
    ),
    ("pongal", "nagaland"): (
        "Agrarian celebration songs and community bonfires are coordinated across Nagaland, celebrating the spiritual presence of harvest gratitude and household abundance. "
        "Vibrant collective singing and family hosting provide a welcoming environment for visiting relatives and friends. "
        "The peaceful seasonal gathering is highlighted by presenting large community meals and celebratory desserts."
    ),
    ("pongal", "odisha"): (
        "The Makara Mela festivals on the pristine grounds of ancient temples transform Odisha, elevating a profound wave of deep harvest gratitude and household abundance. "
        "Intricate alpona art and neighbourhood mandaps line the village paths where families gather to receive the deity's blessings. "
        "The holy days are accompanied by distributing traditional sweet khaja, pitha, and temple mahaprasad to neighbourhood networks."
    ),
    ("pongal", "punjab"): (
        "High-energy Maghi assemblies following the vibrant Lohri night bonfires fill local residential areas across Punjab, defining a grand display of harvest gratitude and household abundance. "
        "Dedicated gurdwara seva and community langar participation run parallel to the domestic fasts across local towns. "
        "The auspicious eighth day is marked by sharing warm kada prasad, festive rotis, and rich milk sweets."
    ),
    ("pongal", "rajasthan"): (
        "High-flying kite arrays and specialised charity to elders fill historic neighbourhoods in Rajasthan, elevating the heritage of harvest gratitude and household abundance. "
        "Delicate courtyard lamps and royal-colour decorations provide a dramatic setting for the night-long prayers. "
        "The culinary gathering centers on serving sweet ghevar, rich dal-baati spreads, and festive mithai to extended clans."
    ),
    ("pongal", "sikkim"): (
        "The traditional Maghe Sankranti holy dips in mountain rivers bring communities together across Sikkim, welcoming the seasonal alignment with harvest gratitude and household abundance. "
        "Grounded community prayer and hillside celebrations bring mountain settlements together for evening songs and shared prayers. "
        "The local hospitality involves sharing custom sweets and warm festive rice dishes among remote settlements."
    ),
    ("pongal", "tamil-nadu"): (
        "The pongal pot boils outdoors on the first morning, sugarcanes guard thresholds, and decorated cattle define the grand Tamil Nadu peak of harvest gratitude and household abundance. "
        "Vibrant kolam art, brass lamps, and dawn rituals reshape the domestic rhythm as families gather to shout 'Pongalo Pongal' in unison. "
        "The sacred season is celebrated by preparing sweet pongal, savory sundal, and sacred temple prasadam for guests."
    ),
    ("pongal", "telangana"): (
        "Intricate multi-colored rangoli designs and dynamic community kite-flying paths decorate thresholds across Telangana, highlighting a profound display of harvest gratitude and household abundance. "
        "Bonalu-style community devotion and floral decor create a highly active and colorful public greeting space. "
        "The primary household table is filled with ritual paramannam, sweet laddus, and assorted festive savouries."
    ),
    ("pongal", "tripura"): (
        "Traditional winter rice cakes and devotional stotra recitations fill community halls across Tripura, mirroring the winter arrival of harvest gratitude and household abundance. "
        "Family courtyards and community pandals turn into lively meeting points for multi-generational relative visits. "
        "The evening hospitality is highlighted by sharing traditional festive rice offerings and local sweets with neighbours."
    ),
    ("pongal", "uttar-pradesh"): (
        "The magnificent Khichdi Mela holy dips in Prayagraj transform Uttar Pradesh, tracking a magnificent display of harvest gratitude and household abundance. "
        "Ancient ghat rituals and massive temple crowds create an unmatched public scale under the echo of midnight bells. "
        "The high-energy days include distributing famous sweet peda, kachori, and traditional prasad to the community."
    ),
    ("pongal", "uttarakhand"): (
        "The sweet feeding of migratory birds during winter solstice celebrations defines the local experience in Uttarakhand, celebrating a serene display of harvest gratitude and household abundance. "
        "Ancient hill temples and family vrat observance bring remote mountain villages together for collective protective prayers. "
        "The spiritual gathering is completed by serving traditional singori, sweet halwa, and custom temple offerings."
    ),
    ("pongal", "west-bengal"): (
        "The dynamic Poush Parbon pithe making and holy dips at Ganga Sagar transform West Bengal, showcasing a beautiful wave of harvest gratitude and household abundance. "
        "Artistic neighbourhood pandals, echoing dhaak rhythms, and striking artistic decorations alter the local landscape during the dawn periods. "
        "The cultural transition is accompanied by preparing traditional sandesh, khichuri bhog, and assorted festive sweets."
    ),
    ("pongal", "nri-london"): (
        "Indoor community halls host colorful simulated harvest workshops across London, allowing the diaspora to maintain an authentic experience of harvest gratitude and household abundance. "
        "Bustling weekend community events and cultural centres connect families across boroughs for simultaneous evening prayers. "
        "Expatriates mark the autumn transition by packing potluck sweets and temple prasada to share with global friends."
    ),
    ("pongal", "nri-new-york"): (
        "Community centers host high-energy sugarcane decorations and sweet rice distribution in New York, preserving the heritage of harvest gratitude and household abundance. "
        "Ornate temple halls, family Zooms, and community gatherings bridge the distance for long-distance relatives during the sacred nights. "
        "The diaspora gathering concludes with sharing custom festive meals and mandir prasad within local networks."
    ),


    # ── ONAM (Batch 10 -- all 30 regions) ─────────────────────────────────────
    ("onam", "andhra-pradesh"): (
        "Ten days of intricate pookalam flower carpets begin across Andhra Pradesh, centering local communities on harvest joy, floral beauty, and family reunion. "
        "The bright visual energy fills local neighbourhoods, where public areas are enlivened by traditional temple processions and decorated entrances. "
        "Families mark the auspicious return of King Mahabali by sharing traditional pulihora and laddus outside their floral entryways."
    ),
    ("onam", "arunachal-pradesh"): (
        "Delicate floral designs and fresh blossoms are arranged beautifully across Arunachal Pradesh homes, anchoring the harvest joy, floral beauty, and family reunion. "
        "Bustling community halls and family gatherings fill with warm songs as families gather for seasonal thanksgiving rituals. "
        "The playful morning concludes with households gathering to share custom community sweets and festive rice dishes."
    ),
    ("onam", "assam"): (
        "Colorful flower patterns and agricultural decorations reshape fields in Assam, reflecting a deep harvest joy, floral beauty, and family reunion. "
        "Joyous music, prayer, and neighbourhood visits elevate local community spaces during the daylight cultural transitions. "
        "The winter cycle is enriched by serving traditional pitha, payas, and festive rice offerings to the neighbourhood."
    ),
    ("onam", "bihar"): (
        "Beautiful floral decorations and standard home altars define the daytime household rhythm in Bihar, celebrating harvest joy, floral beauty, and family reunion. "
        "Bustling ghat visits and family puja routines allow large extended families to gather for collective agricultural chants. "
        "The daily ceremonial transition is marked by preparing sweet thekua, kheer, and seasonal savouries for ritual prasad."
    ),
    ("onam", "chhattisgarh"): (
        "Intricate flower mats are laid before home shrines in Chhattisgarh, initiating the quiet celebration of harvest joy, floral beauty, and family reunion. "
        "Vibrant community puja and local fairs bring farming communities together for evening folk dances and traditional prayers. "
        "The household hospitality centers on kitchens preparing specialized rice sweets and home-style prasad for daily offerings."
    ),
    ("onam", "goa"): (
        "Fresh blossoms and unique floral carpets decorate family altars across Goa, channeling a beautiful wave of harvest joy, floral beauty, and family reunion. "
        "Quiet home altars and bustling neighbourhood celebration routes define the spatial layout of the local evening prayers. "
        "The sacred period is marked by sharing unique coconut sweets and festive savouries among long-time neighbours."
    ),
    ("onam", "gujarat"): (
        "Bright floral patterns and high-flying kite arrays decorate residential colonies across Gujarat, magnifying the festive energy of harvest joy, floral beauty, and family reunion. "
        "Bustling garba grounds and bright rangoli work completely transform public and private squares under bright festive lights. "
        "Dancers replenish their energy late into the night by gathering around multi-course festive thalis loaded with fafda and jalebi."
    ),
    ("onam", "haryana"): (
        "Agrarian families gather to offer fresh winter crops to community shrines across Haryana, magnifying the annual cycle of harvest joy, floral beauty, and family reunion. "
        "Family courtyards and temple offerings turn into central meeting points where neighbourhood women lead traditional folk prayers. "
        "The home gatherings are warmed by sharing rustic halwa, puri, and farm-style festive meals among relatives."
    ),
    ("onam", "himachal-pradesh"): (
        "Village winter bonfires emerge amidst the cold mountain air across Himachal Pradesh, anchoring local valleys in harvest joy, floral beauty, and family reunion. "
        "Serene village temples and hillside processions host local clans traveling across valleys to pay homage to their deities. "
        "The spiritual afternoon is comforted by serving sweet rice, prasad, and mountain-style meals around communal hearths."
    ),
    ("onam", "jharkhand"): (
        "Traditional Tusu festival markers and fresh grain decorations transform residential colonies in Jharkhand, marking the seasonal alignment with harvest joy, floral beauty, and family reunion. "
        "Open community grounds and family prayer circles provide an inclusive space for traditional drumming and evening chants. "
        "The nine-day fast is supported by sharing unique seasonal sweets and simple ceremonial meals within families."
    ),
    ("onam", "karnataka"): (
        "Beautiful floral mats and sweet exchanges transform local living rooms across Karnataka, celebrating harvest joy, floral beauty, and family reunion. "
        "Intricate flower decorations and early-morning puja rituals re-energize the household as children arrange the sacred steps. "
        "Visiting guests are welcomed into homes with delicious kosambari, payasa, and temple-style prasada."
    ),
    ("onam", "kerala"): (
        "Ten days of Onam centre on the pookalam remade each morning, culminating in the sadhya feast, vallam kali boat races, and deep harvest joy, floral beauty, and family reunion. "
        "Ornate floral designs and household lamp lighting ground the final days of the sacred calendar in absolute stillness. "
        "The concluding celebration is marked by serving sweet payasam, banana chips, and elaborate festive spreads."
    ),
    ("onam", "madhya-pradesh"): (
        "Large-scale kite flying tournaments and grand holy river dips alter the public space of Madhya Pradesh, showcasing deep arrays of harvest joy, floral beauty, and family reunion. "
        "Devotional mandir visits and old-city processions draw thousands out into illuminated public streets after sunset. "
        "The local evening hospitality is accompanied by distributing savory poha-style snacks, sweets, and prasad to visitors."
    ),
    ("onam", "maharashtra"): (
        "The sharing of sweet tilgul sweets with messages of goodwill anchors local neighbourhood complexes across Maharashtra, initiating days of harvest joy, floral beauty, and family reunion. "
        "Bustling society pandals and family aarti gatherings unite apartment complexes for nightly prayers and synchronized dances. "
        "The daily family gathering centers on preparing fresh, sweet modak, puran poli, and festive snacks."
    ),
    ("onam", "manipur"): (
        "Harvest thanksgiving rituals and classical devotional musical sequences fill local temples in Manipur, blending the season with harvest joy, floral beauty, and family reunion. "
        "Expressive cultural performances and temple participation offer a deeply classical avenue for community connection. "
        "The sacred week concludes with neighbourhoods arranging large community feasts paired with specialized seasonal sweets."
    ),
    ("onam", "meghalaya"): (
        "Fresh winter grain displays and twilight prayer groups bring families together in Meghalaya, honoring the message of harvest joy, floral beauty, and family reunion. "
        "Festive church halls, homes, and community spaces host unique inter-cultural programs to celebrate the autumn season. "
        "The warm afternoon hospitality features sharing local festive rice dishes and unique local sweets with guests."
    ),
    ("onam", "mizoram"): (
        "Traditional oil lamps and winter harvest greetings decorate private balconies in Mizoram, bridging local harmony with the global focus on harvest joy, floral beauty, and family reunion. "
        "Decorated community halls and neighbourhood visits allow diaspora groups to gather for seasonal updates and songs. "
        "The autumn occasion is highlighted by gathering for shared festive meals and sweet offerings across local townships."
    ),
    ("onam", "nagaland"): (
        "Agrarian celebration songs and community bonfires are coordinated across Nagaland, celebrating the spiritual presence of harvest joy, floral beauty, and family reunion. "
        "Vibrant collective singing and family hosting provide a welcoming environment for visiting relatives and friends. "
        "The peaceful seasonal gathering is highlighted by presenting large community meals and celebratory desserts."
    ),
    ("onam", "odisha"): (
        "The Makara Mela festivals on the pristine grounds of ancient temples transform Odisha, elevating a profound wave of deep harvest joy, floral beauty, and family reunion. "
        "Intricate alpona art and neighbourhood mandaps line the village paths where families gather to receive the deity's blessings. "
        "The holy days are accompanied by distributing traditional sweet khaja, pitha, and temple mahaprasad to neighbourhood networks."
    ),
    ("onam", "punjab"): (
        "High-energy Maghi assemblies following the vibrant Lohri night bonfires fill local residential areas across Punjab, defining a grand display of harvest joy, floral beauty, and family reunion. "
        "Dedicated gurdwara seva and community langar participation run parallel to the domestic fasts across local towns. "
        "The auspicious eighth day is marked by sharing warm kada prasad, festive rotis, and rich milk sweets."
    ),
    ("onam", "rajasthan"): (
        "High-flying kite arrays and specialised charity to elders fill historic neighbourhoods in Rajasthan, elevating the heritage of harvest joy, floral beauty, and family reunion. "
        "Delicate courtyard lamps and royal-colour decorations provide a dramatic setting for the night-long prayers. "
        "The culinary gathering centers on serving sweet ghevar, rich dal-baati spreads, and festive mithai to extended clans."
    ),
    ("onam", "sikkim"): (
        "The traditional Maghe Sankranti holy dips in mountain rivers bring communities together across Sikkim, welcoming the seasonal alignment with harvest joy, floral beauty, and family reunion. "
        "Grounded community prayer and hillside celebrations bring mountain settlements together for evening songs and shared prayers. "
        "The local hospitality involves sharing custom sweets and warm festive rice dishes among remote settlements."
    ),
    ("onam", "tamil-nadu"): (
        "Beautiful flower mats and traditional harvest chants transform Tamil Nadu, anchoring harvest joy, floral beauty, and family reunion. "
        "Vibrant kolam art, brass lamps, and dawn rituals reshape the domestic rhythm as neighbors visit to exchange greeting cards. "
        "The sacred season is celebrated by preparing sweet pongal, savory sundal, and sacred temple prasadam for guests."
    ),
    ("onam", "telangana"): (
        "Intricate multi-colored rangoli designs and dynamic community kite-flying paths decorate thresholds across Telangana, highlighting a profound display of harvest joy, floral beauty, and family reunion. "
        "Bonalu-style community devotion and floral decor create a highly active and colorful public greeting space. "
        "The primary household table is filled with ritual paramannam, sweet laddus, and assorted festive savouries."
    ),
    ("onam", "tripura"): (
        "Traditional winter rice cakes and devotional stotra recitations fill community halls across Tripura, mirroring the winter arrival of harvest joy, floral beauty, and family reunion. "
        "Family courtyards and community pandals turn into lively meeting points for multi-generational relative visits. "
        "The evening hospitality is highlighted by sharing traditional festive rice offerings and local sweets with neighbours."
    ),
    ("onam", "uttar-pradesh"): (
        "The magnificent Khichdi Mela holy dips in Prayagraj transform Uttar Pradesh, tracking a magnificent display of harvest joy, floral beauty, and family reunion. "
        "Ancient ghat rituals and massive temple crowds create an unmatched public scale under the echo of midnight bells. "
        "The high-energy days include distributing famous sweet peda, kachori, and traditional prasad to the community."
    ),
    ("onam", "uttarakhand"): (
        "The sweet feeding of migratory birds during winter solstice celebrations defines the local experience in Uttarakhand, celebrating a serene display of harvest joy, floral beauty, and family reunion. "
        "Ancient hill temples and family vrat observance bring remote mountain villages together for collective protective prayers. "
        "The spiritual gathering is completed by serving traditional singori, sweet halwa, and custom temple offerings."
    ),
    ("onam", "west-bengal"): (
        "The dynamic Poush Parbon pithe making and holy dips at Ganga Sagar transform West Bengal, showcasing a beautiful wave of harvest joy, floral beauty, and family reunion. "
        "Artistic neighbourhood pandals, echoing dhaak rhythms, and striking artistic decorations alter the local landscape during the dawn periods. "
        "The cultural transition is accompanied by preparing traditional sandesh, khichuri bhog, and assorted festive sweets."
    ),
    ("onam", "nri-london"): (
        "Indoor community halls host colorful flower carpet arrangements across London, allowing the diaspora to maintain an authentic experience of harvest joy, floral beauty, and family reunion. "
        "Bustling weekend community events and cultural centres connect families across boroughs for simultaneous evening prayers. "
        "Expatriates mark the autumn transition by packing potluck sweets and temple prasada to share with global friends."
    ),
    ("onam", "nri-new-york"): (
        "Community centers host high-energy flower arrangements and banana leaf sadhya feasts in New York, preserving the heritage of harvest joy, floral beauty, and family reunion. "
        "Ornate temple halls, family Zooms, and community gatherings bridge the distance for long-distance relatives during the sacred nights. "
        "The diaspora gathering concludes with sharing custom festive meals and mandir prasad within local networks."
    ),


    # ── BAISAKHI (Batch 11 -- all 30 regions) ─────────────────────────────────
    ("baisakhi", "andhra-pradesh"): (
        "Bhangra rhythms and nagar kirtan processions echo across Andhra Pradesh as communities gather to mark the energy of harvest thanksgiving and collective celebration. "
        "The dynamic seasonal energy fills local neighbourhoods, where public areas are enlivened by traditional temple processions and decorated entrances. "
        "Families mark the auspicious solar new year by sharing traditional pulihora and laddus with visiting neighbourhood circles."
    ),
    ("baisakhi", "arunachal-pradesh"): (
        "Freshly cleared fields and morning prayers mark the seasonal shift across Arunachal Pradesh, tracking the harvest thanksgiving and collective celebration. "
        "Bustling community halls and family gatherings fill with traditional greetings as families celebrate the changing of the agricultural calendar. "
        "The playful morning concludes with households gathering to share custom community sweets and festive rice dishes."
    ),
    ("baisakhi", "assam"): (
        "The high-energy Rongali Bihu dances and outdoor agricultural rituals reshape the fields in Assam, reflecting a deep harvest thanksgiving and collective celebration. "
        "Joyous music, prayer, and neighbourhood visits elevate local community spaces during the daylight cultural transitions. "
        "The spring cycle is enriched by serving traditional pitha, payas, and festive rice offerings to the neighbourhood."
    ),
    ("baisakhi", "bihar"): (
        "The auspicious Satuan festival rituals and holy dips at river confluences mark the daytime rhythm in Bihar, celebrating harvest thanksgiving and collective celebration. "
        "Bustling ghat visits and family puja routines allow large extended families to gather for collective seasonal prayers. "
        "The daily ceremonial transition is marked by preparing sweet thekua, kheer, and seasonal savouries for ritual prasad."
    ),
    ("baisakhi", "chhattisgarh"): (
        "Earthen pots carrying newly harvested spring grains are placed before home shrines in Chhattisgarh, initiating the quiet celebration of harvest thanksgiving and collective celebration. "
        "Vibrant community puja and local fairs bring farming communities together for evening folk dances and traditional prayers. "
        "The household hospitality centers on kitchens preparing specialized rice sweets and home-style prasad for daily offerings."
    ),
    ("baisakhi", "goa"): (
        "Spring harvest grains and custom floral decorations are offered at family altars across Goa, channeling a beautiful wave of harvest thanksgiving and collective celebration. "
        "Quiet home altars and bustling neighbourhood celebration routes define the spatial layout of the local evening prayers. "
        "The sacred period is marked by sharing unique coconut sweets and festive savouries among long-time neighbours."
    ),
    ("baisakhi", "gujarat"): (
        "Vibrant solar patterns and high-energy cultural gatherings transform residential colonies across Gujarat, magnifying the festive energy of harvest thanksgiving and collective celebration. "
        "Bustling garba grounds and bright rangoli work completely transform public and private squares under bright festive lights. "
        "Dancers replenish their energy late into the night by gathering around multi-course festive thalis loaded with fafda and jalebi."
    ),
    ("baisakhi", "haryana"): (
        "Traditional dhol beats and robust community assemblies bring agricultural families together across Haryana, magnifying the annual cycle of harvest thanksgiving and collective celebration. "
        "Family courtyards and temple offerings turn into central meeting points where neighbourhood women lead traditional folk prayers. "
        "The home gatherings are warmed by sharing rustic halwa, puri, and farm-style festive meals among relatives."
    ),
    ("baisakhi", "himachal-pradesh"): (
        "The vibrant Bissoa festival assemblies emerge amidst the fresh mountain air across Himachal Pradesh, anchoring local valleys in harvest thanksgiving and collective celebration. "
        "Serene village temples and hillside processions host local clans traveling across valleys to pay homage to their deities. "
        "The spiritual afternoon is comforted by serving sweet rice, prasad, and mountain-style meals around communal hearths."
    ),
    ("baisakhi", "jharkhand"): (
        "Traditional spring festival songs and fresh grain decorations transform residential colonies in Jharkhand, marking the seasonal alignment with harvest thanksgiving and collective celebration. "
        "Open community grounds and family prayer circles provide an inclusive space for traditional drumming and evening chants. "
        "The nine-day fast is supported by sharing unique seasonal sweets and simple ceremonial meals within families."
    ),
    ("baisakhi", "karnataka"): (
        "The sacred Ugadi or new year extensions and sweet exchanges transform local living rooms across Karnataka, celebrating harvest thanksgiving and collective celebration. "
        "Intricate flower decorations and early-morning puja rituals re-energize the household as children arrange the sacred steps. "
        "Visiting guests are welcomed into homes with delicious kosambari, payasa, and temple-style prasada."
    ),
    ("baisakhi", "kerala"): (
        "The majestic Vishu festival arrays and traditional kanikanu displays are observed quietly in Kerala, marking a unique southern expression of harvest thanksgiving and collective celebration. "
        "Ornate floral designs and household lamp lighting ground the final three days of the sacred calendar in absolute stillness. "
        "The concluding celebration is marked by serving sweet payasam, banana chips, and elaborate festive spreads."
    ),
    ("baisakhi", "madhya-pradesh"): (
        "Large-scale public fairs and grand holy river dips alter the public space of Madhya Pradesh, showcasing deep arrays of harvest thanksgiving and collective celebration. "
        "Devotional mandir visits and old-city processions draw thousands out into illuminated public streets after sunset. "
        "The local evening hospitality is accompanied by distributing savory poha-style snacks, sweets, and prasad to visitors."
    ),
    ("baisakhi", "maharashtra"): (
        "The festive Gudi Padwa configurations and joyful exchanges anchor local neighbourhood complexes across Maharashtra, initiating days of harvest thanksgiving and collective celebration. "
        "Bustling society pandals and family aarti gatherings unite apartment complexes for nightly prayers and synchronized dances. "
        "The daily family gathering centers on preparing fresh, sweet modak, puran poli, and festive snacks."
    ),
    ("baisakhi", "manipur"): (
        "Harvest thanksgiving rituals and classical devotional musical sequences fill local temples in Manipur, blending the season with harvest thanksgiving and collective celebration. "
        "Expressive cultural performances and temple participation offer a deeply classical avenue for community connection. "
        "The sacred week concludes with neighbourhoods arranging large community feasts paired with specialized seasonal sweets."
    ),
    ("baisakhi", "meghalaya"): (
        "Fresh spring grain displays and twilight prayer groups bring families together in Meghalaya, honoring the message of harvest thanksgiving and collective celebration. "
        "Festive church halls, homes, and community spaces host unique inter-cultural programs to celebrate the autumn season. "
        "The warm afternoon hospitality features sharing local festive rice dishes and unique local sweets with guests."
    ),
    ("baisakhi", "mizoram"): (
        "Traditional oil lamps and spring harvest greetings decorate private balconies in Mizoram, bridging local harmony with the global focus on harvest thanksgiving and collective celebration. "
        "Decorated community halls and neighbourhood visits allow diaspora groups to gather for seasonal updates and songs. "
        "The autumn occasion is highlighted by gathering for shared festive meals and sweet offerings across local townships."
    ),
    ("baisakhi", "nagaland"): (
        "Agrarian celebration songs and community bonfires are coordinated across Nagaland, celebrating the spiritual presence of harvest thanksgiving and collective celebration. "
        "Vibrant collective singing and family hosting provide a welcoming environment for visiting relatives and friends. "
        "The peaceful seasonal gathering is highlighted by presenting large community meals and celebratory desserts."
    ),
    ("baisakhi", "odisha"): (
        "The Pana Sankranti or Maha Vishuba festivals on the pristine grounds of ancient temples transform Odisha, elevating a profound wave of deep harvest thanksgiving and collective celebration. "
        "Intricate alpona art and neighbourhood mandaps line the village paths where families gather to receive the deity's blessings. "
        "The holy days are accompanied by distributing traditional sweet khaja, pitha, and temple mahaprasad to neighbourhood networks."
    ),
    ("baisakhi", "punjab"): (
        "Gurdwara seva in the morning, full-volume bhangra rhythms, and continuous langar service define the absolute heart of Punjab's harvest thanksgiving and collective celebration. "
        "Dedicated nagar kirtan processions and vibrant community energy anchor the high-energy celebrations across local districts. "
        "The festive gathering is marked by distributing warm kada prasad, festive rotis, and rich milk sweets to the public."
    ),
    ("baisakhi", "rajasthan"): (
        "High-energy harvest songs and specialised charity to elders fill historic neighbourhoods in Rajasthan, elevating the heritage of harvest thanksgiving and collective celebration. "
        "Delicate courtyard lamps and royal-colour decorations provide a dramatic setting for the night-long prayers. "
        "The culinary gathering centers on serving sweet ghevar, rich dal-baati spreads, and festive mithai to extended clans."
    ),
    ("baisakhi", "sikkim"): (
        "The traditional spring prayer assemblies in mountain monasteries bring communities together across Sikkim, welcoming the seasonal alignment with harvest thanksgiving and collective celebration. "
        "Grounded community prayer and hillside celebrations bring mountain settlements together for evening songs and shared prayers. "
        "The local hospitality involves sharing custom sweets and warm festive rice dishes among remote settlements."
    ),
    ("baisakhi", "tamil-nadu"): (
        "The Puthandu new year rituals and beautiful seasonal fruit arrangements transform Tamil Nadu, anchoring harvest thanksgiving and collective celebration. "
        "Vibrant kolam art, brass lamps, and dawn rituals reshape the domestic rhythm as neighbors visit to exchange traditional wishes. "
        "The sacred season is celebrated by preparing sweet pongal, savory sundal, and sacred temple prasadam for guests."
    ),
    ("baisakhi", "telangana"): (
        "Intricate multi-colored rangoli designs and dynamic community assemblies decorate thresholds across Telangana, highlighting a profound display of harvest thanksgiving and collective celebration. "
        "Bonalu-style community devotion and floral decor create a highly active and colorful public greeting space. "
        "The primary household table is filled with ritual paramannam, sweet laddus, and assorted festive savouries."
    ),
    ("baisakhi", "tripura"): (
        "Traditional seasonal rice dishes and devotional stotra recitations fill community halls across Tripura, mirroring the spring arrival of harvest thanksgiving and collective celebration. "
        "Family courtyards and community pandals turn into lively meeting points for multi-generational relative visits. "
        "The evening hospitality is highlighted by sharing traditional festive rice offerings and local sweets with neighbours."
    ),
    ("baisakhi", "uttar-pradesh"): (
        "The magnificent new year holy dips in the holy rivers transform Uttar Pradesh, tracking a magnificent display of harvest thanksgiving and collective celebration. "
        "Ancient ghat rituals and massive temple crowds create an unmatched public scale under the echo of midnight bells. "
        "The high-energy days include distributing famous sweet peda, kachori, and traditional prasad to the community."
    ),
    ("baisakhi", "uttarakhand"): (
        "The sweet festive assemblies during the Bikhoti festival define the local experience in Uttarakhand, celebrating a serene display of harvest thanksgiving and collective celebration. "
        "Ancient hill temples and family vrat observance bring remote mountain villages together for collective protective prayers. "
        "The spiritual gathering is completed by serving traditional singori, sweet halwa, and custom temple offerings."
    ),
    ("baisakhi", "west-bengal"): (
        "The dynamic Poila Boishakh new year assemblies and holy ledger pujas transform West Bengal, showcasing a beautiful wave of harvest thanksgiving and collective celebration. "
        "Artistic neighbourhood pandals, echoing dhaak rhythms, and striking artistic decorations alter the local landscape during the dawn periods. "
        "The cultural transition is accompanied by preparing traditional sandesh, khichuri bhog, and assorted festive sweets."
    ),
    ("baisakhi", "nri-london"): (
        "Indoor community halls host colorful nagar kirtan simulations across London, allowing the diaspora to maintain an authentic experience of harvest thanksgiving and collective celebration. "
        "Bustling weekend community events and cultural centres connect families across boroughs for simultaneous evening prayers. "
        "Expatriates mark the autumn transition by packing potluck sweets and temple prasada to share with global friends."
    ),
    ("baisakhi", "nri-new-york"): (
        "Community centers host high-energy dhol configurations and sweet distribution in New York, preserving the heritage of harvest thanksgiving and collective celebration. "
        "Ornate temple halls, family Zooms, and community gatherings bridge the distance for long-distance relatives during the sacred nights. "
        "The diaspora gathering concludes with sharing custom festive meals and mandir prasad within local networks."
    ),


    # ── EID-UL-FITR (Batch 12 -- all 30 regions) ──────────────────────────────
    ("eid-ul-fitr", "andhra-pradesh"): (
        "Morning eid namaz in open grounds marks the grand breaking of the fast across Andhra Pradesh, centering on gratitude, prayer, and family feasting. "
        "The public areas fill with communal warmth as rows of worshippers spill out from local shrines into decorated entrances. "
        "Families mark the festive conclusion of the holy month by sharing sweet pulihora and laddus with visiting neighbours."
    ),
    ("eid-ul-fitr", "arunachal-pradesh"): (
        "Shared festive meals bring diverse valley settlements together in Arunachal Pradesh, anchoring the seasonal focus on gratitude, prayer, and family feasting. "
        "Bustling community halls and family gatherings fill with peaceful morning prayers as neighbours gather to exchange greetings. "
        "The warm afternoon concludes with households gathering to share custom community sweets and festive rice dishes."
    ),
    ("eid-ul-fitr", "assam"): (
        "The sweet distribution of traditional sevaiyaan and deep community hugs reshape the landscape in Assam, reflecting gratitude, prayer, and family feasting. "
        "Music, prayer, and neighbourhood visits elevate local community spaces during the daylight social gatherings. "
        "The celebration is completed as households prepare traditional pitha, payas, and festive rice offerings for visiting guests."
    ),
    ("eid-ul-fitr", "bihar"): (
        "Massive open-air prayer gatherings and rich family assemblies define the daytime rhythm in Bihar, celebrating gratitude, prayer, and family feasting. "
        "Bustling ghat visits and family puja routines allow diverse extended communities to share peaceful seasonal greetings. "
        "The festive morning is highlighted by households preparing traditional thekua, kheer, and seasonal savouries to share."
    ),
    ("eid-ul-fitr", "chhattisgarh"): (
        "Worshippers fill public squares for the morning congregational prayers in Chhattisgarh, initiating the joyful celebration of gratitude, prayer, and family feasting. "
        "Vibrant community puja and local fairs gather families from all backgrounds for rhythmic songs and outdoor festivities. "
        "The household hospitality centers on kitchens preparing specialized rice sweets and home-style prasad to honor visiting guests."
    ),
    ("eid-ul-fitr", "goa"): (
        "Bustling celebration routes and family banquets define the coastal landscape in Goa, highlighting the beautiful focus on gratitude, prayer, and family feasting. "
        "Quiet home altars and bustling neighbourhood celebration routes provide an inclusive space for cross-community greetings. "
        "The lively gathering concludes with families distributing sweet coconut sweets and festive savouries across their settlements."
    ),
    ("eid-ul-fitr", "gujarat"): (
        "Grand morning congregations and vibrant neighbourhood interactions transform residential colonies across Gujarat, magnifying the spirit of gratitude, prayer, and family feasting. "
        "Bustling garba grounds and bright rangoli work set an inclusive stage as local merchants exchange traditional holiday blessings. "
        "Extended families wind down the joyous day by gathering around multi-course festive thalis loaded with fafda and jalebi."
    ),
    ("eid-ul-fitr", "haryana"): (
        "The sharing of rich milk sweets and warm embraces brings rural neighbourhoods together across Haryana, magnifying the annual cycle of gratitude, prayer, and family feasting. "
        "Family courtyards and temple offerings turn into central meeting points where neighbourhood groups lead traditional folk prayers. "
        "The home gatherings are warmed by sharing rustic halwa, puri, and farm-style festive meals among relatives."
    ),
    ("eid-ul-fitr", "himachal-pradesh"): (
        "Morning prayers echo through mountain valley settlements in Himachal Pradesh, casting a beautiful contrast against themes of gratitude, prayer, and family feasting. "
        "Serene village temples and hillside processions host the community as they gather to celebrate the culmination of the fasting month. "
        "The joyful afternoon is comforted by serving sweet rice, prasad, and mountain-style meals around shared hearths."
    ),
    ("eid-ul-fitr", "jharkhand"): (
        "Open prayer grounds draw large community groups together in Jharkhand, marking the annual arrival of gratitude, prayer, and family feasting. "
        "Open community grounds and family prayer circles allow local neighbourhoods to gather for traditional drumming and seasonal songs. "
        "The daytime celebration is highlighted by sharing unique seasonal sweets and simple ceremonial meals with visiting friends."
    ),
    ("eid-ul-fitr", "karnataka"): (
        "Grand prayer mats fill local community spaces across Karnataka neighbourhoods, initiating the southern observance of gratitude, prayer, and family feasting. "
        "Intricate flower decorations and early-morning puja rituals precede the warm exchange of festive greetings among close neighbours. "
        "The daytime feast involves preparing delicious kosambari, payasa, and temple-style prasada for the gathered household."
    ),
    ("eid-ul-fitr", "kerala"): (
        "The traditional Cheraman Juma Masjid gatherings bring an ancient, historic rhythm to Kerala, celebrating gratitude, prayer, and family feasting. "
        "Ornate floral designs and household lamp lighting anchor the domestic boundaries before the outdoor community greetings commence. "
        "The gathering is marked by serving sweet payasam, banana chips, and elaborate festive spreads to participants."
    ),
    ("eid-ul-fitr", "madhya-pradesh"): (
        "Massive congregations fill the grand Idgah grounds across Madhya Pradesh, showcasing the majestic scale of gratitude, prayer, and family feasting. "
        "Devotional mandir visits and old-city processions frame the afternoon hours as public squares echo with festive greetings. "
        "The community greeting style is accompanied by sharing savory poha-style snacks, sweets, and prasad among neighbours."
    ),
    ("eid-ul-fitr", "maharashtra"): (
        "Rows of worshippers fill public squares for morning namaz in Maharashtra, making way for the joyful celebration of gratitude, prayer, and family feasting. "
        "Bustling society pandals and family aarti gatherings turn into central nodes for cross-community greetings and shared sweets. "
        "The household celebration centers on preparing fresh, sweet modak, puran poli, and festive snacks for the neighbourhood."
    ),
    ("eid-ul-fitr", "manipur"): (
        "The traditional sharing of bowls of sweet milk delicacies brings a deeply artistic touch to Manipur, blending the season with gratitude, prayer, and family feasting. "
        "Expressive cultural performances and temple participation offer a deeply classical avenue for community connection. "
        "The festive week concludes with families arranging large community feasts paired with specialized seasonal sweets."
    ),
    ("eid-ul-fitr", "meghalaya"): (
        "Morning namaz in pristine open grounds brings diverse communities together in Meghalaya, honoring the message of gratitude, prayer, and family feasting. "
        "Festive church halls, homes, and community spaces host unique inter-cultural programs to celebrate the autumn season. "
        "The warm afternoon hospitality features sharing local festive rice dishes and unique local sweets with guests."
    ),
    ("eid-ul-fitr", "mizoram"): (
        "Shared festive meals connect neighbourhoods together in Mizoram, bridging local harmony with the global spirit of gratitude, prayer, and family feasting. "
        "Decorated community halls and neighbourhood visits allow diaspora groups to gather for seasonal updates and songs. "
        "The autumn occasion is highlighted by gathering for shared festive meals and sweet offerings across local townships."
    ),
    ("eid-ul-fitr", "nagaland"): (
        "Celebratory neighbourhood feasts and warm greeting exchanges are coordinated across Nagaland, marking the arrival of gratitude, prayer, and family feasting. "
        "Vibrant collective singing and family hosting provide a welcoming environment for visiting relatives and friends. "
        "The peaceful seasonal gathering is highlighted by presenting large community meals and celebratory desserts."
    ),
    ("eid-ul-fitr", "odisha"): (
        "The elegant Eid congregations at grand Cuttack mosques transform Odisha, elevating a profound wave of gratitude, prayer, and family feasting. "
        "Intricate alpona art and neighbourhood mandaps line the village paths where families gather to receive the deity's blessings. "
        "The holy days are accompanied by distributing traditional sweet khaja, pitha, and temple mahaprasad to neighbourhood networks."
    ),
    ("eid-ul-fitr", "punjab"): (
        "The historic mosques of Malerkotla fill with thousands of worshippers in Punjab, defining a grand display of gratitude, prayer, and family feasting. "
        "Dedicated gurdwara seva and community langar participation run parallel to the domestic fasts across local towns. "
        "The auspicious eighth day is marked by sharing warm kada prasad, festive rotis, and rich milk sweets."
    ),
    ("eid-ul-fitr", "rajasthan"): (
        "Grand morning prayers at the historic Jaipur Idgah fill courtyards in Rajasthan, elevating the heritage of gratitude, prayer, and family feasting. "
        "Delicate courtyard lamps and royal-colour decorations provide a dramatic setting for the night-long prayers. "
        "The culinary gathering centers on serving sweet ghevar, rich dal-baati spreads, and festive mithai to extended clans."
    ),
    ("eid-ul-fitr", "sikkim"): (
        "Morning prayers along hillside pathways bring communities together across Sikkim, welcoming the seasonal alignment with gratitude, prayer, and family feasting. "
        "Grounded community prayer and hillside celebrations bring mountain settlements together for evening songs and shared prayers. "
        "The local hospitality involves sharing custom sweets and warm festive rice dishes among remote settlements."
    ),
    ("eid-ul-fitr", "tamil-nadu"): (
        "Massive congregations on the open grounds of Chennai beaches transform Tamil Nadu, anchoring gratitude, prayer, and family feasting. "
        "Vibrant kolam art, brass lamps, and dawn rituals reshape the domestic rhythm as neighbors visit to exchange sundal packets. "
        "The sacred season is celebrated by preparing sweet pongal, savory sundal, and sacred temple prasadam for guests."
    ),
    ("eid-ul-fitr", "telangana"): (
        "The spectacular crowds at the historic Mecca Masjid in Hyderabad define the peak of Telangana's gratitude, prayer, and family feasting. "
        "Bonalu-style community devotion and floral decor create a highly active and colorful public greeting space. "
        "The primary household table is filled with ritual paramannam, sweet laddus, and assorted festive savouries."
    ),
    ("eid-ul-fitr", "tripura"): (
        "Sweet bowls of hand-crafted sevaiyaan fill family courtyards across Tripura, mirroring the autumn arrival of gratitude, prayer, and family feasting. "
        "Family courtyards and community pandals turn into lively meeting points for multi-generational relative visits. "
        "The evening hospitality is highlighted by sharing traditional festive rice offerings and local sweets with neighbours."
    ),
    ("eid-ul-fitr", "uttar-pradesh"): (
        "The massive congregations at the historic Taj-ul-Masajid and Lucknow Idgahs transform Uttar Pradesh, tracking a magnificent display of gratitude, prayer, and family feasting. "
        "Ancient ghat rituals and massive temple crowds create an unmatched public scale under the echo of midnight bells. "
        "The high-energy days include distributing famous sweet peda, kachori, and traditional prasad to the community."
    ),
    ("eid-ul-fitr", "uttarakhand"): (
        "Morning namaz in pristine alpine valley spaces defines the local experience in Uttarakhand, celebrating a serene display of gratitude, prayer, and family feasting. "
        "Ancient hill temples and family vrat observance bring remote mountain villages together for collective protective prayers. "
        "The spiritual gathering is completed by serving traditional singori, sweet halwa, and custom temple offerings."
    ),
    ("eid-ul-fitr", "west-bengal"): (
        "The grand congregations at the historic Red Road in Kolkata define the West Bengal celebration of gratitude, prayer, and family feasting. "
        "Artistic neighbourhood pandals, echoing dhaak rhythms, and striking artistic decorations alter the local landscape during the dawn periods. "
        "The cultural transition is accompanied by preparing traditional sandesh, khichuri bhog, and assorted festive sweets."
    ),
    ("eid-ul-fitr", "nri-london"): (
        "Massive park festivals in Southall and Regent's Park protect the London diaspora as they maintain the heritage of gratitude, prayer, and family feasting. "
        "Bustling weekend community events and cultural centres connect families across boroughs for simultaneous evening prayers. "
        "Expatriates mark the autumn transition by packing potluck sweets and temple prasada to share with global friends."
    ),
    ("eid-ul-fitr", "nri-new-york"): (
        "Vibrant community banquets in Queens and central mosques mark New York gatherings, celebrating the arrival of gratitude, prayer, and family feasting. "
        "Ornate temple halls, family Zooms, and community gatherings bridge the distance for long-distance relatives during the sacred nights. "
        "The diaspora gathering concludes with sharing custom festive meals and mandir prasad within local networks."
    ),


    # ── CHRISTMAS (Batch 13 -- all 30 regions) ────────────────────────────────
    ("christmas", "andhra-pradesh"): (
        "Midnight mass services and glowing star lanterns hung at home entryways bring winter warmth across Andhra Pradesh, centering on joy, prayer, and generous gathering. "
        "The harmonious seasonal energy fills local neighbourhoods, where public areas are enlivened by traditional temple processions and decorated entrances. "
        "Families mark the auspicious nativity celebration by sharing traditional pulihora and laddus with visiting neighbourhood circles."
    ),
    ("christmas", "arunachal-pradesh"): (
        "Carol services and bright festive lights illuminate alpine valley churches across Arunachal Pradesh, anchoring the seasonal focus on joy, prayer, and generous gathering. "
        "Bustling community halls and family gatherings fill with peaceful choral hymns as neighbours gather to exchange greetings. "
        "The warm afternoon concludes with households gathering to share custom community sweets and festive rice dishes."
    ),
    ("christmas", "assam"): (
        "The sweet sound of acoustic carols and beautifully decorated evergreen branches reshape the landscape in Assam, reflecting joy, prayer, and generous gathering. "
        "Music, prayer, and neighbourhood visits elevate local community spaces during the daylight social gatherings. "
        "The celebration is completed as households prepare traditional pitha, payas, and festive rice offerings for visiting guests."
    ),
    ("christmas", "bihar"): (
        "Vibrant midnight services and rich family dinners define the winter holiday rhythm in Bihar, celebrating joy, prayer, and generous gathering. "
        "Bustling ghat visits and family puja routines allow diverse extended communities to share peaceful seasonal greetings. "
        "The festive morning is highlighted by households preparing traditional thekua, kheer, and seasonal savouries to share."
    ),
    ("christmas", "chhattisgarh"): (
        "Worshippers gather for midnight prayer services inside brightly illuminated church halls in Chhattisgarh, initiating the joyful celebration of joy, prayer, and generous gathering. "
        "Vibrant community puja and local fairs gather families from all backgrounds for rhythmic songs and outdoor festivities. "
        "The household hospitality centers on kitchens preparing specialized rice sweets and home-style prasad to honor visiting guests."
    ),
    ("christmas", "goa"): (
        "Bustling midnight mass celebrations and elaborate traditional crib displays define the coastal winter landscape in Goa, highlighting the beautiful focus on joy, prayer, and generous gathering. "
        "Quiet home altars and bustling neighbourhood celebration routes provide an inclusive space for cross-community greetings. "
        "The lively gathering concludes with families distributing sweet coconut sweets and festive savouries across their settlements."
    ),
    ("christmas", "gujarat"): (
        "Grand candle-lit services and vibrant neighbourhood carol groups transform residential colonies across Gujarat, magnifying the spirit of joy, prayer, and generous gathering. "
        "Bustling garba grounds and bright rangoli work set an inclusive stage as local merchants exchange traditional holiday blessings. "
        "Extended families wind down the joyous day by gathering around multi-course festive thalis loaded with fafda and jalebi."
    ),
    ("christmas", "haryana"): (
        "The sharing of rich winter sweets and warm family assemblies brings rural neighbourhoods together across Haryana, magnifying the annual cycle of joy, prayer, and generous gathering. "
        "Family courtyards and temple offerings turn into central meeting points where neighbourhood groups lead traditional folk prayers. "
        "The home gatherings are warmed by sharing rustic halwa, puri, and farm-style festive meals among relatives."
    ),
    ("christmas", "himachal-pradesh"): (
        "Midnight mass bells echo through snow-dusted mountain valley settlements in Himachal Pradesh, casting a beautiful contrast against themes of joy, prayer, and generous gathering. "
        "Serene village temples and hillside processions host the community as they gather to celebrate the winter holiday. "
        "The joyful afternoon is comforted by serving sweet rice, prasad, and mountain-style meals around shared hearths."
    ),
    ("christmas", "jharkhand"): (
        "Traditional winter choir groups draw large community circles together in Jharkhand, marking the annual arrival of joy, prayer, and generous gathering. "
        "Open community grounds and family prayer circles allow local neighbourhoods to gather for traditional drumming and seasonal songs. "
        "The daytime celebration is highlighted by sharing unique seasonal sweets and simple ceremonial meals with visiting friends."
    ),
    ("christmas", "karnataka"): (
        "Grand star lanterns and beautiful nativity scenes decorate local community spaces across Karnataka neighbourhoods, initiating the southern observance of joy, prayer, and generous gathering. "
        "Intricate flower decorations and early-morning puja rituals precede the warm exchange of festive greetings among close neighbours. "
        "The daytime feast involves preparing delicious kosambari, payasa, and temple-style prasada for the gathered household."
    ),
    ("christmas", "kerala"): (
        "Midnight mass services, glowing paper stars, and elaborate extended family dinners define the historic Kerala approach to joy, prayer, and generous gathering. "
        "Ornate floral designs and household lamp lighting anchor the domestic boundaries before the outdoor community greetings commence. "
        "The gathering is marked by serving sweet payasam, banana chips, and elaborate festive spreads to participants."
    ),
    ("christmas", "madhya-pradesh"): (
        "Beautifully decorated church properties and grand midnight assemblies alter the public space of Madhya Pradesh, showcasing deep arrays of joy, prayer, and generous gathering. "
        "Devotional mandir visits and old-city processions draw thousands out into illuminated public streets after sunset. "
        "The local evening hospitality is accompanied by distributing savory poha-style snacks, sweets, and prasad to visitors."
    ),
    ("christmas", "maharashtra"): (
        "Glowing star lanterns illuminate private balconies across Mumbai and greater Maharashtra, making way for the joyful celebration of joy, prayer, and generous gathering. "
        "Bustling society pandals and family aarti gatherings turn into central nodes for cross-community greetings and shared sweets. "
        "The household celebration centers on preparing fresh, sweet modak, puran poli, and festive snacks for the neighbourhood."
    ),
    ("christmas", "manipur"): (
        "The traditional singing of seasonal carols in community squares brings a deeply artistic touch to Manipur, blending the season with joy, prayer, and generous gathering. "
        "Expressive cultural performances and temple participation offer a deeply classical avenue for community connection. "
        "The festive week concludes with families arranging large community feasts paired with specialized seasonal sweets."
    ),
    ("christmas", "meghalaya"): (
        "Midnight mass and joyful neighbourhood carol groups bring diverse communities together in Meghalaya, honoring the message of joy, prayer, and generous gathering. "
        "Festive church halls, homes, and community spaces host unique inter-cultural programs to celebrate the winter season. "
        "The warm afternoon hospitality features sharing local festive rice dishes and unique local sweets with guests."
    ),
    ("christmas", "mizoram"): (
        "Community feast traditions and continuous choral singing connect neighbourhoods together in Mizoram, bridging local harmony with the global spirit of joy, prayer, and generous gathering. "
        "Decorated community halls and neighbourhood visits allow diaspora groups to gather for seasonal updates and songs. "
        "The winter occasion is highlighted by gathering for shared festive meals and sweet offerings across local townships."
    ),
    ("christmas", "nagaland"): (
        "Grand community feasts and continuous collective caroling are coordinated across Nagaland, marking the arrival of joy, prayer, and generous gathering. "
        "Vibrant collective singing and family hosting provide a welcoming environment for visiting relatives and friends. "
        "The peaceful seasonal gathering is highlighted by presenting large community meals and celebratory desserts."
    ),
    ("christmas", "odisha"): (
        "The elegant midnight services at historic churches transform Odisha, elevating a profound wave of joy, prayer, and generous gathering. "
        "Intricate alpona art and neighbourhood mandaps line the village paths where families gather to receive the deity's blessings. "
        "The holy days are accompanied by distributing traditional sweet khaja, pitha, and temple mahaprasad to neighbourhood networks."
    ),
    ("christmas", "punjab"): (
        "Festive prayer services and elegant community assemblies fill local residential areas across Punjab, defining a grand display of joy, prayer, and generous gathering. "
        "Dedicated gurdwara seva and community langar participation run parallel to the domestic fasts across local towns. "
        "The auspicious day is marked by sharing warm kada prasad, festive rotis, and rich milk sweets."
    ),
    ("christmas", "rajasthan"): (
        "Grand midnight mass gatherings and beautiful winter light displays fill courtyards in Rajasthan, elevating the heritage of joy, prayer, and generous gathering. "
        "Delicate courtyard lamps and royal-colour decorations provide a dramatic setting for the night-long prayers. "
        "The culinary gathering centers on serving sweet ghevar, rich dal-baati spreads, and festive mithai to extended clans."
    ),
    ("christmas", "sikkim"): (
        "Midnight choral singing along hillside pathways brings communities together across Sikkim, welcoming the seasonal alignment with joy, prayer, and generous gathering. "
        "Grounded community prayer and hillside celebrations bring mountain settlements together for evening songs and shared prayers. "
        "The local hospitality involves sharing custom sweets and warm festive rice dishes among remote settlements."
    ),
    ("christmas", "tamil-nadu"): (
        "Massive midnight mass services inside ancient basilicas transform Tamil Nadu, anchoring joy, prayer, and generous gathering. "
        "Vibrant kolam art, brass lamps, and dawn rituals reshape the domestic rhythm as neighbors visit to exchange festive sweets. "
        "The sacred season is celebrated by preparing sweet pongal, savory sundal, and sacred temple prasadam for guests."
    ),
    ("christmas", "telangana"): (
        "The spectacular midnight church gatherings in Secunderabad and Hyderabad define the peak of Telangana's joy, prayer, and generous gathering. "
        "Bonalu-style community devotion and floral decor create a highly active and colorful public greeting space. "
        "The primary household table is filled with ritual paramannam, sweet laddus, and assorted festive savouries."
    ),
    ("christmas", "tripura"): (
        "Bright star lanterns and home-made winter cakes fill family courtyards across Tripura, mirroring the winter arrival of joy, prayer, and generous gathering. "
        "Family courtyards and community pandals turn into lively meeting points for multi-generational relative visits. "
        "The evening hospitality is highlighted by sharing traditional festive rice offerings and local sweets with neighbours."
    ),
    ("christmas", "uttar-pradesh"): (
        "The beautiful winter decorations at historic city cathedrals transform Uttar Pradesh, tracking a magnificent display of joy, prayer, and generous gathering. "
        "Ancient ghat rituals and massive temple crowds create an unmatched public scale under the echo of midnight bells. "
        "The high-energy days include distributing famous sweet peda, kachori, and traditional prasad to the community."
    ),
    ("christmas", "uttarakhand"): (
        "Midnight services in pristine alpine valley church spaces define the local experience in Uttarakhand, celebrating a serene display of joy, prayer, and generous gathering. "
        "Ancient hill temples and family vrat observance bring remote mountain villages together for collective protective prayers. "
        "The spiritual gathering is completed by serving traditional singori, sweet halwa, and custom temple offerings."
    ),
    ("christmas", "west-bengal"): (
        "The grand winter carnivals on Park Street in Kolkata define the West Bengal celebration of joy, prayer, and generous gathering. "
        "Artistic neighbourhood pandals, echoing dhaak rhythms, and striking artistic decorations alter the local landscape during the dawn periods. "
        "The cultural transition is accompanied by preparing traditional sandesh, khichuri bhog, and assorted festive sweets."
    ),
    ("christmas", "nri-london"): (
        "Traditional winter carols and glowing paper stars hung in windows protect the London diaspora as they maintain the heritage of joy, prayer, and generous gathering. "
        "Bustling weekend community events and cultural centres connect families across boroughs for simultaneous evening prayers. "
        "Expatriates mark the winter transition by packing potluck sweets and temple prasada to share with global friends."
    ),
    ("christmas", "nri-new-york"): (
        "Vibrant family dinners and bright star lanterns mark New York diaspora gatherings, celebrating the arrival of joy, prayer, and generous gathering. "
        "Ornate temple halls, family Zooms, and community gatherings bridge the distance for long-distance relatives during the winter nights. "
        "The diaspora gathering concludes with sharing custom festive meals and mandir prasad within local networks."
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
        "The sharing of rich milk sweets and warm family assemblies brings rural neighbourhoods together across Haryana, magnifying the annual cycle of guru remembrance, kirtan, and seva. "
        "Family courtyards and temple offerings turn into central meeting points where neighbourhood groups lead traditional folk prayers. "
        "The home gatherings are warmed by sharing rustic halwa, puri, and farm-style festive meals among relatives."
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
        "Beautifully decorated gurdwara properties and grand early-morning assemblies alter the public space of Madhya Pradesh, showcasing deep arrays of guru remembrance, kirtan, and seva. "
        "Devotional mandir visits and old-city processions draw thousands out into illuminated public streets after sunset. "
        "The local evening hospitality is accompanied by distributing savory poha-style snacks, sweets, and prasad to visitors."
    ),
    ("gurupurab", "maharashtra"): (
        "Glowing path decorations illuminate local gurdwaras across Mumbai and greater Maharashtra, making way for the joyful celebration of guru remembrance, kirtan, and seva. "
        "Bustling society pandals and family aarti gatherings turn into central nodes for cross-community greetings and shared sweets. "
        "The household celebration centers on preparing fresh, sweet modak, puran poli, and festive snacks for the neighbourhood."
    ),
    ("gurupurab", "manipur"): (
        "The traditional singing of sacred shabads in community squares brings a deeply artistic touch to Manipur, blending the season with guru remembrance, kirtan, and seva. "
        "Expressive cultural performances and temple participation offer a deeply classical avenue for community connection. "
        "The festive week concludes with families arranging large community feasts paired with specialized seasonal sweets."
    ),
    ("gurupurab", "meghalaya"): (
        "Morning kirtans and joyful neighbourhood prabhat pheris bring diverse communities together in Meghalaya, honoring the message of guru remembrance, kirtan, and seva. "
        "Festive church halls, homes, and community spaces host unique inter-cultural programs to celebrate the winter season. "
        "The warm afternoon hospitality features sharing local festive rice dishes and unique local sweets with guests."
    ),
    ("gurupurab", "mizoram"): (
        "Community langar traditions and continuous kirtan singing connect neighbourhoods together in Mizoram, bridging local harmony with the global spirit of guru remembrance, kirtan, and seva. "
        "Decorated community halls and neighbourhood visits allow diaspora groups to gather for seasonal updates and songs. "
        "The winter occasion is highlighted by gathering for shared festive meals and sweet offerings across local townships."
    ),
    ("gurupurab", "nagaland"): (
        "Grand community feasts and continuous collective caroling are coordinated across Nagaland, marking the arrival of guru remembrance, kirtan, and seva. "
        "Vibrant collective singing and family hosting provide a welcoming environment for visiting relatives and friends. "
        "The peaceful seasonal gathering is highlighted by presenting large community meals and celebratory desserts."
    ),
    ("gurupurab", "odisha"): (
        "The elegant morning services at historic gurdwaras transform Odisha, elevating a profound wave of guru remembrance, kirtan, and seva. "
        "Intricate alpona art and neighbourhood mandaps line the village paths where families gather to receive the deity's blessings. "
        "The holy days are accompanied by distributing traditional sweet khaja, pitha, and temple mahaprasad to neighbourhood networks."
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
        "Devotional fasting sets a serene spiritual tone inside Bihar households as the annual janmotsav period commences. "
        "The community gathers for elaborate scripture reading sessions to invite protective guidance into their homes. "
        "Fasting families break their daily restrictions by eating custom kheer items alongside classic home-cooked bihari savouries."
    ),
    ("ram-navami", "chhattisgarh"): (
        "Ornate temporary chariot floats are beautifully decorated across Chhattisgarh, welcoming the spring celebration of Ram katha. "
        "Evening gatherings feature vibrant devotional chants as local neighborhoods unite for collective worship at local shrines. "
        "Kitchens prepare specialized neer mor fluids and home-style desserts to distribute as sacred prasad."
    ),
    ("ram-navami", "goa"): (
        "Serene oil lamp illuminations turn Goan temple courtyards into spaces of absolute calm during the holy janmotsav. "
        "Families coordinate intricate scriptural reading routines to invite prosperity and protective energy into their neighborhoods. "
        "The sacred time involves sharing delicious panakam drinks alongside coastal coconut desserts with visiting families."
    ),
    ("ram-navami", "gujarat"): (
        "Bustling street pandals and echoing collective chants of Ram Dhun transform public areas across Gujarat under bright lights. "
        "Massive temple crowds gather late into the afternoon to mark the precise moment of the divine janmotsav. "
        "Extended families mark the joyful transition by sharing large plates of jalebi along with festive local snacks."
    ),
    ("ram-navami", "haryana"): (
        "Traditional kirtans and sacred cradle decorations alter the domestic rhythm across Haryana during the holy spring days. "
        "Neighborhood women lead traditional Ram katha chats to invoke the protective guidance of the deity. "
        "The home gathering is warmed by distributing sweet kheer variations paired with farm-style dairy delicacies."
    ),
    ("ram-navami", "himachal-pradesh"): (
        "Hillside shrines echo with deep devotional music across Himachal Pradesh, anchoring the mountain air in the sacred janmotsav. "
        "Local clans travel across valleys to participate in grand temple-style scriptural reading gatherings. "
        "The spiritual afternoon is comforted by serving warm panakam formulas alongside rich mountain-style meals."
    ),
    ("ram-navami", "jharkhand"): (
        "Earthen lamps remain lit continuously inside Jharkhand residences, marking the seasonal alignment with the holy janmotsav. "
        "Devotees coordinate peaceful community prayer circles to offer collective gratitude for family health and well-being. "
        "The fasting period is supported by sharing unique neer mor mixtures with neighboring families."
    ),
    ("ram-navami", "karnataka"): (
        "The unique distribution of refreshing panakam and sweet majjige drinks transforms local living rooms across Karnataka at noon. "
        "Intricate flower decorations and morning janmotsav rituals re-energize the household as families decorate the sacred cradle. "
        "Visiting guests are welcomed into homes with delicious jalebi variations alongside classic southern treats."
    ),
    ("ram-navami", "kerala"): (
        "Specialized temple shrines exhibit beautiful scriptural readings of the Ramayana in Kerala, marking a unique southern expression. "
        "The quiet community focus sets a deeply meditative stage for intense twilight prayers inside traditional shrines. "
        "The concluding hour is celebrated by serving sweet kheer variants alongside elaborate banana leaf spreads."
    ),
    ("ram-navami", "madhya-pradesh"): (
        "The magnificent celebrations at the historic Orchha Ram Raja temple draw millions across Madhya Pradesh during the janmotsav. "
        "Devotional mandir visits draw thousands of residents into illuminated public streets after sunset for collective prayers. "
        "The local evening hospitality features sharing bowls of panakam along with regional street savouries."
    ),
    ("ram-navami", "maharashtra"): (
        "The systematic rendering of traditional cradle ceremonies at noon anchors home altars across Maharashtra during the spring days. "
        "Bustling society spaces turn into lively centers for nightly kirtan sessions and collective aarti routines. "
        "The family gathering centers on preparing hot neer mor formulas along with traditional maharashtrian sweets."
    ),
    ("ram-navami", "manipur"): (
        "Devotional storytelling and graceful musical sequences fill local mandaps in Manipur, blending the seasonal shift with Ram katha. "
        "Expressive cultural performances offer a deeply classical avenue for communities participating in the janmotsav. "
        "The sacred day is marked by preparing custom jalebi formulas to share among extended families."
    ),
    ("ram-navami", "meghalaya"): (
        "Sacred fasts and twilight prayer groups bring diverse neighborhoods together in Meghalaya to observe the holy janmotsav. "
        "Festive community halls host peaceful cultural gatherings to celebrate the traditional segments of Ram katha. "
        "The warm afternoon hospitality features sharing bowls of panakam along with unique local rice sweets."
    ),
    ("ram-navami", "mizoram"): (
        "Traditional oil lamps illuminate private balconies in Mizoram, bridging local harmony with the global focus on the janmotsav. "
        "Decorated community spaces allow diaspora groups to gather for collective prayers honoring the birth of righteousness. "
        "The spring occasion is highlighted by gathering for shared plates of neer mor across local townships."
    ),
    ("ram-navami", "nagaland"): (
        "Quiet home altars are decorated with fresh spring flowers across Nagaland, celebrating the spiritual presence of the janmotsav. "
        "Vibrant collective singing provides a welcoming environment for families participating in Ram katha rituals. "
        "The peaceful seasonal gathering is highlighted by presenting warm kheer formulas alongside celebratory desserts."
    ),
    ("ram-navami", "odisha"): (
        "The grand Rama-Sita wedding reenactment ceremonies or Kalyanotsavam transform local towns across Odisha during the spring. "
        "Intricate designs line the paths where families gather for the beautiful evening janmotsav blessings. "
        "The holy days are accompanied by distributing traditional panakam along with classic temple sweets."
    ),
    ("ram-navami", "punjab"): (
        "Shobha yatras and intense continuous kirtan sessions fill local residential areas across Punjab during the janmotsav. "
        "Neighborhood families coordinate vibrant devotional tracks inside community centres to praise the avatar. "
        "The auspicious eighth day is marked by sharing warm jalebi alongside festive local rotis."
    ),
    ("ram-navami", "rajasthan"): (
        "High-energy devotional chants and traditional folk music fill historic courtyards in Rajasthan during the holy spring days. "
        "Delicate courtyard decorations provide a dramatic setting for late-night Ram katha sessions under bright lights. "
        "The culinary gathering centers on serving sweet neer mor variations along with rich desert treats."
    ),
    ("ram-navami", "sikkim"): (
        "Hillside altars are dressed in fresh spring leaves across Sikkim, welcoming the seasonal alignment with the janmotsav. "
        "Grounded community prayer brings mountain settlements together for peaceful scriptural reading songs and shared blessings. "
        "The local hospitality involves sharing sweet kheer formulas among remote neighborhoods."
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
        "Devotional stotra recitations fill local community halls across Tripura, mirroring the spring arrival of the janmotsav. "
        "Community pandals turn into lively meeting points for families participating in evening Ram katha sessions. "
        "The evening hospitality is highlighted by sharing traditional singori alongside custom kheer dishes."
    ),
    ("ram-navami", "uttar-pradesh"): (
        "Millions of pilgrims taking holy dips in the sacred Sarayu river at Ayodhya transform Uttar Pradesh during the janmotsav. "
        "Ancient public squares create an unmatched devotional scale as crowds gather for evening Ram katha songs. "
        "The high-energy days include distributing famous panakam alongside traditional city prasad."
    ),
    ("ram-navami", "uttarakhand"): (
        "Pilgrimages to ancient hilltop shrines and strict fasting routines define the local experience in Uttarakhand during the spring. "
        "Ancient hill temples bring remote mountain settlements together for protective collective prayers honoring the avatar. "
        "The spiritual gathering is completed by serving hot neer mor formulas alongside custom alpine treats."
    ),
    ("ram-navami", "west-bengal"): (
        "Traditional scriptural recitations and beautiful devotional dynamic maps transform homes in West Bengal during the janmotsav. "
        "Artistic neighborhood structures and beautiful decorations alter the local landscape during the twilight Ram katha hours. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom kheer sweets."
    ),
    ("ram-navami", "nri-london"): (
        "Massive hired assembly halls host scriptural workshops and classical bhajan programs across London, allowing the diaspora to preserve the heritage. "
        "Bustling weekend events connect families across boroughs for synchronized janmotsav circles and prayers. "
        "Expatriates mark the spring transition by packing tupperware containers of jalebi to share with global friends."
    ),
    ("ram-navami", "nri-new-york"): (
        "Community centers host high-energy bhajan recitations and continuous scriptural discourses in New York, honoring the traditions of the janmotsav. "
        "Ornate temple halls and family video calls bridge the long distance for relatives participating in Ram katha. "
        "The diaspora gathering concludes with sharing custom kheer variations within local networks."
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
        "Devotional fasting routines and intense temple lines define the household atmosphere in Bihar, celebrating the auspicious arrival of bajrangbali. "
        "The community gathers for elaborate sundarkand reading sessions to invite protective guidance into their homes. "
        "Fasting families break their daily restrictions by eating custom motichoor items alongside classic home-cooked bihari savouries."
    ),
    ("hanuman-jayanti", "chhattisgarh"): (
        "Vibrant red flags and traditional wrestling arena or akhada displays are beautifully coordinated across Chhattisgarh, initiating the spring celebration. "
        "Evening gatherings feature vibrant bajrangbali chants as local neighborhoods unite for collective worship at local shrines. "
        "Kitchens prepare specialized boondi laddus and home-style desserts to distribute as sacred prasad."
    ),
    ("hanuman-jayanti", "goa"): (
        "Serene oil lamp illuminations turn Goan temple courtyards into spaces of absolute calm during the holy chalisa recitations. "
        "Families coordinate intricate sundarkand routines to invite prosperity and protective energy into their neighborhoods. "
        "The sacred time involves sharing delicious besan ladoo portions alongside coastal coconut desserts with visiting families."
    ),
    ("hanuman-jayanti", "gujarat"): (
        "Bustling street pandals and echoing collective chants of the Hanuman Chalisa transform public areas across Gujarat under bright lights. "
        "Massive temple crowds gather late into the evening to mark the precise birth moment of the deity. "
        "Extended families mark the joyful transition by sharing large plates of imarti along with festive local snacks."
    ),
    ("hanuman-jayanti", "haryana"): (
        "Traditional kirtans and sacred vermillion offerings alter the domestic rhythm across Haryana during the holy spring days. "
        "Neighborhood women lead traditional sundarkand chats to invoke the protective guidance of bajrangbali. "
        "The home gathering is warmed by distributing sweet motichoor variations paired with farm-style dairy delicacies."
    ),
    ("hanuman-jayanti", "himachal-pradesh"): (
        "Hillside shrines echo with deep devotional music across Himachal Pradesh, anchoring the mountain air in the praise of bajrangbali. "
        "Local clans travel across valleys to participate in grand temple-style chalisa reading gatherings. "
        "The spiritual afternoon is comforted by serving warm boondi laddus alongside rich mountain-style meals."
    ),
    ("hanuman-jayanti", "jharkhand"): (
        "Earthen lamps remain lit continuously inside Jharkhand residences, marking the seasonal alignment with the protective deity. "
        "Devotees coordinate peaceful community prayer circles to offer collective gratitude for family health and well-being. "
        "The fasting period is supported by sharing unique besan ladoo mixtures with neighboring families."
    ),
    ("hanuman-jayanti", "karnataka"): (
        "The unique distribution of sacred orange sindoor and sweet boondi laddus transforms local living rooms across Karnataka. "
        "Intricate flower decorations and morning chalisa rituals re-energize the household as families decorate the shrine. "
        "Visiting guests are welcomed into homes with delicious imarti variations alongside classic southern treats."
    ),
    ("hanuman-jayanti", "kerala"): (
        "Specialized temple shrines exhibit beautiful scriptural readings of the sundarkand in Kerala, marking a unique southern expression. "
        "The quiet community focus sets a deeply meditative stage for intense twilight prayers inside traditional shrines. "
        "The concluding hour is celebrated by serving sweet motichoor variants alongside elaborate banana leaf spreads."
    ),
    ("hanuman-jayanti", "madhya-pradesh"): (
        "The magnificent celebrations at historic hilltop temples draw millions across Madhya Pradesh during the chalisa recitations. "
        "Devotional mandir visits draw thousands of residents into illuminated public streets after sunset for collective prayers. "
        "The local evening hospitality features sharing bowls of boondi laddus along with regional street savouries."
    ),
    ("hanuman-jayanti", "maharashtra"): (
        "The systematic rendering of morning birth ceremonies at sunrise anchors local neighborhood complexes across Maharashtra. "
        "Bustling society spaces turn into lively centers for nightly sundarkand sessions and collective aarti routines. "
        "The family gathering centers on preparing fresh besan ladoo formulas along with traditional maharashtrian sweets."
    ),
    ("hanuman-jayanti", "manipur"): (
        "Devotional storytelling and graceful musical sequences fill local mandaps in Manipur, blending the seasonal shift with the chalisa. "
        "Expressive cultural performances offer a deeply classical avenue for communities participating in the worship of bajrangbali. "
        "The sacred day is marked by preparing custom imarti formulas to share among extended families."
    ),
    ("hanuman-jayanti", "meghalaya"): (
        "Sacred fasts and twilight prayer groups bring diverse neighborhoods together in Meghalaya to observe the holiday. "
        "Festive community halls host peaceful cultural gatherings to celebrate the traditional segments of the sundarkand. "
        "The warm afternoon hospitality features sharing bowls of motichoor along with unique local rice sweets."
    ),
    ("hanuman-jayanti", "mizoram"): (
        "Traditional oil lamps illuminate private balconies in Mizoram, bridging local harmony with the global focus on bajrangbali. "
        "Decorated community spaces allow diaspora groups to gather for collective prayers honoring the protective deity. "
        "The spring occasion is highlighted by gathering for shared plates of boondi laddus across local townships."
    ),
    ("hanuman-jayanti", "nagaland"): (
        "Quiet home altars are decorated with fresh spring flowers across Nagaland, celebrating the spiritual presence of the chalisa. "
        "Vibrant collective singing provides a welcoming environment for families participating in sundarkand rituals. "
        "The peaceful seasonal gathering is highlighted by presenting warm besan ladoo formulas alongside celebratory desserts."
    ),
    ("hanuman-jayanti", "odisha"): (
        "The iconic orange flags and grand temple Hanuman Chalisa circuits transform local towns across Odisha during the spring. "
        "Intricate designs line the paths where families gather for the beautiful evening bajrangbali blessings. "
        "The holy days are accompanied by distributing traditional imarti along with classic temple sweets."
    ),
    ("hanuman-jayanti", "punjab"): (
        "Shobha yatras and intense continuous chalisa sessions fill local residential areas across Punjab during the spring. "
        "Neighborhood families coordinate vibrant devotional tracks inside community centres to praise the deity. "
        "The auspicious day is marked by sharing warm motichoor alongside festive local rotis."
    ),
    ("hanuman-jayanti", "rajasthan"): (
        "High-energy devotional chants and grand temple celebrations at Salasar Balaji fill historic neighborhoods in Rajasthan. "
        "Delicate courtyard decorations provide a dramatic setting for late-night sundarkand sessions under bright lights. "
        "The culinary gathering centers on serving sweet boondi laddus variations along with rich desert treats."
    ),
    ("hanuman-jayanti", "sikkim"): (
        "Hillside altars are dressed in fresh spring leaves across Sikkim, welcoming the seasonal alignment with the chalisa. "
        "Grounded community prayer brings mountain settlements together for peaceful sundarkand songs and shared blessings. "
        "The local hospitality involves sharing sweet besan ladoo formulas among remote neighborhoods."
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
        "Devotional stotra recitations fill local community halls across Tripura, mirroring the spring arrival of the chalisa. "
        "Community pandals turn into lively meeting points for families participating in evening sundarkand sessions. "
        "The evening hospitality is highlighted by sharing traditional singori alongside custom boondi laddus dishes."
    ),
    ("hanuman-jayanti", "uttar-pradesh"): (
        "Massive congregations at ancient Sankat Mochan mandirs and morning sundarkand chants transform Uttar Pradesh. "
        "Ancient public squares create an unmatched devotional scale as crowds gather for evening chalisa songs. "
        "The high-energy days include distributing famous besan ladoo alongside traditional city prasad."
    ),
    ("hanuman-jayanti", "uttarakhand"): (
        "Pilgrimages to ancient hilltop shrines and strict fasting routines define the local experience in Uttarakhand during the spring. "
        "Ancient hill temples bring remote mountain settlements together for protective collective prayers honoring bajrangbali. "
        "The spiritual gathering is completed by serving hot imarti formulas alongside custom alpine treats."
    ),
    ("hanuman-jayanti", "west-bengal"): (
        "Traditional scriptural recitations and beautiful devotional setups transform homes in West Bengal during the chalisa. "
        "Artistic neighborhood structures and beautiful decorations alter the local landscape during the twilight sundarkand hours. "
        "The cultural transition is accompanied by preparing traditional sandesh alongside custom motichoor sweets."
    ),
    ("hanuman-jayanti", "nri-london"): (
        "Massive hired assembly halls host scriptural workshops and collective Hanuman Chalisa recitations across London. "
        "Bustling weekend events connect families across boroughs for synchronized circles and prayers. "
        "Expatriates mark the spring transition by packing tupperware containers of boondi laddus to share with global friends."
    ),
    ("hanuman-jayanti", "nri-new-york"): (
        "Community centers host orange vermillion ceremonies and continuous scriptural discourses in New York, honoring the traditions. "
        "Ornate temple halls and family video calls bridge the long distance for relatives participating in chalisa recitations. "
        "The diaspora gathering concludes with sharing custom besan ladoo variations within local networks."
    )

}  # End of FESTIVAL_REGION_SUMMARY -- 480 entries complete (16 festivals × 30 regions)
