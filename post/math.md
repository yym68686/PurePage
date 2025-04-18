# 深度学习里面的数学

[TOC]

## 卡方散度

卡方散度用于衡量两个概率分布之间的差异。给定两个概率分布 P 和 Q，其卡方散度定义为：
$$
D_{\chi^2}(P|Q) = \sum_{x \in \text{supp}(Q)} \frac{(P(x) - Q(x))^2}{Q(x)}
$$
其中 $\text{supp}(Q)$ 表示 Q 的支撑集，即 Q(x) > 0 的所有 x 的集合。

## 卡方互信息

卡方互信息 (χ2-mutual information) 是一种衡量两个随机变量之间关联程度的指标，它基于卡方散度 (χ2-divergence)。

对于两个随机变量 X 和 Y，其联合概率分布为 P<sub>XY</sub>，边缘概率分布分别为 P<sub>X</sub> 和 P<sub>Y</sub>，则 X 和 Y 之间的卡方互信息定义为：
$$
I_{\chi^2}(X;Y) = D_{\chi^2}(P_{XY} | P_X \otimes P_Y) = \sum_y D_{\chi^2}(P_{X|Y}(\cdot | y) | P_X(\cdot)) P_Y(y).
$$
**解释:**

- 卡方互信息可以看作是将联合分布 P<sub>XY</sub> 与假设 X 和 Y 独立时的分布 P<sub>X</sub>⊗P<sub>Y</sub> 进行比较。
- 当 X 和 Y 独立时，卡方互信息为 0。
- 卡方互信息越大，说明 X 和 Y 之间的关联

[arXiv:2409.10559](https://arxiv.org/abs/2409.10559)

## KL 散度 (Kullback-Leibler divergence)

**定义:** 给定两个概率分布 P 和 Q，其 KL 散度定义为：
$$
D_{KL}(P|Q) = \sum_{x \in \text{supp}(P)} P(x) \log \frac{P(x)}{Q(x)}.
$$
在公式 $D_{KL}(P||Q) = \sum_{x \in supp(P)} P(x) \log \frac{P(x)}{Q(x)}$ 中，$supp(P)$ 表示概率分布 $P$ 的**支撑集 (support)**。

更具体地说，$supp(P)$ 是指概率分布 $P$ 中所有概率 $P(x)$ 大于 0 的 $x$ 的集合。 换句话说，它是 \(P\) 分布中所有可能出现的结果的集合。

例如：

*   如果 \(P\) 是一个离散型概率分布，描述抛硬币的结果（正面或反面），如果正面朝上的概率是 0.6，反面朝上的概率是 0.4，那么 $supp(P) = \{正面, 反面\}$。
*   如果 \(P\) 是一个连续型概率分布，例如标准正态分布，那么 \(supp(P)\) 是整个实数轴 $\mathbb{R}$，因为正态分布的概率密度函数在任何实数点上都大于 0。
*   如果\(P\)是一个离散型概率分布，其中\(P(x=1) = 0.5, P(x=2)=0.5\)，其他情况\(P(x)=0\), 那么$supp(P) = \{1, 2\}$.

在KL散度的定义中，求和符号 $\sum_{x \in supp(P)}$ 表示只对那些 \(P(x) > 0\) 的 \(x\) 值进行求和。这样做是因为当 \(P(x) = 0\) 时，$P(x) \log \frac{P(x)}{Q(x)}$ 这一项没有定义 (会出现 0 乘以无穷大的情况)。通过限制在支撑集上求和，可以避免这种未定义的情况。

**特点:**

- **对连续型和离散型数据都适用:** KL 散度可以用于连续型和离散型概率分布。
- **对 P 和 Q 的顺序敏感:** D<sub>KL</sub>(P∥Q) ≠ D<sub>KL</sub>(Q∥P)。
- **对 Q 中概率值接近 0 的情况相对不敏感:** 当 Q(x) 接近 0 而 P(x) 不接近 0 时，KL 散度的值会趋于正无穷；但当 P(x) 和 Q(x) 同时接近 0 时，KL 散度的值仍然可以是有限的。
- **Gibbs 不等式**：它总是【非负】的，并且当且仅当 p1(x) 和 p2(x)在每一处都相同时才为 0。为了理解这一点，我们可以将 KL 散度分解为两部分:

$$
\begin{aligned} K L\left(p_1(x), p_2(x)\right) &  =\int p_1(x) \log p_1(x) d x-\int p_1(x) \log p_2(x) d x \\ & =-\int p_1(x) \log p_2(x) d x-\left(-\int p_1(x) \log p_1(x) d x\right)\end{aligned}
$$

第二项带有负号，其对应的是 p1 的信息熵；第一项也带有负号，代表 p1 和 p2 之间的交叉熵。第一项始终不大于每个给定符号下的第二项，这便是 **Gibbs 不等式**；而 Gibbs 不等式的证明可以使用 **Jensen 不等式**：



[一文详解 codebook 技术史（从 VAE 到 VQ/RQ-VAE 到 FSQ） - 翟泽鹏的文章 - 知乎](https://zhuanlan.zhihu.com/p/2433292582)

前向和反向 KL 散度

https://dibyaghosh.com/blog/probability/kldivergence.html

近似 KL 散度

http://joschu.net/blog/kl-approx.html
