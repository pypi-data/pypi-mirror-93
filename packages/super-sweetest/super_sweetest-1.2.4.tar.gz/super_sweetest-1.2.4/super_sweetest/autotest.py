
from pathlib import Path
import sys
from super_sweetest.data import testsuite_format, testsuite2data, testsuite2report
from super_sweetest.parse import parse
from super_sweetest.elements import e
from super_sweetest.globals import g
from super_sweetest.windows import w
from super_sweetest.testsuite import TestSuite
from super_sweetest.utility import Excel, get_record, mkdir
from super_sweetest.log import logger, set_log
from super_sweetest.junit import JUnit
from super_sweetest.report import summary, markdown
from validator_sa.package_authentication import msg
from super_sweetest.config import _testcase, _elements, _report


class Autotest:
    def __init__(self, file_name, sheet_name, desired_caps={}, server_url=''):
        SERVER_URL_ = None
        if desired_caps:
            self.desired_caps = desired_caps
        else:
            from super_sweetest.servers.common import read_lib_app_config
            self.desired_caps, SERVER_URL = read_lib_app_config()
            SERVER_URL_ = SERVER_URL
        if not self.desired_caps and not SERVER_URL_: # 没有任何配置时
            self.desired_caps = {'platformName': 'Desktop', 'browserName': 'Chrome'} # 源代码
        self.server_url = server_url if not SERVER_URL_ else SERVER_URL_
        self.conditions = {}
        g.plan_name = file_name.split('-')[0]
        g.init(self.desired_caps, self.server_url)

        plan_path = Path('snapshot') / g.plan_name
        task_path = plan_path / g.start_time[1:] 

        for p in ('JUnit', 'report', 'snapshot', plan_path, task_path, 'report/' + g.plan_name):
            mkdir(p)
                  
        g.plan_data['log'] = set_log(logger, task_path)
        
        self.testcase_file = str(
            Path('testcase') / (file_name + '-' + _testcase + '.xlsx'))
        self.elements_file = str(
            Path('element') / (g.plan_name + '-' + _elements + '.xlsx'))
        self.report_xml = str(
            Path('JUnit') / (file_name + '-' + _report + g.start_time + '.xml'))
        self.testcase_workbook = Excel(self.testcase_file, 'r')
        self.sheet_names = self.testcase_workbook.get_sheet(sheet_name)
        self.report_excel = str(Path(
            'report') / g.plan_name / (file_name + '-' + _report + g.start_time + '.xlsx'))
        self.report_workbook = Excel(self.report_excel, 'w')

        self.report_data = {}  # 测试报告详细数据

    def fliter(self, **kwargs):
        # 筛选要执行的测试用例
        self.conditions = kwargs

    def plan(self, row_num=None):
        self.code = 0  # 返回码
        # 1.解析配置文件, row_num 调试 只运行某行用例
        try:
            e.get_elements(self.elements_file)
        except:
            logger.exception('*** Parse config file failure ***')
            self.code = -1
            sys.exit(self.code)

        self.junit = JUnit()
        self.junit_suite = {}

        # 2.逐个执行测试套件
        for sheet_name in self.sheet_names:
            g.sheet_name = sheet_name
            # xml 测试报告初始化
            self.junit_suite[sheet_name] = self.junit.create_suite(
                g.plan_name, sheet_name)
            self.junit_suite[sheet_name].start()

            self.run(sheet_name, row_num)

        self.plan_data = g.plan_end()
        self.testsuite_data = g.testsuite_data

        summary_data = summary(
            self.plan_data, self.testsuite_data, self.report_data, {})
        self.report_workbook.write(summary_data, '_Summary_')
        self.report_workbook.close()

        with open(self.report_xml, 'w', encoding='utf-8') as f:
            self.junit.write(f)

    def run(self, sheet_name, row_num=None):
        # 1.从 Excel 获取测试用例集 , row_num 调试 只运行某行用例
        try:
            data = self.testcase_workbook.read(sheet_name, row_num)
            testsuite = testsuite_format(data)
            msg()
            # logger.info('Testsuite imported from Excel:\n' +
            #             json.dumps(testsuite, ensure_ascii=False, indent=4))
            logger.info('From Excel import testsuite success')
        except:
            logger.exception('*** From Excel import testsuite failure ***')
            self.code = -1
            sys.exit(self.code)

        # 2.初始化全局对象
        try:
            g.set_driver()
            # 如果测试数据文件存在，则从该文件里读取数据，赋值到全局变量列表里
            data_file = Path('data') / (g.plan_name +
                                        '-' + sheet_name + '.csv')
            if data_file.is_file():
                g.var = get_record(str(data_file))
            w.init()
        except:
            logger.exception('*** Init global object failure ***')
            self.code = -1
            sys.exit(self.code)

        # 3.解析测试用例集
        try:
            parse(testsuite)
            logger.debug('testsuite has been parsed:\n' + str(testsuite))
        except:
            logger.exception('*** Parse testsuite failure ***')
            self.code = -1
            sys.exit(self.code)

        # 4.执行测试套件
        ts = TestSuite(testsuite, sheet_name,
                       self.junit_suite[sheet_name], self.conditions)
        ts.run()

        # 5.判断测试结果
        if self.junit_suite[sheet_name].high_errors + self.junit_suite[sheet_name].medium_errors + \
                self.junit_suite[sheet_name].high_failures + self.junit_suite[sheet_name].medium_failures:
            self.code = -1

        # 6.保存测试结果
        try:
            data = testsuite2data(testsuite)
            self.report_workbook.write(data, sheet_name)
            self.report_data[sheet_name] = testsuite2report(testsuite)
        except:
            logger.exception('*** Save the report is failure ***')


    def md(self, md_path):
        markdown(self.plan_data, self.testsuite_data, self.report_data, md_path)