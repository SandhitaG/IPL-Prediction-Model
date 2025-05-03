import subprocess
import json

def get_prediction_reasoning(prediction: dict, match_info: dict) -> str:
    prompt = f"""
    You are a cricket analyst AI. Given the following match context and predictions:

    📋 Match Info: {json.dumps(match_info, indent=2)}
    📊 Prediction: {json.dumps(prediction, indent=2)}

    Explain in 3–5 sentences why this outcome is predicted. Highlight player form, venue influence, and team performance.
    """

    try:
        result = subprocess.run(["ollama", "run", "llama3", prompt], capture_output=True, text=True, timeout=30)
        return result.stdout.strip()
    except Exception as e:
        return f"LLM Reasoning Unavailable: {str(e)}"
