import jpype
import base64
from . import Assist

is_array = lambda var: isinstance(var, (list, tuple))
import os
import logging
from enum import Enum

# BarCodeReader encapsulates an image which may contain one or several barcodes, it then can perform ReadBarCodes operation to detect barcodes.
# This sample shows how to detect Code39 and Code128 barcodes.
# reader = BarCodeReader("test.png", null,  [DecodeType.CODE_39_STANDARD, DecodeType.CODE_128])
# for result in reader.readBarCodes():
#    print("BarCode Type: " + result.getCodeTypeName())
#    print("BarCode CodeText: " + result.getCodeText())
class BarcodeReader (Assist.BaseJavaClass):
    qualitySettings = None
    barcodeRegion = None
    code128DataPortions = None
    recognizedResults = None

    javaClassName = "com.aspose.mw.barcode.recognition.MwBarcodeReader"

    # Initializes a new instance of the BarCodeReader
    # @param image encoded as base64 string or path to image
    # @param rectangles array of object by type Rectangle
    # @param decodeTypes the array of objects by DecodeType
    def __init__(self, image, rectangles, decodeTypes):
        if BarcodeReader.isPath(image):
            image = BarcodeReader.loadImage(image)
        if not(rectangles is None):
            if not( is_array(rectangles)):
                rectangles = [rectangles.toString()]
            else:
                i = 0
                while (i < len(rectangles)):
                    rectangles[i] = rectangles[i].toString()
                    i =  i + 1
        if(decodeTypes != None):
            if not(is_array(decodeTypes)):
                decodeTypes = [decodeTypes]
            i = 0
            while (i < len(decodeTypes)):
                decodeTypes[i] = str(decodeTypes[i].value)
                i += 1
        try:
            java_link = jpype.JClass("com.aspose.mw.barcode.recognition.MwBarcodeReader")
            javaClass = java_link(image, rectangles, decodeTypes)
            super().__init__(javaClass)
            self.init()
        except Exception:
            logging.error("Invalid arguments")
            raise

    @staticmethod
    def isPath(image):
        if (image is not None) and (len(image) < 256 and ('/' in image or '\\' in image)):
            if(os.path.exists(image)):
                return True
        return False

    # Determines whether any of the given decode types is included into
    # @param ...decodeTypes Types to verify.
    # @return bool Value is a true if any types are included into.
    def containsAny(self, decodeTypes):
        i = 0
        while(i < len(decodeTypes)):
            decodeTypes[i] = str(decodeTypes[i].value)
            i += 1
        return self.getJavaClass().containsAny(decodeTypes)

    def loadImage(image):
        is_path_to_image = False
        is_path_to_image = os.path.exists(image)

        if (is_path_to_image):
            image_file= open(image,"rb")
            image_data_binary = image_file.read()
            return (base64.b64encode(image_data_binary)).decode('ascii')
        else:
            return image

    def convertToString(arg):
        if isinstance(arg, int):
            return str(arg)
        elif (isinstance(arg, Assist.Rectangle)):
            return "{[" + arg.toString() + "]}"
        elif (is_array(arg)):
            areasString = "{"

            size = len(arg)
            i = 0
            while i <size:
                areasString += "[" + arg[i].toString() + "]"
                i += 1

            areasString += "}"

            return areasString
        else:
            return arg

    def init(self):
        self.qualitySettings = QualitySettings(self.getJavaClass().getQualitySettings())

    # Gets file name which was assigned by user
    # @return file name
    def getFileName(self):
        return self.getJavaClass().getFileName()

    # Gets the timeout of recognition process in milliseconds.
    # reader = BarCodeReader("test.png", null, null)
    # reader.setTimeout(5000)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    # @return The timeout.
    def getTimeout(self):
        return self.getJavaClass().getTimeout()

    # Sets the timeout of recognition process in milliseconds.
    # reader = BarCodeReader("test.png", null, null)
    # reader.setTimeout(5000)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    # @param value The timeout.
    def setTimeout(self, value):
        self.getJavaClass().setTimeout(value)

    # Enable checksum validation during recognition for 1D barcodes.
    # Default is treated as Yes for symbologies which must contain checksum, as No where checksum only possible.
    # Checksum never used: Codabar
    # Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN
    # Checksum always used: Rest symbologies
    # This sample shows influence of ChecksumValidation on recognition quality and results
    # generator = BarcodeGenerator(EncodeTypes.EAN_13, "1234567890128")
    # generator.save("test.png")
    # reader = BarCodeReader("test.png", null,  DecodeType.EAN_13)
    # //checksum disabled
    # reader.setChecksumValidation(ChecksumValidation.OFF)
    # for result in reader.readBarCodes():
    #     print("BarCode CodeText: " + result.getCodeText())
    #     print("BarCode Value: " + result.getExtended().getOneD().getValue())
    #     print("BarCode Checksum: " + result.getExtended().getOneD().getCheckSum())
    # reader = BarCodeReader("test.png", null,  DecodeType.EAN_13)
    # //checksum enabled
    # reader.setChecksumValidation(ChecksumValidation.ON)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    #    print("BarCode Value: " + result.getExtended().getOneD().getValue())
    #    print("BarCode Checksum: " + result.getExtended().getOneD().getCheckSum())
    # The checksum validation flag.
    def getChecksumValidation(self):
        return ChecksumValidation(int(self.getJavaClass().getChecksumValidation()))

    # Enable checksum validation during recognition for 1D barcodes.
    # Default is treated as Yes for symbologies which must contain checksum, as No where checksum only possible.
    # Checksum never used: Codabar
    # Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN
    # Checksum always used: Rest symbologies
    # This sample shows influence of ChecksumValidation on recognition quality and results
    # generator = BarcodeGenerator(EncodeTypes.EAN_13, "1234567890128")
    # generator.save("test.png")
    # reader = BarCodeReader("test.png", null,  DecodeType.EAN_13)
    # //checksum disabled
    # reader.setChecksumValidation(ChecksumValidation.OFF)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    #    print("BarCode Value: " + result.getExtended().getOneD().getValue())
    #    print("BarCode Checksum: " + result.getExtended().getOneD().getCheckSum())
    # reader = BarCodeReader("test.png", null,  DecodeType.EAN_13)
    # //checksum enabled
    # reader.setChecksumValidation(ChecksumValidation.ON)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    #    print("BarCode Value: " + result.getExtended().getOneD().getValue())
    #    print("BarCode Checksum: " + result.getExtended().getOneD().getCheckSum())
    # The checksum validation flag.
    def setChecksumValidation(self, value):
        self.getJavaClass().setChecksumValidation(value.value)

    # Strip FNC1, FNC2, FNC3 characters from codetext. Default value is false.
    # This sample shows how to strip FNC characters
    # generator = BarcodeGenerator(EncodeTypes.GS1Code128, "(02)04006664241007(37)1(400)7019590754")
    # generator.save("test.png")
    # reader = BarCodeReader("test.png", null,  DecodeType.CODE_128)
    # //StripFNC disabled
    # reader.setStripFNC(false)
    # for result in reader.readBarCodes():
    #     print("BarCode CodeText: " + result.getCodeText())
    # reader = BarCodeReader("test.png", null,  DecodeType.CODE_128)
    # //StripFNC enabled
    # reader.setStripFNC(true)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    def getStripFNC(self):
        return self.getJavaClass().getStripFNC()

    # Strip FNC1, FNC2, FNC3 characters from codetext. Default value is false.
    # This sample shows how to strip FNC characters
    # generator = BarcodeGenerator(EncodeTypes.GS1Code128, "(02)04006664241007(37)1(400)7019590754")
    # generator.save("test.png")
    # reader = BarCodeReader("test.png", null,  DecodeType.CODE_128)
    # //StripFNC disabled
    # reader.setStripFNC(false)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    # reader = BarCodeReader("test.png", null,  DecodeType.CODE_128)
    # //StripFNC enabled
    # reader.setStripFNC(true)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    def setStripFNC(self, value):
        self.getJavaClass().setStripFNC(value)

    # Gets the Interpreting Type for the Customer Information of AustralianPost BarCode.Default is CustomerInformationInterpretingType.OTHER.
    def getCustomerInformationInterpretingType(self):
        return self.getJavaClass().getCustomerInformationInterpretingType()

    # Sets the Interpreting Type for the Customer Information of AustralianPost BarCode.Default is CustomerInformationInterpretingType.OTHER.
    def setCustomerInformationInterpretingType(self, value):
        self.getJavaClass().setCustomerInformationInterpretingType(value.value)

    def abort(self):
        self.getJavaClass().abort()

    # Gets recognized BarCodeResult array
    # This sample shows how to read barcodes with BarCodeReader
    # reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    # reader.readBarCodes()
    # for(let i = 0 reader.getFoundCount() > i ++i)
    #    print("BarCode CodeText: " +  reader.getFoundBarCodes()[i].getCodeText())
    # Value: The recognized BarCodeResult array
    def getFoundBarCodes(self):
        return self.recognizedResults

    # Gets recognized barcodes count<hr><blockquote>
    # This sample shows how to read barcodes with BarCodeReader
    # reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    # reader.readBarCodes()
    # for(let i = 0 reader.getFoundCount() > i ++i)
    #    print("BarCode CodeText: " + reader.getFoundBarCodes()[i].getCodeText())
    # Value: The recognized barcodes count
    def getFoundCount(self):
        return self.getJavaClass().getFoundCount()

    # Reads BarCodeResult from the image.
    # This sample shows how to read barcodes with BarCodeReader
    # reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    # reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    # reader.readBarCodes()
    # for(let i = 0 reader.getFoundCount() > i ++i)
    #    print("BarCode CodeText: " + reader.getFoundBarCodes()[i].getCodeText())
    # @return Returns array of recognized {@code BarCodeResult}s on the image. If nothing is recognized, zero array is returned.
    def readBarCodes(self):
        self.recognizedResults = []
        javaReadBarcodes = self.getJavaClass().readBarCodes()
        i = 0
        while(i < javaReadBarcodes.length):
            self.recognizedResults.append(BarCodeResult(javaReadBarcodes[i]))
            i += 1
        return self.recognizedResults

    # QualitySettings allows to configure recognition quality and speed manually.
    # You can quickly set up QualitySettings by embedded presets: HighPerformance, NormalQuality,
    # HighQuality, MaxBarCodes or you can manually configure separate options.
    # Default value of QualitySettings is NormalQuality.
    # This sample shows how to use QualitySettings with BarCodeReader
    # reader = BarCodeReader("test.png", null, null)
    #  //set high performance mode
    # reader.setQualitySettings(QualitySettings.getHighPerformance())
    # for result in reader.readBarCodes():
    #   print("BarCode CodeText: " + result.getCodeText())
    # reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    # //normal quality mode is set by default
    # for result in reader.readBarCodes():
    #   print("BarCode CodeText: " + result.getCodeText())
    # reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    # //set high performance mode
    # reader.setQualitySettings(QualitySettings.getHighPerformance())
    # //set separate options
    # reader.getQualitySettings().setAllowMedianSmoothing(true)
    # reader.getQualitySettings().setMedianSmoothingWindowSize(5)
    # for result in reader.readBarCodes():
    #   print("BarCode CodeText: " + result.getCodeText())
    # QualitySettings to configure recognition quality and speed.
    def getQualitySettings(self):
        return self.qualitySettings

     # QualitySettings allows to configure recognition quality and speed manually.
     # You can quickly set up QualitySettings by embedded presets: HighPerformance, NormalQuality,
     # HighQuality, MaxBarCodes or you can manually configure separate options.
     # Default value of QualitySettings is NormalQuality.

    # This sample shows how to use QualitySettings with BarCodeReader
    # reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    # //set high performance mode
    # reader.setQualitySettings(QualitySettings.getHighPerformance())
    # for result in reader.readBarCodes():
    #   print("BarCode CodeText: " + result.getCodeText())
    # reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    # //normal quality mode is set by default
    # for result in reader.readBarCodes():
    #   print("BarCode CodeText: " + result.getCodeText())
    # reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    #  //set high performance mode
    # reader.setQualitySettings(QualitySettings.getHighPerformance())
    # //set separate options
    # reader.getQualitySettings().setAllowMedianSmoothing(true)
    # reader.getQualitySettings().setMedianSmoothingWindowSize(5)
    # for result in reader.readBarCodes():
    #   print("BarCode CodeText: " + result.getCodeText())
    # QualitySettings to configure recognition quality and speed.
    def setQualitySettings(self, value):
        self.getJavaClass().setQualitySettings(value.getJavaClass())

    # A flag which force engine to detect codetext encoding for Unicode codesets.
    # This sample shows how to detect text encoding on the fly if DetectEncoding is enabled
    # image = "image.png"
    # generator = BarcodeGenerator(EncodeTypes.QR, "пїЅпїЅпїЅпїЅпїЅ"))
    # generator.getParameters().getBarcode().getQR().setCodeTextEncoding("UTF-8")
    # generator.save(image, BarCodeImageFormat.getPng())
    #     //detects encoding for Unicode codesets is enabled
    # reader = BarCodeReader(image, null, DecodeType.QR)
    # reader.setDetectEncoding(true)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    #     //detect encoding is disabled
    # reader = BarCodeReader(image, null, DecodeType.QR)
    # reader.setDetectEncoding(false)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    def getDetectEncoding(self):
        return self.getJavaClass().getDetectEncoding()

    # A flag which force engine to detect codetext encoding for Unicode codesets.
    # This sample shows how to detect text encoding on the fly if DetectEncoding is enabled
    # let image = "image.png"
    # generator = BarcodeGenerator(EncodeTypes.QR, "пїЅпїЅпїЅпїЅпїЅ")
    # generator.getParameters().getBarcode().getQR().setCodeTextEncoding("UTF-8")
    # generator.save(image, BarCodeImageFormat.getPng())
    # //detects encoding for Unicode codesets is enabled
    # reader = BarCodeReader(image, null, DecodeType.QR)
    # reader.setDetectEncoding(true)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    # //detect encoding is disabled
    # reader = BarCodeReader(image, null, DecodeType.QR)
    # reader.setDetectEncoding(true)
    # for result in reader.readBarCodes():
    #    print("BarCode CodeText: " + result.getCodeText())
    def setDetectEncoding(self, value):
        self.getJavaClass().setDetectEncoding(value)

    # Sets bitmap image and areas for Recognition.
    # Must be called before ReadBarCodes() method.
    # This sample shows how to detect Code39 and Code128 barcodes.
    # let bmp = "test.png"
    # reader = BarCodeReader()
    # reader.setBarCodeReadType([ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    # var img = Image()
    # img.src = 'path_to_image'
    # width = img.width
    # height = img.height
    # reader.setBarCodeImage(bmp, [Rectangle(0, 0, width, height)])
    # for result in results:
    #    print("BarCode Type: " + result.getCodeTypeName())
    #    print("BarCode CodeText: " + result.getCodeText())
    # @param value The bitmap image for Recognition.
    # @param areas areas list for recognition
    # @throws BarcodeException
    def setBarCodeImage(self, image, areas):
        image = BarcodeReader.loadImage(image)
        stringAreas = []
        isAllRectanglesNotNull = False
        if (areas is not None):
            if (isinstance(areas, list) and len(areas) > 0):
                i = 0
                while (i < len(areas)):
                    if ((areas[i] != None)):
                        isAllRectanglesNotNull |= True
                        stringAreas.append(areas[i].toString())
                    i += 1
                if (isAllRectanglesNotNull == False):
                    stringAreas = []
        if(len(stringAreas) == 0):
            self.getJavaClass().setBarCodeImage(image)
        else:
            self.getJavaClass().setBarCodeImage(image, stringAreas)

    # Sets SingleDecodeType type array for Recognition.
    # Must be called before readBarCodes() method.
    # This sample shows how to detect Code39 and Code128 barcodes.
    # reader = BarCodeReader()
    # reader.setBarCodeReadType([ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
    # reader.setBarCodeImage("test.png")
    # for result in reader.readBarCodes():
    #     print("BarCode Type: " + result.getCodeTypeName())
    #     print("BarCode CodeText: " + result.getCodeText())
    # @param types The SingleDecodeType type array to read.
    def setBarCodeReadType(self, types):
        i = 0
        if(isinstance(types, list)):
            while(i < len(types)):
                types[i] = str(types[i].value)
                i += 1
        else:
            types = [str(types.value)]
        self.getJavaClass().setBarCodeReadType(types)

    def getBarCodeDecodeType(self):
        return DecodeType(int(self.getJavaClass().getBarCodeDecodeType()))

    # Exports BarCode properties to the xml-file specified
    # @param xmlFile The name for the file
    # @return Whether or not export completed successfully.
    # Returns True in case of success False Otherwise
    def exportToXml(self, xmlFile):
        return self.getJavaClass().exportToXml(xmlFile)

