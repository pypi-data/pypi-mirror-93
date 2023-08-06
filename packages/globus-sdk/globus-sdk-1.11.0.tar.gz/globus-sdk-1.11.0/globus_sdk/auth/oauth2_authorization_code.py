import logging

import six
from six.moves.urllib.parse import urlencode

from globus_sdk.auth.oauth2_constants import DEFAULT_REQUESTED_SCOPES
from globus_sdk.auth.oauth2_flow_manager import GlobusOAuthFlowManager
from globus_sdk.base import slash_join

logger = logging.getLogger(__name__)


class GlobusAuthorizationCodeFlowManager(GlobusOAuthFlowManager):
    """
    This is the OAuth flow designated for use by Clients wishing to
    authenticate users in a web application backed by a server-side component
    (e.g. an API). The key constraint is that there is a server-side system
    that can keep a Client Secret without exposing it to the web client.
    For example, a Django application can rely on the webserver to own the
    secret, so long as it doesn't embed it in any of the pages it generates.

    The application sends the user to get a temporary credential (an
    ``auth_code``) associated with its Client ID. It then exchanges that
    temporary credential for a token, protecting the exchange with its Client
    Secret (to prove that it really is the application that the user just
    authorized).

    :param auth_client: The ``AuthClient`` used to extract default values for the flow,
        and also to make calls to the Auth service.
    :type auth_client: :class:`ConfidentialAppAuthClient \
        <globus_sdk.ConfidentialAppAuthClient>`
    :param redirect_uri: The page that users should be directed to after authenticating
        at the authorize URL.
    :type redirect_uri: str
    :param requested_scopes: The scopes on the token(s) being requested, as a
        space-separated string or iterable of strings. Defaults to
        ``openid profile email urn:globus:auth:scope:transfer.api.globus.org:all``
    :type requested_scopes: str or iterable of str, optional
    :param state: This string allows an application to pass information back to itself
        in the course of the OAuth flow. Because the user will navigate away from the
        application to complete the flow, this parameter lets the app pass an arbitrary
        string from the starting page to the ``redirect_uri``
    :type state: str, optional
    :param refresh_tokens: When True, request refresh tokens in addition to access
        tokens. [Default: ``False``]
    :type refresh_tokens: bool, optional
    """

    def __init__(
        self,
        auth_client,
        redirect_uri,
        requested_scopes=None,
        state="_default",
        refresh_tokens=False,
    ):
        # default to the default requested scopes
        self.requested_scopes = requested_scopes or DEFAULT_REQUESTED_SCOPES
        # convert scopes iterable to string immediately on load
        if not isinstance(self.requested_scopes, six.string_types):
            self.requested_scopes = " ".join(self.requested_scopes)

        # store the remaining parameters directly, with no transformation
        self.client_id = auth_client.client_id
        self.auth_client = auth_client
        self.redirect_uri = redirect_uri
        self.refresh_tokens = refresh_tokens
        self.state = state

        logger.debug("Starting Authorization Code Flow with params:")
        logger.debug("auth_client.client_id={}".format(auth_client.client_id))
        logger.debug("redirect_uri={}".format(redirect_uri))
        logger.debug("refresh_tokens={}".format(refresh_tokens))
        logger.debug("state={}".format(state))
        logger.debug("requested_scopes={}".format(self.requested_scopes))

    def get_authorize_url(self, additional_params=None):
        """
        Start a Authorization Code flow by getting the authorization URL to
        which users should be sent.

        :param additional_params: Additional parameters to include in the authorize URL.
            Primarily for internal use
        :type additional_params: dict, optional
        :rtype: ``string``

        The returned URL string is encoded to be suitable to display to users
        in a link or to copy into their browser. Users will be redirected
        either to your provided ``redirect_uri`` or to the default location,
        with the ``auth_code`` embedded in a query parameter.
        """
        authorize_base_url = slash_join(
            self.auth_client.base_url, "/v2/oauth2/authorize"
        )
        logger.debug(
            "Building authorization URI. Base URL: {}".format(authorize_base_url)
        )
        logger.debug("additional_params={}".format(additional_params))

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.requested_scopes,
            "state": self.state,
            "response_type": "code",
            "access_type": (self.refresh_tokens and "offline") or "online",
        }
        if additional_params:
            params.update(additional_params)

        params = urlencode(params)
        return "{0}?{1}".format(authorize_base_url, params)

    def exchange_code_for_tokens(self, auth_code):
        """
        The second step of the Authorization Code flow, exchange an
        authorization code for access tokens (and refresh tokens if specified)

        :rtype: :class:`OAuthTokenResponse \
        <globus_sdk.auth.token_response.OAuthTokenResponse>`
        """
        logger.debug(
            (
                "Performing Authorization Code auth_code exchange. "
                "Sending client_id and client_secret"
            )
        )
        return self.auth_client.oauth2_token(
            {
                "grant_type": "authorization_code",
                "code": auth_code.encode("utf-8"),
                "redirect_uri": self.redirect_uri,
            }
        )
