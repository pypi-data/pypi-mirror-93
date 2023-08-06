# -*- coding: utf-8 -*-
#
# This class was auto-generated from the API references found at
# https://support.direct.ingenico.com/documentation/api/reference/
#
from ingenico.direct.sdk.data_object import DataObject
from ingenico.direct.sdk.domain.fraud_results import FraudResults
from ingenico.direct.sdk.domain.payment_product771_specific_output import PaymentProduct771SpecificOutput


class SepaDirectDebitPaymentMethodSpecificOutput(DataObject):
    """
    | Object containing the SEPA direct debit details
    """

    __fraud_results = None
    __payment_product771_specific_output = None
    __payment_product_id = None

    @property
    def fraud_results(self):
        """
        | Object containing the results of the fraud screening

        Type: :class:`ingenico.direct.sdk.domain.fraud_results.FraudResults`
        """
        return self.__fraud_results

    @fraud_results.setter
    def fraud_results(self, value):
        self.__fraud_results = value

    @property
    def payment_product771_specific_output(self):
        """
        Type: :class:`ingenico.direct.sdk.domain.payment_product771_specific_output.PaymentProduct771SpecificOutput`
        """
        return self.__payment_product771_specific_output

    @payment_product771_specific_output.setter
    def payment_product771_specific_output(self, value):
        self.__payment_product771_specific_output = value

    @property
    def payment_product_id(self):
        """
        | Payment product identifier - Please see [payment products](https://support.direct.ingenico.com/documentation/api/reference/index.html#tag/Products) for a full overview of possible values.

        Type: int
        """
        return self.__payment_product_id

    @payment_product_id.setter
    def payment_product_id(self, value):
        self.__payment_product_id = value

    def to_dictionary(self):
        dictionary = super(SepaDirectDebitPaymentMethodSpecificOutput, self).to_dictionary()
        if self.fraud_results is not None:
            dictionary['fraudResults'] = self.fraud_results.to_dictionary()
        if self.payment_product771_specific_output is not None:
            dictionary['paymentProduct771SpecificOutput'] = self.payment_product771_specific_output.to_dictionary()
        if self.payment_product_id is not None:
            dictionary['paymentProductId'] = self.payment_product_id
        return dictionary

    def from_dictionary(self, dictionary):
        super(SepaDirectDebitPaymentMethodSpecificOutput, self).from_dictionary(dictionary)
        if 'fraudResults' in dictionary:
            if not isinstance(dictionary['fraudResults'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['fraudResults']))
            value = FraudResults()
            self.fraud_results = value.from_dictionary(dictionary['fraudResults'])
        if 'paymentProduct771SpecificOutput' in dictionary:
            if not isinstance(dictionary['paymentProduct771SpecificOutput'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['paymentProduct771SpecificOutput']))
            value = PaymentProduct771SpecificOutput()
            self.payment_product771_specific_output = value.from_dictionary(dictionary['paymentProduct771SpecificOutput'])
        if 'paymentProductId' in dictionary:
            self.payment_product_id = dictionary['paymentProductId']
        return self
