"""Common entities in subscription package
"""

from enum import Enum

class BillingCycleTenureType(Enum):
    # A trial billing cycle.
    TRIAL = 1
    # A regular billing cycle.
    REGULAR = 2
