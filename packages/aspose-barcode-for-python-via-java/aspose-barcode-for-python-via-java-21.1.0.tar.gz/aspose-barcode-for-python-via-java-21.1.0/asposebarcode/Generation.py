import jpype
from . import Assist
from enum import Enum
import base64

#  BarcodeGenerator for backend barcode images generation.
#
#  supported symbologies:
#  1D:
#  Codabar, Code11, Code128, Code39Standard, Code39Extended
#  Code93Standard, Code93Extended, EAN13, EAN8, Interleaved2of5,
#  MSI, Standard2of5, UPCA, UPCE, ISBN, GS1Code128, Postnet, Planet
#  EAN14, SCC14, SSCC18, ITF14, SingaporePost ...
#  2D:
#  Aztec, DataMatrix, PDf417, QR code ...
#
#  This sample shows how to create and save a barcode image.
#          encode_type = EncodeTypes.CODE_128
#          generator = BarcodeGenerator($encode_type)
#          generator.setCodeText("123ABC")
class BarcodeGenerator(Assist.BaseJavaClass):
    javaClassName = 'com.aspose.mw.barcode.generation.MwBarcodeGenerator'
    javaClass = None
    parameters = None

    # BarcodeGenerator constructor.
    # @param args can take following combinations of arguments:
    #    1) Barcode symbology type. Use EncodeTypes class to setup a symbology
    #    2) type EncodeTypes, Text to be encoded.
    #   barcodeGenerator = BarcodeGenerator(EncodeTypes.EAN_14, "332211")
    # @throws BarcodeException
    def __init__(self, encodeType, codeText):
        javaBarcodeGenerator = jpype.JClass(self.javaClassName)
        if not isinstance(encodeType, EncodeTypes):
            raise Assist.BarcodeException("Waiting for EncodeTypes type, but got '" + type(encodeType).__name__ + "'")
        self.javaClass = javaBarcodeGenerator(str(encodeType.value), codeText)
        super().__init__(self.javaClass)


    def init(self):
        self.parameters = BaseGenerationParameters(self.getJavaClass().getParameters())

     # Generation parameters.
     # @return BaseGenerationParameters
    def getParameters(self):
        return self.parameters


     # Barcode symbology type.
    def getBarcodeType(self):
        return EncodeTypes(self.getJavaClass().getBarcodeType())

     # Barcode symbology type.
    def setBarcodeType(self, value):
        self.getJavaClass().setBarcodeType(str(value.value))

     # Generate the barcode image under current settings.
     # This sample shows how to create and save a barcode image.
     # @param format_name image format name("PNG", "BMP", "JPEG", "GIF", "TIFF")
     # generator = BarCodeGenerator(EncodeTypes.CODE_128)
     # image = generator.generateBarCodeImage(null)// if value = null, default image format PNG
     # return Base64 representation of barcode image
    def generateBarcodeImage(self, imageFormat):
        try:
            return str(self.javaClass.generateBarcodeImage(imageFormat))
        except Exception as e:
            raise Assist.BarcodeException(e)

     # Save barcode image to specific file in specific format.
     # @param filePath Path to save to.
     # @param format_name image format name("PNG", "BMP", "JPEG", "GIF", "TIFF")
     # generator = BarCodeGenerator(EncodeTypes.CODE_128)
     # generator.save("file path", null)// if value = null, default image format PNG
    def save(self, imagePath,imageFormat):
        base64Str = self.generateBarcodeImage(str(imageFormat))
        base64_bytes = base64.b64decode(base64Str)
        f = open(imagePath, 'wb+')
        f.write(base64_bytes)
        f.close()

    # Text to be encoded.
    def getCodeText(self):
        return self.getJavaClass().getCodeText()

    # Text to be encoded.
    def setCodeText(self, value):
        self.getJavaClass().setCodeText(value)

# Barcode generation parameters.
class BarcodeParameters(Assist.BaseJavaClass):
    xDimension = None
    barHeight = None
    barCodeWidth = None
    barCodeHeight = None
    codeTextParameters = None
    postal = None
    australianPost = None
    codablock = None
    dataBar = None
    dataMatrix = None
    code16K = None
    itf = None
    qr = None
    pdf417 = None
    maxiCode = None
    aztec = None
    codabar = None
    coupon = None
    supplement = None
    dotCode = None
    padding = None
    patchCode = None
    barWidthReduction = None

    def __init__(self, javaClass):
        super().__init__(javaClass)

    def init(self):
        self.xDimension = Unit(self.getJavaClass().getXDimension())
        self.barHeight = Unit(self.getJavaClass().getBarHeight())
        self.barCodeWidth = Unit(self.getJavaClass().getBarCodeWidth())
        self.barCodeHeight = Unit(self.getJavaClass().getBarCodeHeight())
        self.codeTextParameters = CodetextParameters(self.getJavaClass().getCodeTextParameters())
        self.postal = PostalParameters(self.getJavaClass().getPostal())
        self.australianPost = AustralianPostParameters(self.getJavaClass().getAustralianPost())
        self.codablock = CodablockParameters(self.getJavaClass().getCodablock())
        self.dataBar = DataBarParameters(self.getJavaClass().getDataBar())
        self.dataMatrix = DataMatrixParameters(self.getJavaClass().getDataMatrix())
        self.code16K = Code16KParameters(self.getJavaClass().getCode16K())
        self.itf = ITFParameters(self.getJavaClass().getITF())
        self.qr = QrParameters(self.getJavaClass().getQR())
        self.pdf417 = Pdf417Parameters(self.getJavaClass().getPdf417())
        self.maxiCode = MaxiCodeParameters(self.getJavaClass().getMaxiCode())
        self.aztec = AztecParameters(self.getJavaClass().getAztec())
        self.codabar = CodabarParameters(self.getJavaClass().getCodabar())
        self.coupon = CouponParameters(self.getJavaClass().getCoupon())
        self.supplement = SupplementParameters(self.getJavaClass().getSupplement())
        self.dotCode = DotCodeParameters(self.getJavaClass().getDotCode())
        self.padding = Padding(self.getJavaClass().getPadding())
        self.patchCode = PatchCodeParameters(self.getJavaClass().getPatchCode())
        self.barWidthReduction = Unit(self.getJavaClass().getBarWidthReduction());

    # x-dimension is the smallest width of the unit of BarCode bars or spaces.
    # Increase this will increase the whole barcode image width.
    # Ignored if AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    def getXDimension(self):
        return self.xDimension

    # x-dimension is the smallest width of the unit of BarCode bars or spaces.
    # Increase this will increase the whole barcode image width.
    # Ignored if AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    # @throws BarcodeException
    def setXDimension(self, value) :
        self.getJavaClass().setXDimension(value.getJavaClass())
        self.xDimension = value

    # Get bars reduction value that is used to compensate ink spread while printing.
    # @return Unit value of BarWidthReduction
    def getBarWidthReduction(self):
        try:
            return self.barWidthReduction
        except Exception as ex:
            barcode_exception = Assist.BarcodeException(ex)
            raise barcode_exception

    # Sets bars reduction value that is used to compensate ink spread while printing.
    def setBarWidthReduction(self, value):
        try:
            self.getJavaClass().setBarWidthReduction(value.getJavaClass())
            self.barWidthReduction = value
        except Exception as ex:
            barcode_exception = Assist.BarcodeException(ex)
            raise barcode_exception

    # Height of 1D barcodes' bars in Unit value.
    # Ignored if AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    # @throws BarcodeException
    def getBarHeight(self):
        return self.barHeight

    # Height of 1D barcodes' bars in Unit value.
    # Ignored if AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    # @throws BarcodeException
    def setBarHeight(self, value) :
        self.getJavaClass().setBarHeight(value.getJavaClass())
        self.barHeight = value

    # Specifies the different types of automatic sizing modes.
    # Default value: AutoSizeMode.NONE.
    # @deprecated "This method is obsolete. Call BaseGenerationParameters.getAutoSizeMode() instead."
    # @throws BarcodeException
    def getAutoSizeMode(self):
        return self.getJavaClass().getAutoSizeMode()

     # Specifies the different types of automatic sizing modes.
     # Default value: AutoSizeMode.NONE.
     # @deprecated "This method is obsolete. Call BaseGenerationParameters.setAutoSizeMode() instead."
     # @throws BarcodeException
    def setAutoSizeMode(self, value) :
        self.getJavaClass().setAutoSizeMode(value)

     # BarCode image height when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
     # @deprecated "This method is obsolete. Call BaseGenerationParameters.getImageHeight() instead."
    def getBarCodeHeight(self):
        return self.barCodeHeight

     # BarCode image height when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
     # @deprecated "This method is obsolete. Call BaseGenerationParameters.setImageHeight() instead."
    def setBarCodeHeight(self, value) :
        self.getJavaClass().setBarCodeHeight(value.getJavaClass())
        self.barCodeHeight = value

    # BarCode image width when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    # @deprecated "This method is obsolete. Call BaseGenerationParameters.getImageWidth() instead."
    def getBarCodeWidth(self):
        return self.barCodeWidth

    # BarCode image width when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    # @deprecated "This method is obsolete. Call BaseGenerationParameters.setImageWidth() instead."
    def setBarCodeWidth(self, value) :
        self.getJavaClass().setBarCodeWidth(value.getJavaClass())
        self.barCodeWidth = value

    # Bars color.
    # Default value: #000000.
    # @deprecated "This method is obsolete. Call BarcodeParameters.getBarColor() instead."
    def getForeColor(self):
        return self.getBarColor()

    # Bars color.
    # Default value Black.
    # @deprecated "This method is obsolete. Call BarcodeParameters.setBarColor() instead."
    def setForeColor(self, value) :
        self.setBarColor(value)

    # Bars color.
    # Default value: #000000
    def getBarColor(self):
        return self.getJavaClass().getBarColor()

    # Bars color.
    # Default value: #000000.
    def setBarColor(self, value) :
        self.getJavaClass().setBarColor(value)

    # Barcode paddings.
    # Default value: 5pt 5pt 5pt 5pt.
    def getPadding(self):
        return self.padding

    # Barcode paddings.
    # Default value: 5pt 5pt 5pt 5pt.
    def setPadding(self, value) :
        self.getJavaClass().setPadding(value.getJavaClass())
        self.padding = value

    # Always display checksum digit in the human readable text for Code128 and GS1Code128 barcodes.
    def getChecksumAlwaysShow(self):
        return self.getJavaClass().getChecksumAlwaysShow()

    # Always display checksum digit in the human readable text for Code128 and GS1Code128 barcodes.
    def setChecksumAlwaysShow(self, value) :
        self.getJavaClass().setChecksumAlwaysShow(value)

    # Enable checksum during generation 1D barcodes.
    # Default is treated as Yes for symbology which must contain checksum, as No where checksum only possible.
    # Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN, Codabar
    # Checksum always used: Rest symbology
    def isChecksumEnabled(self):
        return self.getJavaClass().isChecksumEnabled()

    # Enable checksum during generation 1D barcodes.
    # Default is treated as Yes for symbology which must contain checksum, as No where checksum only possible.
    # Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN, Codabar
    # Checksum always used: Rest symbology
    def setChecksumEnabled(self, value) :
        self.getJavaClass().setChecksumEnabled(value)

    # Indicates whether explains the character "\" as an escape character in CodeText property. Used for Pdf417, DataMatrix, Code128 only
    # If the EnableEscape is true, "\" will be explained as a special escape character. Otherwise, "\" acts as normal characters.
    # Aspose.BarCode supports inputing decimal ascii code and mnemonic for ASCII control-code characters. For example, \013 and \\CR stands for CR.
    def getEnableEscape(self):
        return self.getJavaClass().getEnableEscape()

    # Indicates whether explains the character "\" as an escape character in CodeText property. Used for Pdf417, DataMatrix, Code128 only
    # If the EnableEscape is true, "\" will be explained as a special escape character. Otherwise, "\" acts as normal characters.
    # <hr>Aspose.BarCode supports inputing decimal ascii code and mnemonic for ASCII control-code characters. For example, \013 and \\CR stands for CR.</hr>
    def setEnableEscape(self, value) :
        self.getJavaClass().setEnableEscape(value)

    # Wide bars to Narrow bars ratio.
    # Default value: 3, that is, wide bars are 3 times as wide as narrow bars.
    # Used for ITF, PZN, PharmaCode, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, IATA2of5, VIN, DeutschePost, OPC, Code32, DataLogic2of5, PatchCode, Code39Extended, Code39Standard
    # The WideNarrowRatio parameter value is less than or equal to 0.
    def getWideNarrowRatio(self):
        return self.getJavaClass().getWideNarrowRatio()

    # Wide bars to Narrow bars ratio.
    # Default value: 3, that is, wide bars are 3 times as wide as narrow bars.
    # Used for ITF, PZN, PharmaCode, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, IATA2of5, VIN, DeutschePost, OPC, Code32, DataLogic2of5, PatchCode, Code39Extended, Code39Standard
    # The WideNarrowRatio parameter value is less than or equal to 0.
    def setWideNarrowRatio(self, value) :
        self.getJavaClass().setWideNarrowRatio(value)

    # Codetext parameters.
    def getCodeTextParameters(self):
        return self.codeTextParameters

    # Gets a value indicating whether bars filled.
    # Only for 1D barcodes.
    # Default value: true.
    def getFilledBars(self):
        return self.getJavaClass().getFilledBars()

    #Sets a value indicating whether bars filled.
    #Only for 1D barcodes.
    #Default value: true.
    def setFilledBars(self, value) :
        self.getJavaClass().setFilledBars(value)

    # Postal parameters. Used for Postnet, Planet.
    def getPostal(self):
        return self.postal

    # PatchCode parameters.
    def getPatchCode(self):
        return self.patchCode


    # AustralianPost barcode parameters.
    def getAustralianPost(self):
        return self.australianPost

    # Databar parameters.
    def getDataBar(self):
        return self.dataBar

    # Codablock parameters.
    def getCodablock(self):
        return self.codablock

    # DataMatrix parameters.
    def getDataMatrix(self):
        return self.dataMatrix

    # Code16K parameters.
    def getCode16K(self):
        return self.code16K

    # DotCode parameters.
    def getDotCode(self):
        return self.dotCode

    # ITF parameters.
    def getITF(self):
        return self.itf

    # PDF417 parameters.
    def getPdf417(self):
        return self.pdf417

    # QR parameters.
    def getQR(self):
        return self.qr

    # Supplement parameters. Used for Interleaved2of5, Standard2of5, EAN13, EAN8, UPCA, UPCE, ISBN, ISSN, ISMN.
    def getSupplement(self):
        return self.supplement

    # MaxiCode parameters.
    def getMaxiCode(self):
        return self.maxiCode

    # Aztec parameters.
    def getAztec(self):
        return self.aztec

    # Codabar parameters.
    def getCodabar(self):
        return self.codabar

    # Coupon parameters. Used for UpcaGs1DatabarCoupon, UpcaGs1Code128Coupon.
    def getCoupon(self):
        return self.coupon

