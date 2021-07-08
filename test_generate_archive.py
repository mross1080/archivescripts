import unittest
from archive_scripts.archive_to_json import extract_content_from_archive,create_archive,strip_sentence

class TestSum(unittest.TestCase):

    def test_format_sentence(self):
        # create_archive()

        sentence_1 = "2/10/20 12:28 p. m. - Los mensajes y las llamadas están cifrados de extremo a extremo. Nadie fuera de este chat, ni siquiera WhatsApp, puede leerlos ni escucharlos. Toca para obtener más información."
        s2 = "2/10/20 12:28 p. m. - +1 (849) 635-8744: ¿Testigos para?"
        self.assertEqual(strip_sentence(s2),"¿Testigos para?")

        s3 = "2/10/20 12:29 p. m. - I.I.R.D: Buenas"
        self.assertEqual(strip_sentence(s3), "Buenas")





if __name__ == '__main__':
    unittest.main()