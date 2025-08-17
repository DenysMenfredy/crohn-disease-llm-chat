from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs):
        """Called each time the LLM generates a new token"""
        self.text += token
        # Update Streamlit UI progressively
        self.container.markdown(self.text)

    def on_llm_end(self, response, **kwargs):
        """Called when LLM is finished"""
        self.container.markdown(self.text)
