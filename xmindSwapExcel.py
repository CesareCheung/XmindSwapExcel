from xmindparser import xmind_to_dict
import xlwt
from fileRead import fileExtract


class xmind_to_excel:
    def ximd_num(self, value):
        '''获取xmind标题个数'''
        try:
            return len(value['topics'])
        except KeyError:
            return 0

    def styles(self):
        """设置单元格的样式的基础方法"""
        self.style = xlwt.XFStyle()
        return self.style

    def borders(self, status=0):
        """设置单元格的边框细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7大粗虚线:8，
        细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13"""
        self.border = xlwt.Borders()
        self.border.left = status
        self.border.right = status
        self.border.top = status
        self.border.bottom = status
        return self.border

    def heights(self, worksheet, line, size=4):
        """设置单元格的高度"""
        self.worksheet.row(line).height_mismatch = True
        self.worksheet.row(line).height = size * 256

    def widths(self, worksheet, line, size=11):
        """设置单元格的宽度"""
        self.worksheet.col(line).width = size * 256

    def alignments(self, **kwargs):
        """设置单元格的对齐方式
        status有两种：horz（水平），vert（垂直）
        horz中的direction常用的有：CENTER（居中）,DISTRIBUTED（两端）,GENERAL,CENTER_ACROSS_SEL（分散）,RIGHT（右边）,LEFT（左边）
        vert中的direction常用的有：CENTER（居中）,DISTRIBUTED（两端）,BOTTOM(下方),TOP（上方）"""
        self.alignment = xlwt.Alignment()

        if "horz" in kwargs.keys():
            self.alignment.horz = eval(f"xlwt.Alignment.HORZ_{kwargs['horz'].upper()}")
            if "vert" in kwargs.keys():
                self.alignment.vert = eval(f"xlwt.Alignment.VERT_{kwargs['vert'].upper()}")
                self.alignment.wrap = 1  # 设置自动换行
            return self.alignment

    def fonts(self, name='宋体', bold=False, underline=False, italic=False, colour='black', height=11):
        """设置单元格中字体的样式
        默认字体为宋体，不加粗，没有下划线，不是斜体，黑色字体"""
        self.font = xlwt.Font()
        # 字体
        self.font.name = name
        # 加粗
        self.font.bold = bold
        # 下划线
        self.font.underline = underline
        # 斜体
        self.font.italic = italic
        # 颜色
        self.font.colour_index = xlwt.Style.colour_map[colour]
        # 大小
        self.font.height = 20 * height
        return self.font

    def patterns(self, colors=1):
        """设置单元格的背景颜色，该数字表示的颜色在xlwt库的其他方法中也适用，默认颜色为白色
        0 = Black, 1 = White,2 = Red, 3 = Green, 4 = Blue,5 = Yellow, 6 = Magenta, 7 = Cyan,
        16 = Maroon, 17 = Dark Green,18 = Dark Blue, 19 = Dark Yellow ,almost brown), 20 = Dark Magenta,
        21 = Teal, 22 = Light Gray,23 = Dark Gray, the list goes on..."""
        self.pattern = xlwt.Pattern()
        self.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        self.pattern.pattern_fore_colour = colors
        return self.pattern

    def cat_xmind(self, fileName):
        self.all = xmind_to_dict(fileName)
        print(self.all)
        self.ExcelName = self.all[0]['topic']['title']

        # 获取xmind模块名称集合
        self.xmind_modleName = self.all[0]['topic']['topics']  #
        # 获取xmind用例
        self.xmind_caseNum = self.xmind_modleName[0]['topics']

        print(self.ExcelName.replace('\n', ''), self.xmind_modleName)
        print(len(self.xmind_modleName), len(self.xmind_caseNum))

        for m in range(len(self.xmind_modleName)):
            print(self.xmind_modleName[m]['topics'][0]['topics'][0]['topics'])
            # print(self.modleName[m]['topics'][0]['topics'][0]['topics'][0]['topics'])
            try:
                if 'topics' in self.xmind_modleName[m]['topics'][0]['topics'][0]['topics'][0].keys():
                    print('what happend')
                    print(self.xmind_modleName[m]['topics'][0]['title'])
                    self.Moudle = self.ExcelName + '\\' + self.xmind_modleName[m]['title'] + '\\' + \
                                  self.xmind_modleName[m]['topics'][0]['title']
                else:
                    print(self.xmind_modleName[m]['title'])
                    self.Moudle = self.ExcelName + '\\' + self.xmind_modleName[m]['title']
            except AssertionError:
                print("处理异常")

            print(self.Moudle)
        self.xmindLevel = self.xmind_modleName[0]
        print()

    def assureLevel(self, *args):
        if ['priority-1'] in args:
            self.testcaseLevel = '1'
        elif ['priority-2'] in args:
            self.testcaseLevel = '2'
        elif ['priority-3'] in args:
            self.testcaseLevel = '3'
        else:
            self.testcaseLevel = '4'
        return self.testcaseLevel

    def write_Excel(self, fileName):
        # 将xmind内容转换成列表内容
        self.xmind_out = xmind_to_dict(fileName)
        # 获取xmind标题
        self.xmind_name = self.xmind_out[0]['topic']['title']
        # 获取xmind模块名称集合
        self.xmind_modleName = self.xmind_out[0]['topic']['topics']
        # 获取xmind用例
        self.xmind_caseNum = self.xmind_modleName[0]['topics']

        # 创建一个workbook 设置编码
        self.workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        self.worksheet = self.workbook.add_sheet(self.xmind_name)

        # 表格头字段写入
        self.rows0 =["用例目录","用例名称","需求ID","前置条件","用例步骤","预期结果","用例类型","用例状态","用例等级","创建人"]

        # 定义一个计数器，统计测试用例数量
        num = 0
        # for i in range(len(self.rows0)):
        #     self.worksheet.write(0, i, self.rows0[i])
        sizes = [10, 10, 10, 15, 30, 10, 50, 50, 10, 10, 10, 15, 10, 10]
        # 设置单元格对齐方式
        dicts = {"horz": "CENTER", "vert": "CENTER"}
        self.style2 = self.styles()
        self.style2.alignment = self.alignments(**dicts)
        """设置单元格中字体的样式默认字体为宋体，不加粗，没有下划线，不是斜体，黑色字体"""
        self.style2.font = self.fonts()
        self.style2.borders = self.borders()
        self.style2.pattern = self.patterns(7)
        self.heights(self.worksheet, 0)
        for i in range(len(self.rows0)):
            self.worksheet.write(0, i, self.rows0[i], self.style2)
            self.widths(self.worksheet, i, size=sizes[i])

        self.style = self.styles()
        self.style.borders = self.borders()

        for m in range(len(self.xmind_modleName)):
            # 获取测试结果
            self.testResult = self.xmind_modleName[m]['topics'][0]['topics'][0]['topics']
            print('获取到的结果为：', self.testResult)

            # 获取xmind用例
            # self.xmind_caseNum = self.xmind_modleName[m]['topics']
            if 'topics' in self.testResult[0].keys():
                self.xmind_caseNum = len(self.xmind_modleName[m]['topics'][0]['topics'])
            else:
                self.xmind_caseNum = len(self.xmind_modleName[m]['topics'])
            print('获取到的模块测试用例数量为：' + str(self.xmind_caseNum))

            for n in range(self.xmind_caseNum):
                '''将模块名称写入到文件中
                1.如果模块中没有子模块，写入模块到测试案例路径
                2.如果模块中有子模块，将父模块和子模块拼接起来写入模块到测试案例路径
                3.读取测试用例名称，将测试用例名称写入excel的测试案例名称
                4.读取测试步骤，将测试用例名称写入excel的测试案例描述
                5.读取预期结果，将测试用例名称写入excel的预期结果
                6.读取优先级标识，将测试用例名称写入excel的优先级
              '''

                try:
                    if 'topics' in self.testResult[0].keys():
                        print('获取到的用例模块为xmind_modleName：' + self.xmind_modleName[m]['topics'][0]['title'])
                        # 测试案例路径
                        self.excel_modleName = self.xmind_modleName[m]['topics'][0]['title']
                        print("测试路径excel_modleName："+self.excel_modleName)
                        # 测试用例名称
                        self.testcaseName = self.xmind_modleName[m]['topics'][0]['topics'][n]['title']
                        print('获取到的测试用例名称为####：' + self.testcaseName, '~~~~~~' + str(n))

                        # 判断测试用例是否有测试步骤,有则写入excel
                        # print('------------',self.xmind_modleName[m]['topics'][0]['topics'][n]['topics'])
                        if 'topics' in self.xmind_modleName[m]['topics'][0]['topics'][n]['topics'][0]:
                            self.testFront = self.xmind_modleName[m]['topics'][0]['topics'][n]['topics'][0]['title']
                            print('获取到的前置条件为~~：' + self.testFront)

                            # 用例有子模块，且拥有测试步骤，提取预期结果
                            self.testStep = \
                                self.xmind_modleName[m]['topics'][0]['topics'][n]['topics'][0]['topics'][0]['title']
                            print('获取到的测试步骤结果为：' + self.testStep)
                            #用例有子模块，且拥有测试步骤，提取预期结果
                            self.ecptctResult = self.xmind_modleName[m]['topics'][0]['topics'][n]['topics'][0]['topics'][0]['topics'][0]['title']
                            print('获取到的测试预期结果为：' + self.ecptctResult)

                        else:
                            self.testFront = None
                            print('获取到的前置条件为~~：', self.testFront)

                            # 用例有子模块，且没有前置条件，提取预期结果
                            self.ecptctResult = self.xmind_modleName[m]['topics'][0]['topics'][n]['topics'][0][
                                'title']
                            print('获取到的测试预期结果为：' + self.ecptctResult)

                            # self.testFront = self.xmind_modleName[m]['topics'][0]['topics'][n]['topics'][0]['topics'][0]['title']
                            # print('获取到的测试前置条件为：' + self.testFront)

                        # 获取测试用例优先级
                        if 'makers' not in self.xmind_modleName[m]['topics'][0]['topics'][n]:
                            self.testcaseLevel = self.assureLevel(['priority-3'])
                        else:
                            self.testcaseLevel = self.xmind_modleName[m]['topics'][0]['topics'][n]['makers']
                            self.testcaseLevel = self.assureLevel(self.testcaseLevel)
                        print('测试用例级别为：', self.testcaseLevel)

                    else:
                        print('获取到的用例模块名称为：' + self.xmind_modleName[m]['title'])
                        self.excel_modleName = self.xmind_modleName[m]['title']
                        self.testcaseName = self.xmind_modleName[m]['topics'][n]['title']
                        print('获取到的测试用例名称为：' + self.testcaseName)

                        # 判断测试用例是否有测试步骤,有则写入excel
                        if 'topics' in self.xmind_modleName[m]['topics'][n]['topics'][0]:
                            self.testStep = self.xmind_modleName[m]['topics'][n]['topics'][0]['title']
                            print('获取到的测试步骤为~~：' + self.testStep)

                            # 测试前置条件
                            self.testFront = \
                                self.xmind_modleName[m]['topics'][0]['topics'][n]['topics'][0]['title']
                            print('获取到的测试前置条件为：' + self.testFront)

                            # 用例没有子模块，且拥有测试步骤，提取预期结果
                            self.ecptctResult = self.xmind_modleName[m]['topics'][n]['topics'][0]['topics'][0]['topics'][0][
                                'title']
                            print('获取到的测试预期结果为：' + self.ecptctResult)

                        else:
                            self.testStep = None
                            print('获取到的测试步骤为~~：', self.testStep)

                            # 用例没有子模块，且没有测试步骤，提取预期结果
                            self.ecptctResult = self.xmind_modleName[m]['topics'][n]['topics'][0]['topics'][0]['topics'][0]['title']
                            print('获取到的测试预期结果为：' + self.ecptctResult)

                            self.testFront = self.xmind_modleName[m]['topics'][0]['topics'][n]['title']
                            print('获取到的测试前置条件为：' + self.testFront)
                        # 获取测试用例优先级
                        if 'makers' not in self.xmind_modleName[m]['topics'][n]:
                            self.testcaseLevel = self.assureLevel(['priority-2'])
                        else:
                            self.testcaseLevel = self.xmind_modleName[m]['topics'][n]['makers']
                            self.testcaseLevel = self.assureLevel(self.testcaseLevel)
                        print('测试用例级别为：', self.testcaseLevel)

                except AssertionError:
                    print("处理异常")
                num += 1
                print('开始写入行数', num)
                #
                # 将所属产品名称写入excel
                self.worksheet.write(num, 0, fileExtract('prodectName'), self.style)
                # 将平台名称写入excel
                # self.worksheet.write(num, 1, fileExtract('platform'), self.style)
                # 读取xmind模块，将所属模块名称写入excel
                # self.worksheet.write(num, 2, fileExtract('modleName'), self.style)
                # 读取xmind测试用例名称，将测试用例名称写入excel
                self.worksheet.write(num, 1, self.testcaseName, self.style)
                #读取需求ID
                self.worksheet.write(num, 2, fileExtract('demand_id'), self.style)

                self.worksheet.write(num, 3, self.testFront, self.style)

                # 读取xmind测试用例步骤，将测试用例步骤写入excel
                self.worksheet.write(num, 4, self.testStep, self.style)
                # 读取xmind测试用例预期结果，将测试用例预期结果写入excel
                self.worksheet.write(num, 5, self.ecptctResult, self.style)
                # 将用例类型写入excel
                self.worksheet.write(num, 6, fileExtract('caseType'), self.style)

                # 将用例状态写入excel
                self.worksheet.write(num, 7, fileExtract('caseStatus'), self.style)

                # 读取xmind测试用例级别，将测试用例级别写入excel
                self.worksheet.write(num, 8, self.testcaseLevel, self.style)

                # 将由谁创建写入excel
                self.worksheet.write(num, 9, fileExtract('author'), self.style)


                # 保存文件到excel
                self.workbook.save(self.xmind_name.replace(' ', '') + '.xls')


if __name__ == '__main__':
    xm = xmind_to_excel()
    # xm.cat_xmind("C:\\Users\\EDY\\Desktop\\test.xmind")
    # xm.cat_xmind("C:\\Users\\EDY\\Desktop\\aaa.xmind")
    # # xm.cat_xmind("C:\\Users\\deanywang\\Desktop\\test.xmind")
    xm.write_Excel("C:\\Users\\1\\Documents\\XmindSwapExcel\\客服系统11.xmind")


