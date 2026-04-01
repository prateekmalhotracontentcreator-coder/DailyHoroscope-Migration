import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { PanchangShareCard, ShareButtons } from '../components/ShareCard';
import PanchangCosmicMap from '../components/PanchangCosmicMap';
import { Calendar, Sun, Moon, Star, Sparkles, ChevronLeft, ChevronRight, Zap, MapPin, Globe, ChevronDown, Clock } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://everydayhoroscope.in';
const OG_IMAGE = `${SITE}/og-image.png`;
const LOC_STORAGE_KEY = 'panchang_location_slug';
const DEFAULT_SLUG = 'new-delhi-india';

// ─── Language translation tables ─────────────────────────────────────────────
const LANG_META_MAP = {
  tamil:    { code:'ta', nativeName:'தமிழ்',    badge:'தமிழ் பஞ்சாங்கம்',   titlePrefix:'இன்றைய தமிழ் பஞ்சாங்கம்',   desc:'இன்றைய தமிழ் பஞ்சாங்கம் — திதி, நட்சத்திரம், யோகம், கரணம், சூரிய உதயம், ராகு காலம்' },
  telugu:   { code:'te', nativeName:'తెలుగు',   badge:'తెలుగు పంచాంగం',     titlePrefix:'నేటి తెలుగు పంచాంగం',       desc:'నేటి తెలుగు పంచాంగం — తిథి, నక్షత్రం, యోగం, కరణం, సూర్యోదయం, రాహు కాలం' },
  malayalam:{ code:'ml', nativeName:'മലയാളം',  badge:'മലയാളം പഞ്ചാംഗം',    titlePrefix:'ഇന്നത്തെ മലയാളം പഞ്ചാംഗം',  desc:'ഇന്നത്തെ മലയാളം പഞ്ചാംഗം — തിഥി, നക്ഷത്രം, യോഗം, കരണം, സൂര്യോദയം, രാഹു കാലം' },
  kannada:  { code:'kn', nativeName:'ಕನ್ನಡ',    badge:'ಕನ್ನಡ ಪಂಚಾಂಗ',       titlePrefix:'ಇಂದಿನ ಕನ್ನಡ ಪಂಚಾಂಗ',        desc:'ಇಂದಿನ ಕನ್ನಡ ಪಂಚಾಂಗ — ತಿಥಿ, ನಕ್ಷತ್ರ, ಯೋಗ, ಕರಣ, ಸೂರ್ಯೋದಯ, ರಾಹು ಕಾಲ' },
  hindi:    { code:'hi', nativeName:'हिंदी',    badge:'हिंदी पंचांग',         titlePrefix:'आज का हिंदी पंचांग',         desc:'आज का हिंदी पंचांग — तिथि, नक्षत्र, योग, करण, सूर्योदय, राहु काल' },
};

const LANG_LABELS_MAP = {
  tamil:    { sunrise:'சூரிய உதயம்', sunset:'சூரிய அஸ்தமனம்', moonrise:'சந்திர உதயம்', moonset:'சந்திர அஸ்தமனம்', tithi:'திதி', nakshatra:'நட்சத்திரம்', yoga:'யோகம்', karana:'கரணம்', vara:'வாரம்', fiveLimbs:'பஞ்சாங்கம் — ஐந்து அங்கங்கள்', timingWindows:'நேர அட்டவணை', auspicious:'நல்ல நேரம்', inauspicious:'தீய நேரம்', observances:'இன்றைய விசேஷங்கள்', now:'இப்போது', sunIn:'சூரியன்', moonIn:'சந்திரன்', paksha:'பக்ஷம்', todayTithi:'இன்றைய திதி', moonPosition:'சந்திர நிலை', moonSign:'சந்திர ராசி', samvat:'சம்வத்', shubhMuhurat:'சுப முகூர்த்தம்', auspiciousWindows:'சுப நேரங்கள்', inauspiciousWindows:'தீய நேரங்கள் — தவிர்க்கவும்', dayChoghadiya:'பகல் சோகடியா', nightChoghadiya:'இரவு சோகடியா', tapDate:'தேதியை தட்டவும்', neutral:'நடுநிலை', tabToday:'இன்று', tabTomorrow:'நாளை', tabTithi:'திதி', tabMuhurat:'முகூர்த்தம்', tabChoghadiya:'சோகடியா', tabCalendar:'நாட்காட்டி', tabFestivals:'விழாக்கள்', },
  telugu:   { sunrise:'సూర్యోదయం', sunset:'సూర్యాస్తమయం', moonrise:'చంద్రోదయం', moonset:'చంద్రాస్తమయం', tithi:'తిథి', nakshatra:'నక్షత్రం', yoga:'యోగం', karana:'కరణం', vara:'వారం', fiveLimbs:'పంచాంగం — పంచ అంగాలు', timingWindows:'సమయ వివరాలు', auspicious:'శుభ సమయం', inauspicious:'అశుభ సమయం', observances:'నేటి విశేషాలు', now:'ఇప్పుడు', sunIn:'సూర్యుడు', moonIn:'చంద్రుడు', paksha:'పక్షం', todayTithi:'నేటి తిథి', moonPosition:'చంద్ర స్థితి', moonSign:'చంద్ర రాశి', samvat:'సంవత్', shubhMuhurat:'శుభ ముహూర్తం', auspiciousWindows:'శుభ సమయాలు', inauspiciousWindows:'అశుభ సమయాలు — నివారించండి', dayChoghadiya:'పగటి చోఘడియా', nightChoghadiya:'రాత్రి చోఘడియా', tapDate:'తేదీని నొక్కండి', neutral:'తటస్థం', tabToday:'ఇవాళ', tabTomorrow:'రేపు', tabTithi:'తిథి', tabMuhurat:'ముహూర్తం', tabChoghadiya:'చోఘడియా', tabCalendar:'క్యాలెండర్', tabFestivals:'పండుగలు', },
  malayalam:{ sunrise:'സൂര്യോദയം', sunset:'സൂര്യാസ്തമയം', moonrise:'ചന്ദ്രോദയം', moonset:'ചന്ദ്രാസ്തമയം', tithi:'തിഥി', nakshatra:'നക്ഷത്രം', yoga:'യോഗം', karana:'കരണം', vara:'വാരം', fiveLimbs:'പഞ്ചാംഗം — പഞ്ച അംഗങ്ങൾ', timingWindows:'സമയ വിവരങ്ങൾ', auspicious:'ശുഭ സമയം', inauspicious:'അശുഭ സമയം', observances:'ഇന്നത്തെ വിശേഷങ്ങൾ', now:'ഇപ്പോൾ', sunIn:'സൂര്യൻ', moonIn:'ചന്ദ്രൻ', paksha:'പക്ഷം', todayTithi:'ഇന്നത്തെ തിഥി', moonPosition:'ചന്ദ്ര സ്ഥാനം', moonSign:'ചന്ദ്ര രാശി', samvat:'സംവത്', shubhMuhurat:'ശുഭ മുഹൂർത്തം', auspiciousWindows:'ശുഭ സമയങ്ങൾ', inauspiciousWindows:'അശുഭ സമയങ്ങൾ — ഒഴിവാക്കുക', dayChoghadiya:'പകൽ ചോഘഡിയ', nightChoghadiya:'രാത്രി ചോഘഡിയ', tapDate:'തിയ്യതി തൊടുക', neutral:'നിഷ്‌പക്ഷം', tabToday:'ഇന്ന്', tabTomorrow:'നാളെ', tabTithi:'തിഥി', tabMuhurat:'മുഹൂർത്തം', tabChoghadiya:'ചോഘഡിയ', tabCalendar:'കലണ്ടർ', tabFestivals:'ഉത്സവങ്ങൾ', },
  kannada:  { sunrise:'ಸೂರ್ಯೋದಯ', sunset:'ಸೂರ್ಯಾಸ್ತ', moonrise:'ಚಂದ್ರೋದಯ', moonset:'ಚಂದ್ರಾಸ್ತ', tithi:'ತಿಥಿ', nakshatra:'ನಕ್ಷತ್ರ', yoga:'ಯೋಗ', karana:'ಕರಣ', vara:'ವಾರ', fiveLimbs:'ಪಂಚಾಂಗ — ಪಂಚ ಅಂಗಗಳು', timingWindows:'ಸಮಯ ವಿವರಗಳು', auspicious:'ಶುಭ ಸಮಯ', inauspicious:'ಅಶುಭ ಸಮಯ', observances:'ಇಂದಿನ ವಿಶೇಷಗಳು', now:'ಈಗ', sunIn:'ಸೂರ್ಯ', moonIn:'ಚಂದ್ರ', paksha:'ಪಕ್ಷ', todayTithi:'ಇಂದಿನ ತಿಥಿ', moonPosition:'ಚಂದ್ರ ಸ್ಥಾನ', moonSign:'ಚಂದ್ರ ರಾಶಿ', samvat:'ಸಂವತ್', shubhMuhurat:'ಶುಭ ಮುಹೂರ್ತ', auspiciousWindows:'ಶುಭ ಸಮಯಗಳು', inauspiciousWindows:'ಅಶುಭ ಸಮಯಗಳು — ತಪ್ಪಿಸಿ', dayChoghadiya:'ಹಗಲು ಚೋಘಡಿಯ', nightChoghadiya:'ರಾತ್ರಿ ಚೋಘಡಿಯ', tapDate:'ದಿನಾಂಕ ಆಯ್ಕೆ', neutral:'ತಟಸ್ಥ', tabToday:'ಇಂದು', tabTomorrow:'ನಾಳೆ', tabTithi:'ತಿಥಿ', tabMuhurat:'ಮುಹೂರ್ತ', tabChoghadiya:'ಚೋಘಡಿಯ', tabCalendar:'ದಿನದರ್ಶಿ', tabFestivals:'ಹಬ್ಬಗಳು', },
  hindi:    { sunrise:'सूर्योदय', sunset:'सूर्यास्त', moonrise:'चंद्रोदय', moonset:'चंद्रास्त', tithi:'तिथि', nakshatra:'नक्षत्र', yoga:'योग', karana:'करण', vara:'वार', fiveLimbs:'पंचांग — पंच अंग', timingWindows:'मुहूर्त विवरण', auspicious:'शुभ मुहूर्त', inauspicious:'अशुभ काल', observances:'आज के विशेष', now:'अभी', sunIn:'सूर्य', moonIn:'चंद्र', paksha:'पक्ष', todayTithi:'आज की तिथि', moonPosition:'चंद्र स्थिति', moonSign:'चंद्र राशि', samvat:'संवत', shubhMuhurat:'शुभ मुहूर्त', auspiciousWindows:'शुभ समय', inauspiciousWindows:'अशुभ काल — टालें', dayChoghadiya:'दिन चौघड़िया', nightChoghadiya:'रात चौघड़िया', tapDate:'तिथि देखें', neutral:'तटस्थ', tabToday:'आज', tabTomorrow:'कल', tabTithi:'तिथि', tabMuhurat:'मुहूर्त', tabChoghadiya:'चौघड़िया', tabCalendar:'कैलेंडर', tabFestivals:'त्यौहार', },
};

