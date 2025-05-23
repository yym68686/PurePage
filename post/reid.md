# Re-ID 综述论文分享

2023.4.26

[PPT链接](./assets/reidoutlook.pdf)

## 1 前言

大家好，接下来我给大家讲述一下这篇 2021 年的 ReID 行人重识别综述文章。

### 背景与应用

行人重识别（Person re-identification）是利用计算机视觉技术判断图像或者视频序列中是否存在特定行人的技术，是一个图像检索的子问题。 任务就是给定一个监控行人图像，检索跨设备下的该行人图像。可以弥补目前固定的摄像头的视觉局限，也可和行人检测/行人跟踪技术结合，也可以广泛应用于智能视频监控、智能安保等领域。

> 多摄像头/跨摄像头问题，跨域问题。在一个数据集合上训练的模型直接应用于另外一个数据集合上的时候，Re-ID 性能会出现大幅度的下降。

## 4 Re-ID 主要研究方向

作者认为 Re-ID 分为五大步骤：

1）数据采集（来源于监控摄像机的原始视频数据）；

2）行人框生成（从视频数据中，通过人工方式或者行人检测或跟踪方式将行人从图中裁切出来，图像中行人将会占据大部分面积）；

3）训练数据标注（包含相机标签和行人标签等其他信息）；

4）重识别模型训练和设计模型（让它从训练数据中尽可能挖掘“如何识别不同行人的隐藏特征表达模式”）；

5）行人检索（将训练好的模型应用到测试场景中，检验该模型的实际效果）。

全文都是围绕以上五个步骤来展开和讨论的。针对以上五个步骤的一些约束条件，文章将 Re-ID 技术分为 Closed-world 和 Open-world 两大子集。

我的理解是 Closed-world 注重于学术研究，是用于研究导向的方法。Open-world 更倾向于解决实际中的开放性问题，考虑更多实际应用中可能遇到的挑战。

Closed-world 可以概括为大家常见的标注完整的有监督的行人重识别方法，Open-world 可以概括为多模态数据，端到端的行人检索，无监督或半监督学习，噪声标注和一些 Open-set 的其他场景。

左图从五个方面对 Closed-world 和 Open-world 涉及到的主要技术进行对比：

1. Closed-world 是单模态的，Open-world 包含了多模态数据，包括：红外图像、素描画、深度图像甚至文本描述。其中一个研究方向就是如何引入和处理多模态信息。
2. closed-world 是用已经做好 bounding boxes 的图片数据进行训练。而 Open-world 大多数就是原始的视频数据和图片数据，如何实现端到端的行人检索是我们需要解决的问题。
3. closed-world 有足够的标注好的数据进行训练，但给每一个摄像头标注数据说非常耗时耗力的，在 Open-world 里没有足够的标签，甚至没有标签。我们在这种情况下如何进行无监督或者半监督学习呢？
4. closed-world 假定所有标注都是对的，但是现实世界存在很多噪声。这个问题催生了对行人重识别中噪声鲁棒性分析的研究。
5. 在 closed-world 里，假定检索的行人一定在检索数据集里面。但在很多场景下，要检索的人很有可能不再检索数据集里。这引导研究者致力于解决开放式人员重识别的问题。

> 从上面的对比中，我们可以了解到 Closed-world 的主要约束一般包含以下假设：
>
> （1）通过图像或视频，可见光（RGB）摄像机捕捉行人；
>
> （2）行人由 bounding boxes 框出；
>
> （3）有足够多的被标注训练数据；
>
> （4）标注的数据标签通常都是正确的；
>
> （5）query person 必须出现在 gallery set 中。

## 5

Closed-world 的研究方向主要分为特征学习，度量学习和排序优化三个部分。研究人员的方法通常针对这三方面进行改进，侧重点不同。有的是提出了新颖的特征学习方法，有的提出有效的度量损失函数，也有的是在测试检索阶段进行优化。

## 6

特征学习方法基本可以分为四种：

1. 全局特征学习，利用全身的全局图像来进行特征学习，常见的改进思路有 Attention 机制，多尺度融合等；
2. 局部特征学习，利用局部图像区域（行人部件或者简单的垂直区域划分）来进行特征学习，并聚合生成最后的行人特征表示；
3. 辅助特征学习，利用一些辅助信息来增强特征学习的效果，如语义信息（比如行人属性等）、视角信息（行人在图像中呈现的不同方位信息）、域信息（比如每一个摄像头下的数据表示一类域）、GAN生成的信息（比如生成行人图像）、数据增强等；
4. 视频特征学习：利用一些视频数据提取时序特征，并且融合多帧图像信息来构建行人特征表达；

