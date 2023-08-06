#
# This class was auto-generated from the API references found at
# https://support.direct.ingenico.com/documentation/api/reference/
#
from abc import ABCMeta, abstractmethod


class IProductsClient:
    """
    Products client interface. Thread-safe.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_payment_products(self, query, context=None):
        """
        Resource /v2/{merchantId}/products - Get payment products

        See also https://support.direct.ingenico.com/documentation/api/reference#operation/GetPaymentProducts

        :param query: :class:`ingenico.direct.sdk.merchant.products.get_payment_products_params.GetPaymentProductsParams`
        :param context: :class:`ingenico.direct.sdk.call_context.CallContext`
        :return: :class:`ingenico.direct.sdk.domain.get_payment_products_response.GetPaymentProductsResponse`
        :raise: ValidationException if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise: AuthorizationException if the request was not allowed (HTTP status code 403)
        :raise: ReferenceException if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise: DirectException if something went wrong at the Ingenico ePayments platform,
                   the Ingenico ePayments platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise: ApiException if the Ingenico ePayments platform returned any other error
        """
        pass

    @abstractmethod
    def get_payment_product(self, payment_product_id, query, context=None):
        """
        Resource /v2/{merchantId}/products/{paymentProductId} - Get payment product

        See also https://support.direct.ingenico.com/documentation/api/reference#operation/GetPaymentProduct

        :param payment_product_id: int
        :param query: :class:`ingenico.direct.sdk.merchant.products.get_payment_product_params.GetPaymentProductParams`
        :param context: :class:`ingenico.direct.sdk.call_context.CallContext`
        :return: :class:`ingenico.direct.sdk.domain.payment_product.PaymentProduct`
        :raise: ValidationException if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise: AuthorizationException if the request was not allowed (HTTP status code 403)
        :raise: ReferenceException if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise: DirectException if something went wrong at the Ingenico ePayments platform,
                   the Ingenico ePayments platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise: ApiException if the Ingenico ePayments platform returned any other error
        """
        pass

    @abstractmethod
    def get_product_directory(self, payment_product_id, query, context=None):
        """
        Resource /v2/{merchantId}/products/{paymentProductId}/directory - Get payment product directory

        See also https://support.direct.ingenico.com/documentation/api/reference#operation/GetProductDirectoryApi

        :param payment_product_id: int
        :param query: :class:`ingenico.direct.sdk.merchant.products.get_product_directory_params.GetProductDirectoryParams`
        :param context: :class:`ingenico.direct.sdk.call_context.CallContext`
        :return: :class:`ingenico.direct.sdk.domain.product_directory.ProductDirectory`
        :raise: ValidationException if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise: AuthorizationException if the request was not allowed (HTTP status code 403)
        :raise: ReferenceException if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise: DirectException if something went wrong at the Ingenico ePayments platform,
                   the Ingenico ePayments platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise: ApiException if the Ingenico ePayments platform returned any other error
        """
        pass

    @abstractmethod
    def get_payment_product_networks(self, payment_product_id, query, context=None):
        """
        Resource /v2/{merchantId}/products/{paymentProductId}/networks - Get payment product networks

        See also https://support.direct.ingenico.com/documentation/api/reference#operation/GetPaymentProductNetworks

        :param payment_product_id: int
        :param query: :class:`ingenico.direct.sdk.merchant.products.get_payment_product_networks_params.GetPaymentProductNetworksParams`
        :param context: :class:`ingenico.direct.sdk.call_context.CallContext`
        :return: :class:`ingenico.direct.sdk.domain.payment_product_networks_response.PaymentProductNetworksResponse`
        :raise: ValidationException if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise: AuthorizationException if the request was not allowed (HTTP status code 403)
        :raise: ReferenceException if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise: DirectException if something went wrong at the Ingenico ePayments platform,
                   the Ingenico ePayments platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise: ApiException if the Ingenico ePayments platform returned any other error
        """
        pass