const LANG_NAKSHATRA = {
  tamil:    {Ashwini:'அஸ்வினி',Bharani:'பரணி',Krittika:'கார்த்திகை',Rohini:'ரோகிணி',Mrigashira:'மிருகசீரிஷம்',Ardra:'திருவாதிரை',Punarvasu:'புனர்பூசம்',Pushya:'பூசம்',Ashlesha:'ஆயில்யம்',Magha:'மகம்',PurvaPhalguni:'பூரம்',UttaraPhalguni:'உத்திரம்',Hasta:'அஸ்தம்',Chitra:'சித்திரை',Swati:'சுவாதி',Vishakha:'விசாகம்',Anuradha:'அனுஷம்',Jyeshtha:'கேட்டை',Mula:'மூலம்',PurvaAshadha:'பூராடம்',UttaraAshadha:'உத்திராடம்',Shravana:'திருவோணம்',Dhanishtha:'அவிட்டம்',Shatabhisha:'சதயம்',PurvaBhadrapada:'பூரட்டாதி',UttaraBhadrapada:'உத்திரட்டாதி',Revati:'ரேவதி'},
  telugu:   {Ashwini:'అశ్విని',Bharani:'భరణి',Krittika:'కృత్తిక',Rohini:'రోహిణి',Mrigashira:'మృగశిర',Ardra:'ఆర్ద్ర',Punarvasu:'పునర్వసు',Pushya:'పుష్యమి',Ashlesha:'ఆశ్లేష',Magha:'మఘ',PurvaPhalguni:'పూర్వఫల్గుణి',UttaraPhalguni:'ఉత్తరఫల్గుణి',Hasta:'హస్త',Chitra:'చిత్ర',Swati:'స్వాతి',Vishakha:'విశాఖ',Anuradha:'అనూరాధ',Jyeshtha:'జ్యేష్ఠ',Mula:'మూల',PurvaAshadha:'పూర్వాషాఢ',UttaraAshadha:'ఉత్తరాషాఢ',Shravana:'శ్రవణ',Dhanishtha:'ధనిష్ఠ',Shatabhisha:'శతభిష',PurvaBhadrapada:'పూర్వభాద్ర',UttaraBhadrapada:'ఉత్తరభాద్ర',Revati:'రేవతి'},
  malayalam:{Ashwini:'അശ്വതി',Bharani:'ഭരണി',Krittika:'കാർത്തിക',Rohini:'രോഹിണി',Mrigashira:'മകയിരം',Ardra:'തിരുവാതിര',Punarvasu:'പുണർതം',Pushya:'പൂയം',Ashlesha:'ആയില്യം',Magha:'മകം',PurvaPhalguni:'പൂരം',UttaraPhalguni:'ഉത്രം',Hasta:'അത്തം',Chitra:'ചിത്തിര',Swati:'ചോതി',Vishakha:'വിശാഖം',Anuradha:'അനിഴം',Jyeshtha:'തൃക്കേട്ട',Mula:'മൂലം',PurvaAshadha:'പൂരാടം',UttaraAshadha:'ഉത്രാടം',Shravana:'തിരുവോണം',Dhanishtha:'അവിട്ടം',Shatabhisha:'ചതയം',PurvaBhadrapada:'പൂരുരുട്ടാതി',UttaraBhadrapada:'ഉത്രട്ടാതി',Revati:'രേവതി'},
  kannada:  {Ashwini:'ಅಶ್ವಿನಿ',Bharani:'ಭರಣಿ',Krittika:'ಕೃತ್ತಿಕ',Rohini:'ರೋಹಿಣಿ',Mrigashira:'ಮೃಗಶಿರ',Ardra:'ಆರ್ದ್ರ',Punarvasu:'ಪುನರ್ವಸು',Pushya:'ಪುಷ್ಯ',Ashlesha:'ಆಶ್ಲೇಷ',Magha:'ಮಘ',PurvaPhalguni:'ಪೂರ್ವ ಫಲ್ಗುಣಿ',UttaraPhalguni:'ಉತ್ತರ ಫಲ್ಗುಣಿ',Hasta:'ಹಸ್ತ',Chitra:'ಚಿತ್ರ',Swati:'ಸ್ವಾತಿ',Vishakha:'ವಿಶಾಖ',Anuradha:'ಅನೂರಾಧ',Jyeshtha:'ಜ್ಯೇಷ್ಠ',Mula:'ಮೂಲ',PurvaAshadha:'ಪೂರ್ವಾಷಾಢ',UttaraAshadha:'ಉತ್ತರಾಷಾಢ',Shravana:'ಶ್ರವಣ',Dhanishtha:'ಧನಿಷ್ಠ',Shatabhisha:'ಶತಭಿಷ',PurvaBhadrapada:'ಪೂರ್ವಭಾದ್ರ',UttaraBhadrapada:'ಉತ್ತರಭಾದ್ರ',Revati:'ರೇವತಿ'},
  hindi:    {Ashwini:'अश्विनी',Bharani:'भरणी',Krittika:'कृत्तिका',Rohini:'रोहिणी',Mrigashira:'मृगशिरा',Ardra:'आर्द्रा',Punarvasu:'पुनर्वसु',Pushya:'पुष्य',Ashlesha:'आश्लेषा',Magha:'मघा',PurvaPhalguni:'पूर्वफाल्गुनी',UttaraPhalguni:'उत्तरफाल्गुनी',Hasta:'हस्त',Chitra:'चित्रा',Swati:'स्वाती',Vishakha:'विशाखा',Anuradha:'अनुराधा',Jyeshtha:'ज्येष्ठा',Mula:'मूल',PurvaAshadha:'पूर्वाषाढ़',UttaraAshadha:'उत्तराषाढ़',Shravana:'श्रवण',Dhanishtha:'धनिष्ठा',Shatabhisha:'शतभिषा',PurvaBhadrapada:'पूर्वभाद्रपद',UttaraBhadrapada:'उत्तरभाद्रपद',Revati:'रेवती'},
};

const LANG_TITHI = {
  tamil:    {Pratipada:'பிரதமை',Dwitiya:'த்விதியை',Tritiya:'திருதியை',Chaturthi:'சதுர்த்தி',Panchami:'பஞ்சமி',Shashthi:'ஷஷ்டி',Saptami:'சப்தமி',Ashtami:'அஷ்டமி',Navami:'நவமி',Dashami:'தசமி',Ekadashi:'ஏகாதசி',Dwadashi:'த்வாதசி',Trayodashi:'திரயோதசி',Chaturdashi:'சதுர்தசி',Purnima:'பூர்ணிமை',Amavasya:'அமாவாசை'},
  telugu:   {Pratipada:'పాడ్యమి',Dwitiya:'విదియ',Tritiya:'తదియ',Chaturthi:'చవితి',Panchami:'పంచమి',Shashthi:'షష్టి',Saptami:'సప్తమి',Ashtami:'అష్టమి',Navami:'నవమి',Dashami:'దశమి',Ekadashi:'ఏకాదశి',Dwadashi:'ద్వాదశి',Trayodashi:'త్రయోదశి',Chaturdashi:'చతుర్దశి',Purnima:'పౌర్ణమి',Amavasya:'అమావాస్య'},
  malayalam:{Pratipada:'പ്രതിപദ',Dwitiya:'ദ്വിതീയ',Tritiya:'തൃതീയ',Chaturthi:'ചതുർഥി',Panchami:'പഞ്ചമി',Shashthi:'ഷഷ്ഠി',Saptami:'സപ്തമി',Ashtami:'അഷ്ടമി',Navami:'നവമി',Dashami:'ദശമി',Ekadashi:'ഏകാദശി',Dwadashi:'ദ്വാദശി',Trayodashi:'ത്രയോദശി',Chaturdashi:'ചതുർദശി',Purnima:'പൗർണ്ണമി',Amavasya:'അമാവാസ്യ'},
  kannada:  {Pratipada:'ಪಾಡ್ಯ',Dwitiya:'ಬಿದಿಗೆ',Tritiya:'ತದಿಗೆ',Chaturthi:'ಚೌತಿ',Panchami:'ಪಂಚಮಿ',Shashthi:'ಷಷ್ಠಿ',Saptami:'ಸಪ್ತಮಿ',Ashtami:'ಅಷ್ಟಮಿ',Navami:'ನವಮಿ',Dashami:'ದಶಮಿ',Ekadashi:'ಏಕಾದಶಿ',Dwadashi:'ದ್ವಾದಶಿ',Trayodashi:'ತ್ರಯೋದಶಿ',Chaturdashi:'ಚತುರ್ದಶಿ',Purnima:'ಹುಣ್ಣಿಮೆ',Amavasya:'ಅಮಾವಾಸ್ಯೆ'},
  hindi:    {Pratipada:'प्रतिपदा',Dwitiya:'द्वितीया',Tritiya:'तृतीया',Chaturthi:'चतुर्थी',Panchami:'पंचमी',Shashthi:'षष्ठी',Saptami:'सप्तमी',Ashtami:'अष्टमी',Navami:'नवमी',Dashami:'दशमी',Ekadashi:'एकादशी',Dwadashi:'द्वादशी',Trayodashi:'त्रयोदशी',Chaturdashi:'चतुर्दशी',Purnima:'पूर्णिमा',Amavasya:'अमावस्या'},
};

const LANG_WEEKDAY = {
  tamil:    ['ஞாயிறு','திங்கள்','செவ்வாய்','புதன்','வியாழன்','வெள்ளி','சனி'],
  telugu:   ['ఆదివారం','సోమవారం','మంగళవారం','బుధవారం','గురువారం','శుక్రవారం','శనివారం'],
  malayalam:['ഞായർ','തിങ്കൾ','ചൊവ്വ','ബുധൻ','വ്യാഴം','വെള്ളി','ശനി'],
  kannada:  ['ಭಾನುವಾರ','ಸೋಮವಾರ','ಮಂಗಳವಾರ','ಬುಧವಾರ','ಗುರುವಾರ','ಶುಕ್ರವಾರ','ಶನಿವಾರ'],
  hindi:    ['रविवार','सोमवार','मंगलवार','बुधवार','गुरुवार','शुक्रवार','शनिवार'],
};

const LANG_PAKSHA = {
  tamil:    {Shukla:'சுக்ல பக்ஷம்',Krishna:'கிருஷ்ண பக்ஷம்'},
  telugu:   {Shukla:'శుక్ల పక్షం',Krishna:'కృష్ణ పక్షం'},
  malayalam:{Shukla:'വെളുത്ത പക്ഷം',Krishna:'കറുത്ത പക്ഷം'},
  kannada:  {Shukla:'ಶುಕ್ಲ ಪಕ್ಷ',Krishna:'ಕೃಷ್ಣ ಪಕ್ಷ'},
  hindi:    {Shukla:'शुक्ल पक्ष',Krishna:'कृष्ण पक्ष'},
};

const LANG_WINDOW = {
  tamil:    {'Brahma Muhurta':'பிரம்ம முகூர்த்தம்','Abhijit Muhurta':'அபிஜித் முகூர்த்தம்','Vijaya Muhurta':'விஜய முகூர்த்தம்','Rahu Kaal':'ராகு காலம்','Yamaganda':'யமகண்டம்','Gulika Kaal':'குளிக காலம்','Dur Muhurta':'துர் முகூர்த்தம்'},
  telugu:   {'Brahma Muhurta':'బ్రహ్మ ముహూర్తం','Abhijit Muhurta':'అభిజిత్ ముహూర్తం','Vijaya Muhurta':'విజయ ముహూర్తం','Rahu Kaal':'రాహు కాలం','Yamaganda':'యమగండం','Gulika Kaal':'గులిక కాలం','Dur Muhurta':'దుర్ ముహూర్తం'},
  malayalam:{'Brahma Muhurta':'ബ്രഹ്മ മുഹൂർത്തം','Abhijit Muhurta':'അഭിജിത് മുഹൂർത്തം','Vijaya Muhurta':'വിജയ മുഹൂർത്തം','Rahu Kaal':'രാഹു കാലം','Yamaganda':'യമഗണ്ഡം','Gulika Kaal':'ഗുളിക കാലം','Dur Muhurta':'ദുർ മുഹൂർത്തം'},
  kannada:  {'Brahma Muhurta':'ಬ್ರಹ್ಮ ಮುಹೂರ್ತ','Abhijit Muhurta':'ಅಭಿಜಿತ್ ಮುಹೂರ್ತ','Vijaya Muhurta':'ವಿಜಯ ಮುಹೂರ್ತ','Rahu Kaal':'ರಾಹು ಕಾಲ','Yamaganda':'ಯಮಗಂಡ','Gulika Kaal':'ಗುಳಿಕ ಕಾಲ','Dur Muhurta':'ದುರ್ ಮುಹೂರ್ತ'},
  hindi:    {'Brahma Muhurta':'ब्रह्म मुहूर्त','Abhijit Muhurta':'अभिजित् मुहूर्त','Vijaya Muhurta':'विजय मुहूर्त','Rahu Kaal':'राहु काल','Yamaganda':'यमगण्ड','Gulika Kaal':'गुलिक काल','Dur Muhurta':'दुर्मुहूर्त'},
};

// Weekday abbreviations for calendar column headers
const LANG_WEEKDAY_ABBR = {
  tamil:    ['ஞா','தி','செ','பு','வி','வெ','ச'],
  telugu:   ['ఆది','సోమ','మంగ','బుధ','గురు','శుక్ర','శని'],
  malayalam:['ഞാ','തി','ചൊ','ബു','വ്യാ','വെ','ശ'],
  kannada:  ['ಭಾ','ಸೋ','ಮಂ','ಬು','ಗು','ಶು','ಶ'],
  hindi:    ['रवि','सोम','मंगल','बुध','गुरु','शुक्र','शनि'],
};

// Choghadiya quality labels
const LANG_CHOG_QUALITY = {
  tamil:    { good:'நல்லது', neutral:'நடுநிலை', caution:'தவிர்க்கவும்' },
  telugu:   { good:'శుభం',   neutral:'తటస్థం',  caution:'అశుభం' },
  malayalam:{ good:'ശുഭം',   neutral:'നിഷ്‌പക്ഷം', caution:'അശുഭം' },
  kannada:  { good:'ಶುಭ',    neutral:'ತಟಸ್ಥ',   caution:'ಅಶುಭ' },
  hindi:    { good:'शुभ',    neutral:'तटस्थ',  caution:'अशुभ' },
};