## 7

度量学习方法基本可以分为三种。早期的度量学习主要是设计不同类型的距离/相似度度量矩阵。深度学习时代，主要包括不同类型的损失函数的设计及采样策略的改进：

- Identity Loss: 将 Re-ID 的训练过程当成图像分类问题，同一个行人的不同图片当成一个类别，常见的有 Softmax 交叉熵损失函数；
- Verification Loss：将 Re-ID 的训练当成图像匹配问题，是否属于同一个行人来进行二分类学习，常见的有对比损失函数，二分类损失函数；
- Triplet Loss：将 Re-ID 的训练当成图像检索问题，同一个行人图片的特征距离要小于不同行人的特征距离，以及其各种改进；

## 8

用学习好的 Re-ID 特征得到初始的检索排序结果后，利用图片之间的相似性关系来进行初始的检索结果优化，主要包括重排序（re-ranking）和排序融合（rank fusion）等方法。

## 9

通过前面的 Closed-world 和 Open-world 对比，我们可以知道 Open-world 研究主要有以下五种挑战：

1）多模态数据，采集的数据不是单一的可见光模态；

2）端到端的行人检索（End-to-end Person Search）,没有预先检测或跟踪好的行人图片或者视频；

3）无监督和半监督学习，标注数据有限或者无标注的新场景；

4）噪声标注的数据（即使有标注，但是数据采集和标注过程中存在噪声或错误）；

5）一些其他 Open-set 场景，查询行人找不到，群体重识别，动态的多摄像头网络等。

## 11

根据前面综述对研究方向的总结，我选择了一篇属于 Closed-world 领域的问题的经典工作来做讲解，它被发表在了 ECCV 2018 上。它使用一种新的特征学习方法进行局部特征学习。

当时提出的基于人体部件划分的 Re-ID 方法主要有两类：

① 第一类是基于人体姿态估计的方法，这类方法的性能受限于姿态估计和 Re-ID 数据集的偏差，难以得到较好的语义分割；

② 第二类不使用语义分割，不对部件进行定位。

这篇文章的主要贡献：

- 提出PCB网络，基于均匀划分的部分学习网络，不需要进行语义分割即可提取部件特征；
- 提出一种自适应的细化池化方法，refined part pooling（RPP），用来调整出现偏差的部件，增强部件的内部一致性。

骨干网络采用了 ResNet-50 网络，除去隐藏的全连接层。

## 12

在 PCB 模块中，输入图片经过骨干网络，得到张量 T。定义沿着通道方向的激活向量为列向量 f(1x 1x c）。

- 先将张量 T 分为 p 个水平部分，然后使用传统的平均池化，把 p 个水平部分在空间上进行下采样，得到 p 个列向量 gi(i= 1,2,…,p)。
- p 个列向量 gi(i=1,2,...,p) 通过一个 1x1 conv，在通道上降到 256 维，得到 p 个列向量 hi(1×1×256)
- 将每—个向量 hi，输入到一个分类器中，分类器由一个全连接层和一个 softmax 函数构成。

> 训练阶段，最小化 p 个id预测的交叉熵损失函数测试阶段，将g 或h的p个片段拼接起来形成最終描述待，即G= [g1,g2，•.•,gp]或H=h1,h2，…,hp〕。

## 13

由于采用的是强制划分，这导致部件内部信息的不一致性问题。

图中每一个小矩形就是一个列向量 f。

作者计算了每一个列向量 f 和各个部件的特征向量 g 之间的余弦距离，哪个距离最小，就记入那个部件。

完成后，观察到两个现象：

1. 同一个水平部分的大部分列向量聚集在一起
2. 一个水平部分中存在异常值与其他水平部分更相似

## 14

论文最后的实验结果表明：

- PCB 相较于 IDE 的提升表明：整合部分信息，可以提高特征的区分能力。
- RPP 可以进一步提升 PCB 的性能，mAP 相较于 rank-1 的提升更大，表明 RPP 在寻找困难匹配上更有用。

> map比rank-1更能够反映算法的整体表现，因为map不仅考虑了最高精度，还考虑了其他精度的影响。map的提升说明算法在寻找困难匹配上更有用，即算法在处理难以区分的行人图像时，能够更准确地进行匹配，从而提高整体识别精度。

## References

https://www.cnblogs.com/orangecyh/p/12611136.html

https://zhuanlan.zhihu.com/p/90429483

专栏：https://zhuanlan.zhihu.com/personReid

[TPAMI2021 深度学习行人重识别综述与展望](https://zhuanlan.zhihu.com/p/342249413)
