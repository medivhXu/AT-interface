#!/usr/bin/env python3

import abc


class DB(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def select(self, sql: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def select_all(self, sql: str) -> tuple:
        raise NotImplementedError

    @abc.abstractmethod
    def insert(self, sql: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, sql: str) -> bool:
        raise NotImplementedError
