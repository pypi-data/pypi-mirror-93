import jpype
import base64
from enum import Enum
from . import Generation, Assist

#  ComplexBarcodeGenerator for backend complex barcode (e.g. SwissQR) images generation.
#
#  This sample shows how to create and save a SwissQR image.
#    swissQRCodetext = SwissQRCodetext(null);
#    swissQRCodetext.getBill().setAccount("Account");
#    swissQRCodetext.getBill().setBillInformation("BillInformation");
#    swissQRCodetext.getBill().setBillInformation("BillInformation");
#    swissQRCodetext.getBill().setAmount(1024);
#    swissQRCodetext.getBill().getCreditor().setName("Creditor.Name");
#    swissQRCodetext.getBill().getCreditor().setAddressLine1("Creditor.AddressLine1");
#    swissQRCodetext.getBill().getCreditor().setAddressLine2("Creditor.AddressLine2");
#    swissQRCodetext.getBill().getCreditor().setCountryCode("Nl");
#    swissQRCodetext.getBill().setUnstructuredMessage("UnstructuredMessage");
#    swissQRCodetext.getBill().setReference("Reference");
#    swissQRCodetext.getBill().addalternativeScheme(new AlternativeScheme("AlternativeSchemeInstruction1"));
#    swissQRCodetext.getBill().addalternativeScheme(new AlternativeScheme("AlternativeSchemeInstruction2"));
#    swissQRCodetext.getBill().setDebtor(new Address(null));
#    swissQRCodetext.getBill().getDebtor().setName("Debtor.Name");
#    swissQRCodetext.getBill().getDebtor().setAddressLine1("Debtor.AddressLine1");
#    swissQRCodetext.getBill().getDebtor().setAddressLine2("Debtor.AddressLine2");
#    swissQRCodetext.getBill().getDebtor().setCountryCode("Lux");
#    cg = ComplexBarcodeGenerator(swissQRCodetext);
#    res = cg.generateBarCodeImage();
class ComplexBarcodeGenerator(Assist.BaseJavaClass):
    javaClassName = "com.aspose.mw.barcode.complexbarcode.MwComplexBarcodeGenerator"
    parameters = None

    def init(self):
        self.parameters = Generation.BaseGenerationParameters(self.getJavaClass().getParameters())

    # Generation parameters.
    def getParameters(self):
        return self.parameters

    # Creates an instance of ComplexBarcodeGenerator.
    # @param arg Complex codetext
    def __init__(self, arg):
        super().__init__(ComplexBarcodeGenerator.initComplexBarcodeGenerator(arg))
        self.init()

    @staticmethod
    def initComplexBarcodeGenerator(arg):
        if isinstance(arg,  SwissQRCodetext):
            javaComplexBarcodeGenerator = jpype.JClass(ComplexBarcodeGenerator.javaClassName)
            return javaComplexBarcodeGenerator(arg.getJavaClass())
        else:
            java_link = jpype.JClass(arg)
            return java_link()

    # Generates complex barcode image under current settings.
    #
    # @param format_name image format name("PNG", "BMP", "JPEG", "GIF", "TIFF")
    # @return  Barcode image. See {@code Bitmap}.
    def generateBarcodeImage(self, format_name):
        base64Image = self.getJavaClass().generateBarCodeImage(format_name)
        return (base64Image)

    # Save barcode image to specific file in specific format.
    # @param filePath Path to save to.
    # @param format_name image format name("PNG", "BMP", "JPEG", "GIF", "TIFF")
    #
    # generator = BarCodeGenerator(EncodeTypes.CODE_128);
    # generator.save("file path", null);// if value = null, default image format PNG
    def save(self, filePath, format_name):
        base64Str = self.generateBarcodeImage(format_name)
        base64_bytes = base64.b64decode(base64Str)
        f = open(filePath, 'wb+')
        f.write(base64_bytes)
        f.close()

