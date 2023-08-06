# -*- coding: utf-8 -*-

import abc

import ftplib
import imaplib
import poplib
import smtplib

import socket

import attr

import six

from cryptoparser.common.algorithm import Authentication, KeyExchange, NamedGroupType
from cryptoparser.common.exception import NotEnoughData, TooMuchData, InvalidType, InvalidValue

from cryptoparser.tls.ciphersuite import TlsCipherSuite, SslCipherKind
from cryptoparser.tls.ldap import (
    LDAPResultCode,
    LDAPExtendedRequestStartTLS,
    LDAPExtendedResponseStartTLS,
)
from cryptoparser.tls.rdp import (
    TPKT,
    COTPConnectionConfirm,
    COTPConnectionRequest,
    RDPProtocol,
    RDPNegotiationRequest,
    RDPNegotiationResponse,
)
from cryptoparser.tls.subprotocol import SslMessageType, SslHandshakeClientHello
from cryptoparser.tls.subprotocol import TlsHandshakeClientHello
from cryptoparser.tls.subprotocol import TlsCipherSuiteVector, TlsContentType, TlsHandshakeType
from cryptoparser.tls.subprotocol import TlsAlertLevel, TlsAlertDescription
from cryptoparser.tls.extension import TlsExtensionServerName
from cryptoparser.tls.extension import (
    TlsExtensionEllipticCurves,
    TlsExtensionSignatureAlgorithms,
    TlsNamedCurve,
    TlsSignatureAndHashAlgorithm,
)

from cryptoparser.tls.record import TlsRecord, SslRecord
from cryptoparser.tls.version import TlsVersion, TlsProtocolVersionFinal, SslVersion

from cryptolyzer.common.exception import NetworkError, NetworkErrorType, SecurityError, SecurityErrorType
from cryptolyzer.tls.exception import TlsAlert
from cryptolyzer.common.transfer import L4ClientTCP, L7TransferBase


class TlsHandshakeClientHelloSpecalization(TlsHandshakeClientHello):
    def __init__(
            self,
            hostname,
            protocol_versions,
            cipher_suites,
            elliptic_curves,
            signature_algorithms,
            extensions
    ):  # pylint: disable=too-many-arguments
        if hostname is not None:
            extensions.append(TlsExtensionServerName(hostname))

        if len(protocol_versions) > 1:
            raise NotImplementedError

        if protocol_versions[0] >= TlsProtocolVersionFinal(TlsVersion.TLS1_2):
            if elliptic_curves is None:
                elliptic_curves = list(TlsNamedCurve)
            if elliptic_curves:
                extensions.append(TlsExtensionEllipticCurves(elliptic_curves))

        if protocol_versions[0] >= TlsProtocolVersionFinal(TlsVersion.TLS1_2):
            if signature_algorithms is None:
                signature_algorithms = list(TlsSignatureAndHashAlgorithm)
            if signature_algorithms:
                extensions.append(TlsExtensionSignatureAlgorithms(signature_algorithms))

        super(TlsHandshakeClientHelloSpecalization, self).__init__(
            cipher_suites=cipher_suites,
            protocol_version=protocol_versions[0],
            extensions=extensions
        )


class TlsHandshakeClientHelloAnyAlgorithm(TlsHandshakeClientHelloSpecalization):
    def __init__(self, protocol_versions, hostname):
        super(TlsHandshakeClientHelloAnyAlgorithm, self).__init__(
            hostname=hostname,
            protocol_versions=protocol_versions,
            cipher_suites=list(TlsCipherSuite),
            elliptic_curves=None,
            signature_algorithms=None,
            extensions=[]
        )


class TlsHandshakeClientHelloAuthenticationBase(TlsHandshakeClientHelloSpecalization):
    # pylint: disable=too-many-ancestors
    def __init__(
            self,
            protocol_version,
            hostname,
            authentication,
            elliptic_curves=(),
            signature_algorithms=()
    ):  # pylint: disable=too-many-arguments
        _cipher_suites = TlsCipherSuiteVector([
            cipher_suite
            for cipher_suite in TlsCipherSuite
            if (cipher_suite.value.authentication and
                cipher_suite.value.authentication == authentication)
        ])

        super(TlsHandshakeClientHelloAuthenticationBase, self).__init__(
            hostname=hostname,
            protocol_versions=[protocol_version, ],
            cipher_suites=TlsCipherSuiteVector(_cipher_suites),
            elliptic_curves=elliptic_curves,
            signature_algorithms=signature_algorithms,
            extensions=[]
        )


