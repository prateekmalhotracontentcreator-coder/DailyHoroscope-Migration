/**
 * PanchangLangPage.jsx
 * Regional-language Panchang pages for Tamil, Telugu, Malayalam, Kannada, Hindi.
 * Same astronomical data from /api/panchang/daily — only labels & SEO are localised.
 */
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Sun, Moon, MapPin, Globe, ChevronDown } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API        = `${BACKEND_URL}/api/panchang`;
const LOC_KEY    = 'panchang_location_slug';
const DEFAULT    = 'new-delhi-india';
const SITE       = 'https://everydayhoroscope.in';

// ─── Language Metadata ───────────────────────────────────────────────────────
const LANG_META = {
  tamil: {
    code: 'ta',
    nativeName: 'தமிழ்',
    pageTitle: 'தமிழ் பஞ்சாங்கம்',
    seoTitle: 'இன்றைய தமிழ் பஞ்சாங்கம்',
    seoDesc: 'இன்றைய தமிழ் பஞ்சாங்கம் — திதி, நட்சத்திரம், யோகம், கரணம், சூரிய உதயம், ராகு காலம் | Everyday Horoscope',
    h1Prefix: 'இன்றைய தமிழ் பஞ்சாங்கம்',
    today: 'இன்று',
  },
  telugu: {
    code: 'te',
    nativeName: 'తెలుగు',
    pageTitle: 'తెలుగు పంచాంగం',
    seoTitle: 'నేటి తెలుగు పంచాంగం',
    seoDesc: 'నేటి తెలుగు పంచాంగం — తిథి, నక్షత్రం, యోగం, కరణం, సూర్యోదయం, రాహు కాలం | Everyday Horoscope',
    h1Prefix: 'నేటి తెలుగు పంచాంగం',
    today: 'నేడు',
  },
  malayalam: {
    code: 'ml',
    nativeName: 'മലയാളം',
    pageTitle: 'മലയാളം പഞ്ചാംഗം',
    seoTitle: 'ഇന്നത്തെ മലയാളം പഞ്ചാംഗം',
    seoDesc: 'ഇന്നത്തെ മലയാളം പഞ്ചാംഗം — തിഥി, നക്ഷത്രം, യോഗം, കരണം, സൂര്യോദയം, രാഹു കാലം | Everyday Horoscope',
    h1Prefix: 'ഇന്നത്തെ മലയാളം പഞ്ചാംഗം',
    today: 'ഇന്ന്',
  },
  kannada: {
    code: 'kn',
    nativeName: 'ಕನ್ನಡ',
    pageTitle: 'ಕನ್ನಡ ಪಂಚಾಂಗ',
    seoTitle: 'ಇಂದಿನ ಕನ್ನಡ ಪಂಚಾಂಗ',
    seoDesc: 'ಇಂದಿನ ಕನ್ನಡ ಪಂಚಾಂಗ — ತಿಥಿ, ನಕ್ಷತ್ರ, ಯೋಗ, ಕರಣ, ಸೂರ್ಯೋದಯ, ರಾಹು ಕಾಲ | Everyday Horoscope',
    h1Prefix: 'ಇಂದಿನ ಕನ್ನಡ ಪಂಚಾಂಗ',
    today: 'ಇಂದು',
  },
  hindi: {
    code: 'hi',
    nativeName: 'हिंदी',
    pageTitle: 'हिंदी पंचांग',
    seoTitle: 'आज का हिंदी पंचांग',
    seoDesc: 'आज का हिंदी पंचांग — तिथि, नक्षत्र, योग, करण, सूर्योदय, राहु काल | Everyday Horoscope',
    h1Prefix: 'आज का हिंदी पंचांग',
    today: 'आज',
  },
};

