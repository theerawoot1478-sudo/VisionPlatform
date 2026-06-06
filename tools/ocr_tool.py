import easyocr


class OCRTool:

    def __init__(self):

        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    def inspect(
        self,
        image
    ):

        try:

            result = self.reader.readtext(
                image
            )

            text = ""

            for item in result:

                text += item[1] + " "

            text = text.strip()

            return {

                "result": "OK",

                "score": 100,

                "text": text

            }

        except Exception as e:

            print(e)

            return {

                "result": "NG",

                "score": 0,

                "text": ""

            }