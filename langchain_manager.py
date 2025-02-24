from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


#
# SYSTEM_PROMPT = """You are a professional writing editor. You take instructions from the user in the context section, and respond to a user's writings in the writing section with a complete new draft, and offer no commentary before or after."""
SYSTEM_PROMPT = """You are a writing editor. Edit the section of text in <writing> based on the instructions in <context>. Respond only with the revised text."""


class LangchainManager:
    def __init__(self, api_key):
        self.system_prompt = SYSTEM_PROMPT
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", google_api_key=api_key, temperature=0
        )

    def get_response(self, context, writing):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("user", f"<context>{context}</context><writing>{writing}</writing>"),
            ]
        )
        messages = prompt.format_messages()

        response = ""
        for token in self.model.stream(messages):
            content = token.content
            response += content

        print(f"\n{response}\n")
        return response
