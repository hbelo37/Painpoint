from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# Initialize the model and tokenizer once at module level
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Add this with other initializations at the top
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

def extract_pain_points(texts, company_name=None):
    """
    Extract and summarize top 5 pain points with company-specific filtering.
    """
    try:
        issues = []
        
        print(f"Processing {len(texts)} texts")

        for text in texts:
            if isinstance(text, dict):
                content = f"{text.get('title', '')} {text.get('description', '')}"
            else:
                content = text

            # Skip if content is too short or doesn't mention company (if company_name is provided)
            if not content or len(content.strip()) < 10:
                continue
            if company_name and company_name.lower() not in content.lower():
                continue

            try:
                sentiment = sentiment_analyzer(content)[0]
                if sentiment['label'] == 'NEGATIVE' and sentiment['score'] > 0.6:
                    summary = content.split('.')[0] if '.' in content else content[:150]
                    issues.append({
                        'summary': summary.strip(),
                        'score': sentiment['score']
                    })
            except Exception as e:
                print(f"Error analyzing text: {e}")
                continue

        # Sort by score and get top 5
        issues.sort(key=lambda x: x['score'], reverse=True)
        formatted_points = []
        
        for issue in issues[:5]:
            formatted_points.append(f"🔴 {issue['summary']}")

        return formatted_points if formatted_points else ["No significant pain points detected."]

    except Exception as e:
        print(f"Error in extract_pain_points: {e}")
        return [f"Error processing text: {str(e)}"]

def extract_keywords(texts):
    """
    Extract key entities such as organizations (ORG), geopolitical entities (GPE), or products (PRODUCT) 
    from the text using a Named Entity Recognition (NER) pipeline.
    """
    keywords = []

    for text in texts:
        entities = ner_pipeline(text)
        for entity in entities:
            if entity['entity_group'] in ['ORG', 'LOC', 'MISC', 'PRODUCT']:
                keywords.append(entity['word'])
    
    return keywords

# Example Usage
if __name__ == "__main__":
    sample_texts = [
        "The company is facing issues with its new product launch in the United States.",
        "Customer feedback indicates dissatisfaction with the pricing strategy.",
        "The marketing department at Apple Inc. is underperforming.",
        "There are concerns about product quality."
    ]