class TlsHandshakeClientHelloAuthenticationRSA(TlsHandshakeClientHelloAuthenticationBase):
    # pylint: disable=too-many-ancestors
    def __init__(self, protocol_version, hostname):
        super(TlsHandshakeClientHelloAuthenticationRSA, self).__init__(
            hostname=hostname,
            protocol_version=protocol_version,
            authentication=Authentication.RSA,
            elliptic_curves=None,
            signature_algorithms=None,
        )


class TlsHandshakeClientHelloAuthenticationDSS(TlsHandshakeClientHelloAuthenticationBase):
    # pylint: disable=too-many-ancestors
    def __init__(self, protocol_version, hostname):
        super(TlsHandshakeClientHelloAuthenticationDSS, self).__init__(
            protocol_version=protocol_version,
            hostname=hostname,
            authentication=Authentication.DSS,
            elliptic_curves=None,
            signature_algorithms=None,
        )


class TlsHandshakeClientHelloAuthenticationECDSA(TlsHandshakeClientHelloAuthenticationBase):
    # pylint: disable=too-many-ancestors
    def __init__(self, protocol_version, hostname):
        super(TlsHandshakeClientHelloAuthenticationECDSA, self).__init__(
            hostname=hostname,
            protocol_version=protocol_version,
            authentication=Authentication.ECDSA,
            elliptic_curves=None,
            signature_algorithms=None,
        )


class TlsHandshakeClientHelloAuthenticationGOST(TlsHandshakeClientHelloAuthenticationBase):
    # pylint: disable=too-many-ancestors
    def __init__(self, protocol_version, hostname):
        super(TlsHandshakeClientHelloAuthenticationGOST, self).__init__(
            protocol_version=protocol_version,
            hostname=hostname,
            authentication=Authentication.GOST_R3410_94
        )


class TlsHandshakeClientHelloAuthenticationRarelyUsed(TlsHandshakeClientHelloSpecalization):
    def __init__(self, protocol_version, hostname):
        _cipher_suites = TlsCipherSuiteVector([
            cipher_suite
            for cipher_suite in TlsCipherSuite
            if (cipher_suite.value.authentication and
                cipher_suite.value.authentication in [
                    Authentication.DSS,
                    Authentication.KRB5,
                    Authentication.PSK,
                    Authentication.SRP,
                    Authentication.anon,
                ])
        ])

        super(TlsHandshakeClientHelloAuthenticationRarelyUsed, self).__init__(
            hostname=hostname,
            protocol_versions=[protocol_version, ],
            cipher_suites=TlsCipherSuiteVector(_cipher_suites),
            elliptic_curves=[],
            signature_algorithms=[],
            extensions=[]
        )


class TlsHandshakeClientHelloKeyExchangeDHE(TlsHandshakeClientHelloSpecalization):
    _CIPHER_SUITES = TlsCipherSuiteVector([
        cipher_suite
        for cipher_suite in TlsCipherSuite
        if cipher_suite.value.key_exchange == KeyExchange.DHE
    ])

    def __init__(self, protocol_version, hostname):
        super(TlsHandshakeClientHelloKeyExchangeDHE, self).__init__(
            hostname=hostname,
            protocol_versions=[protocol_version, ],
            cipher_suites=TlsCipherSuiteVector(self._CIPHER_SUITES),
            elliptic_curves=[
                named_group
                for named_group in TlsNamedCurve
                if (named_group.value.named_group and
                    named_group.value.named_group.value.group_type == NamedGroupType.DH_PARAM)
            ],
            signature_algorithms=None,
            extensions=[]
        )


class TlsHandshakeClientHelloKeyExchangeECDHx(TlsHandshakeClientHelloSpecalization):
    _CIPHER_SUITES = TlsCipherSuiteVector([
        cipher_suite
        for cipher_suite in TlsCipherSuite
        if (cipher_suite.value.key_exchange and
            cipher_suite.value.key_exchange in [KeyExchange.ECDH, KeyExchange.ECDHE])
    ])

    def __init__(self, protocol_version, hostname):
        super(TlsHandshakeClientHelloKeyExchangeECDHx, self).__init__(
            hostname=hostname,
            protocol_versions=[protocol_version, ],
            cipher_suites=TlsCipherSuiteVector(self._CIPHER_SUITES),
            elliptic_curves=None,
            signature_algorithms=None,
            extensions=[]
        )


