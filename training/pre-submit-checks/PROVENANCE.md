# 来源与修改说明

本包由AI辅助编写，以六个技术资产记录的检查问题为线索，新写办公场景、题面、数据、答案与课堂安排。没有复制或执行这些项目的程序；内嵌数据及六个CSV均为本包合成，不是客户文件。

|原资产|本包取用的检查思路|
|---|---|
|0293 CSV merge key diagnostics|空键、重复键与多对多理论配对|
|0314 CSV null/default policy|缺失标记和未经批准的默认值|
|0366 CSV currency precision auditor|两位小数与逐笔/总额舍入口径|
|0609 CSV header alias compatibility|预声明表头别名与重复列|
|0770 CSV delimiter sniffing|分隔符与字段内容的区别|
|0771 Excel date serial boundary|日期系统、序号60及空白值|

本包提供的是新的培训材料，不是上游工具发行物。0609没有可据以再分发其代码的MIT通知；本包仅借用通用检查问题，不含它的代码、样例或配置。其他五项记录有MIT通知，但本包也未复制其代码或原样例。后续采用上游实现时应保留相应原始通知。

日期题资料核对自Microsoft官方说明：[Excel日期系统](https://support.microsoft.com/en-us/office/date-systems-in-excel-e7fe7167-48a9-4b96-bb53-5612a800b487)与[1900闰年兼容问题](https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/excel/wrongly-assumes-1900-is-leap-year)。本包不依赖原项目运行结果作为答案。

新写HTML、题面、讲解及合成CSV采用本包LICENSE中的MIT许可，可编辑并用于培训。未验证真实组织的培训效果，没有学员成绩、客户案例或商业收益主张。
