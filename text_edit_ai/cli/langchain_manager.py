from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model


SYSTEM_PROMPT = """You are a writing editor. Edit the section of text in <writing> based on the instructions in <context>. Respond only with the revised text."""


class LangchainManager:
    def __init__(self, config_manager):
        self.system_prompt = SYSTEM_PROMPT
        self.config_manager = config_manager
        self.api_key = self.config_manager.get_api_key()
        self.model_name = self.config_manager.get_model()
        self.model = self.get_model()

    def get_model(self):
        """Get appropriate chat model based on model name.
        
        Uses ChatGoogleGenerativeAI directly for Google models,
        and init_chat_model for other providers.
        """
        # Handle Google models directly (which had issues with init_chat_model)
        try:
            if self.model_name.startswith("gemini"):
                return ChatGoogleGenerativeAI(
                    model=self.model_name, 
                    google_api_key=self.api_key, 
                    temperature=0
                )
            return init_chat_model(self.model_name, api_key=self.api_key, temperature=0)
        except Exception as e:
            print(f"Error initializing model: {e}")
            print("Model name invalid. Please set another model.")
            self.config_manager.set_model()
            self.__init__(self.config_manager)
            return self.get_model()

    def get_response(self, context, writing):
        try:
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

            return response
        except Exception as e:
            print(f"Error initializing model: {e}")
            print("Model name invalid. Please set another model.")
            self.config_manager.set_model()
            self.__init__(self.config_manager)
            return self.get_response(context, writing)

    def cleanup(self):
        """Clean up resources to prevent gRPC timeout errors."""
        if hasattr(self.model, "client"):
            if hasattr(self.model.client, "close"):
                try:
                    self.model.client.close()
                except Exception:
                    pass
        self.model = None
