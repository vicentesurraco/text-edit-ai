from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

model = init_chat_model("llama3-8b-8192", model_provider="groq")
#
# SYSTEM_PROMPT = """You are a professional writing editor. You take instructions from the user in the context section, and respond to a user's writings in the writing section with a complete new draft, and offer no commentary before or after."""
SYSTEM_PROMPT = """You are a writing editor. Edit the section of text in <writing> based on the instructions in <context>. Respond only with the revised text."""


class LangchainManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.system_prompt = SYSTEM_PROMPT
        self.model = init_chat_model(
            "claude-3-5-sonnet-latest", model_provider="anthropic", temperature=0
        )

    def get_response(self, context, writing):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("user", f"<context>{context}</context><writing>{writing}</writing>"),
            ]
        )
        full_response = ""
        for token in self.model.stream(prompt):
            full_response += token.content
            print(token.content)

        print(f"\n\n here's the full response {full_response}")
        return full_response