// Translation helpers
function tLabel(key, lang) { return lang ? (LANG_LABELS_MAP[lang]?.[key] || key) : null; }
function tNak(name, lang)  { if (!lang || !name) return name; return LANG_NAKSHATRA[lang]?.[name.trim()] || name; }
function tTithi(name, lang){ if (!lang || !name) return name; return LANG_TITHI[lang]?.[name.trim()] || name; }
function tWin(label, lang) {
  if (!lang) return label;
  const map = LANG_WINDOW[lang] || {};
  if (label.startsWith('Dur Muhurta') || label.startsWith('Dur Muhurat')) return map['Dur Muhurta'] || label;
  return map[label] || label;
}
function tDay(lang)  { return lang ? (LANG_WEEKDAY[lang]?.[new Date().getDay()] || '') : null; }
function tPaksha(name, lang) { if (!lang || !name) return name; return LANG_PAKSHA[lang]?.[name] || name; }
function tChogQuality(quality, lang) { if (!lang) return null; return LANG_CHOG_QUALITY[lang]?.[quality] || null; }

const QUALITY_STYLES = {
  good:    { badge: 'bg-green-100 text-green-800' },
  neutral: { badge: 'bg-amber-100 text-amber-800' },
  caution: { badge: 'bg-red-100 text-red-800' },
};

const TYPE_META = {
  daily:      { title: "Today's Panchang",      icon: Sun,      desc: 'Complete Vedic almanac — Tithi, Nakshatra, Yoga, Karana, Sunrise & Sunset' },
  tomorrow:   { title: "Tomorrow's Panchang",   icon: Sun,      desc: 'Complete Vedic almanac for tomorrow — Tithi, Nakshatra, Yoga, Karana' },
  tithi:      { title: 'Tithi — Lunar Day',      icon: Moon,     desc: "Today's Tithi (lunar day) with Paksha phase and timing" },
  choghadiya: { title: 'Choghadiya',             icon: Zap,      desc: 'Auspicious and inauspicious time periods of the day' },
  calendar:   { title: 'Panchang Calendar',      icon: Calendar, desc: 'Monthly Hindu calendar with Tithi and observances' },
  festivals:  { title: 'Festivals & Vrats',      icon: Sparkles, desc: 'Upcoming Hindu festivals and vrat dates' },
  muhurat:    { title: 'Shubh Muhurat Today',    icon: Star,     desc: 'Auspicious timings today — all 15 Vedic muhurtas with quality and exact times' },
};

const ALIAS = {
  today:      'daily',
  tomorrow:   'tomorrow',
  tithi:      'tithi',
  choghadiya: 'choghadiya',
  muhurat:    'muhurat',
  nakshatra:  'daily',
  rahukaal:   'daily',
};

// ─── Timezone abbreviation helper ──────────────────────────────────────────
const TZ_OVERRIDE = {
  'Asia/Kolkata':         'IST',
  'Asia/Kathmandu':       'NPT',
  'Asia/Dubai':           'GST',
  'Asia/Singapore':       'SGT',
  'Asia/Kuala_Lumpur':    'MYT',
  'Asia/Jakarta':         'WIB',
  'Asia/Makassar':        'WITA',
  'Asia/Bangkok':         'ICT',
  'Asia/Shanghai':        'CST',
  'Pacific/Auckland':     'NZST',
  'Australia/Brisbane':   'AEST',
  'Australia/Sydney':     'AEDT',
  'Australia/Melbourne':  'AEDT',
  'America/Toronto':      'EST',
  'America/Vancouver':    'PST',
};

function getTZAbbr(ianaTimezone) {
  if (!ianaTimezone) return 'IST';
  if (TZ_OVERRIDE[ianaTimezone]) return TZ_OVERRIDE[ianaTimezone];
  try {
    const parts = new Intl.DateTimeFormat('en-US', {
      timeZone: ianaTimezone,
      timeZoneName: 'short',
    }).formatToParts(new Date());
    const tzPart = parts.find(p => p.type === 'timeZoneName');
    if (tzPart?.value) return tzPart.value;
  } catch { /* fall through */ }
  return ianaTimezone.split('/').pop().replace('_', ' ');
}

// ─── Time formatting — with seconds ────────────────────────────────────────
function makeFormatTime(tz) {
  return function formatTime(iso) {
    if (!iso) return '--';
    try {
      return new Date(iso).toLocaleTimeString('en-IN', {
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true,
        timeZone: tz || 'Asia/Kolkata',
      });
    } catch { return iso.slice(11, 19); }
  };
}

function formatDate(iso, tz) {
  if (!iso) return '';
  try {
    return new Date(iso).toLocaleDateString('en-IN', {
      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
      timeZone: tz || 'Asia/Kolkata',
    });
  } catch { return iso; }
}

function getTodayInTZ(tz) {
  try {
    const now = new Date();
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(now);
    const map = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${map.year}-${map.month}-${map.day}`;
  } catch {
    const ist = new Date(new Date().getTime() + 5.5 * 60 * 60 * 1000);
    return ist.toISOString().slice(0, 10);
  }
}

function getTomorrowInTZ(tz) {
  try {
    const tomorrow = new Date(new Date().getTime() + 86400000);
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(tomorrow);
    const map = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${map.year}-${map.month}-${map.day}`;
  } catch {
    const ist = new Date(new Date().getTime() + 5.5 * 60 * 60 * 1000);
    ist.setDate(ist.getDate() + 1);
    return ist.toISOString().slice(0, 10);
  }
}

const MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December'];

function humanDate(isoDate, tz) {
  if (!isoDate) return '';
  const [y, m, d] = isoDate.split('-');
  try {
    const weekday = new Date(`${isoDate}T12:00:00Z`).toLocaleDateString('en-IN', { weekday: 'long', timeZone: tz || 'Asia/Kolkata' });
    return `${weekday}, ${parseInt(d)} ${MONTH_NAMES[parseInt(m) - 1]} ${y}`;
  } catch {
    return `${parseInt(d)} ${MONTH_NAMES[parseInt(m) - 1]} ${y}`;
  }
}

// ─── Sun & Moon 2×2 grid ────────────────────────────────────────────────────
function SunMoonCards({ summary, panchang, tzAbbr, lang }) {
  const nak = tNak(panchang.nakshatra?.name, lang) || panchang.nakshatra?.name;
  const paksha = tPaksha(panchang.paksha, lang) || panchang.paksha;
  const cards = [
    { icon: <Sun className="h-5 w-5 text-amber-500 mx-auto mb-1" />,   labelR: tLabel('sunrise', lang),  labelEn: 'Sunrise',  value: summary.sunrise  || '--', sub: `${tLabel('sunIn',lang)||'Sun'} ${panchang.sun_sign}` },
    { icon: <Moon className="h-5 w-5 text-slate-400 mx-auto mb-1" />,  labelR: tLabel('sunset', lang),   labelEn: 'Sunset',   value: summary.sunset   || '--', sub: `${tLabel('moonIn',lang)||'Moon'} ${panchang.moon_sign}` },
    { icon: <Moon className="h-5 w-5 text-blue-300 mx-auto mb-1" />,   labelR: tLabel('moonrise', lang), labelEn: 'Moonrise', value: summary.moonrise || '--', sub: nak ? `${nak} ${tLabel('nakshatra',lang)||'Nakshatra'}` : '' },
    { icon: <Moon className="h-5 w-5 text-indigo-400 mx-auto mb-1" />, labelR: tLabel('moonset', lang),  labelEn: 'Moonset',  value: summary.moonset  || '--', sub: paksha ? paksha : '' },
  ];
  return (
    <div className="grid grid-cols-2 gap-3">
      {cards.map(c => (
        <Card key={c.labelEn} className="p-4 border border-gold/20 text-center">
          {c.icon}
          {lang && c.labelR ? (
            <div className="mt-0.5 mb-0.5">
              <p className="text-xs font-semibold text-foreground leading-tight">{c.labelR}</p>
              <p className="text-[10px] text-muted-foreground uppercase tracking-wide">{c.labelEn}</p>
            </div>
          ) : (
            <p className="text-xs text-muted-foreground uppercase tracking-wide">{c.labelEn}</p>
          )}
          <p className="font-semibold text-base tabular-nums">{c.value}</p>
          {c.sub && <p className="text-xs text-muted-foreground mt-0.5 truncate">{c.sub}</p>}
          <p className="text-[10px] text-gold/70 font-bold mt-0.5">{tzAbbr}</p>
        </Card>
      ))}
    </div>
  );
}

// ─── Timing Windows grouped card ────────────────────────────────────────────
// Splits windows by quality into Auspicious / Inauspicious sub-headers.
const AUSPICIOUS_LABELS = new Set(['Brahma Muhurta', 'Abhijit Muhurta', 'Vijaya Muhurta']);

function TimingWindowsCard({ windows, fmtTime, tzAbbr, lang }) {
  if (!windows?.length) return null;
  const now = new Date();
  const auspicious   = windows.filter(w => w.quality === 'good');
  const inauspicious = windows.filter(w => w.quality !== 'good');

  const renderRow = (w, i) => {
    const isCurrent = now >= new Date(w.start) && now <= new Date(w.end);
    const regional = tWin(w.label, lang);
    const showBilingual = lang && regional !== w.label;
    return (
      <div key={w.label} className={`flex items-center justify-between px-5 py-3 ${isCurrent ? 'bg-gold/5' : ''}`}>
        <div className="flex items-center gap-3">
          {isCurrent && <span className="w-2 h-2 rounded-full bg-green-500 flex-shrink-0" />}
          <div>
            {showBilingual ? (
              <>
                <p className="text-sm font-medium leading-tight">{regional}</p>
                <p className="text-[10px] text-muted-foreground">{w.label}</p>
              </>
            ) : (
              <span className="text-sm font-medium">{w.label}</span>
            )}
          </div>
          {isCurrent && <span className="text-xs text-green-600 font-semibold">{tLabel('now',lang)||'Now'}</span>}
        </div>
        <span className="text-xs text-muted-foreground tabular-nums">{fmtTime(w.start)} — {fmtTime(w.end)}</span>
      </div>
    );
  };

  return (
    <Card className="border border-gold/20 overflow-hidden">
      <div className="px-5 py-3 bg-gold/5 border-b border-gold/20 flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-widest text-gold">{tLabel('timingWindows',lang)||'Timing Windows'}</p>
        <span className="text-[10px] text-muted-foreground font-semibold">{tzAbbr}</span>
      </div>

      {/* ── Auspicious ───────────────────────────────────────────────────── */}
      {auspicious.length > 0 && (
        <>
          <div className="flex items-center gap-2 px-5 py-2 bg-green-50 border-b border-green-100">
            <span className="text-green-600 text-sm">✦</span>
            <p className="text-[11px] font-bold uppercase tracking-widest text-green-700">{tLabel('auspicious',lang)||'Auspicious'}</p>
          </div>
          <div className="divide-y divide-border">
            {auspicious.map(renderRow)}
          </div>
        </>
      )}

      {/* ── Inauspicious ─────────────────────────────────────────────────── */}
      {inauspicious.length > 0 && (
        <>
          <div className="flex items-center gap-2 px-5 py-2 bg-red-50 border-y border-red-100">
            <span className="text-red-500 text-sm">⚠</span>
            <p className="text-[11px] font-bold uppercase tracking-widest text-red-700">{tLabel('inauspicious',lang)||'Inauspicious'}</p>
          </div>
          <div className="divide-y divide-border">
            {inauspicious.map(renderRow)}
          </div>
        </>
      )}
    </Card>
  );
}

