from langchain.callbacks.base import BaseCallbackHandler
import time

class StreamHandler(BaseCallbackHandler):
    def __init__(self, messages_list, placeholder, update_every=5, flush_interval=0.05):
        """
        messages_list: list containing only the last assistant message
        placeholder: st.empty() placeholder for assistant
        """
        self.messages_list = messages_list
        self.placeholder = placeholder
        self.update_every = update_every
        self.flush_interval = flush_interval
        self.text = ""
        self._counter = 0
        self._last_flush = time.time()

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self._counter += 1
        self.messages_list[-1]["content"] = self.text

        if self._counter % self.update_every == 0 or (time.time() - self._last_flush) > self.flush_interval:
            self._render()
            self._last_flush = time.time()

    def _render(self):
        bubble_html = f"""
        <div style="
            background-color:#F1F0F0;
            color:#000000;
            padding:12px 16px;
            border-radius:12px;
            margin:6px 0px;
            font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size:15px;
            line-height:1.4;
            box-shadow:0px 1px 3px rgba(0,0,0,0.1);
            max-width:80%;
            white-space:pre-wrap;
        ">
            <span style="margin-right:6px; font-size:18px;">🤖</span>{self.text}
        </div>
        """
        self.placeholder.markdown(bubble_html, unsafe_allow_html=True)
