# coding: utf-8

"""Base exception handling.
"""

from oslo_log import log as logging
import six
import webob.exc

from .i18n import _

LOG = logging.getLogger(__name__)


class ConvertedException(webob.exc.WSGIHTTPException):
    def __init__(self, code=0, title="", explanation=""):
        self.code = code
        self.title = title
        self.explanation = explanation
        super(ConvertedException, self).__init__()


def _cleanse_dict(original):
    """Strip all admin_password, new_pass, rescue_pass keys from a dict."""
    return {k: v for k, v in six.iteritems(original) if "_pass" not in k}


class BaseException(Exception):
    """Base Nova Exception
    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.
    """
    msg_fmt = _("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except Exception:
                LOG.exception(_('Exception in string format operation'))
                for name, value in six.iteritems(kwargs):
                    LOG.error("%s: %s" % (name, value))    # noqa

                message = self.msg_fmt

        self.message = message
        super(BaseException, self).__init__(message)

    def format_message(self):
        # NOTE(mrodden): use the first argument to the python Exception object
        # which should be our full BaseException message, (see __init__)
        return self.args[0]


class Forbidden(BaseException):
    ec2_code = 'AuthFailure'
    msg_fmt = _("Not authorized.")
    code = 403


class AdminRequired(Forbidden):
    msg_fmt = _("User does not have admin privileges")


class Invalid(BaseException):
    msg_fmt = _("Unacceptable parameters.")
    code = 400


class InvalidAttribute(Invalid):
    msg_fmt = _("Attribute not supported: %(attr)s")


class ServiceUnavailable(Invalid):
    msg_fmt = _("Service is unavailable at this time.")


class InvalidToken(Invalid):
    msg_fmt = _("The token '%(token)s' is invalid or has expired")


class InvalidConnectionInfo(Invalid):
    msg_fmt = _("Invalid Connection Info")


class InvalidHostname(Invalid):
    msg_fmt = _("Invalid characters in hostname '%(hostname)s'")


class InvalidContentType(Invalid):
    msg_fmt = _("Invalid content type %(content_type)s.")


class InvalidAPIVersionString(Invalid):
    msg_fmt = _("API Version String %(version)s is of invalid format. Must "
                "be of format MajorNum.MinorNum.")


class InvalidInput(Invalid):
    msg_fmt = _("Invalid input received: %(reason)s")


class VersionNotFoundForAPIMethod(Invalid):
    msg_fmt = _("API version %(version)s is not supported on this method.")


class BadRequest(BaseException):
    msg_fmt = _("Bad Request")
    code = 400


class MalformedRequestBody(BadRequest):
    msg_fmt = _("Malformed message body: %(reason)s")


class NotFound(BaseException):
    msg_fmt = _("Resource could not be found.")
    code = 404


class FileNotFound(NotFound):
    msg_fmt = _("File %(file_path)s could not be found.")


class ConfigNotFound(BaseException):
    msg_fmt = _("Could not find config at %(path)s")


class PasteAppNotFound(BaseException):
    msg_fmt = _("Could not load paste app '%(name)s' from %(path)s")


class CoreAPIMissing(BaseException):
    msg_fmt = _("Core API extensions are missing: %(missing_apis)s")


# Cannot be templated, msg needs to be constructed when raised.
class InternalError(BaseException):
    ec2_code = 'InternalError'
    msg_fmt = "%(err)s"


class SocketPortInUseException(BaseException):
    msg_fmt = _("Not able to bind %(host)s:%(port)d, %(error)s")