// ─── Location picker ────────────────────────────────────────────────────────
function LocationPicker({ selectedSlug, onSelect }) {
  const [locations, setLocations] = useState([]);
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef(null);

  useEffect(() => {
    axios.get(`${API}/locations`).then(r => setLocations(r.data)).catch(() => {});
  }, []);

  useEffect(() => {
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const selected = locations.find(l => l.slug === selectedSlug);
  const selectedTZAbbr = selected ? getTZAbbr(selected.timezone) : 'IST';
  const countries = [...new Set(locations.map(l => l.country))];

  const filtered = search.trim()
    ? locations.filter(l =>
        l.label.toLowerCase().includes(search.toLowerCase()) ||
        l.country.toLowerCase().includes(search.toLowerCase()) ||
        getTZAbbr(l.timezone).toLowerCase().includes(search.toLowerCase())
      )
    : locations;

  const grouped = countries.reduce((acc, c) => {
    const locs = filtered.filter(l => l.country === c);
    if (locs.length) acc[c] = locs;
    return acc;
  }, {});

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-gold/30 bg-gold/5 text-xs font-semibold text-gold hover:bg-gold/10 transition-colors"
      >
        <MapPin className="h-3 w-3 flex-shrink-0" />
        <span>{selected ? `${selected.label}, ${selected.country}` : 'Select location'}</span>
        <span className="px-1.5 py-0.5 rounded bg-gold/20 text-[10px] font-bold tracking-wide">{selectedTZAbbr}</span>
        <ChevronDown className={`h-3 w-3 flex-shrink-0 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-80 max-h-80 overflow-hidden rounded-xl border border-border bg-background shadow-xl z-50 flex flex-col">
          <div className="p-2 border-b border-border">
            <input
              autoFocus
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search city, country or timezone…"
              className="w-full px-3 py-1.5 text-xs rounded-lg border border-border bg-muted/30 focus:outline-none focus:border-gold/50"
            />
          </div>
          <div className="overflow-y-auto flex-1">
            {Object.entries(grouped).map(([country, locs]) => (
              <div key={country}>
                <div className="flex items-center gap-1.5 px-3 py-1.5 bg-muted/30 sticky top-0">
                  <Globe className="h-3 w-3 text-muted-foreground" />
                  <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">{country}</p>
                </div>
                {locs.map(loc => {
                  const tzAbbr = getTZAbbr(loc.timezone);
                  const isSelected = loc.slug === selectedSlug;
                  return (
                    <button
                      key={loc.slug}
                      onClick={() => { onSelect(loc.slug); setOpen(false); setSearch(''); }}
                      className={`w-full text-left px-4 py-2.5 text-xs hover:bg-gold/10 transition-colors flex items-center justify-between gap-3 ${
                        isSelected ? 'text-gold font-semibold bg-gold/5' : 'text-foreground'
                      }`}
                    >
                      <span className="flex-1">{loc.label}</span>
                      <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wide flex-shrink-0 ${
                        isSelected ? 'bg-gold/30 text-gold' : 'bg-muted text-muted-foreground'
                      }`}>{tzAbbr}</span>
                      {isSelected && <span className="text-gold flex-shrink-0">✓</span>}
                    </button>
                  );
                })}
              </div>
            ))}
            {Object.keys(grouped).length === 0 && (
              <p className="text-xs text-muted-foreground text-center py-6">No locations found</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── SEO helpers ────────────────────────────────────────────────────────────
function webPageSchema({ name, description, url, datePublished }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name, description, url,
    inLanguage: 'en-IN',
    ...(datePublished ? { datePublished } : {}),
    isPartOf: { '@type': 'WebSite', name: 'Everyday Horoscope', url: SITE },
    provider: { '@type': 'Organization', name: 'Everyday Horoscope', url: SITE },
  };
}

function buildPanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData, locationTZ }) {
  const tz = locationTZ || 'Asia/Kolkata';
  const todayISO    = getTodayInTZ(tz);
  const tomorrowISO = getTomorrowInTZ(tz);
  switch (view) {
    case 'daily': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Today's Panchang — ${humanToday}`;
      const description = `Free daily Panchang for ${humanToday}. Tithi, Nakshatra, Yoga, Karana, Brahma Muhurta, Rahu Kaal, Abhijit Muhurta, Vijaya Muhurta, Sunrise & Moonrise with seconds.`;
      const url = `${SITE}/panchang/today`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'tomorrow': {
      const humanTomorrow = humanDate(tomorrowISO, tz);
      const title = `Tomorrow's Panchang — ${humanTomorrow}`;
      const description = `Panchang for ${humanTomorrow}. Tithi, Nakshatra, Yoga, Karana, all timing windows with exact seconds.`;
      const url = `${SITE}/panchang/tomorrow`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: tomorrowISO }) };
    }
    case 'tithi': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Today's Tithi (Lunar Day) — ${humanToday}`;
      const description = `Today's Tithi, Paksha phase, Nakshatra, Moonrise & Moonset for ${humanToday}.`;
      const url = `${SITE}/panchang/tithi`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'choghadiya': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Choghadiya Today — ${humanToday}`;
      const description = `Auspicious and inauspicious time windows for ${humanToday} — Brahma Muhurta, Abhijit, Vijaya Muhurta, Rahu Kaal, Dur Muhurta with exact times.`;
      const url = `${SITE}/panchang/choghadiya`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'festivals': {
      const year = new Date().getFullYear();
      const title = `Hindu Festivals & Vrats ${year} — Complete Calendar`;
      const description = `Full list of Hindu festivals, vrats, and observances for ${year}.`;
      const url = `${SITE}/panchang/festivals`;
      let schema;
      if (festivalData?.items?.length) {
        schema = { '@context': 'https://schema.org', '@type': 'ItemList', name: title, description, url, numberOfItems: festivalData.items.length,
          itemListElement: festivalData.items.slice(0, 20).map((item, idx) => ({ '@type': 'ListItem', position: idx + 1, name: item.name, description: item.summary || item.name, url: `${SITE}/panchang/date/${item.date}` })) };
      } else { schema = webPageSchema({ name: title, description, url }); }
      return { title, description, url, schema };
    }
    case 'calendar': {
      const y = calYear || new Date().getFullYear();
      const mo = calMonth || (new Date().getMonth() + 1);
      const monthLabel = `${MONTH_NAMES[mo - 1]} ${y}`;
      const title = `Panchang Calendar — ${monthLabel}`;
      const description = `Hindu Panchang calendar for ${monthLabel}. Daily Tithi, Nakshatra, festivals, and Vedic observances.`;
      const url = `${SITE}/panchang/calendar/${y}/${mo}`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: `${y}-${String(mo).padStart(2,'0')}-01` }) };
    }
    case 'date': {
      if (!dateValue) return null;
      const humanDay = humanDate(dateValue, tz);
      let title, description;
      if (panchangData?.panchang) {
        const { tithi, nakshatra, yoga } = panchangData.panchang;
        title = `Panchang ${humanDay} — ${tithi.name}, ${nakshatra.name} Nakshatra`;
        description = `Panchang for ${humanDay}: ${tithi.name} (${panchangData.panchang.paksha} Paksha), ${nakshatra.name}, Yoga: ${yoga.name}.`;
      } else {
        title = `Panchang — ${humanDay}`;
        description = `Complete Vedic Panchang for ${humanDay}. All timing windows with exact seconds.`;
      }
      const url = `${SITE}/panchang/date/${dateValue}`;
      const [y, mo] = dateValue.split('-');
      const breadcrumb = { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Panchang', item: `${SITE}/panchang/today` },
        { '@type': 'ListItem', position: 2, name: `${MONTH_NAMES[parseInt(mo)-1]} ${y}`, item: `${SITE}/panchang/calendar/${y}/${parseInt(mo)}` },
        { '@type': 'ListItem', position: 3, name: humanDay, item: url },
      ]};
      return { title, description, url, schema: [breadcrumb, webPageSchema({ name: title, description, url, datePublished: dateValue })] };
    }
    case 'muhurat': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Shubh Muhurat Today | Auspicious Timings ${humanToday} | Everyday Horoscope`;
      const description = `Shubh muhurat today for ${humanToday}. All 15 Vedic muhurtas with auspicious time today, muhurta timings, Rahu Kaal, Abhijit & Vijaya Muhurta with exact seconds.`;
      const url = `${SITE}/panchang/muhurat`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    default: return null;
  }
}

function PanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData, locationTZ }) {
  const seo = useMemo(
    () => buildPanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData, locationTZ }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [view, calYear, calMonth, dateValue, festivalData?.items?.length, panchangData?.panchang?.tithi?.name, locationTZ]
  );
  if (!seo) return null;
  const schemas = Array.isArray(seo.schema) ? seo.schema : seo.schema ? [seo.schema] : [];
  return <SEO title={seo.title} description={seo.description} url={seo.url} image={OG_IMAGE} type="website" schema={schemas.length === 1 ? schemas[0] : schemas.length > 1 ? schemas : null} />;
}

// ─── TZ footer note ─────────────────────────────────────────────────────────
function TZNote({ timezone, locationLabel }) {
  if (!timezone) return null;
  return (
    <p className="flex items-center justify-center gap-1.5 text-xs text-muted-foreground">
      <Clock className="h-3 w-3" />
      All times in <span className="font-semibold text-foreground">{getTZAbbr(timezone)}</span>
      {locationLabel ? ` · ${locationLabel}` : ''}
    </p>
  );
}

// ─── SEO body-copy blocks ───────────────────────────────────────────────────
function PanchangDailySEOContent() {
  return (
    <div className="mt-12 space-y-8 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">What is Panchang?</h2><p>Panchang is the traditional Hindu almanac — the word means "five limbs": Tithi, Vara, Nakshatra, Yoga, and Karana. Together they describe the quality of each day according to Vedic astronomy.</p></div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">Auspicious Muhurtas — Brahma, Abhijit, Vijaya</h2><p><strong className="text-foreground">Brahma Muhurta</strong> (96 min before sunrise) is the Creator's Hour — ideal for meditation and new beginnings. <strong className="text-foreground">Abhijit Muhurta</strong> (solar noon ± 24 min) is the most powerful muhurat of the day. <strong className="text-foreground">Vijaya Muhurta</strong> (Victory Hour) is favoured for journeys and ventures — exact timing shifts by weekday.</p></div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">Inauspicious Windows — Rahu Kaal, Yamaganda, Gulika, Dur Muhurta</h2><p>These four windows are traditionally avoided for new activities. Rahu Kaal is the most widely observed — its slot shifts each day of the week. Yamaganda and Gulika Kaal follow their own rotation. Dur Muhurta occurs twice daily at weekday-specific Muhurta positions.</p></div>
    </div>
  );
}

function PanchangTithiSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">Understanding Tithi</h2><p>A Tithi is a lunar day — the Moon moving 12° from the Sun. There are 30 Tithis per lunar cycle: 15 in Shukla Paksha (waxing) and 15 in Krishna Paksha (waning).</p></div>
    </div>
  );
}

function PanchangChoghadiyaSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">What is Choghadiya?</h2><p>Choghadiya (चौघड़िया) divides each day into 8 equal time slots from sunrise to sunset, and 8 night slots from sunset to next sunrise. Each slot is ruled by a planet and carries a quality — Amrit (Moon, best), Shubh (Jupiter, good), Labh (Mercury, good), Char (Venus, neutral/travel), Udveg (Sun, avoid), Kaal (Saturn, avoid), Rog (Mars, avoid). Use Choghadiya for quick muhurat decisions like starting travel, business dealings, or auspicious activities.</p></div>
    </div>
  );
}

function PanchangFestivalsSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">Hindu Festivals and the Vedic Calendar</h2><p>Hindu festivals are computed from Tithi, Nakshatra, and planetary positions — not fixed to the Gregorian calendar. Our dates use the Swiss Ephemeris for maximum accuracy.</p></div>
    </div>
  );
}

// ─── 15-Muhurta data ─────────────────────────────────────────────────────────
const MUHURTA_LIST = [
  { n: 1,  name: 'Rudra',                  quality: 'caution' },
  { n: 2,  name: 'Ahi (Sarpa)',             quality: 'caution' },
  { n: 3,  name: 'Mitra',                   quality: 'good'    },
  { n: 4,  name: 'Pitru (Pitri)',           quality: 'caution' },
  { n: 5,  name: 'Vasu',                    quality: 'good'    },
  { n: 6,  name: 'Vara (Varah)',            quality: 'good'    },
  { n: 7,  name: 'Vishvedeva',              quality: 'good'    },
  { n: 8,  name: 'Vidhi (Brahma)',          quality: 'neutral' },
  { n: 9,  name: 'Satamukhi (Sutamukhi)',   quality: 'good'    },
  { n: 10, name: 'Puruhuta (Indra)',        quality: 'good'    },
  { n: 11, name: 'Vahini',                  quality: 'neutral' },
  { n: 12, name: 'Naktanakara',             quality: 'caution' },
  { n: 13, name: 'Varuna',                  quality: 'good'    },
  { n: 14, name: 'Aryaman',                 quality: 'good'    },
  { n: 15, name: 'Bhaga',                   quality: 'good'    },
];

const MUHURTA_QUALITY_LABEL = { good: 'Auspicious', neutral: 'Neutral', caution: 'Inauspicious' };
const MUHURTA_QUALITY_BADGE = {
  good:    'bg-green-100 text-green-800',
  neutral: 'bg-amber-100 text-amber-800',
  caution: 'bg-red-100 text-red-800',
};

