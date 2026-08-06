class BillingException(Exception):
    """
    Base exception for the billing module.
    """
    def __init__(self, message: str):
        super().__init__(message)


class PaystackException(BillingException):
    """
    Base exception for Paystack-related errors.
    """
    pass


class PaystackInitializationError(PaystackException):
    """
    Raised when Paystack fails to initialize a transaction.
    """
    pass


class PaystackVerificationError(PaystackException):
    """
    Raised when Paystack verification fails.
    """
    pass


class PaymentProcessingError(BillingException):
    """
    Raised when a verified payment cannot be processed.
    """
    pass