class TlsHandshakeClientHelloBasic(TlsHandshakeClientHelloSpecalization):
    def __init__(self, protocol_version):
        super(TlsHandshakeClientHelloBasic, self).__init__(
            hostname=None,
            protocol_versions=[protocol_version, ],
            cipher_suites=list(TlsCipherSuite),
            elliptic_curves=[],
            signature_algorithms=[],
            extensions=[]
        )


@attr.s
class L7ClientTlsBase(L7TransferBase):
    l4_transfer = attr.ib(init=False, default=None)

    @classmethod
    @abc.abstractmethod
    def get_scheme(cls):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def get_default_port(cls):
        raise NotImplementedError()

    def _init_connection(self):
        self.l4_transfer = L4ClientTCP(self.address, self.port, self.timeout, self.ip)
        self.l4_transfer.init_connection()

    def _do_handshake(
            self,
            tls_client,
            hello_message,
            record_version,
            last_handshake_message_type
    ):
        self.init_connection()

        try:
            tls_client.do_handshake(self, hello_message, record_version, last_handshake_message_type)
        finally:
            self._close_connection()

        return tls_client.server_messages

    def do_ssl_handshake(self, hello_message, last_handshake_message_type=SslMessageType.SERVER_HELLO):
        return self._do_handshake(
            SslClientHandshake(),
            hello_message,
            SslVersion.SSL2,
            last_handshake_message_type
        )

    def do_tls_handshake(
            self,
            hello_message,
            record_version=TlsProtocolVersionFinal(TlsVersion.TLS1_0),
            last_handshake_message_type=TlsHandshakeType.SERVER_HELLO
    ):
        return self._do_handshake(
            TlsClientHandshake(),
            hello_message,
            record_version,
            last_handshake_message_type
        )


