""" Create dependencies from existing code """
from __future__ import annotations

from inspect import isclass
from typing import Union, Callable, Container, Optional
from typing import get_type_hints

from apiens.util import decomarker
from .const import MISSING
from .defs import InjectionToken, Dependency, Resolvable
from ..util.decomarker import Self_T


def signature(*include, exclude: Container[str] = None) -> Callable[[Callable], resolvable_marker]:
    """ Read dependencies from the function's signature. Every typed variable becomes a dependency.

    Example:

        from apiens import di

        @di.signature(exclude=['user'])
        def save_user(user, db_session: DbSession):
            db_session.save(user)

        ...

        injector = di.Injector()
        injector.provide(DbSession, get_session)  # a function
        injector.invoke(save_user)

    Args:
        *include: Argument names to include. All other arguments will be ignored.
        exclude: Argument names to exclude.
    """
    # Make a decorator that will receive the function and read its signature
    def decorator(func) -> resolvable_marker:
        # Read a resolvable from the function
        resolvable = resolvable_from_function_signature(
            func,
            include_only_names=set(include) if include else None,
            exclude_names=set(exclude) if exclude else None,
        )

        # Start
        return resolvable_marker(resolvable).decorator(func)
    return decorator


def kwargs(**deps_kw: Union[InjectionToken, Dependency]) -> resolvable_marker:
    """ Describe the function's dependencies to be provided as keyword arguments

    Example:

        from apiens import di

        @di.kwargs(
            db_session=DbSession
            # Note that the `user` is not a dependency; it's an argument.
        )
        def save_user(user, db_session: DbSession):
            db_session.save(user)

    Args:
        **deps_kw: {kwarg name => injection-token}, or the complete Dependency object for fine-tuning
    """
    return resolvable_marker(Resolvable(
        func=MISSING,
        deps_kw={
            name: Dependency.ensure_dependency(dependency)
            for name, dependency in deps_kw.items()
        },
    ))


def depends(*deps_nopass) -> resolvable_marker:
    """ List the function's dependencies to be resolved but not passed as arguments

    Example:

        from apiens import di

        @di.signature()
        @di.depends('authenticated')  # not passed as an argument; just evaluated.
        def save_user(user, db_session: DbSession):
            db_session.save(user)

        ...

        injector.provide('authenticated', is_authenticated)
        injector.invoke(save_user)

    Args:
        **deps_nopass: injection tokens, or complete Dependency objects for fine-tuning
    """
    return resolvable_marker(Resolvable(
        func=MISSING,
        deps_nopass=[
            Dependency.ensure_dependency(dependency)
            for dependency in deps_nopass
        ]
    ))


class resolvable_marker(decomarker):
    """ A low-level decorator to describe a function's dependencies

    Example:

        @resolvable_marker(Resolvable(
            func=MISSING,
            deps_kw={
                'db_session': DbSession,
            }
        ))
        def save_user(user, db_session: DbSession):
            db_session.save(user)
    """

    resolvable: Resolvable

    def __init__(self, resolvable: Resolvable):
        super().__init__()
        self.resolvable = resolvable

        assert self.resolvable.func is MISSING  # the contract is to set it to MISSING because it's not yet known

    def decorator(self, func: Callable):
        # Bind the Resolvable to a function
        self.resolvable.func = func

        # Done
        return super().decorator(func)

    def _merge(self: Self_T, another: Self_T):
        self.resolvable.merge(another.resolvable)


def resolvable_from_function_signature(func: Callable,
                                       include_only_names: Optional[Container[str]],
                                       exclude_names: Optional[Container[str]],
                                       ) -> Resolvable:
    """ Read keyword dependencies from the function's signature and generate a Resolvable() """
    # If a class is given, use its constructor
    if isclass(func):
        func = func.__init__

    # Create a resolvable
    return Resolvable(
        func=MISSING,
        deps_kw={
            name: Dependency(token=type)
            for name, type in get_type_hints(func).items()
            if name != 'return' and
               (include_only_names is None or name in include_only_names) and
               (exclude_names is None or name not in exclude_names)
        }
    )
