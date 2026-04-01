import React from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";

import {
  SUPPORTED_PANCHANG_LANGUAGES,
  buildPanchangPath,
  getPanchangCopy,
  getPanchangLanguage,
} from "./panchangLocale";

function buildLanguageDestination(pathname, nextLanguage, currentLanguage) {
  const currentPrefix = `/${currentLanguage}/panchang`;
  if (pathname.startsWith(currentPrefix)) {
    return pathname.replace(currentPrefix, `/${nextLanguage}/panchang`);
  }
  if (pathname.startsWith("/panchang")) {
    return pathname.replace("/panchang", `/${nextLanguage}/panchang`);
  }
  return buildPanchangPath(nextLanguage);
}

function PanchangLanguageToggle() {
  const navigate = useNavigate();
  const location = useLocation();
  const { lang } = useParams();
  const currentLanguage = getPanchangLanguage(lang);
  const copy = getPanchangCopy(currentLanguage);

  return (
    <div className="panchang-language-toggle">
      <label htmlFor="panchang-language-select">{copy.languageLabel}</label>
      <select
        id="panchang-language-select"
        value={currentLanguage}
        onChange={(event) => {
          const nextPath = buildLanguageDestination(location.pathname, event.target.value, currentLanguage);
          navigate(`${nextPath}${location.search}`);
        }}
      >
        {SUPPORTED_PANCHANG_LANGUAGES.map((language) => (
          <option key={language.code} value={language.code}>
            {language.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export default PanchangLanguageToggle;