// ─── Label Translations ───────────────────────────────────────────────────────
const LABELS = {
  tamil: {
    sunrise:   'சூரிய உதயம்',
    sunset:    'சூரிய அஸ்தமனம்',
    moonrise:  'சந்திர உதயம்',
    moonset:   'சந்திர அஸ்தமனம்',
    tithi:     'திதி',
    nakshatra: 'நட்சத்திரம்',
    yoga:      'யோகம்',
    karana:    'கரணம்',
    vara:      'வாரம்',
    paksha:    'பக்ஷம்',
    month:     'மாதம்',
    year:      'ஆண்டு',
    samvat:    'சம்வத்',
    rahukaal:  'ராகு காலம்',
    auspicious:'நல்ல நேரம்',
    inauspicious: 'தீய நேரம்',
    timings:   'நேர அட்டவணை',
    fiveLimbs: 'பஞ்சாங்கம் — ஐந்து அங்கங்கள்',
    endsAt:    'முடியும் நேரம்',
    sunIn:     'சூரியன்',
    moonIn:    'சந்திரன்',
    nakshatraOf: 'நட்சத்திரம்',
    pakshaBadge: 'பக்ஷம்',
    brahma:    'பிரம்ம முகூர்த்தம்',
    abhijit:   'அபிஜித் முகூர்த்தம்',
    vijaya:    'விஜய முகூர்த்தம்',
    rahu:      'ராகு காலம்',
    yama:      'யமகண்டம்',
    gulika:    'குளிக காலம்',
    dur:       'துர் முகூர்த்தம்',
    now:       'இப்போது',
  },
  telugu: {
    sunrise:   'సూర్యోదయం',
    sunset:    'సూర్యాస్తమయం',
    moonrise:  'చంద్రోదయం',
    moonset:   'చంద్రాస్తమయం',
    tithi:     'తిథి',
    nakshatra: 'నక్షత్రం',
    yoga:      'యోగం',
    karana:    'కరణం',
    vara:      'వారం',
    paksha:    'పక్షం',
    month:     'మాసం',
    year:      'సంవత్సరం',
    samvat:    'సంవత్',
    rahukaal:  'రాహు కాలం',
    auspicious:'శుభ సమయం',
    inauspicious: 'అశుభ సమయం',
    timings:   'సమయ వివరాలు',
    fiveLimbs: 'పంచాంగం — పంచ అంగాలు',
    endsAt:    'ముగింపు సమయం',
    sunIn:     'సూర్యుడు',
    moonIn:    'చంద్రుడు',
    nakshatraOf: 'నక్షత్రం',
    pakshaBadge: 'పక్షం',
    brahma:    'బ్రహ్మ ముహూర్తం',
    abhijit:   'అభిజిత్ ముహూర్తం',
    vijaya:    'విజయ ముహూర్తం',
    rahu:      'రాహు కాలం',
    yama:      'యమగండం',
    gulika:    'గులిక కాలం',
    dur:       'దుర్ ముహూర్తం',
    now:       'ఇప్పుడు',
  },
  malayalam: {
    sunrise:   'സൂര്യോദയം',
    sunset:    'സൂര്യാസ്തമയം',
    moonrise:  'ചന്ദ്രോദയം',
    moonset:   'ചന്ദ്രാസ്തമയം',
    tithi:     'തിഥി',
    nakshatra: 'നക്ഷത്രം',
    yoga:      'യോഗം',
    karana:    'കരണം',
    vara:      'വാരം',
    paksha:    'പക്ഷം',
    month:     'മാസം',
    year:      'വർഷം',
    samvat:    'സംവത്',
    rahukaal:  'രാഹു കാലം',
    auspicious:'ശുഭ സമയം',
    inauspicious: 'അശുഭ സമയം',
    timings:   'സമയ വിവരങ്ങൾ',
    fiveLimbs: 'പഞ്ചാംഗം — പഞ്ച അംഗങ്ങൾ',
    endsAt:    'അവസാന സമയം',
    sunIn:     'സൂര്യൻ',
    moonIn:    'ചന്ദ്രൻ',
    nakshatraOf: 'നക്ഷത്രം',
    pakshaBadge: 'പക്ഷം',
    brahma:    'ബ്രഹ്മ മുഹൂർത്തം',
    abhijit:   'അഭിജിത് മുഹൂർത്തം',
    vijaya:    'വിജയ മുഹൂർത്തം',
    rahu:      'രാഹു കാലം',
    yama:      'യമഗണ്ഡം',
    gulika:    'ഗുളിക കാലം',
    dur:       'ദുർ മുഹൂർത്തം',
    now:       'ഇപ്പോൾ',
  },
  kannada: {
    sunrise:   'ಸೂರ್ಯೋದಯ',
    sunset:    'ಸೂರ್ಯಾಸ್ತ',
    moonrise:  'ಚಂದ್ರೋದಯ',
    moonset:   'ಚಂದ್ರಾಸ್ತ',
    tithi:     'ತಿಥಿ',
    nakshatra: 'ನಕ್ಷತ್ರ',
    yoga:      'ಯೋಗ',
    karana:    'ಕರಣ',
    vara:      'ವಾರ',
    paksha:    'ಪಕ್ಷ',
    month:     'ಮಾಸ',
    year:      'ಸಂವತ್ಸರ',
    samvat:    'ಸಂವತ್',
    rahukaal:  'ರಾಹು ಕಾಲ',
    auspicious:'ಶುಭ ಸಮಯ',
    inauspicious: 'ಅಶುಭ ಸಮಯ',
    timings:   'ಸಮಯ ವಿವರಗಳು',
    fiveLimbs: 'ಪಂಚಾಂಗ — ಪಂಚ ಅಂಗಗಳು',
    endsAt:    'ಮುಕ್ತಾಯ ಸಮಯ',
    sunIn:     'ಸೂರ್ಯ',
    moonIn:    'ಚಂದ್ರ',
    nakshatraOf: 'ನಕ್ಷತ್ರ',
    pakshaBadge: 'ಪಕ್ಷ',
    brahma:    'ಬ್ರಹ್ಮ ಮುಹೂರ್ತ',
    abhijit:   'ಅಭಿಜಿತ್ ಮುಹೂರ್ತ',
    vijaya:    'ವಿಜಯ ಮುಹೂರ್ತ',
    rahu:      'ರಾಹು ಕಾಲ',
    yama:      'ಯಮಗಂಡ',
    gulika:    'ಗುಳಿಕ ಕಾಲ',
    dur:       'ದುರ್ ಮುಹೂರ್ತ',
    now:       'ಈಗ',
  },
  hindi: {
    sunrise:   'सूर्योदय',
    sunset:    'सूर्यास्त',
    moonrise:  'चंद्रोदय',
    moonset:   'चंद्रास्त',
    tithi:     'तिथि',
    nakshatra: 'नक्षत्र',
    yoga:      'योग',
    karana:    'करण',
    vara:      'वार',
    paksha:    'पक्ष',
    month:     'माह',
    year:      'वर्ष',
    samvat:    'विक्रम संवत',
    rahukaal:  'राहु काल',
    auspicious:'शुभ मुहूर्त',
    inauspicious: 'अशुभ काल',
    timings:   'मुहूर्त विवरण',
    fiveLimbs: 'पंचांग — पंच अंग',
    endsAt:    'समाप्ति',
    sunIn:     'सूर्य',
    moonIn:    'चंद्र',
    nakshatraOf: 'नक्षत्र',
    pakshaBadge: 'पक्ष',
    brahma:    'ब्रह्म मुहूर्त',
    abhijit:   'अभिजित् मुहूर्त',
    vijaya:    'विजय मुहूर्त',
    rahu:      'राहु काल',
    yama:      'यमगण्ड',
    gulika:    'गुलिक काल',
    dur:       'दुर्मुहूर्त',
    now:       'अभी',
  },
};