# Stores a set of four Points that represent a Quadrangle region.
class Quadrangle (Assist.BaseJavaClass):
    javaClassName = "com.aspose.mw.barcode.recognition.MwQuadrangle"

    leftTop = None
    rightTop = None
    rightBottom = None
    leftBottom = None

    # Represents a Quadrangle structure with its properties left uninitialized.Value: Quadrangle
    @staticmethod
    def EMPTY():
        return Quadrangle(Assist.Point(0, 0), Assist.Point(0, 0), Assist.Point(0, 0), Assist.Point(0, 0))

    @staticmethod
    def construct(*args):
        quadrangle = Quadrangle.EMPTY()
        quadrangle.setJavaClass(args[0])
        return quadrangle


    # Initializes a new instance of the Quadrangle structure with the describing points.
    # @param leftTop A Point that represents the left-top corner of the Quadrangle.
    # @param rightTop A Point that represents the right-top corner of the Quadrangle.
    # @param rightBottom A Point that represents the right-bottom corner of the Quadrangle.
    # @param leftBottom A Point that represents the left-bottom corner of the Quadrangle.
    def __init__(self, leftTop, rightTop, rightBottom, leftBottom):
        java_link = jpype.JClass(self.javaClassName)
        javaClass = java_link(leftTop.toString(), rightTop.toString(), rightBottom.toString(), leftBottom.toString())
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.leftTop = Assist.Point(self.getJavaClass().getLeftTop().getX(), self.getJavaClass().getLeftTop().getY())
        self.rightTop = Assist.Point(self.getJavaClass().getRightTop().getX(), self.getJavaClass().getRightTop().getY())
        self.rightBottom = Assist.Point(self.getJavaClass().getRightBottom().getX(), self.getJavaClass().getRightBottom().getY())
        self.leftBottom = Assist.Point(self.getJavaClass().getLeftBottom().getX(), self.getJavaClass().getLeftBottom().getY())

    # Gets left-top corner Point of Quadrangle regionValue: A left-top corner Point of Quadrangle region
    def getLeftTop(self):
        return self.leftTop

    # Gets left-top corner Point of Quadrangle regionValue: A left-top corner Point of Quadrangle region
    def setLeftTop(self, value):
        self.leftTop = value
        self.getJavaClass().setLeftTop(value)

    # Gets right-top corner Point of Quadrangle regionValue: A right-top corner Point of Quadrangle region
    def getRightTop(self):
        return self.rightTop

    # Gets right-top corner Point of Quadrangle regionValue: A right-top corner Point of Quadrangle region
    def setRightTop(self, value):
        self.rightTop = value
        self.getJavaClass().setRightTop(value)

    # Gets right-bottom corner Point of Quadrangle regionValue: A right-bottom corner Point of Quadrangle region
    def getRightBottom(self):
        return self.rightBottom

    # Gets right-bottom corner Point of Quadrangle regionValue: A right-bottom corner Point of Quadrangle region
    def setRightBottom(self, value):
        self.rightBottom = value
        self.getJavaClass().setRightBottom(value)

    # Gets left-bottom corner Point of Quadrangle regionValue: A left-bottom corner Point of Quadrangle region
    def getLeftBottom(self):
        return self.leftBottom

    # Gets left-bottom corner Point of Quadrangle regionValue: A left-bottom corner Point of Quadrangle region
    def setLeftBottom(self, value):
        self.leftBottom = value
        self.getJavaClass().setLeftBottom(value)

    # Tests whether all Points of this Quadrangle have values of zero.Value: Returns true if all Points of this Quadrangle have values of zero otherwise, false.
    def isEmpty(self):
        return self.getJavaClass().isEmpty()

    # Determines if the specified Point is contained within this Quadrangle structure.
    # @param pt The Point to test.
    # @return Returns true if Point is contained within this Quadrangle structure otherwise, false.
    def contains(self, pt):
        return self.getJavaClass().contains(pt)

    # Determines if the specified point is contained within this Quadrangle structure.
    # @param x The x point cordinate.
    # @param y The y point cordinate.
    # @return Returns true if point is contained within this Quadrangle structure otherwise, false.
    def containsPoint(self, x, y):
        return self.getJavaClass().contains(x, y)

    # Determines if the specified Quadrangle is contained or intersect this Quadrangle structure.
    # @param quad The Quadrangle to test.
    # @return Returns true if Quadrangle is contained or intersect this Quadrangle structure otherwise, false.
    def containsQuadrangle(self, quad):
        return self.getJavaClass().contains(quad)

    # Determines if the specified Rectangle is contained or intersect this Quadrangle structure.
    # @param rect The Rectangle to test.
    # @return Returns true if Rectangle is contained or intersect this Quadrangle structure otherwise, false.
    def containsRectangle(self, rect):
        return self.getJavaClass().contains(rect)

    # Returns a value indicating whether this instance is equal to a specified Quadrangle value.
    # @param other An Quadrangle value to compare to this instance.
    # @return true if obj has the same value as this instance otherwise, false.
    def equals(self, other):
        return self.getJavaClass().equals(other)

    # Returns a value indicating whether the first Quadrangle value is equal to the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the same value as second otherwise, false.
    @staticmethod
    def op_Equality(first, second):
        return Quadrangle.isEqual(first, second)

     # Returns a value indicating if the first Quadrangle value is different from the second.

    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the different value from second otherwise, false.
    @staticmethod
    def op_Inequality(first, second):
        return not Quadrangle.isEqual(first, second)

    # Returns the hash code for this instance.
    # @return A 32-bit signed integer hash code.
    def hashCode(self):
        return self.getJavaClass().hashCode()

    # Returns a human-readable string representation of this Quadrangle.
    # @return A string that represents this Quadrangle.
    def toString(self):
        return self.toString()

    # Creates Rectangle bounding this Quadrangle
    # @return returns Rectangle bounding this Quadrangle
    def getBoundingRectangle(self):
        return Assist.Rectangle(self.getJavaClass().getBoundingRectangle().getX(),
                                self.getJavaClass().getBoundingRectangle().getY(),
                                self.getJavaClass().getBoundingRectangle().getWidth(),
                                self.getJavaClass().getBoundingRectangle().getHeight())

    @staticmethod
    def isEqual(first, second):
        return first.equals(second)

