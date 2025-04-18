from parsel import Selector
import unittest
import komiku

class TestMangaKomiku(unittest.TestCase) :
    def setUp(self) :
        self.ruri = komiku.Manga("ruri-dragon").syn()
        self.gaga = komiku.Manga("ruri-s").syn()

    def test_gaga(self) :
        data = self.gaga

        self.assertIsNone(data.result)
        self.assertFalse(data.is_success)
        self.assertEqual(data.code, 404)

    def test_request(self) :
        data = self.ruri

        self.assertTrue(data.is_success)
        self.assertIsNotNone(data.headers)
    
    def test_parser(self) :
        page = self.ruri.page
        
        self.assertEqual(type(page), Selector)
        self.assertEqual(page.css("title::text").get(), "Komik Ruri Dragon - Komiku")
        self.assertEqual(len(page.css("table.inftable tr td")), 16)

    def test_manga_metadata(self) :
        data = self.ruri.result

        self.assertEqual(data["title"], "Ruri Dragon")
        self.assertEqual(data["poster"], "https://cover.komiku.id/wp-content/uploads/2022/09/Manga-Ruri-Dragon.jpg")
        self.assertEqual(data["author"], "Shindou Masaoki ")
        self.assertEqual(data["totalChapters"], 33)
        self.assertEqual(len(data["chapters"]), data["totalChapters"])

        self.assertGreater(len(data["genre"]), 0)
        self.assertGreater(len(data["chapters"]), 1)


class TestChapterKomiku(unittest.TestCase) :
    def setUp(self) :
        self.ruri = komiku.Chapter("ruri-dragon-chapter-31").syn()
    
    def test_parser(self) :
        page = self.ruri.page
        
        self.assertEqual(type(page), Selector)
        self.assertEqual(page.css("title::text").get(), "Chapter 31 - Komik Ruri Dragon - Komiku")
        self.assertEqual(len(page.css("table.tbl tbody tr td")), 6)

    def test_chapter_metadata(self) :
        data = self.ruri.result

        self.assertEqual(data["name"], "Komik Ruri Dragon Chapter 31")
        self.assertEqual(data["chapter"], "31")
        self.assertEqual(len(data["pagesUrl"]), 20)


if __name__ == "__main__" :
    unittest.main()        