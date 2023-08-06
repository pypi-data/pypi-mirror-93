# 标准Readme Python版

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

标准 Readme 样式

README 文件是人们通常最先看到的第一个东西。它应该告诉人们为什么要使用、如何安装、以及如何使用你的代码。README 文件标准化能够使得创建和维护 README 文件更加简单。毕竟，要写好一个文档不是那么容易的。

本仓库包含以下内容：

1. 一个创建标准 README 的[生成器](https://github.com/RichardLitt/generator-standard-readme)的 `Python` 版本。
   (也许它现在还有很多问题,但是它有更多其他强大的功能正在开发中)

## 内容列表

- [背景](#背景)
- [安装](#安装)
- [使用说明](#使用说明)
- [徽章](#徽章)
- [示例](#示例)
- [相关仓库](#相关仓库)
- [维护者](#维护者)
- [如何贡献](#如何贡献)
- [使用许可](#使用许可)

## 背景

如果你的文档是完整的，那么使用你代码的人就不用再去看代码了。这非常的重要。它使得你可以分离接口文档与具体实现。它意味着你可修改实现的代码而保持接口与文档不变。

> 请记住：是文档而非代码，定义了一个模块的功能。

—— [Ken Williams, Perl Hackers](http://mathforum.org/ken/perl_modules.html#document)

写 README 从某种程度上来说相当不易，一直维护下去更是难能可贵。如果可以减少这个过程，则可以让写代码与修改代码更容易，使得是否在说明中指明一处需改有无必要更加清楚，你可以花费更少的时间来考虑是否你最初的文档是否需要更新，你可以分配更多的时间来写代码而非维护文档。

同时，标准化在某些别的地方也有好处。有了标准化，用户就可以花费更少的时间来搜索他们需要的信息，他们同时可以做一个工具来从描述中搜集信息，自动跑示例代码，检查授权协议等等。

这个仓库的目标是：

1. 一个**生成器**用来快速搭建新的 README 的框架。

## 安装

这个项目使用 Python3. 

```sh
$ pip install md2-notfresh
```
> 为什么叫 md2-notfresh 呢? 因为 notfresh 是我的 github ID,而 md 是 markdown 的缩写,所以本来想用 md 作为命令的入口的, 但是因为 md = mkdir,被占用了,所以我用 md2 来表示.
## 使用说明

这是一个 README 生成工具，你可以用它快速生成一个开原仓库的README文档, 当然它本质上说是一个可自定义的 markdown 模板生成工具,更多功能正在开发中。

```sh
使用 md2 -h 来获取帮助
使用 md2 readme 在当前目录生成 README 文件
使用 md2 update-url filename 来更新md文件的网页链接
使用 md2 update-space filename 来更新md文件的英文字母和汉字的空格
# Prints out the standard-readme spec
```

我另外制作了两个命令来做辅助工作, 他们分别是` md2 update-url ` 和 `md2 update-space` , 我现在来简单说一下他们的使用方法.

### 辅助命令用法
- `md2 update-url filename`
如果我们平常喜欢使用 markdown 文档来进行写作, 我想做讨厌的之一是自己写 `[锚文字](实际url)` 了,我们喜欢直接贴一个url, 但是这样的坏处是, 如果这样的 markdown 发表到博客网站, 用户是无法点击的, 只好http复制地址到地址栏, 所以我就写了这样一个命令. 来自动检测并帮助自动更新url
  比如在 a.md 里面的内容是 
```
https://pypi.org/project/md2-notfresh/

```
使用命令 `md2 update-url a.md` 会把它的内容变成

```
[https://pypi.org/project/md2-notfresh/](https://pypi.org/project/md2-notfresh/)

```
如果 url 已经符合规范了, 那么它就不会再次修改了. 所以多次操作是安全的. 它的原理是自动检测 http:// 开头的内容. 我们一般认为 http或者https 开头的都是网址.  

- `md2 update-space filename`
如果我们平常喜欢使用 markdown 文档来进行写作, 我想做讨厌的之一中文和英文字符的空格, 比如`Hello张三`, 我们应该给`张三`和`hello`之间加上空格, 所以这个命令就是自动帮我们完成这件事的.
  
如果汉字和英文已经符合规范了, 那么它就不会再次修改了. 所以多次操作是安全的. 
这个命令请谨慎使用, 确保你真的想在中文和英文中间留一个空格.  

## 徽章
如果你的项目遵循 Standard-Readme 而且项目位于 Github 上，非常希望你能把这个徽章加入你的项目。它可以更多的人访问到这个项目，而且采纳 Stand-README。 加入徽章**并非强制的**。 

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

为了加入徽章到 Markdown 文本里面，可以使用以下代码：

```
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
```

## 示例

想了解我们建议的规范是如何被应用的，请参考 [example-readmes](example-readmes/)。

## 相关仓库

- [Art of Readme](https://github.com/noffle/art-of-readme) — 💌 写高质量 README 的艺术。
- [open-source-template](https://github.com/davidbgk/open-source-template/) — 一个鼓励参与开源的 README 模板。

## 维护者

[@notfresh](https://github.com/notfresh)。

## 如何贡献
直接发我邮箱, notfresh@foxmail.com


标准 Readme 遵循 [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) 行为规范。

### 贡献者

感谢以下参与项目的人：
<a href="graphs/contributors"><img src="https://opencollective.com/standard-readme/contributors.svg?width=890&button=false" /></a>


## 使用许可

[MIT](LICENSE) © notfresh  
