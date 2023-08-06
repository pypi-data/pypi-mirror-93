"""Purplship Canpar client settings."""

from purplship.core.settings import Settings as BaseSettings
from purplship.core.utils import Envelope, apply_namespaceprefix, XP


class Settings(BaseSettings):
    """Canpar connection settings."""

    username: str
    password: str
    language: str = "en"
    id: str = None

    @property
    def carrier_name(self):
        return "canpar"

    @property
    def server_url(self):
        return (
            'https://sandbox.canpar.com/canshipws/services'
            if self.test else
            'https://canship.canpar.com/canshipws/services'
        )


def default_request_serializer(envelope: Envelope) -> str:
    namespace_ = (
        ' xmlns:soap="http://www.w3.org/2003/05/soap-envelope"'
        ' xmlns:ws="http://ws.onlinerating.canshipws.canpar.com"'
        ' xmlns="http://ws.dto.canshipws.canpar.com/xsd"'
        ' xmlns:xsd1="http://dto.canshipws.canpar.com/xsd"'
    )
    envelope.ns_prefix_ = 'soapenv'
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Body.anytypeobjs_[0].ns_prefix_ = "ws"
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0].request, "")
    envelope.Body.anytypeobjs_[0].request.ns_prefix_ = "ws"

    return XP.export(envelope, namespacedef_=namespace_)
