# Mamba 系列全解析与实践

[TOC]

## 状态空间模型

线性时不变系统
$$
x^{\prime} ( t )=\mathbf{A} x ( t )+\mathbf{B} u ( t ) \\
y ( t )=\mathbf{C} x ( t )+\mathbf{D} u ( t )
$$
这是系统的状态方程。ut是输入信号，xt是系统在t时刻的潜在状态。需要算出$x ( t )$确切的表达式，才能通过$y ( t )=\mathbf{C} x ( t )+\mathbf{D} u ( t )$计算出系统在当前状态下的输出。在连续系统下可以通过常微分方程来解决。在离散系统下。使用离散系统的原因在于大语言模型是以token为基础作为一个时间步，并不是一个连续的状态，所以需要对以上的方程做离散化处理。可以使用**双线性变换（Tustin’s method）**的方法计算出x的递归形式。
$$
\begin{aligned} {{x_{k}}} & {{} {{}=\overline{{{{\bf A}}}} x_{k-1}+\overline{{{{\bf B}}}} u_{k}}} \\ 
{{y_{k}}} & {{} {{}=\overline{{{{\bf C}}}} x_{k}}} \\ \end{aligned}
$$
由于D是跳跃连接，为了简化运算，一般省略D。