# Barcode image generation parameters.
class BaseGenerationParameters(Assist.BaseJavaClass):
    captionAbove = None
    captionBelow = None
    barcodeParameters = None
    borderParameters = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.captionAbove = CaptionParameters(self.getJavaClass().getCaptionAbove())
        self.captionBelow = CaptionParameters(self.getJavaClass().getCaptionBelow())
        self.barcodeParameters = BarcodeParameters(self.getJavaClass().getBarcode())
        self.borderParameters = BorderParameters(self.getJavaClass().getBorder())

    # Background color of the barcode image.
    # Default value: #FFFFFF
    # See Color.
    def getBackColor(self):
        return self.getJavaClass().getBackColor()

    # Background color of the barcode image.
    # Default value: #FFFFFF
    # See Color.
    def setBackColor(self, hexValue):
        self.getJavaClass().setBackColor(hexValue)

    # Gets the resolution of the BarCode image.
    # One value for both dimensions.
    # Default value: 96 dpi.
    # The Resolution parameter value is less than or equal to 0.
    def getResolution(self):
        return self.getJavaClass().getResolution()

    # Sets the resolution of the BarCode image.
    # One value for both dimensions.
    # Default value: 96 dpi.
    # The Resolution parameter value is less than or equal to 0.
    def setResolution(self, value):
        self.getJavaClass().setResolution(value)

    #  BarCode image rotation angle, measured in degree, e.g. RotationAngle = 0 or RotationAngle = 360 means no rotation.
    #  If RotationAngle NOT equal to 90, 180, 270 or 0, it may increase the difficulty for the scanner to read the image.
    #  Default value: 0.
    #  This sample shows how to create and save a BarCode image.
    #     generator = BarcodeGenerator( EncodeTypes.DATA_MATRIX)
    #     generator.getParameters().setRotationAngle(7)
    #     generator.save("test.png")
    def getRotationAngle(self):
        return self.getJavaClass().getRotationAngle()

    #  BarCode image rotation angle, measured in degree, e.g. RotationAngle = 0 or RotationAngle = 360 means no rotation.
    #  If RotationAngle NOT equal to 90, 180, 270 or 0, it may increase the difficulty for the scanner to read the image.
    #  Default value: 0.
    #  This sample shows how to create and save a BarCode image.
    #     generator = BarcodeGenerator( EncodeTypes.DATA_MATRIX)
    #     generator.getParameters().setRotationAngle(7)
    #     generator.save("test.png")
    def setRotationAngle(self, value):
        self.getJavaClass().setRotationAngle(value)

    # Caption Above the BarCode image. See CaptionParameters.
    def getCaptionAbove(self):
        return self.captionAbove

    # Caption Above the BarCode image. See CaptionParameters.
    def setCaptionAbove(self, value):
        self.getJavaClass().setCaptionAbove(value.getJavaClass())
        self.captionAbove.updateCaption(value)

    # Caption Below the BarCode image. See CaptionParameters.
    def getCaptionBelow(self):
        return self.captionBelow

    # Caption Below the BarCode image. See CaptionParameters.
    def setCaptionBelow(self, value):
        self.getJavaClass().setCaptionBelow(value.getJavaClass())
        self.captionBelow.updateCaption(value)

    # Specifies the different types of automatic sizing modes.
    # Default value: AutoSizeMode.NONE.
    def getAutoSizeMode(self):
        return AutoSizeMode(self.getJavaClass().getAutoSizeMode())

    # Specifies the different types of automatic sizing modes.
    # Default value: AutoSizeMode.NONE.
    def setAutoSizeMode(self, value):
        self.getJavaClass().setAutoSizeMode(str(value.value))


    # BarCode image height when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    def getImageHeight(self):
        return self.getBarcode().getBarCodeHeight()

    # BarCode image height when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    def setImageHeight(self, value):
        self.getBarcode().setBarCodeHeight(value)


    # BarCode image width when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    def getImageWidth(self):
        return self.getBarcode().getBarCodeWidth()

    # BarCode image width when AutoSizeMode property is set to AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    def setImageWidth(self, value):
        self.getBarcode().setBarCodeWidth(value)

    # Gets the BarcodeParameters that contains all barcode properties.
    def getBarcode(self):
        return self.barcodeParameters

    # Gets the BarcodeParameters that contains all barcode properties.
    def setBarcode(self, value):
        self.getJavaClass().setBarcode(value.getJavaClass())
        self.barcodeParameters = value

    # Gets the BorderParameters that contains all configuration properties for barcode border.
    def getBorder(self):
        return self.borderParameters

# Barcode image border parameters
class BorderParameters(Assist.BaseJavaClass):
    width = None

    def __init__(self, javaClass):
        super().__init__(javaClass)

    def init(self):
        self.width = Unit(self.getJavaClass().getWidth())

    # Border visibility. If false than parameter Width is always ignored (0).
    # Default value: false.
    def getVisible(self):
        return self.getJavaClass().getVisible()

    # Border visibility. If false than parameter Width is always ignored (0).
    # Default value: false.
    def setVisible(self, value):
        self.getJavaClass().setVisible(value)

    # Border width.
    # Default value: 0.
    # Ignored if Visible is set to false.
    def getWidth(self):
        return self.width

    # Border width.
    # Default value: 0.
    # Ignored if Visible is set to false.
    def setWidth(self, value):
        self.getJavaClass().setWidth(value.getJavaClass())
        self.width = value

    # Returns a human-readable string representation of this BorderParameters.
    # @return A string that represents this BorderParameters.
    def toString(self):
        return self.getJavaClass().toString()

    # Border dash style.
    # Default value: BorderDashStyle.SOLID.
    def getDashStyle(self):
        return BorderDashStyle(self.getJavaClass().getDashStyle())

    # Border dash style.
    # Default value: BorderDashStyle.SOLID.
    def setDashStyle(self, value):
        self.getJavaClass().setDashStyle(value.value)

    # Border color.
    # Default value: #000000
    def getColor(self):
        return self.getJavaClass().getColor()

    # Border color.
    # Default value: #000000
    def setColor(self, hexValue):
        self.getJavaClass().setColor(hexValue)

# Caption parameters.
class CaptionParameters(Assist.BaseJavaClass):

    font = None
    padding = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.padding = Padding(self.getJavaClass().getPadding())
        self.font = FontUnit(self.getJavaClass().getFont())

    # Caption text.
    # Default value: empty string.
    def getText(self):
        return self.getJavaClass().getText()

    # Caption text.
    # Default value: empty string.
    def setText(self, value) :
        self.getJavaClass().setText(value)

    # Caption font.
    # Default value: Arial 8pt regular.
    def getFont(self):
        return self.font

    # Caption text visibility.
    # Default value: false.
    def getVisible(self):
        return self.getJavaClass().getVisible()

    # Caption text visibility.
    # Default value: false.
    def setVisible(self, value) :
        self.getJavaClass().setVisible(value)

    # Caption text color.
    # Default value BLACK.
    def getTextColor(self):
        return self.getJavaClass().getTextColor()

    # Caption text color.
    # Default value BLACK.
    def setTextColor(self, rgbValue):
        self.getJavaClass().setTextColor(rgbValue)

    # Captions paddings.
    # Default value for CaptionAbove: 5pt 5pt 0 5pt.
    # Default value for CaptionBelow: 0 5pt 5pt 5pt.
    def getPadding(self):
        return self.padding

    # Captions paddings.
    # Default value for CaptionAbove: 5pt 5pt 0 5pt.
    # Default value for CaptionBelow: 0 5pt 5pt 5pt.
    def setPadding(self, value) :
        self.getJavaClass().setPadding(value.getJavaClass())
        self.padding = value

    # Caption test horizontal alignment.
    # Default valueAlignment.Center.
    def getAlignment(self):
        return self.getJavaClass().getAlignment()

    # Caption test horizontal alignment.
    # Default valueAlignment.Center.
    def setAlignment(self, value) :
        self.getJavaClass().setAlignment(value)

    # Specify word wraps (line breaks) within text.
    # @return bool
    def getNoWrap(self):
        return self.getJavaClass().getNoWrap()

    # Specify word wraps (line breaks) within text.
    def setNoWrap(self, value):
        self.getJavaClass().setNoWrap(value)

#  Specifies the size value in different units (Pixel, Inches, etc.).
#  This sample shows how to create and save a BarCode image.
#    generator = BarcodeGenerator(EncodeTypes.CODE_128)
#    generator.getParameters().getBarcode().getBarHeight().setMillimeters(10)
#    generator.save("test.png")
class Unit(Assist.BaseJavaClass):
    def __init__(self, source):
        super().__init__(Unit.initUnit(source))
        self.init()

    @staticmethod
    def initUnit(source):
        if isinstance(source, Unit):
            return source.getNativeObject()
        return source

    def init(self):
        # TODO: Implement init() method.
        pass

    # Gets size value in pixels.
    def getPixels(self):
        return self.getJavaClass().getPixels()
    
    # Sets size value in pixels.
    def setPixels(self, value):
        self.getJavaClass().setPixels(value)
    
    # Gets size value in inches.
    def getInches(self):
        return self.getJavaClass().getInches()
    
    # Sets size value in inches.
    def setInches(self, value):
            self.getJavaClass().setInches(value)
    
    # Gets size value in millimeters.
    def getMillimeters(self):
            return self.getJavaClass().getMillimeters()
    
    # Sets size value in millimeters.
    def setMillimeters(self, value):
            self.getJavaClass().setMillimeters(value)
    
    # Gets size value in point.
    def getPoint(self):
            return self.getJavaClass().getPoint()
    
    # Sets size value in point.
    def setPoint(self, value):
            self.getJavaClass().setPoint(value)
    
    # Gets size value in document units.
    def getDocument(self):
            return self.getJavaClass().getDocument()
    
    # Sets size value in document units.
    def setDocument(self, value):
        self.getJavaClass().setDocument(value)

    # Returns a human-readable string representation of this Unit.
    # @return A string that represents this Unit.
    def toString(self):
        return self.getJavaClass().toString()

    # Determines whether this instance and a specified object,
    # which must also be a Unit object, have the same value.
    # @param obj The Unit to compare to this instance.
    # @return true if obj is a Unit and its value is the same as this instance
    # otherwise, false. If obj is null, the method returns false.
    def equals(self, obj):
        return self.getJavaClass().equals(obj)