# Stores a QR Structured Append information of recognized barcode
# This sample shows how to get QR Structured Append data
# reader = BarCodeReader("test.png", null,  DecodeType.QR)
# for result in reader.readBarCodes():
#    print("BarCode Type: " + result.getCodeTypeName())
#    print("BarCode CodeText: " + result.getCodeText())
#    print("QR Structured Append Quantity: " + result.getExtended().getQR().getQRStructuredAppendModeBarCodesQuantity())
#    print("QR Structured Append Index: " + result.getExtended().getQR().getQRStructuredAppendModeBarCodeIndex())
#    print("QR Structured Append ParityData: " + result.getExtended().getQR().getQRStructuredAppendModeParityData())
#
class QRExtendedParameters (Assist.BaseJavaClass):
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        return
        # TODO: Implement init() method.

    # Gets the QR structured append mode barcodes quantity. Default value is -1.Value: The quantity of the QR structured append mode barcode.
    def getQRStructuredAppendModeBarCodesQuantity(self):
        return self.getJavaClass().getQRStructuredAppendModeBarCodesQuantity()

    # Gets the index of the QR structured append mode barcode. Index starts from 0. Default value is -1.Value: The quantity of the QR structured append mode barcode.
    def getQRStructuredAppendModeBarCodeIndex(self):
        return self.getJavaClass().getQRStructuredAppendModeBarCodeIndex()

    # Gets the QR structured append mode parity data. Default value is -1.Value: The index of the QR structured append mode barcode.
    def getQRStructuredAppendModeParityData(self):
        return self.getJavaClass().getQRStructuredAppendModeParityData()

    def isEmpty(self):
        return self.getJavaClass().isEmpty()

    # Returns a value indicating whether this instance is equal to a specified QRExtendedParameters value.
    # @param obj An object value to compare to this instance.
    # @return true if obj has the same value as this instance otherwise, false.
    def equals(self, obj):
        return self.getJavaClass().equals(obj)

    # Returns a value indicating whether the first QRExtendedParameters value is equal to the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the same value as second otherwise, false.
    @staticmethod
    def op_Equality(first, second):
        return QRExtendedParameters.isEqual(first, second)

    # Returns a value indicating if the first QRExtendedParameters value is different from the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the different value from second otherwise, false.
    @staticmethod
    def op_Inequality(first, second):
        return not QRExtendedParameters.isEqual(first, second)

    @staticmethod
    def isEqual(first, second):
        return first.equals(second)

    # Returns the hash code for this instance.
    # @return A 32-bit signed integer hash code.
    def hashCode(self):
        return self.getJavaClass().hashCode()

    # Returns a human-readable string representation of this QRExtendedParameters.
    # @return A string that represents this QRExtendedParameters.
    def toString(self):
        return self.getJavaClass().toString()

# Stores a MacroPdf417 metadata information of recognized barcode
# This sample shows how to get Macro Pdf417 metadata
# generator = BarcodeGenerator(EncodeTypes.MacroPdf417, "12345")
# generator.getParameters().getBarcode().getPdf417().setPdf417MacroFileID(10)
# generator.getParameters().getBarcode().getPdf417().setPdf417MacroSegmentsCount(2)
# generator.getParameters().getBarcode().getPdf417().setPdf417MacroSegmentID(1)
# generator.save("test.png")
# reader = BarCodeReader("test.png", null,  DecodeType.MACRO_PDF_417)
# for result in reader.readBarCodes():
#     print("BarCode Type: " + result.getCodeTypeName())
#     print("BarCode CodeText: " + result.getCodeText())
#     print("Macro Pdf417 FileID: " + result.getExtended().getPdf417().getMacroPdf417FileID())
#     print("Macro Pdf417 Segments: " + result.getExtended().getPdf417().getMacroPdf417SegmentsCount())
#     print("Macro Pdf417 SegmentID: " + result.getExtended().getPdf417().getMacroPdf417SegmentID())
class Pdf417ExtendedParameters (Assist.BaseJavaClass):
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        return
        # TODO: Implement init() method.

    # Gets the file ID of the barcode, only available with MacroPdf417.Value: The file ID for MacroPdf417
    def getMacroPdf417FileID(self):
        return str(self.getJavaClass().getMacroPdf417FileID())

    # Gets the segment ID of the barcode,only available with MacroPdf417.Value: The segment ID of the barcode.
    def getMacroPdf417SegmentID(self):
        return int(self.getJavaClass().getMacroPdf417SegmentID())

    # Gets macro pdf417 barcode segments count. Default value is -1.Value: Segments count.
    def getMacroPdf417SegmentsCount(self):
        return int(self.getJavaClass().getMacroPdf417SegmentsCount())

    # Tests whether all parameters has only default values
    # Value: Returns {@code <b>true</b>} if all parameters has only default values otherwise, {@code <b>false</b>}.
    def isEmpty(self):
        return self.getJavaClass().isEmpty()

    # Returns a value indicating whether this instance is equal to a specified Pdf417ExtendedParameters value.
    # @param obj An System.Object value to compare to this instance.
    # @return true if obj has the same value as this instance otherwise, false.
    def equals(self, obj):
        return self.getJavaClass().equals(obj)

    # Returns a value indicating whether the first Pdf417ExtendedParameters value is equal to the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the same value as second otherwise, false.
    @staticmethod
    def op_Equality(first, second):
        return Pdf417ExtendedParameters.isEqual(first, second)

    # Returns a value indicating if the first Pdf417ExtendedParameters value is different from the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the different value from second otherwise, false.
    @staticmethod
    def op_Inequality(first, second):
        return not Pdf417ExtendedParameters.isEqual(first, second)

    # Returns the hash code for this instance.
    # @return A 32-bit signed integer hash code.
    def hashCode(self):
        return self.getJavaClass().hashCode()

    # Returns a human-readable string representation of this Pdf417ExtendedParameters.
    # @return A string that represents this Pdf417ExtendedParameters.
    def toString(self):
        return self.getJavaClass().toString()

    # Returns a value indicating whether the first value is equal to the second
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the same value as second otherwise, false.
    @staticmethod
    def isEqual(first, second):
        return first.equals(second)

# Stores special data of 1D recognized barcode like separate codetext and checksum
# This sample shows how to get 1D barcode value and checksum
# generator = BarcodeGenerator(EncodeTypes.EAN_13, "1234567890128")
# generator.save("test.png")
# reader = BarCodeReader("test.png", null,  DecodeType.EAN_13)
# for result in reader.readBarCodes():
#    print("BarCode Type: " + result.getCodeTypeName())
#    print("BarCode CodeText: " + result.getCodeText())
#    print("BarCode Value: " + result.getExtended().getOneD().getValue())
#    print("BarCode Checksum: " + result.getExtended().getOneD().getCheckSum())
class OneDExtendedParameters (Assist.BaseJavaClass):
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        return
        # TODO: Implement init() method.

    # Gets the codetext of 1D barcodes without checksum. Value: The codetext of 1D barcodes without checksum.
    def getValue(self):
        return self.getJavaClass().getValue()

    # Gets the checksum for 1D barcodes. Value: The checksum for 1D barcode.
    def getCheckSum(self):
        return self.getJavaClass().getCheckSum()

    # Tests whether all parameters has only default values
    # Value: Returns {@code <b>true</b>} if all parameters has only default values otherwise, {@code <b>false</b>}.
    def isEmpty(self):
        return self.getJavaClass().isEmpty()

    # Returns a value indicating whether this instance is equal to a specified OneDExtendedParameters value.
    # @param obj An System.Object value to compare to this instance.
    # @return true if obj has the same value as this instance otherwise, false.
    def equals(self, obj):
        return self.getJavaClass().equals(obj)

    # Returns a value indicating whether the first OneDExtendedParameters value is equal to the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the same value as second otherwise, false.
    @staticmethod
    def op_Equality(first, second):
        return OneDExtendedParameters.isEqual(first, second)

    # Returns a value indicating if the first OneDExtendedParameters value is different from the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the different value from second otherwise, false.
    def op_Inequality(first, second):
        return not OneDExtendedParameters.isEqual(first, second)

    # Returns the hash code for this instance.
    # @return A 32-bit signed integer hash code.
    def hashCode(self):
        return self.getJavaClass().hashCode()

    # Returns a human-readable string representation of this OneDExtendedParameters.
    # @return A string that represents this OneDExtendedParameters.
    def toString(self):
        return self.getJavaClass().toString()

    # Returns a value indicating whether the first value is equal to the second
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the same value as second otherwise, false.
    def isEqual(first, second):
        return first.equals(second)

# Stores special data of Code128 recognized barcode
# Represents the recognized barcode's region and barcode angle
# This sample shows how to get code128 raw values
# generator = BarcodeGenerator(EncodeTypes.Code128, "12345")
# generator.save("test.png")
# reader = BarCodeReader("test.png", null,  DecodeType.CODE_128)
# for result in reader.readBarCodes():
#    print("BarCode Type: " + result.getCodeTypeName())
#    print("BarCode CodeText: " + result.getCodeText())
#    print("Code128 Data Portions: " + result.getExtended().getCode128())
class Code128ExtendedParameters (Assist.BaseJavaClass):
    code128DataPortions = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.code128DataPortions = Code128ExtendedParameters.convertCode128DataPortions(self.getJavaClass().getCode128DataPortions())

    def convertCode128DataPortions(javaCode128DataPortions):
        code128DataPortionsValues = javaCode128DataPortions
        code128DataPortions = []
        i = 0
        while (i < len(code128DataPortionsValues)):
            code128DataPortions.append(Code128DataPortion.construct(code128DataPortionsValues[i]))
            i += 1
        return code128DataPortions

    #  Gets Code128DataPortion array of recognized Code128 barcode Value of the Code128DataPortion.
    def getCode128DataPortions(self):
        return self.code128DataPortions

    def isEmpty(self):
        return self.getJavaClass().isEmpty()

    # Returns a value indicating whether this instance is equal to a specified Code128ExtendedParameters value.
    # @param obj An System.Object value to compare to this instance.
    # @return true if obj has the same value as this instance otherwise, false.
    def equals(self, obj):
        return self.getJavaClass().equals(obj.getJavaClass())

    # Returns a value indicating whether the first Code128ExtendedParameters value is equal to the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the same value as second otherwise, false.
    def op_Equality(first, second):
        return first.equals(second)

    # Returns a value indicating if the first Code128ExtendedParameters value is different from the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the different value from second otherwise, false.
    def op_Inequality(first, second):
        return not Code128ExtendedParameters.isEqual(first, second)

    # Returns the hash code for this instance.
    # @return A 32-bit signed integer hash code.
    def hashCode(self):
        return self.getJavaClass().hashCode()

    # Returns a human-readable string representation of this Code128ExtendedParameters.
    # @return A string that represents this Code128ExtendedParameters.
    def toString(self):
        return self.getJavaClass().toString()

    def isEqual(first, second):
        return first.equals(second)