@attr.s
class L7ClientStartTlsBase(L7ClientTlsBase):
    _l7_client = attr.ib(init=False, default=None)
    _tls_inititalized = attr.ib(init=False, default=False)

    @classmethod
    @abc.abstractmethod
    def get_scheme(cls):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def get_default_port(cls):
        raise NotImplementedError()

    @abc.abstractmethod
    def _init_l7(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def _deinit_l7(self):
        raise NotImplementedError()

    def _init_connection(self):
        self.l4_transfer = L4ClientTCP(self.address, self.port, self.timeout, self.ip)

        self._init_l7()
        self._tls_inititalized = True

    def _close_connection(self):
        if self._l7_client is not None and not self._tls_inititalized:
            self._deinit_l7()
        self.l4_transfer.close()


class L7ClientTls(L7ClientTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'tls'

    @classmethod
    def get_default_port(cls):
        return 443


class L7ClientHTTPS(L7ClientTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'https'

    @classmethod
    def get_default_port(cls):
        return 443


class L7ClientDoH(L7ClientTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'doh'

    @classmethod
    def get_default_port(cls):
        return 443


class L7ClientPOP3S(L7ClientTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'pop3s'

    @classmethod
    def get_default_port(cls):
        return 995


@attr.s
class ClientPOP3(L7ClientStartTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'pop3'

    @classmethod
    def get_default_port(cls):
        return 110

    def _init_l7(self):
        try:
            self._l7_client = poplib.POP3(self.ip, self.port, self.timeout)
            self.l4_transfer.init_connection(self._l7_client.sock)

            response = self._l7_client._shortcmd('STLS')  # pylint: disable=protected-access
            if len(response) < 3 or response[:3] != b'+OK':
                raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)
        except poplib.error_proto as e:
            six.raise_from(SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY), e)

    def _deinit_l7(self):
        try:
            self._l7_client.quit()
        except poplib.error_proto:
            self.l4_transfer.close()


class L7ClientSMTPS(L7ClientTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'smtps'

    @classmethod
    def get_default_port(cls):
        return 465


class ClientSMTP(L7ClientStartTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'smtp'

    @classmethod
    def get_default_port(cls):
        return 587

    def _init_l7(self):
        try:
            self._l7_client = smtplib.SMTP(timeout=self.timeout)
            self._l7_client.connect(self.ip, self.port)
            self.l4_transfer.init_connection(self._l7_client.sock)

            self._l7_client.ehlo()
            if not self._l7_client.has_extn('STARTTLS'):
                raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)
            response, _ = self._l7_client.docmd('STARTTLS')
            if response != 220:
                raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)
        except smtplib.SMTPException as e:
            six.raise_from(SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY), e)

    def _deinit_l7(self):
        try:
            self._l7_client.quit()
        except smtplib.SMTPServerDisconnected:
            pass


class L7ClientIMAPS(L7ClientTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'imaps'

    @classmethod
    def get_default_port(cls):
        return 993


class IMAP4(imaplib.IMAP4, object):
    def __init__(self, host, port, timeout):
        self.timeout = timeout
        super(IMAP4, self).__init__(host, port)

    def open(self, *args, **kwargs):  # pylint: disable=arguments-differ,signature-differs,unused-argument
        self.host = args[0]
        self.port = args[1]
        self.sock = socket.create_connection((self.host, self.port), self.timeout)
        self.file = self.sock.makefile('rb')


class ClientIMAP(L7ClientStartTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'imap'

    @classmethod
    def get_default_port(cls):
        return 143

    @property
    def _capabilities(self):
        return self._l7_client.capabilities

    def _init_l7(self):
        try:
            self._l7_client = IMAP4(self.ip, self.port, self.timeout)
            self.l4_transfer.init_connection(self._l7_client.socket())

            if 'STARTTLS' not in self._capabilities:
                raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)
            response, _ = self._l7_client.xatom('STARTTLS')
            if response != 'OK':
                raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)
        except imaplib.IMAP4.error as e:
            six.raise_from(SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY), e)

    def _deinit_l7(self):
        try:
            self._l7_client.shutdown()
        except IMAP4.error:
            pass


class L7ClientFTPS(L7ClientTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'ftps'

    @classmethod
    def get_default_port(cls):
        return 990


class ClientFTP(L7ClientStartTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'ftp'

    @classmethod
    def get_default_port(cls):
        return 21

    def _init_l7(self):
        try:
            self._l7_client = ftplib.FTP()
            response = self._l7_client.connect(self.address, self.port, self.timeout)
            self.l4_transfer.init_connection(self._l7_client.sock)
            if not response.startswith('220'):
                raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)

            response = self._l7_client.sendcmd('AUTH TLS')
            if not response.startswith('234'):
                raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)
        except ftplib.all_errors as e:
            six.raise_from(SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY), e)

    def _deinit_l7(self):
        try:
            self._l7_client.quit()
        except ftplib.all_errors:
            pass


@attr.s
class ClientRDP(L7ClientStartTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'rdp'

    @classmethod
    def get_default_port(cls):
        return 3389

    def _init_l7(self):
        try:
            self._l7_client = L7ClientTls(self.address, self.port, self.timeout)
            self._l7_client.init_connection()
            self.l4_transfer = self._l7_client.l4_transfer

            neg_req = RDPNegotiationRequest([], [RDPProtocol.SSL, ])
            cotp = COTPConnectionRequest(src_ref=0, user_data=neg_req.compose())
            tpkt = TPKT(version=3, message=cotp.compose())
            request_bytes = tpkt.compose()
            self.l4_transfer.send(request_bytes)

            self.l4_transfer.receive(len(request_bytes))
            tpkt = TPKT.parse_exact_size(self.l4_transfer.buffer)
            cotp = COTPConnectionConfirm.parse_exact_size(tpkt.message)
            neg_rsp = RDPNegotiationResponse.parse_exact_size(cotp.user_data)
            self.l4_transfer.flush_buffer(len(request_bytes))
        except socket.timeout as e:
            six.raise_from(SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY), e)
        except (InvalidValue, InvalidType) as e:
            six.raise_from(SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY), e)

        if RDPProtocol.SSL not in neg_rsp.protocol:
            raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)

    def _deinit_l7(self):
        pass


