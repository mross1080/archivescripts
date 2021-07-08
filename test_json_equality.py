import unittest
from archive_scripts.archive_to_json import extract_content_from_archive,create_archive,strip_sentence
import json

class TestSum(unittest.TestCase):

    # def test_irregular_file(self):
    #     extract_content_from_archive("")

    white_list = {
        0:[22,24],
        1:[],
        2:[],3:[],4:[2],5:[],6:[3],7:[],8:[2],9:[2]

    }

    def test_correct_archive(self):

        canonical_archive_raw = open('TestimonyDB.json', 'r',encoding="utf8")
        canonical_archive = json.load(canonical_archive_raw)

        generated_archive_raw = open('archive.json', 'r',encoding="utf8")
        generated_archive = json.load(generated_archive_raw)

        for question_index, question_data in enumerate(generated_archive):
            print("\n\nLooking at Question {} index {} \n\n".format(generated_archive[question_index]['name'],question_index))


            self.assertEqual(canonical_archive[question_index]['id'], generated_archive[question_index]['id'])
            self.assertEqual(canonical_archive[question_index]['name'], generated_archive[question_index]['name'])
            self.assertEqual(canonical_archive[question_index]['question'], generated_archive[question_index]['question'])

            for convo_index, conversation in enumerate(canonical_archive[question_index]["data"]):
                if convo_index not in self.white_list[question_index]:
                    print("Testing Equality of Conversation {} of Question {}".format(convo_index,
                                                                                      canonical_archive[question_index]['name']))

                    for index,msg in enumerate(conversation):

                        # print(index)
                        # print(conversation[index]["msg_body"])
                        print(generated_archive[question_index]["data"][convo_index][index]["msg_body"])
                        self.assertEqual(conversation[index]["msg_body"].strip(" "), generated_archive[question_index]["data"][convo_index][index]["msg_body"].strip(" "))
                        self.assertEqual(conversation[index]["msg_file_type"].strip(" "), generated_archive[question_index]["data"][convo_index][index]["msg_file_type"].strip(" "))

                else:
                    print("Skipping Conversation {} of Question {}".format(convo_index,
                                                                                      canonical_archive[question_index]['name']))


if __name__ == '__main__':
    unittest.main()