function MuhuratSEOContent() {
  return (
    <div className="mt-12 space-y-8 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">What is Shubh Muhurat?</h2>
        <p>A <strong className="text-foreground">Muhurat</strong> (also spelled Muhurta) is an auspicious time window calculated from the Vedic Panchang — the ancient Hindu almanac. The word literally means "a moment of good omen." In Vedic astrology, not all moments are equal: planetary positions, the lunar day (Tithi), Nakshatra, and the day of the week together determine whether a span of time is favourable, neutral, or to be avoided.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">The 15 Vedic Muhurtas</h2>
        <p>The traditional Vedic system divides each day (sunrise to sunset) into <strong className="text-foreground">15 equal time slots</strong>, each called a Muhurta. The duration of one Muhurta therefore varies by season — roughly 48 minutes on an equinox day. Each slot carries a Sanskrit name and a fixed quality inherited from the presiding deity and planetary ruler. Knowing which Muhurta is active helps practitioners choose the best moment for weddings, business launches, travel, puja, and other significant activities.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Key Auspicious Muhurtas</h2>
        <p><strong className="text-foreground">Abhijit Muhurta</strong> — the solar noon window (±24 min around local solar noon) — is considered the most universally auspicious muhurat and overrides most negative influences. <strong className="text-foreground">Brahma Muhurta</strong> (96 minutes before sunrise) is ideal for study, meditation, and spiritual practice. <strong className="text-foreground">Vijaya Muhurta</strong> (Victory Hour) — weekday-specific — is recommended for journeys and competitive endeavours.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Inauspicious Windows to Avoid</h2>
        <p><strong className="text-foreground">Rahu Kaal</strong> is the most widely observed inauspicious period — its 90-minute slot shifts each day of the week. <strong className="text-foreground">Yamaganda</strong> and <strong className="text-foreground">Gulika Kaal</strong> follow their own weekly rotation. <strong className="text-foreground">Dur Muhurta</strong> occurs twice daily at Rudra and Ahi Muhurta positions. All times shown on this page use the Swiss Ephemeris (pyswisseph) for maximum precision, verified against Drik Panchang.</p>
      </div>
    </div>
  );
}