@attr.s
class ClientXMPP(L7ClientStartTlsBase):
    _STREAM_OPEN = (
        '<stream:stream xmlns=\'jabber:client\' xmlns:stream=\'http://etherx.jabber.org/streams\' '
        'xmlns:tls=\'http://www.ietf.org/rfc/rfc2595.txt\' to=\'{}\' xml:lang=\'en\' version=\'1.0\'>'
    )
    _STARTTLS = b'<starttls xmlns=\'urn:ietf:params:xml:ns:xmpp-tls\'/>'

    @classmethod
    def get_scheme(cls):
        return 'xmpp'

    @classmethod
    def get_default_port(cls):
        return 5222

    @staticmethod
    def _init_xmpp(l4_transfer, address):
        stream_open_message = ClientXMPP._STREAM_OPEN.format(address).encode("utf-8")
        l4_transfer.send(stream_open_message)

        l4_transfer.receive_until(b'<stream:')
        l4_transfer.receive_until(b'>')

        if b'stream:error' in l4_transfer.buffer:
            raise NetworkError(NetworkErrorType.NO_RESPONSE)

        if b'stream:features' not in l4_transfer.buffer:
            l4_transfer.receive_until(b'</stream:features>')

        if b'<starttls xmlns=\'urn:ietf:params:xml:ns:xmpp-tls\'>' not in l4_transfer.buffer:
            raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)

        l4_transfer.flush_buffer()

        l4_transfer.send(ClientXMPP._STARTTLS)
        l4_transfer.receive_until(b'>')

        if b'stream:error' in l4_transfer.buffer:
            raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)

        if l4_transfer.buffer != b'<proceed xmlns=\'urn:ietf:params:xml:ns:xmpp-tls\'/>':
            raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)

        l4_transfer.flush_buffer()

    def _init_l7(self):
        self._l7_client = L7ClientTls(self.address, self.port, self.timeout)
        self._l7_client.init_connection()
        self.l4_transfer = self._l7_client.l4_transfer

        try:
            self._init_xmpp(self.l4_transfer, self.address)
        except NotEnoughData as e:
            six.raise_from(NetworkError(NetworkErrorType.NO_RESPONSE), e)

    def _deinit_l7(self):
        pass


class L7ClientLDAPS(L7ClientTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'ldaps'

    @classmethod
    def get_default_port(cls):
        return 636


@attr.s
class ClientLDAP(L7ClientStartTlsBase):
    @classmethod
    def get_scheme(cls):
        return 'ldap'

    @classmethod
    def get_default_port(cls):
        return 389

    def _init_l7(self):
        try:
            self._l7_client = L7ClientTls(self.address, self.port, self.timeout)
            self._l7_client.init_connection()
            self.l4_transfer = self._l7_client.l4_transfer

            request_bytes = LDAPExtendedRequestStartTLS().compose()
            self.l4_transfer.send(request_bytes)

            try:
                self.l4_transfer.receive(LDAPExtendedResponseStartTLS.HEADER_SIZE)
                LDAPExtendedResponseStartTLS.parse_immutable(self.l4_transfer.buffer)
            except NotEnoughData as e:
                header_size = LDAPExtendedResponseStartTLS.HEADER_SIZE
                header_not_received = header_size - len(self.l4_transfer.buffer) == e.bytes_needed
                if header_not_received:
                    self._close_connection()
                    raise e

                self.l4_transfer.receive(e.bytes_needed)

            ext_response, parsed_length = LDAPExtendedResponseStartTLS.parse_immutable(self.l4_transfer.buffer)
            self.l4_transfer.flush_buffer(parsed_length)
        except socket.timeout as e:
            six.raise_from(SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY), e)
        except (InvalidValue, InvalidType) as e:
            six.raise_from(SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY), e)

        if ext_response.result_code != LDAPResultCode.SUCCESS:
            raise SecurityError(SecurityErrorType.UNSUPPORTED_SECURITY)

    def _deinit_l7(self):
        pass


class TlsClient(object):
    _last_processed_message_type = attr.ib(init=False, default=None)
    server_messages = attr.ib(init=False, default={})

    @staticmethod
    def raise_response_error(transfer):
        response_is_plain_text = transfer.buffer and transfer.buffer_is_plain_text
        transfer.flush_buffer()

        if response_is_plain_text:
            raise SecurityError(SecurityErrorType.PLAIN_TEXT_MESSAGE)

        raise SecurityError(SecurityErrorType.UNPARSABLE_MESSAGE)

    @abc.abstractmethod
    def do_handshake(self, transfer, hello_message, record_version, last_handshake_message_type):
        raise NotImplementedError()