# Address of creditor or debtor.
#
# You can either set street, house number, postal code and town (type structured address)
# or address line 1 and 2 (type combined address elements). The type is automatically set
# once any of these fields is set. Before setting the fields, the address type is undetermined.
# If fields of both types are set, the address type becomes conflicting.
# Name and country code must always be set unless all fields are empty.
class Address(Assist.BaseJavaClass):
    javaClassName = "com.aspose.mw.barcode.complexbarcode.MwAddress"

    def __init__(self, arg):
        super().__init__(Address.initAddress(arg))
        self.init()

    @staticmethod
    def initAddress(arg):
        if (arg == None):
            javaAddress = jpype.JClass(Address.javaClassName)
            return javaAddress()
        return arg

    # Gets the address type.
    #
    # The address type is automatically set by either setting street / house number
    # or address line 1 and 2. Before setting the fields, the address type is Undetermined.
    # If fields of both types are set, the address type becomes Conflicting.
    #
    # Value: The address type.
    def getType(self):
        return self.getJavaClass().getType()

    # Gets the name, either the first and last name of a natural person or the
    # company name of a legal person.
    # Value: The name.
    def getName(self):
        return self.getJavaClass().getName()

    # Sets the name, either the first and last name of a natural person or the
    # company name of a legal person.
    # Value: The name.
    def setName(self, value):
        self.getJavaClass().setName(value)

    # Gets the address line 1.
    #
    # Address line 1 contains street name, house number or P.O. box.
    #
    # Setting this field sets the address type to AddressType.CombinedElements unless it's already
    # AddressType.Structured, in which case it becomes AddressType.Conflicting.
    #
    # This field is only used for combined elements addresses and is optional.
    #
    # Value: The address line 1.
    def getAddressLine1(self):
        return self.getJavaClass().getAddressLine1()

    # Sets the address line 1.
    #
    # Address line 1 contains street name, house number or P.O. box.
    #
    # Setting this field sets the address type to AddressType.CombinedElements unless it's already
    # AddressType.Structured, in which case it becomes AddressType.Conflicting.
    #
    # This field is only used for combined elements addresses and is optional.
    #
    # Value: The address line 1.
    def setAddressLine1(self, value):
        self.getJavaClass().setAddressLine1(value)

    # Gets the address line 2.
    # Address line 2 contains postal code and town.
    # Setting this field sets the address type to AddressType.CombinedElements unless it's already
    # AddressType.Structured, in which case it becomes AddressType.Conflicting.
    # This field is only used for combined elements addresses. For this type, it's mandatory.
    # Value: The address line 2.
    def getAddressLine2(self):
        return self.getJavaClass().getAddressLine2()

    # Sets the address line 2.
    # Address line 2 contains postal code and town.
    # Setting this field sets the address type to AddressType.CombinedElements unless it's already
    # AddressType.Structured, in which case it becomes AddressType.Conflicting.
    # This field is only used for combined elements addresses. For this type, it's mandatory.
    # Value: The address line 2.
    def setAddressLine2(self, value):
        self.getJavaClass().setAddressLine2(value)

    # Gets the street.
    # The street must be speicfied without house number.
    # Setting this field sets the address type to AddressType.Structured unless it's already
    # AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
    # This field is only used for structured addresses and is optional.
    # Value: The street.
    def getStreet(self):
        return self.getJavaClass().getStreet()

    # Sets the street.
    #
    # The street must be speicfied without house number.
    #
    # Setting this field sets the address type to AddressType.Structured unless it's already
    # AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
    #
    # This field is only used for structured addresses and is optional.
    #
    # Value: The street.
    def setStreet(self, value):
        self.getJavaClass().setStreet(value)

    # Gets the house number.
    #
    # Setting this field sets the address type to AddressType.Structured unless it's already
    # AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
    #
    # This field is only used for structured addresses and is optional.
    #
    # Value: The house number.
    def getHouseNo(self):
        return self.getJavaClass().getHouseNo()

    # Sets the house number.
    #
    # Setting this field sets the address type to AddressType.Structured unless it's already
    # AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
    #
    # This field is only used for structured addresses and is optional.
    #
    # Value: The house number.
    def setHouseNo(self, value):
        self.getJavaClass().setHouseNo(value)

    # Gets the postal code.
    #
    # Setting this field sets the address type to AddressType.Structured unless it's already
    # AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
    #
    # This field is only used for structured addresses. For this type, it's mandatory.
    #
    # Value: The postal code.
    def getPostalCode(self):
        return self.getJavaClass().getPostalCode()

    # Sets the postal code.
    #
    # Setting this field sets the address type to AddressType.Structured unless it's already
    # AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
    #
    # This field is only used for structured addresses. For this type, it's mandatory.
    #
    # Value: The postal code.
    def setPostalCode(self, value):
        self.getJavaClass().setPostalCode(value)

    # Gets the town or city.
    #
    # Setting this field sets the address type to AddressType.Structured unless it's already
    # AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
    #
    # This field is only used for structured addresses. For this type, it's mandatory.
    #
    # Value: The town or city.
    def getTown(self):
        return self.getJavaClass().getTown()

    # Sets the town or city.
    #
    # Setting this field sets the address type to AddressType.Structured unless it's already
    # AddressType.CombinedElements, in which case it becomes AddressType.Conflicting.
    #
    # This field is only used for structured addresses. For this type, it's mandatory.
    #
    # Value: The town or city.
    def setTown(self, value):
        self.getJavaClass().setTown(value)

    # Gets the two-letter ISO country code.
    #
    # The country code is mandatory unless the entire address contains null or emtpy values.
    #
    # Value: The ISO country code.
    def getCountryCode(self):
        return self.getJavaClass().getCountryCode()

    # Sets the two-letter ISO country code.
    #
    # The country code is mandatory unless the entire address contains null or emtpy values.
    #
    # Value: The ISO country code.
    def setCountryCode(self, value):
        self.getJavaClass().setCountryCode(value)

    # Clears all fields and sets the type to AddressType.Undetermined.
    def clear(self):
        self.setName(None)
        self.setAddressLine1(None)
        self.setaddressLine2(None)
        self.setStreet(None)
        self.setHouseNo(None)
        self.setPostalCode(None)
        self.setTown(None)
        self.setCountryCode(None)

    
    # Determines whether the specified object is equal to the current object.
    # @return true if the specified object is equal to the current object; otherwise, false.
    # @param obj The object to compare with the current object.
    def equals(self, obj):
        return self.getJavaClass().equals(obj)

    # Gets the hash code for this instance.
    # @return A hash code for the current object.
    def hashCode(self):
        return self.getJavaClass().hashCode()

    def init(self):
        return

