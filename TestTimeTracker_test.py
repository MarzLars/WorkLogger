import unittest
from time_tracker import TimeTracker
from unittest.mock import patch

class TestTimeTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = TimeTracker()

    def test_initial_state(self):
        self.assertIsNone(self.tracker.start_time)
        self.assertEqual(self.tracker.elapsed_time, 0)
        self.assertFalse(self.tracker.running)

    @patch('time_tracker.time')
    def test_start(self, mock_time):
        mock_time.time.return_value = 1000
        self.tracker.start()
        self.assertEqual(self.tracker.start_time, 1000)
        self.assertTrue(self.tracker.running)

    @patch('time_tracker.time')
    def test_pause(self, mock_time):
        mock_time.time.return_value = 1000
        self.tracker.start()
        mock_time.time.return_value = 2000
        self.tracker.pause()
        self.assertEqual(self.tracker.elapsed_time, 1000)
        self.assertFalse(self.tracker.running)

    @patch('time_tracker.time')
    def test_stop(self, mock_time):
        mock_time.time.return_value = 1000
        self.tracker.start()
        mock_time.time.return_value = 2000
        self.tracker.stop()
        self.assertEqual(self.tracker.elapsed_time, 1000)
        self.assertFalse(self.tracker.running)

    def test_reset(self):
        self.tracker.start()
        self.tracker.reset()
        self.assertIsNone(self.tracker.start_time)
        self.assertEqual(self.tracker.elapsed_time, 0)
        self.assertFalse(self.tracker.running)

    def test_log_time(self):
        self.tracker.elapsed_time = 99 * 3600 + 99 * 60 + 99  # 99 hours, 99 minutes, 99 seconds
        description = "Test log"
        print(f"Before log_time: {self.tracker.elapsed_time}")
        self.tracker.log_time(description)
        print(f"After log_time: {self.tracker.elapsed_time}")
        self.assertEqual(self.tracker.elapsed_time, 99 * 3600 + 99 * 60 + 99)

if __name__ == '__main__':
    unittest.main()