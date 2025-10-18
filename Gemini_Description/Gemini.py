import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

env_path = 'D:\clipquery_github\CLIPQUERY\Gemini_Description\.env'
def load_llm(env_path):
    load_dotenv(env_path)
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash") 
    print("Gemini model loaded successfully.")
    return model

PROMPT_TEMPLATE = """
You are an expert video summarizer creating a continuous, scene-by-scene description.

Your task is to synthesize the transcript and frame descriptions for the CURRENT scene into a single, cohesive summary sentence.

You MUST also consider the summary of the PREVIOUS scene to ensure continuity and avoid repetition.

## PREVIOUS SCENE SUMMARY ##
{previous_description}

## CURRENT SCENE DATA ##
Transcript: {transcript_text}
Visuals:
{formatted_visuals}

**Instructions:**
- Combine the transcript and visuals into one fluid sentence describing the main action and dialogue of the CURRENT scene.
- Use the previous summary for context ONLY. Do not repeat information from it.
- Be concise. Output *only* the single summary sentence for the current scene.
"""



def generate_scene_summary(transcript, visuals, model, previous_summary=None):
    """
    Generates a summary for a single scene using the LLM.
    
    :param transcript: The transcript string for the current set.
    :param visuals: The list of visual description objects for the current set.
    :param previous_summary: The summary string generated for the *previous* set.
    :return: A new summary string, or None on failure.
    """
    if not model:
        print("LLM model is not loaded. Skipping summary generation.")
        return None
    
    
    # Handle the very first scene, which has no previous summary
    if previous_summary is None:
        previous_summary = "This is the first scene."

    # 1. Format the data for the prompt
    formatted_visuals = "\n".join([f"- At {v['timestamp']}s: {v['description']}" for v in visuals])
    
    # 2. Create the final prompt
    full_prompt = PROMPT_TEMPLATE.format(
        previous_description=previous_summary,
        transcript_text=transcript,
        formatted_visuals=formatted_visuals
    )
    
    # 3. Call the LLM
    try:
        result = model.invoke(full_prompt)
        return result.content.strip()
    except Exception as e:
        print(f"  [Error] LLM invocation failed: {e}")
        return None