# Address type
class AddressType(Enum):

    # Undetermined
    UNDETERMINED = 0

    # Structured address
    STRUCTURED = 1

    # Combined address elements
    COMBINED_ELEMENTS = 2

    # Conflicting
    CONFLICTING = 3

# Alternative payment scheme instructions
class AlternativeScheme(Assist.BaseJavaClass):
    javaClassName = "com.aspose.mw.barcode.complexbarcode.MwAlternativeScheme"

    def __init__(self, instruction):
        javaAlternativeScheme = jpype.JClass(AlternativeScheme.javaClassName)
        super().__init__(javaAlternativeScheme(instruction))

    # Gets the payment instruction for a given bill.
    #
    # The instruction consists of a two letter abbreviation for the scheme, a separator characters
    # and a sequence of parameters(separated by the character at index 2).
    #
    # Value: The payment instruction.
    def getInstruction(self):
        return self.getJavaClass().getInstruction()

    # Gets the payment instruction for a given bill.
    # The instruction consists of a two letter abbreviation for the scheme, a separator characters
    # and a sequence of parameters(separated by the character at index 2).
    # Value: The payment instruction.
    def setInstruction(self, value):
        self.getJavaClass().setInstruction(value)

    # Determines whether the specified object is equal to the current object.
    # @return true if the specified object is equal to the current object; otherwise, false.
    # @param obj The object to compare with the current object.
    def equals(self, obj):
        return self.getJavaClass().equals(obj)

    # Gets the hash code for this instance.
        # @return  hash code for the current object.
    def hashCode(self):
        return self.getJavaClass().hashCode()

    def init(self):
        return

#  ComplexCodetextReader decodes codetext to specified complex barcode type.
#
#  This sample shows how to recognize and decode SwissQR image.
#
#  cr = BarCodeReader("SwissQRCodetext.png", DecodeType.QR);
#  cr.read();
#  result = ComplexCodetextReader.tryDecodeSwissQR(cr.getCodeText(false));
class ComplexCodetextReader(Assist.BaseJavaClass):
    javaClassName = "com.aspose.mw.barcode.complexbarcode.MwComplexCodetextReader"

    # Decodes SwissQR codetext.
    #
    # @return decoded SwissQRCodetext or null.
    # @param encodedCodetext encoded codetext
    @staticmethod
    def tryDecodeSwissQR(encodedCodetext):
        javaPhpComplexCodetextReader = jpype.JClass(ComplexCodetextReader.javaClassName)
        return SwissQRCodetext(javaPhpComplexCodetextReader.tryDecodeSwissQR(encodedCodetext))

