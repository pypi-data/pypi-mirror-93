"""Transactions handler.

Usage examples:

- Default usage auto-applies all added operations.
```
with transaction() as ops:
    op = Operation(apply_fn=your_apply_fn, rollback_fn=your_rollback_fn)
    ops.add(op)
```

- We can disable auto-apply if necessary. In this case, the context manager
will check if some operations weren't applied at the end of the transaction.
```
op = None
with transaction(auto_apply=False) as ops:
    op = Operation(apply_fn=your_apply_fn, rollback_fn=your_rollback_fn)
    ops.add(create_user)
    op.apply()
```

"""

import itertools
from contextlib import contextmanager
from contextvars import ContextVar
from enum import Enum
from typing import Callable, Generic, Optional, TypeVar

try:
    from transaction import Transaction, TransactionManager  # noqa: WPS433 - nested import
    from transaction.interfaces import IDataManager  # noqa: WPS433 - nested import
    from transaction._manager import _new_transaction  # noqa: WPS436, WPS450, WPS433 - nested import
    from zope.interface import implementer  # noqa: WPS433 - nested import
except ImportError as exc:
    raise Exception('You need to install the `transaction` extra to use the transaction features') from exc


txns = ContextVar('txns', default=[])
id_counter = itertools.count()


class TransactionExt(Transaction):
    def _free(self):
        # We don't want to free any resources after a nested transaction is commited or aborted.
        # Otherwise the parent transaction won't be able to abort it.
        pass


class HierarchicalTransactionManager(TransactionManager):
    @property
    def transactions(self):
        # We store transactions of a hierarchie in a ContextVar to make sure
        # there are no conflicts in an async context.
        return txns.get()

    def __exit__(self, t, v, tb):
        super().__exit__(t, v, tb)
        self.transactions.pop()

    def begin(self):
        # We overload this method to remove a check and join child transactions
        # to the parent transaction as a resource.
        parent_transaction = self._txn
        txn = self._txn = TransactionExt(self._synchs, self)  # noqa: WPS429
        if parent_transaction is not None:
            # We wrap the transaction to give it the same interface as a resource, and link it
            # to the parent transaction. That way, the parent transaction will be able to abort its
            # child transactions if any of them fails.
            parent_transaction.join(TransactionResource(txn))
        _new_transaction(txn, self._synchs)
        return txn

    @property
    def _txn(self):
        if self.transactions:
            # Return the current transaction.
            return self.transactions[-1]
        return None

    @_txn.setter
    def _txn(self, value):
        if value is not None:
            self.transactions.append(value)


@contextmanager
def transaction(auto_apply: bool = True):
    manager = HierarchicalTransactionManager(explicit=True)

    with manager as txn:
        ops = OperationManager()
        txn.join(ops)

        yield ops

        if auto_apply:
            ops.apply()
        else:
            ops.ensure_applied()


class OperationState(Enum):
    pending = 'pending'
    applied = 'applied'
    errored = 'errored'
    reset = 'reset'


class InvalidState(Exception):
    ...


class OperationNotApplied(Exception):
    ...


T = TypeVar('T')

OperationApplyFn = Callable[[], Optional[T]]
OperationRollbackFn = Callable[[Optional[T]], None]


class Operation(Generic[T]):
    result: Optional[T]
    apply_fn: OperationApplyFn[T]
    rollback_fn: OperationRollbackFn[T]

    def __init__(self, apply_fn: OperationApplyFn[T], rollback_fn: OperationRollbackFn[T]):
        self.apply_fn = apply_fn
        self.rollback_fn = rollback_fn
        self.state = OperationState.pending
        self.result = None

    def apply(self):
        if self.state != OperationState.pending:
            raise InvalidState

        try:
            self.result = self.apply_fn()
            self.state = OperationState.applied
        except Exception as ex:
            self.state = OperationState.errored
            raise Exception('Failed to apply operation') from ex

    def rollback(self):
        if self.state != OperationState.applied:
            raise InvalidState

        self.rollback_fn(self.result)
        self.state = OperationState.reset


@implementer(IDataManager)
class OperationManager:  # noqa: WPS214 - too many methods
    def __init__(self):
        self.operations = []
        self._id = next(id_counter)

    def add(self, operation: Operation):
        self.operations.append(operation)

    def apply(self):
        for op in self.operations:
            op.apply()

    def abort(self, txn: Transaction):
        for op in reversed(self.operations):
            if op.state == OperationState.applied:
                op.rollback()

    def ensure_applied(self):
        for op in self.operations:
            if op.state != OperationState.applied:
                raise OperationNotApplied(op.state)

    def sortKey(self):  # noqa: N802
        return self._id

    # Methods under this comment are required as the `IDataManager` interface doesn't define any behavior
    # https://zope.readthedocs.io/en/latest/zdgbook/ComponentsAndInterfaces.html#zope-components

    def tpc_begin(self, txn):
        pass

    def tpc_vote(self, txn):
        pass

    def tpc_finish(self, txn):
        pass

    def commit(self, txn):
        pass


@implementer(IDataManager)
class TransactionResource:
    def __init__(self, txn: Transaction):
        self.txn = txn
        self._id = next(id_counter)

    def abort(self, txn: Transaction):
        self.txn.abort()

    def sortKey(self):  # noqa: N802
        return self._id

    def commit(self, txn: Transaction):
        pass

    def tpc_begin(self, txn):
        pass

    def tpc_vote(self, txn):
        pass

    def tpc_finish(self, txn):
        pass
