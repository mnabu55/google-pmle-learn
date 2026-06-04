#!/usr/bin/env python3
import sys
import argparse
from google.cloud import language_v1

def analyze_text(text: str):
    """
    Analyzes the sentiment and entities of the input text using
    Google Cloud Natural Language API.
    """
    # Create a client
    client = language_v1.LanguageServiceClient()

    # Set up the document
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language="ja"  # Default to Japanese
    )

    print("=== Analyzing Text ===")
    print(f"Input: {text}\n")

    # 1. Sentiment Analysis
    try:
        sentiment_response = client.analyze_sentiment(request={"document": document})
        sentiment = sentiment_response.document_sentiment
        print("--- Sentiment Analysis ---")
        print(f"Score: {sentiment.score:.2f} (ranges from -1.0 to 1.0)")
        print(f"Magnitude: {sentiment.magnitude:.2f} (strength of emotion, >= 0.0)")
        
        # Simple sentiment interpretation
        if sentiment.score >= 0.25:
            interpretation = "Positive 🟢"
        elif sentiment.score <= -0.25:
            interpretation = "Negative 🔴"
        else:
            interpretation = "Neutral / Mixed 🟡"
        print(f"Interpretation: {interpretation}\n")
    except Exception as e:
        print(f"Failed to perform sentiment analysis: {e}\n")

    # 2. Entity Analysis
    try:
        entity_response = client.analyze_entities(request={"document": document})
        print("--- Entity Analysis ---")
        # Sort entities by salience (relevance to the document)
        entities = sorted(entity_response.entities, key=lambda x: x.salience, reverse=True)
        
        # Map entity type enum to string
        type_mapping = {
            language_v1.Entity.Type.UNKNOWN: "UNKNOWN",
            language_v1.Entity.Type.PERSON: "PERSON (人)",
            language_v1.Entity.Type.LOCATION: "LOCATION (場所/地名)",
            language_v1.Entity.Type.ORGANIZATION: "ORGANIZATION (組織/団体)",
            language_v1.Entity.Type.EVENT: "EVENT (イベント)",
            language_v1.Entity.Type.WORK_OF_ART: "WORK_OF_ART (作品)",
            language_v1.Entity.Type.CONSUMER_GOOD: "CONSUMER_GOOD (消費財)",
            language_v1.Entity.Type.OTHER: "OTHER",
            language_v1.Entity.Type.PHONE_NUMBER: "PHONE_NUMBER",
            language_v1.Entity.Type.ADDRESS: "ADDRESS",
            language_v1.Entity.Type.DATE: "DATE",
            language_v1.Entity.Type.NUMBER: "NUMBER",
            language_v1.Entity.Type.PRICE: "PRICE",
        }

        for entity in entities[:10]:  # Limit to top 10 entities
            entity_type = type_mapping.get(entity.type_, "OTHER")
            print(f"- Name: {entity.name}")
            print(f"  Type: {entity_type}")
            print(f"  Salience (Importance): {entity.salience:.2%}")
            if entity.metadata:
                for key, val in entity.metadata.items():
                    print(f"  Metadata - {key}: {val}")
            print()
    except Exception as e:
        print(f"Failed to perform entity analysis: {e}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Google Cloud Natural Language API Sample Script"
    )
    parser.add_argument(
        "text",
        type=str,
        nargs="?",
        default="Google Cloud の Natural Language API はとても便利で強力なツールです。",
        help="Text to be analyzed."
    )
    args = parser.parse_args()
    
    analyze_text(args.text)

if __name__ == "__main__":
    main()