# SwissQR bill standard version
class QrBillStandardVersion(Enum):

    # Version 2.0
    V2_0 = 0


# SwissQR bill data
class SwissQRBill(Assist.BaseJavaClass):
    creditor = None
    debtor = None
    alternativeSchemes = None

    def init(self):
        self.creditor = Address(self.getJavaClass().getCreditor())
        self.debtor = Address(self.getJavaClass().getDebtor())
        self.alternativeSchemes = SwissQRBill.convertAlternativeSchemes(self.getJavaClass().getAlternativeSchemes())

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    @staticmethod
    def convertAlternativeSchemes(javaAlternativeSchemes):
        alternativeSchemes = []
        i = 0
        while i < javaAlternativeSchemes.size():
            alternativeSchemes[i] = AlternativeScheme(javaAlternativeSchemes.get(i))
            i += 1
        return alternativeSchemes

    # Gets the version of the SwissQR bill standard.
    # Value: The SwissQR bill standard version.
    def getVersion(self):
        return self.getJavaClass().getVersion()

    # Sets the version of the SwissQR bill standard.
    # Value: The SwissQR bill standard version.
    def setVersion(self, value):
        self.getJavaClass().setVersion(value)

    # Gets the payment amount.
    #
    # Valid values are between 0.01 and 999,999,999.99.
    #
    # Value: The payment amount.
    def getAmount(self):
        return self.getJavaClass().getAmount()

    # Sets the payment amount.
    #
    # Valid values are between 0.01 and 999,999,999.99.
    #
    # Value: The payment amount.
    def setAmount(self, value):
        self.getJavaClass().setAmount(value)

    # Gets the payment currency.
    #
    # Valid values are "CHF" and "EUR".
    #
    # Value: The payment currency.
    def getCurrency(self):
        return self.getJavaClass().getCurrency()

    # Sets the payment currency.
    #
    # Valid values are "CHF" and "EUR".
    #
    # Value: The payment currency.
    def setCurrency(self, value):
        self.getJavaClass().setCurrency(value)

    # Gets the creditor's account number.
    #
    # Account numbers must be valid IBANs of a bank of Switzerland or
    # Liechtenstein. Spaces are allowed in the account number.
    #
    # Value: The creditor account number.
    def getAccount(self):
        return self.getJavaClass().getAccount()

    # Sets the creditor's account number.
    #
    # Account numbers must be valid IBANs of a bank of Switzerland or
    # Liechtenstein. Spaces are allowed in the account number.
    #
    # Value: The creditor account number.
    def setAccount(self, value):
        self.getJavaClass().setAccount(value)

    # Gets the creditor address.
    # Value: The creditor address.
    def getCreditor(self):
        return self.creditor

    # Sets the creditor address.
    # Value: The creditor address.
    def setCreditor(self, value):
        self.creditor = value
        self.getJavaClass().setCreditor(value.getJavaClass())

    # Gets the creditor payment reference.
    #
    # The reference is mandatory for SwissQR IBANs, i.e.IBANs in the range
    # CHxx30000xxxxxx through CHxx31999xxxxx.
    #
    #
    # If specified, the reference must be either a valid SwissQR reference
    # (corresponding to ISR reference form) or a valid creditor reference
    # according to ISO 11649 ("RFxxxx"). Both may contain spaces for formatting.
    # Value: The creditor payment reference.
    def getReference(self):
        return self.getJavaClass().getReference()

    # Sets the creditor payment reference.
    #
    # The reference is mandatory for SwissQR IBANs, i.e.IBANs in the range
    # CHxx30000xxxxxx through CHxx31999xxxxx.
    #
    #
    # If specified, the reference must be either a valid SwissQR reference
    # (corresponding to ISR reference form) or a valid creditor reference
    # according to ISO 11649 ("RFxxxx"). Both may contain spaces for formatting.
    #
    # Value: The creditor payment reference.
    def setReference(self, value):
        self.getJavaClass().setReference(value)

    # Creates and sets a ISO11649 creditor reference from a raw string by prefixing
    # the String with "RF" and the modulo 97 checksum.
    #
    # Whitespace is removed from the reference
    #
    # @exception ArgumentException rawReference contains invalid characters.
    # @param rawReference The raw reference.
    def createAndSetCreditorReference(self, rawReference):
        self.getJavaClass().createAndSetCreditorReference(rawReference)

    # Gets the debtor address.
    #
    # The debtor is optional. If it is omitted, both setting this field to
    # null or setting an address with all null or empty values is ok.
    #
    # Value: The debtor address.
    def getDebtor(self):
        return self.creditor

    # Sets the debtor address.
    #
    # The debtor is optional. If it is omitted, both setting this field to
    # null or setting an address with all null or empty values is ok.
    #
    # Value: The debtor address.
    def setDebtor(self, value):
        self.debtor = value
        self.getJavaClass().setDebtor(value.getJavaClass())

    # Gets the additional unstructured message.
    # Value: The unstructured message.
    def getUnstructuredMessage(self):
        return self.getJavaClass().getUnstructuredMessage()

    # Sets the additional unstructured message.
    # Value: The unstructured message.
    def setUnstructuredMessage(self, value):
        self.getJavaClass().setUnstructuredMessage(value)

    # Gets the additional structured bill information.
    # Value: The structured bill information.
    def getBillInformation(self):
        return self.getJavaClass().getBillInformation()

    # Sets the additional structured bill information.
    # Value: The structured bill information.
    def setBillInformation(self, value):
        self.getJavaClass().setBillInformation(value)

    # Gets the alternative payment schemes.
    #
    # A maximum of two schemes with parameters are allowed.
    #
    # Value: The alternative payment schemes.
    def getAlternativeSchemes(self):
        return self.alternativeSchemes

    # Sets the alternative payment schemes.
    #
    # A maximum of two schemes with parameters are allowed.
    #
    # Value: The alternative payment schemes.
    def setAlternativeSchemes(self, value):
        self.getJavaClass().getAlternativeSchemes().clear()
        i = 0
        while (i < len(value)):
            self.getJavaClass().getAlternativeSchemes().set(value[i].getJavaClass())
            i += 1

    # Gets the hash code for this instance.
    # @return A hash code for the current object.
    def addAlternativeScheme(self, value):
        alternativeScheme = self.getJavaClass().getAlternativeSchemes().add(value.getJavaClass())


    
    # Determines whether the specified object is equal to the current object.
    # @return true if the specified object is equal to the current object; otherwise, false.
    # @param obj The object to compare with the current object.
    def equals(self,obj):
        return self.getJavaClass().equals(obj.getJavaClass())

    
    # Gets the hash code for this instance.
    # @return A hash code for the current object.
    def hashCode(self):
        return self.getJavaClass().hashCode()

