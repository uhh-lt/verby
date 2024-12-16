import spacy


def build_pipeline(language: str = "de") -> spacy.Language:
    """
    Builds a spacy pipeline with the parser of your choice
    """
    if language == "de":
        nlp = spacy.load("de_dep_news_trf")
    elif language == "en":
        nlp = spacy.load("en_core_web_trf")
    else:
        raise ValueError("Unsupported language code")
    nlp.add_pipe("event_segmentation", after="parser")
    return nlp
