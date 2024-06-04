import unittest
import os
import module3
from utils import utils


class TestModule3(unittest.TestCase):
    def test(self):
        test_directory = "../data/module3Test"
        image_files = [file for file in os.listdir(test_directory) if file.endswith((".jpg", ".png"))]
        json_files = [file for file in os.listdir(test_directory) if file.endswith(".json")]

        image_files.sort()
        json_files.sort()

        bin_picture_list = []
        json_fa_list = []

        for image_file in image_files:
            image_path = os.path.join(test_directory, image_file)

            binary_array = utils.convert_pictures_to_gray_scale_and_binary_array(image_path, 128)

            bin_picture_list.append(binary_array)
        
        for json_file in json_files:
            json_path = os.path.join(test_directory, json_file)

            with open(json_path, 'r') as file:
                json_fa = file.read()
            
            json_fa_list.append(json_fa)
        
        res = module3.solve(json_fa_list, bin_picture_list)

        for i in range(len(res)):
            self.assertEqual(i, res[i])


if __name__ == "__main__":
    unittest.main()