# Paddings parameters.
class Padding(Assist.BaseJavaClass):

    top = None
    bottom = None
    right = None
    left = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.top = Unit(self.getJavaClass().getTop())
        self.bottom = Unit(self.getJavaClass().getBottom())
        self.right = Unit(self.getJavaClass().getRight())
        self.left = Unit(self.getJavaClass().getLeft())

    # Top padding.
    def getTop(self):
        return self.top

    # Top padding.
    def setTop(self, value):
        self.getJavaClass().setTop(value.getJavaClass())
        self.top = value

    # Bottom padding.
    def getBottom(self):
        return self.bottom

    # Bottom padding.
    def setBottom(self, value):
        self.getJavaClass().setBottom(value.getJavaClass())
        self.bottom = value

    # Right padding.
    def getRight(self):
        return self.right

    # Right padding.
    def setRight(self, value):
        self.getJavaClass().setRight(value.getJavaClass())
        self.right = value

    # Left padding.
    def getLeft(self):
        return self.left

    # Left padding.
    def setLeft(self, value):
        self.getJavaClass().setLeft(value.getJavaClass())
        self.left = value

    # Returns a human-readable string representation of this Padding.
    # @return A string that represents this Padding.
    def toString(self):
        return self.getJavaClass().toString()

# Codetext parameters.
class CodetextParameters(Assist.BaseJavaClass):

    font = None
    space = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.font = FontUnit(self.getJavaClass().getFont())
        self.space = Unit(self.getJavaClass().getSpace())

    # Text that will be displayed instead of codetext in 2D barcodes.
    # Used for: Aztec, Pdf417, DataMatrix, QR, MaxiCode, DotCode
    def getTwoDDisplayText(self):
        return self.getJavaClass().getTwoDDisplayText()

    # Text that will be displayed instead of codetext in 2D barcodes.
    # Used for: Aztec, Pdf417, DataMatrix, QR, MaxiCode, DotCode
    def setTwoDDisplayText(self, value):
        self.getJavaClass().setTwoDDisplayText(value)

    # Specify FontMode. If FontMode is set to Auto, font size will be calculated automatically based on xDimension value.
    # It is recommended to use FontMode.AUTO especially in AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    # Default value: FontMode.AUTO.
    def getFontMode(self):
        return FontMode(int(self.getJavaClass().getFontMode()))

    # Specify FontMode. If FontMode is set to Auto, font size will be calculated automatically based on xDimension value.
    # It is recommended to use FontMode.AUTO especially in AutoSizeMode.NEAREST or AutoSizeMode.INTERPOLATION.
    # Default value: FontMode.AUTO.
    def setFontMode(self, value):
        self.getJavaClass().setFontMode(value.value)

    # Specify the displaying CodeText's font.
    # Default value: Arial 5pt regular.
    # Ignored if FontMode is set to FontMode.AUTO.
    def getFont(self):
        return self.font

    # Specify the displaying CodeText's font.
    # Default value: Arial 5pt regular.
    # Ignored if FontMode is set to FontMode.AUTO.
    def setFont(self, value):
        self.getJavaClass().setFont(value.getJavaClass())
        self.font = value

    # Space between the CodeText and the BarCode in Unit value.
    # Default value: 2pt.
    # Ignored for EAN8, EAN13, UPCE, UPCA, ISBN, ISMN, ISSN, UpcaGs1DatabarCoupon.
    def getSpace(self):
        return self.space

    # Space between the CodeText and the BarCode in Unit value.
    # Default value: 2pt.
    # Ignored for EAN8, EAN13, UPCE, UPCA, ISBN, ISMN, ISSN, UpcaGs1DatabarCoupon.
    def setSpace(self, value):
        self.getJavaClass().setSpace(value.getJavaClass())
        self.space = value

    # Gets or sets the alignment of the code text.
    # Default value: TextAlignment.CENTER.
    def getAlignment(self):
        return self.getJavaClass().getAlignment()

    # Gets or sets the alignment of the code text.
    # Default value: TextAlignment.CENTER.
    def setAlignment(self, value):
        self.getJavaClass().setAlignment(value)

    # Specify the displaying CodeText's Color.
    # Default value BLACK.
    def getColor(self):
        return self.getJavaClass().getColor()

    # Specify the displaying CodeText's Color.
    # Default value BLACK.
    def setColor(self, value):
        self.getJavaClass().setColor(value)

    # Specify the displaying CodeText Location, set to CodeLocation.NONE to hide CodeText.
    # Default value:  CodeLocation.BELOW.
    def getLocation(self):
        return self.getJavaClass().getLocation()

    # Specify the displaying CodeText Location, set to  CodeLocation.NONE to hide CodeText.
    # Default value:  CodeLocation.BELOW.
    def setLocation(self, value):
        self.getJavaClass().setLocation(value)

    # Specify word wraps (line breaks) within text.
    # @return bool
    def getNoWrap(self):
        return self.getJavaClass().getNoWrap()

    # Specify word wraps (line breaks) within text.
    def setNoWrap(self, value):
        self.getJavaClass().setNoWrap(value)

    # Returns a human-readable string representation of this CodetextParameters.
    # @return A string that represents this CodetextParameters.
    def toString(self):
        return self.getJavaClass().toString()

# Postal parameters. Used for Postnet, Planet.
class PostalParameters(Assist.BaseJavaClass):

    postalShortBarHeight = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.postalShortBarHeight = Unit(self.getJavaClass().getPostalShortBarHeight())

    # Short bar's height of Postal barcodes.
    def  getPostalShortBarHeight(self):
        return self.postalShortBarHeight

    # Short bar's height of Postal barcodes.
    def  setPostalShortBarHeight(self, value):
        self.getJavaClass().setPostalShortBarHeight(value.getJavaClass())
        self.postalShortBarHeight = value

    # Returns a human-readable string representation of this PostalParameters.
    # @return A string that represents this PostalParameters.
    def toString(self):
        return self.getJavaClass().toString()

# AustralianPost barcode parameters.
class AustralianPostParameters(Assist.BaseJavaClass):
    australianPostShortBarHeight = None

    def __init__(self, javaClass):
        super().__init__(javaClass)

    def init(self):
        self.australianPostShortBarHeight = Unit(self.getJavaClass().getAustralianPostShortBarHeight())

    # Short bar's height of AustralianPost barcode.
    def  getAustralianPostShortBarHeight(self):
        return self.australianPostShortBarHeight

    # Short bar's height of AustralianPost barcode.
    def  setAustralianPostShortBarHeight(self, value):
        self.getJavaClass().setAustralianPostShortBarHeight(value.getJavaClass())
        self.australianPostShortBarHeight = value

    # Interpreting type for the Customer Information of AustralianPost, default to CustomerInformationInterpretingType.Other"
    def  getAustralianPostEncodingTable(self):
        return self.getJavaClass().getAustralianPostEncodingTable()

    # Interpreting type for the Customer Information of AustralianPost, default to CustomerInformationInterpretingType.Other"
    def  setAustralianPostEncodingTable(self, value):
        self.getJavaClass().setAustralianPostEncodingTable(value.value)

    # Returns a human-readable string representation of this AustralianPostParameters.
    # @return A string that represents this AustralianPostParameters.
    def toString(self):
        return self.getJavaClass().toString()