# Class for encoding and decoding the text embedded in the SwissQR code.
class SwissQRCodetext(Assist.BaseJavaClass):
    javaClassName = "com.aspose.mw.barcode.complexbarcode.MwSwissQRCodetext"
    bill = None

    def init(self):
        self.bill = SwissQRBill(self.getJavaClass().getBill())

    # SwissQR bill data
    def getBill(self):
        return self.bill

    # Creates an instance of SwissQRCodetext.
    #
    # @param bill SwissQR bill data
    # @throws BarcodeException
    def  __init__(self, arg):
        super().__init__(SwissQRCodetext.initSwissQRCodetext(arg))
        self.init()

    @staticmethod
    def initSwissQRCodetext(arg):
        if isinstance(arg, SwissQRBill):
            javaClass = jpype.JClass(SwissQRCodetext.javaClassName)
            javaSwissQRCodetext = javaClass(SwissQRCodetext.javaClassName)
            return javaSwissQRCodetext(arg.getJavaClass())
        elif arg is None:
            javaClass = jpype.JClass(SwissQRCodetext.javaClassName)
            javaSwissQRCodetext = javaClass()
            return javaSwissQRCodetext
        else:
            return arg

    # Construct codetext from SwissQR bill data
    #
    # @return Constructed codetext
    def getConstructedCodetext(self):
        return self.getJavaClass().getConstructedCodetext()

    # Initializes Bill with constructed codetext.
    #
    # @param constructedCodetext Constructed codetext.
    def initFromString(self, constructedCodetext):
        self.getJavaClass().initFromString(constructedCodetext)

    # Gets barcode type.
    #
    # @return Barcode type.
    def getBarcodeType(self):
        return self.getJavaClass().getBarcodeType()