// ─── Nakshatra name translations ─────────────────────────────────────────────
const NAKSHATRA_NAMES = {
  tamil: {
    Ashwini:'அஸ்வினி', Bharani:'பரணி', Krittika:'கார்த்திகை',
    Rohini:'ரோகிணி', Mrigashira:'மிருகசீரிஷம்', Ardra:'திருவாதிரை',
    Punarvasu:'புனர்பூசம்', Pushya:'பூசம்', Ashlesha:'ஆயில்யம்',
    Magha:'மகம்', PurvaPhalguni:'பூரம்', UttaraPhalguni:'உத்திரம்',
    Hasta:'அஸ்தம்', Chitra:'சித்திரை', Swati:'சுவாதி',
    Vishakha:'விசாகம்', Anuradha:'அனுஷம்', Jyeshtha:'கேட்டை',
    Mula:'மூலம்', PurvaAshadha:'பூராடம்', UttaraAshadha:'உத்திராடம்',
    Shravana:'திருவோணம்', Dhanishtha:'அவிட்டம்', Shatabhisha:'சதயம்',
    PurvaBhadrapada:'பூரட்டாதி', UttaraBhadrapada:'உத்திரட்டாதி', Revati:'ரேவதி',
  },
  telugu: {
    Ashwini:'అశ్విని', Bharani:'భరణి', Krittika:'కృత్తిక',
    Rohini:'రోహిణి', Mrigashira:'మృగశిర', Ardra:'ఆర్ద్ర',
    Punarvasu:'పునర్వసు', Pushya:'పుష్యమి', Ashlesha:'ఆశ్లేష',
    Magha:'మఘ', PurvaPhalguni:'పూర్వఫల్గుణి', UttaraPhalguni:'ఉత్తరఫల్గుణి',
    Hasta:'హస్త', Chitra:'చిత్ర', Swati:'స్వాతి',
    Vishakha:'విశాఖ', Anuradha:'అనూరాధ', Jyeshtha:'జ్యేష్ఠ',
    Mula:'మూల', PurvaAshadha:'పూర్వాషాఢ', UttaraAshadha:'ఉత్తరాషాఢ',
    Shravana:'శ్రవణ', Dhanishtha:'ధనిష్ఠ', Shatabhisha:'శతభిష',
    PurvaBhadrapada:'పూర్వభాద్ర', UttaraBhadrapada:'ఉత్తరభాద్ర', Revati:'రేవతి',
  },
  malayalam: {
    Ashwini:'അശ്വതി', Bharani:'ഭരണി', Krittika:'കാർത്തിക',
    Rohini:'രോഹിണി', Mrigashira:'മകയിരം', Ardra:'തിരുവാതിര',
    Punarvasu:'പുണർതം', Pushya:'പൂയം', Ashlesha:'ആയില്യം',
    Magha:'മകം', PurvaPhalguni:'പൂരം', UttaraPhalguni:'ഉത്രം',
    Hasta:'അത്തം', Chitra:'ചിത്തിര', Swati:'ചോതി',
    Vishakha:'വിശാഖം', Anuradha:'അനിഴം', Jyeshtha:'തൃക്കേട്ട',
    Mula:'മൂലം', PurvaAshadha:'പൂരാടം', UttaraAshadha:'ഉത്രാടം',
    Shravana:'തിരുവോണം', Dhanishtha:'അവിട്ടം', Shatabhisha:'ചതയം',
    PurvaBhadrapada:'പൂരുരുട്ടാതി', UttaraBhadrapada:'ഉത്രട്ടാതി', Revati:'രേവതി',
  },
  kannada: {
    Ashwini:'ಅಶ್ವಿನಿ', Bharani:'ಭರಣಿ', Krittika:'ಕೃತ್ತಿಕ',
    Rohini:'ರೋಹಿಣಿ', Mrigashira:'ಮೃಗಶಿರ', Ardra:'ಆರ್ದ್ರ',
    Punarvasu:'ಪುನರ್ವಸು', Pushya:'ಪುಷ್ಯ', Ashlesha:'ಆಶ್ಲೇಷ',
    Magha:'ಮಘ', PurvaPhalguni:'ಪೂರ್ವ ಫಲ್ಗುಣಿ', UttaraPhalguni:'ಉತ್ತರ ಫಲ್ಗುಣಿ',
    Hasta:'ಹಸ್ತ', Chitra:'ಚಿತ್ರ', Swati:'ಸ್ವಾತಿ',
    Vishakha:'ವಿಶಾಖ', Anuradha:'ಅನೂರಾಧ', Jyeshtha:'ಜ್ಯೇಷ್ಠ',
    Mula:'ಮೂಲ', PurvaAshadha:'ಪೂರ್ವಾಷಾಢ', UttaraAshadha:'ಉತ್ತರಾಷಾಢ',
    Shravana:'ಶ್ರವಣ', Dhanishtha:'ಧನಿಷ್ಠ', Shatabhisha:'ಶತಭಿಷ',
    PurvaBhadrapada:'ಪೂರ್ವಭಾದ್ರ', UttaraBhadrapada:'ಉತ್ತರಭಾದ್ರ', Revati:'ರೇವತಿ',
  },
  hindi: {
    Ashwini:'अश्विनी', Bharani:'भरणी', Krittika:'कृत्तिका',
    Rohini:'रोहिणी', Mrigashira:'मृगशिरा', Ardra:'आर्द्रा',
    Punarvasu:'पुनर्वसु', Pushya:'पुष्य', Ashlesha:'आश्लेषा',
    Magha:'मघा', PurvaPhalguni:'पूर्वफाल्गुनी', UttaraPhalguni:'उत्तरफाल्गुनी',
    Hasta:'हस्त', Chitra:'चित्रा', Swati:'स्वाती',
    Vishakha:'विशाखा', Anuradha:'अनुराधा', Jyeshtha:'ज्येष्ठा',
    Mula:'मूल', PurvaAshadha:'पूर्वाषाढ़', UttaraAshadha:'उत्तराषाढ़',
    Shravana:'श्रवण', Dhanishtha:'धनिष्ठा', Shatabhisha:'शतभिषा',
    PurvaBhadrapada:'पूर्वभाद्रपद', UttaraBhadrapada:'उत्तरभाद्रपद', Revati:'रेवती',
  },
};

