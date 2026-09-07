# The translation reads fine. The order link is empty.

A small, synthetic release-check case for teams maintaining localized messages and transactional email templates. No customer data, real order, production deployment, or paid engagement is represented here.

## Three defects, four findings

| Seeded defect | Observed finding | Correction |
| --- | --- | --- |
| French greeting loses the English `{name}` variable | `TOKEN_MISMATCH` | Restore `{name}` |
| French resources omit the `help` key | `MISSING_KEY` | Add the missing key |
| Email uses `{{tracking_url}}`, but data defines `order_url` | `UNKNOWN_PLACEHOLDER` and `MISSING_RENDER_VALUE` | Use `{{order_url}}` |

The last defect produces two findings. This is not four independent bugs.

The email rendered before correction:

```html
<p>Hello Demo Buyer</p><p><a href="">View order</a></p>
```

After correcting the variable:

```html
<p>Hello Demo Buyer</p><p><a href="https://example.test/orders/DEMO-001">View order</a></p>
```

`example.test` is a synthetic address, not a live order link.

## Inspect the evidence

- [Before inputs](before.json): English/French resources, template, field names and one synthetic sample.
- [After inputs](after.json): the three minimal corrections.
- [Observed result](observed-result.json): sanitized rule records and rendered output from the local experiment.
- [Review checklist](CHECKLIST.md): a reusable handoff checklist.
- [Origin and limits](PROVENANCE.md).

Two local QA engines were run against these newly authored inputs. The localization command rejected the before resources and accepted the after resources. The notification engine produced the empty link before correction and the expected link afterward. Exact rule codes and rendered links were checked in the experiment script. Corrected inputs produced zero findings in this narrow example, without suppressing issues via approval.

**These files are a recorded worked example, not a standalone validator.** The underlying private engines are not included. Reading the JSON does not execute a fresh audit of your files. The local experiment was repeated twice; it covers only three seeded defects, one language pair and one email sample.

## Why check this separately from the wording?

Variables are part of the message contract. A sentence can remain readable after a required variable is removed. Existing tools already check this class of problem: see [Weblate checks](https://docs.weblate.org/en/latest/user/checks.html) and [i18next interpolation](https://www.i18next.com/translation-function/interpolation). This example did not execute either product and does not claim compatibility with their full syntax.

For an actual release, use a checker and renderer compatible with your application's real template engine. Inspect representative rendered output as well as structural findings. Do not infer delivery, link availability or translation accuracy from a clean static check.

## A useful review handoff

Define the actual engine and formats first. A bounded review can then return:

1. A file/key or variable location for each finding.
2. A synthetic reproduction and expected versus actual output.
3. A minimal correction, with content-owner review where meaning changes.
4. A rerun result and explicit exclusions.

Already using Weblate or equivalent checks? Keep them. This case is not a reason to replace a working localization platform.

Feedback is useful when it identifies a concrete gap: a missed variable, an unsupported format, or a confusing report. Use the repository's issue tracker with a **synthetic** example; do not post customer email addresses, secrets, internal URLs or unpublished client text. There is no purchase requirement or automatic service commitment.

## 中文摘要

这是一个新写合成案例：翻译漏变量、资源缺键、邮件变量写错，三个根因得到四条检查记录。错误邮件实际出现空链接；修正后该组样例检查归零，链接恢复正确。可以将检查清单用于交接，但这里不附原始私有检查引擎，不冒充可直接运行的产品，不证明翻译自然度、兼容所有模板引擎或邮件已经送达。
