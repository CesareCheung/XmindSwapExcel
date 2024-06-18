# XmindSwapExcel
# Xmind转Excel用例
1.需要修改【平台】、【所属模块】、【相关需求】、【用例类型】、【适用阶段】、【用例状态】、【创建人】字段，可以
  在excelPara.ini文件中修改，对应字段如：
  ‘’‘prodectName=基础平台(#20)
     platform:所有平台(#0)
     modleName:XXX
     caseType:功能测试
     testStatus:功能测试阶段
     caseStatus:正常
     author:创建人’‘’
2.xmind可不设置测试用例优先级，如果没有设置，自动处理成低优先级测试用例
3.xmind编写测试用例需遵循规范，最多只能出现两级子模块
4.子模块的第一个测试用例必须编写测试步骤，非第一个用例可不写测试步骤

# Xmind用例编写模板

![xmind编写模板.jpg](xmind%B1%E0%D0%B4%C4%A3%B0%E5.jpg)


![导出excel模板.png](%B5%BC%B3%F6excel%C4%A3%B0%E5.png)