// ─── Tithi translations ───────────────────────────────────────────────────────
const TITHI_NAMES = {
  tamil: {
    Pratipada:'பிரதமை', Dwitiya:'த்விதியை', Tritiya:'திருதியை',
    Chaturthi:'சதுர்த்தி', Panchami:'பஞ்சமி', Shashthi:'ஷஷ்டி',
    Saptami:'சப்தமி', Ashtami:'அஷ்டமி', Navami:'நவமி',
    Dashami:'தசமி', Ekadashi:'ஏகாதசி', Dwadashi:'த்வாதசி',
    Trayodashi:'திரயோதசி', Chaturdashi:'சதுர்தசி',
    Purnima:'பூர்ணிமை', Amavasya:'அமாவாசை',
  },
  telugu: {
    Pratipada:'పాడ్యమి', Dwitiya:'విదియ', Tritiya:'తదియ',
    Chaturthi:'చవితి', Panchami:'పంచమి', Shashthi:'షష్టి',
    Saptami:'సప్తమి', Ashtami:'అష్టమి', Navami:'నవమి',
    Dashami:'దశమి', Ekadashi:'ఏకాదశి', Dwadashi:'ద్వాదశి',
    Trayodashi:'త్రయోదశి', Chaturdashi:'చతుర్దశి',
    Purnima:'పౌర్ణమి', Amavasya:'అమావాస్య',
  },
  malayalam: {
    Pratipada:'പ്രതിപദ', Dwitiya:'ദ്വിതീയ', Tritiya:'തൃതീയ',
    Chaturthi:'ചതുർഥി', Panchami:'പഞ്ചമി', Shashthi:'ഷഷ്ഠി',
    Saptami:'സപ്തമി', Ashtami:'അഷ്ടമി', Navami:'നവമി',
    Dashami:'ദശമി', Ekadashi:'ഏകാദശി', Dwadashi:'ദ്വാദശി',
    Trayodashi:'ത്രയോദശി', Chaturdashi:'ചതുർദശി',
    Purnima:'പൗർണ്ണമി', Amavasya:'അമാവാസ്യ',
  },
  kannada: {
    Pratipada:'ಪಾಡ್ಯ', Dwitiya:'ಬಿದಿಗೆ', Tritiya:'ತದಿಗೆ',
    Chaturthi:'ಚೌತಿ', Panchami:'ಪಂಚಮಿ', Shashthi:'ಷಷ್ಠಿ',
    Saptami:'ಸಪ್ತಮಿ', Ashtami:'ಅಷ್ಟಮಿ', Navami:'ನವಮಿ',
    Dashami:'ದಶಮಿ', Ekadashi:'ಏಕಾದಶಿ', Dwadashi:'ದ್ವಾದಶಿ',
    Trayodashi:'ತ್ರಯೋದಶಿ', Chaturdashi:'ಚತುರ್ದಶಿ',
    Purnima:'ಹುಣ್ಣಿಮೆ', Amavasya:'ಅಮಾವಾಸ್ಯೆ',
  },
  hindi: {
    Pratipada:'प्रतिपदा', Dwitiya:'द्वितीया', Tritiya:'तृतीया',
    Chaturthi:'चतुर्थी', Panchami:'पंचमी', Shashthi:'षष्ठी',
    Saptami:'सप्तमी', Ashtami:'अष्टमी', Navami:'नवमी',
    Dashami:'दशमी', Ekadashi:'एकादशी', Dwadashi:'द्वादशी',
    Trayodashi:'त्रयोदशी', Chaturdashi:'चतुर्दशी',
    Purnima:'पूर्णिमा', Amavasya:'अमावस्या',
  },
};

// Weekday translations
const WEEKDAY_NAMES = {
  tamil:    ['ஞாயிறு','திங்கள்','செவ்வாய்','புதன்','வியாழன்','வெள்ளி','சனி'],
  telugu:   ['ఆదివారం','సోమవారం','మంగళవారం','బుధవారం','గురువారం','శుక్రవారం','శనివారం'],
  malayalam:['ഞായർ','തിങ്കൾ','ചൊവ്വ','ബുധൻ','വ്യാഴം','വെള്ളി','ശനി'],
  kannada:  ['ಭಾನುವಾರ','ಸೋಮವಾರ','ಮಂಗಳವಾರ','ಬುಧವಾರ','ಗುರುವಾರ','ಶುಕ್ರವಾರ','ಶನಿವಾರ'],
  hindi:    ['रविवार','सोमवार','मंगलवार','बुधवार','गुरुवार','शुक्रवार','शनिवार'],
};

