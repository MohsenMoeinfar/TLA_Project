import unittest
import os
import module1
from utils import utils


class TestModule1(unittest.TestCase):
    def test(self):
        test_directory = "../data/module1Test"
        image_files = [file for file in os.listdir(test_directory) if file.endswith((".jpg", ".png"))]
        image_files.sort()
        address_file = [file for file in os.listdir(test_directory) if file.endswith('.txt')][0]
        with open(os.path.join(test_directory, address_file), 'r') as file:
            addresses = file.readlines()

        for i, s in enumerate(addresses):
            if s[-1] == '\n':
                addresses[i] = s[:-1].split(':')
            else:
                addresses[i] = s.split(':')

        for img_ind, image_file in enumerate(image_files):
            image_path = os.path.join(test_directory, image_file)

            binary_array = utils.convert_pictures_to_gray_scale_and_binary_array(image_path)

            fa = module1.solve(binary_array)

            self.assertIsNotNone(fa)

            for address in addresses:
                state = fa.init_state
                for char in address[0]:
                    state = state.transitions[char]

                if fa.is_final(state):
                    self.assertEqual('1', address[1][img_ind], '1')
                else:
                    self.assertEqual('0', address[1][img_ind], '0')


if __name__ == "__main__":
    unittest.main()