# Barcode detector settings.
class BarcodeSvmDetectorSettings (Assist.BaseJavaClass):
    javaClassName = "com.aspose.mw.barcode.recognition.MwBarcodeSvmDetectorSettings"

    # High performance detection preset.
    # Default for {@code QualitySettings.PresetType.HighPerformance}
    HighPerformance = 0

    # Normal quality detection preset.
    # Default for {@code QualitySettings.PresetType.NormalQuality}
    NormalQuality = 1

    # High quality detection preset.
    # Default for {@code QualitySettings.PresetType.HighQualityDetection} and {@code QualitySettings.PresetType.HighQuality}
    HighQuality = 2

    # Max quality detection preset.
    # Default for {@code QualitySettings.PresetType.MaxQualityDetection} and {@code QualitySettings.PresetType.MaxBarCodes}
    MaxQuality = 3

    scanWindowSizes = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.scanWindowSizes = BarcodeSvmDetectorSettings.convertScanWindowSizes(self.getJavaClass().getScanWindowSizes())
        # TODO: Implement init() method.

    def convertScanWindowSizes(javaScanWindowSizes):
        scanWindowSizes = []
        i = 0
        while ( i < javaScanWindowSizes.size()):
            scanWindowSizes.append(str(javaScanWindowSizes.get(i)))
            i += 1
        return scanWindowSizes

    # Scan window sizes in pixels.
    # Allowed sizes are 10, 15, 20, 25, 30.
    # Scanning with small window size takes more time and provides more accuracy but may fail in detecting very big barcodes.
    # Combining of several window sizes can improve detection quality.
    def getScanWindowSizes(self):
        return self.scanWindowSizes

    # Scan window sizes in pixels.
    # Allowed sizes are 10, 15, 20, 25, 30.
    # Scanning with small window size takes more time and provides more accuracy but may fail in detecting very big barcodes.
    # Combining of several window sizes can improve detection quality.
    def setScanWindowSizes(self, value):
        self.scanWindowSizes = value
        self.getJavaClass().setScanWindowSizes(value)

    # Similarity coefficient depends on how homogeneous barcodes are.
    # Use high value for for clear barcodes.
    # Use low values to detect barcodes that ara partly damaged or not lighten evenly.
    # Similarity coefficient must be between [0.5, 0.9]
    def getSimilarityCoef(self):
        return self.getJavaClass().getSimilarityCoef()

    # Similarity coefficient depends on how homogeneous barcodes are.
    # Use high value for for clear barcodes.
    # Use low values to detect barcodes that ara partly damaged or not lighten evenly.
    # Similarity coefficient must be between [0.5, 0.9]
    def setSimilarityCoef(self, value):
        self.getJavaClass().setSimilarityCoef(value)

    # Sets threshold for detected regions that may contain barcodes.
    # Value 0.7 means that bottom 70% of possible regions are filtered out and not processed further.
    # Region likelihood threshold must be between [0.05, 0.9]
    # Use high values for clear images with few barcodes.
    # Use low values for images with many barcodes or for noisy images.
    # Low value may lead to a bigger recognition time.
    def getRegionLikelihoodThresholdPercent(self):
        return self.getJavaClass().getRegionLikelihoodThresholdPercent()

    # Sets threshold for detected regions that may contain barcodes.
    # Value 0.7 means that bottom 70% of possible regions are filtered out and not processed further.
    # Region likelihood threshold must be between [0.05, 0.9]
    # Use high values for clear images with few barcodes.
    # Use low values for images with many barcodes or for noisy images.
    # Low value may lead to a bigger recognition time.
    def setRegionLikelihoodThresholdPercent(self, value):
        self.getJavaClass().setRegionLikelihoodThresholdPercent(value)

    # Allows detector to skip search for diagonal barcodes.
    # Setting it to false will increase detection time but allow to find diagonal barcodes that can be missed otherwise.
    # Enabling of diagonal search leads to a bigger detection time.
    def getSkipDiagonalSearch(self):
        return self.getJavaClass().getSkipDiagonalSearch()

    # Allows detector to skip search for diagonal barcodes.
    # Setting it to false will increase detection time but allow to find diagonal barcodes that can be missed otherwise.
    # Enabling of diagonal search leads to a bigger detection time.
    def setSkipDiagonalSearch(self, value):
        self.getJavaClass().setSkipDiagonalSearch(value)

    # Window size for median smoothing.
    # Typical values are 3 or 4. 0 means no median smoothing.
    # Default value is 0.
    # Median filter window size must be between [0, 10]
    def getMedianFilterWindowSize(self):
        return self.getJavaClass().getMedianFilterWindowSize()

    # Window size for median smoothing.
    # Typical values are 3 or 4. 0 means no median smoothing.
    # Default value is 0.
    # Median filter window size must be between [0, 10]
    def setMedianFilterWindowSize(self, value):
        self.getJavaClass().setMedianFilterWindowSize(value)

    # High performance detection preset.
    # Default for QualitySettings.PresetType.HighPerformance
    @staticmethod
    def getHighPerformance():
        return BarcodeSvmDetectorSettings(QualitySettings.HighPerformance)

    # Normal quality detection preset.
    # Default for QualitySettings.PresetType.NormalQuality
    @staticmethod
    def getNormalQuality():
        return BarcodeSvmDetectorSettings(QualitySettings.NormalQuality)

    # High quality detection preset.
    # Default for QualitySettings.PresetType.HighQualityDetection and QualitySettings.PresetType.HighQuality
    @staticmethod
    def getHighQuality():
        return BarcodeSvmDetectorSettings(QualitySettings.HighQuality)

    # Max quality detection preset.
    # Default for QualitySettings.PresetType.MaxQualityDetection and QualitySettings.PresetType.MaxBarCodes
    @staticmethod
    def getMaxQuality():
        return BarcodeSvmDetectorSettings(QualitySettings.MaxQuality)

# Stores recognized barcode data like SingleDecodeType type, {@code string} codetext,
# BarCodeRegionParameters region and other parameters
# This sample shows how to obtain BarCodeResult.
# generator = BarcodeGenerator(EncodeTypes.Code128, "12345")
# generator.save("test.png")
# reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
# for result in reader.readBarCodes():
#     print("BarCode Type: " + result.getCodeTypeName())
#     print("BarCode CodeText: " + result.getCodeText())
#     print("BarCode Confidence: " + result.getConfidence())
#     print("BarCode ReadingQuality: " + result.getReadingQuality())
#     print("BarCode Angle: " + result.getRegion().getAngle())
class BarCodeResult (Assist.BaseJavaClass):
    region = None
    extended = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.region = BarCodeRegionParameters(self.getJavaClass().getRegion())
        self.extended = BarCodeExtendedParameters(self.getJavaClass().getExtended())

    #  Gets the reading quality. Works for 1D and postal barcodes. Value: The reading quality percent
    def getReadingQuality(self):
        return self.getJavaClass().getReadingQuality()

    #  Gets recognition confidence level of the recognized barcode Value: BarCodeConfidence.Strong does not have fakes or misrecognitions, BarCodeConfidence.Moderate
    # could sometimes have fakes or incorrect codetext because this confidence level for barcodews with weak cheksum or even without it,
    # BarCodeConfidence.NONE always has incorrect codetext and could be fake recognitions
    def getConfidence(self):
        return BarCodeConfidence(str(self.getJavaClass().getConfidence()))

    #  Gets the code text Value: The code text of the barcode
    def getCodeText(self):
        return str(self.getJavaClass().getCodeText())

    #  Gets the encoded code bytes Value: The code bytes of the barcode
    def getCodeBytes(self):
        _str = str(self.getJavaClass().getCodeBytes())
        return _str.split(",")

    #  Gets the barcode type Value: The type information of the recognized barcode
    def getCodeType(self):
        return DecodeType(self.getJavaClass().getCodeType())

    #  Gets the name of the barcode type Value: The type name of the recognized barcode
    def getCodeTypeName(self):
        return str(self.getJavaClass().getCodeTypeName())

    #  Gets the barcode region Value: The region of the recognized barcode
    def getRegion(self):
        return self.region

    #  Gets extended parameters of recognized barcode Value: The extended parameters of recognized barcode
    def getExtended(self):
        return self.extended

    # Returns a value indicating whether this instance is equal to a specified BarCodeResult value.
    # @param other An BarCodeResult value to compare to this instance.
    # @return true if obj has the same value as this instance otherwise, false.
    def equals(self, other):
        return self.getJavaClass().equals(other)

    # Returns a value indicating whether the first BarCodeResult value is equal to the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the same value as second otherwise, false.
    def op_Equality(first, second):
        return BarCodeResult.isEqual(first, second)

    # Returns a value indicating if the first BarCodeResult value is different from the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the different value from second otherwise, false.
    def op_Inequality(first, second):
        return not BarCodeResult.isEqual(first, second)

    # Returns the hash code for this instance.
    # @return A 32-bit signed integer hash code.
    def hashCode(self):
        return self.getJavaClass().hashCode()

    # Returns a human-readable string representation of this BarCodeResult.
    # @return A string that represents this BarCodeResult.
    def toString(self):
        return self.getJavaClass().toString()

    # Creates a copy of BarCodeResult class.
    # @return Returns copy of BarCodeResult class.
    def deepClone(self):
        return BarCodeResult(self)