class TlsClientHandshake(TlsClient):
    def _process_message(self, handshake_message, protocol_version):
        handshake_type = handshake_message.get_handshake_type()
        if handshake_type in self.server_messages:
            raise TlsAlert(TlsAlertDescription.UNEXPECTED_MESSAGE)
        if (handshake_type == TlsHandshakeType.SERVER_HELLO and
                not handshake_message.protocol_version == protocol_version):
            raise TlsAlert(TlsAlertDescription.PROTOCOL_VERSION)

    def do_handshake(
            self,
            transfer,
            hello_message,
            record_version=TlsProtocolVersionFinal(TlsVersion.SSL3),
            last_handshake_message_type=TlsHandshakeType.SERVER_HELLO_DONE
    ):
        self.server_messages = {}
        self._last_processed_message_type = None

        tls_record = TlsRecord([hello_message, ], record_version)
        transfer.send(tls_record.compose())

        while True:
            try:
                record = TlsRecord.parse_exact_size(transfer.buffer)
                transfer.flush_buffer()

                if record.content_type == TlsContentType.ALERT:
                    if (record.messages[0].level == TlsAlertLevel.FATAL or
                            record.messages[0].description == TlsAlertDescription.CLOSE_NOTIFY):
                        raise TlsAlert(record.messages[0].description)

                    transfer.flush_buffer()
                    continue

                if record.content_type != TlsContentType.HANDSHAKE:
                    raise TlsAlert(TlsAlertDescription.UNEXPECTED_MESSAGE)
                for handshake_message in record.messages:
                    self._process_message(handshake_message, hello_message.protocol_version)
                    self._last_processed_message_type = handshake_message.get_handshake_type()
                    self.server_messages[self._last_processed_message_type] = handshake_message

                    if self._last_processed_message_type == last_handshake_message_type:
                        return

                receivable_byte_num = 0
            except NotEnoughData as e:
                receivable_byte_num = e.bytes_needed
            except (InvalidType, InvalidValue):
                self.raise_response_error(transfer)

            try:
                transfer.receive(receivable_byte_num)
            except NotEnoughData as e:
                if transfer.buffer:
                    six.raise_from(NetworkError(NetworkErrorType.NO_CONNECTION), e)

                six.raise_from(NetworkError(NetworkErrorType.NO_RESPONSE), e)


@attr.s
class SslError(ValueError):
    error = attr.ib()


class SslHandshakeClientHelloAnyAlgorithm(SslHandshakeClientHello):
    def __init__(self):
        super(SslHandshakeClientHelloAnyAlgorithm, self).__init__(
            cipher_kinds=list(SslCipherKind)
        )


class SslClientHandshake(TlsClient):
    def do_handshake(
            self,
            transfer,
            hello_message=None,
            record_version=SslVersion.SSL2,
            last_handshake_message_type=SslMessageType.SERVER_HELLO
    ):
        ssl_record = SslRecord(hello_message)
        transfer.send(ssl_record.compose())

        self.server_messages = {}
        while True:
            try:
                record = SslRecord.parse_exact_size(transfer.buffer)
                transfer.flush_buffer()
                if record.message.get_message_type() == SslMessageType.ERROR:
                    raise SslError(record.message.error_type)

                self._last_processed_message_type = record.message.get_message_type()
                self.server_messages[self._last_processed_message_type] = record.message
                if self._last_processed_message_type == last_handshake_message_type:
                    break

                receivable_byte_num = 0
            except NotEnoughData as e:
                receivable_byte_num = e.bytes_needed
            except (InvalidType, InvalidValue, TooMuchData):
                self.raise_response_error(transfer)

            try:
                transfer.receive(receivable_byte_num)
            except NotEnoughData as e:
                if transfer.buffer:
                    try:
                        tls_record = TlsRecord.parse_exact_size(transfer.buffer)
                        transfer.flush_buffer()
                    except (InvalidType, InvalidValue):
                        self.raise_response_error(transfer)
                    else:
                        if (tls_record.content_type == TlsContentType.ALERT and
                                (tls_record.messages[0].description in [
                                    TlsAlertDescription.PROTOCOL_VERSION,
                                    TlsAlertDescription.HANDSHAKE_FAILURE,
                                    TlsAlertDescription.CLOSE_NOTIFY,
                                    TlsAlertDescription.INTERNAL_ERROR,
                                ])):
                            six.raise_from(NetworkError(NetworkErrorType.NO_RESPONSE), e)

                        six.raise_from(NetworkError(NetworkErrorType.NO_CONNECTION), e)
                else:
                    six.raise_from(NetworkError(NetworkErrorType.NO_RESPONSE), e)
