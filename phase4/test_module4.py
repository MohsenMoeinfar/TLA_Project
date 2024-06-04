import unittest
import os
import module4
from utils import utils


class TestModule2(unittest.TestCase):
    def test(self):
        test_directory = "../data/module3Test"
        image_files = [file for file in os.listdir(test_directory) if file.endswith((".jpg", ".png"))]
        json_files = [file for file in os.listdir(test_directory) if file.endswith(".json")]

        image_files.sort()
        json_files.sort()

        for i in range(len(image_files)):
            image_file = image_files[i]
            json_file = json_files[i]

            image_path = os.path.join(test_directory, image_file)
            json_path = os.path.join(test_directory, json_file)

            with open(json_path, 'r') as file:
                json_fa = file.read()

            binary_array = utils.convert_pictures_to_gray_scale_and_binary_array(image_path, 128)
            binary_array2 = module4.solve(json_fa, 128)

            self.assertEqual(binary_array, binary_array2)


if __name__ == "__main__":
    unittest.main()