# Represents the recognized barcode's region and barcode angle
# This sample shows how to get barcode Angle and bounding quadrangle values
# generator = BarcodeGenerator(EncodeTypes.Code128, "12345")
# generator.save("test.png")
# reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
# for result in reader.readBarCodes():
#    print("BarCode CodeText: " + result.getCodeText())
#    print("BarCode Angle: " + result.getRegion().getAngle())
#    print("BarCode Quadrangle: " + result.getRegion().getQuadrangle())
class BarCodeRegionParameters (Assist.BaseJavaClass):
    quad = None
    rect = None
    points = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self.quad = Quadrangle.construct(self.getJavaClass().getQuadrangle())
        self.rect = Assist.Rectangle(self.getJavaClass().getRectangle().getX(),
                                     self.getJavaClass().getRectangle().getY(),
                                     self.getJavaClass().getRectangle().getWidth(),
                                     self.getJavaClass().getRectangle().getHeight())
        self.points = BarCodeRegionParameters.convertJavaPoints(self.getJavaClass().getPoints())
        # TODO: Implement init() method.

    def convertJavaPoints(javaPoints):
        points = []
        i = 0
        while (i < len(javaPoints)):
            points.append(Assist.Point(javaPoints[i].getX(), javaPoints[i].getY()))
            i += 1

        return points

    #  Gets Quadrangle bounding barcode region Value: Returns Quadrangle bounding barcode region
    def getQuadrangle(self):
        return self.quad

    #  Gets the angle of the barcode (0-360). Value: The angle for barcode (0-360).
    def getAngle(self):
        return self.getJavaClass().getAngle()

    #  Gets Points array bounding barcode region Value: Returns Points array bounding barcode region
    def getPoints(self):
        return self.points

    #  Gets Rectangle bounding barcode region Value: Returns Rectangle bounding barcode region
    def getRectangle(self):
        return self.rect

    # Returns a value indicating whether this instance is equal to a specified BarCodeRegionParameters value.
    # @param obj An System.Object value to compare to this instance.
    # @return true if obj has the same value as this instance otherwise, false.
    def equals(self, obj):
        return self.getJavaClass().equals(obj)

    # Returns a value indicating whether the first BarCodeRegionParameters value is equal to the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the same value as second otherwise, false.
    def op_Equality(first, second):
        return BarCodeRegionParameters.isEqual(first, second)

    # Returns a value indicating if the first BarCodeRegionParameters value is different from the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the different value from second otherwise, false.
    def op_Inequality(first, second):
        return not BarCodeRegionParameters.isEqual(first, second)

    # Returns the hash code for this instance.
    # @return A 32-bit signed integer hash code.
    def hashCode(self):
        return self.getJavaClass().hashCode()

    # Returns a human-readable string representation of this BarCodeRegionParameters.
    # @return A string that represents this BarCodeRegionParameters.
    def toString(self):
        return self.getJavaClass().toString()

class BarCodeExtendedParameters (Assist.BaseJavaClass):
    _oneDParameters = None
    _code128Parameters = None
    _qrParameters = None
    _pdf417Parameters = None
    _dataBarParameters = None

    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.init()

    def init(self):
        self._oneDParameters = OneDExtendedParameters(self.getJavaClass().getOneD())
        self._code128Parameters = Code128ExtendedParameters(self.getJavaClass().getCode128())
        self._qrParameters = QRExtendedParameters(self.getJavaClass().getQR())
        self._pdf417Parameters = Pdf417ExtendedParameters(self.getJavaClass().getPdf417())
        self._dataBarParameters = DataBarExtendedParameters(self.getJavaClass().getDataBar())


    # Gets a DataBar additional information<see cref="DataBarExtendedParameters"/> of recognized barcode
    # @return mixed A DataBar additional information<see cref="DataBarExtendedParameters"/> of recognized barcode
    def getDataBar(self):
        return self._dataBarParameters

    #  Gets a special data OneDExtendedParameters of 1D recognized barcode Value: A special data OneDExtendedParameters of 1D recognized barcode
    def getOneD(self):
        return self._oneDParameters

    #  Gets a special data Code128ExtendedParameters of Code128 recognized barcode Value: A special data Code128ExtendedParameters of Code128 recognized barcode
    def getCode128(self):
        return self._code128Parameters

    #  Gets a QR Structured Append information QRExtendedParameters of recognized barcode Value: A QR Structured Append information QRExtendedParameters of recognized barcode
    def getQR(self):
        return self._qrParameters

    #  Gets a MacroPdf417 metadata information Pdf417ExtendedParameters of recognized barcode Value: A MacroPdf417 metadata information Pdf417ExtendedParameters of recognized barcode
    def getPdf417(self):
        return self._pdf417Parameters

    # Returns a value indicating whether this instance is equal to a specified BarCodeExtendedParameters value.
    # @param obj An System.Object value to compare to this instance.
    # @return true if obj has the same value as this instance otherwise, false.
    def equals(self, obj):
        return self.getJavaClass().equals(obj.getJavaClass())

    # Returns a value indicating whether the first BarCodeExtendedParameters value is equal to the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the same value as second otherwise, false.
    def op_Equality(first, second):
        return first.getJavaClass().equals(second.getJavaClass())

    # Returns a value indicating if the first BarCodeExtendedParameters value is different from the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return true if first has the different value from second otherwise, false.
    def op_Inequality(first, second):
        return not first.getJavaClass().equals(second.getJavaClass())

    # Returns the hash code for this instance.
    #  @return A 32-bit signed integer hash code.
    def hashCode(self):
        return self.getJavaClass().hashCode()

    # Returns a human-readable string representation of this BarCodeExtendedParameters.
    # @return A string that represents this BarCodeExtendedParameters.
    def toString(self):
        return self.getJavaClass().toString()

