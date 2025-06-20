import time
from typing import Any, List, Mapping, Optional
# Removed datetime, timedelta as proactive rate limiting is removed
# from datetime import datetime, timedelta

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatGenerationChunk, ChatResult

# Import the specific exceptions to catch
from google.api_core.exceptions import InternalServerError, ResourceExhausted

class RateLimitedModel(BaseChatModel):
    """A wrapper around a chat model that adds a delay after InternalServerError."""

    model: BaseChatModel
    # delay_seconds is no longer used for fixed delay, but keep for potential future use or identification
    delay_seconds: float = 0 # Default to 0 as fixed delay is removed

    def __init__(self, model: BaseChatModel, delay_seconds: float = 0, **kwargs: Any):
        super().__init__(model=model, delay_seconds=delay_seconds, **kwargs)
        # request_timestamps and _wait_for_rate_limit are removed


    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate chat response with a delay after InternalServerError."""
        try:
            return self.model.generate(messages, stop=stop, callbacks=run_manager, **kwargs)
        except (InternalServerError, ResourceExhausted) as e:
            print(f"API error encountered: {e}. Sleeping for 60 seconds before re-raising.")
            time.sleep(60) # Sleep for 1 minute
            raise e # Re-raise the exception


    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> Any:
         """Stream chat response with a delay after InternalServerError."""
         try:
             return self.model.stream(messages, stop=stop, callbacks=run_manager, **kwargs)
         except (InternalServerError, ResourceExhausted) as e:
             print(f"API error encountered: {e}. Sleeping for 60 seconds before re-raising.")
             time.sleep(60) # Sleep for 1 minute
             raise e # Re-raise the exception


    @property
    def _llm_type(self) -> str:
        return f"rate-limited-{self.model._llm_type}"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {
            "model": self.model._identifying_params,
            "delay_seconds": self.delay_seconds, # Keep for identification
        }

    def bind_tools(self, tools: List, **kwargs: Any) -> BaseChatModel:
        """Bind tools to the model."""
        return self.model.bind_tools(tools, **kwargs)