function MuhuratView({ locationSlug, locationTZ, lang }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true); setError(null); setData(null);
    const tz = locationTZ || 'Asia/Kolkata';
    const dateStr = getTodayInTZ(tz);
    axios.get(`${API}/daily`, { params: { location_slug: locationSlug, date: dateStr } })
      .then(r => setData(r.data))
      .catch(() => setError('Failed to load Muhurat data. Please try again.'))
      .finally(() => setLoading(false));
  }, [locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) return <div className="space-y-4">{[...Array(6)].map((_, i) => <div key={i} className="h-14 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (error)   return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data)   return null;

  const { summary, day_quality_windows } = data;
  const locTZ   = data.location?.timezone || locationTZ || 'Asia/Kolkata';
  const fmtTime = makeFormatTime(locTZ);
  const tzAbbr  = getTZAbbr(locTZ);

  // Derive ISO sunrise/sunset from Brahma Muhurta window (end = sunrise) or time strings + date
  const brahmaWindow = (day_quality_windows || []).find(w => w.label === 'Brahma Muhurta');
  const abhijitWindow = (day_quality_windows || []).find(w => w.label === 'Abhijit Muhurta');
  let sunriseMs = null;
  let sunsetMs  = null;
  if (brahmaWindow?.end) {
    // Brahma Muhurta end is sunrise
    sunriseMs = new Date(brahmaWindow.end).getTime();
  } else if (data.date && summary.sunrise) {
    // Fallback: combine date + time string in location tz
    const [hh, mm, ss] = summary.sunrise.split(':').map(Number);
    const d = new Date(`${data.date}T00:00:00`);
    sunriseMs = d.getTime() + (hh * 3600 + mm * 60 + (ss || 0)) * 1000;
  }
  if (abhijitWindow?.start && abhijitWindow?.end && sunriseMs) {
    // Abhijit = noon ± 24 min; midpoint = solar noon = sunrise + daylight/2
    const noonMs = (new Date(abhijitWindow.start).getTime() + new Date(abhijitWindow.end).getTime()) / 2;
    sunsetMs = sunriseMs + (noonMs - sunriseMs) * 2;
  } else if (data.date && summary.sunset) {
    const [hh, mm, ss] = summary.sunset.split(':').map(Number);
    const d = new Date(`${data.date}T00:00:00`);
    sunsetMs = d.getTime() + (hh * 3600 + mm * 60 + (ss || 0)) * 1000;
  }
  const muhurtaSlots = (sunriseMs && sunsetMs) ? MUHURTA_LIST.map((m, i) => {
    const slotMs = (sunsetMs - sunriseMs) / 15;
    const start  = new Date(sunriseMs + i * slotMs);
    const end    = new Date(sunriseMs + (i + 1) * slotMs);
    return { ...m, start, end };
  }) : null;

  const auspicious   = (day_quality_windows || []).filter(w => w.quality === 'good');
  const inauspicious = (day_quality_windows || []).filter(w => w.quality !== 'good');
  const now = new Date();

  return (
    <div className="space-y-6">
      {/* Hero */}
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Star className="h-5 w-5 text-gold" />
          <div>
            {lang ? (
              <>
                <p className="font-playfair font-semibold text-lg leading-tight">{tLabel('shubhMuhurat', lang)}</p>
                <p className="text-xs text-muted-foreground">Shubh Muhurat — {formatDate(data.date + 'T00:00:00', locTZ)}</p>
              </>
            ) : (
              <span className="font-playfair font-semibold text-lg">Shubh Muhurat — {formatDate(data.date + 'T00:00:00', locTZ)}</span>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground">{data.location?.label}, {data.location?.country}</span>
          <span className="px-1.5 py-0.5 rounded bg-gold/20 text-[10px] font-bold text-gold">{tzAbbr}</span>
        </div>
      </div>

      {/* Auspicious windows */}
      {auspicious.length > 0 && (
        <Card className="border border-green-200 overflow-hidden">
          <div className="px-5 py-3 bg-green-50 border-b border-green-100 flex items-center gap-2">
            <span className="text-green-600">✦</span>
            {lang ? (
              <div>
                <p className="text-xs font-semibold uppercase tracking-widest text-green-700">{tLabel('auspiciousWindows', lang)}</p>
                <p className="text-[10px] text-muted-foreground">Auspicious Windows</p>
              </div>
            ) : (
              <p className="text-xs font-semibold uppercase tracking-widest text-green-700">Auspicious Windows</p>
            )}
          </div>
          <div className="divide-y divide-border">
            {auspicious.map(w => {
              const isCurrent = now >= new Date(w.start) && now <= new Date(w.end);
              const regional = tWin(w.label, lang);
              const showBilingual = lang && regional !== w.label;
              return (
                <div key={w.label} className={`flex items-center justify-between px-5 py-3 ${isCurrent ? 'bg-green-50/60' : ''}`}>
                  <div className="flex items-center gap-3">
                    {isCurrent && <span className="w-2 h-2 rounded-full bg-green-500 flex-shrink-0" />}
                    {showBilingual ? (
                      <div>
                        <p className="text-sm font-medium leading-tight">{regional}</p>
                        <p className="text-[10px] text-muted-foreground">{w.label}</p>
                      </div>
                    ) : (
                      <span className="text-sm font-medium">{w.label}</span>
                    )}
                    {isCurrent && <span className="text-xs text-green-600 font-semibold">{tLabel('now', lang) || 'Now'}</span>}
                  </div>
                  <span className="text-xs text-muted-foreground tabular-nums">{fmtTime(w.start)} — {fmtTime(w.end)}</span>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* 15-Muhurta table */}
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20 flex items-center justify-between">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">15 Vedic Muhurtas — Sunrise to Sunset</p>
          <span className="text-[10px] text-muted-foreground font-semibold">{tzAbbr}</span>
        </div>
        {muhurtaSlots ? (
          <div className="divide-y divide-border">
            {muhurtaSlots.map(m => {
              const isCurrent = now >= m.start && now < m.end;
              const qualityR = lang ? (m.quality === 'good' ? tLabel('auspicious', lang) : m.quality === 'caution' ? tLabel('inauspicious', lang) : tLabel('neutral', lang)) : null;
              return (
                <div key={m.n} className={`flex items-center gap-3 px-5 py-3 ${isCurrent ? 'bg-gold/5 ring-inset ring-1 ring-gold/20' : ''}`}>
                  <span className="w-6 text-center text-xs font-bold text-muted-foreground flex-shrink-0">{m.n}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-sm font-medium">{m.name}</span>
                      {isCurrent && <span className="text-[10px] font-bold text-gold bg-gold/10 px-1.5 py-0.5 rounded">{tLabel('now', lang) || 'NOW'}</span>}
                    </div>
                  </div>
                  <div className={`text-[10px] font-medium px-1.5 py-0.5 rounded flex-shrink-0 text-center ${MUHURTA_QUALITY_BADGE[m.quality]}`}>
                    {lang && qualityR ? (
                      <div>
                        <p>{qualityR}</p>
                        <p className="opacity-70">{MUHURTA_QUALITY_LABEL[m.quality]}</p>
                      </div>
                    ) : MUHURTA_QUALITY_LABEL[m.quality]}
                  </div>
                  <span className="text-xs text-muted-foreground tabular-nums whitespace-nowrap flex-shrink-0">
                    {fmtTime(m.start.toISOString())} — {fmtTime(m.end.toISOString())}
                  </span>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground text-center py-8">Muhurta times require sunrise/sunset data</p>
        )}
      </Card>

      {/* Inauspicious windows */}
      {inauspicious.length > 0 && (
        <Card className="border border-red-200 overflow-hidden">
          <div className="px-5 py-3 bg-red-50 border-b border-red-100 flex items-center gap-2">
            <span className="text-red-500">⚠</span>
            {lang ? (
              <div>
                <p className="text-xs font-semibold uppercase tracking-widest text-red-700">{tLabel('inauspiciousWindows', lang)}</p>
                <p className="text-[10px] text-muted-foreground">Inauspicious Windows — Avoid</p>
              </div>
            ) : (
              <p className="text-xs font-semibold uppercase tracking-widest text-red-700">Inauspicious Windows — Avoid</p>
            )}
          </div>
          <div className="divide-y divide-border">
            {inauspicious.map(w => {
              const isCurrent = now >= new Date(w.start) && now <= new Date(w.end);
              const regional = tWin(w.label, lang);
              const showBilingual = lang && regional !== w.label;
              return (
                <div key={w.label} className={`flex items-center justify-between px-5 py-3 ${isCurrent ? 'bg-red-50/40' : ''}`}>
                  <div className="flex items-center gap-3">
                    {isCurrent && <span className="w-2 h-2 rounded-full bg-red-500 flex-shrink-0" />}
                    {showBilingual ? (
                      <div>
                        <p className="text-sm font-medium leading-tight">{regional}</p>
                        <p className="text-[10px] text-muted-foreground">{w.label}</p>
                      </div>
                    ) : (
                      <span className="text-sm font-medium">{w.label}</span>
                    )}
                    {isCurrent && <span className="text-xs text-red-600 font-semibold">{tLabel('now', lang) || 'Now'}</span>}
                  </div>
                  <span className="text-xs text-muted-foreground tabular-nums">{fmtTime(w.start)} — {fmtTime(w.end)}</span>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      <TZNote timezone={locTZ} locationLabel={data.location?.label} />
      <MuhuratSEOContent />
    </div>
  );
}

function PanchangCalendarSEOContent({ calYear, calMonth }) {
  const monthName = MONTH_NAMES[(calMonth || 1) - 1];
  const year = calYear || new Date().getFullYear();
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">Panchang Calendar — {monthName} {year}</h2><p>Tap any date to see the full Panchang — all five limbs, auspicious & inauspicious windows, Moonrise/Moonset with exact seconds.</p></div>
    </div>
  );
}

function PanchangDateSEOContent({ panchangData }) {
  if (!panchangData?.panchang) return null;
  const { tithi, nakshatra, yoga, karana, paksha, lunar_month, sun_sign, moon_sign } = panchangData.panchang;
  const { sunrise, sunset, moonrise, moonset } = panchangData.summary || {};
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Full Panchang Details</h2>
        <p>Tithi: <strong className="text-foreground">{tithi.name}</strong> ({paksha} Paksha, {lunar_month}). Moon: <strong className="text-foreground">{nakshatra.name}</strong> in {moon_sign}. Sun in {sun_sign}. Yoga: <strong className="text-foreground">{yoga.name}</strong>. Karana: <strong className="text-foreground">{karana.name}</strong>.</p>
        <p className="mt-2 tabular-nums">
          Sunrise: <strong className="text-foreground">{sunrise}</strong>
          {sunset   && <> · Sunset: <strong className="text-foreground">{sunset}</strong></>}
          {moonrise && <> · Moonrise: <strong className="text-foreground">{moonrise}</strong></>}
          {moonset  && <> · Moonset: <strong className="text-foreground">{moonset}</strong></>}
        </p>
      </div>
    </div>
  );
}

// ─── Special Yogas Card ──────────────────────────────────────────────────────

const YOGA_QUALITY_STYLES = {
  good:    { card: 'border-emerald-500/30 bg-emerald-500/5', badge: 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400', dot: 'bg-emerald-500', icon: '✦' },
  caution: { card: 'border-amber-500/30 bg-amber-500/5',   badge: 'bg-amber-500/15 text-amber-600 dark:text-amber-400',   dot: 'bg-amber-500',   icon: '⚠' },
  neutral: { card: 'border-border bg-card',                badge: 'bg-muted text-muted-foreground',                         dot: 'bg-muted-foreground', icon: '·' },
};

function SpecialYogasCard({ yogas }) {
  if (!yogas || yogas.length === 0) return null;
  return (
    <div className="space-y-2">
      {yogas.map(yoga => {
        const s = YOGA_QUALITY_STYLES[yoga.quality] || YOGA_QUALITY_STYLES.neutral;
        return (
          <div key={yoga.name} className={`rounded-xl border p-4 ${s.card}`}>
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2.5 min-w-0">
                <span className={`w-2.5 h-2.5 rounded-full flex-shrink-0 mt-0.5 ${s.dot}`} />
                <div className="min-w-0">
                  <p className="font-playfair font-semibold text-sm text-foreground leading-tight">{yoga.name}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{yoga.meaning}</p>
                </div>
              </div>
              <div className="flex-shrink-0 text-right">
                <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${s.badge}`}>
                  {yoga.quality === 'good' ? 'Auspicious' : yoga.quality === 'caution' ? 'Caution' : 'Neutral'}
                </span>
                <p className="text-[10px] text-muted-foreground mt-1">{yoga.nakshatra} · {yoga.vara}</p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ─── Views ──────────────────────────────────────────────────────────────────

function buildQuickDays(centreISO) {
  const base = new Date(centreISO + 'T00:00:00');
  const todayISO = centreISO; // centre chip is always "active"
  return [-2, -1, 0, 1, 2].map(offset => {
    const d = new Date(base);
    d.setDate(d.getDate() + offset);
    const iso = d.toISOString().slice(0, 10);
    const dayNum = d.getDate();
    let label;
    if (offset === 0)  label = 'Today';
    else if (offset === 1) label = 'Tomorrow';
    else if (offset === -1) label = 'Yesterday';
    else label = d.toLocaleDateString('en-GB', { weekday: 'short' });
    return { iso, label, dayNum, isActive: iso === todayISO };
  });
}

function PanchangDailyView({ dayOffset = 0, locationSlug, locationTZ, onDataLoad, lang }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showWarmup, setShowWarmup] = useState(false);
  const shareCardRef = useRef(null);
  const navigate = useNavigate();

  const tz = locationTZ || 'Asia/Kolkata';
  const centreDate = dayOffset === 1 ? getTomorrowInTZ(tz) : getTodayInTZ(tz);
  const quickDays = buildQuickDays(centreDate);

  // Show warming-up banner if the API call takes more than 4 seconds
  useEffect(() => {
    if (!loading) { setShowWarmup(false); return; }
    const timer = setTimeout(() => { if (loading) setShowWarmup(true); }, 4000);
    return () => clearTimeout(timer);
  }, [loading]);

  useEffect(() => {
    setLoading(true); setError(null); setData(null);
    axios.get(`${API}/daily`, { params: { location_slug: locationSlug, date: centreDate } })
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => setError('Failed to load Panchang data. Please try again.'))
      .finally(() => setLoading(false));
  }, [dayOffset, locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) return (
    <div className="space-y-4">
      {showWarmup && (
        <div className="warming-up-banner flex items-center gap-3 px-4 py-3 rounded-xl border border-amber-300/60 bg-amber-50 text-amber-800 text-sm font-medium shadow-sm">
          <span className="text-lg leading-none">☀️</span>
          <span>Warming up the astrology engine… (first load takes ~10s)</span>
        </div>
      )}
      {[...Array(5)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}
    </div>
  );
  if (error)   return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data)   return null;

  const { summary, panchang, day_quality_windows, observances, special_yogas, lagna_chart } = data;
  const locTZ  = data.location?.timezone || locationTZ || 'Asia/Kolkata';
  const fmtTime = makeFormatTime(locTZ);
  const tzAbbr  = getTZAbbr(locTZ);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Sun className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold text-lg">{formatDate(data.date + 'T00:00:00', locTZ)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground">{data.location?.label}, {data.location?.country}</span>
          <span className="px-1.5 py-0.5 rounded bg-gold/20 text-[10px] font-bold text-gold">{tzAbbr}</span>
        </div>
      </div>

      {/* Quick-date strip — 5 chips centred on current view date */}
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-none">
        {quickDays.map(({ iso, label, dayNum, isActive }) => (
          <button
            key={iso}
            type="button"
            onClick={() => navigate(`/panchang/date/${iso}${locationSlug ? `?location_slug=${locationSlug}` : ''}`)}
            className={`flex-shrink-0 flex flex-col items-center px-4 py-2 rounded-xl border text-sm transition-colors ${
              isActive
                ? 'bg-gold text-background border-gold font-semibold'
                : 'border-gold/30 text-muted-foreground hover:border-gold/60 hover:text-foreground'
            }`}
          >
            <span className="text-[10px] uppercase tracking-wide leading-none mb-0.5">{label}</span>
            <strong className="text-base leading-none">{dayNum}</strong>
          </button>
        ))}
      </div>

      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">{tLabel('fiveLimbs',lang)||'Panch Anga — Five Limbs'}</p>
        </div>
        <div className="divide-y divide-border">
          {[
            { labelR: tLabel('tithi',lang),     labelEn: 'Tithi',        value: tTithi(panchang.tithi.name,lang),   sub: (tPaksha(panchang.paksha,lang)||panchang.paksha) + (lang ? '' : ' Paksha') + (panchang.tithi.end ? ' · until ' + fmtTime(panchang.tithi.end) : '') },
            { labelR: tLabel('nakshatra',lang), labelEn: 'Nakshatra',    value: tNak(panchang.nakshatra.name,lang), sub: (lang ? '' : 'Moon in ') + panchang.moon_sign + (panchang.nakshatra.end ? ' · until ' + fmtTime(panchang.nakshatra.end) : '') },
            { labelR: tLabel('yoga',lang),      labelEn: 'Yoga',         value: panchang.yoga.name,                 sub: panchang.yoga.end ? 'Until ' + fmtTime(panchang.yoga.end) : '' },
            { labelR: tLabel('karana',lang),    labelEn: 'Karana',       value: panchang.karana.name,               sub: panchang.karana.end ? 'Until ' + fmtTime(panchang.karana.end) : '' },
            { labelR: tLabel('vara',lang),      labelEn: 'Vara (Day)',   value: tDay(lang) || summary.weekday,      sub: panchang.samvat },
            { labelR: null,                     labelEn: 'Lunar Month',  value: panchang.lunar_month,               sub: panchang.sun_sign ? 'Sun in ' + panchang.sun_sign : '' },
          ].map(item => (
            <div key={item.labelEn} className="flex items-center justify-between px-5 py-4">
              <div>
                {lang && item.labelR ? (
                  <div className="mb-1">
                    <p className="text-sm font-semibold text-foreground leading-tight">{item.labelR}</p>
                    <p className="text-[10px] text-muted-foreground uppercase tracking-wide">{item.labelEn}</p>
                  </div>
                ) : (
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">{item.labelEn}</p>
                )}
                <p className="font-medium text-sm">{item.value}</p>
              </div>
              {item.sub && <p className="text-xs text-muted-foreground text-right max-w-[220px] tabular-nums">{item.sub}</p>}
            </div>
          ))}
        </div>
      </Card>

      {/* Lagna Chart (current rising sign at sunrise) */}
      {lagna_chart && (
        <Card className="border border-gold/20 overflow-hidden">
          <div className="px-5 py-3 bg-gold/5 border-b border-gold/20 flex items-center gap-2">
            <Star className="h-4 w-4 text-gold" />
            <p className="text-xs font-semibold uppercase tracking-widest text-gold">Lagna — Rising Sign at Sunrise</p>
          </div>
          <div className="p-5 space-y-4">
            <div className="flex gap-6">
              <div>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-0.5">Ascendant</p>
                <p className="text-lg font-semibold text-foreground">{lagna_chart.ascendant_sign}</p>
              </div>
              <div>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-0.5">Degree</p>
                <p className="text-lg font-semibold text-foreground">{lagna_chart.ascendant_degree}°</p>
              </div>
            </div>
            {lagna_chart.houses?.length > 0 && (
              <div className="grid grid-cols-4 gap-1.5">
                {lagna_chart.houses.map(h => (
                  <div
                    key={h.house}
                    className={`flex flex-col items-center justify-center py-2 px-1 rounded-lg border text-center ${
                      h.is_ascendant
                        ? 'border-gold bg-gold/10 text-gold'
                        : 'border-gold/20 bg-gold/5 text-muted-foreground'
                    }`}
                  >
                    <span className="text-[9px] uppercase tracking-wide leading-none">{h.is_ascendant ? 'Asc' : `H${h.house}`}</span>
                    <strong className="text-xs font-medium leading-tight mt-0.5">{h.sign}</strong>
                  </div>
                ))}
              </div>
            )}
          </div>
        </Card>
      )}

      {special_yogas?.length > 0 && (
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-2">Special Yogas</p>
          <SpecialYogasCard yogas={special_yogas} />
        </div>
      )}

      <SunMoonCards summary={summary} panchang={panchang} tzAbbr={tzAbbr} lang={lang} />
      <TimingWindowsCard windows={day_quality_windows} fmtTime={fmtTime} tzAbbr={tzAbbr} lang={lang} />

      {observances?.length > 0 && (
        <Card className="border border-gold/20 p-5">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">{tLabel('observances',lang)||"Today's Observances"}</p>
          <div className="space-y-2">
            {observances.map(o => (
              <div key={o.slug} className="flex items-start gap-3">
                <Star className="h-4 w-4 text-gold mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium">{o.name}</p>
                  <p className="text-xs text-muted-foreground">{o.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
      <TZNote timezone={locTZ} locationLabel={data.location?.label} />

      {/* Share buttons */}
      <Card className="border border-gold/20 p-5">
        <ShareButtons
          pageUrl={`https://www.everydayhoroscope.in/panchang/${dayOffset === 0 ? 'today' : 'tomorrow'}`}
          shareText={`Today's Panchang — ${summary?.weekday}, ${data.date}\nTithi: ${panchang?.tithi?.name} · Nakshatra: ${panchang?.nakshatra?.name} · Yoga: ${panchang?.yoga?.name}\nSunrise: ${summary?.sunrise} · Sunset: ${summary?.sunset}`}
          cardRef={shareCardRef}
          filename={`panchang-${data.location?.slug || 'india'}-${data.date || 'today'}`}
          fbPageCaption={`🙏 Today's Panchang — ${summary?.weekday}, ${data.date}
📍 ${data.location?.label || 'India'}

🌅 Sunrise: ${summary?.sunrise}  |  🌇 Sunset: ${summary?.sunset}
🌙 Tithi: ${panchang?.tithi?.name}
⭐ Nakshatra: ${panchang?.nakshatra?.name}
🔯 Yoga: ${panchang?.yoga?.name}

📿 Visit everydayhoroscope.in for complete Panchang details
#Panchang #VedicAstrology #EverydayHoroscope #HinduCalendar #DrikPanchang`}
        />
      </Card>

      {/* Off-screen share card rendered for html2canvas capture */}
      <PanchangShareCard data={data} cardRef={shareCardRef} />

      <div className="flex gap-3">
        <Link to={`/panchang/calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`}
          className="flex-1 flex items-center justify-center gap-2 py-3 border border-gold/30 rounded-xl text-sm font-medium text-gold hover:bg-gold/5 transition-colors">
          <Calendar className="h-4 w-4" /> Monthly Calendar
        </Link>
        <Link to="/panchang/festivals"
          className="flex-1 flex items-center justify-center gap-2 py-3 border border-gold/30 rounded-xl text-sm font-medium text-gold hover:bg-gold/5 transition-colors">
          <Sparkles className="h-4 w-4" /> Festivals &amp; Vrats
        </Link>
      </div>
      <PanchangDailySEOContent />
    </div>
  );
}

function PanchangTithiView({ locationSlug, lang }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    axios.get(`${API}/daily`, { params: { location_slug: locationSlug } })
      .then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, [locationSlug]);
  if (loading) return <div className="space-y-4">{[...Array(3)].map((_, i) => <div key={i} className="h-20 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data)   return <p className="text-center text-muted-foreground py-12">Failed to load Tithi data</p>;
  const { panchang, summary } = data;
  const locTZ  = data.location?.timezone;
  const fmtTime = makeFormatTime(locTZ);
  const tithiName = tTithi(panchang.tithi.name, lang) || panchang.tithi.name;
  const pakshaName = tPaksha(panchang.paksha, lang) || panchang.paksha;
  const nakName = tNak(panchang.nakshatra.name, lang) || panchang.nakshatra.name;
  const moonFields = [
    { labelR: tLabel('moonSign', lang), labelEn: 'Moon Sign', value: panchang.moon_sign },
    { labelR: tLabel('nakshatra', lang), labelEn: 'Nakshatra', value: nakName },
    { labelR: tLabel('moonrise', lang), labelEn: 'Moonrise', value: summary.moonrise || '--' },
    { labelR: tLabel('moonset', lang), labelEn: 'Moonset', value: summary.moonset || '--' },
    { labelR: tLabel('vara', lang), labelEn: 'Weekday', value: tDay(lang) || summary.weekday },
    { labelR: tLabel('samvat', lang), labelEn: 'Samvat', value: panchang.samvat },
  ];
  return (
    <div className="space-y-6">
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          {lang ? (
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest text-gold">{tLabel('todayTithi', lang)}</p>
              <p className="text-[10px] text-muted-foreground uppercase tracking-wide">Today's Tithi</p>
            </div>
          ) : (
            <p className="text-xs font-semibold uppercase tracking-widest text-gold">Today's Tithi</p>
          )}
        </div>
        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-3xl font-playfair font-bold">{tithiName}</p>
              {lang && tithiName !== panchang.tithi.name && (
                <p className="text-sm text-muted-foreground">{panchang.tithi.name}</p>
              )}
              <p className="text-muted-foreground mt-1">{pakshaName}{lang ? '' : ' Paksha'}</p>
            </div>
            <Moon className="h-10 w-10 text-gold/60" />
          </div>
          {panchang.tithi.end && (
            <p className="text-sm text-muted-foreground border-t border-border pt-3 tabular-nums">
              Ends at <span className="font-semibold text-foreground">{fmtTime(panchang.tithi.end)}</span>
              {' '}<span className="text-[10px] font-bold text-gold">{getTZAbbr(locTZ)}</span>
            </p>
          )}
        </div>
      </Card>
      <Card className="border border-gold/20 p-5">
        {lang ? (
          <div className="mb-3">
            <p className="text-xs font-semibold uppercase tracking-widest text-gold">{tLabel('moonPosition', lang)}</p>
            <p className="text-[10px] text-muted-foreground uppercase tracking-wide">Moon Position</p>
          </div>
        ) : (
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">Moon Position</p>
        )}
        <div className="grid grid-cols-2 gap-4">
          {moonFields.map(f => (
            <div key={f.labelEn}>
              {lang && f.labelR ? (
                <div>
                  <p className="text-xs font-semibold text-foreground leading-tight">{f.labelR}</p>
                  <p className="text-[10px] text-muted-foreground uppercase tracking-wide">{f.labelEn}</p>
                </div>
              ) : (
                <p className="text-xs text-muted-foreground">{f.labelEn}</p>
              )}
              <p className="font-semibold mt-0.5 text-sm">{f.value}</p>
            </div>
          ))}
        </div>
      </Card>
      <TZNote timezone={locTZ} locationLabel={data.location?.label} />
      <PanchangTithiSEOContent />
    </div>
  );
}

const CHOG_QUALITY_STYLES = {
  good:    { row: 'border-green-200 bg-green-50/40', badge: 'bg-green-100 text-green-800', dot: 'bg-green-500' },
  neutral: { row: 'border-amber-200 bg-amber-50/40', badge: 'bg-amber-100 text-amber-800', dot: 'bg-amber-500' },
  caution: { row: 'border-red-200 bg-red-50/20',    badge: 'bg-red-100 text-red-800',     dot: 'bg-red-400' },
};

function ChoghadiyaSlotRow({ slot, fmtTime, now, lang }) {
  const isNow = now >= new Date(slot.start) && now < new Date(slot.end);
  const s = CHOG_QUALITY_STYLES[slot.quality] || CHOG_QUALITY_STYLES.neutral;
  const qualityEn = slot.quality === 'good' ? 'Auspicious' : slot.quality === 'caution' ? 'Inauspicious' : 'Neutral';
  const qualityR = tChogQuality(slot.quality, lang);
  return (
    <div className={`flex items-center justify-between px-3 py-2.5 rounded-lg border ${s.row} ${isNow ? 'ring-2 ring-gold/60' : ''}`}>
      <div className="flex items-center gap-2.5 min-w-0">
        <span className={`w-2 h-2 rounded-full flex-shrink-0 ${s.dot}`} />
        <div className="min-w-0">
          <span className="font-semibold text-sm text-foreground">{slot.name}</span>
          <span className="text-xs text-muted-foreground ml-1.5">{slot.ruler}</span>
        </div>
        {isNow && <span className="text-[10px] font-bold text-gold bg-gold/10 px-1.5 py-0.5 rounded">{lang ? tLabel('now', lang) : 'NOW'}</span>}
      </div>
      <div className="flex items-center gap-2 flex-shrink-0">
        <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded text-center ${s.badge}`}>
          {lang && qualityR ? <><span className="block">{qualityR}</span><span className="block opacity-70">{qualityEn}</span></> : qualityEn}
        </span>
        <span className="text-xs text-muted-foreground whitespace-nowrap">{fmtTime(slot.start)}–{fmtTime(slot.end)}</span>
      </div>
    </div>
  );
}

function PanchangChoghadiyaView({ locationSlug, lang }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    axios.get(`${API}/choghadiya`, { params: { location_slug: locationSlug } })
      .then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, [locationSlug]);
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 60000);
    return () => clearInterval(t);
  }, []);
  if (loading) return <div className="space-y-2">{[...Array(8)].map((_, i) => <div key={i} className="h-11 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data)   return <p className="text-center text-muted-foreground py-12">Failed to load Choghadiya</p>;
  const locTZ   = data.location?.timezone;
  const fmtTime = makeFormatTime(locTZ);
  const tzAbbr  = getTZAbbr(locTZ);
  return (
    <div className="space-y-5">
      {/* Day Choghadiya */}
      <div className="rounded-xl border border-border bg-card p-4 space-y-3">
        <div className="flex items-center gap-2">
          <Sun className="h-4 w-4 text-gold" />
          <div>
            {lang ? (
              <>
                <h3 className="font-playfair font-semibold text-base leading-tight">{tLabel('dayChoghadiya', lang)}</h3>
                <p className="text-[10px] text-muted-foreground">Day Choghadiya</p>
              </>
            ) : (
              <h3 className="font-playfair font-semibold text-base">Day Choghadiya</h3>
            )}
          </div>
          <span className="text-xs text-muted-foreground ml-auto">{fmtTime(data.sunrise)} – {fmtTime(data.sunset)}</span>
        </div>
        <div className="space-y-1.5">
          {data.day_choghadiya.map(slot => (
            <ChoghadiyaSlotRow key={slot.index} slot={slot} fmtTime={fmtTime} now={now} lang={lang} />
          ))}
        </div>
      </div>
      {/* Night Choghadiya */}
      <div className="rounded-xl border border-border bg-card p-4 space-y-3">
        <div className="flex items-center gap-2">
          <Moon className="h-4 w-4 text-gold" />
          <div>
            {lang ? (
              <>
                <h3 className="font-playfair font-semibold text-base leading-tight">{tLabel('nightChoghadiya', lang)}</h3>
                <p className="text-[10px] text-muted-foreground">Night Choghadiya</p>
              </>
            ) : (
              <h3 className="font-playfair font-semibold text-base">Night Choghadiya</h3>
            )}
          </div>
          <span className="text-xs text-muted-foreground ml-auto">{fmtTime(data.sunset)} – {fmtTime(data.next_sunrise)}</span>
        </div>
        <div className="space-y-1.5">
          {data.night_choghadiya.map(slot => (
            <ChoghadiyaSlotRow key={slot.index} slot={slot} fmtTime={fmtTime} now={now} lang={lang} />
          ))}
        </div>
      </div>
      <TZNote timezone={locTZ} locationLabel={data.location?.label} />
      <PanchangChoghadiyaSEOContent />
    </div>
  );
}

function PanchangCalendarView({ year, month, locationSlug, lang }) {
  const navigate = useNavigate();
  const today = new Date();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setLoading(true); setData(null);
    axios.get(`${API}/calendar/${year}/${month}`, { params: { location_slug: locationSlug } })
      .then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, [year, month, locationSlug]);
  const prevMonth = month === 1 ? { y: year - 1, m: 12 } : { y: year, m: month - 1 };
  const nextMonth = month === 12 ? { y: year + 1, m: 1 } : { y: year, m: month + 1 };
  const todayISO = today.toISOString().slice(0, 10);
  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <button onClick={() => navigate(`/panchang/calendar/${prevMonth.y}/${prevMonth.m}`)} className="p-2 hover:bg-gold/10 rounded-lg transition-colors"><ChevronLeft className="h-5 w-5 text-gold" /></button>
        <h2 className="font-playfair font-semibold text-xl">{data?.month_label || `${month}/${year}`}</h2>
        <button onClick={() => navigate(`/panchang/calendar/${nextMonth.y}/${nextMonth.m}`)} className="p-2 hover:bg-gold/10 rounded-lg transition-colors"><ChevronRight className="h-5 w-5 text-gold" /></button>
      </div>
      {loading ? (
        <div className="grid grid-cols-7 gap-1">{[...Array(35)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>
      ) : data ? (
        <div className="space-y-1">
          <div className="grid grid-cols-7 gap-1 mb-2">
            {(lang && LANG_WEEKDAY_ABBR[lang]
              ? LANG_WEEKDAY_ABBR[lang].map((r, i) => ({ r, en: ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][i] }))
              : ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map(en => ({ r: null, en }))
            ).map(({ r, en }) => (
              <div key={en} className="text-center py-1">
                {r ? (
                  <>
                    <p className="text-xs font-semibold text-muted-foreground leading-tight">{r}</p>
                    <p className="text-[9px] text-muted-foreground/60">{en}</p>
                  </>
                ) : (
                  <p className="text-xs font-semibold text-muted-foreground">{en}</p>
                )}
              </div>
            ))}
          </div>
          {(() => {
            const firstDay = new Date(year, month - 1, 1).getDay();
            const cells = [...Array(firstDay).fill(null), ...data.days];
            const rows = [];
            for (let i = 0; i < cells.length; i += 7) rows.push(cells.slice(i, i + 7));
            return rows.map((row, ri) => (
              <div key={ri} className="grid grid-cols-7 gap-1">
                {row.map((day, ci) => {
                  if (!day) return <div key={ci} />;
                  const isToday = day.date === todayISO;
                  const hasFestival = day.observances?.length > 0;
                  return (
                    <button key={day.date} onClick={() => navigate(`/panchang/date/${day.date}`)}
                      className={`p-1.5 rounded-lg border text-center w-full transition-all hover:border-gold hover:bg-gold/10 hover:shadow-sm ${isToday ? 'border-gold bg-gold/10' : 'border-border'}`}>
                      <p className={`text-sm font-semibold ${isToday ? 'text-gold' : ''}`}>{day.day}</p>
                      <p className="text-[9px] text-muted-foreground leading-tight mt-0.5 truncate">{day.tithi.split(' ')[1] || day.tithi}</p>
                      {hasFestival && <div className="w-1 h-1 bg-gold rounded-full mx-auto mt-1" />}
                    </button>
                  );
                })}
              </div>
            ));
          })()}
        </div>
      ) : <p className="text-center text-muted-foreground py-12">Failed to load calendar</p>}
      <p className="text-xs text-center text-muted-foreground">
        {lang ? <><span>{tLabel('tapDate', lang)}</span> · </> : null}Tap any date to view full Panchang details
      </p>
      <PanchangCalendarSEOContent calYear={year} calMonth={month} />
    </div>
  );
}

// Festivals observance type translations
const LANG_OBS_TYPE = {
  tamil:    { festival:'திருவிழா', vrat:'விரதம்', ekadashi:'ஏகாதசி', purnima:'பூர்ணிமை', amavasya:'அமாவாசை', chaturthi:'சதுர்த்தி', sankranti:'சங்க்ரான்தி', navratri:'நவராத்திரி' },
  telugu:   { festival:'పండుగ',   vrat:'వ్రతం',    ekadashi:'ఏకాదశి', purnima:'పౌర్ణమి', amavasya:'అమావాస్య', chaturthi:'చవితి', sankranti:'సంక్రాంతి', navratri:'నవరాత్రులు' },
  malayalam:{ festival:'ഉത്സവം',  vrat:'വ്രതം',   ekadashi:'ഏകാദശി', purnima:'പൗർണ്ണമി', amavasya:'അമാവാസ്യ', chaturthi:'ചതുർഥി', sankranti:'സംക്രാന്തി', navratri:'നവരാത്രി' },
  kannada:  { festival:'ಹಬ್ಬ',    vrat:'ವ್ರತ',    ekadashi:'ಏಕಾದಶಿ', purnima:'ಹುಣ್ಣಿಮೆ', amavasya:'ಅಮಾವಾಸ್ಯೆ', chaturthi:'ಚೌತಿ', sankranti:'ಸಂಕ್ರಾಂತಿ', navratri:'ನವರಾತ್ರಿ' },
  hindi:    { festival:'त्योहार', vrat:'व्रत',     ekadashi:'एकादशी',  purnima:'पूर्णिमा',  amavasya:'अमावस्या',  chaturthi:'चतुर्थी', sankranti:'संक्रांति',  navratri:'नवरात्रि' },
};

function PanchangFestivalsView({ locationSlug, onDataLoad, lang }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const year = new Date().getFullYear();
  useEffect(() => {
    axios.get(`${API}/festivals`, { params: { year, location_slug: locationSlug } })
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => setData(null)).finally(() => setLoading(false));
  }, [locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps
  if (loading) return <div className="space-y-3">{[...Array(8)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data?.items?.length) return <p className="text-center text-muted-foreground py-12">No festivals found</p>;
  const grouped = data.items.reduce((acc, item) => { const m = item.date.slice(0,7); if (!acc[m]) acc[m]=[]; acc[m].push(item); return acc; }, {});
  return (
    <div className="space-y-6">
      {Object.entries(grouped).map(([m, items]) => (
        <div key={m}>
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">
            {new Date(m + '-01').toLocaleDateString('en-IN', { month: 'long', year: 'numeric' })}
          </p>
          <div className="space-y-2">
            {items.map(item => (
              <div key={item.slug + item.date} className="flex items-start gap-4 p-4 border border-gold/20 rounded-xl bg-gold/5">
                <div className="text-center min-w-[40px]">
                  <p className="text-xl font-playfair font-bold text-gold">{new Date(item.date + 'T00:00:00').getDate()}</p>
                  <p className="text-[10px] text-muted-foreground uppercase">{new Date(item.date + 'T00:00:00').toLocaleDateString('en-IN', { weekday: 'short' })}</p>
                </div>
                <div>
                  {(() => {
                    const typeKey = item.observance_type?.toLowerCase();
                    const typeR = lang ? (LANG_OBS_TYPE[lang]?.[typeKey] || null) : null;
                    const typeColor = typeKey === 'festival' ? 'bg-amber-100 text-amber-800' : typeKey === 'vrat' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800';
                    return (
                      <span className={`text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full ${typeColor}`}>
                        {typeR ? <>{typeR} · {item.observance_type}</> : item.observance_type}
                      </span>
                    );
                  })()}
                  <p className="font-semibold text-sm mt-1">{item.name}</p>
                  <p className="text-xs text-muted-foreground">{item.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
      <PanchangFestivalsSEOContent />
    </div>
  );
}

function PanchangDateView({ dateStr, locationSlug, onDataLoad }) {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    setLoading(true); setError(null); setData(null);
    axios.get(`${API}/date/${dateStr}`, { params: { location_slug: locationSlug } })
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => {
        axios.get(`${API}/daily`, { params: { date: dateStr, location_slug: locationSlug } })
          .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
          .catch(() => setError('Failed to load Panchang data.'))
          .finally(() => setLoading(false));
      })
      .finally(() => setLoading(false));
  }, [dateStr, locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps
  if (loading) return <div className="space-y-4">{[...Array(5)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (error)   return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data)   return null;
  const { summary, panchang, day_quality_windows, observances, special_yogas } = data;
  const locTZ  = data.location?.timezone || 'Asia/Kolkata';
  const fmtTime = makeFormatTime(locTZ);
  const tzAbbr  = getTZAbbr(locTZ);
  const [y, mo] = dateStr.split('-');
  return (
    <div className="space-y-6">
      <button onClick={() => navigate(`/panchang/calendar/${y}/${parseInt(mo)}`)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-gold transition-colors">
        <ChevronLeft className="h-4 w-4" /> Back to Calendar
      </button>
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Sun className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold text-lg">{formatDate(data.date + 'T00:00:00', locTZ)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground">{data.location?.label}, {data.location?.country}</span>
          <span className="px-1.5 py-0.5 rounded bg-gold/20 text-[10px] font-bold text-gold">{tzAbbr}</span>
        </div>
      </div>
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Panch Anga — Five Limbs</p>
        </div>
        <div className="divide-y divide-border">
          {[
            { label: 'Tithi',      value: panchang.tithi.name,     sub: panchang.paksha + ' Paksha' },
            { label: 'Nakshatra',  value: panchang.nakshatra.name, sub: 'Moon in ' + panchang.moon_sign },
            { label: 'Yoga',       value: panchang.yoga.name,      sub: '' },
            { label: 'Karana',     value: panchang.karana.name,    sub: '' },
            { label: 'Vara (Day)', value: summary.weekday,          sub: panchang.samvat },
          ].map(item => (
            <div key={item.label} className="flex items-center justify-between px-5 py-4">
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">{item.label}</p>
                <p className="font-medium text-sm">{item.value}</p>
              </div>
              {item.sub && <p className="text-xs text-muted-foreground text-right max-w-[200px]">{item.sub}</p>}
            </div>
          ))}
        </div>
      </Card>
      {special_yogas?.length > 0 && (
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-2">Special Yogas</p>
          <SpecialYogasCard yogas={special_yogas} />
        </div>
      )}
      <SunMoonCards summary={summary} panchang={panchang} tzAbbr={tzAbbr} />
      <TimingWindowsCard windows={day_quality_windows} fmtTime={fmtTime} tzAbbr={tzAbbr} />
      {observances?.length > 0 && (
        <Card className="border border-gold/20 p-5">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">Observances</p>
          <div className="space-y-2">
            {observances.map(o => (
              <div key={o.slug} className="flex items-start gap-3">
                <Star className="h-4 w-4 text-gold mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium">{o.name}</p>
                  <p className="text-xs text-muted-foreground">{o.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
      <TZNote timezone={locTZ} locationLabel={data.location?.label} />
      <PanchangDateSEOContent panchangData={data} />
    </div>
  );
}

// ─── Main page ──────────────────────────────────────────────────────────────
export const PanchangPage = ({ lang } = {}) => {
  const { type: rawType = 'daily', year: yearParam, month: monthParam, dateValue } = useParams();
  const resolvedType = ALIAS[rawType] || rawType;
  const isCalendar = resolvedType === 'calendar' || (yearParam && monthParam && !dateValue);
  const isDateView = !!dateValue;
  const activeView = isDateView ? 'date' : isCalendar ? 'calendar' : (resolvedType || 'daily');
  const today = new Date();
  const calYear  = parseInt(yearParam)  || today.getFullYear();
  const calMonth = parseInt(monthParam) || (today.getMonth() + 1);

  const [locationSlug, setLocationSlug] = useState(() => localStorage.getItem(LOC_STORAGE_KEY) || DEFAULT_SLUG);
  const [locationTZ,   setLocationTZ]   = useState('Asia/Kolkata');

  const handleLocationSelect = useCallback((slug) => {
    setLocationSlug(slug);
    localStorage.setItem(LOC_STORAGE_KEY, slug);
  }, []);

  useEffect(() => {
    axios.get(`${API}/locations`)
      .then(r => {
        const loc = r.data.find(l => l.slug === locationSlug);
        if (loc?.timezone) setLocationTZ(loc.timezone);
      })
      .catch(() => {});
  }, [locationSlug]);

  const [festivalData, setFestivalData] = useState(null);
  const [panchangData, setPanchangData] = useState(null);

  useEffect(() => {
    setFestivalData(null);
    setPanchangData(null);
  }, [activeView, dateValue, calYear, calMonth, locationSlug]);

  const config = isDateView
    ? { title: 'Panchang Details', icon: Calendar, desc: 'Complete Vedic almanac for the selected date' }
    : (TYPE_META[activeView] || TYPE_META.daily);

  const langBase = lang ? `/panchang/${lang}` : '/panchang';
  const L = lang ? (LANG_LABELS_MAP[lang] || {}) : {};
  const subNavItems = [
    { key: 'daily',       label: L.tabToday      || 'Today',      icon: Sun,      path: `${langBase}/today` },
    { key: 'tomorrow',    label: L.tabTomorrow   || 'Tomorrow',   icon: Sun,      path: `${langBase}/tomorrow` },
    { key: 'tithi',       label: L.tabTithi      || 'Tithi',      icon: Moon,     path: `${langBase}/tithi` },
    { key: 'muhurat',     label: L.tabMuhurat    || 'Muhurat',    icon: Star,     path: `${langBase}/muhurat` },
    { key: 'choghadiya',  label: L.tabChoghadiya || 'Choghadiya', icon: Zap,      path: `${langBase}/choghadiya` },
    { key: 'calendar',    label: L.tabCalendar   || 'Calendar',   icon: Calendar, path: `${langBase}/calendar/${today.getFullYear()}/${today.getMonth() + 1}` },
    { key: 'festivals',   label: L.tabFestivals  || 'Festivals',  icon: Sparkles, path: `${langBase}/festivals` },
  ];

  const subNavActive = activeView === 'date' ? 'calendar' : activeView;

  return (
    <div className="max-w-3xl mx-auto px-4 py-10 pb-24 lg:pb-10">
      <PanchangSEO
        view={activeView} calYear={calYear} calMonth={calMonth}
        dateValue={dateValue} festivalData={festivalData}
        panchangData={panchangData} locationTZ={locationTZ}
      />
      <div className="text-center mb-6">
        {lang && LANG_META_MAP[lang] ? (
          <>
            <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
              <Calendar className="h-3 w-3" /> {LANG_META_MAP[lang].nativeName} · Vedic Panchang
            </div>
            <h1 className="text-3xl font-playfair font-semibold mb-2">{LANG_META_MAP[lang].badge}</h1>
            <p className="text-muted-foreground">{config.title}</p>
          </>
        ) : (
          <>
            <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
              <Calendar className="h-3 w-3" /> Vedic Panchang
            </div>
            <h1 className="text-3xl font-playfair font-semibold mb-2">{config.title}</h1>
            <p className="text-muted-foreground">{config.desc}</p>
          </>
        )}
      </div>
      <div className="flex justify-end mb-4">
        <LocationPicker selectedSlug={locationSlug} onSelect={handleLocationSelect} />
      </div>
      <div className="flex flex-wrap gap-2 mb-8 border-b border-border pb-4">
        {subNavItems.map(({ key, label, icon: Icon, path }) => (
          <Link key={key} to={path} className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${subNavActive === key ? 'bg-gold text-white' : 'border border-border text-muted-foreground hover:border-gold/50 hover:text-gold'}`}>
            <Icon className="h-3 w-3" />{label}
          </Link>
        ))}
      </div>
      {isDateView                                 && <PanchangDateView     dateStr={dateValue}           locationSlug={locationSlug} onDataLoad={setPanchangData} />}
      {!isDateView && activeView === 'daily'      && <><PanchangCosmicMap locationSlug={locationSlug} dayOffset={0} /><PanchangDailyView    dayOffset={0}                 locationSlug={locationSlug} locationTZ={locationTZ} onDataLoad={setPanchangData} lang={lang} /></>}
      {!isDateView && activeView === 'tomorrow'   && <><PanchangCosmicMap locationSlug={locationSlug} dayOffset={1} /><PanchangDailyView    dayOffset={1}                 locationSlug={locationSlug} locationTZ={locationTZ} onDataLoad={setPanchangData} lang={lang} /></>}
      {!isDateView && activeView === 'tithi'      && <PanchangTithiView                                  locationSlug={locationSlug} lang={lang} />}
      {!isDateView && activeView === 'muhurat'    && <MuhuratView                                        locationSlug={locationSlug} locationTZ={locationTZ} lang={lang} />}
      {!isDateView && activeView === 'choghadiya' && <PanchangChoghadiyaView                             locationSlug={locationSlug} lang={lang} />}
      {!isDateView && activeView === 'calendar'   && <PanchangCalendarView year={calYear} month={calMonth} locationSlug={locationSlug} lang={lang} />}
      {!isDateView && activeView === 'festivals'  && <PanchangFestivalsView                              locationSlug={locationSlug} onDataLoad={setFestivalData} lang={lang} />}
    </div>
  );
};
