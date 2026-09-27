# 常见问题

## 为什么安装名和导入名不同？

当前安装元数据名为 `tumor-heterogeneity`，setuptools 打包的是 `src*`，所以使用 `from src.models import DHIModel`。正式发布拟迁移到 `tumor_heterogeneity`，见 [包设计](package-design.md)，当前不要使用尚未实现的导入路径。

## 为什么分数是 NaN、零或没有输出？

先检查掩膜是否非空、ROI 是否足够大、灰度是否有限、文件是否匹配。接着查看 `features`、`details` 和 CSV 的 `error`。不同模型对过小 ROI 的处理不同；NaN 不应简单替换为零。

## 原始影像可以直接传给 compute 吗？

该接口接收数组，不会读取间距、自动配准或统一分辨率。空间度量模型目前使用单位间距，统一比较时应先准备 1 mm 各向同性数据。CT 和掩膜同形状仍可能对应不同物理空间。

## 预处理出现 OrientImageFilter 错误？

当前 `src/core/preprocess_pipeline.py` 使用 `sitk.OrientImageFilter()`；本地验证所用 SimpleITK 2.5.5 没有该入口。该脚本仍需进行方向 API 兼容修复和真实空间元数据回归验证，不能把 `--help` 通过理解为预处理已通过端到端测试。

此外，当前函数会把 CT 元数据复制给掩膜；这不等同于重采样或配准。首次使用请提供已独立验证、空间一致的预处理图像。本次文档工作没有修改这段算法代码。

## 如何只运行某个模型，并避免自动绘图？

```bash
python run_all_scores.py --dataset demo --models dhi --no-visualize
```

Python 接口则使用 `DHIModel().compute(image, mask)`。

## THI 和 ITH-FS 为什么较慢？

THI 需要逐体素提取局部特征；ITH-FS 需要多尺度特征、近邻图和特征向量计算。ROI 体素数会影响计算与内存成本。先用少量病例验证参数，再执行全队列；当前没有承诺 GPU 加速或病例级并行。

## 三维标签图在哪里？

在提供空间输出的模型 `compute()` 返回值中。批处理为了控制内存只保留表格字段，不会自动导出标签图。

## 是 PyRadiomics 或原版 ITHscore 的等价实现吗？

不是。文档组织参考 PyRadiomics；算法、特征定义和接口应按本项目逐项判断。`ITHscore/` 是独立参考仓库，QuanTAV 的 Python 骨架算法也不能宣称与 MATLAB 原版逐值一致。

## 如何引用和判断许可证？

当前根目录没有正式 `LICENSE` 文件，原 README 中的 MIT 声明不足以替代完整授权文件。正式发布前应补齐主包许可证及第三方代码来源说明；`ITHscore/` 的独立许可不能自动覆盖主包。

当前未提供经过核实的本软件论文条目。研究使用时应记录软件版本、提交和参数，并引用实际使用算法对应的原始文献；不要把原版 ITHscore 的论文当作本仓库所有实现的论文。
