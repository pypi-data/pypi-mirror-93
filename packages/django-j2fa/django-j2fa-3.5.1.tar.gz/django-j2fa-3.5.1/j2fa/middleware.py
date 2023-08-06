import logging
from django.conf import settings
from ipware.ip import get_client_ip  # type: ignore  # pytype: disable=import-error
from j2fa.models import TwoFactorSession
from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import SessionBase
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import resolve, reverse


# These can be overridden in settings.py by defining variable J2FA_EXCLUDED_ROUTES
J2FA_EXCLUDED_ROUTES = [
    "j2fa-obtain-auth",
    "logout",
]

logger = logging.getLogger(__name__)


class Ensure2FactorAuthenticatedMiddleware:
    """
    Ensures that User is 2-factor authenticated.
    Place after session init.
    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    def is_2fa_required(self, user: User) -> bool:
        """
        Checks User.profile.require_2fa boolean.
        You can override this if custom toggle location is needed.
        :param user: User
        :return: bool
        """
        return user.is_authenticated and hasattr(user, "profile") and user.profile.require_2fa  # type: ignore

    def __call__(self, request: HttpRequest):
        user = request.user
        if isinstance(user, User):
            session = request.session
            assert isinstance(session, SessionBase)
            user_agent = request.META.get("HTTP_USER_AGENT", "")
            ip = get_client_ip(request)[0]
            if ip is None and settings.DEBUG:
                ip = "127.0.0.1"

            # excluded routes
            excluded_routes = J2FA_EXCLUDED_ROUTES
            if hasattr(settings, "J2FA_EXCLUDED_ROUTES"):
                excluded_routes = getattr(settings, "J2FA_EXCLUDED_ROUTES")

            # Load auth data, and redirect if not valid
            route_name = resolve(request.path_info).url_name
            if self.is_2fa_required(user) and route_name not in excluded_routes:
                j2fa_session_id = session.get("j2fa_session", None)
                j2fa_session = TwoFactorSession.objects.filter(id=j2fa_session_id).first()
                assert j2fa_session is None or isinstance(j2fa_session, TwoFactorSession)
                if not j2fa_session or not j2fa_session.is_valid(user, ip, user_agent) or not j2fa_session.active:
                    logger.info("J2FA_REQUIRE_AUTH: route=%s, j2fa_session_id=%s", route_name, j2fa_session_id)
                    return redirect(reverse("j2fa-obtain-auth"))

        # get response
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response
