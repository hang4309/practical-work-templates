# Unify the reading, keep its origin

An anonymized implementation note from an AI-assisted industrial data project I participated in. This describes existing architecture, not completed downstream deployment or final site acceptance. No client identity, original source code or actual sensor readings are published.

## The change

The earlier backend organized controllers, services and models separately for different monitoring modules. The refactored version brings readings into a shared model and uses mapping to assign their business module. Latest-value and history queries use that common model; legacy input adapters remain in the code.

Consolidating the data model does not mean every input has equally reliable provenance. The canonical collection entry requires a source file and line number. The legacy adapter explicitly marks records lacking that origin information. It does not manufacture a real file location for them.

Mapping can also remain unassigned when no mapping or payload assignment is available. A populated category is not automatically a correct category; upstream mapping validation still matters.

The upload rate limit accounts for another practical distinction: a vendor application writes batches, so the collector can send short bursts separated by idle periods. The implementation separates sustained rate from burst capacity rather than assuming evenly spaced requests. This is a description of the existing design, not a throughput benchmark or evidence of distributed rate limiting.

## A small illustration

[synthetic-records.json](synthetic-records.json) illustrates two records: one with known file/line origin and one explicitly marked as legacy origin unavailable. Names, IDs, values and the JSON structure are newly authored for explanation. It is not an export of the private schema and not a validated API contract.

When migrating old data, would you let records with incomplete provenance enter the common model with an explicit marker, or hold them separately until that provenance can be recovered? What changes your answer: audit needs, reversibility, downstream calculations, or the cost of delaying migration?

## Limits and possible collaboration

Further project implementation depends on the client's process. It is not being restarted for this article. No final-site, performance, time-saved, safety-certification or customer-outcome claim is made.

For a file-import or interface-mapping problem, a useful starting point is a sanitized example of the input, the expected output and the current failure. Scope and format compatibility should be established before any delivery commitment. Do not post real customer files or credentials in a public issue.

## 中文案例

在一个我参与、通过 AI 协作开发的工业数据采集项目里，早期后端按不同模块分别组织 controller、service 和数据模型。后来重构时，核心调整是把“设备产生的读数”和“读数属于哪个业务模块”分开。

已有重构版本把读数汇入统一模型，业务模块通过映射区分，再提供最新值和历史查询；旧入口在代码中作为兼容层保留。

但统一入口不应把来源也抹平。正式采集入口要求来源文件和行号，缺失时拒绝；兼容旧入口使用明确的兼容标记，不冒充带有真实文件来源的记录。映射及输入都没有给出归属时，可以保留未分配状态，而不是仅为界面完整补一个分类。

另一个取舍是上传节奏。厂商软件按批次写文件，采集请求会短时集中，不能只按平均速率想象负载。已有实现分别设置持续速率和突发容量。

这里只分享现有设计与实现，不代表后续现场工作或最终验收已完成。后续项目实施仍取决于甲方流程。

你的迁移项目中，缺少真实来源信息的旧记录，应进入统一模型并显式标记，还是先隔离、补齐来源再合并？

See [provenance and review limits](PROVENANCE.md). This note is not a runnable system or an independent audit certificate.
