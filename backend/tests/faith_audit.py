from __future__ import annotations

from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


FAITH_STOP_WORDS = [
    "chapter", "verse", "shloka", "slokas", "gita", "bhagavad",
    "bible", "scripture", "testament", "lord", "god", "krishna",
    "arjuna", "christ", "jesus", "holy", "faith", "unto", "shall",
    "thee", "thou", "recitation", "meaning", "translation", "prayer",
    "spiritual", "teaching", "wisdom", "divine",
]


def run_faith_compliance_check(
    page_content_list: list[str],
    ceiling: float = 30.0,
    cluster_name: str = "unnamed",
) -> bool:
    custom_stops = list(text.ENGLISH_STOP_WORDS.union(FAITH_STOP_WORDS))

    vectorizer = TfidfVectorizer(stop_words=custom_stops, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(page_content_list)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    np.fill_diagonal(similarity_matrix, 0)

    worst_pair_score = float(np.max(similarity_matrix)) * 100
    avg_score = float(np.mean(similarity_matrix[similarity_matrix > 0])) * 100

    status = "PASS" if worst_pair_score <= ceiling else "FAIL"
    print(f"[E.C.H.O. Audit] Cluster: {cluster_name}")
    print(f"  Pages tested: {len(page_content_list)}")
    print(f"  Worst-pair: {worst_pair_score:.2f}% (ceiling: {ceiling}%)")
    print(f"  Average: {avg_score:.2f}%")
    print(f"  Result: {status}")

    return worst_pair_score <= ceiling


def audit_gita_cluster(verse_data: list[dict]) -> bool:
    contents = [
        f"{page['hook']} {page.get('etymology_intro', '')} "
        f"{' '.join(item.get('application', '') for item in page.get('etymology_items', []))} "
        f"{page['application']} {page['transit_layer']}"
        for page in verse_data
    ]
    cluster_name = f"gita-{verse_data[0]['chapter']}-{verse_data[0]['verse']}"
    return run_faith_compliance_check(contents, ceiling=30.0, cluster_name=cluster_name)


def audit_bible_topic_cluster(topic_data: list[dict]) -> bool:
    contents = [
        f"{page['emotional_frame']} {page['hermeneutical']} {page['application']} {page['vedic_bridge']}"
        for page in topic_data
    ]
    cluster_name = f"bible-{topic_data[0]['topic_slug']}"
    return run_faith_compliance_check(contents, ceiling=35.0, cluster_name=cluster_name)


def audit_daily_cluster(daily_pages: list[dict]) -> bool:
    contents = [
        f"{page['energy_intro']} {page['gita_application']} {page['bible_application']} {' '.join(page['daily_practices'])}"
        for page in daily_pages
    ]
    return run_faith_compliance_check(contents, ceiling=40.0, cluster_name="daily-sign-month")


def audit_transit_cluster(transit_pages: list[dict], tradition: str) -> bool:
    contents = [
        f"{page['energy_intro']} {page['practice_body']} {page['prayer_body']} {' '.join(item['why_it_fits'] for item in page['scripture_cards'])}"
        for page in transit_pages
        if page["tradition"] == tradition
    ]
    return run_faith_compliance_check(contents, ceiling=40.0, cluster_name=f"transit-{tradition}")