# Codablock parameters.
class CodablockParameters(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        pass

    # Columns count.
    def  getColumns(self):
        return self.getJavaClass().getColumns()

    # Columns count.
    def  setColumns(self, value):
        self.getJavaClass().setColumns(value)

    # Rows count.
    def  getRows(self):
        return self.getJavaClass().getRows()

    # Rows count.
    def  setRows(self, value):
        self.getJavaClass().setRows(value)

    # Height/Width ratio of 2D BarCode module.
    def  getAspectRatio(self):
        return self.getJavaClass().getAspectRatio()

    # Height/Width ratio of 2D BarCode module.
    def  setAspectRatio(self, value):
        self.getJavaClass().setAspectRatio(value)

    # Returns a human-readable string representation of this CodablockParameters.
    # @return A string that represents this CodablockParameters.
    def toString(self):
        return self.getJavaClass().toString()

# Databar parameters.
class DataBarParameters(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        pass

    # Enables flag of 2D composite component with DataBar barcode
    def is2DCompositeComponent(self):
        return self.getJavaClass().is2DCompositeComponent()

    # Enables flag of 2D composite component with DataBar barcode
    def set2DCompositeComponent(self, value):
        self.getJavaClass().set2DCompositeComponent(value)

    # If this flag is set, it allows only GS1 encoding standard for Databar barcode types
    def isAllowOnlyGS1Encoding(self):
        return self.getJavaClass().isAllowOnlyGS1Encoding()

    # If this flag is set, it allows only GS1 encoding standard for Databar barcode types
    def setAllowOnlyGS1Encoding(self, value):
        self.getJavaClass().setAllowOnlyGS1Encoding(value)

    # Columns count.
    def  getColumns(self):
        return self.getJavaClass().getColumns()

    # Columns count.
    def  setColumns(self, value):
        self.getJavaClass().setColumns(value)

    # Rows count.
    def  getRows(self):
        return self.getJavaClass().getRows()

    # Rows count.
    def  setRows(self, value):
        self.getJavaClass().setRows(value)

    # Height/Width ratio of 2D BarCode module.
    # Used for DataBar stacked.
    def  getAspectRatio(self):
        return self.getJavaClass().getAspectRatio()

    # Height/Width ratio of 2D BarCode module.
    # Used for DataBar stacked.
    def  setAspectRatio(self, value):
        self.getJavaClass().setAspectRatio(value)

    # Returns a human-readable string representation of this DataBarParameters.
    # @return A string that represents this DataBarParameters.
    def toString(self):
        return self.getJavaClass().toString()

# DataMatrix parameters.
class DataMatrixParameters(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        pass

    # Gets a Datamatrix ECC type.
    # Default value: DataMatrixEccType.ECC_200.
    def  getDataMatrixEcc(self):
        return self.getJavaClass().getDataMatrixEcc()

    # Sets a Datamatrix ECC type.
    # Default value: DataMatrixEccType.ECC_200.
    def  setDataMatrixEcc(self, value):
        self.getJavaClass().setDataMatrixEcc(value.value)

    # Encode mode of Datamatrix barcode.
    # Default value: DataMatrixEncodeMode.AUTO.
    def  getDataMatrixEncodeMode(self):
        return self.getJavaClass().getDataMatrixEncodeMode()

    # Encode mode of Datamatrix barcode.
    # Default value: DataMatrixEncodeMode.AUTO.
    def  setDataMatrixEncodeMode(self, value):
        self.getJavaClass().setDataMatrixEncodeMode(value.value)

    # ISO/IEC 16022
    # 5.2.4.7 Macro characters
    # 11.3 Protocol for Macro characters in the first position (ECC 200 only)
    # Macro Characters 05 and 06 values are used to obtain more compact encoding in special modes.
    # Can be used only with DataMatrixEccType.Ecc200 or DataMatrixEccType.EccAuto.
    # Cannot be used with EncodeTypes.GS_1_DATA_MATRIX
    # Default value: MacroCharacter.NONE.
    def getMacroCharacters(self):
        return self.getJavaClass().getMacroCharacters()

     # ISO/IEC 16022
     # 5.2.4.7 Macro characters
     # 11.3 Protocol for Macro characters in the first position (ECC 200 only)
     # Macro Characters 05 and 06 values are used to obtain more compact encoding in special modes.
     # Can be used only with DataMatrixEccType.Ecc200 or DataMatrixEccType.EccAuto.
     # Cannot be used with EncodeTypes.GS_1_DATA_MATRIX
     # Default value: MacroCharacter.NONE.
    def setMacroCharacters(self, value):
        self.getJavaClass().setMacroCharacters(value)

    # Columns count.
    def  getColumns(self):
        return self.getJavaClass().getColumns()

    # Columns count.
    def  setColumns(self, value):
        self.getJavaClass().setColumns(value)

    # Rows count.
    def  getRows(self):
        return self.getJavaClass().getRows()

    # Rows count.
    def  setRows(self, value):
        self.getJavaClass().setRows(value)

    # Height/Width ratio of 2D BarCode module.
    def  getAspectRatio(self):
        return self.getJavaClass().getAspectRatio()

    # Height/Width ratio of 2D BarCode module.
    def  setAspectRatio(self, value):
        self.getJavaClass().setAspectRatio(value)

    # Gets the encoding of codetext.
    # Default value: UTF-16
    def  getCodeTextEncoding(self):
        return self.getJavaClass().getCodeTextEncoding().toString()

    # Sets the encoding of codetext.
    # Default value: UTF-16
    def  setCodeTextEncoding(self, value):
        return self.getJavaClass().setCodeTextEncoding(value)

    # Returns a human-readable string representation of this DataMatrixParameters.
    # @return presentation of this DataMatrixParameters.
    def toString(self):
        return self.getJavaClass().toString()

# PatchCode parameters.
class PatchCodeParameters(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        pass

    # Specifies codetext for an extra QR barcode, when PatchCode is generated in page mode.
    def getExtraBarcodeText(self):
        return self.getJavaClass().getExtraBarcodeText()

    # Specifies codetext for an extra QR barcode, when PatchCode is generated in page mode.
    def  setExtraBarcodeText(self, value):
        self.getJavaClass().setExtraBarcodeText(value)

    # PatchCode format. Choose PatchOnly to generate single PatchCode. Use page format to generate Patch page with PatchCodes as borders.
    # Default value: PatchFormat.PATCH_ONLY
    # @return PatchFormat
    def  getPatchFormat(self):
        return self.getJavaClass().getPatchFormat()

    # PatchCode format. Choose PatchOnly to generate single PatchCode. Use page format to generate Patch page with PatchCodes as borders.
    # Default value: PatchFormat.PATCH_ONLY
    def  setPatchFormat(self, value):
        self.getJavaClass().setPatchFormat(int(value.value))

    # Returns a human-readable string representation of this <see cref="PatchCodeParameters"/>.
    # @return A string that represents this <see cref="PatchCodeParameters"/>.
    def toString(self):
        return self.getJavaClass().toString()

# Code16K parameters.
class Code16KParameters(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        pass

    # Height/Width ratio of 2D BarCode module.
    def  getAspectRatio(self):
        return self.getJavaClass().getAspectRatio()

    # Height/Width ratio of 2D BarCode module.
    def  setAspectRatio(self, value):
        self.getJavaClass().setAspectRatio(value)

    # Size of the left quiet zone in xDimension.
    # Default value: 10, meaning if xDimension = 2px than left quiet zone will be 20px.
    def  getQuietZoneLeftCoef(self):
        return self.getJavaClass().getQuietZoneLeftCoef()

    # Size of the left quiet zone in xDimension.
    # Default value: 10, meaning if xDimension = 2px than left quiet zone will be 20px.
    def  setQuietZoneLeftCoef(self, value):
        self.getJavaClass().setQuietZoneLeftCoef(value)

    # Size of the right quiet zone in xDimension.
    # Default value: 1, meaning if xDimension = 2px than right quiet zone will be 2px.
    def  getQuietZoneRightCoef(self):
        return self.getJavaClass().getQuietZoneRightCoef()

    # Size of the right quiet zone in xDimension.
    # Default value: 1, meaning if xDimension = 2px than right quiet zone will be 2px.
    def  setQuietZoneRightCoef(self, value):
        self.getJavaClass().setQuietZoneRightCoef(value)

    # Returns a human-readable string representation of this Code16KParameters.
    # @return A string that represents this Code16KParameters.
    def toString(self):
        return self.getJavaClass().toString()

# DotCode parameters.
class DotCodeParameters(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        pass

    # Mask of Dotcode barcode.
    # Default value: -1.
    def  getDotCodeMask(self):
        return self.getJavaClass().getDotCodeMask()

    # Mask of Dotcode barcode.
    # Default value: -1.
    def  setDotCodeMask(self, value):
        self.getJavaClass().setDotCodeMask(value)

    # Height/Width ratio of 2D BarCode module.
    def  getAspectRatio(self):
        return self.getJavaClass().getAspectRatio()

    # Height/Width ratio of 2D BarCode module.
    def  setAspectRatio(self, value):
        self.getJavaClass().setAspectRatio(value)

    # Returns a human-readable string representation of this DotCodeParameters.
    # @return A string that represents this DotCodeParameters.
    def toString(self):
        return self.getJavaClass().toString()

# ITF parameters.
class ITFParameters(Assist.BaseJavaClass):

    itfBorderThickness = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.itfBorderThickness = Unit(self.getJavaClass().getItfBorderThickness())

    # Gets or sets an ITF border (bearer bar) thickness in Unit value.
    # Default value: 12pt.
    def  getItfBorderThickness(self):
        return self.itfBorderThickness

    # Gets or sets an ITF border (bearer bar) thickness in Unit value.
    # Default value: 12pt.
    def  setItfBorderThickness(self, value):
        self.getJavaClass().setItfBorderThickness(value.getJavaClass())
        self.itfBorderThickness = value

    # Border type of ITF barcode.
    # Default value: ITF14BorderType.BAR.
    def  getItfBorderType(self):
        return ITF14BorderType(int(self.getJavaClass().getItfBorderType()))

    # Border type of ITF barcode.
    # Default value: ITF14BorderType.BAR.
    def  setItfBorderType(self, value):
        self.getJavaClass().setItfBorderType(value.value)

    # Size of the quiet zones in xDimension.
    # Default value: 10, meaning if xDimension = 2px than quiet zones will be 20px.
    # @exception IllegalArgumentException
    # The QuietZoneCoef parameter value is less than 10.
    def  getQuietZoneCoef(self):
        return self.getJavaClass().getQuietZoneCoef()

    # Size of the quiet zones in xDimension.
    # Default value: 10, meaning if xDimension = 2px than quiet zones will be 20px.
    # @exception IllegalArgumentException
    # The QuietZoneCoef parameter value is less than 10.
    def  setQuietZoneCoef(self, value):
        self.getJavaClass().setQuietZoneCoef(value)

    # Returns a human-readable string representation of this ITFParameters.
    # @return A string that represents this ITFParameters.
    def toString(self):
        return self.getJavaClass().toString()

# QR parameters.
class QrParameters(Assist.BaseJavaClass):

    structuredAppend = None
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.structuredAppend = QrStructuredAppendParameters(self.getJavaClass().getStructuredAppend())

    # QR structured append parameters.
    def getStructuredAppend(self):
        return self.structuredAppend

    # QR structured append parameters.
    def setStructuredAppend(self, value):
        self.structuredAppend = value
        self.getJavaClass().setStructuredAppend(value.getJavaClass())

    # Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
    # about the used references for encoding the data in the symbol.
    # Current implementation consists all well known charset encodings.
    def  getQrECIEncoding(self):
        return ECIEncodings(self.getJavaClass().getQrECIEncoding())

    # Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
    # about the used references for encoding the data in the symbol.
    # Current implementation consists all well known charset encodings.
    def  setQrECIEncoding(self, value):
        self.getJavaClass().setQrECIEncoding(value.value)

    # QR symbology type of BarCode's encoding mode.
    # Default value: QREncodeMode.AUTO.
    def  getQrEncodeMode(self):
        return QREncodeMode(int(self.getJavaClass().getQrEncodeMode()))

    # QR symbology type of BarCode's encoding mode.
    # Default value: QREncodeMode.AUTO.
    def  setQrEncodeMode(self, value):
        self.getJavaClass().setQrEncodeMode(value.value)

    # QR / MicroQR selector mode. Select ForceQR for standard QR symbols, Auto for MicroQR.
    def getQrEncodeType(self):
        return QREncodeType(int(self.getJavaClass().getQrEncodeType()))

    # QR / MicroQR selector mode. Select ForceQR for standard QR symbols, Auto for MicroQR.
    def  setQrEncodeType(self, value):
        self.getJavaClass().setQrEncodeType(value.value)

    #  Level of Reed-Solomon error correction for QR barcode.
    #  From low to high: LEVEL_L, LEVEL_M, LEVEL_Q, LEVEL_H. see QRErrorLevel.
    def  getQrErrorLevel(self):
        return QRErrorLevel(int(self.getJavaClass().getQrErrorLevel()))

    #  Level of Reed-Solomon error correction for QR barcode.
    #  From low to high: LEVEL_L, LEVEL_M, LEVEL_Q, LEVEL_H. see QRErrorLevel.
    def  setQrErrorLevel(self, value):
        self.getJavaClass().setQrErrorLevel(value.value)

    # Version of QR Code.
    # From Version1 to Version40 for QR code and from M1 to M4 for MicroQr.
    # Default value is QRVersion.AUTO.
    def  getQrVersion(self):
        return QRVersion(int(self.getJavaClass().getQrVersion()))

    # Version of QR Code.
    # From Version1 to Version40 for QR code and from M1 to M4 for MicroQr.
    # Default value is QRVersion.AUTO.
    def  setQrVersion(self, value):
        self.getJavaClass().setQrVersion(value.value)

    # Height/Width ratio of 2D BarCode module.
    def  getAspectRatio(self):
        return self.getJavaClass().getAspectRatio()

    # Height/Width ratio of 2D BarCode module.
    def  setAspectRatio(self, value):
        self.getJavaClass().setAspectRatio(value)

    # Gets the encoding of codetext.
    # Default value: UTF-8
    def  getCodeTextEncoding(self):
        return self.getJavaClass().getCodeTextEncoding()

    # Sets the encoding of codetext.
    # Default value: UTF-8
    def  setCodeTextEncoding(self, value):
        self.getJavaClass().setCodeTextEncoding(value)

    # Returns a human-readable string representation of this QrParameters.
    # @return A string that represents this QrParameters.
    def toString(self):
        return self.getJavaClass().toString()

# PDF417 parameters.
class Pdf417Parameters(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        pass

    # Pdf417 symbology type of BarCode's compaction mode.
    # Default value: Pdf417CompactionMode.AUTO.
    def  getPdf417CompactionMode(self):
        return self.getJavaClass().getPdf417CompactionMode()

    # Pdf417 symbology type of BarCode's compaction mode.
    # Default value: Pdf417CompactionMode.AUTO.
    def  setPdf417CompactionMode(self, value):
        self.getJavaClass().setPdf417CompactionMode(value.value)

    # Gets or sets Pdf417 symbology type of BarCode's error correction level
    # ranging from level0 to level8, level0 means no error correction info,
    # level8 means best error correction which means a larger picture.
    def  getPdf417ErrorLevel(self):
        return self.getJavaClass().getPdf417ErrorLevel()

    # Gets or sets Pdf417 symbology type of BarCode's error correction level
    # ranging from level0 to level8, level0 means no error correction info,
    # level8 means best error correction which means a larger picture.
    def  setPdf417ErrorLevel(self, value):
        self.getJavaClass().setPdf417ErrorLevel(value.value)

    # Whether Pdf417 symbology type of BarCode is truncated (to reduce space).
    def  getPdf417Truncate(self):
        return self.getJavaClass().getPdf417Truncate()

    # Whether Pdf417 symbology type of BarCode is truncated (to reduce space).
    def  setPdf417Truncate(self, value):
        self.getJavaClass().setPdf417Truncate(value)

    # Columns count.
    def  getColumns(self):
        return self.getJavaClass().getColumns()

    # Columns count.
    def  setColumns(self, value):
        self.getJavaClass().setColumns(value)

    # Rows count.
    def  getRows(self):
        return self.getJavaClass().getRows()

    # Rows count.
    def  setRows(self, value):
        self.getJavaClass().setRows(value)

    # Height/Width ratio of 2D BarCode module.
    def  getAspectRatio(self):
        return self.getJavaClass().getAspectRatio()

    # Height/Width ratio of 2D BarCode module.
    def  setAspectRatio(self, value):
        self.getJavaClass().setAspectRatio(value)

    # Getsmacro Pdf417 barcode's file ID.
    # Used for MacroPdf417.
    def  getPdf417MacroFileID(self):
        return self.getJavaClass().getPdf417MacroFileID()

    # Sets macro Pdf417 barcode's file ID.
    # Used for MacroPdf417.
    def  setPdf417MacroFileID(self, value):
        self.getJavaClass().setPdf417MacroFileID(value)

    # Gets macro Pdf417 barcode's segment ID, which starts from 0, to MacroSegmentsCount - 1.
    def  getPdf417MacroSegmentID(self):
        return self.getJavaClass().getPdf417MacroSegmentID()

    # Sets macro Pdf417 barcode's segment ID, which starts from 0, to MacroSegmentsCount - 1.
    def  setPdf417MacroSegmentID(self, value):
        self.getJavaClass().setPdf417MacroSegmentID(value)

    # Gets macro Pdf417 barcode segments count.
    def  getPdf417MacroSegmentsCount(self):
        return self.getJavaClass().getPdf417MacroSegmentsCount()

    # Sets macro Pdf417 barcode segments count.
    def  setPdf417MacroSegmentsCount(self, value):
        self.getJavaClass().setPdf417MacroSegmentsCount(value)

    # Gets the encoding of codetext.
    # Default value: UTF-8
    def  getCodeTextEncoding(self):
        return self.getJavaClass().getCodeTextEncoding()

    # Sets the encoding of codetext.
    # Default value: UTF-8
    def  setCodeTextEncoding(self, value):
        self.getJavaClass().setCodeTextEncoding(value)

    # Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
    # about the used references for encoding the data in the symbol.
    # Current implementation consists all well known charset encodings.
    def  getPdf417ECIEncoding(self):
        return self.getJavaClass().getPdf417ECIEncoding()

    # Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
    # about the used references for encoding the data in the symbol.
    # Current implementation consists all well known charset encodings.
    def  setPdf417ECIEncoding(self, value):
        self.getJavaClass().setPdf417ECIEncoding(value)

    # Used to instruct the reader to interpret the data contained within the symbol
    # as programming for reader initialization
    # @return
    def isReaderInitialization(self):
        return self.getJavaClass().isReaderInitialization()

    # Used to instruct the reader to interpret the data contained within the symbol
    # as programming for reader initialization
    # @param value
    def setReaderInitialization(self, value):
        self.getJavaClass().setReaderInitialization(value)

    # Returns a human-readable string representation of this Pdf417Parameters.
    # @return A string that represents this Pdf417Parameters.
    def toString(self):
        return self.getJavaClass().toString()

# Supplement parameters. Used for Interleaved2of5, Standard2of5, EAN13, EAN8, UPCA, UPCE, ISBN, ISSN, ISMN.
class SupplementParameters(Assist.BaseJavaClass):

    _space = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self._space = Unit(self.getJavaClass().getSupplementSpace())

    # Supplement data following BarCode.
    def  getSupplementData(self):
        return self.getJavaClass().getSupplementData()

    # Supplement data following BarCode.
    def  setSupplementData(self, value):
        self.getJavaClass().setSupplementData(value)

    # Space between main the BarCode and supplement BarCode in Unit value.
    # @exception IllegalArgumentException
    # The Space parameter value is less than 0.
    def  getSupplementSpace(self):
        return self._space

    # Returns a human-readable string representation of this SupplementParameters.
    # @return A string that represents this SupplementParameters.
    def toString(self):
        return self.getJavaClass().toString()

# MaxiCode parameters.
class MaxiCodeParameters(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        pass

    # Gets a MaxiCode encode mode.
    def  getMaxiCodeEncodeMode(self):
        return self.getJavaClass().getMaxiCodeEncodeMode()

    # Sets a MaxiCode encode mode.
    def  setMaxiCodeEncodeMode(self, value):
        self.getJavaClass().setMaxiCodeEncodeMode(value)

    # Height/Width ratio of 2D BarCode module.
    def  getAspectRatio(self):
        return self.getJavaClass().getAspectRatio()

    # Height/Width ratio of 2D BarCode module.
    def  setAspectRatio(self, value):
        self.getJavaClass().setAspectRatio(value)

    # Returns a human-readable string representation of this MaxiCodeParameters.
    # @return A string that represents this MaxiCodeParameters.
    def toString(self):
        return self.getJavaClass().toString()

# Aztec parameters.
class AztecParameters(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        pass

    # Level of error correction of Aztec types of barcode.
    # Value should between 10 to 95.
    def  getAztecErrorLevel(self):
        return self.getJavaClass().getAztecErrorLevel()

    # Level of error correction of Aztec types of barcode.
    # Value should between 10 to 95.
    def  setAztecErrorLevel(self, value):
        self.getJavaClass().setAztecErrorLevel(value)

    # Gets or sets a Aztec Symbol mode.
    # Default value: AztecSymbolMode.AUTO.
    def  getAztecSymbolMode(self):
        return self.getJavaClass().getAztecSymbolMode()

    # Gets or sets a Aztec Symbol mode.
    # Default value: AztecSymbolMode.AUTO.
    def  setAztecSymbolMode(self, value):
        self.getJavaClass().setAztecSymbolMode(value)

    # Height/Width ratio of 2D BarCode module.
    def  getAspectRatio(self):
        return self.getJavaClass().getAspectRatio()

    # Height/Width ratio of 2D BarCode module.
    def  setAspectRatio(self, value):
        self.getJavaClass().setAspectRatio(value)

    # Gets the encoding of codetext.
    # Default value: UTF-8
    def  getCodeTextEncoding(self):
        return self.getJavaClass().getCodeTextEncoding()

    # Sets the encoding of codetext.
    # Default value: UTF-8
    def  setCodeTextEncoding(self, value):
        self.getJavaClass().setCodeTextEncoding(value)

    # Returns a human-readable string representation of this AztecParameters.
    # @return string that represents this AztecParameters.
    def toString(self):
        return self.getJavaClass().toString()

# Codabar parameters.
class CodabarParameters(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        pass

    # Get the checksum algorithm for Codabar barcodes.
    # Default value: CodabarChecksumMode.MOD_16.
    # To enable checksum calculation set value EnableChecksum.YES to property EnableChecksum.
    # See CodabarChecksumMode.
    def  getCodabarChecksumMode(self):
        return self.getJavaClass().getCodabarChecksumMode()

    # Set the checksum algorithm for Codabar barcodes.
    # Default value: CodabarChecksumMode.MOD_16.
    # To enable checksum calculation set value EnableChecksum.YES to property EnableChecksum.
    # See CodabarChecksumMode.
    def  setCodabarChecksumMode(self, value):
        self.getJavaClass().setCodabarChecksumMode(value.value)

    # Start symbol (character) of Codabar symbology.
    # Default value: CodabarSymbol.A
    def  getCodabarStartSymbol(self):
        return self.getJavaClass().getCodabarStartSymbol()

    # Start symbol (character) of Codabar symbology.
    # Default value: CodabarSymbol.A
    def  setCodabarStartSymbol(self, value):
        self.getJavaClass().setCodabarStartSymbol(value.value)

    # Stop symbol (character) of Codabar symbology.
    # Default value: CodabarSymbol.A
    def  getCodabarStopSymbol(self):
        return self.getJavaClass().getCodabarStopSymbol()

    # Stop symbol (character) of Codabar symbology.
    # Default value: CodabarSymbol.A
    def  setCodabarStopSymbol(self, value):
        self.getJavaClass().setCodabarStopSymbol(value.value)

    # Returns a human-readable string representation of this CodabarParameters.
    # @return A string that represents this CodabarParameters.
    def toString(self):
        return self.getJavaClass().toString()

# Coupon parameters. Used for UpcaGs1DatabarCoupon, UpcaGs1Code128Coupon.
class CouponParameters(Assist.BaseJavaClass):

    _space = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self._space = Unit(self.getJavaClass().getSupplementSpace())


    # Space between main the BarCode and supplement BarCode in Unit value.
    # @exception IllegalArgumentException
    # The Space parameter value is less than 0.
    def  getSupplementSpace(self):
        return self._space

    # Space between main the BarCode and supplement BarCode in Unit value.
    # @exception IllegalArgumentException
    # The Space parameter value is less than 0.
    def  setSupplementSpace(self, value):
        self.getJavaClass().setSupplementSpace(value.getJavaClass())
        self._space = value

    # Returns a human-readable string representation of this CouponParameters.
    # @return A string that represents this CouponParameters.
    def toString(self):
        return self.getJavaClass().toString()

#  Defines a particular format for text, including font face, size, and style attributes
#  where size in Unit value property.
#
#  This sample shows how to create and save a BarCode image.
#   generator = BarcodeGenerator(EncodeTypes.CODE_128)
#   generator.getParameters().getCaptionAbove().setText("CAPTION ABOOVE")
#   generator.getParameters().getCaptionAbove().setVisible(true)
#   generator.getParameters().getCaptionAbove().getFont().setStyle(FontStyle.ITALIC)
#   generator.getParameters().getCaptionAbove().getFont().getSize().setPoint(25)
class FontUnit(Assist.BaseJavaClass):
    _size = None

    def __init__(self, source):
        super().__init__(FontUnit.initFontUnit(source))
        self.init()

    @staticmethod
    def initFontUnit(source):
        if isinstance(source, FontUnit):
            return source.getJavaClass()
        return source

    def init(self):
        self._size = Unit(self.getJavaClass().getSize())

    # Gets the face name of this Font.
    def  getFamilyName(self):
        return self.getJavaClass().getFamilyName()

    # Sets the face name of this Font.
    def  setFamilyName(self, value):
        self.getJavaClass().setFamilyName(value)

    # Gets style information for this FontUnit.
    def  getStyle(self):
        return self.getJavaClass().getStyle()

    # Sets style information for this FontUnit.
    def  setStyle(self, value):
        self.getJavaClass().setStyle(value.value)

    # Gets size of this FontUnit in Unit value.
    # @exception IllegalArgumentException
    # The Size parameter value is less than or equal to 0.
    def getSize(self):
        return self._size


# Helper class for automatic codetext generation of the Extended Codetext Mode
class ExtCodetextBuilder(Assist.BaseJavaClass):

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    # Checks necessity to shield previous item by "\000000"
    #
    # @param Index Index in m_List
    # @return Necessity to shield
    def isNeedToShieldItemFromPrevECI(self, Index):
        return self.getJavaClass().isNeedToShieldItemFromPrevECI(Index)

    # Clears extended codetext items
    def clear(self):
        self.getJavaClass().clear()

    # Adds plain codetext to the extended codetext items
    #
    # @param codetext Codetext in unicode to add as extended codetext item
    def addPlainCodetext(self, codetext):
        self.getJavaClass().addPlainCodetext(codetext)

    # Adds codetext with Extended Channel Identifier
    #
    # @param ECIEncoding Extended Channel Identifier
    # @param codetext    Codetext in unicode to add as extended codetext item with Extended Channel Identifier
    def addECICodetext(self, ECIEncoding, codetext):
        self.getJavaClass().addECICodetext(ECIEncoding.value, codetext)

    # Generate extended codetext from generation items list
    #
    # @return Return string of extended codetext
    def getExtendedCodetext(self):
        return self.getJavaClass().getExtendedCodetext()

# <p>Extended codetext generator for 2D QR barcodes for ExtendedCodetext Mode of QREncodeMode</p>
# <p>Use Display2DText property of BarCodeBuilder to set visible text to removing managing characters.</p>
#
#  Example how to generate FNC1 first position for Extended Mode
#
#  //create codetext
#  lTextBuilder = QrExtCodetextBuilder()
#  lTextBuilder.addFNC1FirstPosition()
#  lTextBuilder.addPlainCodetext("000%89%%0")
#  lTextBuilder.addFNC1GroupSeparator()
#  lTextBuilder.addPlainCodetext("12345&ltFNC1&gt")
#  //generate codetext
#  lCodetext = lTextBuilder.getExtendedCodetext()
#  </pre>
#  Example how to generate FNC1 second position for Extended Mode
#  <pre>
#  //create codetext
#  lTextBuilder = QrExtCodetextBuilder()
#  lTextBuilder.addFNC1SecondPosition("12")
#  lTextBuilder.addPlainCodetext("TRUE3456")
#  //generate codetext
#  lCodetext = lTextBuilder.getExtendedCodetext()
#
#  Example how to generate multi ECI mode for Extended Mode
#
#  //create codetext
# lTextBuilder = QrExtCodetextBuilder()
# lTextBuilder.addECICodetext(ECIEncodings.Win1251, "Will")
# lTextBuilder.addECICodetext(ECIEncodings.UTF8, "Right")
# lTextBuilder.addECICodetext(ECIEncodings.UTF16BE, "Power")
# lTextBuilder.addPlainCodetext("t\\e\\\\st")
#  //generate codetext
# lCodetext = lTextBuilder.getExtendedCodetext()
class QrExtCodetextBuilder(ExtCodetextBuilder):
    javaClassName = "com.aspose.mw.barcode.MwQrExtCodetextBuilder"

    def __init__(self):
        javaQrExtCodetextBuilder = jpype.JClass(self.javaClassName)
        self.javaClass = javaQrExtCodetextBuilder()
        super().__init__(self.javaClass)
        self.init()

    def init(self):
        pass

    # Adds FNC1 in first position to the extended codetext items
    def addFNC1FirstPosition(self):
        self.getJavaClass().addFNC1FirstPosition()

    # Adds FNC1 in second position to the extended codetext items
    #
    # @param codetext Value of the FNC1 in the second position
    def addFNC1SecondPosition(self, codetext):
        self.getJavaClass().addFNC1SecondPosition(codetext)

    # Adds Group Separator (GS - '\\u001D') to the extended codetext items
    def addFNC1GroupSeparator(self):
        self.getJavaClass().addFNC1GroupSeparator()

    # Generates Extended codetext from the extended codetext list.
    #
    # @return Extended codetext as string
    def  getExtendedCodetext(self):
        return self.getJavaClass().getExtendedCodetext()

# QR structured append parameters.
class QrStructuredAppendParameters(Assist.BaseJavaClass):

    def init(self):
        pass

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()
    
    #  Gets the QR structured append mode parity data.
    def getParityByte(self):
        return self.getJavaClass().getParityByte()
    
    # Sets the QR structured append mode parity data.
    def setParityByte(self, value):
        self.getJavaClass().setParityByte(value)
    
    # Gets the index of the QR structured append mode barcode. Index starts from 0.
    def getSequenceIndicator(self):
        return self.getJavaClass().getSequenceIndicator()
    
    # Sets the index of the QR structured append mode barcode. Index starts from 0.
    def setSequenceIndicator(self, value):
        self.getJavaClass().setSequenceIndicator(value)
    
    # Gets the QR structured append mode barcodes quantity. Max value is 16.
    def getTotalCount(self):
        return self.getJavaClass().getTotalCount()
    
    # Sets the QR structured append mode barcodes quantity. Max value is 16.
    def setTotalCount(self, value):
        self.getJavaClass().setTotalCount(value)
    
    def getStateHash(self):
        return self.getJavaClass().getStateHash()

class MacroCharacter:

    # None of Macro Characters are added to barcode data
    NONE = 0

    # 05 Macro craracter is added to barcode data in first position.
    # GS1 Data Identifier ISO 15434
    # Character is translated to "[)>\u001E05\u001D" as decoded data header and "\u001E\u0004" as decoded data trailer.
    #
    # # to generate autoidentified GS1 message like this "(10)123ABC(10)123ABC" in ISO 15434 format you need:
    # generator = BarcodeGenerator(EncodeTypes.DATA_MATRIX, "10123ABC\u001D10123ABC")
    # generator.getParameters().getBarcode().getDataMatrix().setMacroCharacters(MacroCharacter.MACRO_05);
    # reader = new BarCodeReader(generator.generateBarCodeImage(), DecodeType.GS_1_DATA_MATRIX);
    # for result in reader.readBarCodes():
    #     print("BarCode CodeText: " + result.getCodeText());
    MACRO_05 = 5


    # 06 Macro craracter is added to barcode data in first position.
    # ASC MH10 Data Identifier ISO 15434
    # Character is translated to "[)>\u001E06\u001D" as decoded data header and "\u001E\u0004" as decoded data trailer.
    MACRO_06 = 6

# Specifies style information applied to text.
class FontStyle:
    
    # Normal text
    REGULAR = 0;

    # Bold text
    BOLD = 1;

    # Italic text
    ITALIC = 2;

    # Underlined text
    UNDERLINE = 4;

    # Text with a line through the middle
    STRIKEOUT = 8;

# Specifies the start or stop symbol of the Codabar barcode specification.
class CodabarSymbol(Enum):

    # Specifies character A as the start or stop symbol of the Codabar barcode specification.
    A = 65

    # Specifies character B as the start or stop symbol of the Codabar barcode specification.
    B = 66

    # Specifies character C as the start or stop symbol of the Codabar barcode specification.
    C = 67

    # Specifies character D as the start or stop symbol of the Codabar barcode specification.
    D = 68

# DataMatrix encoder's encoding mode, default to AUTO
class DataMatrixEncodeMode(Enum):

    # Automatically pick up the best encode mode for datamatrix encoding
    AUTO = 0

    # Encodes one alphanumeric or two numeric characters per byte
    ASCII = 1

    # Encode 8 bit values
    FULL = 6

    # Encode with the encoding specified in BarCodeBuilder.CodeTextEncoding
    CUSTOM = 7

    # Uses C40 encoding. Encodes Upper-case alphanumeric, Lower case and special characters
    C40 = 8

    # Uses TEXT encoding. Encodes Lower-case alphanumeric, Upper case and special characters
    TEXT = 9

    # Uses EDIFACT encoding. Uses six bits per character, encodes digits, upper-case letters, and many punctuation marks, but has no support for lower-case letters.
    EDIFACT = 10

    # Uses ANSI X12 encoding.
    ANSIX12 = 11

# Specifies the style of dashed border lines.
class BorderDashStyle(Enum):
    # Specifies a solid line.
    SOLID = 0

    # Specifies a line consisting of dashes.
    DASH = 1

    # Specifies a line consisting of dots.
    DOT = 2

    # Specifies a line consisting of a repeating pattern of dash-dot.
    DASH_DOT = 3

    #  Specifies a line consisting of a repeating pattern of dash-dot-dot.
    DASH_DOT_DOT = 4

# ITF14 barcode's border type
class ITF14BorderType(Enum):

    # NO border enclosing the barcode
    NONE = 0

    # FRAME enclosing the barcode
    FRAME = 1

    # Tow horizontal bars enclosing the barcode
    BAR = 2

    # FRAME enclosing the barcode
    FRAME_OUT = 3

    # Tow horizontal bars enclosing the barcode
    BAR_OUT = 4

# Encoding mode for QR barcodes. It is recomended to Use AUTO with CodeTextEncoding = Encoding.UTF8 for latin symbols or digits and UTF_8_BOM for unicode symbols.
class QREncodeMode(Enum):

    # Encode codetext as is non-unicode charset. If there is any unicode character, the codetext will be encoded with value which is set in CodeTextEncoding.
    AUTO = 0

    # Encode codetext as plain bytes. If it detects any unicode character, the character will be encoded as two bytes, lower byte first.
    BYTES = 1

    # Encode codetext with UTF8 encoding with first ByteOfMark character.
    UTF_8_BOM = 2

    # Encode codetext with UTF8 encoding with first ByteOfMark character. It can be problems with some barcode scaners.
    UTF_16_BEBOM = 3

    # Encode codetext with value set in the ECI_ENCODING property. It can be problems with some old (pre 2006) barcode scaners.
    # Example how to use ECI encoding
    #     generator = BarcodeGenerator(EncodeTypes.QR)
    #     generator.setCodeText("12345TEXT")
    #     generator.getParameters().getBarcode().getQR().setQrEncodeMode(QREncodeMode.ECI_ENCODING)
    #     generator.getParameters().getBarcode().getQR().setQrEncodeType(QREncodeType.FORCE_QR)
    #     generator.getParameters().getBarcode().getQR().setQrECIEncoding(ECIEncodings.UTF8)
    #     generator.save("test.png", "PNG")
    ECI_ENCODING = 4

    # Extended Channel mode which supports FNC1 first position, FNC1 second position and multi ECI modes.
    # It is better to use QrExtCodetextBuilder for extended codetext generation.
    # Use Display2DText property to set visible text to removing managing characters.
    # Encoding Principles:
    # All symbols "\" must be doubled "\\" in the codetext.
    # FNC1 in first position is set in codetext as as "&lt;FNC1&gt;"
    # FNC1 in second position is set in codetext as as "&lt;FNC1(value)&gt;". The value must be single symbols (a-z, A-Z) or digits from 0 to 99.
    # Group Separator for FNC1 modes is set as 0x1D character '\\u001D'
    #  If you need to insert "&lt;FNC1&gt;" string into barcode write it as "&lt;\FNC1&gt;"
    # ECI identifiers are set as single slash and six digits identifier "\000026" - UTF8 ECI identifier
    # TO disable current ECI mode and convert to default JIS8 mode zero mode ECI indetifier is set. "\000000"
    # All unicode characters after ECI identifier are automatically encoded into correct character codeset.
    #  Example how to use FNC1 first position in Extended Mode
    #      textBuilder = QrExtCodetextBuilder()
    #      textBuilder.addPlainCodetext("000%89%%0")
    #      textBuilder.addFNC1GroupSeparator()
    #      textBuilder.addPlainCodetext("12345&lt;FNC1&gt;")
    #      //generate barcode
    #      generator = BarcodeGenerator(EncodeTypes.QR)
    #      generator.setCodeText($textBuilder.getExtendedCodetext())
    #      generator.getParameters().getBarcode().getQR().setQrEncodeMode(QREncodeMode.EXTENDED_CODETEXT)
    #      generator.getParameters().getBarcode().getCodeTextParameters().setTwoDDisplayText("My Text")
    #      generator.save("d:/test.png", "PNG")
    # This sample shows how to use FNC1 second position in Extended Mode.
    #    //create codetext
    #    textBuilder = QrExtCodetextBuilder()
    #    textBuilder.addFNC1SecondPosition("12")
    #    textBuilder.addPlainCodetext("TRUE3456")
    #    //generate barcode
    #    generator = BarcodeGenerator(EncodeTypes.QR)
    #    generator.setCodeText($textBuilder.getExtendedCodetext())
    #    generator.getParameters().getBarcode().getCodeTextParameters().setTwoDDisplayText("My Text")
    #    generator.save("d:/test.png", "PNG")
    #    This sample shows how to use multi ECI mode in Extended Mode.
    #   //create codetext
    #    textBuilder = QrExtCodetextBuilder()
    #    textBuilder.addECICodetext(ECIEncodings.Win1251, "Will")
    #    textBuilder.addECICodetext(ECIEncodings.UTF8, "Right")
    #    textBuilder.addECICodetext(ECIEncodings.UTF16BE, "Power")
    #    textBuilder.addPlainCodetext("t\e\\st")
    #   //generate barcode
    #    generator = BarcodeGenerator(EncodeTypes.QR)
    #    generator.setCodeText($textBuilder.getExtendedCodetext())
    #    generator.getParameters().getBarcode().getQR().setQrEncodeMode(QREncodeMode.EXTENDED_CODETEXT)
    #    generator.getParameters().getBarcode().getCodeTextParameters().setTwoDDisplayText("My Text")
    #    generator.save("d:/test.png", "PNG")
    EXTENDED_CODETEXT = 5

# Specify the type of the ECC to encode.
class DataMatrixEccType(Enum):

    # Specifies that encoded Ecc type is defined by default Reed-Solomon error correction or ECC 200.
    ECC_AUTO = 0

    # Specifies that encoded Ecc type is defined ECC 000.
    ECC_000 = 1

    # Specifies that encoded Ecc type is defined ECC 050.
    ECC_050 = 2

    # Specifies that encoded Ecc type is defined ECC 080.
    ECC_080 = 3

    # Specifies that encoded Ecc type is defined ECC 100.
    ECC_100 = 4

    # Specifies that encoded Ecc type is defined ECC 140.
    ECC_140 = 5

    # Specifies that encoded Ecc type is defined ECC 200. Recommended to use.
    ECC_200 = 6

# Version of QR Code.
# From Version1 to Version40 for QR code and from M1 to M4 for MicroQr.
class QRVersion(Enum):

    # Specifies to automatically pick up the best version for QR.
    # This is default value.
    AUTO = 0

    # Specifies version 1 with 21 x 21 modules.
    VERSION_01 = 1

    # Specifies version 2 with 25 x 25 modules.
    VERSION_02 = 2

    # Specifies version 3 with 29 x 29 modules.
    VERSION_03 = 3

    # Specifies version 4 with 33 x 33 modules.
    VERSION_04 = 4

    # Specifies version 5 with 37 x 37 modules.
    VERSION_05 = 5

    # Specifies version 6 with 41 x 41 modules.
    VERSION_06 = 6

    # Specifies version 7 with 45 x 45 modules.
    VERSION_07 = 7

    # Specifies version 8 with 49 x 49 modules.
    VERSION_08 = 8

    # Specifies version 9 with 53 x 53 modules.
    VERSION_09 = 9

    # Specifies version 10 with 57 x 57 modules.
    VERSION_10 = 10

    # Specifies version 11 with 61 x 61 modules.
    VERSION_11 = 11

    # Specifies version 12 with 65 x 65 modules.
    VERSION_12 = 12

    # Specifies version 13 with 69 x 69 modules.
    VERSION_13 = 13

    # Specifies version 14 with 73 x 73 modules.
    VERSION_14 = 14

    # Specifies version 15 with 77 x 77 modules.
    VERSION_15 = 15

    # Specifies version 16 with 81 x 81 modules.
    VERSION_16 = 16

    # Specifies version 17 with 85 x 85 modules.
    VERSION_17 = 17

    # Specifies version 18 with 89 x 89 modules.
    VERSION_18 = 18

    # Specifies version 19 with 93 x 93 modules.
    VERSION_19 = 19

    # Specifies version 20 with 97 x 97 modules.
    VERSION_20 = 20

    # Specifies version 21 with 101 x 101 modules.
    VERSION_21 = 21

    # Specifies version 22 with 105 x 105 modules.
    VERSION_22 = 22

    # Specifies version 23 with 109 x 109 modules.
    VERSION_23 = 23

    # Specifies version 24 with 113 x 113 modules.
    VERSION_24 = 24

    # Specifies version 25 with 117 x 117 modules.
    VERSION_25 = 25

    # Specifies version 26 with 121 x 121 modules.
    VERSION_26 = 26

    # Specifies version 27 with 125 x 125 modules.
    VERSION_27 = 27

    # Specifies version 28 with 129 x 129 modules.
    VERSION_28 = 28

    # Specifies version 29 with 133 x 133 modules.
    VERSION_29 = 29

    # Specifies version 30 with 137 x 137 modules.
    VERSION_30 = 30

    # Specifies version 31 with 141 x 141 modules.
    VERSION_31 = 31

    # Specifies version 32 with 145 x 145 modules.
    VERSION_32 = 32

    # Specifies version 33 with 149 x 149 modules.
    VERSION_33 = 33

    # Specifies version 34 with 153 x 153 modules.
    VERSION_34 = 34

    # Specifies version 35 with 157 x 157 modules.
    VERSION_35 = 35

    # Specifies version 36 with 161 x 161 modules.
    VERSION_36 = 36

    # Specifies version 37 with 165 x 165 modules.
    VERSION_37 = 37

    # Specifies version 38 with 169 x 169 modules.
    VERSION_38 = 38

    # Specifies version 39 with 173 x 173 modules.
    VERSION_39 = 39

    # Specifies version 40 with 177 x 177 modules.
    VERSION_40 = 40

    # Specifies version M1 for Micro QR with 11 x 11 modules.
    VERSION_M1 = 101

    # Specifies version M2 for Micro QR with 13 x 13 modules.
    VERSION_M2 = 102

    # Specifies version M3 for Micro QR with 15 x 15 modules.
    VERSION_M3 = 103

    # Specifies version M4 for Micro QR with 17 x 17 modules.
    VERSION_M4 = 104

# Specifies the Aztec symbol mode.
#
#      generator = BarcodeGenerator(EncodeTypes.AZTEC)
#      generator.setCodeText("125")
#      generator.getParameters().getBarcode().getAztec().setAztecSymbolMode(AztecSymbolMode.RUNE)
#      generator.save("test.png", "PNG")
class AztecSymbolMode(Enum):

    # Specifies to automatically pick up the best symbol (COMPACT or FULL-range) for Aztec.
    # This is default value.
    AUTO = 0

    # Specifies the COMPACT symbol for Aztec.
    # Aztec COMPACT symbol permits only 1, 2, 3 or 4 layers.
    COMPACT = 1

    # Specifies the FULL-range symbol for Aztec.
    # Aztec FULL-range symbol permits from 1 to 32 layers.
    FULL_RANGE = 2

    # Specifies the RUNE symbol for Aztec.
    # Aztec Runes are a series of small but distinct machine-readable marks. It permits only number value from 0 to 255.
    RUNE = 3

# pdf417 barcode's error correction level, from level 0 to level 9, level 0 means no error correction, level 9 means best error correction
class Pdf417ErrorLevel(Enum):

    # level = 0.
    LEVEL_0 = 0

    # level = 1.
    LEVEL_1 = 1

    # level = 2.
    LEVEL_2 = 2

    # level = 3.
    LEVEL_3 = 3

    # level = 4.
    LEVEL_4 = 4

    # level = 5.
    LEVEL_5 = 5
    # level = 6.

    LEVEL_6 = 6

    # level = 7.
    LEVEL_7 = 7

    # level = 8.
    LEVEL_8 = 8

# Pdf417 barcode's compation mode
class Pdf417CompactionMode(Enum):

    # auto detect compation mode
    AUTO = 0

    # text compaction
    TEXT = 1

    # numeric compaction mode
    NUMERIC = 2

    # binary compaction mode
    BINARY = 3

# Level of Reed-Solomon error correction. From low to high: LEVEL_L, LEVEL_M, LEVEL_Q, LEVEL_H.
class QRErrorLevel(Enum):

    # Allows recovery of 7% of the code text
    LEVEL_L = 0

    # Allows recovery of 15% of the code text
    LEVEL_M = 1

    # Allows recovery of 25% of the code text
    LEVEL_Q = 2

    # Allows recovery of 30% of the code text
    LEVEL_H = 3

# QR / MicroQR selector mode. Select FORCE_QR for standard QR symbols, AUTO for MicroQR.
# FORCE_MICRO_QR is used for strongly MicroQR symbol generation if it is possible.
class QREncodeType(Enum):

    # Mode starts barcode version negotiation from MicroQR V1
    AUTO = 0

    # Mode starts barcode version negotiation from QR V1
    FORCE_QR = 1

    # Mode starts barcode version negotiation from from MicroQR V1 to V4. If data cannot be encoded into MicroQR, exception is thrown.
    FORCE_MICRO_QR = 2

# Specifies the checksum algorithm for Codabar
class CodabarChecksumMode(Enum):

    # Specifies Mod 10 algorithm for Codabar.
    MOD_10 = 0

    # Specifies Mod 16 algorithm for Codabar (recomended AIIM).
    MOD_16 = 1

# Codetext location
class CodeLocation(Enum):

    # Codetext below barcode.
    BELOW = 0

    # Codetext above barcode.
    ABOVE = 1

    # Hide codetext.
    NONE = 2

# Font size mode.
class FontMode(Enum):

    # Automatically calculate Font size based on barcode size.
    AUTO = 0

    # Use Font sized defined by user.
    MANUAL = 1

# Text alignment.
class TextAlignment(Enum):

    # Left position.
    LEFT = 0

    # Center position.
    CENTER = 1

    # Right position.
    RIGHT = 2

# Specifies the different types of automatic sizing modes.
# Default value is AutoSizeMode.NONE.
# This sample shows how to create and save a BarCode image.
#  generator = BarcodeGenerator(EncodeTypes.DATA_MATRIX)
#  generator.setAutoSizeMode(AutoSizeMode.NEAREST)
#  generator.getBarCodeWidth().setMillimeters(50)
#  generator.getBarCodeHeight().setInches(1.3f)
#  generator.save("test.png", "PNG")
class AutoSizeMode(Enum):

    # Automatic resizing is disabled. Default value.
    NONE = 0

    # Barcode resizes to nearest lowest possible size
    # which are specified by BarCodeWidth and BarCodeHeight properties.
    NEAREST = 1

    #  Resizes barcode to specified size with little scaling
    #  but it can be little damaged in some cases
    #  because using interpolation for scaling.
    #  Size can be specified by BarcodeGenerator.BarCodeWidth
    #  and BarcodeGenerator.BarCodeHeight properties.
    #
    #  This sample shows how to create and save a BarCode image in Scale mode.
    #
    #      generator = BarcodeGenerator( EncodeTypes.DATA_MATRIX)
    #      generator.getParameters().getBarcode().setAutoSizeMode(AutoSizeMode.INTERPOLATION)
    #      generator.getParameters().getBarcode().getBarCodeWidth().setMillimeters(50)
    #      generator.getParameters().getBarcode().getBarCodeHeight().setInches(1.3)
    #      generator.save("test.png", "PNG)
    INTERPOLATION = 2

# Specifies the unit of measure for the given data.
class GraphicsUnit(Enum):

    # Specifies the world coordinate system unit as the unit of measure.
    WORLD = 0

    # Specifies the unit of measure of the display device. Typically pixels for video displays, and 1/100 inch for printers.
    DISPLAY = 1

    # 	Specifies a device pixel as the unit of measure.
    PIXEL = 2

    # Specifies a printer's point  = 1/72 inch) as the unit of measure.
    POINT = 3

    # Specifies the inch as the unit of measure.
    INCH = 4

    # Specifies the document unit  = 1/300 inch) as the unit of measure.
    DOCUMENT = 5

    # Specifies the millimeter as the unit of measure.
    MILLIMETER = 6

# Specifies the type of barcode to encode.
class EncodeTypes(Enum):

    # Unspecified encode type.
    NONE = -1

    # Specifies that the data should be encoded with CODABAR barcode specification
    CODABAR = 0

    # Specifies that the data should be encoded with CODE 11 barcode specification
    CODE_11 = 1

    # Specifies that the data should be encoded with Standard CODE 39 barcode specification
    CODE_39_STANDARD = 2

    # Specifies that the data should be encoded with Extended CODE 39 barcode specification
    CODE_39_EXTENDED = 3

    # Specifies that the data should be encoded with Standard CODE 93 barcode specification
    CODE_93_STANDARD = 4

    # Specifies that the data should be encoded with Extended CODE 93 barcode specification
    CODE_93_EXTENDED = 5

    # Specifies that the data should be encoded with CODE 128 barcode specification
    CODE_128 = 6

    # Specifies that the data should be encoded with GS1 Code 128 barcode specification. The codetext must contains parentheses for AI.
    GS_1_CODE_128 = 7

    # Specifies that the data should be encoded with EAN-8 barcode specification
    EAN_8 = 8

    # Specifies that the data should be encoded with EAN-13 barcode specification
    EAN_13 = 9

    # Specifies that the data should be encoded with EAN14 barcode specification
    EAN_14 = 10

    # Specifies that the data should be encoded with SCC14 barcode specification
    SCC_14 = 11

    # Specifies that the data should be encoded with SSCC18 barcode specification
    SSCC_18 = 12

    # Specifies that the data should be encoded with UPC-A barcode specification
    UPCA = 13

    # Specifies that the data should be encoded with UPC-E barcode specification
    UPCE = 14

    # Specifies that the data should be encoded with isBN barcode specification
    ISBN = 15

    # Specifies that the data should be encoded with ISSN barcode specification
    ISSN = 16

    # Specifies that the data should be encoded with ISMN barcode specification
    ISMN = 17

    # Specifies that the data should be encoded with Standard 2 of 5 barcode specification
    STANDARD_2_OF_5 = 18

    # Specifies that the data should be encoded with INTERLEAVED 2 of 5 barcode specification
    INTERLEAVED_2_OF_5 = 19

    # Represents Matrix 2 of 5 BarCode
    MATRIX_2_OF_5 = 20

    # Represents Italian Post 25 barcode.
    ITALIAN_POST_25 = 21

    # Represents IATA 2 of 5 barcode.IATA (International Air Transport Assosiation) uses this barcode for the management of air cargo.
    IATA_2_OF_5 = 22

    # Specifies that the data should be encoded with ITF14 barcode specification
    ITF_14 = 23

    # Represents ITF-6  Barcode.
    ITF_6 = 24

    # Specifies that the data should be encoded with MSI Plessey barcode specification
    MSI = 25

    # Represents VIN (Vehicle Identification Number) Barcode.
    VIN = 26

    # Represents Deutsch Post barcode, This EncodeType is also known as Identcode,CodeIdentcode,German Postal 2 of 5 Identcode,
    # Deutsch Post AG Identcode, Deutsch Frachtpost Identcode,  Deutsch Post AG (DHL)
    DEUTSCHE_POST_IDENTCODE = 27

    # Represents Deutsch Post Leitcode Barcode,also known as German Postal 2 of 5 Leitcode, CodeLeitcode, Leitcode, Deutsch Post AG (DHL).
    DEUTSCHE_POST_LEITCODE = 28

    # Represents OPC(Optical Product Code) Barcode,also known as , VCA Barcode VCA OPC, Vision Council of America OPC Barcode.
    OPC = 29

    # Represents PZN barcode.This EncodeType is also known as Pharmacy central number, Pharmazentralnummer
    PZN = 30

    # Represents Code 16K barcode.
    CODE_16_K = 31

    # Represents Pharmacode barcode.
    PHARMACODE = 32

    # 2D barcode symbology DataMatrix
    DATA_MATRIX = 33

    # Specifies that the data should be encoded with QR Code barcode specification
    QR = 34

    # Specifies that the data should be encoded with Aztec barcode specification
    AZTEC = 35

    # Specifies that the data should be encoded with Pdf417 barcode specification
    PDF_417 = 36

    # Specifies that the data should be encoded with MacroPdf417 barcode specification
    MACRO_PDF_417 = 37

    # 2D barcode symbology DataMatrix with GS1 string format
    GS_1_DATA_MATRIX = 48

    # Specifies that the data should be encoded with MicroPdf417 barcode specification
    MICRO_PDF_417 = 55

    # 2D barcode symbology QR with GS1 string format
    GS_1_QR = 56

    # Specifies that the data should be encoded with MaxiCode barcode specification
    MAXI_CODE = 57

    # Specifies that the data should be encoded with DotCode barcode specification
    DOT_CODE = 60

    # Represents Australia Post Customer BarCode
    AUSTRALIA_POST = 38

    # Specifies that the data should be encoded with Postnet barcode specification
    POSTNET = 39

    # Specifies that the data should be encoded with Planet barcode specification
    PLANET = 40

    # Specifies that the data should be encoded with USPS OneCode barcode specification
    ONE_CODE = 41

    # Represents RM4SCC barcode. RM4SCC (Royal Mail 4-state Customer Code) is used for automated mail sort process in UK.
    RM_4_SCC = 42

    # Specifies that the data should be encoded with GS1 Databar omni-directional barcode specification.
    DATABAR_OMNI_DIRECTIONAL = 43

    # Specifies that the data should be encoded with GS1 Databar truncated barcode specification.
    DATABAR_TRUNCATED = 44

    # Represents GS1 DATABAR limited barcode.
    DATABAR_LIMITED = 45

    # Represents GS1 Databar expanded barcode.
    DATABAR_EXPANDED = 46

    # Represents GS1 Databar expanded stacked barcode.
    DATABAR_EXPANDED_STACKED = 52

    # Represents GS1 Databar stacked barcode.
    DATABAR_STACKED = 53

    # Represents GS1 Databar stacked omni-directional barcode.
    DATABAR_STACKED_OMNI_DIRECTIONAL = 54

    # Specifies that the data should be encoded with Singapore Post Barcode barcode specification
    SINGAPORE_POST = 47

    # Specifies that the data should be encoded with Australian Post Domestic eParcel Barcode barcode specification
    AUSTRALIAN_POSTE_PARCEL = 49

    # Specifies that the data should be encoded with Swiss Post Parcel Barcode barcode specification. Supported types: Domestic Mail, International Mail, Additional Services (new)
    SWISS_POST_PARCEL = 50

    # Represents Patch code barcode
    PATCH_CODE = 51

    # Specifies that the data should be encoded with Code32 barcode specification
    CODE_32 = 58

    # Specifies that the data should be encoded with DataLogic 2 of 5 barcode specification
    DATA_LOGIC_2_OF_5 = 59

    # Specifies that the data should be encoded with Dutch KIX barcode specification
    DUTCH_KIX = 61

    # Specifies that the data should be encoded with UPC coupon with GS1-128 Extended Code barcode specification.
    # An example of the input string:
    # BarCodeBuilder.setCodetext("514141100906(8102)03"),
    # where UPCA part is "514141100906", GS1Code128 part is (8102)03.
    UPCA_GS_1_CODE_128_COUPON = 62

    # Specifies that the data should be encoded with UPC coupon with GS1 DataBar addition barcode specification.
    # An example of the input string:
    # BarCodeBuilder.setCodetext("514141100906(8110)106141416543213500110000310123196000"),
    # where UPCA part is "514141100906", DATABAR part is "(8110)106141416543213500110000310123196000".
    # To change the caption, use barCodeBuilder.getCaptionAbove().setText("company prefix + offer code")
    UPCA_GS_1_DATABAR_COUPON = 63

    # Specifies that the data should be encoded with Codablock-F barcode specification.
    CODABLOCK_F = 64

    # Specifies that the data should be encoded with GS1 Codablock-F barcode specification. The codetext must contains parentheses for AI.
    GS_1_CODABLOCK_F = 65

# PatchCode format. Choose PatchOnly to generate single PatchCode. Use page format to generate Patch page with PatchCodes as borders
class PatchFormat(Enum):

    # Generates PatchCode only
    PATCH_ONLY = 0

    # Generates A4 format page with PatchCodes as borders and optional QR in the center
    A4 = 1

    # Generates A4 landscape format page with PatchCodes as borders and optional QR in the center
    A4_LANDSCAPE = 2

    # Generates US letter format page with PatchCodes as borders and optional QR in the center
    US_LETTER = 3

    # Generates US letter landscape format page with PatchCodes as borders and optional QR in the center
    US_LETTER_LANDSCAPE = 4

# Extended Channel Interpretation Identifiers. It is used to tell the barcode reader details
# about the used references for encoding the data in the symbol.
# Current implementation consists all well known charset encodings.
# Currently, it is used only for QR 2D barcode.
#
# Example how to use ECI encoding
#
#     generator = BarcodeGenerator(EncodeTypes.QR)
#     generator.setCodeText("12345TEXT")
#     generator.getParameters().getBarcode().getQR().setQrEncodeMode(QREncodeMode.ECI_ENCODING)
#     generator.getParameters().getBarcode().getQR().setQrEncodeType(QREncodeType.FORCE_QR)
#     generator.getParameters().getBarcode().getQR().setQrECIEncoding(ECIEncodings.UTF_8)
#     generator.save("test.png", "PNG")
class ECIEncodings(Enum):

    # ISO/IEC 8859-1 Latin alphabet No. 1 encoding. ECI Id:"\000003"
    ISO_8859_1 = 3

    # ISO/IEC 8859-2 Latin alphabet No. 2 encoding. ECI Id:"\000004"
    ISO_8859_2 = 4

    # ISO/IEC 8859-3 Latin alphabet No. 3 encoding. ECI Id:"\000005"
    ISO_8859_3 = 5

    # ISO/IEC 8859-4 Latin alphabet No. 4 encoding. ECI Id:"\000006"
    ISO_8859_4 = 6

    # ISO/IEC 8859-5 Latin/Cyrillic alphabet encoding. ECI Id:"\000007"
    ISO_8859_5 = 7

    # ISO/IEC 8859-6 Latin/Arabic alphabet encoding. ECI Id:"\000008"
    ISO_8859_6 = 8

    # ISO/IEC 8859-7 Latin/Greek alphabet encoding. ECI Id:"\000009"
    ISO_8859_7 = 9

    # ISO/IEC 8859-8 Latin/Hebrew alphabet encoding. ECI Id:"\000010"
    ISO_8859_8 = 10

    # ISO/IEC 8859-9 Latin alphabet No. 5 encoding. ECI Id:"\000011"
    ISO_8859_9 = 11

    # ISO/IEC 8859-10 Latin alphabet No. 6 encoding. ECI Id:"\000012"
    ISO_8859_10 = 12

    # ISO/IEC 8859-11 Latin/Thai alphabet encoding. ECI Id:"\000013"
    ISO_8859_11 = 13

    # ISO/IEC 8859-13 Latin alphabet No. 7 (Baltic Rim) encoding. ECI Id:"\000015"
    ISO_8859_13 = 15

    # ISO/IEC 8859-14 Latin alphabet No. 8 (Celtic) encoding. ECI Id:"\000016"
    ISO_8859_14 = 16

    # ISO/IEC 8859-15 Latin alphabet No. 9 encoding. ECI Id:"\000017"
    ISO_8859_15 = 17

    # ISO/IEC 8859-16 Latin alphabet No. 10 encoding. ECI Id:"\000018"
    ISO_8859_16 = 18

    # Shift JIS (JIS X 0208 Annex 1 + JIS X 0201) encoding. ECI Id:"\000020"
    Shift_JIS = 20

    # Windows 1250 Latin 2 (Central Europe) encoding. ECI Id:"\000021"
    Win1250 = 21

    # Windows 1251 Cyrillic encoding. ECI Id:"\000022"
    Win1251 = 22

    # Windows 1252 Latin 1 encoding. ECI Id:"\000023"
    Win1252 = 23

    # Windows 1256 Arabic encoding. ECI Id:"\000024"
    Win1256 = 24

    # ISO/IEC 10646 UCS-2 (High order byte first) encoding. ECI Id:"\000025"
    UTF16BE = 25

    # ISO/IEC 10646 UTF-8 encoding. ECI Id:"\000026"
    UTF8 = 26

    # ISO/IEC 646:1991 International Reference Version of ISO 7-bit coded character set encoding. ECI Id:"\000027"
    US_ASCII = 27

    # Big 5 (Taiwan) Chinese Character Set encoding. ECI Id:"\000028"
    Big5 = 28

    # GB (PRC) Chinese Character Set encoding. ECI Id:"\000029"
    GB18030 = 29

    # Korean Character Set encoding. ECI Id:"\000030"
    EUC_KR = 30

    # <p>No Extended Channel Interpretation/p>
    NONE = 0

# Enable checksum during generation for 1D barcodes.
# Default is treated as Yes for symbologies which must contain checksum, as No where checksum only possible.
# Checksum never used: Codabar
# Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN
# Checksum always used: Rest symbologies
class EnableChecksum(Enum):
    
    # If checksum is required by the specification - it will be attached.
    DEFAULT = 0
    
    # Always use checksum if possible.
    YES = 1
    
    # Do not use checksum.
    NO = 2


# Enable checksum during generation for 1D barcodes.
# Default is treated as Yes for symbologies which must contain checksum, as No where checksum only possible.
# Checksum never used: Codabar
# Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN
# Checksum always used: Rest symbologies

class EnableChecksum:

    # If checksum is required by the specification - it will be attached.
    DEFAULT = 0

    # Always use checksum if possible.
    YES = 1


    # Do not use checksum.
    NO = 2

# Specifies the file format of the image.
class BarCodeImageFormat:

    # Specifies the W3C Portable Network Graphics (PNG) image format.
    PNG = "PNG"

    # Specifies the Joint Photographic Experts Group (JPEG) image format.
    JPEG = "JPEG"

    # Specifies the bitmap (BMP) image format.
    BMP = "BMP"

    # Specifies the Graphics Interchange Format (GIF) image format.
    GIF = "GIF"