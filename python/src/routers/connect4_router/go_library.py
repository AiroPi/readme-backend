from __future__ import annotations

import os
from collections.abc import Sequence
from ctypes import CDLL, POINTER, Structure, c_longlong, c_uint8, c_void_p
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from connect4 import Connect4


_path = os.path.abspath("./golang/connect4img.so")

try:
    _lib = CDLL(_path, mode=0x8)
    print("Library loaded successfully!")
except OSError as e:
    print(f"Failed to load library: {e}")
    raise
except UnicodeDecodeError as e:
    print(f"Unicode decode error: {e}")
    raise


def _slice_type(type: type):
    class GoSlice(Structure):
        _fields_: ClassVar = [("data", POINTER(type)), ("len", c_longlong), ("cap", c_longlong)]

    return GoSlice


_GoIntSlice = _slice_type(c_void_p)
_GoIntSliceSlice = _slice_type(_GoIntSlice)


_lib.GenerateBoard.argtypes = [_GoIntSliceSlice, c_uint8, c_longlong, c_longlong, _GoIntSliceSlice]
_lib.GenerateBoard.restype = None


def _to_go_int_slice_slice(value: Sequence[Sequence[int]]):
    inner_length = len(value[0])
    if not all(len(row) == inner_length for row in value):
        raise ValueError("All rows must have the same length")

    rows = [_to_go_int_slice(row) for row in value]

    length = len(value)
    return _GoIntSliceSlice((_GoIntSlice * length)(*rows), length, length)


def _to_go_int_slice(value: Sequence[int]):
    length = len(value)
    return _GoIntSlice((c_void_p * length)(*value), length, length)


def _to_uint8(value: bool):
    return (c_uint8)(value)


def _to_longlong(value: int):
    return (c_longlong)(value)


def _connect4_export_types(c4: Connect4):
    board = _to_go_int_slice_slice([[p.value for p in row] for row in c4.board])

    is_over = _to_uint8(c4.is_over)
    winner = _to_longlong(-1 if c4.winner is None else c4.winner.value)
    turn = _to_longlong(c4.turn.value)

    win_points = c4._win_points  # type: ignore
    win_pos = len(win_points)
    winner_positions = _GoIntSliceSlice(
        (_GoIntSlice * win_pos)(*[_GoIntSlice((c_void_p * 2)(*xy), 2, 2) for xy in win_points]),
        win_pos,
        win_pos,
    )

    return board, is_over, winner, turn, winner_positions


def generate_board(c4: Connect4):
    _lib.GenerateBoard(*_connect4_export_types(c4))