# QualitySettings allows to configure recognition quality and speed manually.
# You can quickly set up QualitySettings by embedded presets: HighPerformance, NormalQuality,
# HighQuality, MaxBarCodes or you can manually configure separate options.
# Default value of QualitySettings is NormalQuality.
# This sample shows how to use QualitySettings with BarCodeReader
# reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
# //set high performance mode
# reader.setQualitySettings(QualitySettings.getHighPerformance())
# for result in reader.readBarCodes():
#    print("BarCode CodeText: " + result.getCodeText())
# reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
# //normal quality mode is set by default
# for result in reader.readBarCodes():
#   print("BarCode CodeText: " + result.getCodeText())
# reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
# //set high quality mode with low speed recognition
# reader.setQualitySettings(QualitySettings.getHighQuality())
# for result in reader.readBarCodes():
#   print("BarCode CodeText: " + result.getCodeText())
# reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
# //set max barcodes mode, which tries to find all possible barcodes, even incorrect. The slowest recognition mode
# reader.setQualitySettings(QualitySettings.getMaxBarCodes())
# for result in reader.readBarCodes():
#   print("BarCode CodeText: " + result.getCodeText())
# reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
# //set high performance mode
# reader.setQualitySettings(QualitySettings.getHighPerformance())
# //set separate options
# reader.getQualitySettings().setAllowMedianSmoothing(true)
# reader.getQualitySettings().setMedianSmoothingWindowSize(5)
# for result in reader.readBarCodes():
#     print("BarCode CodeText: " + result.getCodeText())
# reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
# //default mode is NormalQuality
# //set separate options
# reader.getQualitySettings().setAllowMedianSmoothing(true)
# reader.getQualitySettings().setMedianSmoothingWindowSize(5)
# for result in reader.readBarCodes():
#   print("BarCode CodeText: " + result.getCodeText())
class QualitySettings (Assist.BaseJavaClass):

    javaClassName = "com.aspose.mw.barcode.recognition.MwQualitySettings"
    detectorSettings = None

    def __init__(self, qualitySettings):
        super().__init__(self.initQualitySettings(qualitySettings))
        if (isinstance(qualitySettings, QualitySettings)):
            self.applyAll(qualitySettings)
        self.init()

    @staticmethod
    def initQualitySettings(qualitySettings):
        if (isinstance(qualitySettings, QualitySettings) | (qualitySettings == None)):
            java_link = jpype.JClass(QualitySettings.javaClassName)
            javaQualitySettings = java_link()
            return javaQualitySettings
        else:
            return qualitySettings

    def init(self):
        self.detectorSettings = BarcodeSvmDetectorSettings(self.getJavaClass().getDetectorSettings())

    # HighPerformance recognition quality preset. High quality barcodes are recognized well in this mode.
    # reader = BarCodeReader("test.png")
    # reader.setQualitySettings(QualitySettings.getHighPerformance())
    #  Value:
    # HighPerformance recognition quality preset.
    @staticmethod
    def getHighPerformance():
        java_link = jpype.JClass(QualitySettings.javaClassName)
        JavaQualitySettings = java_link()
        return QualitySettings(JavaQualitySettings.getHighPerformance())

    # NormalQuality recognition quality preset. Suitable for the most of barcodes
    # reader = BarCodeReader("test.png")
    # reader.setQualitySettings(QualitySettings.getNormalQuality())
    #  Value:
    # NormalQuality recognition quality preset.
    @staticmethod
    def getNormalQuality():
        java_link = jpype.JClass(QualitySettings.javaClassName)
        JavaQualitySettings = java_link()
        return QualitySettings(JavaQualitySettings.getNormalQuality())

    # HighQualityDetection recognition quality preset. Same as NormalQuality but with high quality DetectorSettings
    # reader = BarCodeReader("test.png")
    # reader.setQualitySettings(QualitySettings.getHighQualityDetection())
    #  Value:
    # HighQualityDetection recognition quality preset.
    @staticmethod
    def getHighQualityDetection():
        java_link = jpype.JClass(QualitySettings.javaClassName)
        JavaQualitySettings = java_link()
        return  QualitySettings(JavaQualitySettings.getHighQualityDetection())

    # MaxQualityDetection recognition quality preset. Same as NormalQuality but with highest quality DetectorSettings.
    # Allows to detect diagonal and damaged barcodes.
    # reader = BarCodeReader("test.png")
    # reader.setQualitySettings(QualitySettings.getMaxQualityDetection())
    #  Value:
    # MaxQualityDetection recognition quality preset.
    @staticmethod
    def getMaxQualityDetection():
        java_link = jpype.JClass(QualitySettings.javaClassName)
        JavaQualitySettings = java_link()
        return QualitySettings(JavaQualitySettings.getMaxQualityDetection())

    # HighQuality recognition quality preset. This preset is developed for low quality barcodes.
    # reader = BarCodeReader("test.png")
    # reader.setQualitySettings(QualitySettings.getHighQuality())
    #  Value:
    # HighQuality recognition quality preset.
    @staticmethod
    def getHighQuality():
        java_link = jpype.JClass(QualitySettings.javaClassName)
        JavaQualitySettings = java_link()
        return QualitySettings(JavaQualitySettings.getHighQuality())

    # MaxBarCodes recognition quality preset. This preset is developed to recognize all possible barcodes, even incorrect barcodes.
    # reader = BarCodeReader("test.png")
    # reader.setQualitySettings(QualitySettings.getMaxBarCodes())
    #  Value:
    # MaxBarCodes recognition quality preset.
    @staticmethod
    def getMaxBarCodes():
        java_link = jpype.JClass(QualitySettings.javaClassName)
        JavaQualitySettings = java_link()
        return QualitySettings(JavaQualitySettings.getMaxBarCodes())

    # Allows engine to recognize inverse color image as additional scan. Mode can be used when barcode is white on black background.
    #  Value:
    # Allows engine to recognize inverse color image.
    def getAllowInvertImage(self):
        return self.getJavaClass().getAllowInvertImage()

    # Allows engine to recognize inverse color image as additional scan. Mode can be used when barcode is white on black background.
    #  Value:
    # Allows engine to recognize inverse color image.
    def setAllowInvertImage(self, value):
        self.getJavaClass().setAllowInvertImage(value)

    # Allows engine to recognize barcodes which has incorrect checksumm or incorrect values.
    # Mode can be used to recognize damaged barcodes with incorrect text.
    #  Value:
    # Allows engine to recognize incorrect barcodes.
    def getAllowIncorrectBarcodes(self):
        return self.getJavaClass().getAllowIncorrectBarcodes()

    # Allows engine to recognize barcodes which has incorrect checksumm or incorrect values.
    # Mode can be used to recognize damaged barcodes with incorrect text.
    #  Value:
    # Allows engine to recognize incorrect barcodes.
    def setAllowIncorrectBarcodes(self, value):
        self.getJavaClass().setAllowIncorrectBarcodes(value)

    #  Allows engine to recognize tiny barcodes on large images. Ignored if <see cref="AllowIncorrectBarcodes"/> is set to True. Default value: False.
    # @return If True, allows engine to recognize tiny barcodes on large images.
    def getReadTinyBarcodes(self):
        return self.getJavaClass().getReadTinyBarcodes()

    # Allows engine to recognize tiny barcodes on large images. Ignored if <see cref="AllowIncorrectBarcodes"/> is set to True. Default value: False.
    # @param value If True, allows engine to recognize tiny barcodes on large images.
    def setReadTinyBarcodes(self, value):
        self.getJavaClass().setReadTinyBarcodes(value)

    # Allows engine to recognize color barcodes on color background as additional scan. Extremely slow mode.
    #  Value:
    # Allows engine to recognize color barcodes on color background.
    def getAllowComplexBackground(self):
        return self.getJavaClass().getAllowComplexBackground()

    # Allows engine to recognize color barcodes on color background as additional scan. Extremely slow mode.
    #  Value:v
    # Allows engine to recognize color barcodes on color background.
    def setAllowComplexBackground(self, value):
        self.getJavaClass().setAllowComplexBackground(value)

    # Allows engine to enable median smoothing as additional scan. Mode helps to recognize noised barcodes.
    #  Value:
    # Allows engine to enable median smoothing.
    def getAllowMedianSmoothing(self):
        return self.getJavaClass().getAllowMedianSmoothing()

    # Allows engine to enable median smoothing as additional scan. Mode helps to recognize noised barcodes.
    #  Value:
    # Allows engine to enable median smoothing.
    def setAllowMedianSmoothing(self, value):
        self.getJavaClass().setAllowMedianSmoothing(value)

    # Window size for median smoothing. Typical values are 3 or 4. Default value is 3. AllowMedianSmoothing must be set.
    #  Value:
    # Window size for median smoothing.
    def getMedianSmoothingWindowSize(self):
        return self.getJavaClass().getMedianSmoothingWindowSize()

    # Window size for median smoothing. Typical values are 3 or 4. Default value is 3. AllowMedianSmoothing must be set.
    #  Value:
    # Window size for median smoothing.
    def setMedianSmoothingWindowSize(self, value):
        self.getJavaClass().setMedianSmoothingWindowSize(value)

    # Allows engine to recognize regular image without any restorations as main scan. Mode to recognize image as is.
    #  Value:
    # Allows to recognize regular image without any restorations.
    def getAllowRegularImage(self):
        return self.getJavaClass().getAllowRegularImage()

    # Allows engine to recognize regular image without any restorations as main scan. Mode to recognize image as is.
    #  Value:
    # Allows to recognize regular image without any restorations.
    def setAllowRegularImage(self, value):
        self.getJavaClass().setAllowRegularImage(value)

    # Allows engine to recognize decreased image as additional scan. Size for decreasing is selected by internal engine algorithms.
    # Mode helps to recognize barcodes which are noised and blurred but captured with high resolution.
    #  Value:
    # Allows engine to recognize decreased image
    def getAllowDecreasedImage(self):
        return self.getJavaClass().getAllowDecreasedImage()

    # Allows engine to recognize decreased image as additional scan. Size for decreasing is selected by internal engine algorithms.
    # Mode helps to recognize barcodes which are noised and blurred but captured with high resolution.
    #  Value:
    # Allows engine to recognize decreased image
    def setAllowDecreasedImage(self, value):
        self.getJavaClass().setAllowDecreasedImage(value)

    # Allows engine to recognize image without small white spots as additional scan. Mode helps to recognize noised image as well as median smoothing filtering.
    #  Value:
    # Allows engine to recognize image without small white spots.
    def getAllowWhiteSpotsRemoving(self):
        return self.getJavaClass().getAllowWhiteSpotsRemoving()

    # Allows engine to recognize image without small white spots as additional scan. Mode helps to recognize noised image as well as median smoothing filtering.
    #  Value:
    # Allows engine to recognize image without small white spots.
    def setAllowWhiteSpotsRemoving(self, value):
        self.getJavaClass().setAllowWhiteSpotsRemoving(value)

    # Allows engine for 1D barcodes to recognize regular image with different params as additional scan. Mode helps to recongize low height 1D barcodes.
    #  Value:
    # Allows engine for 1D barcodes to run additional scan.
    def getAllowOneDAdditionalScan(self):
        return self.getJavaClass().getAllowOneDAdditionalScan()

    # Allows engine for 1D barcodes to recognize regular image with different params as additional scan. Mode helps to recongize low height 1D barcodes.
    #  Value:
    # Allows engine for 1D barcodes to run additional scan.
    def setAllowOneDAdditionalScan(self, value):
        self.getJavaClass().setAllowOneDAdditionalScan(value)

    # Allows engine for 1D barcodes to quickly recognize high quality barcodes which fill almost whole image.
    # Mode helps to quickly recognize generated barcodes from Internet.
    #  Value:
    # Allows engine for 1D barcodes to quickly recognize high quality barcodes.
    def getAllowOneDFastBarcodesDetector(self):
        return self.getJavaClass().getAllowOneDFastBarcodesDetector()

    # Allows engine for 1D barcodes to quickly recognize high quality barcodes which fill almost whole image.
    # Mode helps to quickly recognize generated barcodes from Internet.
    #  Value:
    # Allows engine for 1D barcodes to quickly recognize high quality barcodes.
    def setAllowOneDFastBarcodesDetector(self, value):
        self.getJavaClass().setAllowOneDFastBarcodesDetector(value)

    # Allows engine for Postal barcodes to recognize slightly noised images. Mode helps to recognize sligtly damaged Postal barcodes.
    #  Value:
    # Allows engine for Postal barcodes to recognize slightly noised images.
    def getAllowMicroWhiteSpotsRemoving(self):
        return self.getJavaClass().getAllowMicroWhiteSpotsRemoving()

    # Allows engine for Postal barcodes to recognize slightly noised images. Mode helps to recognize sligtly damaged Postal barcodes.
    #  Value:
    # Allows engine for Postal barcodes to recognize slightly noised images.
    def setAllowMicroWhiteSpotsRemoving(self, value):
        self.getJavaClass().setAllowMicroWhiteSpotsRemoving(value)

    # Allows engine to recognize barcodes with salt and paper noise type. Mode can remove small noise with white and black dots.
    #  Value:
    # Allows engine to recognize barcodes with salt and paper noise type.
    def getAllowSaltAndPaperFiltering(self):
        return self.getJavaClass().getAllowSaltAndPaperFiltering()

    # Allows engine to recognize barcodes with salt and paper noise type. Mode can remove small noise with white and black dots.
    #  Value:
    # Allows engine to recognize barcodes with salt and paper noise type.
    def setAllowSaltAndPaperFiltering(self, value):
        self.getJavaClass().setAllowSaltAndPaperFiltering(value)

    # Allows engine to use gap between scans to increase recognition speed. Mode can make recognition problems with low height barcodes.
    #  Value:
    # Allows engine to use gap between scans to increase recognition speed.
    def getAllowDetectScanGap(self):
        return self.getJavaClass().getAllowDetectScanGap()

    # Allows engine to use gap between scans to increase recognition speed. Mode can make recognition problems with low height barcodes.
    #  Value:
    # Allows engine to use gap between scans to increase recognition speed.
    def setAllowDetectScanGap(self, value):
        self.getJavaClass().setAllowDetectScanGap(value)

    # Allows engine for Datamatrix to recognize dashed industrial Datamatrix barcodes.
    # Slow mode which helps only for dashed barcodes which consist from spots.
    #  Value:
    # Allows engine for Datamatrix to recognize dashed industrial barcodes.
    def getAllowDatamatrixIndustrialBarcodes(self):
        return self.getJavaClass().getAllowDatamatrixIndustrialBarcodes()

    # Allows engine for Datamatrix to recognize dashed industrial Datamatrix barcodes.
    # Slow mode which helps only for dashed barcodes which consist from spots.
    #  Value:
    # Allows engine for Datamatrix to recognize dashed industrial barcodes.
    def setAllowDatamatrixIndustrialBarcodes(self, value):
        self.getJavaClass().setAllowDatamatrixIndustrialBarcodes(value)

    # Allows engine for QR/MicroQR to recognize damaged MicroQR barcodes.
    #  Value:
    # Allows engine for QR/MicroQR to recognize damaged MicroQR barcodes.
    def getAllowQRMicroQrRestoration(self):
        return self.getJavaClass().getAllowQRMicroQrRestoration()

    # Allows engine for QR/MicroQR to recognize damaged MicroQR barcodes.
    #  Value:
    # Allows engine for QR/MicroQR to recognize damaged MicroQR barcodes.
    def setAllowQRMicroQrRestoration(self, value):
        self.getJavaClass().setAllowQRMicroQrRestoration(value)

    # Allows engine for 1D barcodes to recognize barcodes with single wiped/glued bars in pattern.
    #  Value:
    # Allows engine for 1D barcodes to recognize barcodes with single wiped/glued bars in pattern.
    def getAllowOneDWipedBarsRestoration(self):
        return self.getJavaClass().getAllowOneDWipedBarsRestoration()

    # Allows engine for 1D barcodes to recognize barcodes with single wiped/glued bars in pattern.
    #  Value:
    # Allows engine for 1D barcodes to recognize barcodes with single wiped/glued bars in pattern.
    def setAllowOneDWipedBarsRestoration(self, value):
        self.getJavaClass().setAllowOneDWipedBarsRestoration(value)

    # Barcode detector settings.
    def getDetectorSettings(self):
        return self.detectorSettings

    # Barcode detector settings.
    def setDetectorSettings(self, value):
        self.getJavaClass().setDetectorSettings(value)
        self.detectorSettings = value

    # apply all values from Src setting to this
    # @param Src source settings
    def applyAll(self, Src):
        self.setAllowInvertImage(Src.getAllowInvertImage())
        self.setAllowIncorrectBarcodes(Src.getAllowIncorrectBarcodes())
        self.setAllowComplexBackground(Src.getAllowComplexBackground())
        self.setAllowMedianSmoothing(Src.getAllowMedianSmoothing())
        self.setMedianSmoothingWindowSize(Src.getMedianSmoothingWindowSize())
        self.setAllowRegularImage(Src.getAllowRegularImage())
        self.setAllowDecreasedImage(Src.getAllowDecreasedImage())
        self.setAllowWhiteSpotsRemoving(Src.getAllowWhiteSpotsRemoving())
        self.setAllowOneDAdditionalScan(Src.getAllowOneDAdditionalScan())
        self.setAllowOneDFastBarcodesDetector(Src.getAllowOneDFastBarcodesDetector())
        self.setAllowMicroWhiteSpotsRemoving(Src.getAllowMicroWhiteSpotsRemoving())
        self.setAllowSaltAndPaperFiltering(Src.getAllowSaltAndPaperFiltering())
        self.setAllowDetectScanGap(Src.getAllowDetectScanGap())