// Paksha translations
const PAKSHA_NAMES = {
  tamil:    { Shukla: 'சுக்ல பக்ஷம்', Krishna: 'கிருஷ்ண பக்ஷம்' },
  telugu:   { Shukla: 'శుక్ల పక్షం', Krishna: 'కృష్ణ పక్షం' },
  malayalam:{ Shukla: 'വെളുത്ത പക്ഷം', Krishna: 'കറുത്ത പക്ഷം' },
  kannada:  { Shukla: 'ಶುಕ್ಲ ಪಕ್ಷ', Krishna: 'ಕೃಷ್ಣ ಪಕ್ಷ' },
  hindi:    { Shukla: 'शुक्ल पक्ष', Krishna: 'कृष्ण पक्ष' },
};

// Timing window label translations (maps English labels → regional)
const WINDOW_LABEL_MAP = {
  tamil: {
    'Brahma Muhurta':  'பிரம்ம முகூர்த்தம்',
    'Abhijit Muhurta': 'அபிஜித் முகூர்த்தம்',
    'Vijaya Muhurta':  'விஜய முகூர்த்தம்',
    'Rahu Kaal':       'ராகு காலம்',
    'Yamaganda':       'யமகண்டம்',
    'Gulika Kaal':     'குளிக காலம்',
    'Dur Muhurta':     'துர் முகூர்த்தம்',
  },
  telugu: {
    'Brahma Muhurta':  'బ్రహ్మ ముహూర్తం',
    'Abhijit Muhurta': 'అభిజిత్ ముహూర్తం',
    'Vijaya Muhurta':  'విజయ ముహూర్తం',
    'Rahu Kaal':       'రాహు కాలం',
    'Yamaganda':       'యమగండం',
    'Gulika Kaal':     'గులిక కాలం',
    'Dur Muhurta':     'దుర్ ముహూర్తం',
  },
  malayalam: {
    'Brahma Muhurta':  'ബ്രഹ്മ മുഹൂർത്തം',
    'Abhijit Muhurta': 'അഭിജിത് മുഹൂർത്തം',
    'Vijaya Muhurta':  'വിജയ മുഹൂർത്തം',
    'Rahu Kaal':       'രാഹു കാലം',
    'Yamaganda':       'യമഗണ്ഡം',
    'Gulika Kaal':     'ഗുളിക കാലം',
    'Dur Muhurta':     'ദുർ മുഹൂർത്തം',
  },
  kannada: {
    'Brahma Muhurta':  'ಬ್ರಹ್ಮ ಮುಹೂರ್ತ',
    'Abhijit Muhurta': 'ಅಭಿಜಿತ್ ಮುಹೂರ್ತ',
    'Vijaya Muhurta':  'ವಿಜಯ ಮುಹೂರ್ತ',
    'Rahu Kaal':       'ರಾಹು ಕಾಲ',
    'Yamaganda':       'ಯಮಗಂಡ',
    'Gulika Kaal':     'ಗುಳಿಕ ಕಾಲ',
    'Dur Muhurta':     'ದುರ್ ಮುಹೂರ್ತ',
  },
  hindi: {
    'Brahma Muhurta':  'ब्रह्म मुहूर्त',
    'Abhijit Muhurta': 'अभिजित् मुहूर्त',
    'Vijaya Muhurta':  'विजय मुहूर्त',
    'Rahu Kaal':       'राहु काल',
    'Yamaganda':       'यमगण्ड',
    'Gulika Kaal':     'गुलिक काल',
    'Dur Muhurta':     'दुर्मुहूर्त',
  },
};

// ─── Timezone helper ──────────────────────────────────────────────────────────
const TZ_OVERRIDE = {
  'Asia/Kolkata': 'IST', 'Asia/Kathmandu': 'NPT', 'Asia/Dubai': 'GST',
  'Asia/Singapore': 'SGT', 'Asia/Kuala_Lumpur': 'MYT', 'Asia/Jakarta': 'WIB',
  'Asia/Bangkok': 'ICT', 'Pacific/Auckland': 'NZST', 'Australia/Brisbane': 'AEST',
  'Australia/Sydney': 'AEDT', 'America/Toronto': 'EST', 'America/Vancouver': 'PST',
};
function getTZAbbr(tz) {
  if (!tz) return 'IST';
  if (TZ_OVERRIDE[tz]) return TZ_OVERRIDE[tz];
  try {
    const parts = new Intl.DateTimeFormat('en-US', { timeZone: tz, timeZoneName: 'short' }).formatToParts(new Date());
    return parts.find(p => p.type === 'timeZoneName')?.value || tz.split('/').pop();
  } catch { return 'IST'; }
}

function makeFormatTime(tz) {
  return (iso) => {
    if (!iso) return '--';
    try {
      return new Date(iso).toLocaleTimeString('en-IN', {
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: true, timeZone: tz || 'Asia/Kolkata',
      });
    } catch { return iso.slice(11, 19); }
  };
}

