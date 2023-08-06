# -*- coding: utf-8 -*-

import abc
import glob
import importlib
import ipaddress
import pkgutil
import os

from cryptoparser.common.base import Serializable
from cryptoparser.common.utils import get_leaf_classes

from cryptoparser.tls.subprotocol import TlsAlertDescription

from cryptolyzer.tls.client import L7ClientTlsBase


class ProtocolHandlerBase(object):
    @classmethod
    def import_plugins(cls):
        plugin_root_dir_parts = __file__.split(os.path.sep)[:-2]  # remove common/analyzer.py
        plugin_module_dir_parts = set()
        plugin_paths = filter(
            lambda path: path != __file__,
            glob.iglob(os.path.sep.join(plugin_root_dir_parts + ['*', 'analyzer.py']))
        )
        for path in plugin_paths:
            plugin_path_parts = path.split(os.path.sep)[-3:-1]  # split plugin dirs
            for index in range(len(plugin_path_parts)):
                plugin_module_dir_parts.add('.'.join(plugin_path_parts[:index + 1]))

        plugin_module_dir_parts = list(plugin_module_dir_parts)
        plugin_module_dir_parts.sort(key=len)
        for plugins_dir in plugin_module_dir_parts:
            ns_pkg = importlib.import_module(plugins_dir, package=None)
            for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
                if name.endswith('.analyzer'):
                    importlib.import_module(name)

    @classmethod
    def from_protocol(cls, protocol):
        cls.import_plugins()

        for handler_class in get_leaf_classes(cls):
            if handler_class.get_protocol() == protocol:
                return handler_class()
        raise KeyError(protocol)

    @classmethod
    def get_protocols(cls):
        cls.import_plugins()

        for handler_class in get_leaf_classes(cls):
            yield handler_class.get_protocol()

    @classmethod
    @abc.abstractmethod
    def get_protocol(cls):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def get_analyzers(cls):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def _get_analyzer_args(cls):
        raise NotImplementedError()

    @classmethod
    def _l7_client_from_uri(cls, uri):
        kwargs = {'scheme': uri.scheme, 'address': uri.host}

        if uri.port:
            kwargs['port'] = int(uri.port)
        if uri.fragment:
            try:
                ipaddress.ip_address(uri.fragment)
            except ValueError:
                pass
            else:
                kwargs['ip'] = uri.fragment

        for analyzer_class in cls.get_analyzers():
            for client_class in analyzer_class.get_clients():
                if client_class.get_scheme() == uri.scheme:
                    return client_class.from_scheme(**kwargs)

        raise NotImplementedError()

    def analyze(self, analyzer, uri):
        l7_client = self._l7_client_from_uri(uri)
        args, kwargs = self._get_analyzer_args()
        return analyzer.analyze(l7_client, *args, **kwargs)

    @classmethod
    def analyzer_from_name(cls, name):
        analyzer_list = [
            analyzer_class
            for analyzer_class in cls.get_analyzers()
            if analyzer_class.get_name() == name
        ]

        if len(analyzer_list) != 1:
            raise ValueError  # pragma: no cover

        return analyzer_list[0]()


class AnalyzerBase(object):
    @classmethod
    @abc.abstractmethod
    def get_name(cls):
        raise NotImplementedError()

    @abc.abstractmethod
    def analyze(self, analyzable):
        raise NotImplementedError()


class AnalyzerResultBase(Serializable):
    pass


class AnalyzerTlsBase(object):
    _ACCEPTABLE_HANDSHAKE_FAILURE_ALERTS = [
        TlsAlertDescription.HANDSHAKE_FAILURE,  # no matching algorithms
        TlsAlertDescription.CLOSE_NOTIFY,  # no matching algorithms
        TlsAlertDescription.INSUFFICIENT_SECURITY,  # not enough secure matching algorithms
        TlsAlertDescription.ILLEGAL_PARAMETER  # unimplemented matching algorithms
    ]

    @classmethod
    def get_clients(cls):
        return list(get_leaf_classes(L7ClientTlsBase))

    @classmethod
    def get_default_scheme(cls):
        return 'tls'

    @abc.abstractmethod
    def analyze(self, analyzable, protocol_version):
        raise NotImplementedError()
