from vaderSentiment.vaderSentiment import (
    SentimentIntensityAnalyzer
)

_sia = SentimentIntensityAnalyzer()


def sentiment_for_text(text):

    if not text or not text.strip():

        return {

            "compound": 0.0,

            "label": "neutral"
        }

    s = _sia.polarity_scores(text)

    c = s.get(
        "compound",
        0.0
    )

    label = (

        "positive"
        if c >= 0.05

        else "negative"
        if c <= -0.05

        else "neutral"
    )

    s["label"] = label

    return s


def extract_text(rv):

    t = rv.get("snippet") or ""

    if not t:

        ex = rv.get(
            "extracted_snippet"
        ) or {}

        t = (

            ex.get("translated")

            or ex.get("original")

            or rv.get("text")

            or ""
        )

    return t