# Contains the data of subtype for Code128 type barcode
class Code128DataPortion (Assist.BaseJavaClass):
    javaClassName = "com.aspose.mw.barcode.recognition.MwCode128DataPortion"

    # Creates a new instance of the {@code Code128DataPortion} class with start code symbol and decoded codetext.
    # @param code128SubType A start encoding symbol
    # @param data A partial codetext
    def __init__(self, code128SubType, data):
        java_link = jpype.JClass(self.javaClassName)
        if isinstance(code128SubType, Code128SubType):
            code128DataPortion = java_link(str(code128SubType.value), data)
        else:
            code128DataPortion = java_link(str(code128SubType), data)

        super().__init__(code128DataPortion)
        self.init()

    def construct(javaClass):
        code128DataPortion = Code128DataPortion(0, "")
        code128DataPortion.setJavaClass(javaClass)
        return code128DataPortion

    # Gets the part of code text related to subtype.
    # @return The part of code text related to subtype
    def getData(self):
        return self.getJavaClass().getData()

    # Gets the part of code text related to subtype.
    # @return The part of code text related to subtype
    def setData(self, value):
        self.getJavaClass().setData(value)

    # Gets the type of Code128 subset
    # @return The type of Code128 subset
    def getCode128SubType(self):
        return self.getJavaClass().getCode128SubType()

    # Gets the type of Code128 subset
    # @return The type of Code128 subset
    def setCode128SubType(self, value):
        self.getJavaClass().setCode128SubType(value)

    def init(self):
        return
        #TODO

    # Returns a human-readable string representation of this {@code Code128DataPortion}.
    # @return A string that represents this {@code Code128DataPortion}.
    def toString(self):
        return self.getJavaClass().toString()

# Stores a DataBar additional information of recognized barcode
# BarCodeReader reader = new BarCodeReader("c:\\test.png", DecodeType.DATABAR_OMNI_DIRECTIONAL);
#
# for(BarCodeResult result : reader.readBarCodes())
#    System.out.println("BarCode Type: " + result.getCodeTypeName());
#    System.out.println("BarCode CodeText: " + result.getCodeText());
#    System.out.println("QR Structured Append Quantity: " + result.getExtended().getQR().getQRStructuredAppendModeBarCodesQuantity());
class DataBarExtendedParameters(Assist.BaseJavaClass):

    javaClassName = "com.aspose.mw.barcode.recognition.MwDataBarExtendedParameters"

    def init(self):
        pass

    
    # Gets the DataBar 2D composite component flag. Default value is false.
    # @return The DataBar 2D composite component flag.
    def is2DCompositeComponent(self):
        return self.getJavaClass().is2DCompositeComponent()


    # Returns a value indicating whether this instance is equal to a specified <see cref="DataBarExtendedParameters"/> value.
    # @param obj An System.Object value to compare to this instance.
    # @return <b>true</b> if obj has the same value as this instance; otherwise, <b>false</b>.
    def equals(self, obj):
        return DataBarExtendedParameters.op_Equality(self, obj)


    # <p>
    # Returns a value indicating whether the first {@code BarCodeExtendedParameters} value is equal to the second.
                                                                                                           # </p>
    # @return {@code <b>true</b>} if first has the same value as second; otherwise, {@code <b>false</b>}.
    # @param first A first compared value
    # @param second A second compared value
    @staticmethod
    def op_Equality(first, second):
        java_link = jpype.JClass(DecodeType.javaClassName)
        javaClass = java_link()
        return javaClass.op_Equality(first.getJavaClass(), second.getJavaClass())


    # Returns a value indicating if the first <see cref="DataBarExtendedParameters"/> value is different from the second.
    # @param first A first compared value
    # @param second A second compared value
    # @return <b>true</b> if first has the different value from second; otherwise, <b>false</b>.
    @staticmethod
    def op_Inequality(first, second):
        return not DataBarExtendedParameters.op_Equality(first, second)


    # Returns the hash code for this instance.
                                     # @return A 32-bit signed integer hash code.

    def hashcode(self):
        return self.getJavaClass().hashcode()


    # Returns a human-readable string representation of this <see cref="DataBarExtendedParameters"/>.
    # @return A string that represents this <see cref="DataBarExtendedParameters"/>.
    def toString(self):
        return self.getJavaClass().toString()

# Specify the type of barcode to read.
# This sample shows how to detect Code39 and Code128 barcodes.
# reader = BarCodeReader("test.png", null,  [ DecodeType.CODE_39_STANDARD, DecodeType.CODE_128 ])
# for result in reader.readBarCodes():
#    print("BarCode Type: " + result.getCodeTypeName())
#    print("BarCode CodeText: " + result.getCodeText())
class DecodeType(Enum):

        # Unspecified decode type.
        NONE = -1

        # Specifies that the data should be decoded with {@code <b>CODABAR</b>} barcode specification
        CODABAR = 0

        # Specifies that the data should be decoded with {@code <b>CODE 11</b>} barcode specification
        CODE_11 = 1

        # Specifies that the data should be decoded with {@code <b>Standard CODE 39</b>} barcode specification
        CODE_39_STANDARD = 2

        # Specifies that the data should be decoded with {@code <b>Extended CODE 39</b>} barcode specification
        CODE_39_EXTENDED = 3

        # Specifies that the data should be decoded with {@code <b>Standard CODE 93</b>} barcode specification
        CODE_93_STANDARD = 4

        # Specifies that the data should be decoded with {@code <b>Extended CODE 93</b>} barcode specification
        CODE_93_EXTENDED = 5

        # Specifies that the data should be decoded with {@code <b>CODE 128</b>} barcode specification
        CODE_128 = 6

        # Specifies that the data should be decoded with {@code <b>GS1 CODE 128</b>} barcode specification
        GS_1_CODE_128 = 7

        # Specifies that the data should be decoded with {@code <b>EAN-8</b>} barcode specification
        EAN_8 = 8

        # Specifies that the data should be decoded with {@code <b>EAN-13</b>} barcode specification
        EAN_13 = 9

        # Specifies that the data should be decoded with {@code <b>EAN14</b>} barcode specification
        EAN_14 = 10

        # Specifies that the data should be decoded with {@code <b>SCC14</b>} barcode specification
        SCC_14 = 11

        # Specifies that the data should be decoded with {@code <b>SSCC18</b>} barcode specification
        SSCC_18 = 12

        # Specifies that the data should be decoded with {@code <b>UPC-A</b>} barcode specification
        UPCA = 13

        # Specifies that the data should be decoded with {@code <b>UPC-E</b>} barcode specification
        UPCE = 14

        # Specifies that the data should be decoded with {@code <b>ISBN</b>} barcode specification
        ISBN = 15

        # Specifies that the data should be decoded with {@code <b>Standard 2 of 5</b>} barcode specification
        STANDARD_2_OF_5 = 16

        # Specifies that the data should be decoded with {@code <b>INTERLEAVED 2 of 5</b>} barcode specification
        INTERLEAVED_2_OF_5 = 17

        # Specifies that the data should be decoded with {@code <b>Matrix 2 of 5</b>} barcode specification
        MATRIX_2_OF_5 = 18

        # Specifies that the data should be decoded with {@code <b>Italian Post 25</b>} barcode specification
        ITALIAN_POST_25 = 19

        # Specifies that the data should be decoded with {@code <b>IATA 2 of 5</b>} barcode specification. IATA (International Air Transport Association) uses this barcode for the management of air cargo.
        IATA_2_OF_5 = 20

        # Specifies that the data should be decoded with {@code <b>ITF14</b>} barcode specification
        ITF_14 = 21

        # Specifies that the data should be decoded with {@code <b>ITF6</b>} barcode specification
        ITF_6 = 22

        # Specifies that the data should be decoded with {@code <b>MSI Plessey</b>} barcode specification
        MSI = 23

        # Specifies that the data should be decoded with {@code <b>VIN</b>} (Vehicle Identification Number) barcode specification
        VIN = 24

        # Specifies that the data should be decoded with {@code <b>DeutschePost Ident code</b>} barcode specification
        DEUTSCHE_POST_IDENTCODE = 25

        # Specifies that the data should be decoded with {@code <b>DeutschePost Leit code</b>} barcode specification
        DEUTSCHE_POST_LEITCODE = 26

        # Specifies that the data should be decoded with {@code <b>OPC</b>} barcode specification
        OPC = 27

        # Specifies that the data should be decoded with {@code <b>PZN</b>} barcode specification. This symbology is also known as Pharma Zentral Nummer
        PZN = 28

        # Specifies that the data should be decoded with {@code <b>Pharmacode</b>} barcode. This symbology is also known as Pharmaceutical BINARY Code
        PHARMACODE = 29

        # Specifies that the data should be decoded with {@code <b>DataMatrix</b>} barcode symbology
        DATA_MATRIX = 30

        # Specifies that the data should be decoded with {@code <b>GS1DataMatrix</b>} barcode symbology
        GS_1_DATA_MATRIX = 31

        # Specifies that the data should be decoded with {@code <b>QR Code</b>} barcode specification
        QR = 32

        # Specifies that the data should be decoded with {@code <b>Aztec</b>} barcode specification
        AZTEC = 33

        # Specifies that the data should be decoded with {@code <b>Pdf417</b>} barcode symbology
        PDF_417 = 34

        # Specifies that the data should be decoded with {@code <b>MacroPdf417</b>} barcode specification
        MACRO_PDF_417 = 35

        # Specifies that the data should be decoded with {@code <b>MicroPdf417</b>} barcode specification
        MICRO_PDF_417 = 36

        # Specifies that the data should be decoded with {@code <b>CodablockF</b>} barcode specification
        CODABLOCK_F = 65

        # Specifies that the data should be decoded with {@code <b>Australia Post</b>} barcode specification
        AUSTRALIA_POST = 37

        # Specifies that the data should be decoded with {@code <b>Postnet</b>} barcode specification
        POSTNET = 38

        # Specifies that the data should be decoded with {@code <b>Planet</b>} barcode specification
        PLANET = 39

        # Specifies that the data should be decoded with USPS {@code <b>OneCode</b>} barcode specification
        ONE_CODE = 40

         # Specifies that the data should be decoded with {@code <b>RM4SCC</b>} barcode specification. RM4SCC (Royal Mail 4-state Customer Code) is used for automated mail sort process in UK.
        RM_4_SCC = 41

        # Specifies that the data should be decoded with {@code <b>GS1 DATABAR omni-directional</b>} barcode specification
        DATABAR_OMNI_DIRECTIONAL = 42

        # Specifies that the data should be decoded with {@code <b>GS1 DATABAR truncated</b>} barcode specification
        DATABAR_TRUNCATED = 43

        # Specifies that the data should be decoded with {@code <b>GS1 DATABAR limited</b>} barcode specification
        DATABAR_LIMITED = 44

        # Specifies that the data should be decoded with {@code <b>GS1 DATABAR expanded</b>} barcode specification
        DATABAR_EXPANDED = 45

        # Specifies that the data should be decoded with {@code <b>GS1 DATABAR stacked omni-directional</b>} barcode specification
        DATABAR_STACKED_OMNI_DIRECTIONAL = 53

        # Specifies that the data should be decoded with {@code <b>GS1 DATABAR stacked</b>} barcode specification
        DATABAR_STACKED = 54

        # Specifies that the data should be decoded with {@code <b>GS1 DATABAR expanded stacked</b>} barcode specification
        DATABAR_EXPANDED_STACKED = 55

        # Specifies that the data should be decoded with {@code <b>Patch code</b>} barcode specification. Barcode symbology is used for automated scanning
        PATCH_CODE = 46

        # Specifies that the data should be decoded with {@code <b>ISSN</b>} barcode specification
        ISSN = 47

        # Specifies that the data should be decoded with {@code <b>ISMN</b>} barcode specification
        ISMN = 48

        # Specifies that the data should be decoded with {@code <b>Supplement(EAN2 EAN5)</b>} barcode specification
        SUPPLEMENT = 49

        # Specifies that the data should be decoded with {@code <b>Australian Post Domestic eParcel Barcode</b>} barcode specification
        AUSTRALIAN_POSTE_PARCEL = 50

        # Specifies that the data should be decoded with {@code <b>Swiss Post Parcel Barcode</b>} barcode specification
        SWISS_POST_PARCEL = 51

        # Specifies that the data should be decoded with {@code <b>SCode16K</b>} barcode specification
        CODE_16_K = 52

        # Specifies that the data should be decoded with {@code <b>MicroQR Code</b>} barcode specification
        MICRO_QR = 56

        # Specifies that the data should be decoded with {@code <b>CompactPdf417</b>} (Pdf417Truncated) barcode specification
        COMPACT_PDF_417 = 57

        # Specifies that the data should be decoded with {@code <b>GS1 QR</b>} barcode specification
        GS_1_QR = 58

        # Specifies that the data should be decoded with {@code <b>MaxiCode</b>} barcode specification
        MAXI_CODE = 59

        # Specifies that the data should be decoded with {@code <b>MICR E-13B</b>} blank specification
        MICR_E_13_B = 60

        # Specifies that the data should be decoded with {@code <b>Code32</b>} blank specification
        CODE_32 = 61

        # Specifies that the data should be decoded with {@code <b>DataLogic 2 of 5</b>} blank specification
        DATA_LOGIC_2_OF_5 = 62

        # Specifies that the data should be decoded with {@code <b>DotCode</b>} blank specification
        DOT_CODE = 63

        # Specifies that the data should be decoded with {@code <b>DotCode</b>} blank specification
        DUTCH_KIX = 64

        # Specifies that data will be checked with all available symbologies
        ALL_SUPPORTED_TYPES = 66

        # Specifies that data will be checked with all of  1D  barcode symbologies
        TYPES_1D = 67

        # Specifies that data will be checked with all of  1.5D POSTAL  barcode symbologies, like  Planet, Postnet, AustraliaPost, OneCode, RM4SCC, DutchKIX
        POSTAL_TYPES = 68

        # Specifies that data will be checked with most commonly used symbologies
        MOST_COMMON_TYPES = 69

    
        # Specifies that data will be checked with all of <b>2D</b> barcode symbologies
        TYPES_2D = 70


        javaClassName = "com.aspose.mw.barcode.recognition.MwDecodeTypeUtils"

    
        # Determines if the specified <see cref="BaseDecodeType"/> contains any 1D barcode symbology
        # @param $symbology
        # @return string <b>true</b> if <see cref="BaseDecodeType"/> contains any 1D barcode symbology; otherwise, returns <b>false</b>.
        @staticmethod
        def is1D(symbology):
            java_link = jpype.JClass(DecodeType.javaClassName)
            javaClass = java_link()
            return javaClass.is1D(symbology)


        # Determines if the specified <see cref="BaseDecodeType"/> contains any Postal barcode symbology
        # @param symbology The <see cref="BaseDecodeType"/> to test
        # @return Returns <b>true</b> if <see cref="BaseDecodeType"/> contains any Postal barcode symbology; otherwise, returns <b>false</b>.
        @staticmethod
        def isPostal(symbology):
            java_link = jpype.JClass(DecodeType.javaClassName)
            javaClass = java_link()
            return javaClass.isPostal(symbology)


        # Determines if the specified <see cref="BaseDecodeType"/> contains any 2D barcode symbology
        # @param symbology The <see cref="BaseDecodeType"/> to test.
        # @return Returns <b>true</b> if <see cref="BaseDecodeType"/> contains any 2D barcode symbology; otherwise, returns <b>false</b>.
        @staticmethod
        def is2D(symbology):
            java_link = jpype.JClass(DecodeType.javaClassName)
            javaClass = java_link()
            return javaClass.is2D(symbology)

        @staticmethod
        def containsAny(decodeType, decodeTypes):
            java_link = jpype.JClass(DecodeType.javaClassName)
            javaClass = java_link()
            return javaClass.containsAny(decodeTypes)

