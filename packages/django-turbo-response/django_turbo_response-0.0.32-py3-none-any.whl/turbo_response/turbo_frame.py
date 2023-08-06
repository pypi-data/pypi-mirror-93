# Standard Library
from typing import Any, Dict, List, Optional, Union

# Django
from django.http import HttpRequest

# Local
from .response import TurboFrameResponse, TurboFrameTemplateResponse, render_turbo_frame
from .template import render_turbo_frame_template


class TurboFrameTemplateProxy:
    """Wraps template functionality."""

    def __init__(
        self,
        template_name: Union[str, List[str]],
        context: Dict[str, Any],
        *,
        dom_id: str,
        **template_kwargs,
    ):
        self.template_name = template_name
        self.context = context
        self.template_kwargs = template_kwargs
        self.dom_id = dom_id

    def render(self) -> str:
        """
        :param content: enclosed content
        :return: a *<turbo-frame>* string
        """
        return render_turbo_frame_template(
            self.template_name, self.context, dom_id=self.dom_id, **self.template_kwargs
        )

    def response(self, request: HttpRequest, **kwargs) -> TurboFrameTemplateResponse:
        return TurboFrameTemplateResponse(
            request,
            self.template_name,
            self.context,
            dom_id=self.dom_id,
            **{**self.template_kwargs, **kwargs},
        )


class TurboFrame:
    """Class for creating Turbo Frame strings and responses."""

    def __init__(self, dom_id: str):
        """
        :param dom_id: DOM ID of turbo frame
        """
        self.dom_id = dom_id

    def render(self, content: str = "") -> str:
        """
        :param content: enclosed content
        :return: a *<turbo-frame>* string
        """
        return render_turbo_frame(dom_id=self.dom_id, content=content)

    def response(self, content: str = "", **response_kwargs) -> TurboFrameResponse:
        """
        :param content: enclosed content
        :return: a *<turbo-frame>* HTTP response
        """
        return TurboFrameResponse(
            dom_id=self.dom_id, content=content, **response_kwargs
        )

    def template(
        self,
        template_name: Union[str, List[str]],
        context=Optional[Dict[str, Any]],
        **template_kwargs,
    ) -> TurboFrameTemplateProxy:
        """
        :param template_name: Django template name(s)
        :param context: template context
        :return: a *<turbo-frame>* HTTP response
        """
        return TurboFrameTemplateProxy(
            template_name, context, dom_id=self.dom_id, **template_kwargs
        )
