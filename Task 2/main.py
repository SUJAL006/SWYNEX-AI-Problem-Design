import os
import json
from enum import Enum
from pydantic import BaseModel, Field
from openai import OpenAI

# Ensure you set your API key in your environment variables:
# export OPENAI_API_KEY="sk-..."
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define our strict label categories
class Category(str, Enum):
    food_quality = "food_quality"
    wait_time = "wait_time"
    cleanliness = "cleanliness"
    other = "other"

# Define the expected JSON output format from the model
class ClassificationResult(BaseModel):
    label: Category = Field(description="The single best category for the comment.")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0.")

def route_comment(comment_text: str, threshold: float = 0.70) -> dict:
    """
    Classifies a dining hall comment and applies routing rules.
    - If confidence < threshold, it becomes 'unlabeled'.
    - If 'cleanliness', it gets a priority flag.
    """
    system_prompt = """
    You are an internal routing assistant for a dining hall. 
    Classify the following short student comment into EXACTLY ONE of these categories:
    - food_quality (taste, temperature, cooking issues)
    - wait_time (lines, slow service)
    - cleanliness (spills, dirty stations, pests, hygiene)
    - other (requests, off-topic, mixed feedback)
    
    Provide your confidence score (0.0 to 1.0).
    """

    # Call the model enforcing the Pydantic schema
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": comment_text}
        ],
        response_format=ClassificationResult,
        temperature=0.1 # Low temperature for more consistent classification
    )

    ai_output = response.choices[0].message.parsed
    
    # Apply business logic constraints
    final_label = ai_output.label.value
    requires_human_review = False
    priority_jump = False

    # Constraint 1: Abstain if below threshold
    if ai_output.confidence < threshold:
        final_label = "unlabeled"
        requires_human_review = True

    # Constraint 2: Cleanliness jumps the queue
    if final_label == "cleanliness":
        priority_jump = True

    return {
        "original_text": comment_text,
        "ai_predicted_label": ai_output.label.value,
        "confidence": round(ai_output.confidence, 2),
        "final_routing_label": final_label,
        "priority_jump_queue": priority_jump,
        "needs_human_coordinator": requires_human_review
    }

if __name__ == "__main__":
    # Load test data
    with open("test_comments.json", "r") as f:
        comments = json.load(f)
    
    print("--- DINING HALL ROUTER PROTOTYPE ---")
    print(f"Applying confidence threshold: 0.70\n")
    
    for comment in comments:
        result = route_comment(comment["text"])
        print(f"Comment: '{result['original_text']}'")
        print(f"  -> Predicted: {result['ai_predicted_label']} ({result['confidence']})")
        print(f"  -> Routed As: {result['final_routing_label']}")
        if result['priority_jump_queue']:
            print(f"  -> ⚠️ ACTION: URGENT QUEUE JUMP (Cleanliness)")
        elif result['needs_human_coordinator']:
            print(f"  -> ⚠️ ACTION: Sent to Human Coordinator (Low Confidence)")
        print("-" * 40)
