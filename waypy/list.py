"""Compatibility linked-list module kept for older imports.

New code should use the public ``Agent`` API or the algorithm modules directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class No:
    """Backward-compatible node used by the original linked-list implementation."""

    pai: Any = None
    valor1: Any = None
    valor2: Any = None
    anterior: "No | None" = None
    proximo: "No | None" = None


class lista:
    """Small linked list preserved for compatibility with older user code."""

    def __init__(self):
        self.head: No | None = None
        self.tail: No | None = None

    def inserePrimeiro(self, v1, v2, p):
        node = No(p, v1, v2)
        if self.head is None:
            self.tail = node
        else:
            node.proximo = self.head
            self.head.anterior = node
        self.head = node

    def insereUltimo(self, v1, v2, p):
        node = No(p, v1, v2)
        if self.head is None:
            self.head = node
        else:
            self.tail.proximo = node
            node.anterior = self.tail
        self.tail = node

    def deletaPrimeiro(self):
        if self.head is None:
            return None

        node = self.head
        self.head = self.head.proximo
        if self.head is None:
            self.tail = None
        else:
            self.head.anterior = None
        return node

    def deletaUltimo(self):
        if self.tail is None:
            return None

        node = self.tail
        self.tail = self.tail.anterior
        if self.tail is None:
            self.head = None
        else:
            self.tail.proximo = None
        return node

    def primeiro(self):
        return self.head

    def ultimo(self):
        return self.tail

    def vazio(self):
        return self.head is None

    def exibeLista(self):
        values = []
        current = self.head
        while current is not None:
            values.append([current.valor1, current.valor2])
            current = current.proximo
        return values

    def exibeCaminho(self):
        current = self.tail
        path = []
        while current is not None:
            path.append(current.valor1)
            current = current.pai
        return list(reversed(path))

    def exibeCaminho1(self, valor):
        current = self.head
        while current is not None and current.valor1 != valor:
            current = current.proximo
        if current is None:
            return []

        path = []
        current = current.pai
        while current is not None:
            path.append(current.valor1)
            current = current.pai
        return path
