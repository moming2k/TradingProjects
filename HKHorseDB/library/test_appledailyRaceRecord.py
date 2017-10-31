from unittest import TestCase
from appledailyRaceRecord import AppledailyRaceRecord


class TestAppledailyRaceRecord(TestCase):
    def setUp(self):
        self.appledaily_race_record = AppledailyRaceRecord()

    def test_get_race_records_with_cache(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        records = self.appledaily_race_record.get_race_records()
        print(records[0:10])

    # Skip this one unless reconstruct as it need longer time to run ( 1218.113s more )
    def test_get_race_records_without_pickle_cache(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        self.appledaily_race_record.show_debug = True
        self.appledaily_race_record.use_pickle_cache = False
        self.appledaily_race_record.save_html_cache = False
        self.appledaily_race_record.get_race_records()

    def test_get_race_record(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        records = self.appledaily_race_record.get_race_record('20170625', '01')
        self.assertIsNotNone(records)
        # print(records)

    def test_get_race_record_by_race_record_id(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        self.appledaily_race_record.show_debug = True
        records = self.appledaily_race_record.get_race_record_by_race_record_id('20170625_01')
        print(records)
        self.assertIsNotNone(records)

    # 20070603_05 is not exist
    # def test_get_race_record_by_race_record_id_20070603_05(self):
    #     self.appledaily_race_record = AppledailyRaceRecord()
    #     self.appledaily_race_record.show_debug = True
    #     records = self.appledaily_race_record.get_race_record_by_race_record_id('20070603_05')
    #     self.assertIsNotNone(records)

    def test_get_race_records_ids_with_cache(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        self.appledaily_race_record.get_race_records_ids()

    def test_get_race_records_ids_without_pickle_cache(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        self.appledaily_race_record.use_pickle_cache = False
        self.appledaily_race_record.save_html_cache = False
        ids = self.appledaily_race_record.get_race_records_ids()
        self.assertGreater(len(ids), 8000, "race ids array should have more than 8000 records")

        print(ids[0:20])

    def test_race_count_by_date_with_html_cache(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        race_count = self.appledaily_race_record.race_count_by_date('20170625')
        self.assertGreater(race_count, 0, "Race count should be greater than zero")

    def test_race_count_by_date_without_html_cache(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        self.appledaily_race_record.show_debug = True
        self.appledaily_race_record.use_html_cache = False

        race_count = self.appledaily_race_record.race_count_by_date('20170625')
        self.assertGreater(race_count, 0, "Race count should be greater than zero")

    def test_get_horse_detail(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        self.appledaily_race_record.show_debug = True
        self.appledaily_race_record.use_html_cache = True

        self.appledaily_race_record.get_horse_detail('horse1.php?temp_horid=12063')

    def test_process_horse_detail(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        self.appledaily_race_record.show_debug = True
        self.appledaily_race_record.use_html_cache = True

        # html = self.appledaily_race_record.get_horse_detail('horse1.php?temp_horid=12063')
        # self.appledaily_race_record.process_horse_detail('horse1.php?temp_horid=12063', html) #3D5881

        html = self.appledaily_race_record.get_horse_detail('horse1.php?temp_horid=3D5881')
        horse_overall_ranking_df, horse_track_ranking_df = self.appledaily_race_record.process_horse_detail('horse1.php?temp_horid=3D5881', html)  # 3D5881
        print(horse_overall_ranking_df)
        print(horse_track_ranking_df)

    def test_get_all_horse_detail(self):
        self.appledaily_race_record = AppledailyRaceRecord()
        self.appledaily_race_record.show_debug = True
        self.appledaily_race_record.use_pickle_cache = True
        self.appledaily_race_record.use_html_cache = True
        self.appledaily_race_record.save_html_cache = True

        horse_overall_ranking, horse_track_ranking = self.appledaily_race_record.get_all_horse_detail()
