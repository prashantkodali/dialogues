import json
import os
from collections import OrderedDict, defaultdict


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            return self.default_factory(key)


class RisawozMapping(object):
    def __init__(self):

        # currently untranslated
        self.API_MAP = keydefaultdict(lambda k: k)
        self.zh_API_MAP = keydefaultdict(lambda k: k)
        self.en_API_MAP = keydefaultdict(lambda k: k)
        self.zh_en_API_MAP = keydefaultdict(lambda k: k)

        self.entity_map = keydefaultdict(lambda k: k)
        self.reverse_entity_map = keydefaultdict(lambda k: k)

        self.zh2en_VALUE_MAP = keydefaultdict(lambda k: k)
        self.en2zh_VALUE_MAP = keydefaultdict(lambda k: k)

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(cur_dir, "mappings/zh2en_missing.json")) as f:
            self.zh2en_missing_MAP = json.load(f)

        self.en2zh_missing_MAP = keydefaultdict(lambda k: k)

        self.en2zh_RELATION_MAP = {"equal_to": "等于", "not": "非", "less_than": "少于", "at_least": "至少", "one_of": "其中之一"}
        self.zh2en_RELATION_MAP = {v: k for k, v in self.en2zh_RELATION_MAP.items()}

        self.zh2en_SPECIAL_MAP = {"不在乎": "don't care"}
        self.en2zh_SPECIAL_MAP = {v: k for k, v in self.zh2en_SPECIAL_MAP.items()}

        # TODO: this mapping should only include slots that are required to make an api call for the domain. It should not include all the slots.
        self.DOMAIN_SLOT_MAP = {
            '医院': ['区域', '名称', '门诊时间', '挂号时间', 'DSA', '3.0T MRI', '重点科室', '电话', '公交线路', '地铁可达', 'CT', '等级', '性质', '类别', '地址'],
            '天气': ['温度', '目的地', '日期', '城市', '风力风向', '天气', '紫外线强度'],
            '旅游景点': [
                '门票价格',
                '电话号码',
                '菜系',
                '名称',
                '评分',
                '最适合人群',
                '房费',
                '景点类型',
                '房型',
                '推荐菜',
                '消费',
                '开放时间',
                '价位',
                '是否地铁直达',
                '区域',
                '地址',
                '特点',
            ],
            '汽车': [
                '座椅通风',
                '油耗水平',
                '级别',
                '能源类型',
                '名称',
                '价格',
                '驱动方式',
                '所属价格区间',
                '车型',
                '座位数',
                '座椅加热',
                '倒车影像',
                '定速巡航',
                '动力水平',
                '车系',
                '厂商',
            ],
            '火车': ['出发时间', '票价', '目的地', '车型', '舱位档次', '日期', '时长', '到达时间', '车次信息', '出发地', '准点率', '航班信息', '坐席'],
            '电影': ['制片国家/地区', '豆瓣评分', '片名', '主演名单', '具体上映时间', '导演', '片长', '类型', '年代', '主演'],
            '电脑': [
                '价格区间',
                '内存容量',
                '商品名称',
                '显卡型号',
                '裸机重量',
                '价格',
                '品牌',
                '系统',
                'CPU型号',
                '系列',
                '特性',
                '屏幕尺寸',
                '游戏性能',
                '分类',
                '产品类别',
                '待机时长',
                '色系',
                '硬盘容量',
                'CPU',
                '显卡类别',
            ],
            '电视剧': ['制片国家/地区', '豆瓣评分', '片名', '主演名单', '首播时间', '导演', '片长', '集数', '单集片长', '类型', '年代', '主演'],
            '辅导班': [
                '开始日期',
                '老师',
                '上课方式',
                '校区',
                '价格',
                '难度',
                '时段',
                '课时',
                '科目',
                '班号',
                '结束日期',
                '年级',
                '下课时间',
                '教室地点',
                '每周',
                '课次',
                '上课时间',
                '区域',
            ],
            '酒店': ['电话号码', '星级', '名称', '房费', '地址', '地铁是否直达', '房型', '停车场', '推荐菜', '酒店类型', '价位', '是否地铁直达', '区域', '评分'],
            '飞机': ['出发时间', '票价', '温度', '目的地', '起飞时间', '舱位档次', '日期', '城市', '到达时间', '出发地', '准点率', '航班信息', '天气'],
            '餐厅': ['营业时间', '电话号码', '菜系', '名称', '评分', '房费', '人均消费', '推荐菜', '开放时间', '价位', '是否地铁直达', '区域', '地址'],
            '通用': [],
        }

        self.zh2en_DOMAIN_MAP = {
            # currently untranslated
            "天气": "weather",
            "火车": "train",
            "电脑": "pc",
            "电影": "movie",
            "辅导班": "class",
            "汽车": "car",
            "餐厅": "restaurant",
            "酒店": "hotel",
            "旅游景点": "attraction",
            "飞机": "flight",
            "医院": "hospital",
            "电视剧": "tv",
            "通用": "general",
        }
        self.en2zh_DOMAIN_MAP = {v: k for k, v in self.zh2en_DOMAIN_MAP.items()}

        # TODO: update below
        self.required_slots = {
            **{k: [] for k, v in self.DOMAIN_SLOT_MAP.items()},
            **{self.zh2en_DOMAIN_MAP[k]: [] for k, v in self.DOMAIN_SLOT_MAP.items()},
        }
        self.api_names = list(self.required_slots.keys())

        self.zh2en_ACT_MAP = {
            # untranslated in the original dataset
            'inform': 'inform',
            'general': 'general',
            'greeting': 'greeting',
            'bye': 'bye',
            'request': 'request',
            'recommend': 'recommend',
            'no-offer': 'no-offer',
        }
        self.en2zh_ACT_MAP = {v: k for k, v in self.zh2en_ACT_MAP.items()}

        self.zh2en_SLOT_MAP = {
            '价格区间': 'price_range',
            '性质': 'nature',
            '特性': 'feature',
            '电话': 'phone',
            '推荐菜': 'recommended_dishes',
            '舱位档次': 'class_of_service',
            '教室地点': 'classroom_location',
            '票价': 'fare',
            '硬盘容量': 'hard_disk_capacity',
            '紫外线强度': 'uv_intensity',
            '价位': 'cost',
            '油耗水平': 'fuel_consumption_level',
            '下课时间': 'get_out_of_class_closing_time',
            '产品类别': 'product_category',
            '具体上映时间': 'specific_release_time',
            '门票价格': 'ticket_price',
            '座位数': 'number_of_seats',
            '动力水平': 'power_level',
            '座椅通风': 'seat_ventilation',
            '上课时间': 'class_time',
            '裸机重量': 'bare_metal_weight',
            '地铁可达': 'metro_reachable',
            '消费': 'consumption',
            '厂商': 'manufacturer',
            '上课方式': 'class_method',
            '科目': 'subject',
            '起飞时间': 'take_off_time',
            '目的地': 'destination',
            '到达时间': 'arrival_time',
            '主演名单': 'starring_list',
            '日期': 'date',
            '时长': 'duration',
            '内存容量': 'memory_capacity',
            '能源类型': 'energy_type',
            '区域': 'area',
            '门诊时间': 'outpatient_time',
            'CT': 'ct',
            '片名': 'title_of_film',
            '驱动方式': 'drive_method',
            '城市': 'city',
            '定速巡航': 'cruise_cruise',
            '制片国家/地区': 'country_of_production',
            '类型': 'type',
            '系列': 'series',
            '名称': 'name',
            '导演': 'director',
            '坐席': 'seat',
            '座椅加热': 'seat_heating',
            '菜系': 'cuisine',
            '系统': 'system',
            '景点类型': 'attraction_type',
            '片长': 'slice_length',
            '课时': 'class_hour',
            '营业时间': 'business_hours',
            '倒车影像': 'backup_image',
            '车型': 'model',
            '主演': 'starring',
            '地址': 'address',
            '最适合人群': 'best_for_the_crowd',
            '挂号时间': 'registration_time',
            '3.0T MRI': '3.0t_mri',
            '难度': 'difficulty',
            '开始日期': 'start_date',
            '出发地': 'departure',
            '房型': 'room_type',
            '显卡类别': 'graphics_card_type',
            '车系': 'car_series',
            '校区': 'campus',
            'DSA': 'dsa',
            '天气': 'weather',
            '重点科室': 'key_department',
            '首播时间': 'first_broadcast_time',
            '电话号码': 'phone_number',
            '温度': 'temperature',
            '分类': 'classification',
            '类别': 'category',
            '色系': 'color_system',
            '评分': 'rating',
            '等级': 'ranking',
            '星级': 'star',
            'CPU型号': 'cpu_model',
            '屏幕尺寸': 'screen_size',
            '游戏性能': 'game_performance',
            '集数': 'number_of_episodes',
            'CPU': 'cpu',
            '准点率': 'on-time_rate',
            '商品名称': 'product_name',
            '级别': 'level',
            '年代': 'age',
            '特点': 'features',
            '停车场': 'parking_lot',
            '豆瓣评分': 'douban_score',
            '车次信息': 'train_information',
            '人均消费': 'per_capita_consumption',
            '品牌': 'brand',
            '每周': 'weekly',
            '时段': 'time_period',
            '年级': 'grade',
            '课次': 'lessons',
            '价格': 'price',
            '结束日期': 'end_date',
            '房费': 'room_rate',
            '公交线路': 'bus_line',
            '出发时间': 'departure_time',
            '待机时长': 'standby_time',
            '单集片长': 'single_episode_length',
            '老师': 'teacher',
            '风力风向': 'wind_wind_direction',
            '航班信息': 'flight_information',
            '显卡型号': 'graphics_card_model',
            '开放时间': 'open_hours',
            '是否地铁直达': 'whether_the_subway_goes_directly',
            '酒店类型': 'hotel_type',
            '所属价格区间': 'the_price_range_it_belongs_to',
            '班号': 'class_number',
            '地铁是否直达': 'whether_the_subway_is_direct',
            # added
            '可用选项': 'available_options',
        }
        self.en2zh_SLOT_MAP = {v: k for k, v in self.zh2en_SLOT_MAP.items()}

        translation_dict = {
            **self.zh2en_DOMAIN_MAP,
            **self.zh2en_SLOT_MAP,
            **self.zh2en_ACT_MAP,
            **self.zh2en_RELATION_MAP,
            **self.zh2en_SPECIAL_MAP,
        }
        self.translation_dict = OrderedDict(sorted(translation_dict.items(), key=lambda item: len(item[0]), reverse=True))
