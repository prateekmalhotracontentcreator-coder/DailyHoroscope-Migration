from __future__ import annotations

import io
import os
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any

import anthropic
import httpx
import textstat
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")
WORD_RE = re.compile(r"\b[\w'-]+\b")
META_TITLE_RE = re.compile(r"\[META_TITLE:(.*?)\]", re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(r"\[META_DESC:(.*?)\]", re.IGNORECASE | re.DOTALL)
FALLBACK_META_SENTENCE_RE = re.compile(r"[.!?]\s+")

HUMANISE_SYSTEM_PROMPT = """
You are E.C.H.O. // P.A.C.E., an internal editorial engine for SEO landing pages.

Rewrite the draft so it sounds human, warm, specific, and confident.
Requirements:
- Preserve the factual meaning.
- Preserve every required SEO keyword verbatim when it can fit naturally.
- Remove robotic filler and generic AI transition phrases.
- Use varied sentence length and natural burstiness.
- Do not mention plagiarism, AI, prompts, or optimisation instructions.
- Do not use bullet lists unless the source text already clearly needs them.
- Produce a meta title under 60 characters.
- Produce a meta description under 155 characters.

Return the final answer in this exact format:
<rewritten content>
[META_TITLE: ...]
[META_DESC: ...]
""".strip()


@dataclass
class HumaniseResult:
    content: str
    meta_title: str
    meta_desc: str


class EchoPaceEngine:
    def __init__(self, serper_api_key: str, anthropic_api_key: str | None = None) -> None:
        self.serper_api_key = (serper_api_key or "").strip()
        self.anthropic_api_key = (anthropic_api_key or os.getenv("ANTHROPIC_API_KEY") or "").strip()
        self._anthropic_client: anthropic.Anthropic | None = None
        self._anthropic_models = [
            os.getenv("ECHO_PACE_ANTHROPIC_MODEL", "").strip(),
            "claude-opus-4-5",
            "claude-sonnet-4-5",
            "claude-3-5-sonnet-latest",
        ]

    def validate_copyright(self, text: str, threshold: float = 0.20) -> dict[str, Any]:
        phrases = self._candidate_phrases(text)
        if not phrases:
            return {
                "is_safe": True,
                "similarity_score": 0.0,
                "matched_sources": [],
                "scanned_sentences": 0,
            }

        if not self.serper_api_key:
            raise RuntimeError("SERPER_API_KEY is not configured")

        matched_sources: list[dict[str, str]] = []
        matched_words = 0
        total_words = sum(self._word_count(phrase) for phrase in phrases)

        with httpx.Client(timeout=15.0) as client:
            for phrase in phrases:
                payload = {"q": f"\"{phrase}\"", "num": 3}
                response = client.post(
                    "https://google.serper.dev/search",
                    headers={
                        "X-API-KEY": self.serper_api_key,
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                response.raise_for_status()
                organic = (response.json() or {}).get("organic") or []
                if not organic:
                    continue

                best_hit = self._best_serper_hit(phrase, organic)
                if best_hit is None:
                    continue

                matched_sources.append(
                    {
                        "phrase": phrase,
                        "title": str(best_hit.get("title") or "").strip(),
                        "url": str(best_hit.get("link") or "").strip(),
                    }
                )
                matched_words += self._word_count(phrase)

        similarity_score = round((matched_words / total_words), 4) if total_words else 0.0
        return {
            "is_safe": similarity_score < threshold,
            "similarity_score": similarity_score,
            "matched_sources": matched_sources,
            "scanned_sentences": len(phrases),
        }

    def humanise_and_optimise(self, text: str, seo_keywords: list[str]) -> dict[str, str]:
        if not self.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not configured")

        keyword_block = "\n".join(f"- {keyword}" for keyword in seo_keywords) or "- None supplied"
        prompt = (
            "Rewrite the SEO draft below for publication.\n\n"
            "Required SEO keywords to preserve exactly when natural:\n"
            f"{keyword_block}\n\n"
            "Draft:\n"
            f"{text.strip()}"
        )
        result = self._run_humanise_prompt(prompt)
        missing = self._missing_keywords(result.content, seo_keywords)

        if missing:
            repair_prompt = (
                "Revise the content below with the lightest possible touch.\n"
                "Keep the tone and structure, but make sure these missing SEO keywords appear verbatim and naturally:\n"
                f"{chr(10).join(f'- {keyword}' for keyword in missing)}\n\n"
                "Current version:\n"
                f"{result.content}"
            )
            repaired = self._run_humanise_prompt(repair_prompt)
            if len(self._missing_keywords(repaired.content, seo_keywords)) <= len(missing):
                result = repaired

        return {
            "content": result.content,
            "meta_title": self._fit_meta(result.meta_title, 60),
            "meta_desc": self._fit_meta(result.meta_desc, 155),
        }

    def calculate_metrics(self, text: str) -> dict[str, float | int]:
        words = WORD_RE.findall(text or "")
        unique_words = {word.lower() for word in words}
        word_count = len(words)
        lexical_diversity = round((len(unique_words) / word_count), 4) if word_count else 0.0
        return {
            "flesch_reading_ease": round(float(textstat.flesch_reading_ease(text or "")), 2),
            "reading_grade_level": round(float(textstat.flesch_kincaid_grade(text or "")), 2),
            "lexical_diversity": lexical_diversity,
            "word_count": word_count,
        }

    def process(self, raw_text: str, seo_keywords: list[str], threshold: float = 0.20) -> dict[str, Any]:
        cleaned_text = (raw_text or "").strip()
        if not cleaned_text:
            raise ValueError("Raw text is required")

        normalised_keywords = self._normalise_keywords(seo_keywords)
        input_metrics = self.calculate_metrics(cleaned_text)
        validation = self.validate_copyright(cleaned_text, threshold=threshold)
        humanised = self.humanise_and_optimise(cleaned_text, normalised_keywords)
        output_metrics = self.calculate_metrics(humanised["content"])
        missing_keywords = self._missing_keywords(humanised["content"], normalised_keywords)

        return {
            "copyright_passed": validation["is_safe"],
            "similarity_score": validation["similarity_score"],
            "matched_sources": validation["matched_sources"],
            "humanised_content": humanised["content"],
            "meta_title": humanised["meta_title"],
            "meta_desc": humanised["meta_desc"],
            "input_metrics": input_metrics,
            "output_metrics": output_metrics,
            "keyword_check": "Pass" if not missing_keywords else f"Fail (Missing: {missing_keywords})",
            "missing_keywords": missing_keywords,
            "scanned_sentences": validation["scanned_sentences"],
        }

    def build_pdf_report(self, report: dict[str, Any]) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.6 * inch,
            leftMargin=0.6 * inch,
            topMargin=0.6 * inch,
            bottomMargin=0.6 * inch,
        )
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="EchoHeading",
                parent=styles["Heading2"],
                textColor=colors.HexColor("#8b5cf6"),
                spaceAfter=8,
            )
        )
        styles.add(
            ParagraphStyle(
                name="EchoBody",
                parent=styles["BodyText"],
                leading=16,
                spaceAfter=8,
            )
        )

        story: list[Any] = [
            Paragraph("E.C.H.O. // P.A.C.E. Report", styles["Title"]),
            Spacer(1, 8),
            Paragraph("Editorial validation, humanisation, and SEO output summary.", styles["EchoBody"]),
            Spacer(1, 8),
        ]

        summary_rows = [
            ["Copyright Check", "Passed" if report.get("copyright_passed") else "Risk Detected"],
            ["Similarity Score", f"{float(report.get('similarity_score', 0)) * 100:.1f}%"],
            ["Keyword Check", str(report.get("keyword_check") or "-")],
            ["Meta Title", self._escape_pdf_text(str(report.get("meta_title") or "-"))],
            ["Meta Description", self._escape_pdf_text(str(report.get("meta_desc") or "-"))],
        ]
        summary_table = Table(summary_rows, colWidths=[140, 340])
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ede9fe")),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f5f3ff")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#c4b5fd")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#ddd6fe")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(summary_table)
        story.append(Spacer(1, 14))

        input_metrics = report.get("input_metrics") or {}
        output_metrics = report.get("output_metrics") or {}
        metrics_rows = [
            ["Metric", "Original", "Optimised"],
            ["Word Count", str(input_metrics.get("word_count", "-")), str(output_metrics.get("word_count", "-"))],
            ["Flesch Reading Ease", str(input_metrics.get("flesch_reading_ease", "-")), str(output_metrics.get("flesch_reading_ease", "-"))],
            ["Reading Grade", str(input_metrics.get("reading_grade_level", "-")), str(output_metrics.get("reading_grade_level", "-"))],
            ["Lexical Diversity", str(input_metrics.get("lexical_diversity", "-")), str(output_metrics.get("lexical_diversity", "-"))],
        ]
        story.append(Paragraph("Metrics", styles["EchoHeading"]))
        metrics_table = Table(metrics_rows, colWidths=[160, 160, 160])
        metrics_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(metrics_table)
        story.append(Spacer(1, 14))

        matched_sources = report.get("matched_sources") or []
        story.append(Paragraph("Matched Sources", styles["EchoHeading"]))
        if matched_sources:
            for index, source in enumerate(matched_sources, start=1):
                phrase = self._escape_pdf_text(str(source.get("phrase") or ""))
                title = self._escape_pdf_text(str(source.get("title") or ""))
                url = self._escape_pdf_text(str(source.get("url") or ""))
                story.append(Paragraph(f"{index}. <b>{title or 'Matched Source'}</b>", styles["EchoBody"]))
                story.append(Paragraph(f"Phrase: {phrase}", styles["EchoBody"]))
                story.append(Paragraph(f"URL: {url}", styles["EchoBody"]))
        else:
            story.append(Paragraph("No matched sources were returned.", styles["EchoBody"]))
        story.append(Spacer(1, 14))

        story.append(Paragraph("Humanised Content", styles["EchoHeading"]))
        for block in self._paragraph_blocks(str(report.get("humanised_content") or "")):
            story.append(Paragraph(self._escape_pdf_text(block), styles["EchoBody"]))

        doc.build(story)
        return buffer.getvalue()

    def _candidate_phrases(self, text: str) -> list[str]:
        candidates: list[str] = []
        seen: set[str] = set()
        for sentence in SENTENCE_SPLIT_RE.split(text or ""):
            cleaned = re.sub(r"\s+", " ", sentence).strip(" -\t\r\n")
            if self._word_count(cleaned) <= 5:
                continue
            normalised = cleaned.lower()
            if normalised in seen:
                continue
            seen.add(normalised)
            candidates.append(cleaned)
        return candidates[:15]

    def _best_serper_hit(self, phrase: str, organic: list[dict[str, Any]]) -> dict[str, Any] | None:
        best_hit: dict[str, Any] | None = None
        best_ratio = 0.0
        phrase_lower = phrase.lower()
        for item in organic:
            combined = " ".join(
                str(item.get(key) or "") for key in ("title", "snippet")
            ).strip()
            combined_lower = combined.lower()
            exact_phrase = phrase_lower in combined_lower
            ratio = SequenceMatcher(None, phrase_lower, combined_lower).ratio() if combined_lower else 0.0
            if exact_phrase:
                ratio = max(ratio, 0.85)
            if ratio > best_ratio:
                best_ratio = ratio
                best_hit = item
        return best_hit if best_ratio >= 0.55 else None

    def _run_humanise_prompt(self, prompt: str) -> HumaniseResult:
        client = self._get_anthropic_client()
        last_error: Exception | None = None
        attempted: list[str] = []

        for model in self._anthropic_models:
            if not model or model in attempted:
                continue
            attempted.append(model)
            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=4096,
                    temperature=0.55,
                    system=HUMANISE_SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw_text = self._anthropic_text(response)
                return self._parse_humanised_response(raw_text)
            except Exception as exc:
                last_error = exc
                if "model" not in str(exc).lower():
                    break

        if last_error is None:
            raise RuntimeError("Anthropic model configuration is empty")
        raise RuntimeError(f"Claude humanisation failed: {last_error}") from last_error

    def _get_anthropic_client(self) -> anthropic.Anthropic:
        if self._anthropic_client is None:
            self._anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        return self._anthropic_client

    def _anthropic_text(self, response: Any) -> str:
        parts = []
        for block in getattr(response, "content", []) or []:
            text = getattr(block, "text", "")
            if text:
                parts.append(text)
        return "\n".join(parts).strip()

    def _parse_humanised_response(self, response_text: str) -> HumaniseResult:
        meta_title_match = META_TITLE_RE.search(response_text or "")
        meta_desc_match = META_DESC_RE.search(response_text or "")

        meta_title = self._clean_meta_value(meta_title_match.group(1) if meta_title_match else "")
        meta_desc = self._clean_meta_value(meta_desc_match.group(1) if meta_desc_match else "")
        content = META_TITLE_RE.sub("", response_text or "")
        content = META_DESC_RE.sub("", content)
        content = content.strip()

        if not meta_title:
            meta_title = self._fallback_meta_title(content)
        if not meta_desc:
            meta_desc = self._fallback_meta_desc(content)

        return HumaniseResult(
            content=content,
            meta_title=self._fit_meta(meta_title, 60),
            meta_desc=self._fit_meta(meta_desc, 155),
        )

    def _fallback_meta_title(self, text: str) -> str:
        snippet = self._fit_meta(text.replace("\n", " "), 60)
        return snippet or "SEO Content Review"

    def _fallback_meta_desc(self, text: str) -> str:
        sentences = FALLBACK_META_SENTENCE_RE.split(text.replace("\n", " "))
        for sentence in sentences:
            cleaned = sentence.strip()
            if cleaned:
                return self._fit_meta(cleaned, 155)
        return "Humanised SEO content ready for admin review."

    def _fit_meta(self, value: str, limit: int) -> str:
        cleaned = re.sub(r"\s+", " ", value or "").strip(" []")
        if len(cleaned) <= limit:
            return cleaned
        shortened = cleaned[: limit - 1].rstrip(" ,;:-")
        return f"{shortened}..."

    def _missing_keywords(self, text: str, seo_keywords: list[str]) -> list[str]:
        content = (text or "").lower()
        missing: list[str] = []
        for keyword in self._normalise_keywords(seo_keywords):
            if keyword.lower() not in content:
                missing.append(keyword)
        return missing

    def _normalise_keywords(self, seo_keywords: list[str]) -> list[str]:
        normalised: list[str] = []
        seen: set[str] = set()
        for keyword in seo_keywords or []:
            cleaned = re.sub(r"\s+", " ", str(keyword or "").strip())
            if not cleaned:
                continue
            lowered = cleaned.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            normalised.append(cleaned)
        return normalised

    def _clean_meta_value(self, value: str) -> str:
        return re.sub(r"\s+", " ", value or "").strip(" ]")

    def _escape_pdf_text(self, value: str) -> str:
        return (
            value.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br/>")
        )

    def _paragraph_blocks(self, text: str) -> list[str]:
        blocks = [block.strip() for block in re.split(r"\n\s*\n", text or "") if block.strip()]
        return blocks or ["-"]

    def _word_count(self, text: str) -> int:
        return len(WORD_RE.findall(text or ""))
