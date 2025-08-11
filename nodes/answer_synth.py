from nodes.gemini_agent import gemini_generate

def answer_synth_node(state: dict) -> dict:
    """
    AnswerSynth node: uses Gemini to synthesize a final answer from extracted content and verified sources.
    """
    user_question = state.get('user_input', '')
    facts = '\n'.join(state.get('extracted_content', []))
    sources = ', '.join(state.get('verified_sources', []))
    prompt = (
        f"User question: {user_question}\n"
        f"Relevant facts:\n{facts}\n"
        f"Sources: {sources}\n"
        "Write a concise, accurate answer using the facts and cite sources where appropriate."
    )
    answer = gemini_generate(prompt)
    state['final_answer'] = answer.strip()
    return state