class Code128SubType(Enum):
    
        # ASCII characters 00 to 95 (0–9, A–Z and control codes), special characters, and FNC 1–4 ///
        CODE_SET_A = 1

        # ASCII characters 32 to 127 (0–9, A–Z, a–z), special characters, and FNC 1–4 ///
        CODE_SET_B = 2

        # 00–99 (encodes two digits with a single code point) and FNC1 ///
        CODE_SET_C = 3

# Defines the interpreting type(C_TABLE or N_TABLE) of customer information for AustralianPost BarCode.
class CustomerInformationInterpretingType(Enum):
    
        # Use C_TABLE to interpret the customer information. Allows A..Z, a..z, 1..9, space and # sing.
        # generator = BarcodeGenerator(EncodeTypes.AUSTRALIA_POST, "5912345678ABCde")
        # generator.getParameters().getBarcode().getAustralianPost().setAustralianPostEncodingTable(CustomerInformationInterpretingType.C_TABLE)
        # image = generator.generateBarCodeImage()
        # reader = BarCodeReader(image, DecodeType.AUSTRALIA_POST)
        # reader.setCustomerInformationInterpretingType(CustomerInformationInterpretingType.C_TABLE)
        # for result in reader.readBarCodes():
        #     print("BarCode Type: " + result.getCodeType())
        #     print("BarCode CodeText: " + result.getCodeText())
        C_TABLE = 0

        # Use N_TABLE to interpret the customer information. Allows digits.
        #  generator = BarcodeGenerator(EncodeTypes.AUSTRALIA_POST, "59123456781234567")
        #  generator.getParameters().getBarcode().getAustralianPost().setAustralianPostEncodingTable(CustomerInformationInterpretingType.N_TABLE)
        #  image = generator.generateBarCodeImage()
        #  reader = BarCodeReader(image, DecodeType.AUSTRALIA_POST)
        #  reader.setCustomerInformationInterpretingType(CustomerInformationInterpretingType.N_TABLE)
        # for result in reader.readBarCodes():
        #     print("BarCode Type: " + result.getCodeType())
        #     print("BarCode CodeText: " + result.getCodeText())
        N_TABLE = 1

        # Do not interpret the customer information. Allows 0, 1, 2 or 3 symbol only.
        # generator = BarcodeGenerator(EncodeTypes.AUSTRALIA_POST, "59123456780123012301230123")
        # generator.getParameters().getBarcode().getAustralianPost().setAustralianPostEncodingTable(CustomerInformationInterpretingType.OTHER)
        # image = generator.generateBarCodeImage()
        # reader = BarCodeReader(image, DecodeType.AUSTRALIA_POST)
        # reader.CustomerInformationInterpretingType = CustomerInformationInterpretingType.OTHER)
        # for result in reader.readBarCodes():
        #    print("BarCode Type: " + result.getCodeType())
        #    print("BarCode CodeText: " + result.getCodeText())
        OTHER = 2

# Contains recognition confidence level
# This sample shows how BarCodeConfidence changed, depending on barcode type
# //Moderate confidence
# generator = BarcodeGenerator(EncodeTypes.CODE_128, "12345")
# generator.save("test.png")
# reader = BarCodeReader("test.png", null,  [DecodeType.CODE_39_STANDARD, DecodeType.CODE_128])
# for result in reader.readBarCodes():
#    print("BarCode Type: " + result.getCodeTypeName())
#    print("BarCode CodeText: " + result.getCodeText())
#    print("BarCode Confidence: " + result.getConfidence())
#    print("BarCode ReadingQuality: " + result.getReadingQuality())
# //Strong confidence
# generator = BarcodeGenerator(EncodeTypes.QR, "12345")
# generator.save("test.png")
# reader = BarCodeReader("test.png", null,  [DecodeType.CODE_39_STANDARD, DecodeType.QR])
# for result in reader.readBarCodes():
#     print("BarCode Type: " + result.getCodeTypeName())
#     print("BarCode CodeText: " + result.getCodeText())
#     print("BarCode Confidence: " + result.getConfidence())
#     print("BarCode ReadingQuality: " + result.getReadingQuality())
class BarCodeConfidence(Enum):
    
        # Recognition confidence of barcode where codetext was not recognized correctly or barcode was detected as posible fake
        NONE = "0"

        # Recognition confidence of barcode (mostly 1D barcodes) with weak checksumm or even without it. Could contains some misrecognitions in codetext
        # or even fake recognitions if  is low

        # @see BarCodeResult.ReadingQuality
        MODERATE = "80"

        # Recognition confidence which was confirmed with BCH codes like Reed–Solomon. There must not be errors in read codetext or fake recognitions
        STRONG = "100"


# Enable checksum validation during recognition for 1D barcodes.
# Default is treated as Yes for symbologies which must contain checksum, as No where checksum only possible.
# Checksum never used: Codabar
# Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN
# Checksum always used: Rest symbologies
# This sample shows influence of ChecksumValidation on recognition quality and results
# generator = BarcodeGenerator(EncodeTypes.EAN_13, "1234567890128")
# generator.save("test.png")
# reader = BarCodeReader("test.png", DecodeType.EAN_13)
# //checksum disabled
# reader.setChecksumValidation(ChecksumValidation.OFF)
# for result in reader.readBarCodes():
#    print("BarCode CodeText: " + result.getCodeText())
#    print("BarCode Value: " + result.getExtended().getOneD().getValue())
#    print("BarCode Checksum: " + result.getExtended().getOneD().getCheckSum())
# reader = BarCodeReader("test.png", DecodeType.EAN_13)
# //checksum enabled
# reader.setChecksumValidation(ChecksumValidation.ON)
# for result in reader.readBarCodes():
#    print("BarCode CodeText: " + result.getCodeText())
#    print("BarCode Value: " + result.getExtended().getOneD().getValue())
#    print("BarCode Checksum: " + result.getExtended().getOneD().getCheckSum())
class ChecksumValidation(Enum):

    # If checksum is required by the specification - it will be validated.
    _default = 0

    # Always validate checksum if possible.
    ON = 1

    # Do not validate checksum.
    OFF = 2