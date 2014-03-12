# This file is part of quichem.
#
# quichem is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# quichem is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with quichem.  If not, see <http://www.gnu.org/licenses/>.

"""Hacks for the ``modgrammar`` module to make it more Pythonic and
more structured.

"""

from __future__ import unicode_literals

from modgrammar import REF, Grammar, GrammarClass, Reference


__all__ = ['default', 'string', 'Token', 'g', 'ref']


def default(token, default):
    """Return a default value if a token is None."""
    return default if token is None else token


def string(token):
    """Access ``.string`` on a token if the token is not None.
    Otherwise return None.

    Use this function to avoid the need to check whether ``.find``
    returns None.

    """
    return token if token is None else token.string


class Token(object):

    """Abstract """

    @classmethod
    def from_attributes(cls, **kw):
        """Create a Token instance with the provided instance
        variables.

        Returns
        -------
        A new Token instance.

        """
        instance = cls()
        for key, value in kw.items():
            setattr(instance, key, value)
        return instance

    def grammar_init(self):
        """Initialize instance variables based on grammar results.

        Called when a grammar element corresponding to this token
        finds a match.

        Must be implemented in subclasses.

        Notes
        -----
        Due to the way this function is implemented, the grammar is
        not passed as a parameter. All methods and attributes
        belonging to the grammar will also belong to `self`.

        """
        raise NotImplementedError


def g(grammar, name, token=None, desc=None):
    """Constructs a grammar class that doubles as the given token.

    This means that the object in the grammar's resulting syntax tree
    will be accessible as if it were an instance of the provided
    token.

    Parameters
    ----------
    grammar : modgrammar.Grammar
        The grammar to associate `token` with.
    name : string
        The name of the resulting grammar, accessible as a tag when
        using `modgrammar.Grammar.find` et al.
    token : Token
        A token class to be associated with `grammar`.
    desc : string
        The description (user-visible name)  of the resulting grammar.
        If not given, defaults to `name`.

    Returns
    -------
    A ``modgrammar`` Grammar class.

    See Also
    --------
    Token.grammar_init

    Notes
    -----

    Motivation
    ++++++++++
    The reasoning behind this function was to allow for both runtime
    parse actions as well as organized code. ``modgrammar``
    combines matching functionality and parse action functionality
    into a single grammar class, which I believe violates the single
    responsibility principle. This function allows parse actions to
    be created as separate classes from the grammar classes.

    By allowing `token` to be optional, named grammars can be created
    without having to define a class for each.

    Implementation
    ++++++++++++++
    While an ideal implementation of parse actions would allow for
    creating a syntax tree based on values returned from a parse
    action function, this is not possible here. Instead, we create
    a subclass of both `token` and `modgrammar.Grammar`. We then
    map grammar_elem_init to `Token.grammar_init` so that the
    grammar class can be dynamically manipulated by another class.

    """
    grammar_ = grammar
    parents = (Grammar,) if token is None else (token, Grammar)

    class G(*parents):
        grammar = grammar_
        grammar_tags = (name,)
        grammar_desc = name if desc is None else desc
        if token is not None:
            def grammar_elem_init(self, sessiondata):
                self.grammar_init()

    return G


class _FunctionReference(Reference):

    """Used to implement `ref`. Functionally equivalent to
    `modgrammar.Reference`, but `resolve` does no dynamic lookup and
    resolves by calling `ref_name`.

    """

    @classmethod
    def resolve(cls, sessiondata={}):
        return cls.ref_name()


def ref(function):
    """Equivalent to `modgrammar.REF`, but rather than taking a
    string, take a function that returns the grammar object.

    This eliminates the need for dynamic class lookup with strings.
    Note that `modgrammar.Grammar.grammar_resolve_refs` can still be
    called to resolve references before parse time.

    Returns
    -------
    A reference grammar object that points to the grammar object
    returned by `function`.

    """
    reference = GrammarClass(
        "<REF>", (_FunctionReference,), dict(ref_name=staticmethod(function)))
    return reference
