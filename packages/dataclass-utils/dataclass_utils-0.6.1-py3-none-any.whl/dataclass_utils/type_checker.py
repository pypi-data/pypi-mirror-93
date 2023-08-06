import dataclasses
from typing import (
    Any,
    AnyStr,
    Dict,
    FrozenSet,
    Generic,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)
import typing

from dataclass_utils.error import Error, type_error

Result = Optional[Error]  # returns error context


def check(value: Any, ty: Type) -> Result:
    """

    # Examples

    >>> assert is_error(check(1, str))
    >>> assert not is_error(check(1, int))
    >>> assert is_error(check(1, list))
    >>> assert is_error(check(1.3, int))
    >>> assert is_error(check(1.3, Union[str, int]))
    """
    if isinstance(ty, type):
        if ty is int:  # For boolean
            if type(value) is not ty:
                return Error(ty, value)
        elif not isinstance(value, ty):
            return Error(ty, value)

    if ty is AnyStr:
        err = check_anystr(value, ty)
        if is_error(err):
            return err

    if (to := typing.get_origin(ty)) is not None:  # generics
        err = check(value, to)
        if is_error(err):
            return err

        if to is list or to is set or to is frozenset:
            err = check_mono_container(value, ty)
        elif to is dict:
            err = check_dict(value, ty)
        elif to is tuple:
            err = check_tuple(value, ty)
        elif to is Literal:
            err = check_literal(value, ty)
        elif to is Union:
            err = check_union(value, ty)

        if is_error(err):
            return err

    if dataclasses.is_dataclass(value):
        err = check_dataclass(value, ty)
        if is_error(err):
            return err
    return None


def check_anystr(value: Any, ty: Type) -> Result:
    if all(not isinstance(value, t) for t in ty.__constraints__):
        return Error(ty=ty, value=value)
    return None


def check_literal(value: Any, ty: Type) -> Result:
    if all(value != t for t in typing.get_args(ty)):
        return Error(ty=ty, value=value)
    return None


def check_tuple(value: Any, ty: Type[Tuple]) -> Result:
    types = typing.get_args(ty)
    if len(value) != len(types):
        return Error(ty=ty, value=value)
    for v, t in zip(value, types):
        err = check(v, t)
        if is_error(err):
            return err
    return None


def check_union(value: Any, ty) -> Result:
    if any(not is_error(check(value, t)) for t in typing.get_args(ty)):
        return None
    return Error(ty=ty, value=value)


def check_mono_container(
    value: Any, ty: Union[Type[List], Type[Set], Type[FrozenSet]]
) -> Result:
    ty_item = typing.get_args(ty)[0]
    for v in value:
        err = check(v, ty_item)
        if is_error(err):
            return err
    return None


def check_dict(value: Dict, ty: Type[Dict]) -> Result:
    args = typing.get_args(ty)
    ty_key = args[0]
    ty_item = args[1]
    for k, v in value.items():
        err = check(k, ty_key)
        if is_error(err):
            return err
        err = check(v, ty_item)
        if is_error(err):
            err.path.append(k)
            return err
    return None


def check_dataclass(value: Any, ty: Type) -> Result:
    for k, ty in typing.get_type_hints(ty).items():
        v = getattr(value, k)
        err = check(v, ty)
        if err is not None:
            err.path.append(k)
            return err
    return None


def is_typevar(ty: Type) -> bool:
    return isinstance(ty, TypeVar)


def is_error(ret: Result) -> bool:
    return ret is not None


def check_root(value: Any):
    """Check dataclass type recursively"""
    err = check_dataclass(value, type(value))
    if err is not None:
        raise type_error(err)
