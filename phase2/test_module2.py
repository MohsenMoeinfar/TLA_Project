import unittest
import os
import module2
from utils import utils


class TestModule2(unittest.TestCase):
    def test(self):
        test_directory = "../data/module2Test"
        image_files = [file for file in os.listdir(test_directory) if file.endswith((".jpg", ".png"))]
        image_files.sort()

        json_fa_file = "json_fa.json"
        with open(os.path.join(test_directory, json_fa_file), 'r') as file:
            json_fa = file.read()

        image_file = image_files[0]
        image_path = os.path.join(test_directory, image_file)

        binary_array = utils.convert_pictures_to_gray_scale_and_binary_array(image_path, 64)

        res = module2.solve(json_fa, binary_array)

        self.assertEqual(res, True)

        image_file = image_files[1]
        image_path = os.path.join(test_directory, image_file)

        binary_array = utils.convert_pictures_to_gray_scale_and_binary_array(image_path, 64)

        res = module2.solve(json_fa, binary_array)

        self.assertEqual(res, False)


if __name__ == "__main__":
    unittest.main()