function getTodayIST() {
  try {
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Kolkata', year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(new Date());
    const m = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${m.year}-${m.month}-${m.day}`;
  } catch {
    return new Date().toISOString().slice(0, 10);
  }
}

// Translate a nakshatra name
function translateNakshatra(name, lang) {
  if (!name) return name;
  const map = NAKSHATRA_NAMES[lang] || {};
  // Try direct match
  if (map[name]) return map[name];
  // Try trimming and matching
  const trimmed = name.trim();
  if (map[trimmed]) return map[trimmed];
  return name; // fallback to English
}

function translateTithi(name, lang) {
  if (!name) return name;
  const map = TITHI_NAMES[lang] || {};
  if (map[name]) return map[name];
  return name;
}

function translateWindow(label, lang) {
  const map = WINDOW_LABEL_MAP[lang] || {};
  // Partial match for Dur Muhurta (can be "Dur Muhurta 1" etc.)
  if (label.startsWith('Dur Muhurta') || label.startsWith('Dur Muhurat')) {
    return map['Dur Muhurta'] || label;
  }
  return map[label] || label;
}

function getLocalWeekday(lang) {
  const names = WEEKDAY_NAMES[lang];
  if (!names) return '';
  return names[new Date().getDay()];
}

// ─── Location Picker (shared component reuse) ────────────────────────────────
function LocationPicker({ selectedSlug, onSelect }) {
  const [locations, setLocations] = useState([]);
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef(null);

  useEffect(() => { axios.get(`${API}/locations`).then(r => setLocations(r.data)).catch(() => {}); }, []);

  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const selected = locations.find(l => l.slug === selectedSlug);
  const tzAbbr = selected ? getTZAbbr(selected.timezone) : 'IST';
  const filtered = search.trim()
    ? locations.filter(l => l.label.toLowerCase().includes(search.toLowerCase()) || l.country.toLowerCase().includes(search.toLowerCase()))
    : locations;
  const countries = [...new Set(locations.map(l => l.country))];
  const grouped = countries.reduce((acc, c) => { const locs = filtered.filter(l => l.country === c); if (locs.length) acc[c] = locs; return acc; }, {});

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-gold/30 bg-gold/5 text-xs font-semibold text-gold hover:bg-gold/10 transition-colors"
      >
        <MapPin className="h-3 w-3 flex-shrink-0" />
        <span>{selected ? `${selected.label}, ${selected.country}` : 'Select location'}</span>
        <span className="px-1.5 py-0.5 rounded bg-gold/20 text-[10px] font-bold">{tzAbbr}</span>
        <ChevronDown className={`h-3 w-3 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <div className="absolute right-0 top-full mt-2 w-80 max-h-80 overflow-hidden rounded-xl border border-border bg-background shadow-xl z-50 flex flex-col">
          <div className="p-2 border-b border-border">
            <input autoFocus value={search} onChange={e => setSearch(e.target.value)}
              placeholder="Search city or country…"
              className="w-full px-3 py-1.5 text-xs rounded-lg border border-border bg-muted/30 focus:outline-none focus:border-gold/50" />
          </div>
          <div className="overflow-y-auto flex-1">
            {Object.entries(grouped).map(([country, locs]) => (
              <div key={country}>
                <div className="flex items-center gap-1.5 px-3 py-1.5 bg-muted/30 sticky top-0">
                  <Globe className="h-3 w-3 text-muted-foreground" />
                  <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">{country}</p>
                </div>
                {locs.map(loc => {
                  const la = getTZAbbr(loc.timezone);
                  const isSel = loc.slug === selectedSlug;
                  return (
                    <button key={loc.slug} onClick={() => { onSelect(loc.slug); setOpen(false); setSearch(''); }}
                      className={`w-full text-left px-4 py-2.5 text-xs hover:bg-gold/10 transition-colors flex items-center justify-between gap-3 ${isSel ? 'text-gold font-semibold bg-gold/5' : 'text-foreground'}`}>
                      <span className="flex-1">{loc.label}</span>
                      <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold flex-shrink-0 ${isSel ? 'bg-gold/30 text-gold' : 'bg-muted text-muted-foreground'}`}>{la}</span>
                      {isSel && <span className="text-gold flex-shrink-0">✓</span>}
                    </button>
                  );
                })}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────
export function PanchangLangPage({ lang }) {
  const meta   = LANG_META[lang];
  const labels = LABELS[lang];
  const navigate = useNavigate();
  const location = useLocation();

  const [locationSlug, setLocationSlug] = useState(() => localStorage.getItem(LOC_KEY) || DEFAULT);
  const [data, setData]     = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState(null);

  const handleSelect = useCallback((slug) => {
    setLocationSlug(slug);
    localStorage.setItem(LOC_KEY, slug);
  }, []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    const date = getTodayIST();
    axios.get(`${API}/daily`, { params: { date, location_slug: locationSlug } })
      .then(r => { if (!cancelled) { setData(r.data); setLoading(false); } })
      .catch(e => { if (!cancelled) { setError(e.message || 'Failed to load'); setLoading(false); } });
    return () => { cancelled = true; };
  }, [locationSlug]);

  if (!meta) return null;

  // ── Derived values ──
  const p      = data?.panchang || {};
  const sum    = data?.summary  || {};
  const locs   = data?.location || {};
  const tz     = locs.timezone || 'Asia/Kolkata';
  const tzAbbr = getTZAbbr(tz);
  const fmt    = makeFormatTime(tz);
  const today  = getTodayIST();
  const [y, mo, d] = today.split('-');
  const dateStr = `${parseInt(d)} ${new Date(`${today}T12:00:00Z`).toLocaleDateString('en-IN', { month: 'long', year: 'numeric', timeZone: tz })}`;

  const nakshatra   = translateNakshatra(p.nakshatra?.name, lang);
  const tithi       = translateTithi(p.tithi?.name, lang);
  const weekday     = getLocalWeekday(lang);
  const paksha      = PAKSHA_NAMES[lang]?.[p.paksha] || p.paksha;

  const windows     = data?.timing_windows || [];
  const auspicious  = windows.filter(w => w.quality === 'good');
  const inauspicious = windows.filter(w => w.quality !== 'good');

  const seoTitle    = `${meta.seoTitle} — ${dateStr} | Everyday Horoscope`;

  // Language switcher links (for hreflang + user convenience)
  const langSwitcher = [
    { lang: 'en', label: 'English', path: '/panchang/today' },
    { lang: 'hi', label: 'हिंदी',   path: '/panchang/hindi' },
    { lang: 'ta', label: 'தமிழ்',   path: '/panchang/tamil' },
    { lang: 'te', label: 'తెలుగు',  path: '/panchang/telugu' },
    { lang: 'ml', label: 'മലയാളം', path: '/panchang/malayalam' },
    { lang: 'kn', label: 'ಕನ್ನಡ',   path: '/panchang/kannada' },
  ];

  return (
    <>
      <SEO
        title={seoTitle}
        description={meta.seoDesc}
        canonical={`${SITE}/panchang/${lang}`}
        lang={meta.code}
      />

      <div className="max-w-2xl mx-auto px-4 pb-10 pt-4 space-y-5">

        {/* ── Hero Header ── */}
        <div className="text-center space-y-1 py-4">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold/70">
            {meta.nativeName} · {dateStr}
          </p>
          <h1 className="font-playfair text-3xl font-bold">
            {meta.h1Prefix}
          </h1>
          <p className="text-sm text-muted-foreground">{weekday}</p>
        </div>

        {/* ── Language Switcher ── */}
        <div className="flex flex-wrap items-center justify-center gap-2">
          {langSwitcher.map(l => (
            <button
              key={l.lang}
              onClick={() => navigate(l.path)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                l.lang === meta.code
                  ? 'border-gold text-gold bg-gold/10 font-semibold'
                  : 'border-border text-muted-foreground hover:text-foreground hover:border-gold/40'
              }`}
            >
              {l.label}
            </button>
          ))}
        </div>

        {/* ── Location Picker ── */}
        <div className="flex justify-end">
          <LocationPicker selectedSlug={locationSlug} onSelect={handleSelect} />
        </div>

        {/* ── Loading / Error ── */}
        {loading && (
          <div className="space-y-3">
            {[1,2,3,4].map(i => <div key={i} className="h-24 rounded-xl bg-muted/30 animate-pulse" />)}
          </div>
        )}
        {error && !loading && (
          <Card className="p-6 text-center border-red-200">
            <p className="text-sm text-red-500">⚠ {error}</p>
            <button onClick={() => setLocationSlug(locationSlug)} className="mt-2 text-xs text-gold underline">Retry</button>
          </Card>
        )}

        {data && !loading && (
          <>
            {/* ── Sun & Moon 2×2 ── */}
            <div className="grid grid-cols-2 gap-3">
              {[
                { icon: <Sun className="h-5 w-5 text-amber-500 mx-auto mb-1" />,   label: labels.sunrise,  value: sum.sunrise  || '--', sub: p.sun_sign  ? `${labels.sunIn}: ${p.sun_sign}`  : '' },
                { icon: <Sun className="h-5 w-5 text-orange-400 mx-auto mb-1" />,  label: labels.sunset,   value: sum.sunset   || '--', sub: p.moon_sign ? `${labels.moonIn}: ${p.moon_sign}` : '' },
                { icon: <Moon className="h-5 w-5 text-blue-300 mx-auto mb-1" />,   label: labels.moonrise, value: sum.moonrise || '--', sub: nakshatra ? `${nakshatra} ${labels.nakshatraOf}` : '' },
                { icon: <Moon className="h-5 w-5 text-indigo-400 mx-auto mb-1" />, label: labels.moonset,  value: sum.moonset  || '--', sub: paksha || '' },
              ].map(c => (
                <Card key={c.label} className="p-4 border border-gold/20 text-center">
                  {c.icon}
                  <p className="text-xs text-muted-foreground mt-0.5">{c.label}</p>
                  <p className="font-semibold text-base tabular-nums">{c.value}</p>
                  {c.sub && <p className="text-xs text-muted-foreground mt-0.5 truncate">{c.sub}</p>}
                  <p className="text-[10px] text-gold/70 font-bold mt-0.5">{tzAbbr}</p>
                </Card>
              ))}
            </div>

            {/* ── Five Limbs Card ── */}
            <Card className="border border-gold/20 overflow-hidden">
              <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
                <p className="text-xs font-semibold uppercase tracking-widest text-gold">{labels.fiveLimbs}</p>
              </div>
              <div className="divide-y divide-border">
                {[
                  { key: 'tithi',     label: labels.tithi,     value: tithi,                  end: p.tithi?.end_time },
                  { key: 'nakshatra', label: labels.nakshatra, value: nakshatra,               end: p.nakshatra?.end_time },
                  { key: 'yoga',      label: labels.yoga,       value: p.yoga?.name,            end: p.yoga?.end_time },
                  { key: 'karana',    label: labels.karana,     value: p.karana?.name,          end: p.karana?.end_time },
                  { key: 'vara',      label: labels.vara,       value: weekday,                 end: null },
                ].map(row => (
                  <div key={row.key} className="flex items-center justify-between px-5 py-3">
                    <div>
                      <p className="text-[11px] text-gold/70 uppercase tracking-wide font-medium">{row.label}</p>
                      <p className="font-semibold text-sm mt-0.5">{row.value || '--'}</p>
                    </div>
                    {row.end && (
                      <div className="text-right">
                        <p className="text-[10px] text-muted-foreground">{labels.endsAt}</p>
                        <p className="text-xs tabular-nums font-medium">{fmt(row.end)}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </Card>

            {/* ── Calendar Metadata ── */}
            {(p.lunar_month || p.samvat || p.paksha) && (
              <Card className="border border-gold/20 overflow-hidden">
                <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
                  <p className="text-xs font-semibold uppercase tracking-widest text-gold">{labels.samvat}</p>
                </div>
                <div className="grid grid-cols-3 divide-x divide-border">
                  {[
                    { label: labels.month,  value: p.lunar_month || '--' },
                    { label: labels.paksha, value: paksha || '--' },
                    { label: labels.samvat, value: p.samvat ? `${p.samvat}` : '--' },
                  ].map(item => (
                    <div key={item.label} className="px-4 py-3 text-center">
                      <p className="text-[10px] text-muted-foreground uppercase tracking-wide">{item.label}</p>
                      <p className="font-semibold text-sm mt-1">{item.value}</p>
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* ── Timing Windows ── */}
            {windows.length > 0 && (
              <Card className="border border-gold/20 overflow-hidden">
                <div className="px-5 py-3 bg-gold/5 border-b border-gold/20 flex items-center justify-between">
                  <p className="text-xs font-semibold uppercase tracking-widest text-gold">{labels.timings}</p>
                  <span className="text-[10px] text-muted-foreground font-semibold">{tzAbbr}</span>
                </div>

                {auspicious.length > 0 && (
                  <>
                    <div className="flex items-center gap-2 px-5 py-2 bg-green-50 border-b border-green-100">
                      <span className="text-green-600 text-sm">✦</span>
                      <p className="text-[11px] font-bold uppercase tracking-widest text-green-700">{labels.auspicious}</p>
                    </div>
                    <div className="divide-y divide-border">
                      {auspicious.map(w => {
                        const now = new Date();
                        const isCurrent = now >= new Date(w.start) && now <= new Date(w.end);
                        return (
                          <div key={w.label} className={`flex items-center justify-between px-5 py-3 ${isCurrent ? 'bg-gold/5' : ''}`}>
                            <div className="flex items-center gap-3">
                              {isCurrent && <span className="w-2 h-2 rounded-full bg-green-500 flex-shrink-0" />}
                              <span className="text-sm font-medium">{translateWindow(w.label, lang)}</span>
                              {isCurrent && <span className="text-xs text-green-600 font-semibold">{labels.now}</span>}
                            </div>
                            <span className="text-xs text-muted-foreground tabular-nums">{fmt(w.start)} — {fmt(w.end)}</span>
                          </div>
                        );
                      })}
                    </div>
                  </>
                )}

                {inauspicious.length > 0 && (
                  <>
                    <div className="flex items-center gap-2 px-5 py-2 bg-red-50 border-y border-red-100">
                      <span className="text-red-500 text-sm">⚠</span>
                      <p className="text-[11px] font-bold uppercase tracking-widest text-red-700">{labels.inauspicious}</p>
                    </div>
                    <div className="divide-y divide-border">
                      {inauspicious.map(w => {
                        const now = new Date();
                        const isCurrent = now >= new Date(w.start) && now <= new Date(w.end);
                        return (
                          <div key={w.label} className={`flex items-center justify-between px-5 py-3 ${isCurrent ? 'bg-red-50/50' : ''}`}>
                            <div className="flex items-center gap-3">
                              {isCurrent && <span className="w-2 h-2 rounded-full bg-red-500 flex-shrink-0" />}
                              <span className="text-sm font-medium">{translateWindow(w.label, lang)}</span>
                              {isCurrent && <span className="text-xs text-red-600 font-semibold">{labels.now}</span>}
                            </div>
                            <span className="text-xs text-muted-foreground tabular-nums">{fmt(w.start)} — {fmt(w.end)}</span>
                          </div>
                        );
                      })}
                    </div>
                  </>
                )}
              </Card>
            )}

            {/* ── SEO Content Block ── */}
            <div className="rounded-xl border border-gold/10 bg-gold/3 p-5 space-y-3 text-sm text-muted-foreground">
              <h2 className="font-playfair text-base font-semibold text-foreground">
                {meta.h1Prefix} — {dateStr}
              </h2>
              <p>
                {lang === 'tamil' && 'இன்றைய பஞ்சாங்கம் நமது வேத ஜோதிட கணக்கீட்டின் படி சூரிய உதயம், திதி, நட்சத்திரம், யோகம், கரணம் மற்றும் ராகு காலம் ஆகியவற்றை வழங்குகிறது.'}
                {lang === 'telugu' && 'నేటి పంచాంగం మన వేద జ్యోతిష్య గణన ప్రకారం సూర్యోదయం, తిథి, నక్షత్రం, యోగం, కరణం మరియు రాహు కాలం అందిస్తుంది.'}
                {lang === 'malayalam' && 'ഇന്നത്തെ പഞ്ചാംഗം നമ്മുടെ വേദ ജ്യോതിഷ കണക്കുകൂട്ടൽ പ്രകാരം സൂര്യോദയം, തിഥി, നക്ഷത്രം, യോഗം, കരണം, രാഹു കാലം എന്നിവ നൽകുന്നു.'}
                {lang === 'kannada' && 'ಇಂದಿನ ಪಂಚಾಂಗ ನಮ್ಮ ವೇದ ಜ್ಯೋತಿಷ ಲೆಕ್ಕಾಚಾರದ ಪ್ರಕಾರ ಸೂರ್ಯೋದಯ, ತಿಥಿ, ನಕ್ಷತ್ರ, ಯೋಗ, ಕರಣ ಮತ್ತು ರಾಹು ಕಾಲ ನೀಡುತ್ತದೆ.'}
                {lang === 'hindi' && 'आज का पंचांग हमारी वैदिक ज्योतिष गणना के अनुसार सूर्योदय, तिथि, नक्षत्र, योग, करण और राहु काल प्रदान करता है।'}
              </p>
              <p className="text-xs text-gold/60">
                Powered by Swiss Ephemeris · Lahiri Ayanamsa · Everyday Horoscope
              </p>
            </div>
          </>
        )}
      </div>
    </>
  );
}

export default PanchangLangPage;
